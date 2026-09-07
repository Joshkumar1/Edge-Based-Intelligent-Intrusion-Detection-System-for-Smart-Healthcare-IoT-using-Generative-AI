import React from 'react';
import { BarChart3, CheckCircle2, Cpu, FileCheck, Layers, ShieldCheck } from 'lucide-react';
import { MLMetrics } from '../../types';

interface AnalyticsViewProps {
  metrics: MLMetrics;
}

export const AnalyticsView: React.FC<AnalyticsViewProps> = ({ metrics }) => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">IEEE Research ML Analytics & Evaluation</h2>
          <p className="text-sm text-muted-foreground">
            Benchmarking detection precision, macro F1-scores, and feature importance distributions.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-semibold px-3 py-1.5 rounded-xl bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
          <CheckCircle2 className="h-4 w-4" />
          <span>IEEE Research Benchmark Metrics</span>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-card border shadow-subtle text-center space-y-2">
          <div className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Macro Precision</div>
          <div className="text-4xl font-extrabold text-medical-teal">
            {(metrics.metrics.macro_precision * 100).toFixed(2)}%
          </div>
          <p className="text-xs text-muted-foreground">Minimal false positives across all attack vectors</p>
        </div>

        <div className="p-6 rounded-2xl bg-card border shadow-subtle text-center space-y-2">
          <div className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Macro Recall</div>
          <div className="text-4xl font-extrabold text-emerald-500">
            {(metrics.metrics.macro_recall * 100).toFixed(2)}%
          </div>
          <p className="text-xs text-muted-foreground">High detection sensitivity for zero-day anomalies</p>
        </div>

        <div className="p-6 rounded-2xl bg-card border shadow-subtle text-center space-y-2">
          <div className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Macro F1-Score</div>
          <div className="text-4xl font-extrabold text-blue-500">
            {(metrics.metrics.macro_f1 * 100).toFixed(2)}%
          </div>
          <p className="text-xs text-muted-foreground">Harmonic mean balance suitable for paper publication</p>
        </div>
      </div>

      {/* Model Architecture & Features Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Model Pipeline Specs */}
        <div className="p-6 rounded-2xl bg-card border shadow-subtle space-y-4">
          <div className="flex items-center space-x-2 border-b pb-3">
            <Layers className="h-5 w-5 text-medical-teal" />
            <h3 className="font-bold text-base">Dual-Stage ML Detection Architecture</h3>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-xl bg-secondary/50 border space-y-1">
              <div className="font-bold text-foreground">Stage 1: Isolation Forest (Zero-Day Anomaly Detector)</div>
              <p className="text-muted-foreground">
                Unsupervised anomaly detection trained exclusively on normal IoT operational vectors. Identifies unknown payload entropy spikes and traffic rate bursts.
              </p>
            </div>

            <div className="p-3 rounded-xl bg-secondary/50 border space-y-1">
              <div className="font-bold text-foreground">Stage 2: Multi-Class Threat Classifier (XGBoost / RandomForest)</div>
              <p className="text-muted-foreground">
                Supervised multi-class model trained on benchmark medical IoT datasets (Edge-IIoTset, N-BaIoT). Classifies attacks into DICOM Ransomware, MQTT Flood, Modbus Injection, ARP Spoofing, or Port Scans.
              </p>
            </div>
          </div>
        </div>

        {/* Feature Dictionary */}
        <div className="p-6 rounded-2xl bg-card border shadow-subtle space-y-4">
          <div className="flex items-center space-x-2 border-b pb-3">
            <BarChart3 className="h-5 w-5 text-medical-teal" />
            <h3 className="font-bold text-base">Extracted Network Telemetry Features</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {metrics.features.map((feat) => (
              <div key={feat} className="p-2.5 rounded-xl border bg-secondary/30 text-xs font-mono flex items-center justify-between">
                <span>{feat}</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-medical-teal/10 text-medical-teal">
                  Active
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
