from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.machine_signal import MachineSignalLog, ClinicalSafetyInterlock
from app.models.device import Device, DeviceStatus
from app.schemas.machine_signals import (
    MachineSignalInput,
    MachineSignalAnalysisResult,
    CollectorStatus,
    DefensePolicyConfig,
    CyberDefenseMode,
    SignalType,
)
from app.services.machine_signals.cybersecurity_engine import cybersecurity_engine
from app.services.machine_signals.collector_manager import collector_manager

router = APIRouter()


@router.get("/collectors", response_model=List[CollectorStatus])
def get_collectors():
    """Returns active physical machine signal collectors and status."""
    return collector_manager.get_collectors()


@router.post("/collectors/{collector_id}/toggle", response_model=CollectorStatus)
def toggle_collector(collector_id: str):
    """Starts or pauses an edge machine signal collector."""
    try:
        return collector_manager.toggle_collector(collector_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.post("/ingest", response_model=MachineSignalAnalysisResult)
def ingest_machine_signal(signal: MachineSignalInput, db: Session = Depends(get_db)):
    """
    Direct Machine Signal Ingestion Endpoint.
    Directly ingests physical/telemetry signal frames from medical equipment or bedside edge nodes.
    Validates anti-replay sequence, checks physiological invariants, performs dual-stage ML detection,
    and applies automated zero-trust cyber defense actions.
    """
    result = cybersecurity_engine.inspect_and_defend(signal=signal, db=db)
    collector_manager.record_received("REST_EDGE_INGEST", rejected=result.is_threat)
    return result


@router.get("/live")
def get_live_machine_signals():
    """Returns the most recent physiological and telemetry signal snapshot for all connected medical machines."""
    return collector_manager.get_latest_signals()


@router.get("/history")
def get_signal_history(
    limit: int = Query(50, ge=1, le=500),
    device_id: Optional[str] = None,
    threats_only: bool = False,
    db: Session = Depends(get_db)
):
    """Retrieves recent signal audit history, integrity verdicts, and cyber defense actions."""
    query = db.query(MachineSignalLog)
    if device_id:
        query = query.filter(MachineSignalLog.device_id == device_id)
    if threats_only:
        query = query.filter(MachineSignalLog.is_threat == 1)

    records = query.order_by(MachineSignalLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "signal_id": r.signal_id,
            "device_id": r.device_id,
            "timestamp": r.timestamp.isoformat() + "Z" if r.timestamp else None,
            "signal_type": r.signal_type,
            "seq_num": r.seq_num,
            "integrity_status": r.integrity_status,
            "physical_invariant_breach": bool(r.physical_invariant_breach),
            "breach_details": r.breach_details,
            "anomaly_score": r.anomaly_score,
            "is_threat": bool(r.is_threat),
            "threat_type": r.threat_type,
            "severity": r.severity,
            "defense_action": r.defense_action,
            "clinical_interlock": bool(r.clinical_interlock),
            "payload": r.get_payload(),
            "alert_id": r.alert_id
        }
        for r in records
    ]


@router.get("/defense-policy", response_model=DefensePolicyConfig)
def get_defense_policy():
    """Retrieves current active cyber defense mode and security policy parameters."""
    return DefensePolicyConfig(
        mode=cybersecurity_engine.defense_mode,
        auto_isolate_critical=cybersecurity_engine.auto_isolate_critical,
        engage_safety_interlocks=cybersecurity_engine.engage_safety_interlocks,
        anti_replay_enforcement=cybersecurity_engine.anti_replay_enforcement
    )


@router.put("/defense-policy", response_model=DefensePolicyConfig)
def update_defense_policy(policy: DefensePolicyConfig):
    """Updates cyber defense mode: PASSIVE_MONITOR, ASSISTED_DEFENSE, or ACTIVE_PREVENTION."""
    cybersecurity_engine.set_defense_mode(
        mode=policy.mode,
        auto_isolate=policy.auto_isolate_critical,
        interlocks=policy.engage_safety_interlocks
    )
    cybersecurity_engine.anti_replay_enforcement = policy.anti_replay_enforcement
    return policy


@router.post("/simulate-attack", response_model=MachineSignalAnalysisResult)
def simulate_machine_attack(
    attack_scenario: str = Query(
        "infusion_overdose",
        description="Scenario: 'infusion_overdose', 'ventilator_barotrauma', 'sensor_spoofing', 'replay_attack', 'dicom_ransomware', 'scada_tamper'"
    ),
    device_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Direct Attack Signal Injection Tester.
    Transmits an authentic physical or protocol exploit signal directly to a machine
    to verify real-time physical invariant detection and automated zero-trust cyber defense.
    """
    if attack_scenario == "infusion_overdose":
        target_device = device_id or "DEV-PUMP-204"
        signal = MachineSignalInput(
            device_id=target_device,
            signal_type=SignalType.INFUSION_TELEMETRY,
            seq_num=collector_manager._get_next_seq(target_device),
            payload={
                "flow_rate_ml_h": 650.0,  # Lethal dose (>300 mL/h)
                "volume_infused_ml": 85.0,
                "bolus_status": "FORCED_OVERRIDE",
                "occlusion_pressure_psi": 18.5
            },
            network_meta={"protocol": "MQTT", "dst_port": 1883}
        )
    elif attack_scenario == "ventilator_barotrauma":
        target_device = device_id or "DEV-VENT-301"
        signal = MachineSignalInput(
            device_id=target_device,
            signal_type=SignalType.VENTILATION_PRESSURE,
            seq_num=collector_manager._get_next_seq(target_device),
            payload={
                "peak_inspiratory_pressure_cmH2O": 48.0,  # Barotrauma danger (>40 cmH2O)
                "peep_cmH2O": 1.2,                       # Alveolar collapse danger
                "respiratory_rate_bpm": 45.0,
                "tidal_volume_ml": 950.0
            },
            network_meta={"protocol": "MODBUS", "dst_port": 502}
        )
    elif attack_scenario == "sensor_spoofing":
        target_device = device_id or "DEV-ICU-101"
        signal = MachineSignalInput(
            device_id=target_device,
            signal_type=SignalType.VITALS,
            seq_num=collector_manager._get_next_seq(target_device),
            payload={
                "heart_rate_bpm": 0.0,   # Asystole deception
                "spo2_pct": 98.8,        # Normal pulse oximetry = physiological paradox
                "systolic_bp": 120.0,
                "diastolic_bp": 80.0
            },
            network_meta={"protocol": "TCP", "dst_port": 8080}
        )
    elif attack_scenario == "replay_attack":
        target_device = device_id or "DEV-SYRINGE-12"
        # Stale/replayed sequence number
        signal = MachineSignalInput(
            device_id=target_device,
            signal_type=SignalType.INFUSION_TELEMETRY,
            seq_num=1,  # Stale sequence number
            payload={
                "flow_rate_ml_h": 2.5,
                "volume_infused_ml": 10.0,
                "occlusion_pressure_psi": 2.1
            },
            network_meta={"protocol": "MQTT", "dst_port": 1883}
        )
    elif attack_scenario == "dicom_ransomware":
        target_device = device_id or "DEV-RAD-405"
        signal = MachineSignalInput(
            device_id=target_device,
            signal_type=SignalType.DICOM_PACS_STREAM,
            seq_num=collector_manager._get_next_seq(target_device),
            payload={
                "modality": "CT",
                "study_uid": "1.2.840.113619.999.ATTACK",
                "entropy": 7.92,
                "pdu_byte_rate": 31000.0,
                "slice_count": 512
            },
            network_meta={"protocol": "DICOM", "dst_port": 104, "packet_length": 1450.0}
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unknown attack scenario: {attack_scenario}")

    return cybersecurity_engine.inspect_and_defend(signal, db=db)


@router.get("/interlocks")
def get_clinical_interlocks(db: Session = Depends(get_db)):
    """Retrieves all active Clinical Safety Interlocks engaged by cyber defense."""
    interlocks = db.query(ClinicalSafetyInterlock).filter(ClinicalSafetyInterlock.is_active == True).all()
    return [
        {
            "id": i.id,
            "device_id": i.device_id,
            "engaged_at": i.engaged_at.isoformat() + "Z" if i.engaged_at else None,
            "reason": i.reason,
            "trigger_signal_id": i.trigger_signal_id,
            "safe_state_mode": i.safe_state_mode,
            "is_active": i.is_active
        }
        for i in interlocks
    ]


@router.post("/interlocks/{device_id}/reset")
def reset_clinical_interlock(
    device_id: str,
    clinician_name: str = Query("Dr. Lead Biomedical Engineer"),
    db: Session = Depends(get_db)
):
    """
    Clinician Override: Clears the safety interlock and reconnects the medical device
    after bedside physical inspection confirms patient safety.
    """
    interlock = db.query(ClinicalSafetyInterlock).filter(
        ClinicalSafetyInterlock.device_id == device_id,
        ClinicalSafetyInterlock.is_active == True
    ).first()

    if not interlock:
        raise HTTPException(status_code=404, detail=f"No active safety interlock found for {device_id}")

    interlock.is_active = False
    interlock.resolved_at = datetime.utcnow()
    interlock.acknowledged_by = clinician_name

    # Reset device status back to Active
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if device and device.status == DeviceStatus.ISOLATED.value:
        device.status = DeviceStatus.ACTIVE.value

    db.commit()
    return {
        "status": "RESET_CONFIRMED",
        "device_id": device_id,
        "acknowledged_by": clinician_name,
        "message": f"Clinical safety interlock for {device_id} successfully cleared. Device returned to active status."
    }


@router.get("/metrics")
def get_cybersecurity_metrics():
    """Returns aggregate cyber defense metrics and signal counters."""
    return {
        "total_signals_processed": cybersecurity_engine.total_signals_processed,
        "total_breaches_detected": cybersecurity_engine.total_breaches_detected,
        "total_replay_attacks_blocked": cybersecurity_engine.total_replay_attacks_blocked,
        "total_interlocks_engaged": cybersecurity_engine.total_interlocks_engaged,
        "total_quarantines_enforced": cybersecurity_engine.total_quarantines_enforced,
        "current_defense_mode": cybersecurity_engine.defense_mode.value,
        "auto_isolate_active": cybersecurity_engine.auto_isolate_critical,
        "anti_replay_enforcement": cybersecurity_engine.anti_replay_enforcement
    }
