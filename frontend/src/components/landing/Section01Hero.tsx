import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, ArrowRight, FileText, Cpu, Activity, Lock, Radio, Zap, HeartPulse } from 'lucide-react';

interface Section01HeroProps {
  onLaunchDashboard: () => void;
}

export const Section01Hero: React.FC<Section01HeroProps> = ({ onLaunchDashboard }) => {
  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative pt-32 pb-20 lg:pt-40 lg:pb-32 overflow-hidden border-b">
      {/* Background Glow Orbs */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-medical-teal/20 via-cyan-500/15 to-transparent blur-[120px] rounded-full pointer-events-none -z-10" />
      <div className="absolute top-1/3 right-10 w-[400px] h-[300px] bg-rose-500/10 blur-[100px] rounded-full pointer-events-none -z-10" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          
          {/* Left Column: Headline & Value Prop */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="lg:col-span-7 space-y-6 text-center lg:text-left"
          >
            {/* Tag Badge */}
            <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-medical-teal/10 border border-medical-teal/20 text-medical-teal text-xs font-semibold">
              <span className="h-2 w-2 rounded-full bg-medical-teal animate-ping" />
              <span>IEEE Research & Enterprise Healthcare AI</span>
            </div>

            {/* Main Headline */}
            <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-foreground leading-[1.1]">
              Protecting Smart Hospitals with{' '}
              <span className="bg-gradient-to-r from-medical-teal via-teal-400 to-cyan-400 bg-clip-text text-transparent">
                Edge Intelligence
              </span>
            </h1>

            {/* Subtitle */}
            <p className="text-base sm:text-lg text-muted-foreground max-w-2xl mx-auto lg:mx-0 leading-relaxed">
              Sub-millisecond intrusion detection for medical IoT devices powered by Edge Computing, Machine Learning, and Privacy-Preserving Local Generative AI. Zero cloud dependency. 100% patient data confidentiality.
            </p>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              <button
                onClick={onLaunchDashboard}
                className="w-full sm:w-auto flex items-center justify-center space-x-3 px-7 py-3.5 rounded-2xl bg-gradient-to-r from-medical-teal to-teal-500 hover:from-teal-600 hover:to-medical-teal text-white font-bold text-sm shadow-glow-teal hover:scale-[1.02] active:scale-[0.98] transition-all"
              >
                <ShieldCheck className="h-5 w-5" />
                <span>Launch Security Cockpit</span>
                <ArrowRight className="h-4 w-4" />
              </button>

              <button
                onClick={() => scrollToSection('research')}
                className="w-full sm:w-auto flex items-center justify-center space-x-2 px-7 py-3.5 rounded-2xl bg-card border hover:bg-secondary text-foreground font-semibold text-sm transition-all"
              >
                <FileText className="h-4 w-4 text-medical-teal" />
                <span>Explore IEEE Paper</span>
              </button>
            </div>

            {/* Trust Micro-Badges */}
            <div className="pt-6 grid grid-cols-3 gap-4 border-t max-w-lg mx-auto lg:mx-0 text-left">
              <div>
                <div className="text-xs font-bold text-foreground font-mono">&lt; 1.2 ms</div>
                <div className="text-[11px] text-muted-foreground">Edge Latency</div>
              </div>
              <div>
                <div className="text-xs font-bold text-emerald-500 font-mono">99.24%</div>
                <div className="text-[11px] text-muted-foreground">Macro Accuracy</div>
              </div>
              <div>
                <div className="text-xs font-bold text-cyan-400 font-mono">0 Bytes</div>
                <div className="text-[11px] text-muted-foreground">Cloud Data Leakage</div>
              </div>
            </div>
          </motion.div>

          {/* Right Column: Interactive Hospital Network Graphic */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="lg:col-span-5 relative"
          >
            <div className="relative p-6 rounded-3xl bg-card/60 border shadow-glass backdrop-blur-md overflow-hidden space-y-6">
              
              {/* Top Graphic Header */}
              <div className="flex items-center justify-between border-b pb-3 text-xs font-mono">
                <div className="flex items-center space-x-2 text-medical-teal font-semibold">
                  <Activity className="h-4 w-4 animate-pulse" />
                  <span>HOSPITAL_EDGE_GATEWAY_NODE</span>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-500 font-bold border border-emerald-500/20">
                  DEFENSE ACTIVE
                </span>
              </div>

              {/* Animated Hospital Network Diagram */}
              <div className="relative h-72 w-full flex items-center justify-center">
                {/* SVG Connection Lines */}
                <svg className="absolute inset-0 w-full h-full pointer-events-none" xmlns="http://www.w3.org/2000/svg">
                  <line x1="20%" y1="30%" x2="50%" y2="50%" stroke="rgba(13, 148, 136, 0.4)" strokeWidth="2" strokeDasharray="4 4" />
                  <line x1="80%" y1="30%" x2="50%" y2="50%" stroke="rgba(13, 148, 136, 0.4)" strokeWidth="2" strokeDasharray="4 4" />
                  <line x1="20%" y1="75%" x2="50%" y2="50%" stroke="rgba(13, 148, 136, 0.4)" strokeWidth="2" strokeDasharray="4 4" />
                  <line x1="80%" y1="75%" x2="50%" y2="50%" stroke="rgba(13, 148, 136, 0.4)" strokeWidth="2" strokeDasharray="4 4" />
                </svg>

                {/* Center Node: Local AI Edge Brain */}
                <motion.div
                  animate={{ scale: [1, 1.05, 1] }}
                  transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
                  className="z-10 h-20 w-20 rounded-2xl bg-gradient-to-tr from-medical-teal to-cyan-400 p-0.5 shadow-glow-teal flex items-center justify-center"
                >
                  <div className="h-full w-full bg-card rounded-[14px] flex flex-col items-center justify-center text-center p-2">
                    <Cpu className="h-7 w-7 text-medical-teal animate-pulse" />
                    <span className="text-[9px] font-mono font-bold text-foreground mt-1">Ollama SLM</span>
                  </div>
                </motion.div>

                {/* Top-Left: Infusion Pump */}
                <div className="absolute top-[10%] left-[10%] p-3 rounded-xl bg-card border shadow-subtle flex items-center space-x-2">
                  <div className="p-1.5 rounded-lg bg-medical-teal/10 text-medical-teal">
                    <HeartPulse className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="text-[11px] font-bold">Infusion Pump</div>
                    <div className="text-[9px] font-mono text-muted-foreground">MQTT | 192.168.10.102</div>
                  </div>
                </div>

                {/* Top-Right: DICOM Workstation */}
                <div className="absolute top-[10%] right-[10%] p-3 rounded-xl bg-card border shadow-subtle flex items-center space-x-2">
                  <div className="p-1.5 rounded-lg bg-rose-500/10 text-rose-500">
                    <Zap className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="text-[11px] font-bold">DICOM PACS</div>
                    <div className="text-[9px] font-mono text-muted-foreground">Port 104 | Ransomware Alert</div>
                  </div>
                </div>

                {/* Bottom-Left: ICU Ventilator */}
                <div className="absolute bottom-[10%] left-[10%] p-3 rounded-xl bg-card border shadow-subtle flex items-center space-x-2">
                  <div className="p-1.5 rounded-lg bg-cyan-500/10 text-cyan-400">
                    <Radio className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="text-[11px] font-bold">ICU Telemetry</div>
                    <div className="text-[9px] font-mono text-muted-foreground">Modbus FC3</div>
                  </div>
                </div>

                {/* Bottom-Right: Security Admin */}
                <div className="absolute bottom-[10%] right-[10%] p-3 rounded-xl bg-card border shadow-subtle flex items-center space-x-2">
                  <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-500">
                    <Lock className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="text-[11px] font-bold">Local Shield</div>
                    <div className="text-[9px] font-mono text-muted-foreground">100% Privacy</div>
                  </div>
                </div>
              </div>

              {/* Live Incident Status Ticker */}
              <div className="p-3 rounded-xl bg-secondary/70 border text-xs flex items-center justify-between">
                <div className="flex items-center space-x-2 text-foreground font-mono">
                  <span className="h-2 w-2 rounded-full bg-emerald-500" />
                  <span>Real-time Isolation Forest + XGBoost scoring active</span>
                </div>
                <span className="text-[10px] text-muted-foreground font-mono">0.84ms</span>
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
};
