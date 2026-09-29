import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.main import app, seed_initial_data
from app.core.database import Base, engine, SessionLocal
from app.models.device import Device, DeviceStatus
from app.models.machine_signal import MachineSignalLog, ClinicalSafetyInterlock
from app.schemas.machine_signals import (
    MachineSignalInput,
    SignalType,
    SignalIntegrityStatus,
    CyberDefenseMode,
    DefenseActionType,
)
from app.services.machine_signals.cybersecurity_engine import cybersecurity_engine
from app.services.machine_signals.collector_manager import collector_manager

# Initialize test database
Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_initial_data(db)
# Reset test devices to active
for dev_id in ["DEV-PUMP-204", "DEV-VENT-301", "DEV-ICU-101", "DEV-RAD-405", "DEV-SYRINGE-12"]:
    d = db.query(Device).filter(Device.device_id == dev_id).first()
    if d:
        d.status = DeviceStatus.ACTIVE.value
db.query(ClinicalSafetyInterlock).delete()
db.commit()
db.close()

client = TestClient(app)


def test_normal_machine_signal_verified():
    """Valid physiological telemetry from an ICU monitor passes validation."""
    signal = MachineSignalInput(
        device_id="DEV-ICU-101",
        signal_type=SignalType.VITALS,
        seq_num=10,
        payload={
            "heart_rate_bpm": 72.0,
            "spo2_pct": 98.0,
            "systolic_bp": 120.0,
            "diastolic_bp": 80.0
        }
    )
    result = cybersecurity_engine.inspect_and_defend(signal)
    assert result.integrity_status == SignalIntegrityStatus.VERIFIED
    assert result.is_threat is False
    assert result.physical_invariant_breach is False
    assert result.defense_action_taken == DefenseActionType.NONE
    assert result.clinical_safety_interlock is False


def test_infusion_pump_lethal_bolus_overdose_detected_and_isolated():
    """
    Simulating a lethal bolus injection attack (>300 mL/h) on Alaris Infusion Pump.
    Engine must detect PHYSICAL_INVARIANT_BREACH, engage clinical safety interlock,
    and autonomously isolate device in ACTIVE_PREVENTION mode.
    """
    cybersecurity_engine.set_defense_mode(CyberDefenseMode.ACTIVE_PREVENTION, auto_isolate=True, interlocks=True)

    attack_signal = MachineSignalInput(
        device_id="DEV-PUMP-204",
        signal_type=SignalType.INFUSION_TELEMETRY,
        seq_num=20,
        payload={
            "flow_rate_ml_h": 650.0,  # Lethal rate
            "volume_infused_ml": 80.0,
            "occlusion_pressure_psi": 12.0
        }
    )

    result = cybersecurity_engine.inspect_and_defend(attack_signal)
    assert result.integrity_status == SignalIntegrityStatus.PHYSICAL_INVARIANT_BREACH
    assert result.is_threat is True
    assert result.severity == "CRITICAL"
    assert result.physical_invariant_breach is True
    assert result.clinical_safety_interlock is True
    assert result.defense_action_taken == DefenseActionType.FIREWALL_ISOLATE
    assert "Lethal Bolus" in result.threat_type

    # Verify device status is ISOLATED in DB
    db_check = SessionLocal()
    try:
        pump = db_check.query(Device).filter(Device.device_id == "DEV-PUMP-204").first()
        assert pump.status == DeviceStatus.ISOLATED.value

        # Verify ClinicalSafetyInterlock row created
        interlock = db_check.query(ClinicalSafetyInterlock).filter(
            ClinicalSafetyInterlock.device_id == "DEV-PUMP-204",
            ClinicalSafetyInterlock.is_active == True
        ).first()
        assert interlock is not None
        assert "Lethal Bolus" in interlock.reason
    finally:
        db_check.close()


def test_ventilator_barotrauma_hijack_detected():
    """Ventilator peak pressure exceeding 40 cmH2O triggers immediate barotrauma protection."""
    attack_signal = MachineSignalInput(
        device_id="DEV-VENT-301",
        signal_type=SignalType.VENTILATION_PRESSURE,
        seq_num=30,
        payload={
            "peak_inspiratory_pressure_cmH2O": 46.5,  # Dangerous pressure
            "peep_cmH2O": 5.0,
            "respiratory_rate_bpm": 18.0
        }
    )

    result = cybersecurity_engine.inspect_and_defend(attack_signal)
    assert result.integrity_status == SignalIntegrityStatus.PHYSICAL_INVARIANT_BREACH
    assert result.is_threat is True
    assert result.severity == "CRITICAL"
    assert "Barotrauma" in result.threat_type
    assert result.clinical_safety_interlock is True


def test_anti_replay_attack_detection():
    """Stale or non-monotonic sequence numbers must be flagged as replay attacks."""
    cybersecurity_engine.anti_replay_enforcement = True

    # First valid signal
    sig1 = MachineSignalInput(
        device_id="DEV-SYRINGE-12",
        signal_type=SignalType.INFUSION_TELEMETRY,
        seq_num=100,
        payload={"flow_rate_ml_h": 2.0}
    )
    res1 = cybersecurity_engine.inspect_and_defend(sig1)
    assert res1.integrity_status == SignalIntegrityStatus.VERIFIED

    # Replayed signal with stale sequence number (seq_num 100 <= 100)
    sig_replay = MachineSignalInput(
        device_id="DEV-SYRINGE-12",
        signal_type=SignalType.INFUSION_TELEMETRY,
        seq_num=100,
        payload={"flow_rate_ml_h": 2.0}
    )
    res2 = cybersecurity_engine.inspect_and_defend(sig_replay)
    assert res2.integrity_status == SignalIntegrityStatus.REPLAY_ATTACK
    assert res2.is_threat is True
    assert "Replay" in res2.threat_type


def test_sensor_spoofing_physiological_paradox():
    """ICU monitor reporting Asystole (HR=0) with 98% SpO2 detected as sensor deception."""
    sig = MachineSignalInput(
        device_id="DEV-ICU-101",
        signal_type=SignalType.VITALS,
        seq_num=200,
        payload={
            "heart_rate_bpm": 0.0,
            "spo2_pct": 98.5
        }
    )
    result = cybersecurity_engine.inspect_and_defend(sig)
    assert result.integrity_status == SignalIntegrityStatus.PHYSICAL_INVARIANT_BREACH
    assert "Sensor Deception" in result.threat_type


def test_defense_mode_passive_monitor_does_not_quarantine():
    """In PASSIVE_MONITOR mode, threats are logged but NO automated quarantine or interlocks engage."""
    cybersecurity_engine.set_defense_mode(CyberDefenseMode.PASSIVE_MONITOR)

    db_session = SessionLocal()
    try:
        rad = db_session.query(Device).filter(Device.device_id == "DEV-RAD-405").first()
        rad.status = DeviceStatus.ACTIVE.value
        db_session.commit()
    finally:
        db_session.close()

    sig = MachineSignalInput(
        device_id="DEV-RAD-405",
        signal_type=SignalType.DICOM_PACS_STREAM,
        seq_num=300,
        payload={
            "entropy": 7.95,
            "pdu_byte_rate": 35000.0
        }
    )
    result = cybersecurity_engine.inspect_and_defend(sig)
    assert result.defense_action_taken == DefenseActionType.LOG_ALERT
    assert result.clinical_safety_interlock is False

    db_session = SessionLocal()
    try:
        rad = db_session.query(Device).filter(Device.device_id == "DEV-RAD-405").first()
        assert rad.status != DeviceStatus.ISOLATED.value
    finally:
        db_session.close()

    # Reset back to ACTIVE_PREVENTION
    cybersecurity_engine.set_defense_mode(CyberDefenseMode.ACTIVE_PREVENTION)


def test_api_signals_endpoints():
    """Tests the /api/v1/signals REST endpoints."""
    # 1. Get collectors
    res = client.get("/api/v1/signals/collectors")
    assert res.status_code == 200
    collectors = res.json()
    assert len(collectors) >= 3

    # 2. Ingest valid signal
    payload = {
        "device_id": "DEV-ICU-101",
        "signal_type": "VITALS",
        "seq_num": 500,
        "payload": {
            "heart_rate_bpm": 76.0,
            "spo2_pct": 99.0
        }
    }
    ingest_res = client.post("/api/v1/signals/ingest", json=payload)
    assert ingest_res.status_code == 200
    data = ingest_res.json()
    assert data["integrity_status"] == "VERIFIED"

    # 3. Simulate attack via API
    sim_res = client.post("/api/v1/signals/simulate-attack?attack_scenario=infusion_overdose")
    assert sim_res.status_code == 200
    sim_data = sim_res.json()
    assert sim_data["physical_invariant_breach"] is True
    assert sim_data["is_threat"] is True

    # 4. Check active interlocks
    interlocks_res = client.get("/api/v1/signals/interlocks")
    assert interlocks_res.status_code == 200
    interlocks = interlocks_res.json()
    assert any(i["device_id"] == "DEV-PUMP-204" for i in interlocks)

    # 5. Clinician reset of safety interlock
    reset_res = client.post("/api/v1/signals/interlocks/DEV-PUMP-204/reset?clinician_name=Dr.+Test")
    assert reset_res.status_code == 200
    assert reset_res.json()["status"] == "RESET_CONFIRMED"

    # 6. Get metrics
    metrics_res = client.get("/api/v1/signals/metrics")
    assert metrics_res.status_code == 200
    metrics_data = metrics_res.json()
    assert metrics_data["total_signals_processed"] > 0
    assert metrics_data["total_breaches_detected"] > 0
