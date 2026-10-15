# EdgeShield AI: Edge-Based Intrusion Detection & Clinical Telemetry Monitoring for Smart Healthcare IoT

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.143.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6.svg)](https://www.typescriptlang.org/)
[![Status: Project Complete](https://img.shields.io/badge/Status-Project%20Complete%20%26%20Verified-emerald.svg)](#final-project-completion--verification-status)
[![Tests: 90 Passed](https://img.shields.io/badge/Tests-90%20Passed%20%2F%200%20Failed-brightgreen.svg)](#automated-test-suite--verification)

> **Project Scope**: Privacy-Preserving, Low-Latency Edge Intrusion Detection, Cyber-Physical Safety Interlocks, Empirical Benchmark Evaluation on Real Cybersecurity Data (Edge-IIoTset), and Prospective Clinical Monitoring Research (MIMIC-IV) for Smart Healthcare IoT.

---

## 🏥 Executive Project Vision

In life-critical hospital environments—where infusion pumps, ICU patient monitors, mechanical ventilators, and DICOM radiology workstations operate continuously—cryptic cybersecurity alerts cause cognitive fatigue and critical response delays. Furthermore, network security cannot be detached from clinical patient context: isolating a device delivering life-critical therapy requires specialized safety interlocks to prevent fatal treatment interruptions.

**EdgeShield AI** provides an integrated edge architecture featuring two strictly decoupled, specialized pipelines:
1. **Pipeline A: IoMT Cybersecurity & Intrusion Detection (IDS)**
   - Ingests multi-protocol network telemetry (Modbus/TCP, MQTT, DICOM, HL7).
   - Evaluated on real **Edge-IIoTset** benchmark data (157,800 records) across 29 genuine protocol features (Configuration B) with zero testbed IP/port leakage.
   - Dual-stage machine learning detection: Supervised threat classification (Random Forest, XGBoost, Decision Tree, Logistic Regression) + Unsupervised novelty detection (Isolation Forest).
   - Dispatches asynchronous explainable AI triaging without blocking line-rate edge packet inspection (<5ms).
   - Enforces host firewall quarantine with cyber-physical safety interlocks that safeguard life-support equipment.
2. **Pipeline B: Clinical Vital-Sign Monitoring & Mortality Risk Research**
   - Ingests physiological vital signs from ICU admissions (MIMIC-IV Clinical Database Demo v2.2, 136 eligible stays).
   - Enforces a prospective 24-hour observation window with zero temporal leakage.
   - Evaluates exploratory hospital mortality risk baselines with patient-level grouped cross-validation and explicit uncertainty reporting.

---

## ⚡ Architectural Pipelines

```
[ PIPELINE A: IoMT CYBERSECURITY IDS (EDGE-IIoTSET BENCHMARK) ]
Medical IoT Packet Stream (DICOM / MQTT / Modbus / TCP / UDP / ICMP)
                       │
                       ▼
         Stage 1: Isolation Forest (Unsupervised Anomaly Detection)
                       │
                       ▼
         Stage 2: Supervised Multi-Class Threat Classifier (Random Forest / XGBoost)
                       │
                       ▼
         Asynchronous Local LLM / RAG over PDF Device Manuals
                       │
                       ▼
 ┌───────────────────────────────────────────────────────────┐
 │ Human-Understandable Clinical Impact Assessment           │
 │ Cyber-Physical Safety Interlock Evaluation                │
 │ Actionable Remediation Playbook                           │
 └───────────────────────────────────────────────────────────┘
                       │
                       ▼
   Edge Firewall Adapter (Linux iptables / Simulation Mode)


[ PIPELINE B: CLINICAL MONITORING & RISK RESEARCH (MIMIC-IV DEMO) ]
ICU Bedside Vital-Sign Telemetry (HR, RR, SpO2, SBP, DBP, MAP, Temp)
                       │
                       ▼
    Strict 24-Hour Observation Window [t_intime, t_intime + 24h)
                       │
                       ▼
    Physiological Quality Screening & 69-Feature Extraction
                       │
                       ▼
    Patient-Grouped Preprocessing Pipeline (Median Imputer + Scaler)
                       │
                       ▼
    L2 Regularized Baseline Model & Explicit Uncertainty Reporting
```

---

## 🛡️ Pipeline A: IoMT Cybersecurity IDS Architecture

### 1. Real Dataset Acquisition & Forensic Inspection (Edge-IIoTset)
- **Source Dataset:** *Edge-IIoTset: A New Comprehensive Realistic Cyber Security Dataset of IoT and IIoT Applications for Machine Learning* (IEEE Access, 2022).
- **Target File:** `datasets/edge_iiotset/selected_ml/ML-EdgeIIoT-dataset.csv` (82,184,390 bytes, 157,800 records, 63 columns).
- **Cryptographic SHA-256:** `53101fad091af20bee815860962a5016b802ee45d456a141042f6183094c3c1a` (Verified via automated unit tests).
- **Forensic Audit Findings:**
  - *8 Constant Columns:* `icmp.unused`, `http.tls_port`, `dns.qry.type`, `dns.retransmit_request_in`, `mqtt.msg_decoded_as`, `mbtcp.len`, `mbtcp.trans_id`, `mbtcp.unit_id` are 100% constant zero. Excluded from models.
  - *15,712 Shifted Timestamp Cells:* Column `frame.time` suffers an off-by-one shifting error for `DDoS_UDP` and `MITM` records. Excluded to prevent scenario schedule leakage.
  - *Zero Testbed Identity Leakage:* IP addresses (`ip.src_host`, `ip.dst_host`) and source ports (`tcp.srcport`) are completely excluded from all feature matrices.

### 2. Dual Feature Engineering Configurations
- **Configuration A (Canonical Edge Interface, 10 Features):** Preserves compatibility with the 9 canonical edge features + 1 missingness indicator (`entropy_is_missing`). Features omitted in the tabular release are imputed strictly on training data via `SimpleImputer(strategy='median')`.
- **Configuration B (Expanded Empirical Benchmark, 29 Features):** 29 genuine, clean numeric protocol features spanning ARP, ICMP, HTTP, TCP, UDP, DNS, and MQTT layers with 100% data completeness.

### 3. Empirical Cybersecurity Benchmark Results (Held-Out Test Set: N=19,103)

| Model Architecture | Feature Configuration | Test Accuracy | Macro Precision | Macro Recall | Macro F1-Score | Normal False Alarm Rate | Median Latency (μs) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Forest (Selected)** | **Config B (29 feat)** | **70.26%** | **68.31%** | **71.75%** | **64.28%** | **18.40%** | **13,554.6 μs** |
| **XGBoost Classifier** | Config B (29 feat) | 70.51% | 67.93% | 70.27% | 63.82% | 53.63% | 146.9 μs |
| **Decision Tree Baseline** | Config B (29 feat) | 70.61% | 68.87% | 70.34% | 63.77% | 58.38% | 31.1 μs |
| **Logistic Regression** | Config B (29 feat) | 64.76% | 68.15% | 53.67% | 56.96% | 46.43% | 38.5 μs |
| **Random Forest** | Config A (10 feat) | 4.48% | 4.67% | 20.20% | 4.32% | 100.00% | 13,527.0 μs |

#### Per-Class Detection Breakdown (Selected Random Forest Config B):
- **Flood DoS / DDoS (7,410 test samples):** Precision: **99.42%** | Recall: 76.23% | F1: **86.30%**
- **Reconnaissance (3,173 test samples):** Precision: 61.86% | Recall: **88.12%** | F1: **72.69%**
- **Ransomware (3,645 test samples):** Precision: **81.40%** | Recall: 45.73% | F1: 58.56%
- **Spoofing / MITM (182 test samples):** Precision: 40.90% | Recall: **100.00%** | F1: 58.05%
- **Command Injection (1,639 test samples):** Precision: **82.06%** | Recall: 38.80% | F1: 52.69%
- **Normal Traffic (3,054 test samples):** Precision: 44.24% | Recall: **81.60%** | F1: 57.37%

### 4. Out-of-Distribution (OOD) Threat Evaluation
- **Held-Out OOD Partition ($N=30,453$ records):** Entire attack classes (`Password`, `Uploading`, `Backdoor`) isolated exclusively to evaluate unsupervised novelty detection.
- **Isolation Forest Calibration:** Trained strictly on Normal baseline traffic ($N=17,011$). Achieved **4.99%** false alarm rate on normal test traffic (matching the 5% contamination target).
- **Scientific Takeaway:** Unsupervised novelty detection provides a crucial complementary check, but cannot replace multi-class supervised classification for application-layer threats.

### 5. Cyber-Physical Safety Interlocks & Machine Signal Defense
- **Clinical Safety Interlock State Machine:** For life-critical equipment (e.g. Puritan Bennett ventilators, Alaris infusion pumps), network anomalies trigger `ClinicalSafetyInterlock` (`LOCAL_BEDSIDE_OVERRIDE_LOCKED`), preventing automated firewall quarantine from severing life-support telemetry without bedside clinician confirmation.
- **Direct Machine Signal Cyber Defense:** Monitors physical device signals to detect:
  - *Lethal Bolus Overdose Hijack:* Malicious infusion rate surges (>50 mL/hr).
  - *Ventilator Barotrauma Hijack:* Peak inspiratory pressure exceeding 40 cmH2O.
  - *Telemetry Anti-Replay Attack:* Non-monotonic sequence counter tampering.
  - *Physiological Paradox Screening:* Impossible vital combinations (e.g. SpO2 99% with 0 bpm heart rate).

---

## 🔬 Pipeline B: Clinical Monitoring Research Module (MIMIC-IV Demo)

### 1. Research Cohort Construction
- **Source Dataset:** MIMIC-IV Clinical Database Demo v2.2 (`mimic-iv-clinical-database-demo-2.2`), 140 ICU stays audited across 100 unique ICU patients.
- **Pre-Prediction Exclusions ($N=4$ stays excluded):**
  - Stays with ICU length of stay $< 24\text{ hours}$ ($N=2$) or zero vital sign charting ($N=2$).
- **Eligible Cohort:** Exactly **136 ICU stays across 98 unique patients** (18 in-hospital deaths, 118 hospital survivors; 13.24% mortality prevalence).
- **Strict 24-Hour Observation Boundary:** Bounded strictly to $[t_{\text{intime}}, t_{\text{intime}} + 24\text{h})$. 50,432 post-24h vital observations excluded, eliminating temporal target leakage.
- **Patient-Level Grouped Splitting:** `GroupShuffleSplit` on `subject_id` guarantees **0 patient overlap** between training ($N=101$, 13 deaths) and testing ($N=35$, 5 deaths) partitions.

### 2. 69-Feature Physiological Schema & Empirical Evaluation
- **Features:** 7 core vitals (`heart_rate`, `respiratory_rate`, `spo2`, `systolic_bp`, `diastolic_bp`, `mean_bp`, `temperature_celsius`) $\times$ 9 statistical metrics (63 features) + 6 data-quality and missingness indicators.
- **Held-Out Test Set ($N=35$, 5 deaths):** ROC-AUC: **0.7600** | PR-AUC: **0.6160** | Accuracy: **82.86%** | Sensitivity: **60.0%** | Specificity: **86.67%** | Brier Score: **0.1268**.
- **5-Fold Grouped Cross-Validation ($N=136$, 18 deaths):** Out-of-fold ROC-AUC: **0.5325** | PR-AUC: **0.3083** | Accuracy: **75.00%**.
- **The Small-Sample Optimism Gap:** The contrast between held-out test AUC (0.7600) and cross-validation AUC (0.5325) exposes the extreme sensitivity volatility when evaluated on only 5 deaths.
- **Mandatory Clinical Disclaimer:** Exploratory engineering baseline only; strictly non-diagnostic; no clinical reliance permitted without human physician review.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI/UX** | React 18, TypeScript 5.2, Vite, Tailwind CSS, Lucide Icons |
| **Backend API** | FastAPI 0.143+, Python 3.11/3.14, SQLAlchemy, SQLite WAL, WebSockets |
| **Cybersecurity ML** | Scikit-Learn 1.9+, XGBoost 3.4+, NumPy 2.5+, Pandas 3.0+, Joblib |
| **Clinical ML Pipeline** | Scikit-Learn (LogisticRegression, GroupShuffleSplit, GroupKFold), Matplotlib, Seaborn |
| **Local GenAI / SLM** | Ollama (Llama 3 / Phi-3) + PyMuPDF Vector Document RAG + Rule Fallback |
| **Enforcement & Safety** | Linux iptables Adapter + Safe Simulation Adapter + Clinical Safety Interlocks |
| **Presentation Engine** | Python-pptx (30 Widescreen 16:9 Slides with Complete Speaker Notes) |

---

## 🚀 Quickstart & Complete Reproduction Guide

### 1. Setup Python Environment
```bash
# From repository root:
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install matplotlib seaborn python-pptx
```

### 2. Run Empirical Cybersecurity Training & Benchmarking
```bash
# Trains RF, XGBoost, Decision Tree, Logistic Regression & Isolation Forest on Edge-IIoTset
python ml_pipeline/train_empirical_ids.py

# Artifacts generated under ml_pipeline/models/empirical/:
# - rf_classifier_config_b.joblib, xgb_classifier_config_b.joblib, isolation_forest_config_b.joblib
# - evaluation_metrics.json, EMPIRICAL_EVALUATION_REPORT.md
# - High-resolution figures under ml_pipeline/models/empirical/figures/
```

### 3. Run Clinical Pipeline & Generate Publication Plots
```bash
# Step 1: Run prospective cohort audit and verification
python build_prediction_cohort.py

# Step 2: Construct temporally valid 24-hour feature dataset
python build_feature_dataset.py

# Step 3: Run comprehensive data quality and plausibility checks
python validate_feature_dataset.py

# Step 4: Train and evaluate patient-grouped baseline models
python train_baseline_model.py

# Step 5: Generate publication-grade clinical evaluation figures
python research/patient_monitoring/generate_clinical_eval_plots.py
```

### 4. Run Automated Test Suite (90 Passing Tests)
```bash
PYTHONPATH=backend:. pytest backend/tests ml_pipeline/data_ingestion/test_feature_extractor.py -v
# Output: 90 passed, 0 failed in 2.51s
```

### 5. Build Frontend for Production
```bash
cd frontend
npm install
npm run build
# Output: 0 TypeScript errors; bundled via Vite in 1.25s
cd ..
```

### 6. Generate the Final 30-Slide PowerPoint Presentation
```bash
python presentation_output/final/generate_final_presentation.py

# Generates:
# presentation_output/final/EdgeShield_AI_Final_Project_Presentation.pptx
# Audited in: presentation_output/final/FINAL_PRESENTATION_VERIFICATION.md
```

### 7. Start Development Servers
```bash
# Terminal 1: FastAPI Backend (Port 8000)
PYTHONPATH=backend uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: React Frontend (Port 5173)
cd frontend
npm run dev
```

Interactive API documentation is available at `http://localhost:8000/docs`, and the operational dashboard at `http://localhost:5173`.

---

## 📄 Final Project Completion & Verification Status

The complete end-to-end delivery of EdgeShield AI has been audited and signed off:
- **Final Completion Report:** [`presentation_output/final/FINAL_PROJECT_COMPLETION_REPORT.md`](presentation_output/final/FINAL_PROJECT_COMPLETION_REPORT.md)
- **Final Presentation Verification:** [`presentation_output/final/FINAL_PRESENTATION_VERIFICATION.md`](presentation_output/final/FINAL_PRESENTATION_VERIFICATION.md)
- **Final PowerPoint Deck:** [`presentation_output/final/EdgeShield_AI_Final_Project_Presentation.pptx`](presentation_output/final/EdgeShield_AI_Final_Project_Presentation.pptx)
- **Empirical Cybersecurity Report:** [`ml_pipeline/models/empirical/EMPIRICAL_EVALUATION_REPORT.md`](ml_pipeline/models/empirical/EMPIRICAL_EVALUATION_REPORT.md)
- **Phase 2 Data Preparation Report:** [`presentation_output/PHASE2_2_DATA_PREPARATION_REPORT.md`](presentation_output/PHASE2_2_DATA_PREPARATION_REPORT.md)
- **Automated Test Suite:** **90 passed, 0 failed (100% passing)**
- **Frontend Build:** **0 compilation or linting errors**
- **Deliverables Status:** **All 10 project phases complete and verified**

---

## 📄 License & Attribution

Distributed under the MIT License.
- Cybersecurity dataset derived from **Edge-IIoTset** (Ferrag et al., Technology Innovation Institute & De Montfort University, *IEEE Access* 2022).
- Clinical dataset derived from **PhysioNet MIMIC-IV Clinical Database Demo v2.2** (Johnson et al., PhysioNet 2023).
