export type DeviceCategory =
  | 'Infusion Pump'
  | 'Patient Monitor'
  | 'ICU Telemetry Station'
  | 'DICOM Radiology Workstation'
  | 'Smart Ventilator'
  | 'Smart Syringe Driver'
  | 'Hospital Edge Security Gateway';

export type DeviceStatus = 'Active' | 'Warning' | 'Critical' | 'Isolated' | 'Offline';

export interface Device {
  id: number;
  device_id: string;
  name: string;
  category: DeviceCategory | string;
  ip_address: string;
  mac_address: string;
  location: string;
  firmware_version: string;
  status: DeviceStatus | string;
  risk_score: number;
  protocol: string;
  last_seen: string;
  created_at: string;
}

export type SeverityLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFORMATIONAL';
export type AlertStatus = 'NEW' | 'INVESTIGATING' | 'MITIGATED' | 'FALSE_POSITIVE';

export interface Alert {
  id: number;
  alert_id: string;
  timestamp: string;
  source_ip: string;
  destination_ip: string;
  target_device_id?: string;
  target_device_name?: string;
  protocol: string;
  anomaly_score: number;
  is_anomaly: number;
  threat_type: string;
  confidence: number;
  severity: SeverityLevel;
  key_features?: Record<string, number>;
  clinical_explanation?: string;
  clinical_impact?: string;
  recommended_mitigation?: string;
  explanation_status?: 'PENDING' | 'GENERATING' | 'COMPLETED' | 'FAILED' | 'UNAVAILABLE';
  ai_latency_ms?: number;
  correlation_id?: string;
  packet_count?: number;
  traffic_origin?: 'LIVE' | 'SIMULATOR' | 'REPLAYED' | 'GATEWAY';
  status: AlertStatus;
  resolved_by?: string;
  resolved_at?: string;
}

export interface NetworkPacket {
  src_ip: string;
  dst_ip: string;
  src_port: number;
  dst_port: number;
  protocol: string;
  packet_length: number;
  flow_duration: number;
  header_length: number;
  byte_rate: number;
  packet_rate: number;
  tcp_syn_flag: number;
  mqtt_msg_rate: number;
  modbus_fn_code: number;
  entropy: number;
  device_id?: string;
  device_name?: string;
  location?: string;
}

export interface TelemetryStreamEvent {
  type: 'TELEMETRY_PACKET' | string;
  event_type?: string;
  event_id?: string;
  correlation_id?: string;
  source?: 'LIVE' | 'SIMULATOR' | 'REPLAYED' | 'GATEWAY' | string;
  timestamp: string;
  packet: NetworkPacket;
  detection: {
    is_anomaly: boolean;
    anomaly_score: number;
    threat_type: string;
    confidence: number;
    severity: SeverityLevel;
    key_features: Record<string, number>;
  };
  detection_latency_ms?: number;
}

export interface DashboardStats {
  total_devices: number;
  active_alerts: number;
  critical_alerts: number;
  devices_at_risk: number;
  threat_distribution: Record<string, number>;
  system_health: 'OPTIMAL' | 'ELEVATED_THREAT' | 'CRITICAL';
  edge_ai_status: string;
  detection_latency_ms?: number;
  ai_latency_ms?: number;
}


export interface MLMetrics {
  features: string[];
  labels: string[];
  metrics: {
    macro_precision: number;
    macro_recall: number;
    macro_f1: number;
  };
}

// Document / Research Paper Types
export interface DocumentSection {
  heading: string;
  content: string;
}

export interface DocumentPage {
  page_number: number;
  title: string;
  sections: DocumentSection[];
  doc_id?: string;
  doc_title?: string;
  total_pages?: number;
}

export interface DocumentItem {
  id: string;
  title: string;
  filename: string;
  file_size_bytes: number;
  total_pages: number;
  uploaded_at: string;
  category: string;
  summary: string;
  is_default?: boolean;
  pages?: DocumentPage[];
}

export interface DocumentSearchResult {
  doc_id: string;
  doc_title: string;
  page_number: number;
  section: string;
  match_count: number;
  snippet: string;
}

// Unified Copilot Types
export type CopilotContextType = 'research' | 'incident' | 'device' | 'architecture' | 'telemetry';

export interface SourceAttribution {
  type: string; // 'Research Document' | 'Security Telemetry' | 'ML Prediction' | 'General Knowledge'
  detail: string;
}

export interface CopilotRequest {
  context_type: CopilotContextType;
  query: string;
  context_id?: string;
  context_data?: Record<string, any>;
}

export interface CopilotResponse {
  summary: string;
  evidence?: string;
  analysis?: string;
  recommended_mitigation?: string;
  sources: SourceAttribution[];
  page_reference?: number;
  document_title?: string;
  section?: string;
  ai_engine_used: string;
}

// Direct Machine Signals & Cyber Defense Types
export type SignalIntegrityStatus =
  | 'VERIFIED'
  | 'ANOMALOUS_VALUE'
  | 'REPLAY_ATTACK'
  | 'SIGNATURE_INVALID'
  | 'PHYSICAL_INVARIANT_BREACH'
  | 'MALFORMED';

export type CyberDefenseMode = 'PASSIVE_MONITOR' | 'ASSISTED_DEFENSE' | 'ACTIVE_PREVENTION';

export type DefenseActionType =
  | 'NONE'
  | 'LOG_ALERT'
  | 'SIGNAL_DROP'
  | 'SAFETY_INTERLOCK_ENGAGED'
  | 'FIREWALL_ISOLATE';

export interface MachineSignalAnalysisResult {
  signal_id: string;
  device_id: string;
  device_name: string;
  device_category: string;
  timestamp: string;
  seq_num: number;
  integrity_status: SignalIntegrityStatus;
  physical_invariant_breach: boolean;
  breach_details?: string;
  anomaly_score: number;
  is_threat: boolean;
  threat_type: string;
  severity: SeverityLevel;
  defense_mode: CyberDefenseMode;
  defense_action_taken: DefenseActionType;
  clinical_safety_interlock: boolean;
  enforcement_details?: Record<string, any>;
  alert_id?: string;
  latency_ms: number;
  payload: Record<string, any>;
}

export interface CollectorStatus {
  collector_id: string;
  name: string;
  collector_type: string;
  status: 'RUNNING' | 'STOPPED' | 'ERROR';
  endpoint: string;
  signals_received: number;
  signals_rejected: number;
  last_signal_time?: string;
  description: string;
}

export interface DefensePolicyConfig {
  mode: CyberDefenseMode;
  auto_isolate_critical: boolean;
  engage_safety_interlocks: boolean;
  anti_replay_enforcement: boolean;
  rate_limit_per_machine_hz?: number;
  alert_escalation_threshold?: number;
}

export interface ClinicalSafetyInterlock {
  id: number;
  device_id: string;
  engaged_at: string;
  reason: string;
  trigger_signal_id?: string;
  safe_state_mode: string;
  is_active: boolean;
}

export interface CybersecurityMetrics {
  total_signals_processed: number;
  total_breaches_detected: number;
  total_replay_attacks_blocked: number;
  total_interlocks_engaged: number;
  total_quarantines_enforced: number;
  current_defense_mode: CyberDefenseMode;
  auto_isolate_active: boolean;
  anti_replay_enforcement: boolean;
}

export interface MachineSignalHistoryItem {
  id: number;
  signal_id: string;
  device_id: string;
  timestamp: string;
  signal_type: string;
  seq_num: number;
  integrity_status: SignalIntegrityStatus;
  physical_invariant_breach: boolean;
  breach_details?: string;
  anomaly_score: number;
  is_threat: boolean;
  threat_type: string;
  severity: SeverityLevel;
  defense_action: DefenseActionType;
  clinical_interlock: boolean;
  payload: Record<string, any>;
  alert_id?: string;
}

