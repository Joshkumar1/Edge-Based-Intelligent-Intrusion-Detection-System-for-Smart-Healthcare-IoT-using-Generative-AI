import React from 'react';
import { ShieldCheck, Cpu, Sun, Moon, Radio, Activity, Search, Sparkles } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

interface NavbarProps {
  isConnected: boolean;
  activeAlertsCount: number;
  onNavigateHome?: () => void;
  onOpenSearch?: () => void;
  onToggleCopilot?: () => void;
  isCopilotOpen?: boolean;
  activeContext?: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  isConnected,
  activeAlertsCount,
  onNavigateHome,
  onOpenSearch,
  onToggleCopilot,
  isCopilotOpen,
  activeContext = 'research'
}) => {
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

      {/* Global Search Bar (Trigger) */}
      {onOpenSearch && (
        <button
          onClick={onOpenSearch}
          className="hidden md:flex items-center space-x-2 bg-secondary/80 hover:bg-secondary border text-muted-foreground hover:text-foreground px-3.5 py-1.5 rounded-xl text-xs font-medium transition-all max-w-sm w-72 justify-between"
        >
          <div className="flex items-center space-x-2 truncate">
            <Search className="h-3.5 w-3.5 text-medical-teal" />
            <span className="truncate">Search incidents, devices, research...</span>
          </div>
          <kbd className="text-[10px] font-mono bg-card px-1.5 py-0.5 rounded border text-muted-foreground">
            ⌘K
          </kbd>
        </button>
      )}

      {/* Status Badges & Controls */}
      <div className="flex items-center space-x-3">
        {/* AI Copilot Toggle Button */}
        {onToggleCopilot && (
          <button
            onClick={onToggleCopilot}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
              isCopilotOpen
                ? 'bg-medical-teal text-white shadow-glow-teal border-medical-teal'
                : 'bg-secondary/80 hover:bg-secondary text-foreground hover:border-medical-teal/50'
            }`}
          >
            <Sparkles className={`h-3.5 w-3.5 ${isCopilotOpen ? 'text-white' : 'text-medical-teal'}`} />
            <span className="hidden sm:inline">AI Copilot</span>
            <span className={`text-[9px] uppercase px-1.5 py-0.2 rounded font-mono ${
              isCopilotOpen ? 'bg-white/20 text-white' : 'bg-medical-teal/15 text-medical-teal'
            }`}>
              {activeContext}
            </span>
          </button>
        )}

        {/* Telemetry Status */}
        <div className="hidden lg:flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-secondary text-xs font-medium border">
          <Radio className={`h-3.5 w-3.5 ${isConnected ? 'text-emerald-500 animate-pulse' : 'text-amber-500'}`} />
          <span className="hidden sm:inline">Telemetry:</span>
          <span className={isConnected ? 'text-emerald-500 font-semibold font-mono' : 'text-amber-500 font-semibold font-mono'}>
            {isConnected ? 'LIVE' : 'Connecting'}
          </span>
        </div>

        {/* Active Alert Badge */}
        {activeAlertsCount > 0 && (
          <div className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-xl bg-rose-500/10 text-rose-500 border border-rose-500/20 text-xs font-semibold animate-pulse">
            <Activity className="h-3.5 w-3.5" />
            <span>{activeAlertsCount} Alerts</span>
          </div>
        )}

        {/* Dark/Light Mode Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-xl border bg-secondary/80 hover:bg-secondary transition-colors text-muted-foreground hover:text-foreground"
          title="Toggle Dark/Light Mode"
        >
          {theme === 'dark' ? <Sun className="h-4 w-4 text-amber-400" /> : <Moon className="h-4 w-4 text-slate-700" />}
        </button>

        {/* User Profile */}
        <div className="hidden xl:flex items-center space-x-2 pl-2 border-l">
          <div className="h-8 w-8 rounded-full bg-medical-teal/20 text-medical-teal font-bold text-xs flex items-center justify-center border border-medical-teal/40">
            ES
          </div>
          <div className="text-xs">
            <div className="font-semibold">Security Officer</div>
            <div className="text-[10px] text-muted-foreground">Smart ICU Ward</div>
          </div>
        </div>
      </div>
    </header>
  );
};
