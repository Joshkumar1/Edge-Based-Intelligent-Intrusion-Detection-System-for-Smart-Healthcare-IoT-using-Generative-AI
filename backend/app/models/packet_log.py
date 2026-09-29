from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base


class PacketLog(Base):
    __tablename__ = "packet_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    src_ip = Column(String, nullable=False)
    dst_ip = Column(String, nullable=False)
    src_port = Column(Integer, nullable=False)
    dst_port = Column(Integer, nullable=False)
    protocol = Column(String, nullable=False)
    
    # IoT Telemetry Features
    packet_length = Column(Float, nullable=False)
    flow_duration = Column(Float, nullable=False)
    header_length = Column(Float, nullable=False)
    byte_rate = Column(Float, nullable=False)
    packet_rate = Column(Float, nullable=False)
    tcp_syn_flag = Column(Integer, default=0)
    mqtt_msg_rate = Column(Float, default=0.0)
    modbus_fn_code = Column(Integer, default=0)
    entropy = Column(Float, default=0.0)
    
    # Canonical Event Tracing
    event_id = Column(String, index=True, nullable=True)
    correlation_id = Column(String, index=True, nullable=True)
    device_id = Column(String, index=True, nullable=True)
    traffic_origin = Column(String, default="LIVE")  # LIVE, SIMULATOR, REPLAYED, GATEWAY
    detection_latency_ms = Column(Float, default=0.0)
    
    # Classification Result
    is_anomaly = Column(Integer, default=0)
    predicted_label = Column(String, default="Normal")
    threat_score = Column(Float, default=0.0)

