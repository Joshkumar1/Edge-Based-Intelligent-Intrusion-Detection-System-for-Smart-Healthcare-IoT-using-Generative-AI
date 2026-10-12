# EdgeShield AI: Edge-Based Intrusion Detection & Clinical Telemetry Monitoring for Smart Healthcare IoT

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6.svg)](https://www.typescriptlang.org/)
[![Status: Phase 1 Complete](https://img.shields.io/badge/Status-Phase%201%20Verified-emerald.svg)](#phase-1-verification-status)

> **Project Scope**: Privacy-Preserving, Low-Latency Edge Intrusion Detection, Cyber-Physical Safety Interlocks, and Prospective Clinical Monitoring Research for Smart Hospitals.

---

## 🏥 Executive Project Vision

In life-critical hospital environments—where infusion pumps, ICU patient monitors, and DICOM radiology workstations operate continuously—cryptic cybersecurity alerts cause cognitive fatigue and critical response delays. Furthermore, network security cannot be detached from clinical patient context: isolating a device delivering life-critical therapy requires specialized safety interlocks.

**EdgeShield AI** provides an integrated edge architecture featuring two decoupled, specialized pipelines:
1. **Pipeline A: IoMT Cybersecurity & Intrusion Detection (IDS)**
   - Ingests multi-protocol network telemetry (Modbus/TCP, MQTT, DICOM).
   - Performs dual-stage machine learning detection (unsupervised anomaly detection + multi-class attack classification).
   - Dispatches asynchronous explainable AI triaging without blocking line-rate edge packet inspection.
   - Enforces host firewall quarantine with cyber-physical safety interlocks that safeguard life-support equipment.
2. **Pipeline B: Clinical Vital-Sign Monitoring & Mortality Risk Research**
   - Ingests physiological vital signs from ICU admissions.
   - Enforces a prospective 24-hour observation window with zero temporal leakage.
   - Evaluates exploratory hospital mortality risk baselines with grouped patient-level cross-validation and explicit uncertainty reporting.

---

## ⚡ Architectural Pipelines

```
[ PIPELINE A: IoMT CYBERSECURITY IDS ]
Medical IoT Packet Stream (DICOM / MQTT / Modbus)
                       │
                       ▼
         Stage 1: Isolation Forest (Zero-Day Anomaly Detection)
                       │
                       ▼
         Stage 2: Random Forest Multi-Class Threat Classifier
                       │
                       ▼
         Asynchronous Local LLM / Deterministic Explainability
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
ICU Bedside Vital-Sign Telemetry (HR, RR, SpO2, BP, Temp)
                       │
                       ▼
    Strict 24-Hour Observation Window [intime, intime + 24h)
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

### 1. Dual-Stage ML Detection Engine
- **Stage 1 (Unsupervised Anomaly Detection):** Scikit-learn `IsolationForest` (100 estimators, 5% contamination) evaluates normalized network features to detect zero-day deviations.
- **Stage 2 (Supervised Multi-Class Threat Classifier):** Scikit-learn `RandomForestClassifier` (100 estimators, max depth 12) classifies attacks into canonical categories:
  - `Normal`
  - `DICOM Ransomware` (high entropy, burst transfers targeting PACS)
  - `MQTT Flood DoS` (massive publish message rates targeting telemetry brokers)
  - `Modbus Command Injection` (unauthorized coil/register write function codes)
  - `ARP Spoofing MITM` (anomalous packet rates with small frame lengths)
  - `Port Scan Reconnaissance` (high TCP SYN flag frequency with tiny packet lengths)

### 2. Cybersecurity Training Data & Performance Transparency
> **IMPORTANT DATASET PROVENANCE NOTICE:**  
> The current Phase 1 intrusion detection models in `ml_pipeline/models/` were trained using a synthetic medical IoT dataset generator (`ml_pipeline/train_ids.py`). The generator uses parametric statistical distributions (Gaussian and uniform distributions) designed to simulate the feature characteristics of smart hospital devices (infusion pumps, patient monitors, imaging stations) inspired by published benchmark taxonomies (such as Edge-IIoTset and N-BaIoT).  
> **The current IDS model has NOT been trained or empirically validated on uncurated physical PCAP captures of the raw Edge-IIoTset, N-BaIoT, or TON_IoT datasets.**  
> Because the synthetic data classes are cleanly separable by construction, synthetic evaluation yields idealized 100% precision and recall metrics. Real-world validation against physical testbed packet captures remains planned for subsequent phases.

### 3. Edge Latency & Decoupled AI Explainability
- **Detection Latency:** Edge ML scoring operates synchronously in `< 5 ms` per packet on standard x86_64/ARM edge hardware.
- **Asynchronous AI Workers:** Generative AI / LLM explanations (via local Ollama or rule-based fallback engines) are dispatched asynchronously in background tasks (`ai_enricher.py`), ensuring that slow language model inference never blocks edge packet forwarding or real-time alert dispatch.
- **Generative AI Boundary:** Generative AI strictly assists with operational explanations and mitigation suggestions; it **never** makes autonomous packet blocking or quarantine decisions.

### 4. Enforcement Modes & Cyber-Physical Safety Interlocks
- **Host Firewall Adapter:** Real OS-level Linux firewall controller (`iptables` / `nftables`) applying validated, idempotent, commented drop rules (`edgeshield-isolated-<id>`). If executed on non-Linux platforms or without `iptables` installed, the adapter cleanly returns status `UNSUPPORTED`.
- **Simulation Enforcement Adapter:** Default development adapter (`EDGE_ENFORCEMENT_MODE=simulation`) tracking in-memory isolation state and transparently returning status `SIMULATED` with an explicit notice that no OS firewall was modified.
- **Clinical Safety Interlocks:** For life-critical equipment (e.g., infusion pumps, mechanical ventilators), cyber threats trigger a `ClinicalSafetyInterlock` row (`LOCAL_BEDSIDE_OVERRIDE_LOCKED`), preventing automated network disconnections from severing life-support telemetry without clinician review.

---

## 🔬 Pipeline B: Clinical Monitoring Research Module (MIMIC-IV Demo)

### 1. Research Cohort Construction
- **Source Dataset:** MIMIC-IV Clinical Database Demo 2.2 (`mimic-iv-clinical-database-demo-2.2`), a pedagogical sample of 100 patients and 140 ICU stays provided by PhysioNet for engineering validation.
- **Pre-Prediction Exclusions ($N=4$ stays excluded):**
  - *Deaths before or at 24 hours:* 2 stays (`36871784` died at 1.24h; `38275267` died at 12.65h). Patients deceased prior to the prediction horizon cannot be prospectively predicted.
  - *Discharges before or at 24 hours:* 2 stays (`32554129` discharged at 17.0h; `30864406` discharged at 23.7h).
- **Eligible Cohort:** Exactly **136 ICU stays across 98 unique patients** (18 in-hospital deaths, 118 hospital survivors; 13.24% mortality prevalence). 4 patients had mixed outcomes across separate hospital admissions.

### 2. Strict 24-Hour Observation Window & Leakage Prevention
- **Prospective Prediction Time:** Strictly defined as $t_{\text{pred}} = t_{\text{intime}} + 24\text{ hours}$.
- **Half-Open Observation Window:** All predictor features are derived strictly from $[t_{\text{intime}}, t_{\text{intime}} + 24\text{h})$. Records with $\text{charttime} \ge t_{\text{pred}}$ (50,432 post-24h chart events) are strictly ignored, eliminating temporal leakage.
- **Patient-Level Grouping:** Multiple ICU stays for the same patient are constrained to the same split (`GroupShuffleSplit` on `subject_id`). Patient overlap between training ($N=101$ stays, 73 patients) and testing ($N=35$ stays, 25 patients) partitions is exactly **0**.
- **Preprocessing Isolation:** Missing-value imputation (`SimpleImputer(strategy='median')`) and standardization (`StandardScaler()`) are fit strictly within training folds.

### 3. 69-Feature Baseline Model
- **Observation Summary (6 features):** Zero-value flags, low SpO2 flags, extreme heart-rate flags, total flagged observations, distinct monitored hours, and total vital measurements count.
- **Core Physiological Vitals (63 features):** 7 core vital signs (`heart_rate`, `respiratory_rate`, `spo2`, `systolic_bp`, `diastolic_bp`, `mean_bp`, `temperature_celsius`), each represented by 9 statistical metrics:
  - Measurement count, explicit missing indicator (`_is_missing`), most recent measurement, mean, min, max, standard deviation, time since last measurement (hours), and late-minus-early trend.
- **Model Specification:** Regularized Logistic Regression ($L_2$ penalty, $C=0.1$, balanced class weights, L-BFGS solver).

### 4. Empirical Evaluation & Uncertainty Analysis
| Evaluation Strategy | Cohort Size | In-Hospital Deaths | ROC-AUC | PR-AUC | Accuracy | Sensitivity | Specificity |
|---|---|---|---|---|---|---|---|
| **Held-Out Test Set (Single Split)** | 35 stays (25 patients) | 5 deaths | **0.7600** | **0.6160** | 0.8286 | 0.6000 | 0.8667 |
| **5-Fold Grouped Cross-Validation (OOF)** | 136 stays (98 patients) | 18 deaths | **0.5325** | **0.3083** | 0.7500 | 0.3333 | 0.8136 |

#### Statistical Uncertainty & Metric Interpretation:
- **Small-Sample Variance:** The single held-out test ROC-AUC (0.7600) is subject to extreme sampling variability due to having only 5 positive deaths in the test partition. A 2,000-sample bootstrap analysis yields a 95% confidence interval for test ROC-AUC of **$[0.3120, 1.0000]$** (spanning over 68 percentage points).
- **Grouped Cross-Validation Reality:** The 5-fold grouped out-of-fold ROC-AUC of **0.5325** (mean fold ROC-AUC $0.5540 \pm 0.1064$) accurately reflects the true baseline predictive capability of non-invasive vital signs on this cohort when evaluating across all 18 positive cases.

### 5. Mandatory Clinical & Regulatory Disclaimer
> **CLINICAL RESEARCH DISCLAIMER:**  
> The patient vital-sign monitoring and hospital mortality risk estimation modules in EdgeShield AI are exploratory engineering baseline implementations developed exclusively for pipeline verification and technical demonstration on the MIMIC-IV Demo research dataset.  
> They are **NOT** clinically validated, **NOT** medical devices, **NOT** FDA-cleared, and must **NEVER** be utilized for patient triage, clinical diagnosis, bedside decision-making, or real patient care.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI/UX** | React 18, TypeScript 5.2, Vite, Tailwind CSS, Recharts, Framer Motion, Lucide Icons |
| **Backend API** | FastAPI 0.110+, Python 3.11/3.14, SQLAlchemy, SQLite, WebSockets |
| **Cybersecurity ML** | Scikit-learn (Isolation Forest, Random Forest), NumPy, Pandas |
| **Clinical ML Pipeline** | Scikit-learn (LogisticRegression, GroupKFold, GroupShuffleSplit), Joblib |
| **Local GenAI / SLM** | Ollama (Llama 3 8B / Phi-3) + Local Deterministic Healthcare Expert Rule Fallback |
| **Deployment & Ops** | Docker, Docker Compose, Linux iptables adapter |

---

## 🚀 Quickstart & Reproduction Guide

### 1. Setup Python Environment
```bash
# From repository root:
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Reproduce Clinical Data & Baseline Model Pipeline
```bash
# Step 1: Run prospective cohort audit and verification
python build_prediction_cohort.py

# Step 2: Construct temporally valid 24-hour feature dataset
python build_feature_dataset.py

# Step 3: Run comprehensive data quality and plausibility checks
python validate_feature_dataset.py

# Step 4: Train and evaluate patient-grouped baseline models
python train_baseline_model.py
```

### 3. Run Automated Backend Tests
```bash
PYTHONPATH=backend ./venv/bin/pytest backend/tests -v
# Output: 77 passed across 6 test suites
```

### 4. Build Frontend for Production
```bash
cd frontend
npm install
npm run build
# Output: 0 TypeScript errors; bundled via Vite
```

### 5. Start Development Servers
```bash
# Terminal 1: FastAPI Backend (Port 8000)
PYTHONPATH=backend ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: React Frontend (Port 5173)
cd frontend
npm run dev
```

Interactive API documentation will be available at `http://localhost:8000/docs`, and the dashboard at `http://localhost:5173`.

---

## 📄 Phase 1 Verification Status

The comprehensive Phase 1 completion audit has been conducted and documented:
- Audit Report: [`presentation_output/PHASE1_FINAL_AUDIT.md`](presentation_output/PHASE1_FINAL_AUDIT.md)
- Automated Test Suite: **77 passed, 0 failed**
- Frontend Build: **0 compilation or linting errors**
- Scope Verification: **All 18 Phase 1 scope items verified**

---

## 📄 License & Attribution

Distributed under the MIT License. Clinical data derived from PhysioNet MIMIC-IV Clinical Database Demo 2.2 under the PhysioNet Credentialed Data Use Agreement.
