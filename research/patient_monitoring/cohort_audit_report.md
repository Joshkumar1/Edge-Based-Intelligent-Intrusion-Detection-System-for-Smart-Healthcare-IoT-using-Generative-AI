# EdgeShield AI: Prospective Cohort Audit Report
**Module:** Patient Vital-Sign Monitoring and Hospital Mortality Risk Research  
**Dataset:** MIMIC-IV Clinical Database Demo 2.2  
**Target:** In-Hospital Mortality (`hospital_expire_flag`) after 24 hours  
**Prediction Window:** `[intime, intime + 24h]`

---

## 1. Executive Summary & Flow Chart

```
Total ICU Stays: 140 (100 Unique Patients)
       │
       ├── Many-to-One Linkage to Hospital Admissions: 140 (0 missing outcomes)
       │
       ▼
Prospective Filtering at Prediction Time (intime + 24h):
       ├── Excluded: Died before/at 24h: 2 stays (stay_id 36871784, 38275267)
       └── Excluded: Discharged alive before/at 24h: 2 stays (stay_id 32554129, 30864406)
       │
       ▼
Eligible Cohort: 136 ICU Stays (98 Unique Patients)
       ├── Hospital Deaths: 18 stays (14 unique patients, 13.24%)
       └── Hospital Survivors: 118 stays (88 unique patients, 86.76%)
```

---

## 2. Prospective Eligibility Verification

For a prospective clinical prediction made at 24 hours after ICU admission:
1. **Alive at Prediction Time:** Patients who died before or at 24 hours cannot be treated as future-death cases. In MIMIC-IV Demo, 2 patients died prior to 24h:
   - `stay_id 36871784` (Subject `10017492`): died at 1h 14m after ICU admission (`2116-07-05 08:05:00`).
   - `stay_id 38275267` (Subject `10025463`): died at 12h 39m after ICU admission (`2137-10-09 15:30:00`).
2. **Hospitalized at Prediction Time:** Patients discharged from the hospital alive before 24 hours are excluded:
   - `stay_id 32554129` (Subject `10020187`): discharged alive at 20.69h (`2170-02-25 15:00:00`).
   - `stay_id 30864406` (Subject `10026406`): discharged alive at 23.94h (`2129-01-05 14:10:00`).
3. **ICU Transfers vs Hospital Stays:**
   - 19 stays were discharged from the ICU to general hospital wards before 24h but remained in the hospital.
   - For all 136 eligible stays, vital sign coverage during their monitored interval was audited.

---

## 3. Vital Sign Coverage Audit (First 24 Hours)

- **Eligible Stays with Core Vital Signs (HR, RR, SpO2):** 136 / 136 (100.0%)
- **Eligible Stays with >= 18 Distinct Monitored Hours:** 126 / 136 (92.65%)
- **Eligible Stays with >= 24 Distinct Monitored Hours:** 84 / 136 (61.76%)
- **Median Monitored Hours:** 24.0 hours
- **Median Measurements per Stay:** 145.5 records

---

## 4. Patient Independence & Repeated Admissions

- **Unique Patients:** 98
- **Stays per Patient:**
  - 1 stay(s): 73 patient(s)
  - 2 stay(s): 16 patient(s)
  - 3 stay(s): 6 patient(s)
  - 4 stay(s): 2 patient(s)
  - 5 stay(s): 1 patient(s)
- **Cross-Admission Outcome Overlap:** 4 patients (10003400, 10005817, 10015931, 10023117) had multiple admissions where an earlier admission resulted in survival and a later admission resulted in hospital mortality.
> **Clinical Machine Learning Requirement:** Any model training split must group by `subject_id` to strictly prevent patient leakage across training and validation sets.

---

## 5. Timestamp Inconsistencies Audit

- `intime > outtime`: 0 cases (clean)
- `admittime > dischtime`: 0 cases (clean)
- `intime < admittime`: 2 cases (stay_ids: [35679826, 31494479]). Stays began ~35-42 minutes before formal administrative admission logging (common in emergency department to ICU transfers).
- `outtime > dischtime`: 22 cases. Discharged/deceased administrative stamp recorded slightly prior to final ICU chart checkout.
- Missing `deathtime` when `hospital_expire_flag == 1`: 0 cases (clean).
- Unexpected `deathtime` when `hospital_expire_flag == 0`: 0 cases (clean).

---

## 6. Scientific Feasibility Assessment

- **Total Positive Class Size:** 18 stays (14 unique patients).
- **Statistical Implication:** With only 14 unique deceased patients in the entire dataset, a typical 80/20 train/test split would allocate only 2 to 3 deaths to the test partition. A single prediction error would cause test sensitivity to swing by 33% to 50%.
- **Conclusion:** While the feature engineering and monitoring pipeline is fully functional and validated, this demo dataset cannot support statistically robust clinical performance claims. Any model developed must be classified strictly as an **exploratory baseline** with wide confidence intervals.
