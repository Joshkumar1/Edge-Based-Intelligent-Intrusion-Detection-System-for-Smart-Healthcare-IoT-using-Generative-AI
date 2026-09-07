import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.detection import NetworkPacketInput, DetectionResult
from app.services.ml_engine import ml_engine
from app.services.llm_service import llm_assistant
from app.services.traffic_sim import traffic_simulator
from app.models.device import Device
from app.models.alert import Alert

router = APIRouter()


@router.post("/analyze", response_model=DetectionResult)
async def analyze_packet(packet: NetworkPacketInput, db: Session = Depends(get_db)):
    features = packet.model_dump()
    
    # 1. Run ML Detection Engine
    is_anomaly, anomaly_score, threat_type, confidence, severity, key_features = ml_engine.predict_packet(features)
    
    # 2. Find target device details
    device = db.query(Device).filter(
        (Device.ip_address == packet.dst_ip) | (Device.device_id == "DEV-ICU-101")
    ).first()
    
    target_device_id = device.device_id if device else "DEV-UNKNOWN"
    target_device_name = device.name if device else "Unregistered Medical Device"
    target_device_type = device.category if device else "Medical IoT Gateway"
    location = device.location if device else "ICU Ward"

    explanation, impact, mitigation = None, None, None

    if is_anomaly and threat_type != "Normal":
        # 3. Generate Local LLM Explanation
        explanation, impact, mitigation, _ = await llm_assistant.generate_explanation(
            threat_type=threat_type,
            severity=severity,
            source_ip=packet.src_ip,
            target_device_name=target_device_name,
            target_device_type=target_device_type,
            location=location,
            key_features=key_features
        )

        # 4. Save Alert to Database
        alert_id = f"ALT-{uuid.uuid4().hex[:8].upper()}"
        alert = Alert(
            alert_id=alert_id,
            timestamp=datetime.utcnow(),
            source_ip=packet.src_ip,
            destination_ip=packet.dst_ip,
            target_device_id=target_device_id,
            protocol=packet.protocol,
            anomaly_score=anomaly_score,
            is_anomaly=1,
            threat_type=threat_type,
            confidence=confidence,
            severity=severity,
            key_features=key_features,
            clinical_explanation=explanation,
            clinical_impact=impact,
            recommended_mitigation=mitigation,
            status="NEW"
        )
        db.add(alert)

        # Update Device Risk Score
        if device:
            device.risk_score = min(100.0, device.risk_score + (30.0 if severity == "CRITICAL" else 15.0))
            if severity in ["CRITICAL", "HIGH"]:
                device.status = "Critical" if severity == "CRITICAL" else "Warning"

        db.commit()

    return DetectionResult(
        is_anomaly=is_anomaly,
        anomaly_score=anomaly_score,
        threat_type=threat_type,
        confidence=confidence,
        severity=severity,
        key_features=key_features,
        target_device_id=target_device_id,
        target_device_name=target_device_name,
        explanation=explanation,
        impact=impact,
        mitigation=mitigation
    )


@router.post("/simulate")
async def simulate_packet(attack_type: str = "random", db: Session = Depends(get_db)):
    """Simulates a incoming packet stream event for testing & visual demonstration."""
    force_attack = None if attack_type == "random" else attack_type
    simulated_features = traffic_simulator.generate_packet(force_attack=force_attack)
    
    packet_input = NetworkPacketInput(
        src_ip=simulated_features["src_ip"],
        dst_ip=simulated_features["dst_ip"],
        src_port=simulated_features["src_port"],
        dst_port=simulated_features["dst_port"],
        protocol=simulated_features["protocol"],
        packet_length=simulated_features["packet_length"],
        flow_duration=simulated_features["flow_duration"],
        header_length=simulated_features["header_length"],
        byte_rate=simulated_features["byte_rate"],
        packet_rate=simulated_features["packet_rate"],
        tcp_syn_flag=simulated_features["tcp_syn_flag"],
        mqtt_msg_rate=simulated_features["mqtt_msg_rate"],
        modbus_fn_code=simulated_features["modbus_fn_code"],
        entropy=simulated_features["entropy"]
    )
    
    result = await analyze_packet(packet_input, db)
    return {"simulated_features": simulated_features, "detection_result": result}
