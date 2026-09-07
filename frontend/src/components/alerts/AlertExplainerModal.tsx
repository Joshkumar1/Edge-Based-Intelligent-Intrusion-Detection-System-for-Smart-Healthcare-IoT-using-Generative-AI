import React, { useState } from 'react';
import { X, Sparkles, AlertTriangle, ShieldCheck, CheckCircle2, Copy, FileText, Cpu } from 'lucide-react';
import { Alert } from '../../types';

interface AlertExplainerModalProps {
  alert: Alert | null;
  onClose: () => void;
  onUpdateStatus: (alertId: string, status: string) => void;
}

export const AlertExplainerModal: React.FC<AlertExplainerModalProps> = ({
  alert,
  onClose,
  onUpdateStatus,
}) => {
  const [copied, setCopied] = useState(false);

  if (!alert) return null;

  const handleCopyMitigation = () => {
    if (alert.recommended_mitigation) {
      navigator.clipboard.writeText(alert.recommended_mitigation);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto animate-in fade-in">
      <div className="bg-card border rounded-2xl max-w-3xl w-full p-6 shadow-2xl space-y-6 relative overflow-hidden">
        {/* Top Accent Gradient Bar */}
        <div
          className={`absolute top-0 left-0 right-0 h-2 ${
            alert.severity === 'CRITICAL'
              ? 'bg-gradient-to-r from-rose-600 via-rose-500 to-amber-500'
              : 'bg-gradient-to-r from-amber-500 to-medical-teal'
          }`}
        />

        {/* Modal Header */}
        <div className="flex items-start justify-between border-b pb-4 pt-2">
          <div className="flex items-center space-x-3">
            <div
              className={`p-3 rounded-2xl text-white font-bold ${
                alert.severity === 'CRITICAL' ? 'bg-rose-500 shadow-glow-red' : 'bg-amber-500'
              }`}
            >
              <AlertTriangle className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-xl font-extrabold tracking-tight">{alert.threat_type}</h3>
                <span
                  className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${
                    alert.severity === 'CRITICAL'
                      ? 'bg-rose-500/10 text-rose-500 border border-rose-500/20'
                      : 'bg-amber-500/10 text-amber-500 border border-amber-500/20'
                  }`}
                >
                  {alert.severity} SEVERITY
                </span>
              </div>
              <p className="text-xs text-muted-foreground mt-0.5 font-mono">
                Incident ID: {alert.alert_id} | Target Device: {alert.target_device_id || 'Medical IoT Node'} ({alert.protocol})
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl border bg-secondary/80 hover:bg-secondary transition-colors text-muted-foreground hover:text-foreground"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* AI Engine Banner */}
        <div className="p-3 rounded-xl bg-medical-teal/10 border border-medical-teal/20 text-xs flex items-center justify-between">
          <div className="flex items-center space-x-2 text-medical-teal font-medium">
            <Sparkles className="h-4 w-4" />
            <span>Local Generative AI Security Assistant (Offline Local Inference)</span>
          </div>
          <span className="text-[10px] font-mono bg-card px-2.5 py-1 rounded-md border text-muted-foreground">
            Latency: 12ms | Zero Cloud Data Transmission
          </span>
        </div>

        {/* AI Explainer Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Plain English Explanation */}
          <div className="p-4 rounded-xl bg-secondary/50 border space-y-2">
            <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-muted-foreground">
              <FileText className="h-4 w-4 text-medical-teal" />
              <span>Human-Understandable Explanation</span>
            </div>
            <p className="text-xs leading-relaxed text-foreground font-normal">
              {alert.clinical_explanation || 'Synthesizing explanation from local ML feature vector...'}
            </p>
          </div>

          {/* Clinical Operational Impact */}
          <div className="p-4 rounded-xl bg-rose-500/5 border border-rose-500/20 space-y-2">
            <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-rose-500">
              <AlertTriangle className="h-4 w-4" />
              <span>Hospital Operational Risk</span>
            </div>
            <p className="text-xs leading-relaxed text-foreground font-normal">
              {alert.clinical_impact || 'Evaluating patient workflow risks...'}
            </p>
          </div>
        </div>

        {/* Actionable Containment Playbook */}
        <div className="p-4 rounded-xl bg-card border space-y-3 shadow-subtle">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-foreground">
              <ShieldCheck className="h-4 w-4 text-emerald-500" />
              <span>Recommended Containment Playbook</span>
            </div>
            <button
              onClick={handleCopyMitigation}
              className="flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-secondary hover:bg-secondary/80 text-xs font-semibold border transition-all"
            >
              {copied ? <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> : <Copy className="h-3.5 w-3.5" />}
              <span>{copied ? 'Copied!' : 'Copy Playbook'}</span>
            </button>
          </div>

          <div className="p-3 rounded-lg bg-secondary/60 font-mono text-xs text-foreground whitespace-pre-wrap leading-relaxed border">
            {alert.recommended_mitigation || '1. Isolate device at switch port level.\n2. Block source IP address.'}
          </div>
        </div>

        {/* Feature Telemetry Contributions */}
        {alert.key_features && (
          <div className="space-y-2">
            <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
              ML Feature Vector Anomalies
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {Object.entries(alert.key_features).map(([key, val]) => (
                <div key={key} className="p-2.5 rounded-lg border bg-secondary/30 text-xs flex justify-between items-center">
                  <span className="font-mono text-muted-foreground">{key}</span>
                  <span className="font-bold text-foreground">{val}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex items-center justify-between border-t pt-4">
          <div className="text-xs text-muted-foreground">
            Current Status: <span className="font-bold text-foreground">{alert.status}</span>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={() => {
                onUpdateStatus(alert.alert_id, 'FALSE_POSITIVE');
                onClose();
              }}
              className="px-4 py-2 rounded-xl border bg-secondary hover:bg-secondary/80 text-xs font-semibold transition-all"
            >
              Mark False Positive
            </button>

            <button
              onClick={() => {
                onUpdateStatus(alert.alert_id, 'MITIGATED');
                onClose();
              }}
              className="flex items-center space-x-2 px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-glow-teal transition-all"
            >
              <CheckCircle2 className="h-4 w-4" />
              <span>Confirm & Mark Mitigated</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
