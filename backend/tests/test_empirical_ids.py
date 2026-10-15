"""
Unit & Integration Tests for Empirical Benchmark IDS Pipeline (Phase 2.3, 3, & 4).
Verifies:
- Empirical model loading and artifact verification
- Controlled model fallback upon missing or corrupted files
- 29-feature schema compatibility & prediction inference
- Analytical status and metrics API endpoints
- Unbroken backward compatibility for Phase 1 canonical pipeline
"""

import os
import tempfile
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.ml_engine import ml_engine, CONFIG_B_FEATURE_NAMES, CANONICAL_6_CLASSES


@pytest.fixture
def client():
    return TestClient(app)


def test_empirical_models_loaded():
    """Verify that empirical benchmark models are loaded and available."""
    status = ml_engine.get_model_status()
    assert status["empirical_models_loaded"] is True
    assert status["empirical_feature_count"] == 29
    assert len(status["empirical_classes"]) == 6
    assert status["empirical_models_available"]["random_forest_config_b"] is True
    assert status["empirical_models_available"]["xgboost_config_b"] is True
    assert status["empirical_models_available"]["isolation_forest_config_b"] is True


def test_empirical_prediction_random_forest():
    """Verify prediction with the empirical 29-feature Random Forest model."""
    sample_features = {feat: 0.0 for feat in CONFIG_B_FEATURE_NAMES}
    sample_features["tcp_flags"] = 2.0
    sample_features["tcp_connection_syn"] = 1.0

    is_anomaly, anomaly_score, threat_type, confidence, severity, key_features = (
        ml_engine.predict_packet_empirical(sample_features, model_type="rf")
    )

    assert isinstance(is_anomaly, bool)
    assert 0.0 <= anomaly_score <= 1.0
    assert threat_type in CANONICAL_6_CLASSES
    assert 0.0 <= confidence <= 1.0
    assert severity in ["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert isinstance(key_features, dict)


def test_empirical_prediction_xgboost():
    """Verify prediction with the empirical 29-feature XGBoost model."""
    sample_features = {feat: 0.0 for feat in CONFIG_B_FEATURE_NAMES}
    sample_features["icmp_checksum"] = 12345.0

    is_anomaly, anomaly_score, threat_type, confidence, severity, key_features = (
        ml_engine.predict_packet_empirical(sample_features, model_type="xgb")
    )

    assert isinstance(is_anomaly, bool)
    assert 0.0 <= anomaly_score <= 1.0
    assert threat_type in CANONICAL_6_CLASSES
    assert 0.0 <= confidence <= 1.0


def test_empirical_fallback_on_missing_model():
    """Verify graceful fallback when given an empty / invalid model directory."""
    with tempfile.TemporaryDirectory() as empty_dir:
        success = ml_engine.load_empirical_models(empty_dir)
        assert success is False
        assert ml_engine.empirical_loaded is False

        # Must fall back gracefully to Phase 1 prediction without crashing
        res = ml_engine.predict_packet_empirical({"packet_length": 300.0})
        assert len(res) == 6

        # Reload working models to restore state
        restored = ml_engine.load_empirical_models()
        assert restored is True
        assert ml_engine.empirical_loaded is True


def test_model_status_endpoint(client):
    """Test GET /api/v1/analytics/model-status endpoint."""
    response = client.get("/api/v1/analytics/model-status")
    assert response.status_code == 200
    data = response.json()
    assert data["active_version"] == "phase1_synthetic"
    assert data["phase1_models_loaded"] is True
    assert data["empirical_models_loaded"] is True
    assert data["empirical_feature_count"] == 29


def test_empirical_metrics_endpoint(client):
    """Test GET /api/v1/analytics/empirical-metrics endpoint."""
    response = client.get("/api/v1/analytics/empirical-metrics")
    assert response.status_code == 200
    data = response.json()
    assert "Random_Forest_Config_B" in data
    assert "XGBoost_Config_B" in data
    assert "Isolation_Forest_Config_B" in data
    assert "model_artifact_sizes_kb" in data


def test_phase1_backward_compatibility():
    """Verify Phase 1 canonical prediction remains intact."""
    canonical_features = {
        "packet_length": 1400.0,
        "flow_duration": 15.0,
        "header_length": 40.0,
        "byte_rate": 20000.0,
        "packet_rate": 80.0,
        "tcp_syn_flag": 0,
        "mqtt_msg_rate": 0.0,
        "modbus_fn_code": 0,
        "entropy": 7.8
    }
    is_anomaly, score, threat_type, conf, sev, feats = ml_engine.predict_packet(canonical_features)
    assert isinstance(is_anomaly, bool)
    assert threat_type in [
        "Normal", "DICOM Ransomware", "MQTT Flood DoS",
        "Modbus Command Injection", "ARP Spoofing MITM", "Port Scan Reconnaissance"
    ]
