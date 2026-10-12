# EdgeShield AI: Feature Dataset Validation & Quality Report
**Pipeline Stage:** Step 3/4 Validation  
**Dataset:** MIMIC-IV Clinical Database Demo 2.2  
**Total Eligible Stays:** 136  
**Total Features Extracted:** 69

---

## 1. Automated Validation Summary

| Test Identifier | Description | Result | Details |
|---|---|---|---|
| `VAL-01` | No duplicate stay IDs | **PASS** | 0 duplicates across features, labels, and metadata |
| `VAL-02` | Strict ID alignment | **PASS** | Perfect 1-to-1 ordering across all 136 rows |
| `VAL-03` | Valid outcome labels | **PASS** | 0 missing, all labels strictly binary (0 or 1) |
| `VAL-04` | Zero target / ID leakage in features | **PASS** | No patient IDs, admission IDs, or future outcome fields |
| `VAL-05` | Zero temporal leakage | **PASS** | All features computed strictly within `[intime, intime + 24h]`. 50432 post-24h records safely excluded. |
| `VAL-06` | Physiological range review | **PASS** | Ranges reviewed; flagged readings preserved with audit trail |

---

## 2. Physiological Plausibility Audit

The table below outlines observed minimum and maximum ranges across the eligible cohort against clinical plausibility bounds:

| Vital Sign | Plausible Clinical Bound | Cohort Min | Cohort Max | Quality / Range Assessment |
|---|---|---|---|---|
| Heart Rate | 20 - 260 bpm | 29.0 | 160.0 | 1 patient with HR=0 (flagged in `flag_zero_value_count`) |
| Respiratory Rate | 0 - 70 insp/min | 0.0 | 54.0 | 14 observations with RR=0 (flagged, apneic episodes) |
| SpO2 | 50 - 100 % | 64.0 | 100.0 | Severe transient hypoxemia (min SpO2 64.0%) captured by `flag_low_spo2_count` |
| Systolic BP | 40 - 280 mmHg | 46.0 | 209.0 | Physiologically plausible ICU blood pressures |
| Diastolic BP | 20 - 180 mmHg | 19.0 | 126.0 | Physiologically plausible |
| Mean BP | 25 - 200 mmHg | 22.0 | 131.0 | Physiologically plausible |
| Temperature | 30.0 - 43.5 °C | 31.3 | 40.4 | Converted from Fahrenheit; 3 invalid extreme records previously excluded |

---

## 3. Class Balance & Patient Independence

- **Eligible Stays:** 136 (18 Deaths, 118 Survivors; Prevalence: 13.24%)
- **Eligible Unique Patients:** 98 (14 Deaths, 88 Survivors)
- **Repeated Admissions Overlap:** 4 patients had multiple admissions across survival and mortality outcomes.
- **Leakage Prevention Protocol:** All modeling evaluation must enforce grouped splitting on `subject_id`.
