from enum import Enum
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class TrafficOrigin(str, Enum):
    LIVE = "LIVE"
    SIMULATOR = "SIMULATOR"
    REPLAYED = "REPLAYED"
    GATEWAY = "GATEWAY"
    MACHINE_DIRECT = "MACHINE_DIRECT"


class DeviceMatchStatus(str, Enum):
    MATCHED = "MATCHED"
    UNREGISTERED = "UNREGISTERED"
    AMBIGUOUS = "AMBIGUOUS"


class ObservationType(str, Enum):
    NORMAL_OBSERVATION = "NORMAL_OBSERVATION"
    ANOMALOUS_OBSERVATION = "ANOMALOUS_OBSERVATION"
    SECURITY_ALERT = "SECURITY_ALERT"


class ExplanationStatus(str, Enum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    UNAVAILABLE = "UNAVAILABLE"


class StageLatencyMetrics(BaseModel):
    ingestion_ms: float = 0.0
    normalization_ms: float = 0.0
    feature_extraction_ms: float = 0.0
    anomaly_detection_ms: float = 0.0
    classifier_ms: float = 0.0
    persistence_ms: float = 0.0
    websocket_ms: float = 0.0
    total_detection_ms: float = 0.0
    ai_explanation_ms: Optional[float] = None


class SecurityEvent(BaseModel):
    """
    Canonical strongly typed representation of an edge security observation.
    Traces one observation from ingestion through normalization, device resolution,
    feature extraction, ML inference, persistence, WebSocket broadcast, and async AI enrichment.
    """
    event_id: str = Field(..., description="Unique event identifier (e.g. EVT-UUID)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event creation timestamp")
    
    # Provenance and Network Context
    source: TrafficOrigin = Field(default=TrafficOrigin.LIVE, description="Telemetry traffic provenance")
    source_ip: str
    source_port: int
    destination_ip: str
    destination_port: int
    protocol: str
    
    # Device Context & Strict Resolution
    device_id: str = Field(default="DEV-UNREGISTERED", description="Registered Device ID or DEV-UNREGISTERED")
    device_match_status: DeviceMatchStatus = Field(default=DeviceMatchStatus.UNREGISTERED)
    device_name: Optional[str] = None
    device_category: Optional[str] = None
    device_location: Optional[str] = None
    
    # Telemetry and Features
    raw_telemetry: Dict[str, Any] = Field(default_factory=dict)
    extracted_features: Dict[str, float] = Field(default_factory=dict)
    
    # ML Evidence (Separated from policy/enforcement)
    anomaly_score: float = Field(default=0.0, description="Normalized Isolation Forest anomaly score [0.0, 1.0]")
    anomaly_detected: bool = Field(default=False)
    classifier_prediction: str = Field(default="Normal")
    classifier_confidence: float = Field(default=0.0)
    threat_type: str = Field(default="Normal")
    severity: str = Field(default="INFORMATIONAL")  # CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL
    
    # Pipeline & Model Lineage
    observation_type: ObservationType = Field(default=ObservationType.NORMAL_OBSERVATION)
    model_version: str = Field(default="v2.1-edge-hybrid")
    feature_schema_version: str = Field(default="schema-v1.0")
    detection_pipeline_version: str = Field(default="pipeline-v2.0-canonical")
    correlation_id: str = Field(..., description="Correlation key/ID linking related flow events")
    
    # Processing Metrics & Timestamps
    processing_timestamps: Dict[str, float] = Field(default_factory=dict)
    latency_metrics: StageLatencyMetrics = Field(default_factory=StageLatencyMetrics)
    
    # AI Enrichment Lifecycle
    explanation_status: ExplanationStatus = Field(default=ExplanationStatus.PENDING)
    explanation: Optional[str] = None
    clinical_impact: Optional[str] = None
    recommended_mitigation: Optional[str] = None
    ai_engine_used: Optional[str] = None
    
    # Correlated Alert & Enforcement Recommendation (Policy Output, NOT Automated Action)
    alert_id: Optional[str] = None
    packet_count: int = 1
    enforcement_recommendation: Optional[str] = None  # e.g. "RECOMMEND_ISOLATION", "MONITOR"
    enforcement_status: str = "NONE"  # NONE, RECOMMENDED (Enforcement only executed via Task 1 authorized API)


class WebSocketEventEnvelope(BaseModel):
    """Structured contract for all WebSocket broadcasts."""
    event_type: str  # security_event, alert_created, alert_updated, ai_enrichment, telemetry
    event_id: str
    timestamp: str
    correlation_id: str
    payload: Dict[str, Any]
