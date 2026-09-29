from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(String, unique=True, index=True, nullable=False)
    
    # Actor / Identity
    actor_id = Column(Integer, nullable=True)
    actor_username = Column(String, nullable=False, index=True)
    actor_role = Column(String, nullable=False)
    
    # Action Metadata
    action_type = Column(String, nullable=False, index=True)  # DEVICE_ISOLATION, DEVICE_RECONNECT, ALERT_STATUS_UPDATE, etc.
    target_entity_type = Column(String, nullable=False, index=True)  # DEVICE, ALERT, DOCUMENT, POLICY
    target_entity_id = Column(String, nullable=False, index=True)
    target_device_id = Column(String, nullable=True, index=True)
    
    # State Transition
    previous_state = Column(String, nullable=True)
    new_state = Column(String, nullable=True)
    impact_assessment = Column(Text, nullable=True)  # Clinical impact assessment or operator justification
    
    # Network & Enforcement Context
    timestamp = Column(DateTime(timezone=True), default=utc_now, index=True, nullable=False)
    source_ip = Column(String, nullable=True)  # Operator client IP address
    
    # Enforcement Execution
    enforcement_mode = Column(String, nullable=False)  # SIMULATION, HOST_FIREWALL, SDN_CONTROLLER
    enforcement_status = Column(String, nullable=False)  # ENFORCED, SIMULATED, FAILED, UNSUPPORTED
    enforcement_result = Column(JSON, nullable=True)  # Output, command results, verification details
    
    # Outcome
    success = Column(Boolean, default=False, nullable=False)
    failure_reason = Column(Text, nullable=True)
    correlation_id = Column(String, nullable=True, index=True)
