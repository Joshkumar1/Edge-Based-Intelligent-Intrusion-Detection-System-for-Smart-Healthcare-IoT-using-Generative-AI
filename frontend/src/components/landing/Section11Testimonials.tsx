import React from 'react';
import { motion } from 'framer-motion';
import { Quote, Star, ShieldCheck } from 'lucide-react';

export const Section11Testimonials: React.FC = () => {
  const testimonials = [
    {
      name: 'Dr. Marcus Vance',
      role: 'Chief Medical Information Officer (CMIO)',
      org: 'MetroHealth University System',
      quote: 'EdgeShield AI completely eliminates the stress of cryptic security alerts. During a simulated DICOM ransomware test, the local AI explainer gave our team plain-language containment steps in seconds, protecting patient care continuity.',
      avatar: 'MV',
    },
    {
      name: 'Elena Rostova',
      role: 'Director of Biomedical Security',
      org: 'St. Jude Healthcare Network',
      quote: 'The fact that EdgeShield AI runs completely offline via local Ollama SLMs is a game changer for HIPAA compliance. Zero bytes of our patient telemetry leave the edge gateway.',
      avatar: 'ER',
    },
    {
      name: 'Prof. David Chen',
      role: 'IEEE Senior Member & IoT Researcher',
      org: 'Institute for Edge Cybersecurity',
      quote: 'The dual-stage Isolation Forest and XGBoost ML architecture combined with explainable AI sets a gold standard for IEEE publication. The sub-millisecond edge latency metrics are remarkable.',
      avatar: 'DC',
    },
  ];

  return (
    <section className="py-24 border-b bg-card/30 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-medical-teal/10 border border-medical-teal/20 text-medical-teal text-xs font-semibold">
            <Quote className="h-4 w-4" />
            <span>Trusted by Healthcare Leaders</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            Validated by Administrators, Biomedical Engineers & Researchers
          </h2>
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((t, idx) => (
            <motion.div
              key={t.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              className="p-8 rounded-3xl bg-card border shadow-subtle flex flex-col justify-between space-y-6 hover:border-medical-teal/40 transition-all"
            >
              <div className="space-y-4">
                <div className="flex items-center space-x-1 text-amber-400">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 fill-current" />
                  ))}
                </div>

                <p className="text-xs sm:text-sm text-foreground leading-relaxed italic">
                  "{t.quote}"
                </p>
              </div>

              <div className="flex items-center space-x-3 pt-4 border-t">
                <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-medical-teal to-teal-400 text-white font-bold text-xs flex items-center justify-center shadow-md">
                  {t.avatar}
                </div>
                <div>
                  <div className="font-bold text-xs text-foreground">{t.name}</div>
                  <div className="text-[11px] text-muted-foreground">{t.role}</div>
                  <div className="text-[10px] text-medical-teal font-semibold">{t.org}</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

      </div>
    </section>
  );
};
