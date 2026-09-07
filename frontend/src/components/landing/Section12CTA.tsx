import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, ArrowRight, Sparkles, FileText } from 'lucide-react';

interface Section12CTAProps {
  onLaunchDashboard: () => void;
}

export const Section12CTA: React.FC<Section12CTAProps> = ({ onLaunchDashboard }) => {
  return (
    <section className="py-24 border-b relative overflow-hidden">
      {/* Glow Effects */}
      <div className="absolute inset-0 bg-gradient-to-tr from-medical-teal/10 via-transparent to-rose-500/10 pointer-events-none" />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="p-10 sm:p-14 rounded-3xl bg-card border border-medical-teal/40 shadow-glass text-center space-y-8 relative overflow-hidden"
        >
          <div className="h-16 w-16 rounded-2xl bg-gradient-to-tr from-medical-teal to-cyan-400 text-white flex items-center justify-center mx-auto shadow-glow-teal">
            <ShieldCheck className="h-8 w-8" />
          </div>

          <div className="space-y-4 max-w-2xl mx-auto">
            <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-foreground">
              Ready to Protect Smart Hospital Infrastructure?
            </h2>
            <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
              Experience edge-native intrusion detection, real-time WebSocket telemetry, and privacy-preserving local AI explanations today.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
            <button
              onClick={onLaunchDashboard}
              className="w-full sm:w-auto flex items-center justify-center space-x-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-medical-teal to-teal-500 hover:from-teal-600 hover:to-medical-teal text-white font-bold text-sm shadow-glow-teal hover:scale-105 transition-all"
            >
              <Sparkles className="h-5 w-5" />
              <span>Launch Hospital Security Cockpit</span>
              <ArrowRight className="h-4 w-4" />
            </button>

            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto flex items-center justify-center space-x-2 px-8 py-4 rounded-2xl bg-card border hover:bg-secondary text-foreground font-semibold text-sm transition-all"
            >
              <FileText className="h-4 w-4 text-medical-teal" />
              <span>View GitHub Repository</span>
            </a>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
