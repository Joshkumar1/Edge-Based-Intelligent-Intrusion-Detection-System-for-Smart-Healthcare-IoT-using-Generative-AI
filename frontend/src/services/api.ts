import { Device, Alert, DashboardStats, MLMetrics, NetworkPacket } from '../types';

const API_BASE = '/api/v1';

export const apiService = {
  // Dashboard Stats
  async getDashboardStats(): Promise<DashboardStats> {
    try {
      const res = await fetch(`${API_BASE}/dashboard/stats`);
      if (!res.ok) throw new Error('API Error');
      return await res.json();
    } catch {
      // Fallback mock stats
      return {
        total_devices: 18,
        active_alerts: 4,
        critical_alerts: 1,
        devices_at_risk: 3,
        threat_distribution: {
          'DICOM Ransomware': 1,
          'MQTT Flood DoS': 2,
          'Modbus Command Injection': 1,
        },
        system_health: 'ELEVATED_THREAT',
        edge_ai_status: 'ONLINE (0.84ms Latency)',
      };
    }
  },

  // Devices
  async getDevices(): Promise<Device[]> {
    try {
      const res = await fetch(`${API_BASE}/devices/`);
      if (!res.ok) throw new Error('API Error');
      return await res.json();
    } catch {
      return [
        {
          id: 1,
          device_id: 'DEV-ICU-101',
          name: 'ICU Telemetry Station A',
          category: 'ICU Telemetry Station',
          ip_address: '192.168.10.101',
          mac_address: '00:1A:2B:3C:4D:5E',
          location: 'ICU Wing B - Room 301',
          firmware_version: 'v4.2.1-sec',
          status: 'Active',
          risk_score: 12.0,
          protocol: 'Modbus/TCP',
          last_seen: new Date().toISOString(),
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          device_id: 'DEV-PUMP-204',
          name: 'Alaris Infusion Pump #4',
          category: 'Infusion Pump',
          ip_address: '192.168.10.102',
          mac_address: '00:1A:2B:99:88:77',
          location: 'Pediatrics - Room 104',
          firmware_version: 'v2.1.0',
          status: 'Warning',
          risk_score: 68.5,
          protocol: 'MQTT',
          last_seen: new Date().toISOString(),
          created_at: new Date().toISOString(),
        },
        {
          id: 3,
          device_id: 'DEV-RAD-405',
          name: 'Siemens DICOM Radiology Workstation',
          category: 'DICOM Radiology Workstation',
          ip_address: '192.168.10.104',
          mac_address: '00:1A:2B:11:22:33',
          location: 'Radiology Imaging Bay 2',
          firmware_version: 'v5.1.2',
          status: 'Critical',
          risk_score: 94.0,
          protocol: 'DICOM',
          last_seen: new Date().toISOString(),
          created_at: new Date().toISOString(),
        },
        {
          id: 4,
          device_id: 'DEV-VENT-301',
          name: 'Puritan Bennett Ventilator',
          category: 'Smart Ventilator',
          ip_address: '192.168.10.103',
          mac_address: '00:1A:2B:44:55:66',
          location: 'ICU Wing A - Room 102',
          firmware_version: 'v3.0.4',
          status: 'Active',
          risk_score: 5.0,
          protocol: 'Modbus',
          last_seen: new Date().toISOString(),
          created_at: new Date().toISOString(),
        },
      ];
    }
  },

  // Alerts
  async getAlerts(severity?: string, status?: string): Promise<Alert[]> {
    try {
      let url = `${API_BASE}/alerts/`;
      const params = new URLSearchParams();
      if (severity) params.append('severity', severity);
      if (status) params.append('status', status);
      if (params.toString()) url += `?${params.toString()}`;

      const res = await fetch(url);
      if (!res.ok) throw new Error('API Error');
      return await res.json();
    } catch {
      return [
        {
          id: 101,
          alert_id: 'ALT-8A4F129B',
          timestamp: new Date(Date.now() - 14 * 60000).toISOString(),
          source_ip: '172.16.8.204',
          destination_ip: '192.168.10.104',
          target_device_id: 'DEV-RAD-405',
          protocol: 'DICOM',
          anomaly_score: 0.94,
          is_anomaly: 1,
          threat_type: 'DICOM Ransomware',
          confidence: 0.96,
          severity: 'CRITICAL',
          key_features: { packet_length: 1450.0, byte_rate: 28500.0, entropy: 7.88 },
          clinical_explanation:
            'An unauthorized external host (172.16.8.204) is transferring highly encrypted payload data (Byte Entropy: 7.88/8.0) into the Siemens DICOM Radiology Workstation at Radiology Imaging Bay 2. This pattern matches ransomware targeting PACS radiology image repositories.',
          clinical_impact:
            'High patient care risk: Ransomware encryption could lock radiology scans (CT/MRI), delaying emergency surgical procedures and compromising patient medical history integrity.',
          recommended_mitigation:
            '1. Instantly isolate Siemens DICOM Radiology Workstation at network switch VLAN boundary.\n2. Block TCP port 104 and incoming traffic from host 172.16.8.204.\n3. Verify shadow volume backups for DICOM imaging repositories before rebooting.',
          status: 'NEW',
        },
        {
          id: 102,
          alert_id: 'ALT-3C9D77E1',
          timestamp: new Date(Date.now() - 42 * 60000).toISOString(),
          source_ip: '10.0.4.88',
          destination_ip: '192.168.10.102',
          target_device_id: 'DEV-PUMP-204',
          protocol: 'MQTT',
          anomaly_score: 0.72,
          is_anomaly: 1,
          threat_type: 'MQTT Flood DoS',
          confidence: 0.89,
          severity: 'HIGH',
          key_features: { mqtt_msg_rate: 415.0, packet_rate: 370.0 },
          clinical_explanation:
            'A massive surge of telemetry messages (415 msgs/sec) is flooding the MQTT broker connected to Alaris Infusion Pump #4 at Pediatrics - Room 104. This Denial of Service packet burst is exhausting processing bandwidth.',
          clinical_impact:
            'Operational risk: Infusion pump rate adjustments or telemetry alarm alerts may experience severe latency, preventing nursing staff from receiving real-time patient medication updates.',
          recommended_mitigation:
            '1. Enable rate limiting on MQTT broker for IP 10.0.4.88.\n2. Force re-authentication of all IoT client publish certificates.\n3. Verify physical patient infusion pump state at Pediatrics - Room 104.',
          status: 'INVESTIGATING',
        },
      ];
    }
  },

  async updateAlertStatus(alert_id: string, status: string): Promise<Alert> {
    const res = await fetch(`${API_BASE}/alerts/${alert_id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, resolved_by: 'Hospital IT Admin' }),
    });
    return await res.json();
  },

  // Packet Simulation
  async simulatePacket(attack_type: string = 'random'): Promise<any> {
    const res = await fetch(`${API_BASE}/detection/simulate?attack_type=${attack_type}`, {
      method: 'POST',
    });
    return await res.json();
  },

  // ML Metrics
  async getMLMetrics(): Promise<MLMetrics> {
    try {
      const res = await fetch(`${API_BASE}/analytics/metrics`);
      if (!res.ok) throw new Error('API Error');
      return await res.json();
    } catch {
      return {
        features: [
          'packet_length', 'flow_duration', 'header_length', 'byte_rate',
          'packet_rate', 'tcp_syn_flag', 'mqtt_msg_rate', 'modbus_fn_code', 'entropy'
        ],
        labels: [
          'Normal', 'DICOM Ransomware', 'MQTT Flood DoS',
          'Modbus Command Injection', 'ARP Spoofing MITM', 'Port Scan Reconnaissance'
        ],
        metrics: {
          macro_precision: 0.9924,
          macro_recall: 0.9891,
          macro_f1: 0.9907
        }
      };
    }
  }
};
