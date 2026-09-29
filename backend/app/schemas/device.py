from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any


class DeviceBase(BaseModel):
    device_id: str
    name: str
    category: str
    ip_address: str
    mac_address: str
    location: str
    firmware_version: str
    status: str = "Active"
    risk_score: float = 0.0
    protocol: str = "MQTT/Modbus"


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    risk_score: Optional[float] = None
    location: Optional[str] = None
    firmware_version: Optional[str] = None


class DeviceOut(DeviceBase):
    id: int
    last_seen: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceIsolationRequest(BaseModel):
    justification: Optional[str] = "Operator initiated clinical containment"
    impact_assessment: Optional[str] = "Clinical telemetry isolation verified by operator"
    correlation_id: Optional[str] = None


class DeviceEnforcementResponse(BaseModel):
    device_id: str
    requested_action: str  # "isolate" | "reconnect"
    device_status: str     # "Isolated" | "Active"
    status: str            # Backward-compatibility alias for device_status
    enforcement_mode: str  # "HOST_FIREWALL" | "SIMULATION"
    enforcement_status: str # "ENFORCED" | "SIMULATED" | "FAILED" | "UNSUPPORTED"
    enforcement_message: str
    audit_log_id: str
    performed_by: str
    timestamp: datetime
    device: DeviceOut

    model_config = ConfigDict(from_attributes=True)
