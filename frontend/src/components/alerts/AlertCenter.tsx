import React, { useState } from 'react';
import { AlertTriangle, Filter, Search, Sparkles, CheckCircle2, ShieldAlert } from 'lucide-react';
import { Alert } from '../../types';

interface AlertCenterProps {
  alerts: Alert[];
  onSelectAlert: (alert: Alert) => void;
  onUpdateStatus: (alertId: string, status: string) => void;
}

export const AlertCenter: React.FC<AlertCenterProps> = ({ alerts, onSelectAlert, onUpdateStatus }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [severityFilter, setSeverityFilter] = useState<string>('ALL');
  const [statusFilter, setStatusFilter] = useState<string>('ALL');

  const filteredAlerts = alerts.filter((alert) => {
    const matchesSearch =
      alert.threat_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      alert.source_ip.includes(searchTerm) ||
      (alert.target_device_id && alert.target_device_id.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesSeverity = severityFilter === 'ALL' || alert.severity === severityFilter;
    const matchesStatus = statusFilter === 'ALL' || alert.status === statusFilter;

    return matchesSearch && matchesSeverity && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Intrusion Incident Center</h2>
          <p className="text-sm text-muted-foreground">
            Manage, triage, and execute local AI-guided mitigations for hospital cyber alerts.
          </p>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="p-4 rounded-2xl bg-card border shadow-subtle flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Search */}
        <div className="relative w-full md:w-80">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search by threat, IP, or Device ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 rounded-xl bg-secondary/80 border text-xs focus:outline-none focus:ring-2 focus:ring-medical-teal"
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          <div className="flex items-center space-x-2 text-xs">
            <Filter className="h-4 w-4 text-muted-foreground" />
            <span className="text-muted-foreground font-medium">Severity:</span>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-secondary border text-xs font-semibold focus:outline-none"
            >
              <option value="ALL">All Severities</option>
              <option value="CRITICAL">Critical</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
            </select>
          </div>

          <div className="flex items-center space-x-2 text-xs">
            <span className="text-muted-foreground font-medium">Status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-secondary border text-xs font-semibold focus:outline-none"
            >
              <option value="ALL">All Statuses</option>
              <option value="NEW">New</option>
              <option value="INVESTIGATING">Investigating</option>
              <option value="MITIGATED">Mitigated</option>
            </select>
          </div>
        </div>
      </div>

      {/* Alert Feed List */}
      <div className="space-y-3">
        {filteredAlerts.length === 0 ? (
          <div className="p-12 rounded-2xl bg-card border text-center space-y-3">
            <ShieldAlert className="h-10 w-10 text-muted-foreground mx-auto" />
            <div className="font-bold text-base">No Matching Intrusion Incidents</div>
            <p className="text-xs text-muted-foreground">Adjust filters or search parameters.</p>
          </div>
        ) : (
          filteredAlerts.map((alert) => (
            <div
              key={alert.alert_id}
              className="p-5 rounded-2xl bg-card border shadow-subtle flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-medical-teal/40 transition-all"
            >
              <div className="flex items-start space-x-4">
                <div
                  className={`p-3 rounded-2xl text-white font-bold mt-1 ${
                    alert.severity === 'CRITICAL' ? 'bg-rose-500 shadow-glow-red' : 'bg-amber-500'
                  }`}
                >
                  <AlertTriangle className="h-6 w-6" />
                </div>
                <div className="space-y-1">
                  <div className="flex items-center space-x-3">
                    <span className="font-extrabold text-base text-foreground">{alert.threat_type}</span>
                    <span
                      className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${
                        alert.severity === 'CRITICAL'
                          ? 'bg-rose-500/10 text-rose-500 border border-rose-500/20'
                          : 'bg-amber-500/10 text-amber-500 border border-amber-500/20'
                      }`}
                    >
                      {alert.severity}
                    </span>
                    <span className="text-xs font-mono text-muted-foreground">
                      ID: {alert.alert_id} | Protocol: {alert.protocol}
                    </span>
                  </div>

                  <p className="text-xs text-muted-foreground leading-relaxed max-w-2xl">
                    {alert.clinical_explanation || 'Click Explain AI for detailed clinical impact analysis.'}
                  </p>

                  <div className="flex items-center space-x-4 text-[11px] text-muted-foreground pt-1">
                    <span>Source: <strong className="font-mono text-foreground">{alert.source_ip}</strong></span>
                    <span>Target: <strong className="font-mono text-foreground">{alert.destination_ip} ({alert.target_device_id || 'Medical Node'})</strong></span>
                    <span>Score: <strong className="text-medical-teal">{Math.round(alert.anomaly_score * 100)}%</strong></span>
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3 self-end md:self-center border-t md:border-t-0 pt-3 md:pt-0">
                <button
                  onClick={() => onSelectAlert(alert)}
                  className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-medical-teal text-white font-semibold text-xs shadow-glow-teal hover:opacity-90 transition-all"
                >
                  <Sparkles className="h-4 w-4" />
                  <span>Explain AI & Mitigation</span>
                </button>

                {alert.status !== 'MITIGATED' && (
                  <button
                    onClick={() => onUpdateStatus(alert.alert_id, 'MITIGATED')}
                    className="p-2 rounded-xl border bg-secondary hover:bg-emerald-500/10 hover:text-emerald-500 transition-colors"
                    title="Quick Mark Mitigated"
                  >
                    <CheckCircle2 className="h-5 w-5" />
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
