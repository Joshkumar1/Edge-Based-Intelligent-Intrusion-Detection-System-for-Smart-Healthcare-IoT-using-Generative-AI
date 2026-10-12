"""
Build temporally valid 24-hour feature dataset for EdgeShield AI.
Patient Vital-Sign Monitoring and Hospital Mortality Risk Research.

Principles:
1. Temporal correctness: Features use only data strictly within [intime, intime + 24h].
2. Zero leakage: Identifiers and outcome flags are stored in separate files.
3. Transparent missingness: Never fill physiological vitals with zero. Retain explicit
   missing indicators and imputation flags.
4. Independent quality flags: Track zero values, hypoxemia, and extreme HR as independent features.
"""

from pathlib import Path
import numpy as np
import pandas as pd

PROCESSED_DATA = Path("research/processed_data")
OUTPUT_DIR = Path("research/patient_monitoring")

VITAL_SIGNS = [
    "heart_rate",
    "respiratory_rate",
    "spo2",
    "systolic_bp",
    "diastolic_bp",
    "mean_bp",
    "temperature_celsius",
]


def build_features():
    print("=" * 60)
    print("EdgeShield AI: Constructing 24-Hour Feature Dataset")
    print("=" * 60)

    # 1. Load eligible cohort
    eligible_file = OUTPUT_DIR / "eligible_cohort.csv"
    if not eligible_file.exists():
        raise FileNotFoundError("Run build_prediction_cohort.py first to create eligible_cohort.csv.")

    eligible = pd.read_csv(
        eligible_file,
        parse_dates=["intime", "outtime", "prediction_time", "admittime", "dischtime", "deathtime"],
    )
    print(f"Loaded {len(eligible)} eligible ICU stays across {eligible['subject_id'].nunique()} patients.")

    # 2. Load normalized vitals
    vitals_file = PROCESSED_DATA / "mimic_vitals_normalized.csv"
    vitals = pd.read_csv(vitals_file, parse_dates=["charttime"])

    # 3. Restrict measurements strictly to [intime, prediction_time]
    merged = vitals.merge(
        eligible[["stay_id", "intime", "prediction_time"]],
        on="stay_id",
        how="inner",
    )

    # Temporal boundary condition: charttime >= intime AND charttime < prediction_time [intime, intime + 24h)
    valid_window = merged[
        (merged["charttime"] >= merged["intime"])
        & (merged["charttime"] < merged["prediction_time"])
    ].copy()

    # Calculate mid-window point (12 hours) for trend calculation
    valid_window["mid_time"] = valid_window["intime"] + pd.Timedelta(hours=12)
    valid_window["is_late_window"] = valid_window["charttime"] >= valid_window["mid_time"]

    print(f"Total valid measurements in 24h window: {len(valid_window)}")

    # 4. Extract features per stay
    feature_rows = []

    for _, stay_row in eligible.iterrows():
        sid = stay_row["stay_id"]
        pred_time = stay_row["prediction_time"]
        stay_vitals = valid_window[valid_window["stay_id"] == sid]

        row_feat = {"stay_id": sid}

        # Quality flag counts
        row_feat["flag_zero_value_count"] = int((stay_vitals["quality_flag"] == "review_zero_value").sum())
        row_feat["flag_low_spo2_count"] = int((stay_vitals["quality_flag"] == "review_low_spo2").sum())
        row_feat["flag_extreme_hr_count"] = int((stay_vitals["quality_flag"] == "review_extreme_heart_rate").sum())
        row_feat["total_flagged_observations"] = (
            row_feat["flag_zero_value_count"]
            + row_feat["flag_low_spo2_count"]
            + row_feat["flag_extreme_hr_count"]
        )

        # Distinct monitored hours
        row_feat["distinct_monitored_hours"] = int(stay_vitals["charttime"].dt.floor("h").nunique())
        row_feat["total_vital_measurements"] = int(len(stay_vitals))

        # Vital-specific features
        for v in VITAL_SIGNS:
            v_data = stay_vitals[stay_vitals["measurement"] == v]
            count = len(v_data)

            row_feat[f"{v}_count"] = int(count)
            row_feat[f"{v}_is_missing"] = int(count == 0)

            if count > 0:
                values = v_data["valuenum"].values
                sorted_v = v_data.sort_values("charttime")

                # Recent value (latest in the 24h window)
                row_feat[f"{v}_recent"] = float(sorted_v.iloc[-1]["valuenum"])
                row_feat[f"{v}_mean"] = float(np.mean(values))
                row_feat[f"{v}_min"] = float(np.min(values))
                row_feat[f"{v}_max"] = float(np.max(values))
                row_feat[f"{v}_std"] = float(np.std(values)) if count > 1 else 0.0

                # Time since last measurement in hours
                last_time = sorted_v.iloc[-1]["charttime"]
                hrs_since = (pred_time - last_time).total_seconds() / 3600.0
                row_feat[f"{v}_time_since_last_h"] = float(hrs_since)

                # Early vs late trend (hours 12-24 vs 0-12)
                early_v = v_data[~v_data["is_late_window"]]["valuenum"]
                late_v = v_data[v_data["is_late_window"]]["valuenum"]
                if len(early_v) > 0 and len(late_v) > 0:
                    row_feat[f"{v}_trend_late_minus_early"] = float(np.mean(late_v) - np.mean(early_v))
                else:
                    row_feat[f"{v}_trend_late_minus_early"] = np.nan
            else:
                row_feat[f"{v}_recent"] = np.nan
                row_feat[f"{v}_mean"] = np.nan
                row_feat[f"{v}_min"] = np.nan
                row_feat[f"{v}_max"] = np.nan
                row_feat[f"{v}_std"] = np.nan
                row_feat[f"{v}_time_since_last_h"] = 24.0  # max possible in 24h window
                row_feat[f"{v}_trend_late_minus_early"] = np.nan

        feature_rows.append(row_feat)

    features_df = pd.DataFrame(feature_rows)

    # 5. Build separate metadata and label dataframes
    metadata_df = eligible[
        [
            "subject_id",
            "hadm_id",
            "stay_id",
            "intime",
            "outtime",
            "prediction_time",
            "admittime",
            "dischtime",
            "deathtime",
        ]
    ].copy()

    labels_df = eligible[["stay_id", "subject_id", "hospital_expire_flag"]].copy()

    # Ensure consistent stay_id ordering
    features_df = features_df.sort_values("stay_id").reset_index(drop=True)
    metadata_df = metadata_df.sort_values("stay_id").reset_index(drop=True)
    labels_df = labels_df.sort_values("stay_id").reset_index(drop=True)

    # Separate feature matrix (dropping stay_id for strict ML safety)
    feature_matrix = features_df.drop(columns=["stay_id"])

    # 6. Save datasets
    features_file = OUTPUT_DIR / "features_24h.csv"
    labels_file = OUTPUT_DIR / "labels_24h.csv"
    metadata_file = OUTPUT_DIR / "metadata_cohort_24h.csv"

    features_df.to_csv(features_file, index=False)
    labels_df.to_csv(labels_file, index=False)
    metadata_df.to_csv(metadata_file, index=False)

    print(f"Saved feature dataset ({features_df.shape[0]} rows, {features_df.shape[1]} cols) to {features_file}")
    print(f"Saved label dataset ({labels_df.shape[0]} rows) to {labels_file}")
    print(f"Saved metadata dataset ({metadata_df.shape[0]} rows) to {metadata_file}")

    # 7. Generate feature summary and missingness report
    feat_summary = []
    for col in feature_matrix.columns:
        s = feature_matrix[col]
        feat_summary.append({
            "feature": col,
            "dtype": str(s.dtype),
            "missing_count": int(s.isna().sum()),
            "missing_pct": round(float(s.isna().mean() * 100), 2),
            "mean": round(float(s.mean()), 3) if np.issubdtype(s.dtype, np.number) and s.notna().any() else None,
            "std": round(float(s.std()), 3) if np.issubdtype(s.dtype, np.number) and s.notna().any() else None,
            "min": round(float(s.min()), 3) if np.issubdtype(s.dtype, np.number) and s.notna().any() else None,
            "max": round(float(s.max()), 3) if np.issubdtype(s.dtype, np.number) and s.notna().any() else None,
        })

    summary_df = pd.DataFrame(feat_summary)
    summary_file = OUTPUT_DIR / "feature_summary.csv"
    summary_df.to_csv(summary_file, index=False)

    # Vital sign missingness specific report
    vital_missing = []
    for v in VITAL_SIGNS:
        vital_missing.append({
            "vital_sign": v,
            "missing_stays_count": int(features_df[f"{v}_is_missing"].sum()),
            "missing_stays_pct": round(features_df[f"{v}_is_missing"].mean() * 100, 2),
            "median_measurements_when_present": float(features_df.loc[features_df[f"{v}_count"] > 0, f"{v}_count"].median()),
            "median_time_since_last_h": float(features_df[f"{v}_time_since_last_h"].median()),
        })

    vital_missing_df = pd.DataFrame(vital_missing)
    vital_missing_file = OUTPUT_DIR / "missingness_report.csv"
    vital_missing_df.to_csv(vital_missing_file, index=False)

    print(f"Saved feature summary to {summary_file}")
    print(f"Saved missingness report to {vital_missing_file}")

    print("\n=== VITAL SIGN AVAILABILITY IN 24H WINDOW ===")
    print(vital_missing_df.to_string(index=False))


if __name__ == "__main__":
    build_features()
