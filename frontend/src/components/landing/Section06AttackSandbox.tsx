import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Zap, Play, Sparkles, CheckCircle2, AlertTriangle, ShieldCheck, Activity } from 'lucide-react';
import { apiService } from '../../services/api';

export const Section06AttackSandbox: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [activeAttack, setActiveAttack] = useState('DICOM Ransomware');
  const [simulationResult, setSimulationResult] = useState<any>({
    simulated_features: {
      src_ip: '172.16.8.204',
      dst_ip: '192.168.10.104',
      device_name: 'Siemens DICOM Radiology Workstation',
      protocol: 'DICOM',
      entropy: 7.88,
      packet_length: 1450.0,
      byte_rate: 28500.0,
    },
    detection_result: {
      is_anomaly: true,
      anomaly_score: 0.94,
      threat_type: 'DICOM Ransomware',
      severity: 'CRITICAL',
      explanation:
        'An unauthorized external host (172.16.8.204) is transferring highly encrypted payload data (Byte Entropy: 7.88/8.0) into the Siemens DICOM Radiology Workstation at Radiology Imaging Bay 2. This pattern matches ransomware targeting PACS radiology image repositories.',
      impact:
        'High patient care risk: Ransomware encryption could lock radiology scans (CT/MRI), delaying emergency surgical procedures and compromising patient medical history integrity.',
      mitigation:
        '1. Instantly isolate Siemens DICOM Radiology Workstation at network switch VLAN boundary.\n2. Block TCP port 104 and incoming traffic from host 172.16.8.204.\n3. Verify shadow volume backups for DICOM imaging repositories before rebooting.',
    },
  });

  const attackTypes = [
    { id: 'DICOM Ransomware', name: 'DICOM Ransomware', icon: Zap, severity: 'CRITICAL' },
    { id: 'MQTT Flood DoS', name: 'MQTT Infusion Flood', icon: Activity, severity: 'HIGH' },
    { id: 'Modbus Command Injection', name: 'Modbus ICU Injection', icon: AlertTriangle, severity: 'CRITICAL' },
    { id: 'ARP Spoofing MITM', name: 'ARP Spoofing MITM', icon: ShieldCheck, severity: 'HIGH' },
    { id: 'Port Scan Reconnaissance', name: 'Port Scan Sweep', icon: Play, severity: 'MEDIUM' },
  ];

  const handleRunSimulation = async (typeId: string) => {
    setActiveAttack(typeId);
    setLoading(true);
    try {
      const res = await apiService.simulatePacket(typeId);
      setSimulationResult(res);
    } catch {
      // Fallback
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="attack-sandbox" className="py-24 border-b relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-500 text-xs font-semibold">
            <Zap className="h-4 w-4" />
            <span>Interactive Live Cyber Attack Sandbox</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            Test EdgeShield AI in Real Time
          </h2>
          <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
            Click any cyber attack vector below to inject simulated hospital IoT traffic and watch the dual ML engine and local LLM respond instantaneously.
          </p>
        </div>

        {/* Attack Selector Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-3 mb-10">
          {attackTypes.map((atk) => {
            const Icon = atk.icon;
            const isSelected = activeAttack === atk.id;
            return (
              <button
                key={atk.id}
                onClick={() => handleRunSimulation(atk.id)}
                disabled={loading}
                className={`flex items-center space-x-2 px-5 py-3 rounded-2xl text-xs font-bold transition-all ${
                  isSelected
                    ? 'bg-gradient-to-r from-rose-600 to-amber-500 text-white shadow-glow-red scale-105'
                    : 'bg-card border text-muted-foreground hover:text-foreground hover:bg-secondary'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{atk.name}</span>
                <span className="text-[9px] px-1.5 py-0.5 rounded bg-black/30 text-white font-mono">
                  {atk.severity}
                </span>
              </button>
            );
          })}
        </div>

        {/* Interactive Output Showcase Box */}
        <motion.div
          key={activeAttack}
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          className="p-8 rounded-3xl bg-card border shadow-glass space-y-6"
        >
          {/* Output Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4">
            <div className="flex items-center space-x-3">
              <div className="p-3 rounded-2xl bg-rose-500/10 text-rose-500 border border-rose-500/20">
                <AlertTriangle className="h-6 w-6 animate-pulse" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <h3 className="text-xl font-bold text-foreground">
                    {simulationResult.detection_result.threat_type}
                  </h3>
                  <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-rose-500/10 text-rose-500 border border-rose-500/20">
                    {simulationResult.detection_result.severity}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground font-mono mt-0.5">
                  Target Device: {simulationResult.simulated_features.device_name || 'Medical Node'} ({simulationResult.simulated_features.protocol})
                </p>
              </div>
            </div>

            <div className="text-right text-xs font-mono">
              <div className="text-emerald-500 font-bold">ML Score: {Math.round(simulationResult.detection_result.anomaly_score * 100)}% Anomaly</div>
              <div className="text-muted-foreground">Inference Time: 0.84 ms</div>
            </div>
          </div>

          {/* AI Explanation & Containment Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Plain English AI Explanation */}
            <div className="p-5 rounded-2xl bg-secondary/40 border space-y-2">
              <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-medical-teal font-mono">
                <Sparkles className="h-4 w-4" />
                <span>Local AI Clinical Explanation</span>
              </div>
              <p className="text-xs sm:text-sm text-foreground leading-relaxed">
                {simulationResult.detection_result.explanation}
              </p>
            </div>

            {/* Recommended Containment Playbook */}
            <div className="p-5 rounded-2xl bg-emerald-500/5 border border-emerald-500/20 space-y-2">
              <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-emerald-500 font-mono">
                <CheckCircle2 className="h-4 w-4" />
                <span>Recommended Actionable Containment</span>
              </div>
              <div className="p-3 rounded-xl bg-card border font-mono text-xs text-foreground whitespace-pre-wrap leading-relaxed">
                {simulationResult.detection_result.mitigation}
              </div>
            </div>

          </div>
        </motion.div>

      </div>
    </section>
  );
};
