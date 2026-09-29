import asyncio
import time
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from app.core.database import SessionLocal
from app.models.alert import Alert
from app.schemas.security_event import SecurityEvent, ExplanationStatus
from app.services.llm_service import llm_assistant
from app.websockets.stream_manager import manager

logger = logging.getLogger("edgeshield.ai_enricher")


class AIEnrichmentService:
    """
    Decoupled Asynchronous AI Explainability Worker.
    Ensures the edge ML detection pipeline is never blocked by LLM execution.
    Executes in background, updates database state, and broadcasts real-time enrichment via WebSockets.
    """

    async def enrich_security_event(self, event_dict: Dict[str, Any], alert_id: Optional[str] = None):
        """
        Background task: Enriches a security event / alert with clinical impact and mitigation advice.
        Handles Ollama availability truthfully:
        - Ollama Online -> explanation_status = COMPLETED
        - Ollama Offline/Timeout -> explanation_status = UNAVAILABLE (with deterministic fallback text)
        - Unhandled Exception -> explanation_status = FAILED
        """
        t_start = time.perf_counter()
        
        event_id = event_dict.get("event_id", "")
        correlation_id = event_dict.get("correlation_id", "")
        threat_type = event_dict.get("threat_type", "Unknown Anomaly")
        severity = event_dict.get("severity", "MEDIUM")
        source_ip = event_dict.get("source_ip", "0.0.0.0")
        target_device_name = event_dict.get("device_name") or "Unregistered Medical Device"
        target_device_type = event_dict.get("device_category") or "Medical IoT Device"
        location = event_dict.get("device_location") or "Hospital Facility"
        key_features = event_dict.get("extracted_features", {})

        # Transition state: GENERATING
        db = SessionLocal()
        try:
            if alert_id:
                alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
                if alert:
                    alert.explanation_status = ExplanationStatus.GENERATING.value
                    db.commit()
        except Exception as e:
            logger.warning(f"Failed to set GENERATING state on alert {alert_id}: {e}")
        finally:
            db.close()

        # Execute LLM generation independently from edge detection
        explanation = None
        impact = None
        mitigation = None
        engine_used = None
        explanation_status = ExplanationStatus.PENDING

        try:
            explanation, impact, mitigation, engine_used = await llm_assistant.generate_explanation(
                threat_type=threat_type,
                severity=severity,
                source_ip=source_ip,
                target_device_name=target_device_name,
                target_device_type=target_device_type,
                location=location,
                key_features=key_features
            )
            
            # Truthful AI state distinction
            if "Ollama" in engine_used:
                explanation_status = ExplanationStatus.COMPLETED
            else:
                # Ollama was offline/unreachable; fallback engine was utilized
                explanation_status = ExplanationStatus.UNAVAILABLE

        except Exception as e:
            logger.error(f"Error executing AI explainability for event {event_id}: {e}")
            explanation_status = ExplanationStatus.FAILED
            explanation = "AI explanation service encountered an internal failure."
            impact = "Operational assessment unavailable."
            mitigation = "Follow standard emergency hospital IoT incident response protocols."
            engine_used = "Failure Handler"

        t_end = time.perf_counter()
        ai_latency_ms = round((t_end - t_start) * 1000.0, 2)

        # Update persisted Alert state in database
        db = SessionLocal()
        try:
            if alert_id:
                alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
                if alert:
                    alert.clinical_explanation = explanation
                    alert.clinical_impact = impact
                    alert.recommended_mitigation = mitigation
                    alert.explanation_status = explanation_status.value
                    alert.ai_latency_ms = ai_latency_ms
                    db.commit()
                    db.refresh(alert)
                    logger.info(
                        f"[AI-Enrichment] Event {event_id} | Alert {alert_id} | "
                        f"Status: {explanation_status.value} | Latency: {ai_latency_ms} ms | Engine: {engine_used}"
                    )
        except Exception as e:
            logger.error(f"Failed to update alert {alert_id} with AI explanation: {e}")
            db.rollback()
        finally:
            db.close()

        # Broadcast real-time AI enrichment update via WebSocket
        try:
            enrichment_payload = {
                "alert_id": alert_id,
                "event_id": event_id,
                "correlation_id": correlation_id,
                "explanation_status": explanation_status.value,
                "clinical_explanation": explanation,
                "clinical_impact": impact,
                "recommended_mitigation": mitigation,
                "ai_engine_used": engine_used,
                "ai_latency_ms": ai_latency_ms,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            await manager.broadcast_envelope(
                event_type="ai_enrichment",
                event_id=event_id,
                correlation_id=correlation_id,
                payload=enrichment_payload
            )
            
            # Also broadcast alert_updated envelope for alert center UI
            if alert_id:
                await manager.broadcast_envelope(
                    event_type="alert_updated",
                    event_id=event_id,
                    correlation_id=correlation_id,
                    payload=enrichment_payload
                )
        except Exception as e:
            logger.warning(f"Failed to broadcast AI enrichment for event {event_id}: {e}")

    def schedule_enrichment(self, event_dict: Dict[str, Any], alert_id: Optional[str] = None):
        """Dispatches enrichment as a non-blocking background task."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.enrich_security_event(event_dict, alert_id=alert_id))
        except RuntimeError:
            import threading
            def _runner():
                try:
                    asyncio.run(self.enrich_security_event(event_dict, alert_id=alert_id))
                except Exception as e:
                    logger.debug(f"Background thread enrichment error: {e}")
            t = threading.Thread(target=_runner, daemon=True)
            t.start()



ai_enricher = AIEnrichmentService()
