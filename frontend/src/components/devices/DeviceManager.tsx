import React, { useState } from 'react';
import { Monitor, ShieldAlert, Wifi, HardDrive, MapPin, Sparkles, ShieldOff, CheckCircle2 } from 'lucide-react';
import { Device } from '../../types';

interface DeviceManagerProps {
  devices: Device[];
  onRequestAction?: (device: Device, action: 'isolate' | 'reconnect') => void;
  onAskCopilot?: (device: Device) => void;
}

export const DeviceManager: React.FC<DeviceManagerProps> = ({
  devices,
  onRequestAction,
  onAskCopilot
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');

  const filteredDevices = devices.filter(
    (dev) => selectedCategory === 'ALL' || dev.category === selectedCategory
  );

  const categories = Array.from(new Set(devices.map((d) => d.category)));

  return (
    <div className="space-y-6 animate-in fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Smart Hospital Device Inventory</h2>
          <p className="text-sm text-muted-foreground">
            Monitor medical IoT device risk scores, VLAN locations, protocols, and execute edge switch quarantine.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-semibold px-3 py-1.5 rounded-xl bg-secondary border">
          <Monitor className="h-4 w-4 text-medical-teal" />
          <span>{devices.length} Total Registered Nodes</span>
        </div>
      </div>

      {/* Empty State */}
      {devices.length === 0 && (
        <div className="p-12 rounded-2xl bg-card border text-center space-y-3">
          <Monitor className="h-10 w-10 text-muted-foreground mx-auto" />
          <div className="text-base font-bold">No hospital assets have been registered.</div>
          <p className="text-xs text-muted-foreground">
            Connect an edge gateway probe or register devices in the hospital inventory database.
          </p>
        </div>
      )}

      {/* Category Filter Tabs */}
      {devices.length > 0 && (
        <div className="flex items-center space-x-2 overflow-x-auto pb-2">
          <button
            onClick={() => setSelectedCategory('ALL')}
            className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
              selectedCategory === 'ALL'
                ? 'bg-medical-teal text-white shadow-glow-teal'
                : 'bg-card border text-muted-foreground hover:text-foreground'
            }`}
          >
            All Device Categories ({devices.length})
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                selectedCategory === cat
                  ? 'bg-medical-teal text-white shadow-glow-teal'
                  : 'bg-card border text-muted-foreground hover:text-foreground'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      )}

      {/* Device Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredDevices.map((device) => {
          const isHighRisk = device.risk_score > 50;
          const isIsolated = device.status === 'Isolated';

          return (
            <div
              key={device.device_id}
              className={`p-5 rounded-2xl bg-card border shadow-subtle flex flex-col justify-between space-y-4 transition-all ${
                isIsolated
                  ? 'border-rose-500/50 bg-rose-500/[0.03]'
                  : 'hover:border-medical-teal/40'
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div
                      className={`p-2.5 rounded-xl text-white font-bold ${
                        isIsolated
                          ? 'bg-slate-700'
                          : isHighRisk
                          ? 'bg-rose-500 shadow-glow-red'
                          : 'bg-medical-teal'
                      }`}
                    >
                      <Monitor className="h-5 w-5" />
                    </div>
                    <div>
                      <h4 className="font-bold text-sm text-foreground">{device.name}</h4>
                      <div className="text-[10px] font-mono text-muted-foreground">{device.device_id}</div>
                    </div>
                  </div>

                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      device.status === 'Active'
                        ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20'
                        : device.status === 'Critical'
                        ? 'bg-rose-500/10 text-rose-500 border border-rose-500/20'
                        : device.status === 'Isolated'
                        ? 'bg-slate-500/20 text-slate-400 border border-slate-500/30'
                        : 'bg-amber-500/10 text-amber-500 border border-amber-500/20'
                    }`}
                  >
                    {device.status}
                  </span>
                </div>

                <div className="space-y-1.5 text-xs text-muted-foreground border-t pt-3">
                  <div className="flex justify-between items-center">
                    <span className="flex items-center space-x-1.5">
                      <MapPin className="h-3.5 w-3.5 text-medical-teal" />
                      <span>Location:</span>
                    </span>
                    <span className="font-medium text-foreground">{device.location}</span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="flex items-center space-x-1.5">
                      <Wifi className="h-3.5 w-3.5 text-medical-teal" />
                      <span>IP / Protocol:</span>
                    </span>
                    <span className="font-mono text-foreground">
                      {device.ip_address} ({device.protocol})
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="flex items-center space-x-1.5">
                      <HardDrive className="h-3.5 w-3.5 text-medical-teal" />
                      <span>Firmware:</span>
                    </span>
                    <span className="font-mono text-foreground">{device.firmware_version}</span>
                  </div>
                </div>
              </div>

              {/* Risk Gauge Bar */}
              <div className="space-y-2 border-t pt-3">
                <div className="flex justify-between text-[11px]">
                  <span className="text-muted-foreground font-medium">Risk Score:</span>
                  <span className={`font-bold ${isHighRisk ? 'text-rose-500' : 'text-emerald-500'}`}>
                    {device.risk_score} / 100
                  </span>
                </div>
                <div className="h-2 w-full rounded-full bg-secondary overflow-hidden">
                  <div
                    className={`h-full transition-all duration-500 ${
                      isHighRisk ? 'bg-rose-500' : 'bg-emerald-500'
                    }`}
                    style={{ width: `${Math.min(100, device.risk_score)}%` }}
                  />
                </div>

                {/* Actions: Isolate & Ask Copilot */}
                <div className="flex items-center space-x-2 pt-2">
                  {onRequestAction && (
                    <button
                      onClick={() => onRequestAction(device, isIsolated ? 'reconnect' : 'isolate')}
                      className={`flex-1 py-1.5 px-2.5 rounded-xl text-[11px] font-bold flex items-center justify-center space-x-1.5 border transition-all ${
                        isIsolated
                          ? 'bg-emerald-500/15 border-emerald-500/30 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/25'
                          : 'bg-rose-500/10 border-rose-500/30 text-rose-600 dark:text-rose-400 hover:bg-rose-500/20'
                      }`}
                    >
                      {isIsolated ? (
                        <>
                          <CheckCircle2 className="h-3 w-3" />
                          <span>Reconnect</span>
                        </>
                      ) : (
                        <>
                          <ShieldOff className="h-3 w-3" />
                          <span>Isolate Device</span>
                        </>
                      )}
                    </button>
                  )}

                  {onAskCopilot && (
                    <button
                      onClick={() => onAskCopilot(device)}
                      className="p-1.5 rounded-xl border bg-secondary hover:bg-secondary/80 text-medical-teal transition-all"
                      title="Ask AI Copilot about this device"
                    >
                      <Sparkles className="h-4 w-4" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
