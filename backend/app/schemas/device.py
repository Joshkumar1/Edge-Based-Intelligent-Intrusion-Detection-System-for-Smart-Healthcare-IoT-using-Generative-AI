from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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

    class Config:
        from_attributes = True
