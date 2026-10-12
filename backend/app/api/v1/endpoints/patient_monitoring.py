"""
FastAPI router for Patient Vital-Sign Monitoring & Hospital Mortality Risk Research.
EdgeShield AI.
"""

from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, status

from app.schemas.patient_monitoring import (
    ClinicalPredictionRequest,
    ClinicalPredictionResponse,
    MortalityRiskAssessmentRequest,
    MortalityRiskAssessmentResponse,
    VitalSignInput,
    VitalSignValidationResponse,
)
from app.services.patient_monitoring_service import patient_monitoring_service

router = APIRouter()


@router.get("/status", summary="Patient Monitoring Module Status")
def get_service_status() -> Dict[str, Any]:
    """Check module operational status, loaded model artifact, and data pipeline health."""
    has_model = patient_monitoring_service.model is not None
    return {
        "module": "Patient Vital-Sign Monitoring & Hospital Mortality Risk",
        "status": "ONLINE",
        "model_loaded": has_model,
        "model_version": "1.0.0-mimic4-demo-baseline" if has_model else "UNAVAILABLE",
        "dataset": "MIMIC-IV Clinical Database Demo 2.2",
        "mode": "Research & Engineering Verification Only",
    }


@router.post("/validate-vitals", response_model=VitalSignValidationResponse, summary="Validate Patient Vital Signs")
def validate_vitals(vitals: VitalSignInput) -> VitalSignValidationResponse:
    """
    Validate patient vital signs against physiological bounds, convert temperature to Celsius,
    and detect quality flags (zero measurements, hypoxemia, extreme heart rate).
    """
    try:
        return patient_monitoring_service.validate_vital_signs(vitals)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Vital sign validation error: {str(e)}",
        )


@router.post("/assess-risk", response_model=MortalityRiskAssessmentResponse, summary="Assess Experimental Mortality Risk")
def assess_mortality_risk(request: MortalityRiskAssessmentRequest) -> MortalityRiskAssessmentResponse:
    """
    Produce an experimental in-hospital mortality risk estimate for an eligible ICU patient.
    Includes mandatory clinical disclaimers and small-sample limitations.
    """
    try:
        return patient_monitoring_service.assess_risk(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid assessment input: {str(e)}",
        )


@router.post("/predict", response_model=ClinicalPredictionResponse, summary="Standardized Clinical Model Prediction")
def predict_clinical_outcome(request: ClinicalPredictionRequest) -> ClinicalPredictionResponse:
    """
    Standardized clinical model prediction endpoint accepting precomputed feature vectors
    or bedside vital-sign measurements.
    """
    try:
        return patient_monitoring_service.predict_clinical_outcome(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Clinical prediction input error: {str(e)}",
        )


@router.get("/cohort-summary", summary="Research Cohort Audit Summary")
def get_cohort_summary() -> Dict[str, Any]:
    """Retrieve verified MIMIC-IV Demo cohort audit counts, exclusions, and coverage metrics."""
    summary = patient_monitoring_service.get_cohort_summary()
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cohort audit summary not found. Ensure build_prediction_cohort.py has been executed.",
        )
    return summary


@router.get("/sample-records", summary="Get Anonymized Sample Patient Vitals")
def get_sample_records() -> List[Dict[str, Any]]:
    """Return realistic anonymized sample patient vital-sign profiles for demonstration."""
    return [
        {
            "stay_id": 31269608,
            "patient_label": "Patient A (Stable ICU Floor Monitored)",
            "vitals": {
                "heart_rate": 78.0,
                "respiratory_rate": 16.0,
                "spo2": 98.0,
                "systolic_bp": 122.0,
                "diastolic_bp": 74.0,
                "mean_bp": 90.0,
                "temperature": 37.1,
                "temperature_unit": "C",
            },
            "hours_monitored": 24.0,
            "expected_risk_category": "LOW",
        },
        {
            "stay_id": 38559363,
            "patient_label": "Patient B (Compensated Tachycardia / Elevated)",
            "vitals": {
                "heart_rate": 118.0,
                "respiratory_rate": 24.0,
                "spo2": 93.0,
                "systolic_bp": 105.0,
                "diastolic_bp": 62.0,
                "mean_bp": 76.0,
                "temperature": 38.6,
                "temperature_unit": "C",
            },
            "hours_monitored": 24.0,
            "expected_risk_category": "ELEVATED",
        },
        {
            "stay_id": 39543480,
            "patient_label": "Patient C (Critical Hypotensive & Hypoxemic)",
            "vitals": {
                "heart_rate": 138.0,
                "respiratory_rate": 32.0,
                "spo2": 82.0,
                "systolic_bp": 84.0,
                "diastolic_bp": 48.0,
                "mean_bp": 60.0,
                "temperature": 39.4,
                "temperature_unit": "C",
            },
            "hours_monitored": 24.0,
            "expected_risk_category": "HIGH",
        },
    ]
