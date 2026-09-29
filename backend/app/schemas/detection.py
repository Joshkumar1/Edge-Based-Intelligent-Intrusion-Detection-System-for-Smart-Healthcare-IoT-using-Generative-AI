from pydantic import BaseModel, Field
from typing import Dict, Optional, Any, List


class NetworkPacketInput(BaseModel):
    src_ip: str = Field(default="192.168.1.105", description="Source IP address")
    dst_ip: str = Field(default="192.168.1.50", description="Destination IP address (Target Device)")
    src_port: int = Field(default=49152, description="Source TCP/UDP Port")
    dst_port: int = Field(default=1883, description="Destination TCP/UDP Port (e.g., 1883 MQTT, 502 Modbus, 104 DICOM)")
    protocol: str = Field(default="MQTT", description="Protocol name")
    
    # Telemetry Features
    packet_length: float = Field(default=512.0, description="Packet size in bytes")
    flow_duration: float = Field(default=1.25, description="Flow duration in seconds")
    header_length: float = Field(default=32.0, description="Header size in bytes")
    byte_rate: float = Field(default=409.6, description="Transmission rate in bytes/sec")
    packet_rate: float = Field(default=10.0, description="Packet count per sec")
    tcp_syn_flag: int = Field(default=0, description="TCP SYN flag (1 or 0)")
    mqtt_msg_rate: float = Field(default=15.0, description="MQTT messages per sec")
    modbus_fn_code: int = Field(default=0, description="Modbus function code (e.g. 5, 6, 16)")
    entropy: float = Field(default=4.5, description="Payload byte entropy (0.0 to 8.0)")
    traffic_origin: Optional[str] = Field(default="LIVE", description="LIVE, SIMULATOR, REPLAYED, GATEWAY")
    correlation_id: Optional[str] = Field(default=None, description="Optional caller correlation ID")


class DetectionResult(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    threat_type: str
    confidence: float
    severity: str
    key_features: Dict[str, float]
    target_device_id: Optional[str] = None
    target_device_name: Optional[str] = None
    explanation: Optional[str] = None
    impact: Optional[str] = None
    mitigation: Optional[str] = None
    
    # Canonical Tracing & Latency Metrics
    event_id: Optional[str] = None
    correlation_id: Optional[str] = None
    observation_type: Optional[str] = None
    device_match_status: Optional[str] = None
    traffic_origin: Optional[str] = "LIVE"
    explanation_status: Optional[str] = "PENDING"
    detection_latency_ms: float = 0.0
    ai_explanation_latency_ms: Optional[float] = None
    alert_id: Optional[str] = None
    packet_count: int = 1

