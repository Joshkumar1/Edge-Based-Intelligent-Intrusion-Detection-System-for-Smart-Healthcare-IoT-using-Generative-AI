from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any


class AuditLogOut(BaseModel):
    id: int
    audit_id: str
    actor_id: Optional[int] = None
    actor_username: str
    actor_role: str
    action_type: str
    target_entity_type: str
    target_entity_id: str
    target_device_id: Optional[str] = None
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    impact_assessment: Optional[str] = None
    timestamp: datetime
    source_ip: Optional[str] = None
    enforcement_mode: str
    enforcement_status: str
    enforcement_result: Optional[Dict[str, Any]] = None
    success: bool
    failure_reason: Optional[str] = None
    correlation_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
