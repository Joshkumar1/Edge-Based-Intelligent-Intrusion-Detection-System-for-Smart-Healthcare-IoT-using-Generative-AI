import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { HeartPulse, Cpu, ShieldCheck, Sparkles, CheckCircle2, ArrowRight } from 'lucide-react';

export const Section04HowItWorks: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    {
      num: '01',
      title: 'Medical Device Telemetry',
      subtitle: 'DICOM, MQTT & Modbus Traffic Ingestion',
      desc: 'Infusion pumps, ICU patient monitors, and DICOM PACS workstations transmit raw network packets into the local edge gateway interface.',
      icon: HeartPulse,
      details: 'Feature extraction captures packet length, byte entropy, flow duration, MQTT rates, and Modbus function codes.',
    },
    {
      num: '02',
      title: 'Sub-Millisecond Edge Evaluation',
      subtitle: 'NVIDIA Jetson / Industrial Gateway',
      desc: 'Features pass through the standardized scaler and Isolation Forest model in < 1.2ms without sending data to external cloud servers.',
      icon: Cpu,
      details: 'Unsupervised anomaly scoring measures decision distance from baseline normal operational vectors.',
    },
    {
      num: '03',
      title: 'ML Threat Classification',
      subtitle: 'Supervised Multi-Class XGBoost Model',
      desc: 'If an anomaly is detected, the multi-class model identifies the precise attack type (DICOM Ransomware, MQTT Flood, Modbus Injection, ARP Spoofing).',
      icon: ShieldCheck,
      details: 'Calculates top contributing feature importance weights (SHAP values).',
    },
    {
      num: '04',
      title: 'Local AI Clinical Explainer',
      subtitle: 'Ollama Offline SLM Inference',
      desc: 'The local SLM translates complex mathematical feature weights into human-readable clinical impact descriptions and containment steps.',
      icon: Sparkles,
      details: 'Ensures zero cognitive load for hospital administrators and biomedical staff.',
    },
    {
      num: '05',
      title: 'Actionable Containment Response',
      subtitle: 'VLAN Isolation & Mitigation',
      desc: 'IT admins execute 1-click containment commands to isolate infected MAC addresses, block malicious ports, and protect patient safety.',
      icon: CheckCircle2,
      details: 'Instant status update pushed across real-time WebSockets to all hospital security terminals.',
    },
  ];

  return (
    <section id="how-it-works" className="py-24 border-b bg-card/30 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-medical-teal/10 border border-medical-teal/20 text-medical-teal text-xs font-semibold">
            <span>5-Step Execution Pipeline</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            How EdgeShield AI Protects Hospital Infrastructure
          </h2>
          <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
            From raw network packet ingestion to local LLM clinical explanations—every stage runs on the edge.
          </p>
        </div>

        {/* Timeline Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          {/* Step Selector List */}
          <div className="lg:col-span-5 space-y-3">
            {steps.map((step, idx) => {
              const Icon = step.icon;
              const isActive = activeStep === idx;
              return (
                <div
                  key={step.num}
                  onClick={() => setActiveStep(idx)}
                  className={`p-4 rounded-2xl border cursor-pointer transition-all flex items-start space-x-4 ${
                    isActive
                      ? 'bg-card border-medical-teal shadow-glow-teal'
                      : 'bg-card/40 border-transparent hover:bg-card hover:border-border'
                  }`}
                >
                  <div
                    className={`p-2.5 rounded-xl font-mono text-xs font-extrabold ${
                      isActive ? 'bg-medical-teal text-white' : 'bg-secondary text-muted-foreground'
                    }`}
                  >
                    {step.num}
                  </div>

                  <div className="flex-1 space-y-1">
                    <div className="flex items-center justify-between">
                      <h4 className={`font-bold text-sm ${isActive ? 'text-foreground' : 'text-muted-foreground'}`}>
                        {step.title}
                      </h4>
                      {isActive && <ArrowRight className="h-4 w-4 text-medical-teal" />}
                    </div>
                    <p className="text-xs text-muted-foreground line-clamp-1">{step.subtitle}</p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Active Step Feature Display */}
          <div className="lg:col-span-7">
            <motion.div
              key={activeStep}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4 }}
              className="p-8 rounded-3xl bg-card border shadow-glass space-y-6 relative overflow-hidden"
            >
              <div className="flex items-center justify-between border-b pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-3 rounded-2xl bg-medical-teal/10 text-medical-teal border border-medical-teal/20">
                    {React.createElement(steps[activeStep].icon, { className: 'h-6 w-6' })}
                  </div>
                  <div>
                    <span className="text-xs font-mono font-bold text-medical-teal">STAGE {steps[activeStep].num}</span>
                    <h3 className="text-xl font-bold tracking-tight text-foreground">
                      {steps[activeStep].title}
                    </h3>
                  </div>
                </div>

                <span className="text-xs font-mono bg-secondary px-3 py-1 rounded-full text-muted-foreground border">
                  {steps[activeStep].subtitle}
                </span>
              </div>

              <p className="text-sm text-foreground leading-relaxed">
                {steps[activeStep].desc}
              </p>

              <div className="p-4 rounded-xl bg-secondary/50 border space-y-1 text-xs">
                <div className="font-bold text-medical-teal uppercase tracking-wider font-mono">
                  Technical Specification:
                </div>
                <div className="text-muted-foreground font-mono">
                  {steps[activeStep].details}
                </div>
              </div>
            </motion.div>
          </div>

        </div>
      </div>
    </section>
  );
};
