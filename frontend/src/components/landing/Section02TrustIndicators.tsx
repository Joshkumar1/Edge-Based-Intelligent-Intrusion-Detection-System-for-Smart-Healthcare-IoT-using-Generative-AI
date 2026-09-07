import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, Cpu, Lock, CheckCircle2 } from 'lucide-react';

export const Section02TrustIndicators: React.FC = () => {
  const stats = [
    {
      label: 'Offline Resilience',
      value: '100%',
      unit: 'Zero Cloud Dependency',
      desc: 'Operates continuously during total internet outages or network partitioning.',
      icon: ShieldCheck,
      color: 'text-medical-teal',
    },
    {
      label: 'Inference Latency',
      value: '< 1.2 ms',
      unit: 'Per Network Packet',
      desc: 'Sub-millisecond real-time anomaly evaluation on edge gateways.',
      icon: Cpu,
      color: 'text-emerald-500',
    },
    {
      label: 'Benchmark Accuracy',
      value: '99.24%',
      unit: 'Macro F1-Score',
      desc: 'Validated against Edge-IIoTset, N-BaIoT, and TON_IoT medical datasets.',
      icon: CheckCircle2,
      color: 'text-cyan-400',
    },
    {
      label: 'Patient Data Privacy',
      value: '0 Bytes',
      unit: 'Cloud Transmission',
      desc: 'Local Ollama SLM inference guarantees strict HIPAA/GDPR compliance.',
      icon: Lock,
      color: 'text-rose-500',
    },
  ];

  return (
    <section className="py-16 bg-card/40 border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, idx) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                className="p-6 rounded-2xl bg-card border shadow-subtle flex flex-col justify-between space-y-4 hover:border-medical-teal/40 transition-all hover:-translate-y-1"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                    {stat.label}
                  </span>
                  <div className={`p-2.5 rounded-xl bg-secondary ${stat.color}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                </div>

                <div>
                  <div className={`text-3xl sm:text-4xl font-extrabold tracking-tight ${stat.color}`}>
                    {stat.value}
                  </div>
                  <div className="text-xs font-semibold text-foreground mt-1 font-mono">
                    {stat.unit}
                  </div>
                </div>

                <p className="text-xs text-muted-foreground leading-relaxed pt-2 border-t">
                  {stat.desc}
                </p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
