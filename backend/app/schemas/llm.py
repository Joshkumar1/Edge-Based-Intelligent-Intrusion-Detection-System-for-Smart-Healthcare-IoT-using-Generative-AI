from pydantic import BaseModel, Field
from typing import Dict, Optional, Any, List


class ExplainRequest(BaseModel):
    threat_type: str
    severity: str
    source_ip: str
    target_device_name: str
    target_device_type: str
    location: str
    key_features: Dict[str, float]


class ExplainResponse(BaseModel):
    clinical_explanation: str
    clinical_impact: str
    recommended_mitigation: str
    ai_engine_used: str  # "Ollama (Llama 3)" or "EdgeShield Deterministic Engine"


class SourceAttribution(BaseModel):
    type: str  # "Research Document", "Security Telemetry", "ML Prediction", "General Knowledge"
    detail: str


class CopilotRequest(BaseModel):
    context_type: str = Field(default="research", description="Context: 'research', 'incident', 'device', 'architecture', 'telemetry'")
    query: str = Field(..., description="User question or prompt for the copilot")
    context_id: Optional[str] = Field(default=None, description="Document ID or Incident ID")
    context_data: Optional[Dict[str, Any]] = Field(default=None, description="Metadata dictionary for active context")


class CopilotResponse(BaseModel):
    summary: str
    evidence: Optional[str] = None
    analysis: Optional[str] = None
    recommended_mitigation: Optional[str] = None
    sources: List[SourceAttribution] = []
    page_reference: Optional[int] = None
    document_title: Optional[str] = None
    section: Optional[str] = None
    ai_engine_used: str
