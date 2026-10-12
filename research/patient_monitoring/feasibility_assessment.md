# EdgeShield AI: Clinical ML Feasibility Assessment
**Project:** EdgeShield AI — Patient Vital-Sign Monitoring & Hospital Mortality Risk  
**Dataset:** MIMIC-IV Clinical Database Demo 2.2  
**Target:** Prospective In-Hospital Mortality (`hospital_expire_flag`) after 24 Hours  
**Stage:** Step 3 Verification & Feasibility Analysis  

---

## 1. Executive Summary

This feasibility assessment examines whether the MIMIC-IV Demo dataset can support the development and statistically defensible evaluation of a predictive clinical machine learning model for hospital mortality risk.

### Core Findings
1. **Pipeline Completeness:** The data engineering pipeline (data ingestion, Celsius normalization, vital-sign quality auditing, prospective 24-hour windowing, and leak-free feature construction) is **fully functional, verified, and complete**.
2. **Descriptive Monitoring Utility:** The dataset supports **Level A (Descriptive Vital-Sign Monitoring and Data Quality Screening)** with 100% vital coverage across heart rate, respiratory rate, and SpO2.
3. **Exploratory Modeling Baseline:** The dataset supports **Level B (Exploratory Technical Baseline)** to verify feature-model pipeline interoperability, preprocessing isolation, and patient-level splitting.
4. **Clinical Validation Infeasibility:** The dataset **DOES NOT support Level C (Meaningful / Generalizable Clinical Evaluation)**. There are only **14 unique eligible deceased patients** (18 ICU stays). In any prospective evaluation partition, the test set contains fewer than 5 positive death cases, causing extreme metric volatility and making statistical inference ungeneralizable.

---

## 2. Quantitative Evidence & Class Distribution

| Cohort Dimension | Total | Hospital Mortality (Positive) | Hospital Survivors (Negative) | Prevalence |
|---|---|---|---|---|
| **Raw ICU Stays** | 140 | 20 | 120 | 14.29% |
| **Raw Unique Patients** | 100 | 15 | 89 | 15.00%* |
| **Excluded Prior to 24h** | 4 | 2 (died <= 24h) | 2 (discharged alive <= 24h) | - |
| **Eligible ICU Stays** | **136** | **18** | **118** | **13.24%** |
| **Eligible Unique Patients** | **98** | **14** | **88** | **14.29%** |
| **Patient-Split Test Partition (25%)** | 35 | 5 | 30 | 14.29% |

*\*Note: 4 patients had multiple hospitalizations with differing outcomes (survival in earlier stay, mortality in subsequent stay).*

---

## 3. Why Statistical Clinical Evaluation Is Infeasible on MIMIC-IV Demo

### A. Extreme Small-Sample Sensitivity Volatility
When a held-out test partition contains only 5 positive death instances:
- Detecting 2 of 5 deaths yields a sensitivity of **40.0%**.
- Detecting 3 of 5 deaths yields a sensitivity of **60.0%**.
- Detecting 4 of 5 deaths yields a sensitivity of **80.0%**.
A single patient prediction shifts the reported sensitivity by **20 to 40 percentage points**. The 95% Wilson confidence interval for 3/5 successes spans **[23.1%, 88.2%]**, which provides virtually zero clinical discriminatory value.

### B. High Risk of False Discovery (p >> N Problem)
The feature space contains 69 physiological and quality indicators. With only 14 positive patients in the entire dataset, the effective sample size is insufficient to estimate model parameters without substantial variance and high vulnerability to spurious correlations.

### C. Demonstration Sample Bias
MIMIC-IV Demo is an arbitrary 100-patient sub-sample created by PhysioNet for educational tutorials, query practice, and pipeline integration tests. It is not an epidemiologically representative cohort and cannot be used to estimate true hospital mortality likelihoods.

---

## 4. Methodological Safeguards & Scientific Policy

To uphold scientific integrity and adhere to clinical AI standards:
1. **No Data Fabrication:** We will not artificially synthesize positive cases (e.g., via SMOTE or generative sampling prior to partitioning).
2. **No Arbitrary Label Shifting:** We will not redefine mortality using arbitrary surrogate thresholds (e.g. labeling tachycardic episodes as "deaths") to artificially inflate the positive class.
3. **No Patient Leakage:** All data partitions strictly group by `subject_id` to guarantee that no patient appears in both training and test partitions.
4. **Mandatory Software Disclaimers:** Any model artifacts integrated into the EdgeShield AI backend must return explicit `experimental_research_only` flags and mandatory disclaimers prohibiting clinical reliance.

---

## 5. Architectural Recommendation

Proceed with:
1. **Technical Baseline Implementation:** An L2-regularized Logistic Regression and Dummy Majority classifier to demonstrate reproducible pipeline architecture and report baseline benchmarks with transparent uncertainty bounds.
2. **Patient-Monitoring Backend Service:** A dedicated FastAPI service providing vital sign validation, quality auditing, missingness detection, and experimental risk estimation.
3. **Interactive Frontend View:** A dedicated EdgeShield AI dashboard displaying patient vital monitoring, trend lines, missingness cards, and cohort audit results.
