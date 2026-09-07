import React from 'react';
import { LayoutDashboard, AlertTriangle, Monitor, BarChart3, Zap, ShieldAlert, FileText, Settings } from 'lucide-react';

export type TabType = 'dashboard' | 'alerts' | 'devices' | 'analytics' | 'simulator' | 'docs';

interface SidebarProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  activeAlertsCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, activeAlertsCount }) => {
  const navItems = [
    { id: 'dashboard', label: 'Overview Dashboard', icon: LayoutDashboard },
    { id: 'alerts', label: 'Alert Center', icon: AlertTriangle, badge: activeAlertsCount },
    { id: 'devices', label: 'Device Inventory', icon: Monitor },
    { id: 'analytics', label: 'ML Analytics', icon: BarChart3 },
    { id: 'simulator', label: 'Attack Simulator', icon: Zap },
    { id: 'docs', label: 'IEEE Research Docs', icon: FileText },
  ];

  return (
    <aside className="w-64 border-r bg-card/60 backdrop-blur-md flex flex-col justify-between p-4 transition-colors">
      <div className="space-y-1">
        <div className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
          Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id as TabType)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? 'bg-medical-teal text-white shadow-glow-teal font-semibold'
                  : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`h-4 w-4 ${isActive ? 'text-white' : 'text-muted-foreground'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge !== undefined && item.badge > 0 && (
                <span
                  className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                    isActive ? 'bg-white text-medical-teal' : 'bg-rose-500 text-white'
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Edge System Specs Widget */}
      <div className="p-3 rounded-xl bg-secondary/80 border text-xs space-y-2">
        <div className="flex items-center space-x-2 font-semibold text-foreground">
          <ShieldAlert className="h-4 w-4 text-medical-teal" />
          <span>Edge Node Status</span>
        </div>
        <div className="text-[11px] text-muted-foreground space-y-1">
          <div className="flex justify-between">
            <span>Edge Gateway:</span>
            <span className="font-mono text-foreground">NVIDIA Jetson / x86</span>
          </div>
          <div className="flex justify-between">
            <span>Inference Latency:</span>
            <span className="font-mono text-emerald-500 font-bold">&lt; 1.2ms</span>
          </div>
          <div className="flex justify-between">
            <span>Local SLM:</span>
            <span className="font-mono text-foreground">Llama 3 8B</span>
          </div>
        </div>
      </div>
    </aside>
  );
};
