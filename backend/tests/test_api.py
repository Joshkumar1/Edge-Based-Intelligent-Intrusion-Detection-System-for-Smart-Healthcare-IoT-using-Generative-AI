import pytest
from fastapi.testclient import TestClient
from app.main import app, seed_initial_data
from app.core.database import Base, engine, SessionLocal

# Initialize database tables for tests
Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_initial_data(db)
db.close()

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "EdgeShield AI"
    assert data["status"] == "OPERATIONAL"


def test_dashboard_stats():
    response = client.get("/api/v1/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_devices" in data
    assert "active_alerts" in data


def test_devices_list():
    response = client.get("/api/v1/devices/")
    assert response.status_code == 200
    devices = response.json()
    assert len(devices) > 0


def test_packet_analysis():
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
    response = client.post("/api/v1/detection/analyze", json=packet)
    assert response.status_code == 200
    data = response.json()
    assert data["is_anomaly"] is True
    assert data["threat_type"] == "DICOM Ransomware"
    assert data["target_device_id"] == "DEV-RAD-405"
    assert data["explanation_status"] == "PENDING"
    assert data["detection_latency_ms"] > 0
    assert data["event_id"] is not None

