from enum import Enum
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class MachineType(str, Enum):
    INFUSION_PUMP = "Infusion Pump"
    SMART_VENTILATOR = "Smart Ventilator"
    PATIENT_MONITOR = "Patient Monitor"
    ICU_TELEMETRY = "ICU Telemetry Station"
    DICOM_GATEWAY = "DICOM Radiology Workstation"
    SMART_SYRINGE = "Smart Syringe Driver"
    SCADA_CONTROLLER = "SCADA Controller"


class SignalType(str, Enum):
    VITALS = "VITALS"
    INFUSION_TELEMETRY = "INFUSION_TELEMETRY"
    VENTILATION_PRESSURE = "VENTILATION_PRESSURE"
    DICOM_PACS_STREAM = "DICOM_PACS_STREAM"
    MODBUS_SCADA_SIGNAL = "MODBUS_SCADA_SIGNAL"
    DEVICE_DIAGNOSTIC = "DEVICE_DIAGNOSTIC"


class SignalIntegrityStatus(str, Enum):
    VERIFIED = "VERIFIED"
    ANOMALOUS_VALUE = "ANOMALOUS_VALUE"
    REPLAY_ATTACK = "REPLAY_ATTACK"
    SIGNATURE_INVALID = "SIGNATURE_INVALID"
    PHYSICAL_INVARIANT_BREACH = "PHYSICAL_INVARIANT_BREACH"
    MALFORMED = "MALFORMED"


class CyberDefenseMode(str, Enum):
    PASSIVE_MONITOR = "PASSIVE_MONITOR"
    ASSISTED_DEFENSE = "ASSISTED_DEFENSE"
    ACTIVE_PREVENTION = "ACTIVE_PREVENTION"


class DefenseActionType(str, Enum):
    NONE = "NONE"
    LOG_ALERT = "LOG_ALERT"
    SIGNAL_DROP = "SIGNAL_DROP"
    SAFETY_INTERLOCK_ENGAGED = "SAFETY_INTERLOCK_ENGAGED"
    FIREWALL_ISOLATE = "FIREWALL_ISOLATE"


class MachineSignalInput(BaseModel):
    device_id: str = Field(..., description="Target or emitting medical device identifier")
    signal_type: SignalType = Field(default=SignalType.VITALS, description="Type of signal payload")
    seq_num: int = Field(default=1, description="Monotonically increasing sequence number for anti-replay verification")
    timestamp: Optional[datetime] = Field(default=None, description="Signal capture timestamp from machine")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Raw physical sensor / telemetry data points")
    network_meta: Optional[Dict[str, Any]] = Field(default=None, description="Transport layer metadata if captured from interface")
    signature: Optional[str] = Field(default=None, description="Cryptographic machine attestation signature")


class MachineSignalAnalysisResult(BaseModel):
    signal_id: str
    device_id: str
    device_name: str
    device_category: str
    timestamp: datetime
    seq_num: int
    integrity_status: SignalIntegrityStatus
    physical_invariant_breach: bool
    breach_details: Optional[str] = None
    anomaly_score: float = 0.0
    is_threat: bool = False
    threat_type: str = "Normal"
    severity: str = "INFORMATIONAL"
    defense_mode: CyberDefenseMode
    defense_action_taken: DefenseActionType
    clinical_safety_interlock: bool = False
    enforcement_details: Optional[Dict[str, Any]] = None
    alert_id: Optional[str] = None
    latency_ms: float = 0.0
    payload: Dict[str, Any] = Field(default_factory=dict)


class CollectorStatus(BaseModel):
    collector_id: str
    name: str
    collector_type: str  # REST_INGEST, TCP_SOCKET, MQTT_BRIDGE, EMITTER
    status: str          # RUNNING, STOPPED, ERROR
    endpoint: str        # e.g. "POST /api/v1/signals/ingest", "tcp://0.0.0.0:9100"
    signals_received: int
    signals_rejected: int
    last_signal_time: Optional[datetime] = None
    description: str


class DefensePolicyConfig(BaseModel):
    mode: CyberDefenseMode = CyberDefenseMode.ACTIVE_PREVENTION
    auto_isolate_critical: bool = True
    engage_safety_interlocks: bool = True
    anti_replay_enforcement: bool = True
    rate_limit_per_machine_hz: int = 50
    alert_escalation_threshold: float = 0.85
