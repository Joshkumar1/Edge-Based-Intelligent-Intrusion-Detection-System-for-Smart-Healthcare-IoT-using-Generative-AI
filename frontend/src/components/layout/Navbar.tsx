import React from 'react';
import { ShieldCheck, Cpu, Sun, Moon, Radio, Activity } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

interface NavbarProps {
  isConnected: boolean;
  activeAlertsCount: number;
  onNavigateHome?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ isConnected, activeAlertsCount, onNavigateHome }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-30 h-16 border-b bg-card/80 backdrop-blur-md px-6 flex items-center justify-between transition-colors">
      {/* Brand & Subtitle */}
      <div 
        onClick={onNavigateHome}
        className="flex items-center space-x-3 cursor-pointer group"
      >
        <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-medical-teal to-teal-400 flex items-center justify-center shadow-glow-teal text-white group-hover:scale-105 transition-transform">
          <ShieldCheck className="h-6 w-6" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="font-bold text-lg tracking-tight">EdgeShield AI</h1>
            <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full bg-medical-teal/10 text-medical-teal font-semibold border border-medical-teal/20">
              Healthcare Edge IDS
            </span>
          </div>
          <p className="text-xs text-muted-foreground hidden sm:block">
            Intelligent Edge-Based Intrusion Detection for Smart Hospitals
          </p>
        </div>
      </div>

      {/* Status Badges & Controls */}
      <div className="flex items-center space-x-4">
        {/* Edge AI Engine Status */}
        <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-secondary text-xs font-medium border">
          <Cpu className="h-4 w-4 text-medical-teal" />
          <span>Local Ollama SLM:</span>
          <span className="text-emerald-500 font-semibold">Active</span>
        </div>

        {/* WebSocket Stream Status */}
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-secondary text-xs font-medium border">
          <Radio className={`h-4 w-4 ${isConnected ? 'text-emerald-500 animate-pulse' : 'text-amber-500'}`} />
          <span className="hidden sm:inline">Telemetry Stream:</span>
          <span className={isConnected ? 'text-emerald-500 font-semibold' : 'text-amber-500 font-semibold'}>
            {isConnected ? 'LIVE (1.5s)' : 'Connecting...'}
          </span>
        </div>

        {/* Active Alert Badge */}
        {activeAlertsCount > 0 && (
          <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-rose-500/10 text-rose-500 border border-rose-500/20 text-xs font-semibold animate-pulse">
            <Activity className="h-4 w-4" />
            <span>{activeAlertsCount} Active Incidents</span>
          </div>
        )}

        {/* Dark/Light Mode Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2.5 rounded-xl border bg-secondary/80 hover:bg-secondary transition-colors text-muted-foreground hover:text-foreground"
          title="Toggle Dark/Light Mode"
        >
          {theme === 'dark' ? <Sun className="h-4 w-4 text-amber-400" /> : <Moon className="h-4 w-4 text-slate-700" />}
        </button>

        {/* User Profile */}
        <div className="flex items-center space-x-2 pl-2 border-l">
          <div className="h-8 w-8 rounded-full bg-medical-navy text-white font-bold text-xs flex items-center justify-center">
            HA
          </div>
          <div className="hidden lg:block text-xs">
            <div className="font-semibold">Hospital Admin</div>
            <div className="text-[10px] text-muted-foreground">Biomedical Security</div>
          </div>
        </div>
      </div>
    </header>
  );
};
