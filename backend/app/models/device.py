from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from datetime import datetime
import enum
from app.core.database import Base


class DeviceCategory(str, enum.Enum):
    INFUSION_PUMP = "Infusion Pump"
    PATIENT_MONITOR = "Patient Monitor"
    ICU_TELEMETRY = "ICU Telemetry Station"
    DICOM_GATEWAY = "DICOM Radiology Workstation"
    VENTILATOR = "Smart Ventilator"
    SMART_SYRINGE = "Smart Syringe Driver"
    EDGE_GATEWAY = "Hospital Edge Security Gateway"


class DeviceStatus(str, enum.Enum):
    ACTIVE = "Active"
    WARNING = "Warning"
    CRITICAL = "Critical"
    ISOLATED = "Isolated"
    OFFLINE = "Offline"


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True, nullable=False)  # e.g., DEV-ICU-101
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    location = Column(String, nullable=False)  # e.g. ICU Wing B, Room 304
    firmware_version = Column(String, nullable=False)
    status = Column(String, default=DeviceStatus.ACTIVE.value)
    risk_score = Column(Float, default=0.0)  # 0 to 100
    protocol = Column(String, default="MQTT/Modbus")  # DICOM, MQTT, Modbus, CoAP, HL7
    last_seen = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
