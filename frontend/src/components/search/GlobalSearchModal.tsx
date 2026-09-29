import React, { useState, useEffect, useRef } from 'react';
import {
  Search, X, AlertTriangle, Monitor, BookOpen, Cpu, Zap,
  ArrowRight, Shield, Terminal
} from 'lucide-react';
import { Alert, Device } from '../../types';

interface GlobalSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  alerts: Alert[];
  devices: Device[];
  onSelectResult: (type: 'alert' | 'device' | 'research' | 'simulator' | 'analytics', item?: any) => void;
}

export const GlobalSearchModal: React.FC<GlobalSearchModalProps> = ({
  isOpen,
  onClose,
  alerts,
  devices,
  onSelectResult,
}) => {
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const q = query.toLowerCase().trim();

  // Static items searchable
  const staticItems = [
    {
      id: 'res-paper',
      type: 'research' as const,
      title: 'EdgeShield AI IEEE Research Paper',
      subtitle: 'Section III: Dual-Stage Detection ML Architecture & Isolation Forest',
      icon: BookOpen,
      category: 'Research Document',
      payload: { docId: 'DOC-IEEE-EDGESHIELD-2026', page: 3 }
    },
    {
      id: 'res-datasets',
      type: 'analytics' as const,
      title: 'Edge-IIoTset & N-BaIoT Dataset Methodology',
      subtitle: '14 multi-protocol IoT cyberattack categories benchmark metrics',
      icon: Shield,
      category: 'Dataset Methodology',
      payload: {}
    },
    {
      id: 'arch-iso-forest',
      type: 'analytics' as const,
      title: 'Stage 1: Isolation Forest Anomaly Boundary Filter',
      subtitle: 'Unsupervised zero-day detection in sub-millisecond edge time',
      icon: Cpu,
      category: 'Architecture Component',
      payload: {}
    },
    {
      id: 'arch-xgboost',
      type: 'analytics' as const,
      title: 'Stage 2: XGBoost Multi-Class Classifier',
      subtitle: 'Categorization of DICOM, MQTT, Modbus, and ARP vectors',
      icon: Cpu,
      category: 'Architecture Component',
      payload: {}
    },
    {
      id: 'sim-mqtt',
      type: 'simulator' as const,
      title: 'MQTT Flood DoS Attack Simulation Sandbox',
      subtitle: 'Generates telemetry burst to test rate limiter & isolation',
      icon: Zap,
      category: 'Attack Simulation',
      payload: { attack: 'MQTT Flood DoS' }
    },
    {
      id: 'sim-dicom',
      type: 'simulator' as const,
      title: 'DICOM Ransomware High-Entropy Encryption Sandbox',
      subtitle: 'Simulates unauthorized port 104 image repository locking',
      icon: Zap,
      category: 'Attack Simulation',
      payload: { attack: 'DICOM Ransomware' }
    },
    {
      id: 'sim-modbus',
      type: 'simulator' as const,
      title: 'Modbus Command Injection Simulation Sandbox',
      subtitle: 'Simulates port 502 unauthorized write command to ventilators',
      icon: Zap,
      category: 'Attack Simulation',
      payload: { attack: 'Modbus Command Injection' }
    }
  ];

  // Dynamic filter for Alerts
  const matchedAlerts = alerts.filter(a =>
    !q ||
    a.alert_id.toLowerCase().includes(q) ||
    a.threat_type.toLowerCase().includes(q) ||
    a.source_ip.toLowerCase().includes(q) ||
    a.protocol.toLowerCase().includes(q) ||
    (a.clinical_explanation && a.clinical_explanation.toLowerCase().includes(q))
  ).map(a => ({
    id: a.alert_id,
    type: 'alert' as const,
    title: `${a.threat_type} (${a.alert_id})`,
    subtitle: `Source: ${a.source_ip} • Target: ${a.target_device_id || 'Unknown'} • Severity: ${a.severity}`,
    icon: AlertTriangle,
    category: 'Security Incident',
    payload: a
  }));

  // Dynamic filter for Devices
  const matchedDevices = devices.filter(d =>
    !q ||
    d.device_id.toLowerCase().includes(q) ||
    d.name.toLowerCase().includes(q) ||
    d.category.toLowerCase().includes(q) ||
    d.ip_address.toLowerCase().includes(q) ||
    d.location.toLowerCase().includes(q) ||
    d.protocol.toLowerCase().includes(q)
  ).map(d => ({
    id: d.device_id,
    type: 'device' as const,
    title: `${d.name} (${d.device_id})`,
    subtitle: `${d.category} • IP: ${d.ip_address} • Location: ${d.location} • Status: ${d.status}`,
    icon: Monitor,
    category: 'Hospital Asset',
    payload: d
  }));

  // Filter static items
  const matchedStatic = staticItems.filter(s =>
    !q ||
    s.title.toLowerCase().includes(q) ||
    s.subtitle.toLowerCase().includes(q) ||
    s.category.toLowerCase().includes(q)
  );

  const allResults = [...matchedAlerts, ...matchedDevices, ...matchedStatic];

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-start justify-center pt-20 p-4">
      <div className="bg-card border rounded-3xl max-w-2xl w-full shadow-2xl overflow-hidden animate-in zoom-in-95">
        {/* Search Input Bar */}
        <div className="p-4 border-b flex items-center space-x-3 bg-secondary/50">
          <Search className="h-5 w-5 text-medical-teal shrink-0" />
          <input
            ref={inputRef}
            type="text"
            placeholder="Search incidents, devices, attack types, research, architecture... (e.g. MQTT, DICOM)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-sm font-medium outline-none placeholder:text-muted-foreground"
          />
          <button
            onClick={onClose}
            className="p-1 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground text-xs font-bold"
          >
            ESC
          </button>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-2 space-y-1 text-xs">
          {allResults.length === 0 ? (
            <div className="p-8 text-center text-muted-foreground">
              No matching cybersecurity incidents, medical assets, or research sections found.
            </div>
          ) : (
            allResults.map((res) => {
              const Icon = res.icon;
              return (
                <button
                  key={res.id}
                  onClick={() => {
                    onSelectResult(res.type, res.payload);
                    onClose();
                  }}
                  className="w-full text-left p-3 rounded-2xl hover:bg-secondary/70 flex items-center justify-between group transition-all"
                >
                  <div className="flex items-center space-x-3 overflow-hidden">
                    <div className="p-2 rounded-xl bg-secondary group-hover:bg-medical-teal/20 text-medical-teal transition-colors">
                      <Icon className="h-4 w-4" />
                    </div>
                    <div className="truncate">
                      <div className="font-bold text-foreground text-xs flex items-center space-x-2">
                        <span>{res.title}</span>
                        <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-secondary text-muted-foreground">
                          {res.category}
                        </span>
                      </div>
                      <div className="text-[11px] text-muted-foreground truncate mt-0.5">
                        {res.subtitle}
                      </div>
                    </div>
                  </div>
                  <ArrowRight className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 group-hover:text-medical-teal transition-all ml-2 shrink-0" />
                </button>
              );
            })
          )}
        </div>

        <div className="px-4 py-2 border-t bg-secondary/30 text-[11px] text-muted-foreground flex justify-between items-center font-mono">
          <span>Press ESC to close</span>
          <span>{allResults.length} index matches</span>
        </div>
      </div>
    </div>
  );
};
