import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

def create_architecture_diagram(output_path="figures/fig1_architecture.png"):
    fig, ax = plt.subplots(figsize=(15, 8.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background color
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Color Palette - Professional IEEE Journal Theme
    c_tier1_border = '#0284C7' # Sky Blue
    c_tier1_bg = '#F0F9FF'
    c_tier2_border = '#4F46E5' # Indigo
    c_tier2_bg = '#EEF2FF'
    c_tier3_border = '#0D9488' # Teal
    c_tier3_bg = '#F0FDFA'
    c_tier4_border = '#D97706' # Amber
    c_tier4_bg = '#FFFBEB'

    tier_y = 12
    tier_h = 76
    tier_w = 21.5

    # Coordinates for 4 Tiers
    tiers = [
        {
            "name": "TIER 1: EDGE TELEMETRY & SENSING",
            "x": 2.5, "y": tier_y, "w": tier_w, "h": tier_h,
            "border": c_tier1_border, "bg": c_tier1_bg,
            "badge": "L2-L7 Medical Network Layer",
            "subsections": [
                ("IoMT Medical Equipment", [
                    "• Smart Infusion Pumps (Alaris / B. Braun)",
                    "• Mechanical Ventilators (PB 980 / Dräger)",
                    "• ICU Multiparameter Patient Monitors",
                    "• PACS DICOM Imaging Workstations"
                ], '#E0F2FE', '#0369A1'),
                ("Clinical & IoT Protocols", [
                    "• Modbus/TCP (Port 502) - Telemetry",
                    "• MQTT (Port 1883) - Pub/Sub Sensor Stream",
                    "• DICOM (Port 104) - Medical Images",
                    "• HL7 v2/v3 (Port 2575) - Patient Feeds"
                ], '#E0F2FE', '#0369A1'),
                ("Dual Ingestion Paths", [
                    "• Live Edge Telemetry Interface",
                    "• Synthetic / OOD Attack Injector",
                    "• TrafficOrigin Metadata Provenance",
                    "• Hardware Zero-Copy Ring Buffer"
                ], '#E0F2FE', '#0369A1')
            ]
        },
        {
            "name": "TIER 2: CANONICAL DETECTION ENGINE",
            "x": 26.5, "y": tier_y, "w": tier_w, "h": tier_h,
            "border": c_tier2_border, "bg": c_tier2_bg,
            "badge": "Sub-5ms Real-Time Fast Path",
            "subsections": [
                ("Device Resolution & Mapping", [
                    "• IP/MAC -> Hospital Device Inventory",
                    "• Resolution: Matched, Ambiguous, Unreg.",
                    "• Profile Lookup: Life-Critical Flagging",
                    "• Baselined Dynamic Baseline Threshold"
                ], '#E0E7FF', '#3730A3'),
                ("Dual-Stage ML Scoring", [
                    "• Leakage-Safe Config B (29 Features)",
                    "• Stage 1: Unsupervised Isolation Forest",
                    "  - Anomaly Score Calibrated to [0.0, 1.0]",
                    "• Stage 2: Supervised Random Forest",
                    "  - 6 Classes (Flood, Ransom, MITM, etc.)",
                    "  - Zero IP/Port Leakage Guarantee"
                ], '#E0E7FF', '#3730A3'),
                ("Alert Flooding Aggregation", [
                    "• 60s Sliding Aggregation Window",
                    "• Deduplication of Volumetric Floods",
                    "• Rolling Exponential Risk Decay (15m)",
                    "• Device States: Active, Warning, Critical"
                ], '#E0E7FF', '#3730A3')
            ]
        },
        {
            "name": "TIER 3: LOCAL AI & SAFETY INTERLOCKS",
            "x": 50.5, "y": tier_y, "w": tier_w, "h": tier_h,
            "border": c_tier3_border, "bg": c_tier3_bg,
            "badge": "Cyber-Physical Safety Interlock",
            "subsections": [
                ("Cyber-Physical Safety Interlock", [
                    "• Bedside Clinician Override Guarantee",
                    "• Lethal Bolus Block (>50 mL/h freeze)",
                    "• Ventilator Barotrauma (>40 cmH2O block)",
                    "• Anti-Replay & Physiological Paradox Check",
                    "• VLAN Isolation with Device Continuity"
                ], '#CCFBF1', '#0F766E'),
                ("Asynchronous Local Explainable AI", [
                    "• Non-blocking Worker (Decoupled Queue)",
                    "• Lifecycle: PENDING -> GEN -> COMPLETED",
                    "• PyMuPDF Vector RAG over Service Manuals",
                    "• Clinical Impact & Mitigation Context",
                    "• Deterministic Heuristic Fallback"
                ], '#CCFBF1', '#0F766E'),
                ("Controlled Enforcement Adapters", [
                    "• Host Linux iptables (DROP Attacker IP)",
                    "• In-Flight Verification (sudo -n, iptables -C)",
                    "• Exact Inverse Rollback (iptables -D)",
                    "• Simulation Adapter for Dev / Staging"
                ], '#CCFBF1', '#0F766E')
            ]
        },
        {
            "name": "TIER 4: DASHBOARD & CLINICAL PIPELINE",
            "x": 74.5, "y": tier_y, "w": tier_w, "h": tier_h,
            "border": c_tier4_border, "bg": c_tier4_bg,
            "badge": "Operator UI & Decoupled Clinical",
            "subsections": [
                ("FastAPI Core & WebSockets", [
                    "• Async ASGI Coroutines (<2ms loop)",
                    "• SQLite WAL (Non-Blocking Concurrency)",
                    "• WebSocket Stream Manager (2s updates)",
                    "• REST API (Alerts, Devices, Audit Logs)"
                ], '#FEF3C7', '#B45309'),
                ("React 18 Operator Dashboard", [
                    "• Real-time Telemetry & Threat Monitor",
                    "• Device Inventory & Health Status Grid",
                    "• Explainable AI Copilot Drawer View",
                    "• Interlock Bedside Override Controls"
                ], '#FEF3C7', '#B45309'),
                ("Decoupled Pipeline B: Clinical", [
                    "• MIMIC-IV ICU Vital Signs Monitoring",
                    "• 24h Bounded Window (Zero Future Leak)",
                    "• 69 Physiological Statistical Features",
                    "• Patient-Grouped Split (ROC-AUC 0.7600)",
                    "• Strict Research-Only Medical Baseline"
                ], '#FEF3C7', '#B45309')
            ]
        }
    ]

    # Draw Tiers
    for t in tiers:
        # Outer Card
        outer = FancyBboxPatch((t["x"], t["y"]), t["w"], t["h"],
                               boxstyle="round,pad=0.3,rounding_size=1.2",
                               edgecolor=t["border"], facecolor=t["bg"],
                               linewidth=2.0, zorder=1)
        ax.add_patch(outer)

        # Tier Header Banner
        header = FancyBboxPatch((t["x"] + 0.3, t["y"] + t["h"] - 5.5), t["w"] - 0.6, 5.0,
                                boxstyle="round,pad=0.2,rounding_size=0.8",
                                edgecolor=t["border"], facecolor=t["border"],
                                linewidth=1.0, zorder=2)
        ax.add_patch(header)

        # Header Title
        ax.text(t["x"] + t["w"]/2.0, t["y"] + t["h"] - 3.0, t["name"],
                color="#FFFFFF", fontsize=8.2, fontweight='bold',
                ha='center', va='center', zorder=3)

        # Badge under header
        ax.text(t["x"] + t["w"]/2.0, t["y"] + t["h"] - 7.2, f"[{t['badge']}]",
                color=t["border"], fontsize=7.2, fontweight='bold', style='italic',
                ha='center', va='center', zorder=3)

        # Draw Subsections
        sub_y_start = t["y"] + t["h"] - 9.5
        box_spacing = 21.5
        for i, (title, items, box_bg, box_border) in enumerate(t["subsections"]):
            cur_y = sub_y_start - (i * box_spacing) - 20.0
            box_h = 20.0

            sub_box = FancyBboxPatch((t["x"] + 0.8, cur_y), t["w"] - 1.6, box_h,
                                     boxstyle="round,pad=0.2,rounding_size=0.6",
                                     edgecolor=box_border, facecolor=box_bg,
                                     linewidth=1.2, zorder=2)
            ax.add_patch(sub_box)

            # Subsection Title
            ax.text(t["x"] + 1.4, cur_y + box_h - 2.5, title,
                    color=box_border, fontsize=7.8, fontweight='bold',
                    ha='left', va='center', zorder=3)

            # Subsection items
            line_y = cur_y + box_h - 5.2
            for item in items:
                ax.text(t["x"] + 1.4, line_y, item,
                        color='#1E293B', fontsize=6.3,
                        ha='left', va='center', zorder=3)
                line_y -= 3.1

    # Connective Flow Arrows Between Tiers
    arrow_props_fw = dict(arrowstyle="-|>,head_width=0.4,head_length=0.7",
                          color="#1E293B", lw=2.2, mutation_scale=15)
    arrow_props_dash = dict(arrowstyle="-|>,head_width=0.35,head_length=0.6",
                           color="#0D9488", lw=1.8, linestyle="--", mutation_scale=12)

    # Tier 1 -> Tier 2 (Telemetry Stream)
    ax.annotate("", xy=(26.3, 56), xytext=(24.2, 56),
                arrowprops=arrow_props_fw, zorder=5)
    ax.text(25.3, 58.5, "L2-L7 Raw\nTelemetry", color="#0369A1", fontsize=6.8,
            fontweight='bold', ha='center', va='bottom', zorder=6,
            bbox=dict(boxstyle="square,pad=0.1", fc="#FFFFFF", ec="none"))

    # Tier 2 -> Tier 3 (Anomalies & Threat Detections)
    ax.annotate("", xy=(50.3, 56), xytext=(48.2, 56),
                arrowprops=arrow_props_fw, zorder=5)
    ax.text(49.3, 58.5, "Threat Events\n& Risk Scores", color="#3730A3", fontsize=6.8,
            fontweight='bold', ha='center', va='bottom', zorder=6,
            bbox=dict(boxstyle="square,pad=0.1", fc="#FFFFFF", ec="none"))

    # Tier 3 -> Tier 4 (Enriched Alerts & Safety Directives)
    ax.annotate("", xy=(74.3, 56), xytext=(72.2, 56),
                arrowprops=arrow_props_fw, zorder=5)
    ax.text(73.3, 58.5, "Enriched Alerts\n& Interlocks", color="#0F766E", fontsize=6.8,
            fontweight='bold', ha='center', va='bottom', zorder=6,
            bbox=dict(boxstyle="square,pad=0.1", fc="#FFFFFF", ec="none"))

    # Feedback / Safety Interlock override loop (Tier 4 -> Tier 3)
    ax.annotate("", xy=(72.2, 28), xytext=(74.3, 28),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6",
                                color="#D97706", lw=1.8, linestyle="-.", mutation_scale=12),
                zorder=5)
    ax.text(73.3, 30.5, "Clinician\nOverride", color="#B45309", fontsize=6.5,
            fontweight='bold', ha='center', va='bottom', zorder=6,
            bbox=dict(boxstyle="square,pad=0.1", fc="#FFFFFF", ec="none"))

    # Title Banner across top
    title_box = FancyBboxPatch((2.5, 90.0), 95.0, 7.5,
                               boxstyle="round,pad=0.3,rounding_size=1.0",
                               edgecolor='#1E293B', facecolor='#0F172A',
                               linewidth=1.5, zorder=2)
    ax.add_patch(title_box)

    ax.text(50.0, 94.8, "EdgeShield AI: Four-Tier Edge-Native Architecture & Dual-Pipeline Decoupling",
            color="#38BDF8", fontsize=11.5, fontweight='bold', ha='center', va='center', zorder=4)
    ax.text(50.0, 91.8, "Strict Decoupling of Sub-5ms IoMT Cybersecurity (Pipeline A) and Prospective MIMIC-IV Clinical Monitoring (Pipeline B)",
            color="#E2E8F0", fontsize=7.8, ha='center', va='center', zorder=4)

    # Footnote / Legend banner across bottom
    legend_box = FancyBboxPatch((2.5, 2.5), 95.0, 7.0,
                                boxstyle="round,pad=0.2,rounding_size=0.8",
                                edgecolor='#CBD5E1', facecolor='#F8FAFC',
                                linewidth=1.0, zorder=2)
    ax.add_patch(legend_box)

    legend_text = (
        "Dual-Pipeline Invariant: Pipeline A processes network telemetry (L2-L7) with zero patient data. "
        "Pipeline B processes clinical vitals (MIMIC-IV) with zero packet telemetry.\n"
        "Cyber-Physical Safety Guarantee: Life-critical devices (infusion pumps, ventilators) trigger bedside clinician override interlocks before any autonomous network isolation."
    )
    ax.text(50.0, 6.0, legend_text, color='#334155', fontsize=6.8, ha='center', va='center', zorder=3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Architecture diagram successfully saved to {output_path}")

if __name__ == '__main__':
    create_architecture_diagram()
