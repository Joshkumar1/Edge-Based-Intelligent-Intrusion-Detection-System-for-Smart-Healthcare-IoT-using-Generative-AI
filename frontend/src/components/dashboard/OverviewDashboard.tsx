import React, { useState, useEffect } from 'react';
import { ShieldCheck, AlertTriangle, Monitor, Cpu, Activity, ArrowUpRight, Zap, Sparkles } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';
import { DashboardStats, Alert, TelemetryStreamEvent } from '../../types';

interface OverviewDashboardProps {
  stats: DashboardStats;
  alerts: Alert[];
  lastTelemetryEvent: TelemetryStreamEvent | null;
  onSelectAlert: (alert: Alert) => void;
  onSimulateAttack: () => void;
}

export const OverviewDashboard: React.FC<OverviewDashboardProps> = ({
  stats,
  alerts,
  lastTelemetryEvent,
  onSelectAlert,
  onSimulateAttack,
}) => {
  const [telemetryHistory, setTelemetryHistory] = useState<any[]>([]);

  // Update telemetry graph data as live packets arrive
  useEffect(() => {
    if (lastTelemetryEvent) {
      const { packet, detection } = lastTelemetryEvent;
      const timeStr = new Date().toLocaleTimeString([], { hour12: false, minute: '2-digit', second: '2-digit' });
      setTelemetryHistory((prev) => {
        const updated = [
          ...prev,
          {
            time: timeStr,
            packetRate: packet.packet_rate,
            byteRate: Math.round(packet.byte_rate / 10),
            entropy: packet.entropy * 10,
            isAnomaly: detection.is_anomaly ? 100 : 0,
          },
        ];
        return updated.slice(-20); // Keep last 20 data points
      });
    }
  }, [lastTelemetryEvent]);

  const threatChartData = Object.entries(stats.threat_distribution || {}).map(([name, count]) => ({
    name,
    count,
  }));

  const COLORS = ['#E11D48', '#F59E0B', '#0D9488', '#2563EB', '#8B5CF6'];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Hospital Security Cockpit</h2>
          <p className="text-sm text-muted-foreground">
            Real-time medical IoT telemetry, edge anomaly scores, and explainable AI insights.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={onSimulateAttack}
            className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-rose-500 to-amber-500 text-white font-semibold text-xs shadow-glow-red hover:opacity-95 transition-all"
          >
            <Zap className="h-4 w-4" />
            <span>Simulate IoT Attack Burst</span>
          </button>
        </div>
      </div>

      {/* Top Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Monitored Devices */}
        <div className="p-5 rounded-2xl bg-card border shadow-subtle flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Monitored IoT Devices
            </span>
            <div className="p-2 rounded-xl bg-medical-teal/10 text-medical-teal">
              <Monitor className="h-5 w-5" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-extrabold">{stats.total_devices}</div>
            <div className="text-xs text-emerald-500 font-medium flex items-center mt-1">
              <span>100% Edge Gateways Connected</span>
            </div>
          </div>
        </div>

        {/* Active Incidents */}
        <div className="p-5 rounded-2xl bg-card border shadow-subtle flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Active Intrusion Incidents
            </span>
            <div className="p-2 rounded-xl bg-rose-500/10 text-rose-500">
              <AlertTriangle className="h-5 w-5" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-rose-500">{stats.active_alerts}</div>
            <div className="text-xs text-rose-400 font-medium flex items-center mt-1">
              <span>{stats.critical_alerts} Critical Ransomware / DoS</span>
            </div>
          </div>
        </div>

        {/* High Risk Devices */}
        <div className="p-5 rounded-2xl bg-card border shadow-subtle flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              High Risk Devices
            </span>
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-500">
              <Activity className="h-5 w-5" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-amber-500">{stats.devices_at_risk}</div>
            <div className="text-xs text-amber-500 font-medium flex items-center mt-1">
              <span>Radiology & Infusion Subnets</span>
            </div>
          </div>
        </div>

        {/* Inference Latency */}
        <div className="p-5 rounded-2xl bg-card border shadow-subtle flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Inference Speed
            </span>
            <div className="p-2 rounded-xl bg-medical-teal/10 text-medical-teal">
              <Cpu className="h-5 w-5" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-emerald-500">0.84 ms</div>
            <div className="text-xs text-muted-foreground font-medium flex items-center mt-1">
              <span>Zero-Cloud Dependency</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid: Telemetry Graph & Threat Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Real-time Telemetry Graph */}
        <div className="lg:col-span-2 p-5 rounded-2xl bg-card border shadow-subtle space-y-4">
          <div className="flex items-center justify-between border-b pb-3">
            <div>
              <h3 className="font-bold text-base">Real-time Edge Traffic & Anomaly Telemetry</h3>
              <p className="text-xs text-muted-foreground">Streaming packet rates, payload entropy, and ML anomaly flags.</p>
            </div>
            <span className="flex items-center space-x-1 text-xs font-semibold text-emerald-500 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-ping"></span>
              <span>WebSocket Stream</span>
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={telemetryHistory.length > 0 ? telemetryHistory : [
                { time: '11:00', packetRate: 12, byteRate: 40, entropy: 38 },
                { time: '11:01', packetRate: 15, byteRate: 45, entropy: 40 },
                { time: '11:02', packetRate: 380, byteRate: 280, entropy: 78 },
                { time: '11:03', packetRate: 20, byteRate: 50, entropy: 42 },
              ]}>
                <defs>
                  <linearGradient id="colorPacket" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0D9488" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#0D9488" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorEntropy" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#E11D48" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#E11D48" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                <XAxis dataKey="time" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#1E293B', borderRadius: '12px', color: '#FFF' }} />
                <Area type="monotone" dataKey="packetRate" name="Packet Rate (pkts/s)" stroke="#0D9488" fillOpacity={1} fill="url(#colorPacket)" />
                <Area type="monotone" dataKey="entropy" name="Payload Entropy (x10)" stroke="#E11D48" fillOpacity={1} fill="url(#colorEntropy)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Threat Distribution Chart */}
        <div className="p-5 rounded-2xl bg-card border shadow-subtle space-y-4 flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-base border-b pb-3">Threat Vector Breakdown</h3>
            <p className="text-xs text-muted-foreground mt-1">Classified intrusion types across hospital subnets.</p>
          </div>

          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={threatChartData.length > 0 ? threatChartData : [
                { name: 'Ransomware', count: 1 },
                { name: 'MQTT DoS', count: 2 },
                { name: 'Modbus Inj.', count: 1 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#1E293B', borderRadius: '12px', color: '#FFF' }} />
                <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                  {threatChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="text-xs text-center text-muted-foreground font-medium pt-2 border-t">
            Isolation Forest + XGBoost Multi-Class Model
          </div>
        </div>
      </div>

      {/* Active High-Priority Incidents */}
      <div className="p-5 rounded-2xl bg-card border shadow-subtle space-y-4">
        <div className="flex items-center justify-between border-b pb-3">
          <div>
            <h3 className="font-bold text-base">Active Intrusion Incidents</h3>
            <p className="text-xs text-muted-foreground">Select any incident to open the Local Generative AI Clinical Explainer.</p>
          </div>
          <span className="text-xs font-semibold text-rose-500 bg-rose-500/10 px-3 py-1 rounded-full">
            {alerts.length} Total Alerts
          </span>
        </div>

        <div className="space-y-3">
          {alerts.map((alert) => (
            <div
              key={alert.alert_id}
              onClick={() => onSelectAlert(alert)}
              className="p-4 rounded-xl border bg-secondary/40 hover:bg-secondary transition-all cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-medical-teal/50"
            >
              <div className="flex items-start space-x-3">
                <div
                  className={`p-2.5 rounded-xl text-white font-bold mt-1 ${
                    alert.severity === 'CRITICAL' ? 'bg-rose-500 shadow-glow-red' : 'bg-amber-500'
                  }`}
                >
                  <AlertTriangle className="h-5 w-5" />
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-sm text-foreground">{alert.threat_type}</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      alert.severity === 'CRITICAL' ? 'bg-rose-500/10 text-rose-500 border border-rose-500/20' : 'bg-amber-500/10 text-amber-500 border border-amber-500/20'
                    }`}>
                      {alert.severity}
                    </span>
                    <span className="text-xs text-muted-foreground font-mono">
                      Target: {alert.target_device_id || 'Unknown Device'} ({alert.protocol})
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1 line-clamp-1">
                    {alert.clinical_explanation || 'Click to view local AI explanation.'}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-3 self-end md:self-center">
                <div className="text-right text-xs">
                  <div className="font-mono text-muted-foreground">{alert.source_ip} &rarr; {alert.destination_ip}</div>
                  <div className="text-[10px] text-muted-foreground">{new Date(alert.timestamp).toLocaleTimeString()}</div>
                </div>
                <button className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-medical-teal text-white font-semibold text-xs shadow-glow-teal hover:opacity-90 transition-all">
                  <Sparkles className="h-3.5 w-3.5" />
                  <span>Explain AI</span>
                  <ArrowUpRight className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
