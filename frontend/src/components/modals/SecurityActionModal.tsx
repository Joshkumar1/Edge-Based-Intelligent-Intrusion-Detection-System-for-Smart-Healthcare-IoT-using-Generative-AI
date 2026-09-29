import React, { useState } from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle2, Loader2, X } from 'lucide-react';
import { Device } from '../../types';
import { apiService } from '../../services/api';

interface SecurityActionModalProps {
  device: Device | null;
  action: 'isolate' | 'reconnect';
  onClose: () => void;
  onSuccess: (updatedDevice: Device) => void;
}

export const SecurityActionModal: React.FC<SecurityActionModalProps> = ({
  device,
  action,
  onClose,
  onSuccess,
}) => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (!device) return null;

  const isIsolate = action === 'isolate';

  const handleConfirm = async () => {
    setIsExecuting(true);
    setErrorMessage(null);
    try {
      let updated: Device;
      if (isIsolate) {
        updated = await apiService.isolateDevice(device.device_id);
      } else {
        updated = await apiService.reconnectDevice(device.device_id);
      }
      onSuccess(updated);
      onClose();
    } catch (e: any) {
      setErrorMessage(e.message || 'Security action failed to execute on the edge gateway.');
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-card border rounded-3xl p-6 max-w-lg w-full shadow-2xl space-y-5 animate-in zoom-in-95">
        {/* Header */}
        <div className="flex items-center justify-between border-b pb-3">
          <div className="flex items-center space-x-2 text-rose-500 font-bold text-sm">
            <ShieldAlert className="h-5 w-5" />
            <span>Security Action Confirmation</span>
          </div>
          <button
            onClick={onClose}
            className="text-muted-foreground hover:text-foreground text-sm font-bold"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Action Details Card */}
        <div className="p-4 rounded-2xl bg-secondary/50 border space-y-2.5 text-xs">
          <div className="flex justify-between">
            <span className="text-muted-foreground">Target Device:</span>
            <span className="font-bold font-mono text-foreground">{device.name} ({device.device_id})</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">Category / Location:</span>
            <span className="font-medium text-foreground">{device.category} • {device.location}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">Action:</span>
            <span className="font-bold font-mono text-rose-500">
              {isIsolate ? 'Network Switch Port Isolation / VLAN Quarantine' : 'Restore Network Connectivity'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">Target IP Address:</span>
            <span className="font-mono text-foreground">{device.ip_address}</span>
          </div>
        </div>

        {/* Clinical Impact Warning */}
        <div className={`p-4 rounded-2xl border text-xs space-y-1.5 ${
          isIsolate
            ? 'bg-rose-500/10 border-rose-500/30 text-rose-600 dark:text-rose-400'
            : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-600 dark:text-emerald-400'
        }`}>
          <div className="flex items-center space-x-1.5 font-bold">
            <AlertTriangle className="h-4 w-4" />
            <span>Clinical Impact Assessment</span>
          </div>
          <p className="text-[11px] leading-relaxed text-muted-foreground">
            {isIsolate
              ? 'Warning: Isolating this device will sever all IP packets across hospital VLAN switches. Patient vital sign telemetry and infusion rate updates will be cut off from the central nursing station. Ensure bedside clinical alarms are actively monitored.'
              : 'Restoring connectivity will re-enable all inbound and outbound IP traffic over the hospital IoT network. Verify that malware has been neutralized before reconnecting.'}
          </p>
        </div>

        {/* Error message if execution fails */}
        {errorMessage && (
          <div className="p-3 rounded-xl bg-rose-500/20 border border-rose-500/40 text-xs text-rose-500">
            {errorMessage}
          </div>
        )}

        {/* Confirmation Actions */}
        <div className="flex items-center justify-end space-x-3 pt-2">
          <button
            type="button"
            onClick={onClose}
            disabled={isExecuting}
            className="px-4 py-2 rounded-xl border text-xs font-semibold hover:bg-secondary transition-all"
          >
            Cancel
          </button>

          <button
            type="button"
            onClick={handleConfirm}
            disabled={isExecuting}
            className={`px-4 py-2 rounded-xl text-xs font-bold text-white flex items-center space-x-2 transition-all ${
              isIsolate
                ? 'bg-rose-600 hover:bg-rose-700 shadow-glow-rose'
                : 'bg-emerald-600 hover:bg-emerald-700'
            } disabled:opacity-50`}
          >
            {isExecuting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Executing Enforcement...</span>
              </>
            ) : (
              <>
                <CheckCircle2 className="h-4 w-4" />
                <span>{isIsolate ? 'Confirm Device Isolation' : 'Confirm Reconnection'}</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
