import React, { useState, useEffect } from 'react';
import { ShieldCheck, ArrowRight, Sun, Moon, Sparkles } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

interface LandingNavbarProps {
  onLaunchDashboard: () => void;
}

export const LandingNavbar: React.FC<LandingNavbarProps> = ({ onLaunchDashboard }) => {
  const { theme, toggleTheme } = useTheme();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-card/80 backdrop-blur-xl border-b shadow-lg py-3'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        {/* Brand */}
        <div
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          className="flex items-center space-x-3 cursor-pointer group"
        >
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-medical-teal via-teal-500 to-cyan-400 flex items-center justify-center shadow-glow-teal text-white group-hover:scale-105 transition-transform">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-lg tracking-tight text-foreground">EdgeShield AI</span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-medical-teal/10 text-medical-teal border border-medical-teal/20">
                Healthcare Edge IDS
              </span>
            </div>
            <p className="text-[11px] text-muted-foreground hidden sm:block">
              Intelligent Edge-Based Intrusion Detection
            </p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center space-x-8 text-xs font-semibold text-muted-foreground">
          <button
            onClick={() => scrollToSection('why-edgeshield')}
            className="hover:text-foreground transition-colors"
          >
            Why EdgeShield
          </button>
          <button
            onClick={() => scrollToSection('how-it-works')}
            className="hover:text-foreground transition-colors"
          >
            How It Works
          </button>
          <button
            onClick={() => scrollToSection('architecture')}
            className="hover:text-foreground transition-colors"
          >
            Architecture
          </button>
          <button
            onClick={() => scrollToSection('attack-sandbox')}
            className="hover:text-foreground transition-colors"
          >
            Live Sandbox
          </button>
          <button
            onClick={() => scrollToSection('research')}
            className="hover:text-foreground transition-colors"
          >
            IEEE Research
          </button>
          <button
            onClick={() => scrollToSection('tech-stack')}
            className="hover:text-foreground transition-colors"
          >
            Tech Stack
          </button>
        </nav>

        {/* Action Controls */}
        <div className="flex items-center space-x-4">
          <button
            onClick={toggleTheme}
            className="p-2.5 rounded-xl border bg-secondary/80 hover:bg-secondary transition-colors text-muted-foreground hover:text-foreground"
            title="Toggle Dark/Light Theme"
          >
            {theme === 'dark' ? <Sun className="h-4 w-4 text-amber-400" /> : <Moon className="h-4 w-4 text-slate-700" />}
          </button>

          <button
            onClick={onLaunchDashboard}
            className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-medical-teal to-teal-500 hover:from-teal-600 hover:to-medical-teal text-white font-bold text-xs shadow-glow-teal hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            <Sparkles className="h-4 w-4" />
            <span>Launch Security Cockpit</span>
            <ArrowRight className="h-4 w-4 ml-0.5" />
          </button>
        </div>
      </div>
    </header>
  );
};
