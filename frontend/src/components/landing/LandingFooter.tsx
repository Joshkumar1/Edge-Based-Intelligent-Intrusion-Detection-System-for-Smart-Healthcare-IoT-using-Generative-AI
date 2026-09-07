import React from 'react';
import { ShieldCheck, Heart } from 'lucide-react';

export const LandingFooter: React.FC = () => {
  return (
    <footer className="bg-card/60 border-t py-12 text-xs text-muted-foreground">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Brand Info */}
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <div className="h-7 w-7 rounded-lg bg-medical-teal flex items-center justify-center text-white font-bold">
                <ShieldCheck className="h-4 w-4" />
              </div>
              <span className="font-extrabold text-sm text-foreground">EdgeShield AI</span>
            </div>
            <p className="text-[11px] leading-relaxed">
              Intelligent Edge-Based Intrusion Detection & Explainable AI Assistant for Smart Hospitals.
            </p>
          </div>

          {/* Product Links */}
          <div className="space-y-2">
            <div className="font-bold text-foreground uppercase tracking-wider">Product</div>
            <ul className="space-y-1.5">
              <li><a href="#why-edgeshield" className="hover:text-foreground transition-colors">Why EdgeShield</a></li>
              <li><a href="#how-it-works" className="hover:text-foreground transition-colors">How It Works</a></li>
              <li><a href="#architecture" className="hover:text-foreground transition-colors">System Architecture</a></li>
              <li><a href="#attack-sandbox" className="hover:text-foreground transition-colors">Live Sandbox</a></li>
            </ul>
          </div>

          {/* Research & Docs */}
          <div className="space-y-2">
            <div className="font-bold text-foreground uppercase tracking-wider">Research</div>
            <ul className="space-y-1.5">
              <li><a href="#research" className="hover:text-foreground transition-colors">IEEE Publication Outline</a></li>
              <li><a href="#tech-stack" className="hover:text-foreground transition-colors">ML Benchmark Datasets</a></li>
              <li><a href="/api/v1/openapi.json" target="_blank" className="hover:text-foreground transition-colors">REST API Reference</a></li>
              <li><a href="http://localhost:8000/docs" target="_blank" className="hover:text-foreground transition-colors">FastAPI Swagger Docs</a></li>
            </ul>
          </div>

          {/* Legal & Compliance */}
          <div className="space-y-2">
            <div className="font-bold text-foreground uppercase tracking-wider">Compliance</div>
            <ul className="space-y-1.5">
              <li><span>HIPAA Security Rule Compliant</span></li>
              <li><span>HITECH Local Data Safeguards</span></li>
              <li><span>GDPR Zero-Cloud Transmission</span></li>
              <li><span>MIT Open Source License</span></li>
            </ul>
          </div>

        </div>

        <div className="pt-8 border-t flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px]">
          <div>
            &copy; {new Date().getFullYear()} EdgeShield AI. Intelligent Healthcare Cybersecurity Platform.
          </div>
          <div className="flex items-center space-x-1">
            <span>Built for Smart Hospital Protection</span>
          </div>
        </div>

      </div>
    </footer>
  );
};
