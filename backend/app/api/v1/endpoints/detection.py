from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.detection import NetworkPacketInput, DetectionResult
from app.schemas.security_event import TrafficOrigin
from app.services.security_pipeline import security_pipeline
from app.services.traffic_sim import traffic_simulator

router = APIRouter()


@router.post("/analyze", response_model=DetectionResult)
def analyze_packet(packet: NetworkPacketInput, db: Session = Depends(get_db)):
    """
    Thin transport endpoint for edge packet analysis.
    Validates payload and delegates directly to the Canonical Security Pipeline.
    Non-blocking: ML detection executes in sub-5ms; LLM explainability runs asynchronously.
    """
    origin = TrafficOrigin(packet.traffic_origin) if packet.traffic_origin else TrafficOrigin.LIVE
    
    # Ingest through canonical pipeline
    event = security_pipeline.ingest(telemetry=packet, origin=origin, db=db)

    return DetectionResult(
        is_anomaly=event.anomaly_detected,
        anomaly_score=event.anomaly_score,
        threat_type=event.threat_type,
        confidence=event.classifier_confidence,
        severity=event.severity,
        key_features=event.extracted_features,
        target_device_id=event.device_id,
        target_device_name=event.device_name,
        explanation=event.explanation,
        impact=event.clinical_impact,
        mitigation=event.recommended_mitigation,
        event_id=event.event_id,
        correlation_id=event.correlation_id,
        observation_type=event.observation_type.value,
        device_match_status=event.device_match_status.value,
        traffic_origin=event.source.value,
        explanation_status=event.explanation_status.value,
        detection_latency_ms=event.latency_metrics.total_detection_ms,
        ai_explanation_latency_ms=event.latency_metrics.ai_explanation_ms,
        alert_id=event.alert_id,
        packet_count=event.packet_count
    )


@router.post("/simulate")
def simulate_packet(attack_type: str = "random", db: Session = Depends(get_db)):
    """
    Simulates an incoming packet stream event.
    Explicitly marked with source = SIMULATOR and processed through the Canonical Security Pipeline.
    """
    force_attack = None if attack_type == "random" else attack_type
    simulated_features = traffic_simulator.generate_packet(force_attack=force_attack)
    
    # Process through the exact same canonical pipeline with SIMULATOR provenance
    event = security_pipeline.ingest(
        telemetry=simulated_features,
        origin=TrafficOrigin.SIMULATOR,
        db=db
    )

    detection_result = DetectionResult(
        is_anomaly=event.anomaly_detected,
        anomaly_score=event.anomaly_score,
        threat_type=event.threat_type,
        confidence=event.classifier_confidence,
        severity=event.severity,
        key_features=event.extracted_features,
        target_device_id=event.device_id,
        target_device_name=event.device_name,
        explanation=event.explanation,
        impact=event.clinical_impact,
        mitigation=event.recommended_mitigation,
        event_id=event.event_id,
        correlation_id=event.correlation_id,
        observation_type=event.observation_type.value,
        device_match_status=event.device_match_status.value,
        traffic_origin=event.source.value,
        explanation_status=event.explanation_status.value,
        detection_latency_ms=event.latency_metrics.total_detection_ms,
        ai_explanation_latency_ms=event.latency_metrics.ai_explanation_ms,
        alert_id=event.alert_id,
        packet_count=event.packet_count
    )

    return {
        "simulated_features": simulated_features,
        "detection_result": detection_result,
        "traffic_origin": "SIMULATOR",
        "event_id": event.event_id,
        "alert_id": event.alert_id
    }
