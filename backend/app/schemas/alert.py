from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


class AlertOut(BaseModel):
    id: int
    alert_id: str
    timestamp: datetime
    source_ip: str
    destination_ip: str
    target_device_id: Optional[str] = None
    protocol: str
    anomaly_score: float
    is_anomaly: int
    threat_type: str
    confidence: float
    severity: str
    key_features: Optional[Dict[str, float]] = None
    clinical_explanation: Optional[str] = None
    clinical_impact: Optional[str] = None
    recommended_mitigation: Optional[str] = None
    status: str
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AlertUpdateStatus(BaseModel):
    status: str  # MITIGATED, INVESTIGATING, FALSE_POSITIVE
    resolved_by: Optional[str] = None
