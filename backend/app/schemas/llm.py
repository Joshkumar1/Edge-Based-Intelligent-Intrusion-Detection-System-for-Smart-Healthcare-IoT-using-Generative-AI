from pydantic import BaseModel
from typing import Dict, Optional, Any


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
