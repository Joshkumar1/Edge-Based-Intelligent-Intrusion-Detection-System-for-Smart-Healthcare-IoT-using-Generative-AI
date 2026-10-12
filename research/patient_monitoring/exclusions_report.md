# EdgeShield AI: Exclusions and Cohort Eligibility Audit Trail
**Total ICU Stays Evaluated:** 140  
**Total Stays Included:** 136  
**Total Stays Excluded:** 4  

---

## 1. Exclusion Criteria & Justification

| Exclusion Category | Stay Count | Subject IDs | Clinical & Methodological Justification |
|---|---|---|---|
| **Death before / at 24h prediction time** | 2 | 10017492, 10025463 | Prospective prediction requires the patient to be alive at hour 24. Patients who died before hour 24 cannot be treated as prospective future outcomes. |
| **Discharged alive from hospital before / at 24h** | 2 | 10020187, 10026406 | Patients discharged prior to hour 24 left the acute inpatient setting before the observation period was complete. |

---

## 2. Excluded Records Details

| Stay ID | Subject ID | Admission Time | ICU In-Time | Death Time | Discharge Time | Exclusion Reason |
|---|---|---|---|---|---|---|
| 32554129 | 10020187 | 2170-02-24 00:00:00 | 2170-02-24 18:18:46 | nan | 2170-02-25 15:00:00 | Discharged alive from hospital before 24h prediction time |
| 36871784 | 10017492 | 2116-06-26 18:25:00 | 2116-07-05 06:50:16 | 2116-07-05 08:05:00 | 2116-07-05 08:05:00 | Died before or at 24h prediction time |
| 30864406 | 10026406 | 2129-01-03 15:55:00 | 2129-01-05 02:37:19 | nan | 2129-01-05 14:10:00 | Discharged alive from hospital before 24h prediction time |
| 38275267 | 10025463 | 2137-10-08 21:20:00 | 2137-10-09 02:51:25 | 2137-10-09 15:30:00 | 2137-10-09 15:30:00 | Died before or at 24h prediction time |
