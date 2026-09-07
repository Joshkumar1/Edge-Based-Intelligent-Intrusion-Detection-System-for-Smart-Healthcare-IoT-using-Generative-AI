import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Monitor, Cpu, ShieldCheck, Sparkles, LayoutDashboard, CheckCircle2 } from 'lucide-react';

export const Section05Architecture: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState('edge-gateway');

  const nodes = [
    {
      id: 'iot-devices',
      label: 'Smart Medical IoT Devices',
      category: 'Network Edge',
      icon: Monitor,
      desc: 'Infusion Pumps, ICU Patient Monitors, DICOM PACS Radiology Workstations, and Smart Ventilators.',
      specs: ['Protocols: DICOM, MQTT, Modbus/TCP, HL7', 'Subnets: VLAN 10 (ICU), VLAN 20 (Radiology)', 'Streaming Packet Rate: 10 - 450 pkts/sec'],
    },
    {
      id: 'edge-gateway',
      label: 'Edge Security Gateway Node',
      category: 'Edge Hardware',
      icon: Cpu,
      desc: 'NVIDIA Jetson / Industrial x86 rack server deployed on-premises inside the hospital server rack.',
      specs: ['Hardware: NVIDIA Jetson Orin / Industrial PC', 'Inference Latency: < 1.2 ms per packet', 'Offline Resilience: 100% (Zero Cloud Dependency)'],
    },
    {
      id: 'ml-engine',
      label: 'Dual ML Intrusion Detector',
      category: 'Machine Learning',
      icon: ShieldCheck,
      desc: 'Isolation Forest (for zero-day anomaly boundaries) + XGBoost Classifier (for multi-class threat signatures).',
      specs: ['Accuracy: 99.24% Macro F1-Score', 'Features: Byte entropy, packet rate, flow duration, SYN flags', 'Benchmark Datasets: Edge-IIoTset, N-BaIoT, TON_IoT'],
    },
    {
      id: 'local-slm',
      label: 'Privacy-Preserving Local SLM',
      category: 'Generative AI',
      icon: Sparkles,
      desc: 'Ollama API running Llama-3 8B / Phi-3 locally with deterministic expert rule synthesis fallback.',
      specs: ['Privacy: 0 Bytes patient data cloud transmission', 'Output: Clinical impact & step-by-step containment playbooks', 'Compliance: HIPAA, HITECH & GDPR compliant'],
    },
    {
      id: 'dashboard',
      label: 'Hospital Security Cockpit UI',
      category: 'User Experience',
      icon: LayoutDashboard,
      desc: 'High-clarity dashboard built for hospital IT administrators, biomedical engineers, and security analysts.',
      specs: ['Real-time WebSockets telemetry streaming', 'Stress-reducing visual ergonomics & Dark/Light mode', '1-Click containment execution'],
    },
  ];

  const currentNode = nodes.find((n) => n.id === selectedNode) || nodes[1];

  return (
    <section id="architecture" className="py-24 border-b relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-medical-teal/10 border border-medical-teal/20 text-medical-teal text-xs font-semibold">
            <span>Interactive Topology Visualizer</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            Modular Edge Architecture
          </h2>
          <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
            Click on any architectural node below to inspect data flows, protocol specifications, and security guarantees.
          </p>
        </div>

        {/* Node Flow Tabs */}
        <div className="flex items-center justify-center space-x-2 overflow-x-auto pb-6">
          {nodes.map((node) => {
            const Icon = node.icon;
            const isSelected = selectedNode === node.id;
            return (
              <button
                key={node.id}
                onClick={() => setSelectedNode(node.id)}
                className={`flex items-center space-x-2 px-4 py-3 rounded-2xl text-xs font-bold whitespace-nowrap transition-all ${
                  isSelected
                    ? 'bg-medical-teal text-white shadow-glow-teal scale-105'
                    : 'bg-card border text-muted-foreground hover:text-foreground hover:bg-secondary'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{node.label}</span>
              </button>
            );
          })}
        </div>

        {/* Selected Node Details Card */}
        <motion.div
          key={selectedNode}
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="max-w-4xl mx-auto p-8 rounded-3xl bg-card border shadow-glass space-y-6"
        >
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4">
            <div className="flex items-center space-x-3">
              <div className="p-3.5 rounded-2xl bg-medical-teal/10 text-medical-teal border border-medical-teal/20">
                {React.createElement(currentNode.icon, { className: 'h-7 w-7' })}
              </div>
              <div>
                <span className="text-xs font-mono font-bold text-medical-teal uppercase tracking-wider">
                  {currentNode.category}
                </span>
                <h3 className="text-xl font-bold tracking-tight text-foreground">
                  {currentNode.label}
                </h3>
              </div>
            </div>

            <span className="text-xs font-mono bg-secondary px-3.5 py-1.5 rounded-full text-foreground border font-semibold">
              STATUS: OPERATIONAL
            </span>
          </div>

          <p className="text-sm text-foreground leading-relaxed">
            {currentNode.desc}
          </p>

          <div className="space-y-2 pt-2">
            <div className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
              Technical Specifications & System Parameters:
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {currentNode.specs.map((spec, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-secondary/50 border text-xs font-mono text-foreground flex items-center space-x-2">
                  <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" />
                  <span>{spec}</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

      </div>
    </section>
  );
};
