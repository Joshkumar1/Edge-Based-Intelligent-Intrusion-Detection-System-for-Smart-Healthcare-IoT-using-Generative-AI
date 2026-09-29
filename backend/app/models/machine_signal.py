import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from app.core.database import Base


class MachineSignalLog(Base):
    __tablename__ = "machine_signal_logs"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(String, unique=True, index=True, nullable=False)
    device_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    signal_type = Column(String, nullable=False)
    seq_num = Column(Integer, default=1)
    integrity_status = Column(String, default="VERIFIED")
    physical_invariant_breach = Column(Integer, default=0)
    breach_details = Column(String, nullable=True)
    anomaly_score = Column(Float, default=0.0)
    is_threat = Column(Integer, default=0)
    threat_type = Column(String, default="Normal")
    severity = Column(String, default="INFORMATIONAL")
    defense_action = Column(String, default="NONE")
    clinical_interlock = Column(Integer, default=0)
    payload_json = Column(Text, default="{}")
    alert_id = Column(String, nullable=True)

    def get_payload(self) -> dict:
        try:
            return json.loads(self.payload_json) if self.payload_json else {}
        except Exception:
            return {}


class ClinicalSafetyInterlock(Base):
    """
    Safety Interlock state for medical machines under active cyber defense.
    Ensures life-support machines (infusion pumps, ventilators) safely switch
    to local clinician fail-safe manual override rather than catastrophic abrupt cutoff.
    """
    __tablename__ = "clinical_safety_interlocks"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True, nullable=False)
    engaged_at = Column(DateTime, default=datetime.utcnow)
    reason = Column(String, nullable=False)
    trigger_signal_id = Column(String, nullable=True)
    safe_state_mode = Column(String, default="LOCAL_BEDSIDE_OVERRIDE_LOCKED")
    acknowledged_by = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
