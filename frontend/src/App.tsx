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
import { ResearchDocsView } from './components/docs/ResearchDocsView';
import { apiService } from './services/api';
import { useWebSocket } from './hooks/useWebSocket';
import { DashboardStats, Device, Alert, MLMetrics } from './types';

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
    edge_ai_status: 'ONLINE (0.84ms Latency)',
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

  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);

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
    const interval = setInterval(loadData, 8000); // Polling sync
    return () => clearInterval(interval);
  }, []);

  // Update when real-time WebSocket anomaly packet arrives
  useEffect(() => {
    if (lastEvent && lastEvent.detection.is_anomaly) {
      loadData();
    }
  }, [lastEvent]);

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

  // If in Landing Page mode, render LandingPage component
  if (viewMode === 'landing') {
    return <LandingPage onLaunchDashboard={() => setViewMode('dashboard')} />;
  }

  // Dashboard Security Cockpit Mode
  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground animate-in fade-in">
      {/* Top Navigation Navbar */}
      <Navbar
        isConnected={isConnected}
        activeAlertsCount={stats.active_alerts}
        onNavigateHome={() => setViewMode('landing')}
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
              onSelectAlert={(alert) => setSelectedAlert(alert)}
              onSimulateAttack={() => setActiveTab('simulator')}
            />
          )}

          {activeTab === 'alerts' && (
            <AlertCenter
              alerts={alerts}
              onSelectAlert={(alert) => setSelectedAlert(alert)}
              onUpdateStatus={handleUpdateStatus}
            />
          )}

          {activeTab === 'devices' && <DeviceManager devices={devices} />}

          {activeTab === 'analytics' && <AnalyticsView metrics={metrics} />}

          {activeTab === 'simulator' && (
            <AttackSimulator
              onAlertGenerated={(alert) => {
                setAlerts((prev) => [alert, ...prev]);
                setSelectedAlert(alert);
              }}
            />
          )}

          {activeTab === 'docs' && <ResearchDocsView />}
        </main>
      </div>

      {/* Deep-Dive AI Explainer Modal */}
      <AlertExplainerModal
        alert={selectedAlert}
        onClose={() => setSelectedAlert(null)}
        onUpdateStatus={handleUpdateStatus}
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
