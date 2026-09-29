import React, { useState, useEffect } from 'react';
import {
  Activity,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Zap,
  Radio,
  Server,
  AlertTriangle,
  RotateCcw,
  Play,
  CheckCircle2,
  XCircle,
  Cpu,
  Lock,
  Clock,
  Sparkles,
  Flame,
  ArrowUpRight,
  Filter,
  RefreshCw,
  Power
} from 'lucide-react';
import { apiService } from '../../services/api';
import {
  CollectorStatus,
  DefensePolicyConfig,
  CyberDefenseMode,
  ClinicalSafetyInterlock,
  MachineSignalHistoryItem,
  MachineSignalAnalysisResult,
  CybersecurityMetrics,
} from '../../types';

export const MachineSignalsView: React.FC = () => {
  const [defensePolicy, setDefensePolicy] = useState<DefensePolicyConfig>({
    mode: 'ACTIVE_PREVENTION',
    auto_isolate_critical: true,
    engage_safety_interlocks: true,
    anti_replay_enforcement: true,
  });

  const [collectors, setCollectors] = useState<CollectorStatus[]>([]);
  const [liveSignals, setLiveSignals] = useState<Record<string, any>>({});
  const [interlocks, setInterlocks] = useState<ClinicalSafetyInterlock[]>([]);
  const [metrics, setMetrics] = useState<CybersecurityMetrics>({
    total_signals_processed: 0,
    total_breaches_detected: 0,
    total_replay_attacks_blocked: 0,
    total_interlocks_engaged: 0,
    total_quarantines_enforced: 0,
    current_defense_mode: 'ACTIVE_PREVENTION',
    auto_isolate_active: true,
    anti_replay_enforcement: true,
  });

  const [history, setHistory] = useState<MachineSignalHistoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedScenario, setSelectedScenario] = useState<string>('infusion_overdose');
  const [selectedDevice, setSelectedDevice] = useState<string>('DEV-PUMP-204');
  const [simulationRunning, setSimulationRunning] = useState<boolean>(false);
  const [lastSimResult, setLastSimResult] = useState<MachineSignalAnalysisResult | null>(null);
  const [clinicianName, setClinicianName] = useState<string>('Dr. Lead Biomedical Engineer');

  const loadSignalData = async () => {
    try {
      const [colData, liveData, polData, lockData, metricData, histData] = await Promise.all([
        apiService.getCollectors(),
        apiService.getLiveSignals(),
        apiService.getDefensePolicy(),
        apiService.getClinicalInterlocks(),
        apiService.getCybersecurityMetrics(),
        apiService.getSignalHistory({ limit: 25 }),
      ]);

      setCollectors(colData);
      setLiveSignals(liveData);
      setDefensePolicy(polData);
      setInterlocks(lockData);
      setMetrics(metricData);
      setHistory(histData);
    } catch (e) {
      console.error('Error loading machine signals data', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSignalData();
    const interval = setInterval(loadSignalData, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleModeChange = async (newMode: CyberDefenseMode) => {
    const updated = { ...defensePolicy, mode: newMode };
    setDefensePolicy(updated);
    try {
      await apiService.updateDefensePolicy(updated);
      loadSignalData();
    } catch (e) {
      console.error('Failed to update defense policy', e);
    }
  };

  const handleToggleCollector = async (collectorId: string) => {
    try {
      await apiService.toggleCollector(collectorId);
      loadSignalData();
    } catch (e) {
      console.error('Failed to toggle collector', e);
    }
  };

  const handleSimulateAttack = async () => {
    setSimulationRunning(true);
    try {
      const res = await apiService.simulateMachineAttack(selectedScenario, selectedDevice);
      setLastSimResult(res);
      await loadSignalData();
    } catch (e) {
      console.error('Simulation error', e);
    } finally {
      setSimulationRunning(false);
    }
  };

  const handleResetInterlock = async (deviceId: string) => {
    try {
      await apiService.resetClinicalInterlock(deviceId, clinicianName);
      await loadSignalData();
    } catch (e) {
      console.error('Reset interlock error', e);
    }
  };

  // Connected medical machines directory
  const machineList = [
    {
      id: 'DEV-PUMP-204',
      name: 'Alaris Infusion Pump #4',
      category: 'Infusion Pump',
      location: 'Pediatrics - Room 104',
      protocol: 'MQTT Telemetry',
      sampleRate: '2.5 Hz',
      normalPayloadKey: 'flow_rate_ml_h',
      normalUnit: 'mL/h',
      metricLabel: 'Infusion Rate',
      safeRange: '0.1 – 200.0 mL/h',
    },
    {
      id: 'DEV-VENT-301',
      name: 'Puritan Bennett Ventilator',
      category: 'Smart Ventilator',
      location: 'ICU Wing A - Room 102',
      protocol: 'Modbus/TCP',
      sampleRate: '5.0 Hz',
      normalPayloadKey: 'peak_inspiratory_pressure_cmH2O',
      normalUnit: 'cmH2O',
      metricLabel: 'Peak Airway Pressure',
      safeRange: '10.0 – 35.0 cmH2O',
    },
    {
      id: 'DEV-ICU-101',
      name: 'ICU Telemetry Station A',
      category: 'ICU Telemetry Station',
      location: 'ICU Wing B - Room 301',
      protocol: 'TCP / Direct Vitals',
      sampleRate: '10.0 Hz',
      normalPayloadKey: 'heart_rate_bpm',
      normalUnit: 'BPM',
      metricLabel: 'Patient Heart Rate',
      safeRange: '50 – 140 BPM',
    },
    {
      id: 'DEV-RAD-405',
      name: 'Siemens DICOM Radiology',
      category: 'DICOM Workstation',
      location: 'Radiology Imaging Bay 2',
      protocol: 'DICOM C-STORE',
      sampleRate: '1.0 Hz',
      normalPayloadKey: 'entropy',
      normalUnit: '/ 8.0',
      metricLabel: 'Payload Shannon Entropy',
      safeRange: '2.0 – 5.5 / 8.0',
    },
    {
      id: 'DEV-SYRINGE-12',
      name: 'Baxter Smart Syringe Driver',
      category: 'Smart Syringe',
      location: 'Oncology Ward - Room 208',
      protocol: 'MQTT / Direct Microflow',
      sampleRate: '2.0 Hz',
      normalPayloadKey: 'flow_rate_ml_h',
      normalUnit: 'mL/h',
      metricLabel: 'Microflow Rate',
      safeRange: '0.1 – 15.0 mL/h',
    }
  ];

  return (
    <div className="space-y-6 pb-12 animate-in fade-in duration-300">
      {/* 1. Header & Defense Mode Control Cockpit */}
      <div className="rounded-2xl border bg-card/75 backdrop-blur-md p-6 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-1.5">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 rounded-xl bg-medical-teal/15 text-medical-teal border border-medical-teal/30">
                <Activity className="h-6 w-6 animate-pulse" />
              </div>
              <div>
                <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
                  Direct Machine Signals & Cyber Defense
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-500 border border-emerald-500/30">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-ping mr-1.5" />
                    LIVE CPS ENGINE
                  </span>
                </h1>
                <p className="text-xs md:text-sm text-muted-foreground">
                  Ingesting direct physiological waveforms, operational telemetry, and physical invariant boundaries from smart medical machines.
                </p>
              </div>
            </div>
          </div>

          {/* Cyber Defense Mode Selector */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 bg-secondary/60 p-2 rounded-xl border border-border/70">
            <span className="text-xs font-semibold text-muted-foreground px-2 flex items-center gap-1.5">
              <Shield className="h-3.5 w-3.5 text-medical-teal" />
              Cyber Defense Mode:
            </span>
            <div className="flex items-center space-x-1">
              <button
                onClick={() => handleModeChange('PASSIVE_MONITOR')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  defensePolicy.mode === 'PASSIVE_MONITOR'
                    ? 'bg-amber-500 text-white shadow-sm'
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                }`}
              >
                Passive Monitor
              </button>
              <button
                onClick={() => handleModeChange('ASSISTED_DEFENSE')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  defensePolicy.mode === 'ASSISTED_DEFENSE'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                }`}
              >
                Assisted Defense
              </button>
              <button
                onClick={() => handleModeChange('ACTIVE_PREVENTION')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                  defensePolicy.mode === 'ACTIVE_PREVENTION'
                    ? 'bg-emerald-600 text-white shadow-sm ring-2 ring-emerald-500/30'
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                }`}
              >
                <Zap className="h-3 w-3" />
                Active Zero-Trust Prevention
              </button>
            </div>
          </div>
        </div>

        {/* Defense Policy Details Ribbon */}
        <div className="mt-4 pt-4 border-t border-border/50 flex flex-wrap items-center justify-between gap-4 text-xs text-muted-foreground">
          <div className="flex flex-wrap items-center gap-4">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
              Anti-Replay Nonce Verification: <strong className="text-foreground">Active</strong>
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
              Physical Invariant Checking (IEC 60601-1-8): <strong className="text-foreground">Enforced</strong>
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
              Autonomous Host Firewall Quarantine: <strong className={defensePolicy.mode === 'ACTIVE_PREVENTION' ? 'text-emerald-500' : 'text-amber-500'}>
                {defensePolicy.mode === 'ACTIVE_PREVENTION' ? 'Enabled (<1.2ms)' : 'Manual Operator Approval Required'}
              </strong>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-[11px] font-mono text-muted-foreground">Status:</span>
            <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-medical-teal/15 text-medical-teal border border-medical-teal/30">
              {defensePolicy.mode === 'ACTIVE_PREVENTION' ? 'Autonomous Containment Armed' : 'Auditing Mode'}
            </span>
          </div>
        </div>
      </div>

      {/* 2. Active Clinical Safety Interlocks Banner (if engaged) */}
      {interlocks.length > 0 && (
        <div className="rounded-2xl border-2 border-rose-500/60 bg-rose-500/10 p-5 backdrop-blur-md shadow-lg animate-in slide-in-from-top-2">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-start space-x-3">
              <div className="p-2 rounded-xl bg-rose-500 text-white shrink-0">
                <AlertTriangle className="h-6 w-6 animate-bounce" />
              </div>
              <div>
                <h3 className="text-base font-bold text-rose-500 flex items-center gap-2">
                  Clinical Safety Interlock Engaged ({interlocks.length} Machine{interlocks.length > 1 ? 's' : ''})
                </h3>
                <p className="text-xs text-foreground/80 mt-0.5">
                  Anomalous machine signals triggered automated patient fail-safe protections. Network traffic is isolated while life-support parameters are locked in local bedside manual override.
                </p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {interlocks.map((item) => (
                    <span
                      key={item.id}
                      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-mono font-bold bg-card border border-rose-500/40 text-foreground"
                    >
                      <Lock className="h-3 w-3 text-rose-500" />
                      {item.device_id}: {item.reason}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3 shrink-0">
              {interlocks.map((item) => (
                <button
                  key={item.id}
                  onClick={() => handleResetInterlock(item.device_id)}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-rose-500 hover:bg-rose-600 text-white shadow-md hover:shadow-glow-rose transition-all flex items-center gap-2"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  Clear & Reconnect {item.device_id}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 3. Cyber Defense Metrics Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-2xl border bg-card/60 backdrop-blur-md space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
            <Radio className="h-3.5 w-3.5 text-medical-teal" />
            Signals Ingested
          </span>
          <div className="text-2xl font-bold font-mono text-foreground">
            {metrics.total_signals_processed.toLocaleString()}
          </div>
          <p className="text-[10px] text-muted-foreground">Direct machine frames processed</p>
        </div>

        <div className="p-4 rounded-2xl border bg-card/60 backdrop-blur-md space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
            <Flame className="h-3.5 w-3.5 text-rose-500" />
            Physical Breaches Blocked
          </span>
          <div className="text-2xl font-bold font-mono text-rose-500">
            {metrics.total_breaches_detected}
          </div>
          <p className="text-[10px] text-muted-foreground">Overdose, barotrauma & paradoxes</p>
        </div>

        <div className="p-4 rounded-2xl border bg-card/60 backdrop-blur-md space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
            <Lock className="h-3.5 w-3.5 text-indigo-500" />
            Anti-Replay Blocks
          </span>
          <div className="text-2xl font-bold font-mono text-indigo-500">
            {metrics.total_replay_attacks_blocked}
          </div>
          <p className="text-[10px] text-muted-foreground">Stale & out-of-order frames</p>
        </div>

        <div className="p-4 rounded-2xl border bg-card/60 backdrop-blur-md space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
            <ShieldCheck className="h-3.5 w-3.5 text-emerald-500" />
            Quarantines Enforced
          </span>
          <div className="text-2xl font-bold font-mono text-emerald-500">
            {metrics.total_quarantines_enforced}
          </div>
          <p className="text-[10px] text-muted-foreground">Autonomous edge firewall cuts</p>
        </div>
      </div>

      {/* 4. Connected Medical Machines: Live Waveforms & Signals Matrix */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Cpu className="h-4 w-4 text-medical-teal" />
            Connected Clinical Equipment Telemetry Matrix
          </h2>
          <span className="text-xs text-muted-foreground font-mono">
            {machineList.length} Connected Direct Feeds
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {machineList.map((m) => {
            const live = liveSignals[m.id];
            const isInterlocked = interlocks.some(i => i.device_id === m.id);
            const val = live?.payload?.[m.normalPayloadKey];
            const displayVal = val !== undefined ? val : '—';
            const isAnomalous = live?.is_threat || isInterlocked;

            return (
              <div
                key={m.id}
                className={`p-5 rounded-2xl border transition-all relative overflow-hidden backdrop-blur-md ${
                  isInterlocked
                    ? 'border-rose-500/70 bg-rose-500/5 shadow-md'
                    : isAnomalous
                    ? 'border-amber-500/50 bg-amber-500/5'
                    : 'border-border/80 bg-card/75 hover:border-medical-teal/50'
                }`}
              >
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded-md bg-secondary text-muted-foreground border">
                      {m.id}
                    </span>
                    <h3 className="font-bold text-sm text-foreground mt-1.5">{m.name}</h3>
                    <p className="text-[11px] text-muted-foreground">{m.location}</p>
                  </div>

                  <span
                    className={`px-2.5 py-1 rounded-full text-[10px] font-bold flex items-center gap-1 ${
                      isInterlocked
                        ? 'bg-rose-500 text-white shadow-sm'
                        : isAnomalous
                        ? 'bg-amber-500 text-white'
                        : 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/30'
                    }`}
                  >
                    {isInterlocked ? (
                      <>
                        <Lock className="h-2.5 w-2.5" />
                        INTERLOCKED
                      </>
                    ) : isAnomalous ? (
                      <>
                        <AlertTriangle className="h-2.5 w-2.5" />
                        THREAT FLAGGED
                      </>
                    ) : (
                      <>
                        <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
                        SECURE
                      </>
                    )}
                  </span>
                </div>

                {/* Real-time Physical Signal Value */}
                <div className="mt-4 p-3 rounded-xl bg-secondary/50 border border-border/50 flex items-center justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-semibold text-muted-foreground">
                      {m.metricLabel}
                    </span>
                    <div className="text-xl font-mono font-bold text-foreground flex items-baseline gap-1 mt-0.5">
                      <span>{displayVal}</span>
                      <span className="text-xs font-normal text-muted-foreground">{m.normalUnit}</span>
                    </div>
                  </div>

                  <div className="text-right">
                    <span className="text-[10px] uppercase font-semibold text-muted-foreground">
                      Safe Baseline
                    </span>
                    <p className="text-xs font-mono text-muted-foreground mt-0.5">{m.safeRange}</p>
                  </div>
                </div>

                {/* Oscilloscope / Signal Waveform Graphic Animation */}
                <div className="mt-3 h-10 w-full rounded-lg bg-background/50 border border-border/40 p-1 flex items-center justify-between overflow-hidden relative">
                  <div className="absolute inset-0 flex items-center justify-around opacity-30">
                    <div className="h-full w-[1px] bg-border" />
                    <div className="h-full w-[1px] bg-border" />
                    <div className="h-full w-[1px] bg-border" />
                    <div className="h-full w-[1px] bg-border" />
                  </div>
                  {/* Waveform Bars */}
                  <div className="flex items-center gap-1 w-full justify-between z-10 px-2">
                    {[40, 65, 30, 85, 45, 95, 20, 70, 50, 90, 35, 60, 80, 45, 100].map((h, i) => (
                      <div
                        key={i}
                        className={`w-1 rounded-full transition-all duration-300 ${
                          isInterlocked
                            ? 'bg-rose-500'
                            : isAnomalous
                            ? 'bg-amber-500'
                            : 'bg-medical-teal'
                        }`}
                        style={{
                          height: `${Math.max(15, (h * (isAnomalous ? 1.2 : 0.8)) % 32)}px`,
                          animation: `pulse ${1 + (i % 3) * 0.4}s infinite ease-in-out`
                        }}
                      />
                    ))}
                  </div>
                </div>

                {/* Metadata Footer */}
                <div className="mt-3 pt-3 border-t border-border/40 flex items-center justify-between text-[11px] text-muted-foreground">
                  <span className="font-mono">{m.protocol}</span>
                  <span className="font-mono text-foreground font-semibold">Rate: {m.sampleRate}</span>
                  <span className="text-emerald-500 font-mono font-bold">&lt; 1.2ms</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 5. Direct Signal Exploit Simulator & Testing Lab */}
      <div className="rounded-2xl border bg-card/75 backdrop-blur-md p-6 shadow-sm space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-foreground flex items-center gap-2">
              <Zap className="h-4 w-4 text-rose-500" />
              Machine Exploit Injection & Direct Signal Testing Lab
            </h2>
            <p className="text-xs text-muted-foreground">
              Inject authentic physical invariant breaches and protocol attacks directly into medical machines to evaluate real-time cybersecurity response.
            </p>
          </div>

          <span className="text-xs font-mono px-3 py-1 rounded-lg bg-secondary text-muted-foreground border">
            Mode: <strong className="text-foreground">{defensePolicy.mode}</strong>
          </span>
        </div>

        {/* Controls Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1.5">
              Target Medical Machine
            </label>
            <select
              value={selectedDevice}
              onChange={(e) => setSelectedDevice(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-secondary border border-border text-foreground text-xs font-medium focus:ring-2 focus:ring-medical-teal"
            >
              <option value="DEV-PUMP-204">DEV-PUMP-204 (Alaris Infusion Pump #4)</option>
              <option value="DEV-VENT-301">DEV-VENT-301 (Puritan Bennett Ventilator)</option>
              <option value="DEV-ICU-101">DEV-ICU-101 (ICU Telemetry Station A)</option>
              <option value="DEV-RAD-405">DEV-RAD-405 (Siemens DICOM Workstation)</option>
              <option value="DEV-SYRINGE-12">DEV-SYRINGE-12 (Baxter Syringe Driver)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1.5">
              Attack Scenario / Invariant Breach
            </label>
            <select
              value={selectedScenario}
              onChange={(e) => setSelectedScenario(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-secondary border border-border text-foreground text-xs font-medium focus:ring-2 focus:ring-medical-teal"
            >
              <option value="infusion_overdose">Lethal Bolus Overdose (650 mL/h &gt; Max 200 mL/h)</option>
              <option value="ventilator_barotrauma">Ventilator Barotrauma Hijack (48 cmH2O &gt; Safe 35)</option>
              <option value="sensor_spoofing">Sensor Deception Paradox (HR=0 with 99% SpO2)</option>
              <option value="replay_attack">Signal Replay Attack (Stale Sequence Nonce)</option>
              <option value="dicom_ransomware">PACS DICOM Ransomware In-Flight (Entropy 7.92)</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={handleSimulateAttack}
              disabled={simulationRunning}
              className="w-full px-4 py-2.5 rounded-xl text-xs font-bold bg-rose-500 hover:bg-rose-600 disabled:opacity-50 text-white shadow-md hover:shadow-glow-rose transition-all flex items-center justify-center gap-2"
            >
              {simulationRunning ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  Transmitting Direct Signal...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4 fill-current" />
                  Transmit Exploit Signal Directly
                </>
              )}
            </button>
          </div>
        </div>

        {/* Real-time Analysis Result Card */}
        {lastSimResult && (
          <div className="p-4 rounded-xl border border-rose-500/40 bg-rose-500/5 space-y-3 animate-in fade-in">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-rose-500/20 pb-3">
              <div className="flex items-center space-x-2">
                <ShieldAlert className="h-5 w-5 text-rose-500" />
                <span className="font-bold text-sm text-foreground">
                  CPS Defense Response: <span className="text-rose-500 font-mono">{lastSimResult.threat_type}</span>
                </span>
              </div>
              <div className="flex items-center gap-2 text-xs font-mono">
                <span className="px-2 py-0.5 rounded bg-rose-500 text-white font-bold text-[10px]">
                  {lastSimResult.severity}
                </span>
                <span className="text-muted-foreground">Latency: <strong className="text-emerald-500">{lastSimResult.latency_ms}ms</strong></span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div className="space-y-1">
                <span className="text-muted-foreground font-semibold">Physical Invariant Verdict:</span>
                <p className="text-foreground bg-background/60 p-2.5 rounded-lg border border-border/50">
                  {lastSimResult.breach_details || 'Violation flagged by real-time safety boundary checks.'}
                </p>
              </div>

              <div className="space-y-1">
                <span className="text-muted-foreground font-semibold">Cyber Defense Countermeasure Taken:</span>
                <div className="bg-background/60 p-2.5 rounded-lg border border-border/50 space-y-1">
                  <div className="flex items-center justify-between">
                    <span>Action:</span>
                    <span className="font-mono font-bold text-rose-500">{lastSimResult.defense_action_taken}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Clinical Safety Interlock:</span>
                    <span className={lastSimResult.clinical_safety_interlock ? 'text-rose-500 font-bold' : 'text-muted-foreground'}>
                      {lastSimResult.clinical_safety_interlock ? 'ENGAGED (Fail-Safe Override)' : 'Not Required'}
                    </span>
                  </div>
                  {lastSimResult.alert_id && (
                    <div className="flex items-center justify-between">
                      <span>Correlated Incident Alert:</span>
                      <span className="font-mono text-medical-teal font-bold">{lastSimResult.alert_id}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 6. Direct Signal Collectors & Listeners Status Panel */}
      <div className="space-y-3">
        <h2 className="text-sm font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
          <Server className="h-4 w-4 text-medical-teal" />
          Active Direct Signal Ingestion Collectors
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {collectors.map((c) => {
            const isRunning = c.status === 'RUNNING';
            return (
              <div
                key={c.collector_id}
                className="p-4 rounded-2xl border bg-card/60 backdrop-blur-md flex flex-col justify-between space-y-3"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-secondary text-muted-foreground uppercase border">
                      {c.collector_type}
                    </span>
                    <button
                      onClick={() => handleToggleCollector(c.collector_id)}
                      className={`px-2 py-0.5 rounded-full text-[10px] font-bold flex items-center gap-1 transition-all ${
                        isRunning
                          ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/30 hover:bg-rose-500/10 hover:text-rose-500'
                          : 'bg-muted text-muted-foreground hover:bg-emerald-500/10 hover:text-emerald-500'
                      }`}
                    >
                      <Power className="h-2.5 w-2.5" />
                      {isRunning ? 'RUNNING' : 'STOPPED'}
                    </button>
                  </div>

                  <h3 className="font-bold text-xs text-foreground mt-2">{c.name}</h3>
                  <p className="text-[11px] text-muted-foreground mt-1 line-clamp-2">{c.description}</p>
                </div>

                <div className="pt-2 border-t border-border/50 text-[11px] space-y-1">
                  <div className="flex justify-between text-muted-foreground">
                    <span>Endpoint:</span>
                    <span className="font-mono text-foreground font-semibold">{c.endpoint}</span>
                  </div>
                  <div className="flex justify-between text-muted-foreground">
                    <span>Frames Received:</span>
                    <span className="font-mono text-medical-teal font-bold">{c.signals_received}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 7. Live Machine Signal Stream Audit Feed */}
      <div className="rounded-2xl border bg-card/75 backdrop-blur-md p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Clock className="h-4 w-4 text-medical-teal" />
            <h3 className="font-bold text-sm text-foreground">Real-Time Machine Signal Audit Stream</h3>
          </div>
          <button
            onClick={loadSignalData}
            className="text-xs text-muted-foreground hover:text-foreground flex items-center gap-1.5 transition-colors"
          >
            <RefreshCw className="h-3 w-3" />
            Refresh
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-border/60 text-muted-foreground">
                <th className="pb-2.5 font-semibold">Signal ID</th>
                <th className="pb-2.5 font-semibold">Device</th>
                <th className="pb-2.5 font-semibold">Signal Type</th>
                <th className="pb-2.5 font-semibold">Seq #</th>
                <th className="pb-2.5 font-semibold">Integrity Status</th>
                <th className="pb-2.5 font-semibold">Defense Action</th>
                <th className="pb-2.5 font-semibold">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/40 font-mono">
              {history.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-6 text-center text-muted-foreground">
                    No machine signals recorded yet. Direct signal background collector running.
                  </td>
                </tr>
              ) : (
                history.map((row) => (
                  <tr key={row.id} className="hover:bg-secondary/40 transition-colors">
                    <td className="py-2.5 font-bold text-foreground">{row.signal_id}</td>
                    <td className="py-2.5 text-foreground">{row.device_id}</td>
                    <td className="py-2.5 text-muted-foreground">{row.signal_type}</td>
                    <td className="py-2.5 text-muted-foreground">#{row.seq_num}</td>
                    <td className="py-2.5">
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold ${
                          row.integrity_status === 'VERIFIED'
                            ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/30'
                            : 'bg-rose-500/10 text-rose-500 border border-rose-500/30'
                        }`}
                      >
                        {row.integrity_status === 'VERIFIED' ? (
                          <CheckCircle2 className="h-3 w-3" />
                        ) : (
                          <XCircle className="h-3 w-3" />
                        )}
                        {row.integrity_status}
                      </span>
                    </td>
                    <td className="py-2.5">
                      <span
                        className={`font-semibold text-[11px] ${
                          row.defense_action === 'FIREWALL_ISOLATE'
                            ? 'text-rose-500 font-bold'
                            : row.defense_action === 'SAFETY_INTERLOCK_ENGAGED'
                            ? 'text-amber-500 font-bold'
                            : 'text-muted-foreground'
                        }`}
                      >
                        {row.defense_action}
                      </span>
                    </td>
                    <td className="py-2.5 text-muted-foreground text-[11px]">
                      {row.timestamp ? new Date(row.timestamp).toLocaleTimeString() : '—'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
