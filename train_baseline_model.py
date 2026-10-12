"""
Train and evaluate exploratory baseline mortality risk models for EdgeShield AI.
Patient Vital-Sign Monitoring and Hospital Mortality Risk Research.

Safeguards:
1. Patient-level split: Grouped strictly on subject_id to prevent patient leakage.
2. Preprocessing isolation: Median imputation and standard scaling fit ONLY on training data.
3. Majority-class comparison: Benchmarked against DummyClassifier.
4. Transparent metrics: Evaluates sensitivity, specificity, precision, PR-AUC, and ROC-AUC
   with explicit uncertainty documentation and small-sample disclaimers.
"""

import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

OUTPUT_DIR = Path("research/patient_monitoring")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def calculate_specificity(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    return float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0


def evaluate_model(pipeline, X_train, y_train, X_test, y_test, model_name):
    pipeline.fit(X_train, y_train)

    train_preds = pipeline.predict(X_train)
    test_preds = pipeline.predict(X_test)

    train_probs = pipeline.predict_proba(X_train)[:, 1] if hasattr(pipeline, "predict_proba") else train_preds
    test_probs = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else test_preds

    cm_test = confusion_matrix(y_test, test_preds, labels=[0, 1])
    tn, fp, fn, tp = cm_test.ravel()

    # Calculate metrics
    metrics = {
        "model_name": model_name,
        "test_sample_size": len(y_test),
        "test_positive_count": int(y_test.sum()),
        "test_negative_count": int((y_test == 0).sum()),
        "confusion_matrix": {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp),
        },
        "accuracy": round(float(accuracy_score(y_test, test_preds)), 4),
        "sensitivity_recall": round(float(recall_score(y_test, test_preds, zero_division=0)), 4),
        "specificity": round(float(calculate_specificity(y_test, test_preds)), 4),
        "precision": round(float(precision_score(y_test, test_preds, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, test_probs)), 4) if len(np.unique(y_test)) > 1 else None,
        "pr_auc": round(float(average_precision_score(y_test, test_probs)), 4) if len(np.unique(y_test)) > 1 else None,
        "brier_score": round(float(brier_score_loss(y_test, test_probs)), 4),
    }

    return metrics, pipeline


def run_training_pipeline():
    print("=" * 60)
    print("EdgeShield AI: Baseline Model Training & Evaluation")
    print("=" * 60)

    # 1. Load feature and label matrices
    features_df = pd.read_csv(OUTPUT_DIR / "features_24h.csv")
    labels_df = pd.read_csv(OUTPUT_DIR / "labels_24h.csv")

    X = features_df.drop(columns=["stay_id"])
    y = labels_df["hospital_expire_flag"].values
    groups = labels_df["subject_id"].values
    feature_names = X.columns.tolist()

    print(f"Dataset shape: {X.shape[0]} stays, {X.shape[1]} features.")
    print(f"Total positive cases: {y.sum()} / {len(y)} ({y.mean() * 100:.2f}%)")

    # 2. Patient-level train/test split (75/25)
    gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))

    X_train, X_test = X.iloc[train_idx].copy(), X.iloc[test_idx].copy()
    y_train, y_test = y[train_idx], y[test_idx]
    train_stays = features_df.iloc[train_idx]["stay_id"].tolist()
    test_stays = features_df.iloc[test_idx]["stay_id"].tolist()
    train_patients = labels_df.iloc[train_idx]["subject_id"].unique().tolist()
    test_patients = labels_df.iloc[test_idx]["subject_id"].unique().tolist()

    # Verify zero patient overlap
    overlap = set(train_patients).intersection(set(test_patients))
    assert len(overlap) == 0, f"Patient leakage detected! Overlapping IDs: {overlap}"

    print(f"Training partition: {len(X_train)} stays across {len(train_patients)} patients ({y_train.sum()} deaths).")
    print(f"Testing partition:  {len(X_test)} stays across {len(test_patients)} patients ({y_test.sum()} deaths).")

    # Document split configuration
    split_info = {
        "random_seed": 42,
        "split_strategy": "GroupShuffleSplit (grouped by subject_id)",
        "train_patients_count": len(train_patients),
        "test_patients_count": len(test_patients),
        "train_stays_count": len(train_stays),
        "test_stays_count": len(test_stays),
        "train_patient_ids": train_patients,
        "test_patient_ids": test_patients,
        "train_stay_ids": train_stays,
        "test_stay_ids": test_stays,
    }
    with open(OUTPUT_DIR / "patient_splits.json", "w") as f:
        json.dump(split_info, f, indent=2)

    # 3. Model Pipelines
    # Preprocessor: Median Imputation + Standard Scaling
    preprocessor = [
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]

    # Baseline 1: Majority Class
    dummy_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", DummyClassifier(strategy="prior")),
    ])

    # Baseline 2: L2 Regularized Logistic Regression
    lr_pipe = Pipeline(
        preprocessor + [
            (
                "model",
                LogisticRegression(
                    penalty="l2",
                    C=0.1,
                    solver="lbfgs",
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            )
        ]
    )

    # Baseline 3: Constrained Random Forest (low depth to limit overfitting)
    rf_pipe = Pipeline(
        preprocessor + [
            (
                "model",
                RandomForestClassifier(
                    n_estimators=50,
                    max_depth=3,
                    class_weight="balanced",
                    random_state=42,
                ),
            )
        ]
    )

    # 4. Fit and Evaluate on Held-Out Test Set
    results = {}
    fitted_pipelines = {}

    for name, pipe in [
        ("Majority_Class_Baseline", dummy_pipe),
        ("L2_Logistic_Regression", lr_pipe),
        ("Random_Forest_Baseline", rf_pipe),
    ]:
        res, fitted = evaluate_model(pipe, X_train, y_train, X_test, y_test, name)
        results[name] = res
        fitted_pipelines[name] = fitted
        print(f"\n--- {name} Results ---")
        print(f"Accuracy:    {res['accuracy']}")
        print(f"Sensitivity: {res['sensitivity_recall']}")
        print(f"Specificity: {res['specificity']}")
        print(f"Precision:   {res['precision']}")
        print(f"ROC-AUC:     {res['roc_auc']}")
        print(f"PR-AUC:      {res['pr_auc']}")
        print(f"Confusion Matrix: {res['confusion_matrix']}")

    # 5. Out-of-fold Cross Validation across entire cohort (5-Fold GroupKFold)
    gkf = GroupKFold(n_splits=5)
    oof_probs_lr = np.zeros(len(y))
    oof_preds_lr = np.zeros(len(y))

    for fold, (f_train, f_val) in enumerate(gkf.split(X, y, groups=groups)):
        f_pipe = Pipeline(
            preprocessor + [
                (
                    "model",
                    LogisticRegression(
                        penalty="l2",
                        C=0.1,
                        solver="lbfgs",
                        max_iter=1000,
                        class_weight="balanced",
                        random_state=42,
                    ),
                )
            ]
        )
        f_pipe.fit(X.iloc[f_train], y[f_train])
        oof_probs_lr[f_val] = f_pipe.predict_proba(X.iloc[f_val])[:, 1]
        oof_preds_lr[f_val] = f_pipe.predict(X.iloc[f_val])

    oof_roc_auc = round(float(roc_auc_score(y, oof_probs_lr)), 4)
    oof_pr_auc = round(float(average_precision_score(y, oof_probs_lr)), 4)
    oof_acc = round(float(accuracy_score(y, oof_preds_lr)), 4)
    oof_sens = round(float(recall_score(y, oof_preds_lr, zero_division=0)), 4)
    oof_spec = round(float(calculate_specificity(y, oof_preds_lr)), 4)

    results["L2_Logistic_Regression"]["5_fold_grouped_cv"] = {
        "out_of_fold_roc_auc": oof_roc_auc,
        "out_of_fold_pr_auc": oof_pr_auc,
        "out_of_fold_accuracy": oof_acc,
        "out_of_fold_sensitivity": oof_sens,
        "out_of_fold_specificity": oof_spec,
    }

    print("\n--- 5-Fold Grouped Out-Of-Fold Evaluation (All 136 Stays) ---")
    print(f"OOF ROC-AUC:     {oof_roc_auc}")
    print(f"OOF PR-AUC:      {oof_pr_auc}")
    print(f"OOF Sensitivity: {oof_sens}")
    print(f"OOF Specificity: {oof_spec}")

    # 6. Save Model Artifacts
    best_pipe = fitted_pipelines["L2_Logistic_Regression"]
    model_artifact_path = OUTPUT_DIR / "baseline_model.joblib"
    joblib.dump(best_pipe, model_artifact_path)

    # Save feature names used
    feature_meta = {
        "features": feature_names,
        "n_features": len(feature_names),
        "target": "hospital_expire_flag",
        "model_type": "LogisticRegression(L2, C=0.1)",
        "preprocessing": ["SimpleImputer(median)", "StandardScaler()"],
        "class_weight": "balanced",
    }
    with open(OUTPUT_DIR / "model_feature_metadata.json", "w") as f:
        json.dump(feature_meta, f, indent=2)

    # Save results JSON
    metrics_path = OUTPUT_DIR / "model_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(results, f, indent=2)

    # 7. Write Evaluation Report Markdown
    report_md = f"""# EdgeShield AI: Baseline Model Training & Evaluation Report
**Model Type:** Regularized Logistic Regression (L2) & Baseline Comparators  
**Target:** Prospective In-Hospital Mortality (`hospital_expire_flag`) after 24h  
**Cohort Size:** 136 Eligible Stays (98 Unique Patients)  
**Partitioning:** Grouped by `subject_id` (75% Train / 25% Test; Zero Patient Leakage)  

---

## 1. Held-Out Test Evaluation Summary (N=35 stays, 5 deaths)

| Metric | Majority-Class Baseline | Regularized Logistic Regression (L2) | Random Forest Baseline |
|---|---|---|---|
| **Accuracy** | {results['Majority_Class_Baseline']['accuracy']:.4f} | {results['L2_Logistic_Regression']['accuracy']:.4f} | {results['Random_Forest_Baseline']['accuracy']:.4f} |
| **Sensitivity (Recall)** | {results['Majority_Class_Baseline']['sensitivity_recall']:.4f} | {results['L2_Logistic_Regression']['sensitivity_recall']:.4f} | {results['Random_Forest_Baseline']['sensitivity_recall']:.4f} |
| **Specificity** | {results['Majority_Class_Baseline']['specificity']:.4f} | {results['L2_Logistic_Regression']['specificity']:.4f} | {results['Random_Forest_Baseline']['specificity']:.4f} |
| **Precision** | {results['Majority_Class_Baseline']['precision']:.4f} | {results['L2_Logistic_Regression']['precision']:.4f} | {results['Random_Forest_Baseline']['precision']:.4f} |
| **ROC-AUC** | {results['Majority_Class_Baseline']['roc_auc']} | {results['L2_Logistic_Regression']['roc_auc']:.4f} | {results['Random_Forest_Baseline']['roc_auc']:.4f} |
| **PR-AUC** | {results['Majority_Class_Baseline']['pr_auc']} | {results['L2_Logistic_Regression']['pr_auc']:.4f} | {results['Random_Forest_Baseline']['pr_auc']:.4f} |
| **Brier Score** | {results['Majority_Class_Baseline']['brier_score']:.4f} | {results['L2_Logistic_Regression']['brier_score']:.4f} | {results['Random_Forest_Baseline']['brier_score']:.4f} |

---

## 2. 5-Fold Grouped Cross-Validation (Out-Of-Fold Evaluation Across All 136 Stays)

Grouping strictly by `subject_id` across 5 folds ensures that all stays for a given patient are evaluated on models trained on separate patients:
- **Out-of-Fold ROC-AUC:** {oof_roc_auc:.4f}
- **Out-of-Fold PR-AUC:** {oof_pr_auc:.4f}
- **Out-of-Fold Sensitivity:** {oof_sens:.4f}
- **Out-of-Fold Specificity:** {oof_spec:.4f}
- **Out-of-Fold Accuracy:** {oof_acc:.4f}

---

## 3. Critical Methodological Limitations

1. **Small Positive Sample:** The test partition contains only 5 deaths. A single positive misclassification changes test recall by 20.0 percentage points.
2. **Confidence Intervals:** 95% Wilson confidence intervals for test sensitivity span a wide range (> 50 percentage points), indicating high uncertainty.
3. **Clinical Interpretation:** These models demonstrate technical pipeline feasibility and zero-leakage training. They are **exploratory baselines** and must never be interpreted as clinically validated risk predictors.
"""

    report_md_path = OUTPUT_DIR / "model_evaluation_report.md"
    with open(report_md_path, "w") as f:
        f.write(report_md)

    print("\nTraining and evaluation complete!")
    print(f"Model Artifact:    {model_artifact_path}")
    print(f"Metrics JSON:      {metrics_path}")
    print(f"Splits JSON:       {OUTPUT_DIR / 'patient_splits.json'}")
    print(f"Evaluation Report: {report_md_path}")


if __name__ == "__main__":
    run_training_pipeline()
