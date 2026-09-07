import React from 'react';
import { motion } from 'framer-motion';
import { Layers, Cpu, Database, Box, Radio, Code2, Server, ShieldCheck } from 'lucide-react';

export const Section10TechStack: React.FC = () => {
  const techStack = [
    { name: 'React 18 & TypeScript', category: 'Frontend UI', desc: 'Strict component architecture, Framer Motion, and Tailwind CSS.', icon: Code2 },
    { name: 'FastAPI & Python 3.11', category: 'Backend API', desc: 'High-performance asynchronous Python REST & WebSockets gateway.', icon: Server },
    { name: 'Ollama & Llama 3 8B', category: 'Local GenAI', desc: 'Privacy-preserving offline SLM inference running locally.', icon: Cpu },
    { name: 'Isolation Forest', category: 'Zero-Day ML', desc: 'Unsupervised anomaly detection trained on baseline IoT vectors.', icon: ShieldCheck },
    { name: 'XGBoost Classifier', category: 'Multi-Class ML', desc: 'Supervised threat classification model with SHAP feature weights.', icon: Layers },
    { name: 'SQLAlchemy & SQLite', category: 'Database Storage', desc: 'High-reliability SQL schema tracking devices, alerts, and packet logs.', icon: Database },
    { name: 'WebSockets Engine', category: 'Real-Time Telemetry', desc: 'Sub-second streaming network telemetry and instant push alerts.', icon: Radio },
    { name: 'Docker & Docker Compose', category: 'Deployment', desc: 'Multi-container orchestration for 1-click hospital edge deployment.', icon: Box },
  ];

  return (
    <section id="tech-stack" className="py-24 border-b relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-medical-teal/10 border border-medical-teal/20 text-medical-teal text-xs font-semibold">
            <Layers className="h-4 w-4" />
            <span>Modern Technology Stack</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            Built with Modern, Production-Grade Technologies
          </h2>
          <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
            Every library, model, and framework was selected for maximum speed, strict type safety, and zero cloud dependency.
          </p>
        </div>

        {/* Tech Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {techStack.map((tech, idx) => {
            const Icon = tech.icon;
            return (
              <motion.div
                key={tech.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.05 }}
                whileHover={{ y: -4 }}
                className="p-6 rounded-2xl bg-card border shadow-subtle flex flex-col justify-between space-y-4 hover:border-medical-teal/40 transition-all"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="p-2.5 rounded-xl bg-medical-teal/10 text-medical-teal border border-medical-teal/20">
                      <Icon className="h-5 w-5" />
                    </div>
                    <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-secondary text-muted-foreground border">
                      {tech.category}
                    </span>
                  </div>

                  <h4 className="font-bold text-base text-foreground">{tech.name}</h4>
                  <p className="text-xs text-muted-foreground leading-relaxed">{tech.desc}</p>
                </div>
              </motion.div>
            );
          })}
        </div>

      </div>
    </section>
  );
};
