"""
Pydantic schemas for Patient Vital-Sign Monitoring & Hospital Mortality Risk Research.
EdgeShield AI.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class VitalSignInput(BaseModel):
    """Input representation for patient vital sign measurements."""
    heart_rate: Optional[float] = Field(None, description="Heart rate in beats per minute (bpm)", ge=0, le=300)
    respiratory_rate: Optional[float] = Field(None, description="Respiratory rate in breaths/min", ge=0, le=100)
    spo2: Optional[float] = Field(None, description="Oxygen saturation percentage (%)", ge=0, le=100)
    systolic_bp: Optional[float] = Field(None, description="Systolic blood pressure (mmHg)", ge=0, le=350)
    diastolic_bp: Optional[float] = Field(None, description="Diastolic blood pressure (mmHg)", ge=0, le=250)
    mean_bp: Optional[float] = Field(None, description="Mean arterial pressure (mmHg)", ge=0, le=250)
    temperature: Optional[float] = Field(None, description="Body temperature", ge=20.0, le=115.0)
    temperature_unit: str = Field("C", description="Temperature unit: 'C' (Celsius) or 'F' (Fahrenheit)")


class VitalSignValidationResponse(BaseModel):
    """Validation response including range checks and data quality flags."""
    valid: bool
    temperature_celsius: Optional[float] = None
    validation_messages: List[str] = Field(default_factory=list)
    quality_flags: List[str] = Field(default_factory=list)
    missing_measurements: List[str] = Field(default_factory=list)


class MortalityRiskAssessmentRequest(BaseModel):
    """Request payload for experimental hospital mortality risk assessment."""
    subject_id: Optional[int] = Field(None, description="Optional research subject identifier")
    stay_id: Optional[int] = Field(None, description="Optional ICU stay identifier")
    vitals: Optional[VitalSignInput] = Field(None, description="Raw vital sign measurements")
    features: Optional[Dict[str, float]] = Field(None, description="Precomputed feature dictionary")
    hours_monitored: float = Field(24.0, description="Observation duration in hours", ge=1.0, le=168.0)


class MortalityRiskAssessmentResponse(BaseModel):
    """Response payload with experimental risk estimation and mandatory clinical disclaimer."""
    prediction: Optional[int] = Field(None, description="Binary prediction thresholded at 0.5 (0 = survival, 1 = in-hospital mortality)")
    estimated_probability: Optional[float] = Field(None, description="Estimated probability of in-hospital mortality (0.0 to 1.0)")
    risk_score: Optional[float] = Field(None, description="Alias for estimated_probability")
    risk_category: str = Field(..., description="Risk category: LOW, ELEVATED, HIGH, or INDETERMINATE")
    model_name: str = Field("LogisticRegression(L2, C=0.1)", description="Model identifier")
    model_version: str = Field("1.0.0-mimic4-demo-baseline", description="Model version")
    prediction_target: str = Field("hospital_expire_flag", description="Eventual in-hospital mortality after 24h")
    prediction_horizon: str = Field("post-24h in-hospital stay among eligible cohort", description="Prediction horizon")
    experimental_research_only: bool = True
    clinical_disclaimer: str
    limitations: List[str]
    quality_flags: List[str]
    missing_measurements: List[str]
    validated_vitals_celsius: Dict[str, Optional[float]]


class ClinicalPredictionRequest(BaseModel):
    """Request payload for direct clinical feature or vital prediction."""
    subject_id: Optional[int] = Field(None, description="Optional patient research identifier")
    stay_id: Optional[int] = Field(None, description="Optional ICU stay identifier")
    vitals: Optional[VitalSignInput] = Field(None, description="Raw vital sign measurements")
    features: Optional[Dict[str, float]] = Field(None, description="Precomputed 69-feature vector")
    hours_monitored: float = Field(24.0, ge=1.0, le=168.0, description="Monitored duration in hours")


class ClinicalPredictionResponse(BaseModel):
    """Standardized clinical prediction response schema."""
    prediction: Optional[int] = Field(None, description="Binary prediction thresholded at 0.5 (0 = survival, 1 = mortality)")
    estimated_probability: Optional[float] = Field(None, description="Estimated probability of in-hospital mortality (0.0 to 1.0)")
    risk_category: str = Field(..., description="LOW, ELEVATED, HIGH, or INDETERMINATE")
    model_name: str = Field(..., description="Name of the model utilized")
    prediction_target: str = Field("hospital_expire_flag", description="Eventual in-hospital mortality after 24h")
    prediction_horizon: str = Field("post-24h in-hospital stay among eligible cohort", description="Prediction horizon")
    experimental_research_only: bool = True
    clinical_disclaimer: str
    limitations: List[str]
    missing_features: List[str] = Field(default_factory=list)
    quality_flags: List[str] = Field(default_factory=list)


class CohortSummaryResponse(BaseModel):
    """Summary of the verified MIMIC-IV Demo research cohort."""
    pipeline_stage: str
    dataset: str
    prediction_time_definition: str
    counts_before_filtering: Dict[str, int]
    exclusions: Dict[str, int]
    eligible_cohort: Dict[str, object]
    coverage_metrics: Dict[str, object]
    model_metrics: Optional[Dict[str, object]] = None
