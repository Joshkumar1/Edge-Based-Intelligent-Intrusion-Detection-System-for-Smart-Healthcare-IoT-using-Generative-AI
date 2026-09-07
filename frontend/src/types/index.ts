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
  type: 'TELEMETRY_PACKET';
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
}

export interface DashboardStats {
  total_devices: number;
  active_alerts: number;
  critical_alerts: number;
  devices_at_risk: number;
  threat_distribution: Record<string, number>;
  system_health: 'OPTIMAL' | 'ELEVATED_THREAT' | 'CRITICAL';
  edge_ai_status: string;
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
