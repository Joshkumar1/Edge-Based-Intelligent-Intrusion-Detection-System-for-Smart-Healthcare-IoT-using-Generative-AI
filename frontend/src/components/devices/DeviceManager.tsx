import React, { useState } from 'react';
import { Monitor, ShieldCheck, AlertTriangle, Wifi, HardDrive, MapPin, Activity } from 'lucide-react';
import { Device } from '../../types';

interface DeviceManagerProps {
  devices: Device[];
}

export const DeviceManager: React.FC<DeviceManagerProps> = ({ devices }) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');

  const filteredDevices = devices.filter(
    (dev) => selectedCategory === 'ALL' || dev.category === selectedCategory
  );

  const categories = Array.from(new Set(devices.map((d) => d.category)));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Smart Hospital Device Inventory</h2>
          <p className="text-sm text-muted-foreground">
            Monitor medical IoT device risk scores, VLAN locations, protocols, and edge gateway connectivity.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-semibold px-3 py-1.5 rounded-xl bg-secondary border">
          <Monitor className="h-4 w-4 text-medical-teal" />
          <span>{devices.length} Total Registered Nodes</span>
        </div>
      </div>

      {/* Category Filter Tabs */}
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

      {/* Device Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredDevices.map((device) => {
          const isHighRisk = device.risk_score > 50;
          return (
            <div
              key={device.device_id}
              className="p-5 rounded-2xl bg-card border shadow-subtle flex flex-col justify-between space-y-4 hover:border-medical-teal/40 transition-all"
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div
                      className={`p-2.5 rounded-xl text-white font-bold ${
                        isHighRisk ? 'bg-rose-500 shadow-glow-red' : 'bg-medical-teal'
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
              <div className="space-y-1 border-t pt-3">
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
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
