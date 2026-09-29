import React, { useState } from 'react';
import { Zap, Play, ShieldAlert, Sparkles, CheckCircle2 } from 'lucide-react';
import { apiService } from '../../services/api';
import { Alert } from '../../types';

interface AttackSimulatorProps {
  onAlertGenerated: (alert: Alert) => void;
}

export const AttackSimulator: React.FC<AttackSimulatorProps> = ({ onAlertGenerated }) => {
  const [loading, setLoading] = useState(false);
  const [lastResult, setLastResult] = useState<any>(null);

  const handleSimulate = async (attackType: string) => {
    setLoading(true);
    try {
      const res = await apiService.simulatePacket(attackType);
      setLastResult(res);

      // Truthful state sync: update parent alert center if an alert was produced
      if (res?.detection_result?.is_anomaly && res?.alert_id) {
        const det = res.detection_result;
        const generatedAlert: Alert = {
          id: Date.now(),
          alert_id: res.alert_id,
          timestamp: new Date().toISOString(),
          source_ip: res.simulated_features?.src_ip || '10.0.4.88',
          destination_ip: res.simulated_features?.dst_ip || '192.168.10.104',
          target_device_id: det.target_device_id,
          target_device_name: det.target_device_name,
          protocol: res.simulated_features?.protocol || 'TCP',
          anomaly_score: det.anomaly_score,
          is_anomaly: 1,
          threat_type: det.threat_type,
          confidence: det.confidence,
          severity: det.severity,
          key_features: det.key_features,
          clinical_explanation: det.explanation,
          clinical_impact: det.impact,
          recommended_mitigation: det.mitigation,
          status: 'NEW',
          traffic_origin: 'SIMULATOR',
          explanation_status: det.explanation_status || 'PENDING'
        };
        onAlertGenerated(generatedAlert);
      }
    } catch (e) {
      console.error('Simulation error', e);
    } finally {
      setLoading(false);
    }
  };

  const attackPresets = [
    {
      id: 'DICOM Ransomware',
      title: 'DICOM Radiology Ransomware Burst',
      desc: 'Simulates high byte entropy (7.88/8.0) payload encryption targeting Siemens DICOM PACS Workstation.',
      severity: 'CRITICAL',
    },
    {
      id: 'MQTT Flood DoS',
      title: 'Infusion Pump MQTT Telemetry Flood',
      desc: 'Simulates 420 msgs/sec publish rate flood overwhelming Alaris Infusion Pump #4.',
      severity: 'HIGH',
    },
    {
      id: 'Modbus Command Injection',
      title: 'ICU Ventilator Modbus Register Injection',
      desc: 'Simulates unauthorized Modbus write function codes (FC16) targeting Puritan Bennett Ventilator.',
      severity: 'CRITICAL',
    },
    {
      id: 'ARP Spoofing MITM',
      title: 'ARP Spoofing Man-In-The-Middle',
      desc: 'Simulates MAC address forgery to intercept central nursing monitor telemetry.',
      severity: 'HIGH',
    },
    {
      id: 'Port Scan Reconnaissance',
      title: 'Sequential TCP SYN Port Reconnaissance',
      desc: 'Simulates rapid TCP SYN sweeps across medical IoT device subnet ports.',
      severity: 'MEDIUM',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-2xl font-bold tracking-tight">Interactive IoT Attack Simulator</h2>
            <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-amber-500/10 text-amber-500 border border-amber-500/20">
              Simulated Provenance
            </span>
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            Inject realistic smart hospital cyber attack vectors into the canonical edge pipeline. Detections are labeled SIMULATOR to prevent mixing with live telemetry.
          </p>
        </div>
      </div>

      {/* Preset Buttons Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {attackPresets.map((preset) => (
          <div
            key={preset.id}
            className="p-5 rounded-2xl bg-card border shadow-subtle flex flex-col justify-between space-y-4 hover:border-medical-teal/40 transition-all"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span
                  className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    preset.severity === 'CRITICAL'
                      ? 'bg-rose-500/10 text-rose-500 border border-rose-500/20'
                      : 'bg-amber-500/10 text-amber-500 border border-amber-500/20'
                  }`}
                >
                  {preset.severity}
                </span>
                <Zap className="h-4 w-4 text-rose-500" />
              </div>
              <h4 className="font-bold text-base text-foreground">{preset.title}</h4>
              <p className="text-xs text-muted-foreground leading-relaxed">{preset.desc}</p>
            </div>

            <button
              onClick={() => handleSimulate(preset.id)}
              disabled={loading}
              className="w-full flex items-center justify-center space-x-2 py-2.5 rounded-xl bg-gradient-to-r from-rose-600 to-amber-500 hover:opacity-95 text-white font-bold text-xs shadow-glow-red transition-all disabled:opacity-50"
            >
              <Play className="h-3.5 w-3.5 fill-current" />
              <span>{loading ? 'Processing Pipeline...' : 'Inject Attack Vector'}</span>
            </button>
          </div>
        ))}
      </div>

      {/* Simulation Result Box */}
      {lastResult && (
        <div className="p-6 rounded-2xl bg-card border shadow-subtle space-y-4 animate-in fade-in">
          <div className="flex items-center justify-between border-b pb-3">
            <div className="flex items-center space-x-2 text-emerald-500 font-bold text-base">
              <CheckCircle2 className="h-5 w-5" />
              <span>Injected & Processed by Canonical Security Pipeline</span>
            </div>
            <span className="text-[10px] font-mono uppercase bg-secondary px-2.5 py-1 rounded-md text-muted-foreground border">
              Provenance: {lastResult.traffic_origin || 'SIMULATOR'}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="p-4 rounded-xl bg-secondary/50 border space-y-2">
              <div className="font-bold uppercase tracking-wider text-muted-foreground flex justify-between">
                <span>ML Detection Evidence</span>
                <span className="text-emerald-500 font-mono">
                  {lastResult.detection_result.detection_latency_ms ? `${lastResult.detection_result.detection_latency_ms.toFixed(2)} ms` : 'sub-millisecond'}
                </span>
              </div>
              <div className="space-y-1">
                <div>Threat Type: <strong className="text-foreground font-mono">{lastResult.detection_result.threat_type}</strong></div>
                <div>Anomaly Score: <strong className="text-rose-500 font-mono">{(lastResult.detection_result.anomaly_score * 100).toFixed(1)}%</strong></div>
                <div>Confidence: <strong className="text-foreground font-mono">{(lastResult.detection_result.confidence * 100).toFixed(1)}%</strong></div>
                <div>Severity: <strong className="text-foreground">{lastResult.detection_result.severity}</strong></div>
                <div>Target Device: <strong className="text-foreground font-mono">{lastResult.detection_result.target_device_id || 'DEV-UNREGISTERED'}</strong> ({lastResult.detection_result.device_match_status || 'UNREGISTERED'})</div>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-medical-teal/10 border border-medical-teal/20 space-y-2">
              <div className="font-bold uppercase tracking-wider text-medical-teal flex items-center justify-between">
                <div className="flex items-center space-x-1">
                  <Sparkles className="h-4 w-4" />
                  <span>AI Clinical Explanation</span>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-medical-teal/20 text-medical-teal border border-medical-teal/30">
                  {lastResult.detection_result.explanation_status || 'PENDING'}
                </span>
              </div>
              <p className="text-foreground leading-relaxed">
                {lastResult.detection_result.explanation || 'AI explanation is being generated asynchronously by local Ollama...'}
              </p>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
