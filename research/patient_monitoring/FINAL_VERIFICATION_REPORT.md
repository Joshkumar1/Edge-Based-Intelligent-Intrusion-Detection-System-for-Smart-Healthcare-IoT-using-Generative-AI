# EdgeShield AI — Final Verification & Audit Report
**Date:** October 2026  
**Module:** Patient Vital-Sign Monitoring & Hospital Mortality Risk Research + IoMT Intrusion Detection  
**Environment:** macOS, Python 3.14 (.venv), FastAPI Backend, React 18 + Vite Frontend  
**Author:** Senior Full-Stack & ML Engineer / Software Testing Engineer  

---

## 1. Executive Summary

All phases of the requested EdgeShield AI evaluation, backend audit, clinical model integration, schema validation, test expansion, frontend verification, production build, and model evaluation audit have been completed autonomously and verified.

1. **Backend Test Suite:** **77 passed, 0 failed** across 6 test modules (`test_api.py`, `test_canonical_pipeline.py`, `test_documents_and_copilot.py`, `test_machine_signals.py`, `test_patient_monitoring.py`, `test_security_and_enforcement.py`).
2. **Clinical Model Integration:** `baseline_model.joblib` and `model_feature_metadata.json` loaded once at service startup, validating the 69 expected features, rejecting non-finite numbers (NaN, infinity), and handling missing values with the fitted median imputer.
3. **Frontend Production Build:** `tsc && vite build` passed cleanly in **1.28s** with **0 TypeScript errors** and **0 build errors**.
4. **End-to-End & Schema Verification:** All API endpoints (`/health`, `/status`, `/validate-vitals`, `/assess-risk`, `/predict`, `/cohort-summary`, `/sample-records`) map 1-to-1 to the frontend's TypeScript interfaces and Pydantic schemas.
5. **Architectural Separation:** Patient monitoring operates as an independent module alongside EdgeShield's existing IoMT intrusion-detection and machine-signal defense systems without cross-contamination.
6. **Scientific Audit Findings:** The disparity between held-out test ROC-AUC (0.7600) and 5-fold grouped out-of-fold ROC-AUC (0.5325) has been investigated and documented: it is caused by small-sample variance ($N=5$ deaths in the test partition, producing a wide 95% bootstrap CI of $[0.3120, 1.0000]$).

---

## 2. Backend Test Summary

Executed with `.venv/bin/pytest tests` inside `backend/`:

| Test Suite | Tests Executed | Passed | Failed | Status |
|---|---|---|---|---|
| `tests/test_api.py` | 4 | 4 | 0 | PASS |
| `tests/test_canonical_pipeline.py` | 14 | 14 | 0 | PASS |
| `tests/test_documents_and_copilot.py` | 7 | 7 | 0 | PASS |
| `tests/test_machine_signals.py` | 7 | 7 | 0 | PASS |
| `tests/test_patient_monitoring.py` | 28 | 28 | 0 | PASS |
| `tests/test_security_and_enforcement.py` | 17 | 17 | 0 | PASS |
| **Total** | **77** | **77** | **0** | **100% PASS** |

### Key Test Categories Covered:
- **Health Check & Service Status:** GET `/health` returns status `healthy` with timestamp and active modules (`intrusion_detection: ONLINE`, `patient_monitoring: ONLINE`).
- **OpenAPI Schema Generation:** GET `/api/v1/openapi.json` successfully generates with all patient monitoring and cybersecurity paths.
- **CORS Behavior:** OPTIONS preflight returns status 200/204 with `Access-Control-Allow-Origin`.
- **Prospective Cohort & Leakage Tests:**
  - 140 ICU stays linked to hospital admissions with 0 missing outcomes.
  - 2 deaths before or at 24h excluded (`stay_id` 36871784, 38275267).
  - 2 discharges before or at 24h excluded (`stay_id` 32554129, 30864406).
  - 136 eligible stays retained across 98 unique patients.
  - 0 duplicate stay IDs; strict alignment between features, labels, and metadata.
  - 0 target leakage features; 0 temporal leakage violations.
  - Patient-level splitting verified with 0 patient overlap between train and test.
- **Validation & Quality Logic:**
  - Temperature unit conversion (Fahrenheit to Celsius).
  - Quality flag detection (`review_zero_value`, `review_low_spo2`, `review_extreme_heart_rate`).
  - Missing measurements tracked explicitly without zero-substitution.
- **Model Loading & Fallbacks:**
  - Model artifact exists and loads correctly.
  - Missing artifact directory handled gracefully, returning `INDETERMINATE` and clear disclaimers.
  - Corrupted model artifact file handled safely without crashing.
  - Metadata feature mismatch detected, deactivating model safely.
- **Prediction Endpoints:**
  - Valid bedside vital sign inputs and valid precomputed 69-feature vectors.
  - Unexpected features outside the 69-feature schema rejected with HTTP 422.
  - Empty requests missing both vitals and features rejected with HTTP 422.
  - Non-finite numeric inputs (NaN, infinity, string "NaN") rejected with HTTP 422.
  - Negative vital signs (e.g., negative SpO2) rejected with HTTP 422.
  - Prediction probability verified finite and bounded in $[0.0, 1.0]$.
- **IoMT Intrusion-Detection Unification:**
  - Device inventory (`/api/v1/devices/`), alert feeds (`/api/v1/alerts/`), and signal collectors (`/api/v1/signals/collectors`) remain 100% functional.

---

## 3. Frontend Build Summary

Executed in `frontend/` using `npm run build`:
- **Command:** `tsc && vite build`
- **TypeScript Compiler (`tsc`):** 0 errors.
- **Vite Bundler:** Bundled 2,669 modules in 1.28s.
- **Output Artifacts:**
  - `dist/index.html`: 0.96 kB (gzip: 0.54 kB)
  - `dist/assets/index-DokeBdAz.css`: 44.60 kB (gzip: 7.77 kB)
  - `dist/assets/index-CPkF_3IZ.js`: 860.00 kB (gzip: 236.13 kB)
- **Status:** **PASS (Zero Build Errors)**

---

## 4. Frontend Component & UX Audit

- **Navigation:** Added "Patient Vitals & Risk" navigation item to `frontend/src/components/layout/Sidebar.tsx` with `HeartPulse` icon and `Step 3 Verified` badge.
- **Route / View:** Mounted `PatientMonitoringView` in `frontend/src/App.tsx`.
- **Demonstration Selector:** 3 realistic demonstration cases pre-loaded from MIMIC-IV Demo (`Stay 31269608`, `Stay 38559363`, `Stay 39543480`) clearly labeled as demonstration records.
- **Interactive Vitals Panel:** Allows entering Heart Rate, Respiratory Rate, SpO2, Systolic BP, Diastolic BP, and Body Temperature with dynamic °C/°F unit switching.
- **Data Quality Screening:** Renders real-time clinical screening flags (zero values, hypoxemia, extreme heart rate) and lists missing measurements being handled by the median imputer.
- **Visual Distinction:** Clinical risk prediction is visually and conceptually separated from observed vital measurements, displayed in a dedicated card with clear category badges (`LOW`, `ELEVATED`, `HIGH`).
- **Disclaimers:** Mandatory research disclaimer banner permanently visible at the top of the view, stating that the model is for research/engineering verification and not an FDA-cleared diagnostic device.

---

## 5. Model Evaluation Audit Findings

### Investigation of Scientific Validity:
1. **Observation Window Boundary:** The observation window is strictly defined as the half-open interval $[t_{\text{intime}}, t_{\text{intime}} + 24\text{h})$. In `build_feature_dataset.py`, the temporal filter was hardened to `charttime < prediction_time`, correctly excluding 3 measurements recorded at exactly $t = 24.0$h.
2. **Outcome Labels:** Verified against MIMIC-IV `admissions.csv.gz` using `validate="many_to_one"`. All 140 stays link cleanly; 0 missing outcomes.
3. **Pre-Prediction Deaths Excluded:** 2 stays (`36871784`, `38275267`) died prior to hour 24 and were excluded.
4. **Pre-Prediction Discharges Excluded:** 2 stays (`32554129`, `30864406`) were discharged alive prior to hour 24 and were excluded.
5. **Patient-Level Grouping:** All repeat stays for a patient are assigned to the same partition. Overlap between train and test patients is 0.
6. **Preprocessing Isolation:** Imputation (`SimpleImputer`) and scaling (`StandardScaler`) are fit strictly inside the training pipelines. No test fold statistics leak into preprocessing.
7. **Cross-Validation Class Representation:** Every fold of the 5-fold `GroupKFold` contains positive mortality cases (Fold 0: 3, Fold 1: 2, Fold 2: 6, Fold 3: 3, Fold 4: 4).
8. **Saved Model Identity:** The saved model `baseline_model.joblib` is the pipeline trained on the 75% training partition ($N=101$ stays, 73 patients), while held-out performance is reported on the separate 25% test partition ($N=35$ stays, 25 patients).

### Resolution of the Performance Discrepancy:
- **Held-Out Test Set (Single Split):**
  - Sample size: 35 stays, only 5 deaths.
  - Logistic Regression ROC-AUC: **0.7600**
  - Random Forest ROC-AUC: **0.7667**
  - Logistic Regression PR-AUC: **0.6160**
  - **95% Bootstrap Confidence Interval for Test ROC-AUC:** **[0.3120, 1.0000]**
- **5-Fold Grouped Out-Of-Fold Cross-Validation (All 136 Stays):**
  - Sample size: 136 stays, 18 deaths (14 unique deceased patients).
  - Out-of-Fold ROC-AUC: **0.5325**
  - Mean Fold ROC-AUC: **0.5540 $\pm$ 0.1064**
  - Out-of-Fold PR-AUC: **0.3083**
  - Mean Fold PR-AUC: **0.3580 $\pm$ 0.1411**
- **Conclusion:** The single held-out test ROC-AUC (0.76) is inflated by high sampling variance on a small sample of 5 positive events. Its 95% confidence interval spans over 68 percentage points ($[0.312, 1.000]$), which fully encloses the cross-validation performance. The 5-fold grouped cross-validation score (0.53 to 0.55) represents the true expected performance of non-invasive vital signs on this small demo cohort.

---

## 6. Dependency & Security Review

- **Environment Standardization:** Installed `email-validator` in `.venv` to resolve Pydantic EmailStr compatibility across root execution.
- **No Hardcoded Secrets Committed:** Sensitive tokens use environment variables or local fallback development keys.
- **CORS:** Configured for local development (`http://localhost:5173`, `http://localhost:3000`).
- **Datetime Modernization:** Updated `datetime.utcnow()` to `datetime.now(timezone.utc)` in health endpoints to prevent Python 3.14 deprecation warnings.
- **Exception Sanitization:** Service catches unexpected exceptions and maps them to clean HTTP 422 / 500 responses without exposing internal server traces or stack frames to clients.
- **Safe Model Loading:** Service uses repository-relative artifact paths with graceful fallback to `INDETERMINATE` if artifacts are missing or corrupted.

---

## 7. Files Modified & Created

### New Files Created:
1. `build_prediction_cohort.py` — Prospective cohort audit and eligibility verification script.
2. `build_feature_dataset.py` — 24-hour vital-sign feature extraction script (strict $[t_{\text{intime}}, t_{\text{intime}} + 24\text{h})$ window).
3. `validate_feature_dataset.py` — Comprehensive dataset quality and temporal validation script.
4. `train_baseline_model.py` — Baseline model training, patient-level splitting, and 5-fold grouped evaluation script.
5. `backend/app/schemas/patient_monitoring.py` — Pydantic request/response schemas for patient monitoring.
6. `backend/app/services/patient_monitoring_service.py` — Service layer for physiological validation, feature mapping, and model inference.
7. `backend/app/api/v1/endpoints/patient_monitoring.py` — FastAPI REST router for patient monitoring endpoints.
8. `backend/tests/test_patient_monitoring.py` — 28 unit and integration tests for patient monitoring.
9. `frontend/src/components/patient/PatientMonitoringView.tsx` — React component for patient vitals monitoring, screening, and risk prediction.
10. `research/patient_monitoring/*` — 19 artifact files (CSVs, JSON summaries, reports, model pickle).
11. `research/patient_monitoring/FINAL_VERIFICATION_REPORT.md` — This verification report.

### Existing Files Modified:
1. `backend/app/api/v1/router.py` — Registered patient monitoring router.
2. `backend/app/main.py` — Added `/health` endpoint and timezone-aware UTC datetime.
3. `frontend/src/App.tsx` — Registered patient monitoring tab.
4. `frontend/src/components/layout/Sidebar.tsx` — Added navigation link for patient monitoring.
5. `frontend/src/services/api.ts` — Added API methods for patient monitoring.
6. `frontend/src/types/index.ts` — Added TypeScript interfaces for patient monitoring.
7. `research/patient_monitoring/README.md` — Updated pipeline documentation, metrics, and reproduction instructions.

---

## 8. Exact Reproduction Commands

```bash
# ============================================================================
# 1. Pipeline Reproduction (from repository root)
# ============================================================================
source .venv/bin/activate

# Step 3: Run prospective cohort audit and verification
python build_prediction_cohort.py

# Step 4: Construct temporally valid 24-hour features
python build_feature_dataset.py

# Step 5: Execute comprehensive data validation and plausibility checks
python validate_feature_dataset.py

# Step 6 & 7: Train and evaluate patient-grouped baseline models
python train_baseline_model.py

# ============================================================================
# 2. Backend Testing (all 77 tests)
# ============================================================================
cd backend
PYTHONPATH=. ../.venv/bin/pytest tests
cd ..

# ============================================================================
# 3. Frontend Production Build
# ============================================================================
cd frontend
npm run build
cd ..

# ============================================================================
# 4. Starting the Application Locally
# ============================================================================
# Terminal 1: Backend
cd backend
PYTHONPATH=. ../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## 9. Clinical Disclaimer & Regulatory Notice

> **MANDATORY CLINICAL DISCLAIMER:**  
> The patient vital-sign monitoring and hospital mortality risk estimation modules in EdgeShield AI are exploratory engineering baseline implementations developed exclusively for pipeline verification and technical demonstration on the MIMIC-IV Demo research dataset.  
> They are **NOT** clinically validated, **NOT** medical devices, **NOT** FDA-cleared, and must **NEVER** be utilized for patient triage, clinical diagnosis, bedside decision-making, or real patient care.
