import React, { useState, useEffect } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { LandingPage } from './components/landing/LandingPage';
import { Navbar } from './components/layout/Navbar';
import { Sidebar, TabType } from './components/layout/Sidebar';
import { OverviewDashboard } from './components/dashboard/OverviewDashboard';
import { AlertCenter } from './components/alerts/AlertCenter';
import { AlertExplainerModal } from './components/alerts/AlertExplainerModal';
import { DeviceManager } from './components/devices/DeviceManager';
import { AnalyticsView } from './components/analytics/AnalyticsView';
import { AttackSimulator } from './components/simulator/AttackSimulator';
import { DocumentReader } from './components/docs/DocumentReader';
import { AICopilotDrawer } from './components/copilot/AICopilotDrawer';
import { SecurityActionModal } from './components/modals/SecurityActionModal';
import { GlobalSearchModal } from './components/search/GlobalSearchModal';
import { MachineSignalsView } from './components/signals/MachineSignalsView';

import { apiService } from './services/api';
import { useWebSocket } from './hooks/useWebSocket';
import { DashboardStats, Device, Alert, MLMetrics, CopilotContextType } from './types';

export const AppContent: React.FC = () => {
  const [viewMode, setViewMode] = useState<'landing' | 'dashboard'>('landing');
  const [activeTab, setActiveTab] = useState<TabType>('dashboard');
  
  const [stats, setStats] = useState<DashboardStats>({
    total_devices: 18,
    active_alerts: 2,
    critical_alerts: 1,
    devices_at_risk: 2,
    threat_distribution: {
      'DICOM Ransomware': 1,
      'MQTT Flood DoS': 1,
    },
    system_health: 'ELEVATED_THREAT',
    edge_ai_status: 'ONLINE (Sub-millisecond Detection)',
  });


  const [devices, setDevices] = useState<Device[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [metrics, setMetrics] = useState<MLMetrics>({
    features: [
      'packet_length', 'flow_duration', 'header_length', 'byte_rate',
      'packet_rate', 'tcp_syn_flag', 'mqtt_msg_rate', 'modbus_fn_code', 'entropy'
    ],
    labels: [
      'Normal', 'DICOM Ransomware', 'MQTT Flood DoS',
      'Modbus Command Injection', 'ARP Spoofing MITM', 'Port Scan Reconnaissance'
    ],
    metrics: {
      macro_precision: 0.9924,
      macro_recall: 0.9891,
      macro_f1: 0.9907
    }
  });

  // Selected state & context persistence
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);
  const [selectedDocId, setSelectedDocId] = useState<string>('DOC-IEEE-EDGESHIELD-2026');
  const [selectedDocPage, setSelectedDocPage] = useState<number>(1);
  const [activeContext, setActiveContext] = useState<CopilotContextType>('telemetry');

  // Modals & Drawers state
  const [isCopilotOpen, setIsCopilotOpen] = useState<boolean>(false);
  const [isSearchOpen, setIsSearchOpen] = useState<boolean>(false);
  const [securityActionDevice, setSecurityActionDevice] = useState<Device | null>(null);
  const [securityActionType, setSecurityActionType] = useState<'isolate' | 'reconnect'>('isolate');

  // Subscribe to live WebSocket telemetry stream
  const { lastEvent, isConnected } = useWebSocket('/ws/telemetry');

  // Load initial data from FastAPI backend
  const loadData = async () => {
    try {
      const [statsData, devicesData, alertsData, metricsData] = await Promise.all([
        apiService.getDashboardStats(),
        apiService.getDevices(),
        apiService.getAlerts(),
        apiService.getMLMetrics(),
      ]);

      setStats(statsData);
      setDevices(devicesData);
      setAlerts(alertsData);
      setMetrics(metricsData);
    } catch (e) {
      console.error('Data load error', e);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 8000);
    return () => clearInterval(interval);
  }, []);

  // Update when real-time WebSocket anomaly packet arrives
  useEffect(() => {
    if (lastEvent && (lastEvent.detection?.is_anomaly || lastEvent.event_type === 'alert_created' || lastEvent.event_type === 'alert_updated')) {
      loadData();
    }
  }, [lastEvent]);


  // Sync activeContext with activeTab
  useEffect(() => {
    if (activeTab === 'docs') setActiveContext('research');
    else if (activeTab === 'alerts') setActiveContext('incident');
    else if (activeTab === 'devices') setActiveContext('device');
    else if (activeTab === 'simulator' || activeTab === 'analytics') setActiveContext('architecture');
    else setActiveContext('telemetry');
  }, [activeTab]);

  // Global Keyboard Shortcut: Cmd+K / Ctrl+K for Global Search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsSearchOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleUpdateStatus = async (alertId: string, status: string) => {
    try {
      await apiService.updateAlertStatus(alertId, status);
      loadData();
    } catch (e) {
      setAlerts(prev =>
        prev.map(a => (a.alert_id === alertId ? { ...a, status: status as any } : a))
      );
    }
  };

  // Handle Global Search Selection
  const handleSelectSearchResult = (type: string, payload: any) => {
    if (type === 'alert' && payload) {
      setSelectedAlert(payload);
      setActiveTab('alerts');
      setActiveContext('incident');
    } else if (type === 'device' && payload) {
      setSelectedDevice(payload);
      setActiveTab('devices');
      setActiveContext('device');
    } else if (type === 'research') {
      if (payload?.docId) setSelectedDocId(payload.docId);
      if (payload?.page) setSelectedDocPage(payload.page);
      setActiveTab('docs');
      setActiveContext('research');
    } else if (type === 'simulator') {
      setActiveTab('simulator');
      setActiveContext('architecture');
    } else if (type === 'analytics') {
      setActiveTab('analytics');
      setActiveContext('architecture');
    }
  };

  // If in Landing Page mode, render LandingPage component
  if (viewMode === 'landing') {
    return <LandingPage onLaunchDashboard={() => setViewMode('dashboard')} />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground animate-in fade-in">
      {/* Top Navigation Navbar */}
      <Navbar
        isConnected={isConnected}
        activeAlertsCount={stats.active_alerts}
        onNavigateHome={() => setViewMode('landing')}
        onOpenSearch={() => setIsSearchOpen(true)}
        onToggleCopilot={() => setIsCopilotOpen(prev => !prev)}
        isCopilotOpen={isCopilotOpen}
        activeContext={activeContext}
      />

      {/* Main Layout Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          activeAlertsCount={stats.active_alerts}
        />

        {/* Dynamic Page Workspace */}
        <main className="flex-1 p-6 md:p-8 overflow-y-auto max-w-7xl mx-auto w-full">
          {activeTab === 'dashboard' && (
            <OverviewDashboard
              stats={stats}
              alerts={alerts}
              lastTelemetryEvent={lastEvent}
              onSelectAlert={(alert) => {
                setSelectedAlert(alert);
                setActiveContext('incident');
              }}
              onSimulateAttack={() => setActiveTab('simulator')}
            />
          )}

          {activeTab === 'signals' && (
            <MachineSignalsView />
          )}


          {activeTab === 'alerts' && (
            <AlertCenter
              alerts={alerts}
              onSelectAlert={(alert) => {
                setSelectedAlert(alert);
                setActiveContext('incident');
              }}
              onUpdateStatus={handleUpdateStatus}
              onInvestigateCopilot={(alert) => {
                setSelectedAlert(alert);
                setActiveContext('incident');
                setIsCopilotOpen(true);
              }}
            />
          )}

          {activeTab === 'devices' && (
            <DeviceManager
              devices={devices}
              onRequestAction={(device, action) => {
                setSecurityActionDevice(device);
                setSecurityActionType(action);
              }}
              onAskCopilot={(device) => {
                setSelectedDevice(device);
                setActiveContext('device');
                setIsCopilotOpen(true);
              }}
            />
          )}

          {activeTab === 'analytics' && <AnalyticsView metrics={metrics} />}

          {activeTab === 'simulator' && (
            <AttackSimulator
              onAlertGenerated={(alert) => {
                setAlerts((prev) => [alert, ...prev]);
                setSelectedAlert(alert);
                setActiveContext('incident');
              }}
            />
          )}

          {activeTab === 'docs' && (
            <DocumentReader
              initialDocId={selectedDocId}
              initialPage={selectedDocPage}
              onAskCopilot={(docId, pageNum) => {
                setSelectedDocId(docId);
                setSelectedDocPage(pageNum);
                setActiveContext('research');
                setIsCopilotOpen(true);
              }}
              onNavigateTab={(tab) => {
                setActiveTab(tab as TabType);
              }}
            />
          )}
        </main>
      </div>

      {/* Deep-Dive AI Explainer Modal */}
      <AlertExplainerModal
        alert={selectedAlert}
        onClose={() => setSelectedAlert(null)}
        onUpdateStatus={handleUpdateStatus}
      />

      {/* Unified Ambient AI Copilot Drawer */}
      <AICopilotDrawer
        isOpen={isCopilotOpen}
        onClose={() => setIsCopilotOpen(false)}
        activeContext={activeContext}
        selectedAlert={selectedAlert}
        selectedDevice={selectedDevice}
        selectedDocId={selectedDocId}
        selectedDocPage={selectedDocPage}
        onNavigateToDocumentPage={(docId, pageNum) => {
          setSelectedDocId(docId);
          setSelectedDocPage(pageNum);
          setActiveTab('docs');
          setActiveContext('research');
        }}
      />

      {/* Security Action Confirmation Workflow Modal */}
      <SecurityActionModal
        device={securityActionDevice}
        action={securityActionType}
        onClose={() => setSecurityActionDevice(null)}
        onSuccess={(updatedDevice) => {
          setDevices(prev => prev.map(d => d.device_id === updatedDevice.device_id ? updatedDevice : d));
        }}
      />

      {/* Global Search Palette Modal (Ctrl+K) */}
      <GlobalSearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        alerts={alerts}
        devices={devices}
        onSelectResult={handleSelectSearchResult}
      />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
};

export default App;
