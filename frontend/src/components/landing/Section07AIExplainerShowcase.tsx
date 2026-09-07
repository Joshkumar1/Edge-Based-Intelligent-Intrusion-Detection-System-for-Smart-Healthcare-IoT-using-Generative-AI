import React from 'react';
import { Sparkles, Terminal, FileText, CheckCircle2, ShieldAlert } from 'lucide-react';

export const Section07AIExplainerShowcase: React.FC = () => {
  return (
    <section className="py-24 border-b bg-card/30 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-medical-teal/10 border border-medical-teal/20 text-medical-teal text-xs font-semibold">
            <Sparkles className="h-4 w-4" />
            <span>Generative AI Security Showcase</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
            Like Having a Senior SOC Engineer Working 24/7 Inside Your Hospital
          </h2>
          <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
            Raw security logs are overwhelming. EdgeShield AI synthesizes raw network features into plain-language clinical insights instantly.
          </p>
        </div>

        {/* Split Showcase Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
          
          {/* Left Side: Raw Network Logs (Before EdgeShield) */}
          <div className="p-6 rounded-3xl bg-slate-950 border border-slate-800 space-y-4 font-mono text-xs text-slate-300">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2 text-rose-400">
                <Terminal className="h-4 w-4" />
                <span>RAW_NETWORK_INTRUSION_LOG.pcap</span>
              </div>
              <span className="text-[10px] bg-rose-500/20 text-rose-400 px-2 py-0.5 rounded">CRYPTIC LOG</span>
            </div>

            <div className="space-y-2 text-[11px] leading-relaxed text-slate-400 overflow-x-auto">
              <div>[2026-08-01 11:04:12] SRC=172.16.8.204 DST=192.168.10.104 PROTO=DICOM PORT=104</div>
              <div>LEN=1450 FLOW_DUR=25.4 HEADER_LEN=40 BYTE_RATE=28500.0 PKT_RATE=85.0</div>
              <div>TCP_SYN=0 MQTT_MSG_RATE=0.0 MODBUS_FN_CODE=0 PAYLOAD_ENTROPY=7.8821</div>
              <div className="text-rose-400">
                [ALERT_TRIGGER] ISOLATION_FOREST_SCORE=-0.8421 XGBOOST_CLASS=1 (DICOM_RANSOMWARE)
              </div>
              <div className="text-slate-500">
                &gt;&gt; Error: Raw telemetry unreadable for non-security staff. No mitigation playbook attached.
              </div>
            </div>
          </div>

          {/* Right Side: EdgeShield AI Explanation (After EdgeShield) */}
          <div className="p-6 rounded-3xl bg-card border border-medical-teal/40 shadow-glow-teal space-y-4">
            <div className="flex items-center justify-between border-b pb-3 text-xs">
              <div className="flex items-center space-x-2 text-medical-teal font-bold">
                <Sparkles className="h-4 w-4" />
                <span>EDGESHIELD_LOCAL_AI_EXPLAINER</span>
              </div>
              <span className="text-[10px] bg-emerald-500/10 text-emerald-500 px-2.5 py-0.5 rounded-full font-bold border border-emerald-500/20">
                HUMAN UNDERSTANDABLE
              </span>
            </div>

            <div className="space-y-3">
              <div>
                <div className="text-xs font-bold text-muted-foreground uppercase tracking-wider">Clinical Explanation:</div>
                <p className="text-xs text-foreground mt-1 leading-relaxed">
                  An unauthorized external host (172.16.8.204) is transferring highly encrypted payload data (Byte Entropy: 7.88/8.0) into the Siemens DICOM Radiology Workstation at Radiology Imaging Bay 2. This pattern matches ransomware targeting PACS radiology image repositories.
                </p>
              </div>

              <div>
                <div className="text-xs font-bold text-rose-400 uppercase tracking-wider">Hospital Operational Risk:</div>
                <p className="text-xs text-foreground mt-1 leading-relaxed">
                  Ransomware encryption could lock radiology scans (CT/MRI), delaying emergency surgical procedures and compromising patient medical history integrity.
                </p>
              </div>

              <div className="p-3 rounded-xl bg-secondary/60 border text-xs font-mono text-foreground space-y-1">
                <div className="font-bold text-emerald-500 flex items-center space-x-1">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  <span>Actionable Containment Playbook:</span>
                </div>
                <div>1. Instantly isolate Siemens DICOM Radiology Workstation at network switch VLAN boundary.</div>
                <div>2. Block TCP port 104 and incoming traffic from host 172.16.8.204.</div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};
