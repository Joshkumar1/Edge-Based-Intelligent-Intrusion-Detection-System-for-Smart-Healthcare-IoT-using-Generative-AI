from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from datetime import datetime
from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String, unique=True, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Network context
    source_ip = Column(String, nullable=False)
    destination_ip = Column(String, nullable=False)
    target_device_id = Column(String, nullable=True)
    protocol = Column(String, nullable=False)
    
    # ML Detection Results
    anomaly_score = Column(Float, nullable=False)
    is_anomaly = Column(Integer, default=1)  # 1 = Anomaly, 0 = Normal
    threat_type = Column(String, nullable=False)  # Ransomware, MQTT Flood, Modbus Injection, etc.
    confidence = Column(Float, nullable=False)
    severity = Column(String, nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    
    # Explainable AI & LLM Fields
    key_features = Column(JSON, nullable=True)  # Key telemetry features that triggered alert
    clinical_explanation = Column(Text, nullable=True)  # LLM Human explanation
    clinical_impact = Column(Text, nullable=True)  # Hospital operational impact
    recommended_mitigation = Column(Text, nullable=True)  # Step-by-step containment instructions
    explanation_status = Column(String, default="PENDING", index=True)  # PENDING, GENERATING, COMPLETED, FAILED, UNAVAILABLE
    ai_latency_ms = Column(Float, nullable=True)

    # Event Correlation & Aggregation
    correlation_id = Column(String, index=True, nullable=True)
    packet_count = Column(Integer, default=1)
    last_seen = Column(DateTime, default=datetime.utcnow, index=True)
    traffic_origin = Column(String, default="LIVE")  # LIVE, SIMULATOR, REPLAYED, GATEWAY
    
    # Resolution Status
    status = Column(String, default="NEW")  # NEW, INVESTIGATING, MITIGATED, FALSE_POSITIVE
    resolved_by = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

