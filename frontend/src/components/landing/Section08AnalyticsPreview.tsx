import React from 'react';
import { BarChart3, Activity, PieChart, ShieldAlert } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';

export const Section08AnalyticsPreview: React.FC = () => {
  const activityData = [
    { time: '08:00', normal: 420, attack: 0 },
    { time: '09:00', normal: 480, attack: 0 },
    { time: '10:00', normal: 510, attack: 12 },
    { time: '11:00', normal: 490, attack: 380 },
    { time: '12:00', normal: 460, attack: 5 },
    { time: '13:00', normal: 500, attack: 0 },
  ];

  const threatDistribution = [
    { name: 'DICOM Ransomware', count: 12, color: '#E11D48' },
    { name: 'MQTT Flood DoS', count: 28, color: '#F59E0B' },
    { name: 'Modbus Injection', count: 8, color: '#0D9488' },
    { name: 'ARP Spoofing MITM', count: 15, color: '#2563EB' },
    { name: 'Port Scanning', count: 22, color: '#8B5CF6' },
  ];

  return (
    <section className="py-24 border-b relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-medical-teal/10 border border-medical-teal/20 text-medical-teal text-xs font-semibold">
            <BarChart3 className="h-4 w-4" />
            <span>Real-Time Security Analytics</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            Complete Telemetry & Risk Score Visibility
          </h2>
          <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
            Monitor real-time network throughput, anomaly spikes, and risk distribution across all medical device subnets.
          </p>
        </div>

        {/* Analytics Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Traffic Activity Graph */}
          <div className="lg:col-span-7 p-6 rounded-3xl bg-card border shadow-subtle space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <div className="flex items-center space-x-2 font-bold text-sm">
                <Activity className="h-4 w-4 text-medical-teal" />
                <span>Live Network Telemetry & Anomaly Spikes</span>
              </div>
              <span className="text-xs font-mono text-emerald-500 font-bold bg-emerald-500/10 px-2.5 py-0.5 rounded-full">
                WebSocket Live
              </span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={activityData}>
                  <defs>
                    <linearGradient id="colorNormal" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0D9488" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#0D9488" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorAttack" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#E11D48" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#E11D48" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                  <XAxis dataKey="time" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#1E293B', borderRadius: '12px', color: '#FFF' }} />
                  <Area type="monotone" dataKey="normal" name="Normal IoT Traffic" stroke="#0D9488" fillOpacity={1} fill="url(#colorNormal)" />
                  <Area type="monotone" dataKey="attack" name="Intrusion Packet Burst" stroke="#E11D48" fillOpacity={1} fill="url(#colorAttack)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Threat Distribution Chart */}
          <div className="lg:col-span-5 p-6 rounded-3xl bg-card border shadow-subtle space-y-4 flex flex-col justify-between">
            <div className="flex items-center justify-between border-b pb-3">
              <div className="flex items-center space-x-2 font-bold text-sm">
                <PieChart className="h-4 w-4 text-medical-teal" />
                <span>Threat Vector Classification</span>
              </div>
              <span className="text-xs font-mono text-muted-foreground">XGBoost Model</span>
            </div>

            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={threatDistribution}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                  <XAxis dataKey="name" tick={{ fontSize: 9 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#1E293B', borderRadius: '12px', color: '#FFF' }} />
                  <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                    {threatDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="text-xs text-muted-foreground text-center font-mono border-t pt-2">
              Tested on 6,000+ benchmark medical IoT vectors
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};
