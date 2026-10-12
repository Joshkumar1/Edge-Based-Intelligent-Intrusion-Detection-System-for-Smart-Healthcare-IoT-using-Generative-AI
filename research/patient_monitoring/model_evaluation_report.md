# EdgeShield AI: Baseline Model Training & Evaluation Report
**Model Type:** Regularized Logistic Regression (L2) & Baseline Comparators  
**Target:** Prospective In-Hospital Mortality (`hospital_expire_flag`) after 24h  
**Cohort Size:** 136 Eligible Stays (98 Unique Patients)  
**Partitioning:** Grouped by `subject_id` (75% Train / 25% Test; Zero Patient Leakage)  

---

## 1. Held-Out Test Evaluation Summary (N=35 stays, 5 deaths)

| Metric | Majority-Class Baseline | Regularized Logistic Regression (L2) | Random Forest Baseline |
|---|---|---|---|
| **Accuracy** | 0.8571 | 0.8286 | 0.9143 |
| **Sensitivity (Recall)** | 0.0000 | 0.6000 | 0.6000 |
| **Specificity** | 1.0000 | 0.8667 | 0.9667 |
| **Precision** | 0.0000 | 0.4286 | 0.7500 |
| **ROC-AUC** | 0.5 | 0.7600 | 0.7667 |
| **PR-AUC** | 0.1429 | 0.6160 | 0.4894 |
| **Brier Score** | 0.1226 | 0.1268 | 0.1395 |

---

## 2. 5-Fold Grouped Cross-Validation (Out-Of-Fold Evaluation Across All 136 Stays)

Grouping strictly by `subject_id` across 5 folds ensures that all stays for a given patient are evaluated on models trained on separate patients:
- **Out-of-Fold ROC-AUC:** 0.5325
- **Out-of-Fold PR-AUC:** 0.3083
- **Out-of-Fold Sensitivity:** 0.3333
- **Out-of-Fold Specificity:** 0.8136
- **Out-of-Fold Accuracy:** 0.7500

---

## 3. Critical Methodological Limitations

1. **Small Positive Sample:** The test partition contains only 5 deaths. A single positive misclassification changes test recall by 20.0 percentage points.
2. **Confidence Intervals:** 95% Wilson confidence intervals for test sensitivity span a wide range (> 50 percentage points), indicating high uncertainty.
3. **Clinical Interpretation:** These models demonstrate technical pipeline feasibility and zero-leakage training. They are **exploratory baselines** and must never be interpreted as clinically validated risk predictors.
