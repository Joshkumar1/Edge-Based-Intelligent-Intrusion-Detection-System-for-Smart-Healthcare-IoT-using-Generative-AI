import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, ShieldCheck, Sparkles, HeartPulse, ArrowUpRight } from 'lucide-react';

export const Section03WhyEdgeShield: React.FC = () => {
  const pillars = [
    {
      id: 'edge',
      title: 'Low-Latency Edge Computing',
      tag: 'Zero Cloud Dependency',
      desc: 'Traditional cloud firewalls introduce unacceptable network latency (>200ms) and crash during internet link failures. EdgeShield AI processes network telemetry directly on local NVIDIA Jetson & industrial rack gateways with < 1.2ms latency.',
      icon: Cpu,
      gradient: 'from-medical-teal to-teal-500',
    },
    {
      id: 'ml-ids',
      title: 'Dual-Stage Machine Learning IDS',
      tag: 'Zero-Day Anomaly Detection',
      desc: 'Fixed signatures miss polymorphic malware. EdgeShield AI combines an unsupervised Isolation Forest (detecting unknown anomaly boundaries) with an XGBoost classifier trained on benchmark medical IoT datasets.',
      icon: ShieldCheck,
      gradient: 'from-cyan-500 to-blue-600',
    },
    {
      id: 'genai',
      title: 'Local Generative AI Assistant',
      tag: 'Ollama Local SLM',
      desc: 'Translates raw mathematical feature importances and network signatures into plain-language clinical risk explanations and step-by-step mitigation playbooks using local Llama-3 / Phi-3 SLMs.',
      icon: Sparkles,
      gradient: 'from-amber-500 to-rose-500',
    },
    {
      id: 'privacy',
      title: 'Privacy-First Healthcare Design',
      tag: 'HIPAA & GDPR Compliant',
      desc: 'Medical telemetry contains sensitive patient identifiers and internal hospital topology. EdgeShield AI never transmits data to cloud APIs, guaranteeing 100% patient data confidentiality.',
      icon: HeartPulse,
      gradient: 'from-emerald-500 to-teal-600',
    },
  ];

  return (
    <section id="why-edgeshield" className="py-24 border-b relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-medical-teal/10 border border-medical-teal/20 text-medical-teal text-xs font-semibold">
            <span>Why EdgeShield AI</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            Engineered Specifically for the High-Stakes Reality of Smart Hospitals
          </h2>
          <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
            Traditional IDS products only emit cryptic technical alerts. EdgeShield AI detects, explains, and guides hospital administrators with sub-millisecond precision.
          </p>
        </div>

        {/* 4 Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {pillars.map((pillar, idx) => {
            const Icon = pillar.icon;
            return (
              <motion.div
                key={pillar.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                whileHover={{ y: -6 }}
                className="group p-8 rounded-3xl bg-card border shadow-subtle flex flex-col justify-between space-y-6 hover:border-medical-teal/40 transition-all relative overflow-hidden"
              >
                {/* Accent Corner Glow */}
                <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${pillar.gradient} opacity-5 blur-2xl group-hover:opacity-15 transition-opacity`} />

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className={`h-12 w-12 rounded-2xl bg-gradient-to-tr ${pillar.gradient} text-white flex items-center justify-center shadow-lg`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <span className="text-xs font-bold px-3 py-1 rounded-full bg-secondary text-foreground border font-mono">
                      {pillar.tag}
                    </span>
                  </div>

                  <h3 className="text-xl font-bold tracking-tight text-foreground group-hover:text-medical-teal transition-colors">
                    {pillar.title}
                  </h3>

                  <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                    {pillar.desc}
                  </p>
                </div>

                <div className="pt-4 border-t flex items-center text-xs font-semibold text-medical-teal group-hover:translate-x-1 transition-transform">
                  <span>Explore Architectural Blueprint</span>
                  <ArrowUpRight className="h-4 w-4 ml-1" />
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
