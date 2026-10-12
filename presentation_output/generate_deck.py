"""
EdgeShield AI: Professional Technical Presentation Generator
Generates a polished 19-slide widescreen PowerPoint presentation based on
verified repository implementation, audit artifacts, and research metrics.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.abspath("presentation_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
PPTX_PATH = os.path.join(OUTPUT_DIR, "EdgeShield_AI_Technical_Presentation.pptx")

# ==============================================================================
# DESIGN SYSTEM & PALETTE (Dark Enterprise Cybersecurity & Smart Healthcare)
# ==============================================================================
COLOR_BG = RGBColor(11, 17, 32)         # Deep Midnight Slate (#0B1120)
COLOR_CARD = RGBColor(22, 34, 56)       # Dark Navy Card (#162238)
COLOR_CARD_ALT = RGBColor(18, 28, 47)   # Alternate Card (#121C2F)
COLOR_BORDER = RGBColor(45, 63, 94)     # Slate Border (#2D3F5E)
COLOR_BORDER_TEAL = RGBColor(20, 184, 166) # Teal Border
COLOR_TEXT_WHITE = RGBColor(248, 250, 252) # Pure Off-White (#F8FAFC)
COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # Slate Muted (#94A3B8)
COLOR_TEXT_LIGHT = RGBColor(203, 213, 225) # Body Text (#CBD5E1)
COLOR_TEAL = RGBColor(14, 165, 233)     # Medical / Tech Cyan (#0EA5E9)
COLOR_MINT = RGBColor(20, 184, 166)     # Clinical Mint (#14B8A6)
COLOR_ROSE = RGBColor(239, 68, 68)      # Alert / Threat Rose (#EF4444)
COLOR_AMBER = RGBColor(245, 158, 11)    # Warning / Disclaimers (#F59E0B)
COLOR_EMERALD = RGBColor(16, 185, 129)  # Passed / Verified Green (#10B981)
COLOR_INDIGO = RGBColor(99, 102, 241)   # Architecture / ML Indigo (#6366F1)

FONT_HEADING = "Helvetica"
FONT_BODY = "Arial"


def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: Set solid slide background
    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    # Helper: Add standard slide header
    def add_header(slide, slide_num, title, category="EDGESHIELD AI — TECHNICAL & RESEARCH REVIEW"):
        # Category / Tracker Pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.3))
        tf = cat_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"{category.upper()}  |  SLIDE {slide_num:02d} OF 19"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEAL

        # Slide Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.0), Inches(0.6))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_WHITE

        # Divider line
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02))
        div.fill.solid()
        div.fill.fore_color.rgb = COLOR_BORDER
        div.line.fill.background()

    # Helper: Add rounded card container
    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # Helper: Add speaker notes
    def set_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text.strip()

    # ==========================================================================
    # SLIDE 1: Title & Executive Overview
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Top accent bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(2.2), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_TEAL
    top_bar.line.fill.background()

    # Project Title
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.05), Inches(11.7), Inches(1.4))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "EdgeShield AI"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "An Edge-Based Intelligent Intrusion Detection and Generative AI Framework for Secure Smart Healthcare IoT Networks"
    p1_sub.font.name = FONT_BODY
    p1_sub.font.size = Pt(15)
    p1_sub.font.color.rgb = COLOR_TEAL
    p1_sub.space_before = Pt(6)

    # 3 Summary Cards
    card1 = add_card(s1, 0.8, 2.7, 3.65, 3.8)
    tf_c1 = card1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "🛡️ IoMT Cybersecurity"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE
    bullets_c1 = [
        "Monitors connected hospital devices (infusion pumps, smart ventilators, DICOM PACS).",
        "Dual-Stage ML Detection: Isolation Forest anomaly detector + 6-class Random Forest threat classifier.",
        "Sub-millisecond edge packet processing with physical invariant & anti-replay validation.",
        "Linux iptables firewall isolation with automated Clinical Safety Interlocks."
    ]
    for b in bullets_c1:
        p_b = tf_c1.add_paragraph()
        p_b.text = f"• {b}"
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = COLOR_TEXT_LIGHT
        p_b.space_before = Pt(8)

    card2 = add_card(s1, 4.84, 2.7, 3.65, 3.8)
    tf_c2 = card2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "🤖 Local GenAI & RAG"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE
    bullets_c2 = [
        "Offline Small Language Models (Ollama Llama-3 / Phi-3) executing locally.",
        "Zero Cloud Data Egress: Complete compliance with HIPAA, HITECH & GDPR.",
        "Decoupled Asynchronous Explainability: Explains alerts in human language without blocking edge detection.",
        "Local RAG Copilot with PDF document search across medical device protocols."
    ]
    for b in bullets_c2:
        p_b = tf_c2.add_paragraph()
        p_b.text = f"• {b}"
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = COLOR_TEXT_LIGHT
        p_b.space_before = Pt(8)

    card3 = add_card(s1, 8.88, 2.7, 3.65, 3.8)
    tf_c3 = card3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "🏥 Clinical Research Module"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT
    bullets_c3 = [
        "Completely decoupled research pipeline using MIMIC-IV Demo 2.2 dataset.",
        "Prospective 24-Hour Window: Extracts 69 features across 7 vital signs with strict zero-leakage protocol.",
        "Patient-Grouped Validation: Evaluates L2 Logistic Regression & Random Forest baseline comparators.",
        "Engineering & Research Prototype: Mandatory disclaimers; not an FDA-cleared diagnostic device."
    ]
    for b in bullets_c3:
        p_b = tf_c3.add_paragraph()
        p_b.text = f"• {b}"
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = COLOR_TEXT_LIGHT
        p_b.space_before = Pt(8)

    # Bottom Metadata Strip
    strip = add_card(s1, 0.8, 6.7, 11.733, 0.5, bg_color=COLOR_CARD_ALT)
    tf_s = strip.text_frame
    p_s = tf_s.paragraphs[0]
    p_s.text = "Key Takeaway: EdgeShield AI integrates IoMT edge security operations with an audited, leak-free clinical informatics pipeline. Both modules operate independently on decoupled services."
    p_s.font.size = Pt(10)
    p_s.font.color.rgb = COLOR_TEXT_MUTED
    p_s.alignment = PP_ALIGN.CENTER

    set_notes(s1, """
Speaker Notes — Slide 1: Executive Overview
• Purpose: Introduce EdgeShield AI as a multi-domain engineering and research prototype designed for smart hospital infrastructure.
• Emphasize Architectural Decoupling: Make it clear right away that the cybersecurity intrusion detection system and the clinical patient-monitoring risk pipeline are NOT a single trained model. They are two distinct, complementary subsystems operating on a unified platform.
• Key Motivation: Modern hospitals operate thousands of connected IoT devices (infusion pumps, telemetry monitors, ventilators). Security alerts in hospitals often confuse biomedical engineers because they lack clinical context. EdgeShield solves this by combining deterministic ML intrusion detection, local privacy-preserving generative AI explainability, and an audited clinical vital-sign research pipeline.
• Potential Questions:
  - Q: Is this deployed in an active hospital?
  - A: No, this is an advanced engineering prototype and research pipeline verified against MIMIC-IV Demo data and simulated medical IoT streams.
""")

    # ==========================================================================
    # SLIDE 2: Background: Modern Smart Healthcare & Connected IoMT
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, 2, "Modern Smart Healthcare & Connected IoMT Landscape")

    # 4 Pillar Cards
    pillars = [
        ("Massive Medical IoT Attack Surface", "Infusion pumps, smart ventilators, ICU monitors, and PACS radiology servers now continuously stream telemetry over hospital LANs. Medical devices cannot run traditional endpoint protection agents due to firmware and FDA certification constraints.", COLOR_TEAL),
        ("Inherent Healthcare Protocol Weaknesses", "Protocols such as DICOM (port 104), MQTT (port 1883), Modbus/TCP (port 502), and HL7 were engineered for interoperability rather than adversarial resistance, lacking mutual authentication and encryption in legacy deployments.", COLOR_ROSE),
        ("Life-Critical Clinical Consequences", "Unlike corporate IT, healthcare intrusions threaten patient lives: ransomware locks diagnostic MRI scans, DoS attacks starve infusion pumps of telemetry, and command injection attacks can manipulate ventilator pressures or silence alarms.", COLOR_AMBER),
        ("Why Edge Architecture is Essential", "Cloud-based IDS introduces >200ms round-trip latency, high bandwidth costs, and outage vulnerabilities. Edge gateways adjacent to clinical subnets achieve <5ms response times, 100% offline survivability, and zero cloud data egress.", COLOR_EMERALD),
    ]

    for i, (title, desc, accent) in enumerate(pillars):
        x = 0.8 + i * 2.98
        card = add_card(s2, x, 1.6, 2.78, 5.3)
        tf = card.text_frame
        tf.word_wrap = True
        
        # Header box inside card
        p_num = tf.paragraphs[0]
        p_num.text = f"0{i+1}"
        p_num.font.name = FONT_HEADING
        p_num.font.size = Pt(28)
        p_num.font.bold = True
        p_num.font.color.rgb = accent

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_WHITE
        p_t.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_TEXT_LIGHT
        p_d.space_before = Pt(12)

    set_notes(s2, """
Speaker Notes — Slide 2: Background & Context
• Healthcare IoMT Growth: Hospitals have seen exponential adoption of connected medical devices. An average hospital bed has 10–15 connected devices.
• The Problem with Legacy Protocols: Modbus, DICOM, and MQTT were created decades ago or designed for industrial simplicity. They often transmit plaintext data, making them prime targets for man-in-the-middle attacks, packet flooding, or malformed function injection.
• Edge Justification: Emphasize why edge computing is chosen. In critical care (ICU, OR), network decisions must happen in milliseconds. Transmitting sensitive patient waveforms to third-party cloud APIs violates HIPAA and creates severe reliability hazards if the hospital's internet connection degrades.
• Anticipated Question: Can't we just install antivirus on medical devices?
  - Answer: No. Medical devices run proprietary real-time operating systems (RTOS) or locked Linux firmware. Modifying software on certified medical devices can void regulatory approval. Intrusion detection must therefore occur non-intrusively at the network edge.
""")

    # ==========================================================================
    # SLIDE 3: Problem Statement
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, 3, "Problem Statement: Dual Challenges in Healthcare Systems")

    # Column 1: Cybersecurity Challenges
    c1 = add_card(s3, 0.8, 1.6, 5.7, 5.3)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "PART A: Healthcare IoT Cybersecurity Challenges"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE

    cyber_probs = [
        ("Cognitive Alert Fatigue", "Commercial firewalls emit cryptic alerts (e.g., 'SYN_FLOOD port 1883') that clinical biomedical engineers cannot rapidly interpret in terms of patient therapy impacts."),
        ("Zero-Day & Polymorphic Exploits", "Signature firewalls fail against previously unseen packet variations targeting medical IoT devices without known CVE signatures."),
        ("Catastrophic Disconnect Hazards", "Blindly terminating network ports on medical devices can shut down life-support equipment or halt chemotherapy delivery, causing clinical harm."),
        ("Regulatory & Privacy Constraints", "Transmitting hospital packet traces to cloud LLMs (OpenAI, Anthropic) risks HIPAA/GDPR violations due to embedded patient identifiers in DICOM or HL7 payloads.")
    ]
    for title, desc in cyber_probs:
        pt = tf1.add_paragraph()
        pt.text = f"• {title}: "
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(8)
        
        # Inline description
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    # Column 2: Clinical Data Science Challenges
    c2 = add_card(s3, 6.83, 1.6, 5.7, 5.3)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "PART B: Critical Care Clinical Data & ML Challenges"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT

    clin_probs = [
        ("Temporal Boundary & Target Leakage", "Many academic clinical ML models inadvertently evaluate records recorded after the prediction cutoff, or fail to prospectively exclude pre-prediction deaths and discharges."),
        ("Pervasive Patient-Level Overlap Leakage", "ICU patients frequently have repeated admissions. Random stay-level splitting allows features from the same patient into both train and test splits, causing severe overfitting."),
        ("Small Demonstration Sample Volatility", "Evaluating models on small demo cohorts (e.g., MIMIC-IV Demo) produces wide confidence intervals. Overstated claims without uncertainty bounds mislead stakeholders."),
        ("Conflating Bedside Heuristics with ML", "Clinical monitoring software often misrepresents simple threshold alerts (e.g., tachycardia > 120 bpm) as predictive artificial intelligence, confusing validation boundaries.")
    ]
    for title, desc in clin_probs:
        pt = tf2.add_paragraph()
        pt.text = f"• {title}: "
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(8)

        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    set_notes(s3, """
Speaker Notes — Slide 3: Problem Statement
• Delineate Both Problem Domains: Highlight that smart hospitals face dual technical challenges: defending medical hardware against sophisticated cyber threats while also properly validating clinical monitoring pipelines without academic leakage.
• Emphasize Alert Fatigue: Biomedical engineers are not cybersecurity analysts. When an alarm triggers on an infusion pump, they need to know: Is this a network attack? What therapy is being disrupted? What manual override must I execute?
• Emphasize Data Leakage in Clinical ML: Most published hospital AI models fail in practice because they leak future information (temporal leakage) or evaluate duplicate ICU stays from the same patient across splits (patient overlap leakage). EdgeShield AI tackles this by instituting an audited zero-leakage methodology.
""")

    # ==========================================================================
    # SLIDE 4: Project Objectives & Core Engineering Principles
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, 4, "Project Objectives & Core Engineering Principles")

    # Left Container: Primary Objectives
    left_c = add_card(s4, 0.8, 1.6, 5.7, 5.3)
    tf_l = left_c.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "🎯 Primary Engineering Objectives"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    objs = [
        "Develop an Edge-First Cyber Defense Engine capable of multi-protocol packet ingestion (DICOM, MQTT, Modbus) with sub-millisecond anomaly detection.",
        "Integrate Privacy-Preserving GenAI that translates raw ML feature importances into clinical impact assessments and actionable containment playbooks offline.",
        "Implement Safe Cyber-Physical Enforcement with Clinical Safety Interlocks, supporting Linux iptables and development simulation adapters.",
        "Construct a Leak-Free 24-Hour Clinical Data Pipeline on the MIMIC-IV Demo 2.2 dataset with prospective temporal boundaries.",
        "Engineer 69 Clinical Features across 7 vital signs and evaluate patient-grouped baseline mortality models with full uncertainty transparency.",
        "Deliver a Full-Stack Web Cockpit (FastAPI + React 18) verified with 100% automated backend test coverage."
    ]
    for o in objs:
        po = tf_l.add_paragraph()
        po.text = f"✓ {o}"
        po.font.size = Pt(10.5)
        po.font.color.rgb = COLOR_TEXT_LIGHT
        po.space_before = Pt(8)

    # Right Container: Non-Negotiable Principles
    right_c = add_card(s4, 6.83, 1.6, 5.7, 5.3)
    tf_r = right_c.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "⚖️ Non-Negotiable Principles & Safeguards"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    principles = [
        ("Strict Architectural Separation", "Cybersecurity and clinical prediction modules operate on separate services, endpoints, and data structures. No cross-contamination of models."),
        ("Zero Data Leakage Protocol", "Observation window strictly enforced as [t_in, t_in + 24h). All stays with death or discharge <= 24h prospectively excluded."),
        ("Rigorous Grouped Splitting", "All repeat ICU stays from the same patient are kept in the same partition. Zero patient overlap between training and test sets."),
        ("Scientific Honesty & Wide CIs", "Disclose small-sample volatility: report the wide 95% bootstrap confidence interval [0.312, 1.000] and grouped CV results truthfully."),
        ("Safety-First Enforcement", "Never claim an in-memory database update is a real network firewall; provide explicit status distinctions between OS iptables and SIMULATION.")
    ]
    for title, desc in principles:
        pt = tf_r.add_paragraph()
        pt.text = f"• {title}: "
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(8)

        pd = tf_r.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    set_notes(s4, """
Speaker Notes — Slide 4: Objectives & Principles
• Focus on Engineering Integrity: Explain that EdgeShield AI was built with strict engineering guardrails rather than unrealistic hype.
• Decoupling Principle: Re-emphasize that the cybersecurity pipeline and the clinical pipeline solve two separate operational needs.
• Scientific Honesty: Acknowledge upfront that because the clinical dataset is a demonstration sample (MIMIC-IV Demo, 100 patients), we explicitly document confidence intervals and cross-validation discrepancies rather than claiming clinical perfection.
• Safety Interlocks: Point out that automated network disconnection in hospitals can be dangerous; fail-safe interlocks are an essential architectural requirement.
""")

    # ==========================================================================
    # SLIDE 5: Proposed Solution: Modular Dual-Pipeline Architecture
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, 5, "Proposed Solution: Modular Dual-Pipeline Architecture")

    # Left Pipeline: Cybersecurity
    pipe_left = add_card(s5, 0.8, 1.6, 5.7, 5.3)
    tf_pl = pipe_left.text_frame
    tf_pl.word_wrap = True
    p = tf_pl.paragraphs[0]
    p.text = "PIPELINE A: IoMT CYBERSECURITY PLATFORM"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    steps_cyber = [
        ("1. Multi-Protocol Ingest", "Continuous packet feeds (DICOM, MQTT, Modbus) & direct machine signals (TCP 9100, REST, MQTT bridge)."),
        ("2. Feature Extraction", "Computes 9 network telemetry metrics (packet length, byte rate, entropy, SYN flags, Modbus fn code)."),
        ("3. Dual-Stage ML Inference", "Stage 1: Isolation Forest (Zero-Day Anomaly Boundary)\nStage 2: Random Forest (Multi-Class Threat Categorization)"),
        ("4. Incident Correlation", "Rolling 60-second flow aggregator groups repetitive packets into single correlation incidents."),
        ("5. Decoupled AI Explainability", "Asynchronous background worker calls local Ollama SLM (Llama-3/Phi-3) or Expert Rule Engine for clinical impact & triage steps."),
        ("6. Dual-Mode Enforcement", "Enforces network quarantine via Linux iptables FORWARD DROP rules or development simulation adapter.")
    ]
    for title, desc in steps_cyber:
        pt = tf_pl.add_paragraph()
        pt.text = f"▶ {title}"
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(6)
        pd = tf_pl.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    # Right Pipeline: Clinical Research
    pipe_right = add_card(s5, 6.83, 1.6, 5.7, 5.3)
    tf_pr = pipe_right.text_frame
    tf_pr.word_wrap = True
    p = tf_pr.paragraphs[0]
    p.text = "PIPELINE B: CLINICAL VITAL-SIGN RESEARCH"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT

    steps_clin = [
        ("1. MIMIC-IV Clinical Demo Cohort", "140 ICU stays linked to hospital outcomes; 4 stays with death/discharge <= 24h prospectively excluded (136 eligible stays)."),
        ("2. Prospective 24h Observation", "Strict half-open interval [t_in, t_in + 24h) eliminates edge temporal leakage."),
        ("3. 69-Feature Engineering", "Extracts 9 summary stats across 7 core vital signs plus 6 overall data quality & observation indicators."),
        ("4. Preprocessing Isolation", "Median imputer and standard scaler fitted strictly on training folds to eliminate statistics leakage."),
        ("5. Patient-Grouped Evaluation", "Evaluates L2 Logistic Regression & Random Forest against Dummy Majority-Class Baseline using GroupShuffleSplit."),
        ("6. Disclaimed Risk Service", "Serves probability scores bounded [0, 1] categorized as LOW, ELEVATED, or HIGH with mandatory academic disclaimers.")
    ]
    for title, desc in steps_clin:
        pt = tf_pr.add_paragraph()
        pt.text = f"▶ {title}"
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(6)
        pd = tf_pr.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    set_notes(s5, """
Speaker Notes — Slide 5: Dual-Pipeline Architecture
• Walk Through the Flow: Guide the audience through the two parallel tracks.
• Track A (Cybersecurity): Shows the transition from raw network packets to feature extraction, sub-millisecond ML scoring, asynchronous local GenAI explanation, and safe network isolation.
• Track B (Clinical Informatics): Shows how raw MIMIC-IV ICU chart events pass through strict prospective filtering, 24-hour observation windows, 69-feature engineering, isolated preprocessing, and risk categorization.
• Key Point: Both pipelines converge on the same presentation dashboard (React 18) and API server (FastAPI), but their data pathways, models, and endpoints remain completely distinct.
""")

    # ==========================================================================
    # SLIDE 6: Comprehensive System Architecture
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, 6, "Comprehensive System Architecture & Layer Integration")

    # 3 Horizontal Tier Blocks
    tier1 = add_card(s6, 0.8, 1.6, 11.733, 1.5)
    tf1 = tier1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "TIER 1: PRESENTATION & INTERACTION LAYER (React 18 + TypeScript + Vite + Tailwind CSS)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p1 = tf1.add_paragraph()
    p1.text = "• Views: Overview Dashboard, Machine Signals Monitor, Patient Vitals & Risk View, Alert Center, Device Manager, ML Analytics, Attack Simulator, Document Reader.\n• Modals & Drawers: Deep-Dive AI Explainer Modal, Ambient AI Copilot Drawer (5 contexts: research, incident, device, architecture, telemetry), Security Action Workflow.\n• Communication: Real-time telemetry via WebSocket (/ws/telemetry), REST API service layer with full TypeScript typing."
    p1.font.size = Pt(10.5)
    p1.font.color.rgb = COLOR_TEXT_LIGHT
    p1.space_before = Pt(4)

    tier2 = add_card(s6, 0.8, 3.3, 11.733, 1.8)
    tf2 = tier2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "TIER 2: API & APPLICATION LOGIC LAYER (Python 3.11+ / FastAPI / Pydantic / SQLAlchemy)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p2 = tf2.add_paragraph()
    p2.text = "• Service Decoupling: CanonicalSecurityPipeline, MLEngineService (IsolationForest/RandomForest), AIEnrichmentService (Ollama), PDFService (RAG), PatientMonitoringService.\n• Endpoints: /health, /api/v1/devices, /alerts, /detection, /signals, /llm, /documents, /patient-monitoring (validate-vitals, assess-risk, predict, cohort-summary, sample-records).\n• Request Validation: Pydantic schemas enforcing physiological bounds, finite numeric checks (rejection of NaN/Inf), and 69-feature schema matching."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = COLOR_TEXT_LIGHT
    p2.space_before = Pt(4)

    tier3 = add_card(s6, 0.8, 5.3, 11.733, 1.6)
    tf3 = tier3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "TIER 3: DATA, MODEL & ENFORCEMENT LAYER (SQLite / Scikit-Learn / Ollama SLM / Host Firewall)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT
    p3 = tf3.add_paragraph()
    p3.text = "• Model Binaries: baseline_model.joblib (L2 Logistic Regression), classifier.joblib (100-tree Random Forest), isolation_forest.joblib, scaler.joblib.\n• Storage: SQLite (edgeshield.db: devices, alerts, packet logs, machine signals, safety interlocks, audit logs) + MIMIC-IV Demo 2.2 parquet/csv data.\n• Enforcement Adapters: HostFirewallAdapter (Linux iptables FORWARD DROP) and SimulationEnforcementAdapter (macOS/Windows dev fallback)."
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = COLOR_TEXT_LIGHT
    p3.space_before = Pt(4)

    set_notes(s6, """
Speaker Notes — Slide 6: Comprehensive Architecture
• Explain the Three-Tier Structure: Detail how the React frontend, FastAPI backend, and data/enforcement layers interact cleanly.
• Highlight Request Validation: Notice how FastAPI and Pydantic act as a gatekeeper. If someone sends NaN, Infinity, or an unrecognized feature key to the clinical endpoint, it gets rejected immediately with an HTTP 422 before reaching the model.
• Persistence & Models: Point out that model artifacts are versioned in `research/patient_monitoring/` and loaded into memory on FastAPI startup.
""")

    # ==========================================================================
    # SLIDE 7: Cybersecurity Module: Telemetry Ingestion & Device Inventory
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, 7, "Cybersecurity Module: Telemetry Ingestion & Device Inventory")

    # Card 1: Medical Device Inventory
    c1 = add_card(s7, 0.8, 1.6, 5.7, 5.3)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "📋 Smart Hospital Medical Device Inventory"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    devices = [
        ("DEV-ICU-101", "ICU Telemetry Station A", "192.168.10.101", "Modbus/TCP", "Risk: 12.0 (Active)"),
        ("DEV-PUMP-204", "Alaris Infusion Pump #4", "192.168.10.102", "MQTT", "Risk: 68.5 (Warning)"),
        ("DEV-VENT-301", "Puritan Bennett Ventilator", "192.168.10.103", "Modbus", "Risk: 5.0 (Active)"),
        ("DEV-RAD-405", "Siemens DICOM Workstation", "192.168.10.104", "DICOM", "Risk: 94.0 (Critical)"),
        ("DEV-SYRINGE-12", "Baxter Smart Syringe Driver", "192.168.10.105", "MQTT", "Risk: 18.0 (Active)")
    ]
    for dev_id, name, ip, proto, risk in devices:
        pt = tf1.add_paragraph()
        pt.text = f"• {dev_id}: {name}"
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = f"   IP: {ip} | Protocol: {proto} | Status: {risk}"
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    p_note = tf1.add_paragraph()
    p_note.text = "\nDatabase Tracking: Stores MAC addresses, firmware versions, hospital locations, and real-time risk scores updated dynamically based on telemetry."
    p_note.font.size = Pt(10)
    p_note.font.color.rgb = COLOR_TEXT_MUTED

    # Card 2: Collector Interfaces & Incident Correlation
    c2 = add_card(s7, 6.83, 1.6, 5.7, 5.3)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🔌 Ingestion Interfaces & Flow Correlation"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT

    collectors = [
        ("Bedside REST Ingest", "POST /api/v1/signals/ingest — High-throughput JSON collector for bedside micro-gateways (Raspberry Pi, industrial gateways)."),
        ("Medical Machine TCP Socket", "tcp://0.0.0.0:9100 — Direct raw TCP stream listener accepting continuous hospital device byte streams."),
        ("Hospital MQTT Telemetry Bridge", "Subscribes to hospital-broker.lan:1883/devices/+/telemetry for continuous vital and infusion telemetry."),
        ("Incident Flow Correlator", "IncidentCorrelator groups repetitive packets within a rolling 60-second window by (src_ip, dst_ip, threat_type, protocol, device_id), preventing notification floods."),
        ("PipelineMetricsCollector", "In-memory rolling metrics window (200 events) tracks average detection latency (verified < 1.0 ms) and AI latency.")
    ]
    for title, desc in collectors:
        pt = tf2.add_paragraph()
        pt.text = f"▶ {title}"
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    set_notes(s7, """
Speaker Notes — Slide 7: Ingestion & Device Inventory
• Asset Visibility: Emphasize that you cannot defend what you cannot see. The Device Manager maintains a real-time inventory of hospital assets with IP/MAC mapping and dynamic risk scores.
• Multi-Channel Telemetry: Medical equipment communicates over different channels. The system implements a REST ingest endpoint, a direct raw TCP listener on port 9100, and an MQTT broker bridge.
• Incident Correlation: During an active flood attack, a sensor might emit 1,000 packets per second. The Incident Correlator aggregates these into a single alert flow with an incrementing packet counter, preventing the security dashboard from crashing or overwhelming operators.
""")

    # ==========================================================================
    # SLIDE 8: Cyber-Physical Threat Detection & Machine Signal Invariants
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, 8, "Cyber-Physical Threat Detection & Machine Signal Invariants")

    # Left: 9 Feature Vectors & ML Models
    left_c = add_card(s8, 0.8, 1.6, 5.7, 5.3)
    tf1 = left_c.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "⚡ 9-Feature Vector & Dual-Stage Detection"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    feats = [
        "packet_length (bytes)", "flow_duration (seconds)", "header_length (bytes)",
        "byte_rate (bytes/sec)", "packet_rate (pkts/sec)", "tcp_syn_flag (0 or 1)",
        "mqtt_msg_rate (msgs/sec)", "modbus_fn_code (fn code ID)", "entropy (payload 0-8)"
    ]
    p_f = tf1.add_paragraph()
    p_f.text = "Extracted Telemetry Features (9): " + ", ".join(feats[:5]) + ", " + ", ".join(feats[5:])
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = COLOR_TEXT_LIGHT
    p_f.space_before = Pt(4)

    attacks = [
        ("Normal", "Baseline medical traffic (flow 0.1-5s, modest rates, read fn codes)."),
        ("DICOM Ransomware", "Burst payloads, high encryption entropy (>7.5), large packet size (>1300B) targeting PACS radiology archives."),
        ("MQTT Flood DoS", "Massive message rate (>300 msgs/s) starving infusion pump telemetry brokers."),
        ("Modbus Command Injection", "Unauthorized write commands (Fn Codes 5, 6, 15, 16) targeting ventilators."),
        ("ARP Spoofing MITM", "High packet rate with small packet lengths (<80B) intercepting patient vitals."),
        ("Port Scan Reconnaissance", "High TCP SYN flag rate with tiny packets searching for exposed medical ports.")
    ]
    for att, desc in attacks:
        pt = tf1.add_paragraph()
        pt.text = f"• {att}: "
        pt.font.bold = True
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_ROSE if att != "Normal" else COLOR_EMERALD
        pt.space_before = Pt(4)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    # Right: Machine Signal Invariant & CPS Engine
    right_c = add_card(s8, 6.83, 1.6, 5.7, 5.3)
    tf2 = right_c.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🩺 Cyber-Physical Invariants & Anti-Replay"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT

    invariants = [
        ("Anti-Replay & Sequence Enforcement", "Tracks monotonic sequence counters and timestamp freshness per device; rejects stale, replayed, or out-of-order packets attempting to forge vital-sign trends."),
        ("Bolus Overdose Protection", "Monitors infusion pump flow rate invariants (e.g., maximum safe infusion rate 999 mL/h). Flags sudden anomalous multiplier jumps as cyber-tampering."),
        ("Barotrauma Ventilator Hijack Defense", "Inspects ventilator peak inspiratory pressure (PIP). Flags attempts to force high pressure (>40 cmH2O) that would cause patient lung barotrauma."),
        ("Sensor Value Spoofing Defense", "Cross-validates physiological trends against physical bounds; detects artificial square-wave sensor injection attacks."),
        ("Verified Implementation", "Engineered in MachineSignalCybersecurityEngine with active state tracking per connected medical device ID.")
    ]
    for title, desc in invariants:
        pt = tf2.add_paragraph()
        pt.text = f"▶ {title}"
        pt.font.bold = True
        pt.font.size = Pt(10.5)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    set_notes(s8, """
Speaker Notes — Slide 8: Detection & Invariants
• 9 Network Features: Explain why entropy, packet rates, and protocol-specific fields (Modbus function codes, MQTT rates) are ideal for detecting medical device compromises.
• Contrast the 2-Stage Model: Stage 1 uses an unsupervised Isolation Forest trained on normal traffic. This detects unknown anomalies and zero-day deviations. Stage 2 uses a multi-class Random Forest to classify known attack behaviors (ransomware, DoS, command injection).
• Cyber-Physical Security (CPS): Emphasize that EdgeShield AI doesn't just look at IP packets; it inspects the physical parameters inside the payload (infusion rates, ventilator pressure, sequence freshness). A packet might be syntactically valid Modbus, but if it tells a ventilator to exceed safe airway pressure, EdgeShield flags it as a cyber-physical invariant breach.
""")

    # ==========================================================================
    # SLIDE 9: Explainable AI & Privacy-Preserving Local SLM Architecture
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, 9, "Explainable AI & Privacy-Preserving Local SLM Architecture")

    # Diagram box across top
    flow_box = add_card(s9, 0.8, 1.6, 11.733, 2.1)
    tf_f = flow_box.text_frame
    tf_f.word_wrap = True
    p = tf_f.paragraphs[0]
    p.text = "DECOUPLED ASYNCHRONOUS EXPLAINABILITY WORKFLOW"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p_flow = tf_f.add_paragraph()
    p_flow.text = """
    Network Packet Ingest ──► ML Engine (< 1ms) ──► Alert Stored (Status: PENDING) ──► Stream to UI via WebSocket
                                     │
                                     ▼ (Dispatched Asynchronously in Background)
    AIEnrichmentService Worker ──► Ollama Local Daemon (Llama-3 / Phi-3) ──► Generates Clinical Explanation & Playbook
                                     │ (Fallback if Offline: Deterministic Rule Engine)
                                     ▼
    Database Alert Record Updated (Status: COMPLETED / UNAVAILABLE) ──► Broadcast Enrichment via WebSocket
    """
    p_flow.font.name = "Courier New"
    p_flow.font.size = Pt(9.5)
    p_flow.font.color.rgb = COLOR_TEXT_LIGHT
    p_flow.space_before = Pt(4)

    # 3 Detail Cards Below
    c1 = add_card(s9, 0.8, 3.9, 3.65, 3.0)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🔒 Privacy-Preserving SLMs"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE
    b1 = [
        "Runs Small Language Models (Ollama Llama-3 8B / Phi-3) completely offline on edge hardware.",
        "Zero Cloud Egress: Protects protected health information (PHI) and network topology maps.",
        "Full compliance with HIPAA Security Rule, HITECH, and EU GDPR requirements."
    ]
    for b in b1:
        pb = tf1.add_paragraph()
        pb.text = f"• {b}"
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = COLOR_TEXT_LIGHT
        pb.space_before = Pt(4)

    c2 = add_card(s9, 4.84, 3.9, 3.65, 3.0)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "📋 Structured Clinical Output"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE
    b2 = [
        "Clinical Explanation: Translates telemetry (e.g., 'entropy 7.8 on port 104') into plain English medical context.",
        "Operational Impact: Evaluates consequence (e.g., 'emergency surgery delayed due to locked CT scans').",
        "Actionable Mitigation: Delivers step-by-step containment instructions for biomedical engineers."
    ]
    for b in b2:
        pb = tf2.add_paragraph()
        pb.text = f"• {b}"
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = COLOR_TEXT_LIGHT
        pb.space_before = Pt(4)

    c3 = add_card(s9, 8.88, 3.9, 3.65, 3.0)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "⚖️ Strict Generative Boundary"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    b3 = [
        "GenAI NEVER makes classification decisions or triggers network blocking actions.",
        "Detection is 100% deterministic via the ML engine; GenAI functions strictly as an advisory analyst.",
        "Truthful Status Tracking: Alerts reflect COMPLETED (Ollama online), UNAVAILABLE (offline fallback), or FAILED."
    ]
    for b in b3:
        pb = tf3.add_paragraph()
        pb.text = f"• {b}"
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = COLOR_TEXT_LIGHT
        pb.space_before = Pt(4)

    set_notes(s9, """
Speaker Notes — Slide 9: Explainable AI & Local SLMs
• Why Generative AI in an IDS? Intrusion detection alerts are notoriously cryptic. An alert saying "Port 104 anomaly" means nothing to a floor nurse or biomedical tech. EdgeShield translates that into: "Siemens PACS workstation is receiving encrypted burst traffic consistent with DICOM Ransomware; CT scans may be locked; isolate workstation and notify radiology."
• Latency Decoupling: A critical architectural point is that the LLM is asynchronous. If the LLM takes 2 seconds to generate text, the network packet detection was already completed in 0.5 milliseconds. The edge detection pipeline is NEVER stalled.
• Privacy Compliance: Emphasize that hospitals CANNOT send network logs to external public APIs like ChatGPT because packets can contain patient names or medical record numbers. Running local SLMs via Ollama ensures complete data sovereignty.
• Crucial Boundary: Clarify that the LLM never blocks traffic. Security enforcement is strictly deterministic.
""")

    # ==========================================================================
    # SLIDE 10: Security Enforcement: Linux iptables vs. Development Simulation
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, 10, "Security Enforcement: Linux iptables vs. Development Simulation")

    # Mode 1: HostFirewallAdapter
    c1 = add_card(s10, 0.8, 1.6, 5.7, 5.3)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🐧 Linux Host Firewall Enforcement (Production)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    items_iptables = [
        ("Architecture", "Implemented via HostFirewallAdapter in firewall_service.py."),
        ("Kernel-Level Quarantine", "Injects deterministic DROP rules directly into Linux iptables/nftables FORWARD chain to block compromised medical IoT traffic."),
        ("Command Injection Prevention", "Strictly parses and sanitizes IP addresses using Python's ipaddress module before command generation."),
        ("Idempotency Verification", "Executes iptables -C FORWARD before rule insertion to verify whether the rule already exists, preventing duplicate rule accumulation."),
        ("Traceable Comment Tags", "Tags rules with unique comments: -m comment --comment edgeshield-isolated-<device_id> for deterministic removal."),
        ("Post-Condition Verification", "Executes automated post-insertion check; returns FAILED if rule is not actively verified in kernel state.")
    ]
    for title, desc in items_iptables:
        pt = tf1.add_paragraph()
        pt.text = f"• {title}: "
        pt.font.bold = True
        pt.font.size = Pt(10.5)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    # Mode 2: Simulation & Safety Interlocks
    c2 = add_card(s10, 6.83, 1.6, 5.7, 5.3)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "💻 Development Simulation & Safety Interlocks"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    items_sim = [
        ("SimulationEnforcementAdapter", "Default mode in development (macOS, Windows, testing). Transparently manages isolated device set in memory without altering OS networking."),
        ("Truthful Status Reporting", "Explicitly reports status: SIMULATED with message: 'No OS firewall rules were modified on darwin/windows'. Never falsely claims real isolation."),
        ("Clinical Safety Interlocks", "ClinicalSafetyInterlock database table and engine safeguards life-support devices (infusion pumps, ventilators) under cyber defense."),
        ("Fail-Safe Bedside Override", "Instead of abrupt power cutoff, interlock triggers safe state: LOCAL_BEDSIDE_OVERRIDE_LOCKED, requiring clinician manual verification."),
        ("Audit Trail Logging", "All isolation and reconnection events are cryptographically recorded in the AuditLog database table with timestamp, operator, and reason.")
    ]
    for title, desc in items_sim:
        pt = tf2.add_paragraph()
        pt.text = f"• {title}: "
        pt.font.bold = True
        pt.font.size = Pt(10.5)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    set_notes(s10, """
Speaker Notes — Slide 10: Security Enforcement
• Truth in Engineering: Address one of the most common flaws in student or prototype security projects: claiming that a database record update "isolates the device from the network." EdgeShield AI implements an explicit Adapter pattern.
• Linux Production Mode: In Linux deployment, `HostFirewallAdapter` executes real `iptables` commands with `-I FORWARD 1 -s <IP> -j DROP` and checks idempotency and post-verification.
• macOS / Development Simulation: On developer laptops or macOS, it uses `SimulationEnforcementAdapter`, which transparently returns `status: SIMULATED` and explicitly tells the UI that no host rules were changed.
• Clinical Interlocks: Explain the concept of safety interlocks. If an infusion pump is attacked while infusing epinephrine, you cannot simply sever the network or turn off the device—that could kill the patient. The system engages a safety interlock that locks the device into local manual bedside control mode so the clinician at the bedside can manage therapy safely.
""")

    # ==========================================================================
    # SLIDE 11: Clinical Monitoring Module: Motivation & MIMIC-IV Demo Cohort
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, 11, "Clinical Monitoring Module: Research Context & Cohort Audit")

    # 3 Summary Cards
    c1 = add_card(s11, 0.8, 1.6, 3.65, 5.3)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🎯 Clinical Research Objective"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT
    pts1 = [
        "Investigate the technical feasibility of predicting post-24h in-hospital mortality using non-invasive bedside vital signs.",
        "Demonstrate an audited, zero-leakage clinical data engineering pipeline.",
        "Provide a benchmark baseline model (L2 Logistic Regression vs Random Forest).",
        "Deliver clear clinical disclaimers distinguishing exploratory risk estimates from certified diagnostic devices."
    ]
    for pt in pts1:
        p_ = tf1.add_paragraph()
        p_.text = f"• {pt}"
        p_.font.size = Pt(10.5)
        p_.font.color.rgb = COLOR_TEXT_LIGHT
        p_.space_before = Pt(8)

    c2 = add_card(s11, 4.84, 1.6, 3.65, 5.3)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "📊 MIMIC-IV Demo 2.2 Cohort"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    pts2 = [
        "Source: Beth Israel Deaconess Medical Center critical care database (Demo 2.2 release).",
        "Raw Dataset Scope: 140 ICU stays across 100 unique patients.",
        "Linkage Audit: Verified against admissions.csv.gz using many-to-one join on (subject_id, hadm_id).",
        "Outcome Coverage: 140 out of 140 stays linked to hospital outcomes with exactly 0 missing labels."
    ]
    for pt in pts2:
        p_ = tf2.add_paragraph()
        p_.text = f"• {pt}"
        p_.font.size = Pt(10.5)
        p_.font.color.rgb = COLOR_TEXT_LIGHT
        p_.space_before = Pt(8)

    c3 = add_card(s11, 8.88, 1.6, 3.65, 5.3)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "🔍 Patient Units vs Stays"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    pts3 = [
        "Critical Distinction: An ICU stay is not an independent patient.",
        "Repeated Admissions: 26 patients in the cohort experienced multiple ICU stays (up to 5 stays per patient).",
        "Mixed Outcomes: 4 patients experienced multiple admissions spanning both survival and mortality outcomes.",
        "Sample Size Reality: The small cohort serves to prove pipeline integrity and methodology, not clinical predictive power."
    ]
    for pt in pts3:
        p_ = tf3.add_paragraph()
        p_.text = f"• {pt}"
        p_.font.size = Pt(10.5)
        p_.font.color.rgb = COLOR_TEXT_LIGHT
        p_.space_before = Pt(8)

    set_notes(s11, """
Speaker Notes — Slide 11: Clinical Research Motivation & Cohort
• Context Shift: We now examine the second major module: the patient vital-sign monitoring and mortality risk research pipeline.
• MIMIC-IV Demo 2.2: Clarify that the demo cohort is a small, publicly accessible subset of MIMIC-IV containing 100 patients and 140 ICU stays.
• Patient vs Stay: Emphasize this statistical distinction. An ICU stay is an episode of care, but a single patient can be admitted multiple times. If an ML engineer treats each stay as independent, information from the patient will leak across partitions.
• Research Purpose: Reiterate that this module is intended to demonstrate a reproducible, leakage-free data science pipeline. It is not large enough to train a production-grade diagnostic algorithm.
""")

    # ==========================================================================
    # SLIDE 12: Prospective Cohort Eligibility Audit & Leakage Elimination
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, 12, "Prospective Cohort Eligibility Audit & Leakage Elimination")

    # Table of Exclusions
    t_box = add_card(s12, 0.8, 1.6, 11.733, 5.3)
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p = tf_t.paragraphs[0]
    p.text = "COHORT ELIGIBILITY AUDIT TRAIL (Total Stays: 140 ──► Excluded: 4 ──► Eligible: 136)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p_sub = tf_t.add_paragraph()
    p_sub.text = "Prospective prediction requires all evaluated patients to be alive and present in the ICU at the prediction point (ICU intime + 24.0h)."
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = COLOR_TEXT_LIGHT
    p_sub.space_before = Pt(4)

    # Breakdown grid
    ex_text = [
        ("Stay 36871784 (Subject 10017492)", "ICU in: 2116-07-05 06:50 | Death: 2116-07-05 08:05", "Died at 1.25 hours after ICU admission", "EXCLUDED: Death occurred before 24h prediction point"),
        ("Stay 38275267 (Subject 10025463)", "ICU in: 2137-10-09 02:51 | Death: 2137-10-09 15:30", "Died at 12.64 hours after ICU admission", "EXCLUDED: Death occurred before 24h prediction point"),
        ("Stay 32554129 (Subject 10020187)", "ICU in: 2170-02-24 18:18 | Disch: 2170-02-25 15:00", "Discharged alive at 20.69 hours after admission", "EXCLUDED: Acute stay terminated before 24h window closed"),
        ("Stay 30864406 (Subject 10026406)", "ICU in: 2129-01-05 02:37 | Disch: 2129-01-05 14:10", "Discharged alive at 11.54 hours after admission", "EXCLUDED: Acute stay terminated before 24h window closed")
    ]
    for stay, times, dur, reason in ex_text:
        pt = tf_t.add_paragraph()
        pt.text = f"• {stay}: {reason}"
        pt.font.bold = True
        pt.font.size = Pt(10.5)
        pt.font.color.rgb = COLOR_ROSE
        pt.space_before = Pt(6)
        pd = tf_t.add_paragraph()
        pd.text = f"   {times} ({dur})"
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    # Final Summary inside box
    p_sum = tf_t.add_paragraph()
    p_sum.text = """
    FINAL VERIFIED ELIGIBLE COHORT METRICS:
    • Eligible ICU Stays: 136 (18 Deaths, 118 Survivors | Mortality Prevalence: 13.24%)
    • Eligible Unique Patients: 98 (14 Deaths, 88 Survivors | 4 patients with mixed outcomes)
    • Core Vital Coverage: 100.0% (all 136 stays have recorded Heart Rate, Respiratory Rate, and SpO2)
    • Zero Target Leakage: 0 future outcomes or post-24h event flags present in feature matrix.
    """
    p_sum.font.size = Pt(10.5)
    p_sum.font.color.rgb = COLOR_MINT
    p_sum.space_before = Pt(10)

    set_notes(s12, """
Speaker Notes — Slide 12: Eligibility Audit & Leakage Elimination
• Methodological Rigor: Explain why these 4 exclusions are required.
• Pre-Prediction Deaths: If a patient dies at hour 12 of their ICU stay, you cannot predict their post-24h mortality at hour 24 because they are already dead. Including them causes severe retrospective target leakage.
• Pre-Prediction Discharges: If a patient is discharged alive from the hospital at hour 15, they are no longer in the acute care setting at hour 24.
• Final Eligible Numbers: 136 stays across 98 patients, with 18 mortality events. Note that these 18 deaths correspond to only 14 unique deceased individuals because some patients had repeated admissions.
• Complete Audit Trail: The repository contains `exclusions_report.md` and `cohort_audit_summary.json` documenting every stay ID and timestamp.
""")

    # ==========================================================================
    # SLIDE 13: 24-Hour Observation Window & 69-Feature Engineering Schema
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, 13, "24-Hour Observation Window & 69-Feature Engineering Schema")

    # Left: Window Definition & 7 Vitals
    c1 = add_card(s13, 0.8, 1.6, 5.7, 5.3)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "⏱️ Observation Window & Core Vitals"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p_w = tf1.add_paragraph()
    p_w.text = "Strict Half-Open Interval: [t_intime, t_intime + 24.0 hours)\nEnforces charttime < prediction_time. 3 boundary measurements recorded at exactly t = 24.0h were audited and excluded to ensure strict prospective isolation. Over 50,400 post-24h chart events safely excluded."
    p_w.font.size = Pt(10)
    p_w.font.color.rgb = COLOR_TEXT_LIGHT
    p_w.space_before = Pt(4)

    p_v = tf1.add_paragraph()
    p_v.text = "The 7 Core Vital Signs Monitored:"
    p_v.font.bold = True
    p_v.font.size = Pt(11)
    p_v.font.color.rgb = COLOR_TEXT_WHITE
    p_v.space_before = Pt(8)

    v_list = [
        ("Heart Rate", "20 - 260 bpm", "Tachycardia / Bradycardia trends"),
        ("Respiratory Rate", "0 - 70 insp/min", "Tachypnea / Apneic arrest flags"),
        ("Oxygen Saturation (SpO2)", "50 - 100 %", "Hypoxemic episodes (< 70% flagged)"),
        ("Systolic Blood Pressure", "40 - 280 mmHg", "Hypotension / Shock indicator"),
        ("Diastolic Blood Pressure", "20 - 180 mmHg", "Perfusion pressure"),
        ("Mean Arterial Pressure (MAP)", "25 - 200 mmHg", "Critical perfusion marker"),
        ("Body Temperature (°C)", "30.0 - 43.5 °C", "Converted from °F; hypothermia/pyrexia")
    ]
    for v_name, bounds, clinical in v_list:
        pv = tf1.add_paragraph()
        pv.text = f"• {v_name} ({bounds}): {clinical}"
        pv.font.size = Pt(9.5)
        pv.font.color.rgb = COLOR_TEXT_LIGHT
        pv.space_before = Pt(3)

    # Right: 69 Features Breakdown
    c2 = add_card(s13, 6.83, 1.6, 5.7, 5.3)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "📐 69 Engineered Features Breakdown"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT

    p_sub2 = tf2.add_paragraph()
    p_sub2.text = "Total Features: 63 Vital Features + 6 Observation Indicators = 69 Features"
    p_sub2.font.size = Pt(10)
    p_sub2.font.color.rgb = COLOR_TEXT_WHITE
    p_sub2.space_before = Pt(4)

    stats = [
        ("1. count", "Number of distinct chart recordings in 24h"),
        ("2. is_missing", "Binary flag indicating complete absence of vital sign"),
        ("3. recent", "Most recent observation value within the 24h window"),
        ("4. mean", "Arithmetic mean across all valid measurements in window"),
        ("5. min", "Minimum recorded observation value in window"),
        ("6. max", "Maximum recorded observation value in window"),
        ("7. std", "Sample standard deviation (0.0 if count <= 1)"),
        ("8. time_since_last_h", "Hours elapsed between most recent vital and hour 24"),
        ("9. trend_late_minus_early", "Mean of hours 12–24 minus mean of hours 0–12")
    ]
    for s_name, s_desc in stats:
        ps = tf2.add_paragraph()
        ps.text = f"• {s_name}: {s_desc}"
        ps.font.size = Pt(9)
        ps.font.color.rgb = COLOR_TEXT_LIGHT
        ps.space_before = Pt(2)

    p_extra = tf2.add_paragraph()
    p_extra.text = "\n6 General Observation & Screening Features:\n• flag_zero_value_count, flag_low_spo2_count, flag_extreme_hr_count\n• total_flagged_observations, distinct_monitored_hours, total_vital_measurements"
    p_extra.font.size = Pt(9.5)
    p_extra.font.color.rgb = COLOR_AMBER
    p_extra.space_before = Pt(4)

    set_notes(s13, """
Speaker Notes — Slide 13: Features & Temporal Definition
• Precise Temporal Window: Explain that the observation interval $[t_{\text{intime}}, t_{\text{intime}} + 24\text{h})$ is half-open. Measurements recorded exactly at $t=24.0\text{h}$ are excluded so that no information at or after the prediction boundary enters the feature vectors.
• 7 Vital Signs $\times$ 9 Statistical Metrics = 63 Features: For each vital sign, we calculate count, missingness, recent value, mean, min, max, standard deviation, latency to hour 24, and the trajectory trend (late 12 hours minus early 12 hours).
• 6 General Quality Features: Track overall monitoring density and clinical screening flags (zero values, severe hypoxemia < 70%, extreme heart rates). Total = 69 features.
• Feature Schema Verification: The model artifact strictly validates this 69-feature schema on every API request.
""")

    # ==========================================================================
    # SLIDE 14: Machine Learning Pipeline: Preprocessing Isolation & Grouped Splits
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, 14, "Machine Learning Pipeline: Preprocessing Isolation & Grouped Splits")

    # 4 Sequential Cards
    steps = [
        ("Step 1: Patient Grouping", "Enforced GroupShuffleSplit on subject_id (75% Train / 25% Test; seed=42).\n• Train: 101 stays across 73 unique patients (13 deaths).\n• Test: 35 stays across 25 unique patients (5 deaths).\n• Zero patient overlap: assert len(set(train_patients).intersection(test_patients)) == 0.", COLOR_TEAL),
        ("Step 2: Preprocessing Isolation", "Median imputation and standard scaling are wrapped inside sklearn.pipeline.Pipeline.\n• SimpleImputer(strategy='median') fit strictly on training fold.\n• StandardScaler() fit strictly on training fold.\n• Zero testing statistics leak into preprocessing transformations.", COLOR_MINT),
        ("Step 3: Baseline Model Architectures", "1. Majority-Class DummyClassifier (predicts prior class distribution).\n2. Regularized Logistic Regression (L2 penalty, C=0.1, balanced weights, lbfgs solver).\n3. Constrained Random Forest (50 trees, max depth 3, balanced class weights).", COLOR_INDIGO),
        ("Step 4: Grouped Cross-Validation", "Executed 5-fold GroupKFold cross-validation across all 136 stays.\n• Every fold preserves patient independence.\n• Every fold contains positive mortality cases (Fold 0: 3, Fold 1: 2, Fold 2: 6, Fold 3: 3, Fold 4: 4).\n• Evaluates out-of-fold generalization.", COLOR_AMBER)
    ]

    for i, (title, desc, accent) in enumerate(steps):
        x = 0.8 + i * 2.98
        card = add_card(s14, x, 1.6, 2.78, 5.3)
        tf = card.text_frame
        tf.word_wrap = True
        
        p_num = tf.paragraphs[0]
        p_num.text = f"PHASE {i+1}"
        p_num.font.name = FONT_HEADING
        p_num.font.size = Pt(14)
        p_num.font.bold = True
        p_num.font.color.rgb = accent

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_WHITE
        p_t.space_before = Pt(6)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = COLOR_TEXT_LIGHT
        p_d.space_before = Pt(10)

    set_notes(s14, """
Speaker Notes — Slide 14: ML Pipeline & Preprocessing Isolation
• Leakage Elimination: Reiterate the two major leakage prevention steps:
  1. Grouped Partitioning: Grouping on `subject_id` ensures that if Patient X was admitted three times, all three stays reside in the training split (or all in test). None are split across.
  2. Isolated Preprocessing: If you compute the median or standard deviation of the entire dataset before splitting, you leak test distribution info into training. By using `sklearn.pipeline.Pipeline`, the `SimpleImputer` and `StandardScaler` are fitted strictly on `X_train`.
• Model Selection Rationale: In high-dimensional, small-sample regimes (69 features for 101 training stays), complex models overfit instantly. Constrained L2 Logistic Regression with high regularization ($C=0.1$) and low-depth Random Forest (depth 3) are appropriate exploratory baselines.
""")

    # ==========================================================================
    # SLIDE 15: Model Evaluation Results: Comparative Benchmark & Uncertainty Analysis
    # ==========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, 15, "Model Evaluation Results & Scientific Discrepancy Resolution")

    # Table Card
    t_card = add_card(s15, 0.8, 1.6, 11.733, 2.9)
    tf_t = t_card.text_frame
    tf_t.word_wrap = True
    p = tf_t.paragraphs[0]
    p.text = "HELD-OUT TEST SET EVALUATION (N=35 stays, 25 patients, 5 deaths)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    # Table for metrics
    # Row headers
    metrics_table = [
        ("Metric", "Majority-Class Baseline", "L2 Logistic Regression (C=0.1)", "Constrained Random Forest (depth=3)"),
        ("Accuracy", "85.71%", "82.86%", "91.43%"),
        ("Sensitivity (Recall)", "0.00%", "60.00% (3 / 5)", "60.00% (3 / 5)"),
        ("Specificity", "100.00%", "86.67% (26 / 30)", "96.67% (29 / 30)"),
        ("Precision", "0.00%", "42.86% (3 / 7)", "75.00% (3 / 4)"),
        ("ROC-AUC", "0.5000", "0.7600 (was 0.7533 pre-hardening)", "0.7667"),
        ("PR-AUC", "0.1429", "0.6160 (was 0.6151 pre-hardening)", "0.4894"),
        ("Brier Score Loss", "0.1226", "0.1268", "0.1395"),
        ("Confusion Matrix", "TN: 30, FP: 0, FN: 5, TP: 0", "TN: 26, FP: 4, FN: 2, TP: 3", "TN: 29, FP: 1, FN: 2, TP: 3")
    ]
    
    # We will format as clean formatted text blocks in the card
    text_content = ""
    for row in metrics_table:
        text_content += f"{row[0]:<22} | {row[1]:<24} | {row[2]:<35} | {row[3]:<32}\n"
    
    p_code = tf_t.add_paragraph()
    p_code.text = text_content
    p_code.font.name = "Courier New"
    p_code.font.size = Pt(8.5)
    p_code.font.color.rgb = COLOR_TEXT_LIGHT
    p_code.space_before = Pt(4)

    # Discrepancy Analysis Card Below
    disc_card = add_card(s15, 0.8, 4.65, 11.733, 2.25)
    tf_d = disc_card.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "🔬 Scientific Discrepancy Resolution & Bootstrap Uncertainty Audit"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    analysis_bullets = [
        ("Disparity with Grouped Cross-Validation", "5-fold grouped out-of-fold ROC-AUC across all 136 stays is 0.5325 (PR-AUC: 0.3083, sensitivity: 33.33%, specificity: 81.36%, accuracy: 75.00%). Mean fold ROC-AUC: 0.5540 ± 0.1064."),
        ("Small-Sample Volatility Cause", "The held-out test split contains only 5 positive deaths. Misclassifying a single patient swings sensitivity by 20.0 percentage points."),
        ("Wide 95% Bootstrap Confidence Interval", "Resampling audit reveals the test ROC-AUC 95% bootstrap CI is [0.3120, 1.0000] (spanning 68.8 percentage points), fully enclosing the 0.5325 cross-validation score."),
        ("Scientific Conclusion", "The single held-out test score (0.76) is subject to high sampling noise on N=5 events. The grouped cross-validation score (~0.53–0.55) reflects true expected baseline vital-sign predictive ability on this demo cohort.")
    ]
    for title, desc in analysis_bullets:
        pb = tf_d.add_paragraph()
        pb.text = f"• {title}: {desc}"
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = COLOR_TEXT_LIGHT
        pb.space_before = Pt(3)

    set_notes(s15, """
Speaker Notes — Slide 15: Evaluation Results & Discrepancy
• Walk Through the Table: Review the metrics. Both L2 Logistic Regression and Random Forest achieved 60% test recall (3 out of 5 deaths identified). Random Forest had higher accuracy (91.4%) and precision (75%), but this is driven by high specificity on the majority class.
• The Crucial Discrepancy Question: Anticipate this inevitable reviewer question: "Why did test ROC-AUC reach 0.76 while 5-fold grouped CV out-of-fold ROC-AUC was only 0.53?"
• The Exact Scientific Answer: The test set has only 5 positive events. In such small samples, high test scores are driven by random favorable split partitioning. The bootstrap 95% confidence interval spans from 0.312 to 1.000—meaning the true test performance is statistically indistinguishable from chance (0.50) or cross-validation (0.53).
• Honesty Takeaway: EdgeShield AI explicitly documents this discrepancy rather than hiding the CV score or claiming clinical generalizability.
""")

    # ==========================================================================
    # SLIDE 16: Full-Stack Implementation: FastAPI Backend & React 18 Dashboard
    # ==========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, 16, "Full-Stack Implementation: FastAPI Backend & React 18 Dashboard")

    # Left: FastAPI Endpoints & Validation
    c1 = add_card(s16, 0.8, 1.6, 5.7, 5.3)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "⚡ FastAPI Clinical & Security Endpoints"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    routes = [
        ("GET /health", "Returns service status, UTC timestamp, and module health (intrusion_detection: ONLINE, patient_monitoring: ONLINE)."),
        ("GET /api/v1/patient-monitoring/status", "Reports model artifact status (baseline_model.joblib), loaded schema version, and research mode."),
        ("POST /api/v1/patient-monitoring/validate-vitals", "Physiological range screening, °F to °C conversion, and flags zero values, hypoxemia, or extreme heart rates."),
        ("POST /api/v1/patient-monitoring/assess-risk", "Produces experimental in-hospital mortality risk estimate with category (LOW / ELEVATED / HIGH) & mandatory disclaimers."),
        ("POST /api/v1/patient-monitoring/predict", "Standardized clinical prediction validating 69-feature vector schema. Rejects NaN, Inf, and unexpected keys with HTTP 422."),
        ("GET /api/v1/patient-monitoring/cohort-summary", "Returns verified MIMIC-IV Demo cohort metrics (136 eligible stays, 18 deaths, 0 leakage)."),
        ("GET /api/v1/patient-monitoring/sample-records", "Serves 3 demonstration cases from MIMIC-IV Demo (Stays 31269608, 38559363, 39543480).")
    ]
    for ep, desc in routes:
        pt = tf1.add_paragraph()
        pt.text = f"• {ep}"
        pt.font.bold = True
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(4)
        pd = tf1.add_paragraph()
        pd.text = f"   {desc}"
        pd.font.size = Pt(9)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    # Right: React 18 Patient Monitoring View
    c2 = add_card(s16, 6.83, 1.6, 5.7, 5.3)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🖥️ React 18 Patient Vitals & Risk UI Component"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT

    ui_features = [
        ("Demonstration Case Selector", "Pre-loads real MIMIC-IV Demo records (Patient A: Stable Floor, Patient B: Tachycardic, Patient C: Critical Hypotensive/Hypoxemic)."),
        ("Interactive Vital Input & Unit Switching", "Input fields for HR, RR, SpO2, SBP, DBP, and Body Temperature with dynamic °C / °F switching and normal range cues."),
        ("Real-Time Data Quality Screening", "Renders review badges: review_zero_value, review_low_spo2, review_extreme_heart_rate and displays missing measurements handled by median imputer."),
        ("Visual Prediction Separation", "Clinical risk probability is strictly separated from observed vital cards into a dedicated Risk Card with risk categories (LOW, ELEVATED, HIGH)."),
        ("Permanent Research Disclaimer Banner", "Prominent amber disclaimer visible at top of view: clearly states that the model is for research verification and NOT an FDA diagnostic tool.")
    ]
    for title, desc in ui_features:
        pt = tf2.add_paragraph()
        pt.text = f"▶ {title}"
        pt.font.bold = True
        pt.font.size = Pt(10.5)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(5)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    set_notes(s16, """
Speaker Notes — Slide 16: Full-Stack Implementation
• API Reliability: The backend API implements robust defensive engineering. Notice the sanitization: non-finite values (like `NaN` or `Infinity`), negative vitals (e.g. negative SpO2), or unknown feature keys are rejected with HTTP 422 Unprocessable Entity.
• Graceful Fallback: If `baseline_model.joblib` is missing or corrupted, the service does not crash; it returns risk score `INDETERMINATE` with a clear explanation.
• Frontend Design in React: `PatientMonitoringView.tsx` incorporates demonstration case buttons pre-loaded with MIMIC-IV records so evaluators can test stable, elevated, and critical cases with a single click.
• Visual Clarity: The UI visually separates raw measurements from model predictions so users never confuse observed physiological signs with algorithmic predictions.
""")

    # ==========================================================================
    # SLIDE 17: Engineering Verification: 77 Automated Tests & Production Build
    # ==========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, 17, "Engineering Verification: 77 Automated Tests & Production Build")

    # Left: Pytest Summary
    c1 = add_card(s17, 0.8, 1.6, 5.7, 5.3)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🧪 Backend Automated Test Suite: 77 Passed, 0 Failed"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    test_modules = [
        ("test_patient_monitoring.py (28 Tests)", "Validates prospective cohort exclusions, 0 temporal leakage, 0 patient overlap, NaN/Inf rejection, °F to °C conversion, quality flags, and missing artifact graceful fallbacks."),
        ("test_security_and_enforcement.py (17 Tests)", "Tests Linux iptables command generation, idempotency -C check, SimulationEnforcementAdapter status, and ClinicalSafetyInterlock state transitions."),
        ("test_canonical_pipeline.py (14 Tests)", "Verifies end-to-end edge packet ingestion, rolling incident correlation, 60s flow aggregation, and latency tracking collector."),
        ("test_machine_signals.py (7 Tests)", "Verifies physical invariant breaches (bolus overdose, ventilator pressure hijack), anti-replay sequence checks, and socket collectors."),
        ("test_documents_and_copilot.py (7 Tests)", "Tests PDF document RAG search, multi-context AI copilot (5 contexts), and citation generation."),
        ("test_api.py (4 Tests)", "Validates GET /health, OpenAPI schema generation, and CORS preflight headers.")
    ]
    for mod, desc in test_modules:
        pt = tf1.add_paragraph()
        pt.text = f"• {mod}"
        pt.font.bold = True
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(4)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    # Right: Frontend Production Build
    c2 = add_card(s17, 6.83, 1.6, 5.7, 5.3)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "📦 Frontend Production Build & Integration Audit"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    build_metrics = [
        ("TypeScript Compiler (tsc)", "0 TypeScript compilation errors. All frontend interfaces strictly typed to Pydantic schemas."),
        ("Vite Production Bundler", "Successfully bundled 2,669 modules in 1.28 seconds."),
        ("Production Assets Generated", "dist/index.html (0.96 kB)\ndist/assets/index.css (44.60 kB | gzip: 7.77 kB)\ndist/assets/index.js (860.00 kB | gzip: 236.13 kB)"),
        ("Live API Integration Audit", "Verified live HTTP 200 responses on /health, /api/v1/devices, /alerts, /signals, and /patient-monitoring."),
        ("Timezone & Modernization Audit", "Modernized datetime.utcnow() to datetime.now(timezone.utc) across all services, ensuring compatibility with modern Python 3.12+ / 3.14.")
    ]
    for title, desc in build_metrics:
        pt = tf2.add_paragraph()
        pt.text = f"▶ {title}"
        pt.font.bold = True
        pt.font.size = Pt(10.5)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(5)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    set_notes(s17, """
Speaker Notes — Slide 17: Engineering Verification
• Test Coverage: 77 tests were executed with pytest inside `backend/` and achieved 100% pass rate (0 failures).
• Key Test Highlights:
  - Prospective Cohort: Tests verify that Stays 36871784 and 38275267 (deaths <= 24h) and Stays 32554129 and 30864406 (discharges <= 24h) are strictly excluded.
  - Leakage Protection: Tests verify 0 patient overlap between training and testing sets.
  - Robust Error Handling: Tests verify that corrupted model files or missing folders do not cause server 500 errors, but cleanly transition to `INDETERMINATE`.
• Frontend Build: `tsc && vite build` bundled 2,669 modules with zero TypeScript errors. This demonstrates production readiness of the code artifacts.
""")

    # ==========================================================================
    # SLIDE 18: Critical Limitations, Ethical Considerations & Clinical Disclaimers
    # ==========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18)
    add_header(s18, 18, "Critical Limitations, Ethical Considerations & Clinical Disclaimers")

    # 3 Warning Containers
    c1 = add_card(s18, 0.8, 1.6, 3.65, 5.3)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "⚠️ Statistical & Dataset Limitations"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    l1 = [
        "Small Positive Sample Size: Only 14 unique deceased patients (18 stays) in the entire eligible demo cohort.",
        "High Metric Volatility: Single misclassifications swing test recall by 20.0 percentage points.",
        "Wide Confidence Intervals: 95% bootstrap CI for test ROC-AUC is [0.312, 1.000], indicating extreme estimation uncertainty.",
        "Vital-Signs Only: Models lack laboratory values (lactate, arterial blood gases), ventilation parameters, and vasopressor infusions."
    ]
    for l in l1:
        pl = tf1.add_paragraph()
        pl.text = f"• {l}"
        pl.font.size = Pt(10)
        pl.font.color.rgb = COLOR_TEXT_LIGHT
        pl.space_before = Pt(6)

    c2 = add_card(s18, 4.84, 1.6, 3.65, 5.3)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "⚖️ Mandatory Clinical Disclaimer"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE
    l2 = [
        "NOT an FDA-Cleared Medical Device: EdgeShield AI has not been evaluated, cleared, or approved by the US FDA or CE notified bodies.",
        "Exploratory Engineering Prototype: Built solely for technical demonstration, pipeline verification, and research methodology proof.",
        "NEVER for Patient Care: The risk estimates must NEVER be used for bedside triage, patient diagnosis, clinical intervention, or clinical decision-making.",
        "Permanently Disclaimed in Software: Displayed in API metadata, JSON responses, and permanently rendered on the React UI banner."
    ]
    for l in l2:
        pl = tf2.add_paragraph()
        pl.text = f"• {l}"
        pl.font.size = Pt(10)
        pl.font.color.rgb = COLOR_TEXT_LIGHT
        pl.space_before = Pt(6)

    c3 = add_card(s18, 8.88, 1.6, 3.65, 5.3)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "🛡️ Cybersecurity Ethical Guardrails"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    l3 = [
        "No Autonomous Disconnection: Life-support machines are protected by Clinical Safety Interlocks preventing catastrophic therapy cutoffs.",
        "Advisory GenAI Boundary: Local LLMs strictly explain alerts and suggest triage playbooks; they never make blocking decisions.",
        "Privacy & Sovereignty: All AI inference runs locally without cloud transmission, preventing data breaches of patient telemetry.",
        "Auditability: Every administrative and containment action is logged with operator identification in SQLite audit trails."
    ]
    for l in l3:
        pl = tf3.add_paragraph()
        pl.text = f"• {l}"
        pl.font.size = Pt(10)
        pl.font.color.rgb = COLOR_TEXT_LIGHT
        pl.space_before = Pt(6)

    set_notes(s18, """
Speaker Notes — Slide 18: Limitations & Ethical Disclaimers
• Transparency as a Strength: Emphasize that in biomedical engineering and clinical informatics, recognizing limitations is the hallmark of serious scientific work.
• Sample Size Reality: Reiterate that 14 deceased patients cannot produce a production model. The confidence intervals are wide ($[0.312, 1.000]$), which is why we frame the model strictly as an exploratory baseline.
• Regulatory Clearances: Medical software intended to predict mortality in hospitals requires rigorous clinical trials, Software as a Medical Device (SaMD) documentation, and FDA 510(k) or De Novo clearance. EdgeShield AI makes zero claims of clinical deployment.
• Ethical Safeguards: Point out that autonomous systems in hospitals must always incorporate fail-safe mechanisms—interlocks that prioritize patient life over pure network isolation.
""")

    # ==========================================================================
    # SLIDE 19: Future Scope & Conclusion
    # ==========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19)
    add_header(s19, 19, "Future Scope & Conclusion")

    # Left: Future Scope
    c1 = add_card(s19, 0.8, 1.6, 5.7, 5.3)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🚀 Future Research & Engineering Roadmap"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    future_items = [
        ("Full-Scale Clinical Cohort Training", "Scale pipeline from MIMIC-IV Demo to full MIMIC-IV (over 70,000 ICU stays) and external eICU Collaborative Research Database."),
        ("Multimodal Clinical Covariates", "Incorporate continuous arterial lines, blood gas laboratory values (lactate, pH), medications (vasopressors), and clinical text notes."),
        ("Temporal Deep Learning Models", "Investigate Transformer-based and recurrent architectures (LSTM, Temporal Convolutional Networks) for dynamic hourly deterioration tracking."),
        ("Physical Hardware Edge Testing", "Benchmark inference latency and thermal profiles on physical NVIDIA Jetson Orin Nano and industrial medical edge gateways."),
        ("Hospital Cyber-Range Evaluation", "Connect collector interfaces to hardware-in-the-loop medical testbeds to evaluate live multi-stage ransomware and protocol injection attacks.")
    ]
    for title, desc in future_items:
        pt = tf1.add_paragraph()
        pt.text = f"▶ {title}"
        pt.font.bold = True
        pt.font.size = Pt(10.5)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(5)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    # Right: Conclusion
    c2 = add_card(s19, 6.83, 1.6, 5.7, 5.3)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🏁 Conclusion & Key Engineering Achievements"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MINT

    conclusions = [
        ("Modular Dual-Pipeline Architecture", "Demonstrated that healthcare IoT environments can benefit from decoupled edge intrusion detection and clinical vital monitoring on a unified platform."),
        ("Sub-Millisecond Edge Security", "Achieved real-time packet anomaly scoring with physical invariant validation, safe iptables enforcement, and offline GenAI triage."),
        ("Audited Zero-Leakage Clinical Science", "Established a strictly prospective 24-hour ICU observation window, verified 69 clinical features, and proved patient-grouped evaluation integrity on MIMIC-IV Demo."),
        ("Production-Ready Software Quality", "Verified with 77 passed backend tests (0 failures), 0 build errors in Vite, and robust Pydantic/FastAPI defensive input validation."),
        ("Scientific Integrity & Honesty", "Transparently resolved performance discrepancies and wide bootstrap confidence intervals without making unsupported clinical claims.")
    ]
    for title, desc in conclusions:
        pt = tf2.add_paragraph()
        pt.text = f"✓ {title}"
        pt.font.bold = True
        pt.font.size = Pt(10.5)
        pt.font.color.rgb = COLOR_TEXT_WHITE
        pt.space_before = Pt(5)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = COLOR_TEXT_LIGHT

    set_notes(s19, """
Speaker Notes — Slide 19: Future Scope & Conclusion
• Summarize the Technical Journey: Conclude by reiterating the core value proposition of EdgeShield AI.
• Future Directions: Mention that moving from the 100-patient MIMIC-IV Demo to the full 70,000-stay MIMIC-IV dataset and adding laboratory variables (lactate, arterial blood gas) will allow training deep sequence models with clinical statistical power.
• Hardware Edge Deployment: Highlight the next step of testing on physical NVIDIA Jetson and edge gateway appliances in a medical cyber-range testbed.
• Final Conclusion: EdgeShield AI successfully bridges the gap between low-latency IoT cybersecurity and leak-free critical care clinical informatics, supported by verified software engineering and scientific honesty.
• Invite Questions: Open the floor to questions from reviewers.
""")

    prs.save(PPTX_PATH)
    print(f"[+] Successfully generated PowerPoint deck at: {PPTX_PATH}")


if __name__ == "__main__":
    create_deck()
