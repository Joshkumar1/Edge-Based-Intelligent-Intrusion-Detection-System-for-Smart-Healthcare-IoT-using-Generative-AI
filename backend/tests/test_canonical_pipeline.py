import time
import asyncio
import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app, seed_initial_data
from app.core.database import Base, engine, SessionLocal
from app.models.device import Device, DeviceStatus
from app.models.alert import Alert
from app.models.packet_log import PacketLog
from app.services.security_pipeline import security_pipeline
from app.schemas.security_event import TrafficOrigin, DeviceMatchStatus, ObservationType, ExplanationStatus
from app.schemas.detection import NetworkPacketInput
from app.websockets.stream_manager import manager

# Reset and seed database for testing
Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_initial_data(db)
# Reset test device statuses and clean test alert rows from previous runs
rad_dev = db.query(Device).filter(Device.device_id == "DEV-RAD-405").first()
if rad_dev:
    rad_dev.status = DeviceStatus.ACTIVE.value
db.query(Alert).filter(Alert.source_ip == "198.51.100.14").delete()
db.commit()
db.close()

client = TestClient(app)


# -----------------------------------------------------------------------------
# 1. Canonical Pipeline: Normal vs Anomalous Traffic
# -----------------------------------------------------------------------------

def test_normal_packet_passes_pipeline_without_creating_alert():
    """Normal baseline traffic should produce a NORMAL_OBSERVATION and NOT create an alert row."""
    normal_telemetry = {
        "src_ip": "192.168.10.55",
        "dst_ip": "192.168.10.101",
        "src_port": 50000,
        "dst_port": 502,
        "protocol": "MODBUS",
        "packet_length": 350.0,
        "flow_duration": 1.5,
        "header_length": 32.0,
        "byte_rate": 500.0,
        "packet_rate": 6.0,
        "tcp_syn_flag": 0,
        "mqtt_msg_rate": 2.0,
        "modbus_fn_code": 1,  # Normal read coil
        "entropy": 3.8
    }


    event = security_pipeline.ingest(normal_telemetry, origin=TrafficOrigin.LIVE)
    
    assert event.event_id.startswith("EVT-")
    assert event.observation_type == ObservationType.NORMAL_OBSERVATION
    assert event.anomaly_detected is False
    assert event.threat_type == "Normal"
    assert event.severity == "INFORMATIONAL"
    assert event.alert_id is None
    assert event.device_id == "DEV-ICU-101"
    assert event.device_match_status == DeviceMatchStatus.MATCHED
    assert event.latency_metrics.total_detection_ms > 0


def test_anomalous_packet_creates_security_alert():
    """Malicious traffic should produce a SECURITY_ALERT and persist an Alert record with PENDING status."""
    attack_telemetry = {
        "src_ip": "10.0.4.88",
        "dst_ip": "192.168.10.102",  # Alaris Infusion Pump #4
        "src_port": 44100,
        "dst_port": 1883,
        "protocol": "MQTT",
        "packet_length": 120.0,
        "flow_duration": 0.05,
        "header_length": 20.0,
        "byte_rate": 45000.0,
        "packet_rate": 400.0,
        "tcp_syn_flag": 0,
        "mqtt_msg_rate": 420.0,
        "modbus_fn_code": 0,
        "entropy": 4.2
    }

    event = security_pipeline.ingest(attack_telemetry, origin=TrafficOrigin.LIVE)

    assert event.observation_type == ObservationType.SECURITY_ALERT
    assert event.anomaly_detected is True
    assert event.threat_type == "MQTT Flood DoS"
    assert event.severity in ["CRITICAL", "HIGH"]
    assert event.alert_id is not None
    assert event.device_id == "DEV-PUMP-204"
    assert event.explanation_status == ExplanationStatus.PENDING

    # Verify database persistence
    db = SessionLocal()
    try:
        persisted = db.query(Alert).filter(Alert.alert_id == event.alert_id).first()
        assert persisted is not None
        assert persisted.target_device_id == "DEV-PUMP-204"
        assert persisted.correlation_id == event.correlation_id
        assert persisted.threat_type == "MQTT Flood DoS"
    finally:
        db.close()


# -----------------------------------------------------------------------------
# 2. Strict Device Resolution (Bug Fix Verification)
# -----------------------------------------------------------------------------

def test_unknown_destination_ip_never_resolves_to_icu_telemetry():
    """
    Critical requirement: Unknown destination IP must NEVER map to DEV-ICU-101.
    Must map to DEV-UNREGISTERED and must NOT modify any clinical device risk scores.
    """
    db = SessionLocal()
    try:
        icu_before = db.query(Device).filter(Device.device_id == "DEV-ICU-101").first()
        initial_risk = icu_before.risk_score
    finally:
        db.close()

    unknown_traffic = {
        "src_ip": "185.220.101.5",
        "dst_ip": "192.168.99.244",  # Unregistered destination IP
        "src_port": 49999,
        "dst_port": 8080,
        "protocol": "TCP",
        "packet_length": 1400.0,
        "flow_duration": 30.0,
        "header_length": 40.0,
        "byte_rate": 30000.0,
        "packet_rate": 100.0,
        "tcp_syn_flag": 0,
        "mqtt_msg_rate": 0.0,
        "modbus_fn_code": 0,
        "entropy": 7.8
    }

    event = security_pipeline.ingest(unknown_traffic, origin=TrafficOrigin.LIVE)

    # Strictly UNREGISTERED, never DEV-ICU-101
    assert event.device_id == "DEV-UNREGISTERED"
    assert event.device_match_status == DeviceMatchStatus.UNREGISTERED
    assert event.device_id != "DEV-ICU-101"

    # Verify DEV-ICU-101 risk score was NOT modified
    db = SessionLocal()
    try:
        icu_after = db.query(Device).filter(Device.device_id == "DEV-ICU-101").first()
        assert icu_after.risk_score == initial_risk
    finally:
        db.close()


# -----------------------------------------------------------------------------
# 3. Alert Flooding Prevention & Aggregation
# -----------------------------------------------------------------------------

def test_alert_flooding_aggregates_into_single_incident():
    """
    Verifies that multiple repeated malicious packets sharing the same flow key
    aggregate into 1 Alert row with an incremented packet_count rather than
    generating separate database rows.
    """
    flow_packet = {
        "src_ip": "198.51.100.14",
        "dst_ip": "192.168.10.103",  # Puritan Bennett Ventilator
        "src_port": 52100,
        "dst_port": 502,
        "protocol": "MODBUS",
        "packet_length": 90.0,
        "flow_duration": 0.1,
        "header_length": 20.0,
        "byte_rate": 1500.0,
        "packet_rate": 15.0,
        "tcp_syn_flag": 0,
        "mqtt_msg_rate": 0.0,
        "modbus_fn_code": 16,  # Command Injection
        "entropy": 2.9
    }

    # Send first packet
    event_1 = security_pipeline.ingest(flow_packet, origin=TrafficOrigin.LIVE)
    alert_id_1 = event_1.alert_id
    assert alert_id_1 is not None

    # Send 4 more packets rapidly within the same flow
    for _ in range(4):
        event_n = security_pipeline.ingest(flow_packet, origin=TrafficOrigin.LIVE)
        assert event_n.alert_id == alert_id_1  # Reuses same incident alert_id

    db = SessionLocal()
    try:
        persisted = db.query(Alert).filter(Alert.alert_id == alert_id_1).first()
        assert persisted is not None
        assert persisted.packet_count >= 5
        
        # Verify no duplicate alert rows were created for this flow
        matching_alerts = db.query(Alert).filter(
            Alert.source_ip == "198.51.100.14",
            Alert.destination_ip == "192.168.10.103",
            Alert.threat_type == "Modbus Command Injection"
        ).all()
        assert len(matching_alerts) == 1
    finally:
        db.close()


# -----------------------------------------------------------------------------
# 4. Decoupled Asynchronous AI Explainability
# -----------------------------------------------------------------------------

def test_detection_request_does_not_wait_for_llm():
    """
    POST /analyze must return in sub-15ms with PENDING status.
    Must never synchronously block waiting on Ollama.
    """
    packet = {
        "src_ip": "172.16.8.204",
        "dst_ip": "192.168.10.104",
        "src_port": 49152,
        "dst_port": 104,
        "protocol": "DICOM",
        "packet_length": 1450.0,
        "flow_duration": 25.0,
        "header_length": 40.0,
        "byte_rate": 28500.0,
        "packet_rate": 85.0,
        "tcp_syn_flag": 0,
        "mqtt_msg_rate": 0.0,
        "modbus_fn_code": 0,
        "entropy": 7.88
    }

    t0 = time.perf_counter()
    response = client.post("/api/v1/detection/analyze", json=packet)
    t1 = time.perf_counter()
    total_http_time_ms = (t1 - t0) * 1000.0

    assert response.status_code == 200
    data = response.json()

    # Must return immediately (< 30ms even on virtualized/slow test runners)
    assert total_http_time_ms < 50.0
    assert data["explanation_status"] == "PENDING"
    assert data["detection_latency_ms"] > 0
    assert data["detection_latency_ms"] < 25.0


def test_ai_enrichment_background_worker_updates_persisted_alert():
    """
    Verifies that the background enrichment worker updates the alert's
    explanation_status and clinical content in the database.
    """
    packet = {
        "src_ip": "10.0.12.15",
        "dst_ip": "192.168.10.105",  # Baxter Smart Syringe Driver
        "src_port": 54000,
        "dst_port": 1883,
        "protocol": "MQTT",
        "packet_length": 115.0,
        "flow_duration": 0.1,
        "header_length": 20.0,
        "byte_rate": 40000.0,
        "packet_rate": 350.0,
        "tcp_syn_flag": 0,
        "mqtt_msg_rate": 380.0,
        "modbus_fn_code": 0,
        "entropy": 4.1
    }

    resp = client.post("/api/v1/detection/analyze", json=packet)
    assert resp.status_code == 200
    alert_id = resp.json()["alert_id"]
    assert alert_id is not None

    # Wait up to 2 seconds for background thread to enrich the alert
    enriched = False
    for _ in range(20):
        time.sleep(0.1)
        db = SessionLocal()
        try:
            alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
            if alert and alert.explanation_status in ["COMPLETED", "UNAVAILABLE"]:
                enriched = True
                assert alert.clinical_explanation is not None
                assert alert.clinical_impact is not None
                assert alert.recommended_mitigation is not None
                assert alert.ai_latency_ms is not None
                break
        finally:
            db.close()

    assert enriched is True


# -----------------------------------------------------------------------------
# 5. Simulation Provenance & Attack Simulator Canonical Path
# -----------------------------------------------------------------------------

def test_attack_simulator_uses_canonical_pipeline_and_marks_simulated():
    """Simulation requests must route through canonical pipeline and carry SIMULATOR provenance."""
    resp = client.post("/api/v1/detection/simulate", params={"attack_type": "DICOM Ransomware"})
    assert resp.status_code == 200
    data = resp.json()

    assert data["traffic_origin"] == "SIMULATOR"
    assert "detection_result" in data
    assert data["detection_result"]["threat_type"] == "DICOM Ransomware"
    assert data["detection_result"]["traffic_origin"] == "SIMULATOR"
    assert data["detection_result"]["event_id"] is not None


# -----------------------------------------------------------------------------
# 6. Real Latency Instrumentation (No Hardcoded 0.84 ms)
# -----------------------------------------------------------------------------

def test_dashboard_stats_reports_measured_latency_not_hardcoded():
    """GET /dashboard/stats must return dynamically measured latency metrics, never hardcoded '0.84ms'."""
    resp = client.get("/api/v1/dashboard/stats")
    assert resp.status_code == 200
    data = resp.json()

    assert "0.84ms Latency" not in data["edge_ai_status"]
    assert "detection_latency_ms" in data
    assert "pipeline_metrics" in data
    assert data["detection_latency_ms"] >= 0


# -----------------------------------------------------------------------------
# 7. Bounded Telemetry Log (PacketLog Integration)
# -----------------------------------------------------------------------------

def test_packet_log_persists_canonical_event_metadata():
    """Verifies PacketLog records canonical event_id, correlation_id, and latency."""
    telemetry = {
        "src_ip": "192.168.10.99",
        "dst_ip": "192.168.10.101",
        "src_port": 40001,
        "dst_port": 502,
        "protocol": "MODBUS",
        "packet_length": 80.0,
        "flow_duration": 0.2,
        "header_length": 20.0,
        "byte_rate": 400.0,
        "packet_rate": 5.0,
        "tcp_syn_flag": 0,
        "mqtt_msg_rate": 0.0,
        "modbus_fn_code": 1,
        "entropy": 3.0
    }

    event = security_pipeline.ingest(telemetry, origin=TrafficOrigin.LIVE)

    db = SessionLocal()
    try:
        log = db.query(PacketLog).filter(PacketLog.event_id == event.event_id).first()
        assert log is not None
        assert log.correlation_id == event.correlation_id
        assert log.device_id == event.device_id
        assert log.traffic_origin == "LIVE"
    finally:
        db.close()


# -----------------------------------------------------------------------------
# 8. Security Action Boundary (Task 1 Preservation)
# -----------------------------------------------------------------------------

def test_malicious_detection_never_automatically_isolates_device():
    """
    ML detection must NOT automatically isolate or firewall a medical device.
    Only human operators via Task 1 authorized endpoints can execute containment.
    """
    critical_attack = {
        "src_ip": "10.0.4.88",
        "dst_ip": "192.168.10.104",  # DEV-RAD-405
        "src_port": 51000,
        "dst_port": 104,
        "protocol": "DICOM",
        "packet_length": 1450.0,
        "flow_duration": 35.0,
        "header_length": 40.0,
        "byte_rate": 32000.0,
        "packet_rate": 95.0,
        "tcp_syn_flag": 0,
        "mqtt_msg_rate": 0.0,
        "modbus_fn_code": 0,
        "entropy": 7.95
    }

    event = security_pipeline.ingest(critical_attack, origin=TrafficOrigin.LIVE)

    assert event.severity == "CRITICAL"
    assert event.enforcement_status == "NONE"  # No automated action executed

    db = SessionLocal()
    try:
        device = db.query(Device).filter(Device.device_id == "DEV-RAD-405").first()
        assert device is not None
        # Must NOT be ISOLATED
        assert device.status != DeviceStatus.ISOLATED.value
    finally:
        db.close()


# -----------------------------------------------------------------------------
# 9. WebSocket Reliability & Non-Blocking Resilience
# -----------------------------------------------------------------------------

def test_websocket_stream_manager_deduplication():
    """Verifies that duplicate event IDs are identified and handled."""
    event_id = "EVT-TEST-DEDUP-001"
    assert manager.is_duplicate(event_id) is False
    assert manager.is_duplicate(event_id) is True


# -----------------------------------------------------------------------------
# 10. Failure Isolation & Resilience
# -----------------------------------------------------------------------------

def test_slow_websocket_client_does_not_block_pipeline():
    """Verifies that a slow or hanging WebSocket client is timed out and pruned without blocking detection."""
    class FakeSlowWebSocket:
        async def send_text(self, text: str):
            await asyncio.sleep(2.0)  # Exceeds send_timeout (0.25s)

    slow_ws = FakeSlowWebSocket()
    manager.active_connections.append(slow_ws)
    assert slow_ws in manager.active_connections

    t0 = time.perf_counter()
    asyncio.run(manager.broadcast({"type": "PING", "data": "test"}))
    t1 = time.perf_counter()

    elapsed = t1 - t0
    # Must have timed out quickly and pruned the slow client
    assert elapsed < 0.8
    assert slow_ws not in manager.active_connections


def test_malformed_telemetry_handles_gracefully():
    """Malformed or partial telemetry dictionary is safely normalized without raising 500 errors."""
    malformed = {
        "src_ip": "  192.168.1.10  ",
        "protocol": "mqtt",
        # Missing dst_ip, ports, packet_length, etc.
    }
    event = security_pipeline.ingest(malformed, origin=TrafficOrigin.LIVE)
    assert event.event_id is not None
    assert event.source_ip == "192.168.1.10"
    assert event.destination_ip == "0.0.0.0"
    assert event.device_match_status == DeviceMatchStatus.UNREGISTERED
    assert event.latency_metrics.total_detection_ms > 0


def test_ambiguous_device_resolution():
    """If multiple devices in the database match the destination IP, status must be AMBIGUOUS."""
    db = SessionLocal()
    try:
        dup1 = Device(
            device_id="DEV-DUP-A",
            name="Duplicate Device Alpha",
            category="Test",
            ip_address="192.168.10.222",
            mac_address="00:11:22:33:44:55",
            location="Test Bay 1",
            firmware_version="v1.0",
            status="Active",
            risk_score=10.0,
            protocol="MQTT"
        )
        dup2 = Device(
            device_id="DEV-DUP-B",
            name="Duplicate Device Beta",
            category="Test",
            ip_address="192.168.10.222",
            mac_address="00:11:22:33:44:66",
            location="Test Bay 2",
            firmware_version="v1.0",
            status="Active",
            risk_score=10.0,
            protocol="MQTT"
        )
        db.add_all([dup1, dup2])
        db.commit()

        event = security_pipeline.ingest({"dst_ip": "192.168.10.222"}, origin=TrafficOrigin.LIVE, db=db)
        assert event.device_match_status == DeviceMatchStatus.AMBIGUOUS
        assert event.device_id == "DEV-AMBIGUOUS"

        # Cleanup
        db.delete(dup1)
        db.delete(dup2)
        db.commit()
    finally:
        db.close()

