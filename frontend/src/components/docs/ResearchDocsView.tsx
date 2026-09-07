import React from 'react';
import { BookOpen, ShieldCheck, Cpu, Database, Lock, Terminal, Award } from 'lucide-react';

export const ResearchDocsView: React.FC = () => {
  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <div className="border-b pb-4">
        <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-medical-teal mb-1">
          <Award className="h-4 w-4" />
          <span>IEEE Research & Technical Documentation</span>
        </div>
        <h2 className="text-2xl font-extrabold tracking-tight">
          EdgeShield AI: Intelligent Edge-Based Intrusion Detection for Smart Healthcare IoT
        </h2>
        <p className="text-sm text-muted-foreground mt-1">
          Architectural design decisions, edge ML pipeline, local SLM privacy compliance, and system implementation details.
        </p>
      </div>

      {/* Grid Documentation Modules */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Why Edge Computing? */}
        <div className="p-6 rounded-2xl bg-card border shadow-subtle space-y-3">
          <div className="flex items-center space-x-2 text-base font-bold text-foreground">
            <Cpu className="h-5 w-5 text-medical-teal" />
            <h3>Why Edge Computing for Smart Hospitals?</h3>
          </div>
          <p className="text-xs text-muted-foreground leading-relaxed">
            Cloud-based IDS architectures introduce unacceptable internet latency (&gt;250ms), cloud connection dependencies, and data exposure vulnerabilities. Medical IoT environments (ICU telemetry, infusion pumps, ventilators) demand sub-millisecond anomaly detection and 100% offline resilience during network partitioning.
          </p>
        </div>

        {/* Why Local LLMs? */}
        <div className="p-6 rounded-2xl bg-card border shadow-subtle space-y-3">
          <div className="flex items-center space-x-2 text-base font-bold text-foreground">
            <Lock className="h-5 w-5 text-medical-teal" />
            <h3>Privacy-Preserving Local AI Inference</h3>
          </div>
          <p className="text-xs text-muted-foreground leading-relaxed">
            Hospitals cannot transmit patient-identifying telemetry or internal network topology to public cloud LLMs due to strict HIPAA, HITECH, and GDPR compliance regulations. EdgeShield AI executes local Small Language Models (Ollama Llama-3 8B / Phi-3) directly on hospital edge gateways.
          </p>
        </div>

        {/* ML Engine Architecture */}
        <div className="p-6 rounded-2xl bg-card border shadow-subtle space-y-3">
          <div className="flex items-center space-x-2 text-base font-bold text-foreground">
            <Database className="h-5 w-5 text-medical-teal" />
            <h3>Dual-Stage ML Detection Pipeline</h3>
          </div>
          <p className="text-xs text-muted-foreground leading-relaxed">
            Combines unsupervised Isolation Forest (for zero-day anomaly boundary detection) with a multi-class XGBoost Classifier trained on benchmark IoT security datasets (Edge-IIoTset, N-BaIoT, TON_IoT).
          </p>
        </div>

        {/* Generative AI Role */}
        <div className="p-6 rounded-2xl bg-card border shadow-subtle space-y-3">
          <div className="flex items-center space-x-2 text-base font-bold text-foreground">
            <ShieldCheck className="h-5 w-5 text-medical-teal" />
            <h3>Generative AI Role Boundary</h3>
          </div>
          <p className="text-xs text-muted-foreground leading-relaxed">
            Generative AI NEVER makes security block/allow decisions. Security classification is handled deterministically by the ML model. The local SLM solely acts as an expert assistant—translating mathematical feature importances into plain-language clinical impact explanations and containment playbooks.
          </p>
        </div>
      </div>

      {/* IEEE Publication Outline Card */}
      <div className="p-6 rounded-2xl bg-card border shadow-subtle space-y-4">
        <div className="flex items-center space-x-2 border-b pb-3 font-bold text-base">
          <BookOpen className="h-5 w-5 text-medical-teal" />
          <span>IEEE Research Paper Structure Outline</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          <div className="p-3 rounded-xl bg-secondary/50 border">
            <div className="font-bold text-foreground">I. Introduction</div>
            <div className="text-muted-foreground">Smart hospital IoT attack surfaces & edge constraints.</div>
          </div>

          <div className="p-3 rounded-xl bg-secondary/50 border">
            <div className="font-bold text-foreground">II. Related Work</div>
            <div className="text-muted-foreground">Survey of network IDS, local SLMs, and medical IoT security.</div>
          </div>

          <div className="p-3 rounded-xl bg-secondary/50 border">
            <div className="font-bold text-foreground">III. EdgeShield System Architecture</div>
            <div className="text-muted-foreground">Dual ML engine, local Ollama integration, WebSocket streaming.</div>
          </div>

          <div className="p-3 rounded-xl bg-secondary/50 border">
            <div className="font-bold text-foreground">IV. Experimental Benchmarks</div>
            <div className="text-muted-foreground">Precision, Recall, F1, and sub-millisecond edge latency metrics.</div>
          </div>

          <div className="p-3 rounded-xl bg-secondary/50 border">
            <div className="font-bold text-foreground">V. Clinical Explainability Case Studies</div>
            <div className="text-muted-foreground">DICOM ransomware & MQTT flood mitigation playbooks.</div>
          </div>

          <div className="p-3 rounded-xl bg-secondary/50 border">
            <div className="font-bold text-foreground">VI. Conclusion & Future Work</div>
            <div className="text-muted-foreground">Edge computing roadmap for smart healthcare defense.</div>
          </div>
        </div>
      </div>
    </div>
  );
};
