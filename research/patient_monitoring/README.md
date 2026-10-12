# EdgeShield AI — Patient Vital-Sign Monitoring & Hospital Mortality Risk Research

## 1. Module Overview & Purpose

This module establishes the clinical data engineering and machine learning pipeline for **EdgeShield AI**, focusing on patient vital-sign monitoring, prospective cohort verification, physiological data-quality screening, and exploratory in-hospital mortality risk estimation.

While EdgeShield AI focuses primarily on cybersecurity intrusion detection for Internet of Medical Things (IoMT) devices, this module serves the clinical telemetry layer: evaluating non-invasive physiological vital signs extracted from intensive care admissions.

---

## 2. Dataset Information

- **Dataset:** MIMIC-IV Clinical Database Demo 2.2 (`mimic-iv-clinical-database-demo-2.2`)
- **Raw ICU Stays:** 140 stays
- **Raw Unique Patients:** 100 patients
- **Raw Admissions:** 275 hospital admissions
- **Core Vital Signs (Item IDs):**
  - Heart Rate: `220045`
  - Oxygen Saturation (SpO2): `220277`
  - Respiratory Rate: `220210`
  - Systolic Blood Pressure: `220179`
  - Diastolic Blood Pressure: `220180`
  - Mean Blood Pressure: `220181`
  - Temperature Fahrenheit: `223761`
  - Temperature Celsius: `223762`
- **Important Note:** MIMIC-IV Demo is a pedagogical sample of 100 patients provided by PhysioNet for engineering validation. It is not an epidemiologically representative cohort for clinical diagnostic deployment.

---

## 3. Current Pipeline Status

| Pipeline Stage | Script / Module | Status | Key Outputs |
|---|---|---|---|
| **Step 1: Vital Extraction & Quality Flagging** | `extract_vitals.py`, `flag_vital_quality.py` | Complete & Verified | `mimic_vitals_long.csv`, `mimic_vitals_quality_checked.csv` |
| **Step 2: Temperature Normalization & Hourly Windowing** | `normalize_vitals.py`, `prepare_time_windows.py` | Complete & Verified | `mimic_vitals_normalized.csv`, `patient_hourly_vitals.csv` |
| **Step 3: Prospective Cohort Audit & Eligibility Verification** | `build_prediction_cohort.py` | Complete & Verified | `eligible_cohort.csv`, `excluded_cohort.csv`, `cohort_audit_summary.json` |
| **Step 4: 24-Hour Feature Engineering & Leakage Prevention** | `build_feature_dataset.py` | Complete & Verified | `features_24h.csv`, `labels_24h.csv`, `metadata_cohort_24h.csv` |
| **Step 5: Data Quality & Plausibility Validation** | `validate_feature_dataset.py` | Complete & Verified | `data_quality_report.json`, `data_quality_report.md`, `exclusions_report.md` |
| **Step 6: Sample Size & Feasibility Assessment** | `research/patient_monitoring/feasibility_assessment.md` | Complete & Verified | Formal Feasibility Document |
| **Step 7: Baseline Model Training & Grouped Evaluation** | `train_baseline_model.py` | Complete & Verified | `baseline_model.joblib`, `model_metrics.json`, `patient_splits.json` |
| **Step 8: FastAPI Backend Service Integration** | `backend/app/api/v1/endpoints/patient_monitoring.py` | Complete & Verified | `/api/v1/patient-monitoring/*` endpoints, 28 dedicated unit & contract tests (77 total backend tests) |
| **Step 9: React Dashboard Frontend Integration** | `frontend/src/components/patient/PatientMonitoringView.tsx` | Complete & Verified | "Patient Vitals & Risk" interactive UI tab, production build passing (0 TS errors) |

---

## 4. Prospective Prediction Target & Window Definition

### Prospective Prediction Time
$$\text{Prediction Time} = \text{ICU Admission Time} + 24\text{ hours}$$

### Observation Window
All features are calculated strictly within the half-open interval:
$$[\text{intime}, \text{intime} + 24\text{ hours})$$
Measurements recorded exactly at or after $t = \text{intime} + 24\text{h}$ are treated as post-prediction and strictly excluded.

### Target Definition
- **Target:** `hospital_expire_flag`
- **Clinical Meaning:** Death before hospital discharge, among patients alive and hospitalized at the 24-hour prediction time.
- **Exclusion 1 (Death Before Prediction Time):** Patients who died before or at hour 24 cannot be prospectively predicted. 2 stays (`36871784`, `38275267`) died prior to hour 24 and are excluded.
- **Exclusion 2 (Hospital Discharge Before Prediction Time):** Patients discharged alive before hour 24 left acute inpatient care prior to the window end. 2 stays (`32554129`, `30864406`) are excluded.
- **Final Eligible Cohort:** **136 ICU stays across 98 unique patients** (18 deaths, 118 survivors).

---

## 5. Leakage Prevention & Methodological Safeguards

1. **Strict Temporal Separation:** Only vital observations with $\text{intime} \le \text{charttime} < \text{prediction\_time}$ enter feature computation. Post-24h records (n=50,828) are completely ignored during feature generation.
2. **Metadata & Identifier Isolation:** Identifiers (`subject_id`, `hadm_id`, `stay_id`, timestamps) and outcome labels (`hospital_expire_flag`) are saved in separate CSV files. The feature matrix contains exclusively numerical and Boolean predictor variables.
3. **Patient-Level Grouping:** Multiple ICU stays for the same patient are kept in the same partition (`GroupShuffleSplit` and `GroupKFold` grouped on `subject_id`). 4 patients had mixed outcomes across admissions; patient-level grouping strictly eliminates patient cross-contamination.
4. **No Preprocessing Contamination:** Imputation (`SimpleImputer(strategy='median')`) and standardization (`StandardScaler()`) are fit exclusively on training data folds.
5. **Transparent Missingness Handling:** Missing values are never filled with zero. Instead, explicit missing indicators (`_is_missing`) and measurement counts are tracked.

---

## 6. Model Limitations & Feasibility Assessment

- **Small Positive Class:** Across all 136 eligible stays, there are only 18 deaths (14 unique deceased patients).
- **Metric Sensitivity Volatility:** In a held-out test partition of 35 stays (5 deaths), each single prediction error shifts test sensitivity by 20.0 percentage points.
- **Disparity between Single Split and Cross-Validation:**
  - Single Held-Out Test Set: ROC-AUC = 0.7600, PR-AUC = 0.6160 (95% Bootstrap CI: [0.3120, 1.0000])
  - 5-Fold Grouped Out-Of-Fold Cross-Validation: ROC-AUC = 0.5325, PR-AUC = 0.3083, Mean Fold ROC-AUC = 0.5540 $\pm$ 0.1064
- **Statistical Finding:** The held-out test set performance reflects small-sample sampling variance due to having only 5 positive events in the test partition. The grouped cross-validation score represents a much lower-variance estimate across the entire cohort.
- **Regulatory Status:** The trained model is an exploratory technical baseline. It is not an FDA-cleared diagnostic tool and must not be used for clinical decision making.

---

## 7. Exact Commands to Reproduce Pipeline

From the project root (`/Users/govathotyjoshkumar/Code Files/MP`):

```bash
# 1. Activate Python virtual environment
source .venv/bin/activate

# 2. Step 3: Run prospective cohort audit and verification
python build_prediction_cohort.py

# 3. Step 4: Construct temporally valid 24-hour features
python build_feature_dataset.py

# 4. Step 5: Execute comprehensive data validation and plausibility checks
python validate_feature_dataset.py

# 5. Step 6 & 7: Train and evaluate patient-grouped baseline models
python train_baseline_model.py

# 6. Step 8: Run backend test suite (all 77 unit, integration, and security tests)
cd backend
PYTHONPATH=. ../.venv/bin/pytest tests
cd ..

# 7. Step 9: Build React frontend application
cd frontend
npm run build
cd ..
```

---

## 8. Artifact Directory Map

All artifacts are persisted in `research/patient_monitoring/`:

```
research/patient_monitoring/
├── README.md                          <- This documentation
├── cohort_audit_summary.json          <- Machine-readable audit metrics (Step 3)
├── cohort_audit_report.md             <- Comprehensive cohort audit report (Step 3)
├── eligible_cohort.csv                <- 136 eligible stays with outcomes and coverage
├── excluded_cohort.csv                <- 4 excluded stays with reasons and timestamps
├── features_24h.csv                   <- 136 x 70 clean numerical feature dataset
├── labels_24h.csv                     <- 136 binary hospital mortality labels
├── metadata_cohort_24h.csv            <- 136 stay and admission administrative metadata
├── feature_summary.csv                <- Descriptive statistics for all 69 predictors
├── missingness_report.csv             <- Missingness percentages per vital sign
├── data_quality_report.json           <- Automated validation test results
├── data_quality_report.md             <- Clinical bounds plausibility review
├── exclusions_report.md               <- Full audit trail of excluded stays
├── feasibility_assessment.md          <- Sample size and statistical feasibility analysis
├── baseline_model.joblib              <- Trained Scikit-Learn Pipeline (Imputer + Scaler + LogisticRegression)
├── model_feature_metadata.json        <- Feature names and preprocessing configurations
├── model_metrics.json                 <- Held-out test and 5-fold cross-validation metrics
├── model_evaluation_report.md         <- Comprehensive evaluation benchmarks and limitations
└── patient_splits.json                <- Patient-level train and test split assignments
```
