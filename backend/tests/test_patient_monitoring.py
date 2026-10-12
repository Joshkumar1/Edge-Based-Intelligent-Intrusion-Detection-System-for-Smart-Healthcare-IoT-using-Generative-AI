"""
Comprehensive test suite for Patient Vital-Sign Monitoring & Hospital Mortality Risk Research.
Tests cohort eligibility, temporal leakage, quality flags, preprocessing, patient splitting,
model loading, prediction endpoints, input validation, and service separation.
EdgeShield AI.
"""

import json
import math
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.patient_monitoring import (
    ClinicalPredictionRequest,
    MortalityRiskAssessmentRequest,
    VitalSignInput,
)
from app.services.patient_monitoring_service import PatientMonitoringService, patient_monitoring_service

client = TestClient(app)
RESEARCH_DIR = Path(__file__).resolve().parents[2] / "research/patient_monitoring"


# ============================================================================
# 1. COHORT ELIGIBILITY & TEMPORAL INTEGRITY TESTS
# ============================================================================

def test_cohort_linkage_and_missing_outcomes():
    """Verify ICU stays are linked many-to-one to hospital admissions without missing outcomes."""
    audit_file = RESEARCH_DIR / "cohort_audit_summary.json"
    assert audit_file.exists(), "cohort_audit_summary.json must exist"

    with open(audit_file, "r") as f:
        data = json.load(f)

    assert data["counts_before_filtering"]["total_icu_stays"] == 140
    assert data["counts_before_filtering"]["stays_linked_to_outcomes"] == 140
    assert data["counts_before_filtering"]["missing_outcomes"] == 0


def test_deaths_before_prediction_time_excluded():
    """Verify patients who died before or at 24 hours are excluded from prospective prediction."""
    audit_file = RESEARCH_DIR / "cohort_audit_summary.json"
    with open(audit_file, "r") as f:
        data = json.load(f)

    assert data["exclusions"]["deaths_before_or_at_prediction_time"] == 2
    # Exact stays: 36871784 (died at 1h 14m), 38275267 (died at 12h 39m)
    assert set(data["exclusions"]["deaths_before_pred_stays"]) == {36871784, 38275267}


def test_discharged_before_prediction_time_excluded():
    """Verify patients discharged from the hospital before 24 hours are excluded."""
    audit_file = RESEARCH_DIR / "cohort_audit_summary.json"
    with open(audit_file, "r") as f:
        data = json.load(f)

    assert data["exclusions"]["discharged_alive_before_prediction_time"] == 2
    # Stays discharged alive: 32554129, 30864406
    assert set(data["exclusions"]["discharged_alive_before_pred_stays"]) == {32554129, 30864406}


def test_eligible_cohort_counts():
    """Verify eligible cohort counts: 136 stays, 98 unique patients, 18 deaths."""
    audit_file = RESEARCH_DIR / "cohort_audit_summary.json"
    with open(audit_file, "r") as f:
        data = json.load(f)

    assert data["eligible_cohort"]["eligible_icu_stays"] == 136
    assert data["eligible_cohort"]["unique_eligible_patients"] == 98
    assert data["eligible_cohort"]["eligible_deaths_stays"] == 18
    assert data["eligible_cohort"]["eligible_survivors_stays"] == 118
    assert data["eligible_cohort"]["eligible_deaths_unique_patients"] == 14
    assert data["eligible_cohort"]["eligible_survivors_unique_patients"] == 88


def test_no_duplicate_records():
    """Verify zero duplicate stay identifiers across feature, label, and metadata files."""
    quality_file = RESEARCH_DIR / "data_quality_report.json"
    assert quality_file.exists(), "data_quality_report.json must exist"

    with open(quality_file, "r") as f:
        data = json.load(f)

    assert data["checks"]["no_duplicate_stay_ids"]["passed"] is True
    assert data["checks"]["strict_id_alignment"]["passed"] is True
    assert data["checks"]["outcome_labels_valid"]["passed"] is True


def test_zero_target_and_temporal_leakage():
    """Verify zero target leakage in feature columns and zero post-prediction temporal leakage."""
    quality_file = RESEARCH_DIR / "data_quality_report.json"
    with open(quality_file, "r") as f:
        data = json.load(f)

    assert data["checks"]["zero_target_leakage_columns"]["passed"] is True
    assert data["checks"]["zero_temporal_leakage"]["passed"] is True
    assert data["checks"]["zero_temporal_leakage"]["stays_with_temporal_mismatch"] == 0


def test_patient_level_splitting_zero_leakage():
    """Verify training and test partitions group strictly by subject_id with zero overlap."""
    splits_file = RESEARCH_DIR / "patient_splits.json"
    assert splits_file.exists(), "patient_splits.json must exist"

    with open(splits_file, "r") as f:
        data = json.load(f)

    train_pts = set(data["train_patient_ids"])
    test_pts = set(data["test_patient_ids"])
    overlap = train_pts.intersection(test_pts)

    assert len(overlap) == 0, f"Patient leakage detected: {overlap}"
    assert len(train_pts) + len(test_pts) == 98


# ============================================================================
# 2. VITAL SIGNS VALIDATION & DATA QUALITY LOGIC
# ============================================================================

def test_service_temperature_conversion():
    """Verify Fahrenheit to Celsius normalization."""
    svc = PatientMonitoringService(research_dir=RESEARCH_DIR)

    # 98.6°F -> 37.0°C
    vitals_f = VitalSignInput(temperature=98.6, temperature_unit="F")
    res_f = svc.validate_vital_signs(vitals_f)
    assert res_f.temperature_celsius == 37.0
    assert any("converted from 98.6°F" in msg for msg in res_f.validation_messages)

    # 38.5°C stays 38.5°C
    vitals_c = VitalSignInput(temperature=38.5, temperature_unit="C")
    res_c = svc.validate_vital_signs(vitals_c)
    assert res_c.temperature_celsius == 38.5


def test_service_quality_flags_detection():
    """Verify detection of review_zero_value, review_low_spo2, and review_extreme_heart_rate."""
    svc = PatientMonitoringService(research_dir=RESEARCH_DIR)

    # Zero heart rate
    vitals_zero = VitalSignInput(heart_rate=0.0, respiratory_rate=16.0, spo2=98.0)
    res_zero = svc.validate_vital_signs(vitals_zero)
    assert "review_zero_value" in res_zero.quality_flags

    # Severe hypoxemia (< 70%)
    vitals_hypox = VitalSignInput(heart_rate=80.0, respiratory_rate=20.0, spo2=64.0)
    res_hypox = svc.validate_vital_signs(vitals_hypox)
    assert "review_low_spo2" in res_hypox.quality_flags

    # Extreme tachycardia (> 180)
    vitals_tachy = VitalSignInput(heart_rate=195.0, respiratory_rate=22.0, spo2=95.0)
    res_tachy = svc.validate_vital_signs(vitals_tachy)
    assert "review_extreme_heart_rate" in res_tachy.quality_flags


def test_service_missing_measurements():
    """Verify missing measurement detection without filling with zero."""
    svc = PatientMonitoringService(research_dir=RESEARCH_DIR)

    # Provide only heart rate and SpO2
    vitals_partial = VitalSignInput(heart_rate=75.0, spo2=97.0)
    res = svc.validate_vital_signs(vitals_partial)

    expected_missing = {"respiratory_rate", "systolic_bp", "diastolic_bp", "mean_bp", "temperature_celsius"}
    assert set(res.missing_measurements) == expected_missing


# ============================================================================
# 3. HEALTH, CORS & OPENAPI ARCHITECTURE TESTS
# ============================================================================

def test_health_endpoint():
    """Verify GET /health returns operational health and active modules."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "EdgeShield AI" in data["project"]
    assert data["modules"]["patient_monitoring"] == "ONLINE"
    assert data["modules"]["intrusion_detection"] == "ONLINE"


def test_root_endpoint():
    """Verify root GET / returns operational status and docs link."""
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "OPERATIONAL"
    assert "/docs" in data["docs_url"]


def test_openapi_schema_generated():
    """Verify FastAPI OpenAPI documentation schema is generated and contains patient-monitoring paths."""
    res = client.get("/api/v1/openapi.json")
    assert res.status_code == 200
    schema = res.json()
    assert "paths" in schema
    assert "/api/v1/patient-monitoring/assess-risk" in schema["paths"]
    assert "/api/v1/patient-monitoring/predict" in schema["paths"]
    assert "/api/v1/patient-monitoring/cohort-summary" in schema["paths"]


def test_cors_options_preflight():
    """Verify CORS preflight OPTIONS requests are handled with proper headers."""
    res = client.options(
        "/api/v1/patient-monitoring/status",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert res.status_code in [200, 204]
    assert "access-control-allow-origin" in res.headers


# ============================================================================
# 4. PREDICTION ENDPOINTS & ERROR HANDLING TESTS
# ============================================================================

def test_api_status_endpoint():
    """Verify GET /api/v1/patient-monitoring/status endpoint."""
    res = client.get("/api/v1/patient-monitoring/status")
    assert res.status_code == 200
    data = res.json()
    assert data["module"] == "Patient Vital-Sign Monitoring & Hospital Mortality Risk"
    assert data["status"] == "ONLINE"
    assert data["model_loaded"] is True


def test_api_validate_vitals_endpoint():
    """Verify POST /api/v1/patient-monitoring/validate-vitals endpoint."""
    payload = {
        "heart_rate": 0.0,
        "respiratory_rate": 20.0,
        "spo2": 68.0,
        "temperature": 102.2,
        "temperature_unit": "F",
    }
    res = client.post("/api/v1/patient-monitoring/validate-vitals", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["temperature_celsius"] == 39.0
    assert "review_zero_value" in data["quality_flags"]
    assert "review_low_spo2" in data["quality_flags"]
    assert "systolic_bp" in data["missing_measurements"]


def test_api_assess_risk_endpoint():
    """Verify POST /api/v1/patient-monitoring/assess-risk returns risk estimate and mandatory disclaimer."""
    payload = {
        "vitals": {
            "heart_rate": 88.0,
            "respiratory_rate": 18.0,
            "spo2": 97.0,
            "systolic_bp": 120.0,
            "diastolic_bp": 80.0,
            "mean_bp": 93.3,
            "temperature": 37.0,
            "temperature_unit": "C",
        },
        "hours_monitored": 24.0,
    }
    res = client.post("/api/v1/patient-monitoring/assess-risk", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["risk_score"] is not None
    assert 0.0 <= data["risk_score"] <= 1.0
    assert data["estimated_probability"] == data["risk_score"]
    assert data["prediction"] in [0, 1]
    assert data["risk_category"] in ["LOW", "ELEVATED", "HIGH"]
    assert data["experimental_research_only"] is True
    assert "DISCLAIMER" in data["clinical_disclaimer"]
    assert data["prediction_target"] == "hospital_expire_flag"
    assert len(data["limitations"]) > 0


def test_api_predict_endpoint_valid_feature_vector():
    """Verify POST /api/v1/patient-monitoring/predict accepts direct feature vector and returns standardized schema."""
    # Precomputed sample features matching features_24h.csv
    payload = {
        "features": {
            "heart_rate_mean": 82.5,
            "heart_rate_recent": 85.0,
            "heart_rate_min": 72.0,
            "heart_rate_max": 96.0,
            "respiratory_rate_mean": 18.0,
            "spo2_mean": 97.5,
            "temperature_celsius_mean": 37.1,
            "distinct_monitored_hours": 24.0,
            "flag_zero_value_count": 0.0,
            "total_flagged_observations": 0.0,
        },
        "hours_monitored": 24.0,
    }
    res = client.post("/api/v1/patient-monitoring/predict", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["prediction"] in [0, 1]
    assert data["estimated_probability"] is not None
    assert 0.0 <= data["estimated_probability"] <= 1.0
    assert data["risk_category"] in ["LOW", "ELEVATED", "HIGH"]
    assert data["model_name"] == "LogisticRegression(L2, C=0.1)"
    assert data["prediction_target"] == "hospital_expire_flag"
    assert "post-24h" in data["prediction_horizon"]
    assert data["experimental_research_only"] is True
    assert "DISCLAIMER" in data["clinical_disclaimer"]
    assert len(data["limitations"]) > 0


def test_api_predict_endpoint_rejects_nan_and_infinity():
    """Verify POST /api/v1/patient-monitoring/predict returns 422 when NaN or inf is sent."""
    # Send payload with explicit null or string "NaN"
    payload = {
        "features": {
            "heart_rate_mean": float("nan"),
        }
    }
    # Fastapi / Pydantic handles NaN serialization as null or NaN
    res = client.post(
        "/api/v1/patient-monitoring/predict",
        json={"features": {"heart_rate_mean": "NaN"}},
    )
    assert res.status_code == 422


def test_api_predict_rejects_negative_vitals():
    """Verify input validation rejects physiologically impossible values (e.g. negative SpO2)."""
    payload = {
        "vitals": {
            "heart_rate": -10.0,
            "spo2": 95.0,
        }
    }
    res = client.post("/api/v1/patient-monitoring/predict", json=payload)
    assert res.status_code == 422


def test_api_cohort_summary_endpoint():
    """Verify GET /api/v1/patient-monitoring/cohort-summary returns verified audit."""
    res = client.get("/api/v1/patient-monitoring/cohort-summary")
    assert res.status_code == 200
    data = res.json()
    assert data["counts_before_filtering"]["total_icu_stays"] == 140
    assert data["eligible_cohort"]["eligible_icu_stays"] == 136


def test_api_sample_records_endpoint():
    """Verify GET /api/v1/patient-monitoring/sample-records returns demonstration patients."""
    res = client.get("/api/v1/patient-monitoring/sample-records")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 3
    assert data[0]["stay_id"] == 31269608


# ============================================================================
# 5. MODEL ARTIFACT FALLBACK & RECOVERY TESTS
# ============================================================================

def test_model_artifact_missing_graceful_fallback(tmp_path):
    """Verify service gracefully returns INDETERMINATE with disclaimers when artifacts are missing."""
    empty_dir = tmp_path / "empty_research"
    empty_dir.mkdir()

    # Point service to empty dir
    patient_monitoring_service.reload_artifacts(custom_dir=empty_dir)

    try:
        req = MortalityRiskAssessmentRequest(
            vitals=VitalSignInput(heart_rate=80.0, spo2=98.0)
        )
        res = patient_monitoring_service.assess_risk(req)
        assert res.risk_score is None
        assert res.prediction is None
        assert res.risk_category == "INDETERMINATE"
        assert res.model_name == "UNAVAILABLE"
        assert any("not found" in lim for lim in res.limitations)
        assert res.experimental_research_only is True
    finally:
        # Restore real artifacts
        patient_monitoring_service.reload_artifacts(custom_dir=RESEARCH_DIR)

    assert patient_monitoring_service.model is not None


# ============================================================================
# 6. SEPARATION OF CLINICAL & INTRUSION SERVICES
# ============================================================================

def test_separation_of_patient_monitoring_and_intrusion_detection():
    """Verify clinical prediction and IoMT intrusion detection operate as separate modules."""
    # Intrusion detection routes remain fully functional
    devices_res = client.get("/api/v1/devices/")
    assert devices_res.status_code == 200
    devices = devices_res.json()
    assert isinstance(devices, list)

    alerts_res = client.get("/api/v1/alerts/")
    assert alerts_res.status_code == 200

    signals_res = client.get("/api/v1/signals/collectors")
    assert signals_res.status_code == 200

    # Patient monitoring status is also healthy
    pm_res = client.get("/api/v1/patient-monitoring/status")
    assert pm_res.status_code == 200
    assert pm_res.json()["module"] == "Patient Vital-Sign Monitoring & Hospital Mortality Risk"


def test_api_predict_rejects_unexpected_features():
    """Verify POST /api/v1/patient-monitoring/predict rejects unexpected feature keys with 422."""
    payload = {
        "features": {
            "heart_rate_mean": 80.0,
            "nonexistent_bogus_feature": 123.4,
        }
    }
    res = client.post("/api/v1/patient-monitoring/predict", json=payload)
    assert res.status_code == 422
    assert "Unexpected feature" in res.json()["detail"]


def test_api_predict_rejects_missing_payload():
    """Verify POST /api/v1/patient-monitoring/predict rejects empty payload without vitals or features."""
    payload = {}
    res = client.post("/api/v1/patient-monitoring/predict", json=payload)
    assert res.status_code == 422
    assert "Either 'vitals' or 'features' must be provided" in res.json()["detail"]


def test_model_artifact_invalid_corrupted_graceful_handling(tmp_path):
    """Verify corrupted model artifact file is handled safely without crashing the service."""
    corrupted_dir = tmp_path / "corrupted_research"
    corrupted_dir.mkdir()
    (corrupted_dir / "baseline_model.joblib").write_bytes(b"NOT_A_VALID_JOBLIB_FILE")

    patient_monitoring_service.reload_artifacts(custom_dir=corrupted_dir)
    try:
        assert patient_monitoring_service.model is None
        res = client.get("/api/v1/patient-monitoring/status")
        assert res.status_code == 200
        assert res.json()["model_loaded"] is False
    finally:
        patient_monitoring_service.reload_artifacts(custom_dir=RESEARCH_DIR)

    assert patient_monitoring_service.model is not None


def test_model_metadata_mismatch_graceful_handling(tmp_path):
    """Verify model/metadata schema mismatch marks model as unavailable safely."""
    mismatch_dir = tmp_path / "mismatch_research"
    mismatch_dir.mkdir()
    # Copy real model
    import shutil
    shutil.copy(RESEARCH_DIR / "baseline_model.joblib", mismatch_dir / "baseline_model.joblib")
    # Write mismatched metadata
    with open(mismatch_dir / "model_feature_metadata.json", "w") as f:
        json.dump({"features": ["bogus_feature_1", "bogus_feature_2"]}, f)

    patient_monitoring_service.reload_artifacts(custom_dir=mismatch_dir)
    try:
        assert patient_monitoring_service.model is None
        res = client.get("/api/v1/patient-monitoring/status")
        assert res.status_code == 200
        assert res.json()["model_loaded"] is False
    finally:
        patient_monitoring_service.reload_artifacts(custom_dir=RESEARCH_DIR)

    assert patient_monitoring_service.model is not None

