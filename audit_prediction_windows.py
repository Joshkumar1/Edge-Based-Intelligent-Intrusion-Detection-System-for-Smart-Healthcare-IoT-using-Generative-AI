import pandas as pd
from pathlib import Path

BASE = Path("datasets/mimic-iv-clinical-database-demo-2.2")

# Load ICU stays and hospital outcomes.
icustays = pd.read_csv(
    BASE / "icu/icustays.csv.gz",
    compression="gzip",
    parse_dates=["intime", "outtime"],
)

admissions = pd.read_csv(
    BASE / "hosp/admissions.csv.gz",
    compression="gzip",
    parse_dates=["admittime", "dischtime", "deathtime"],
)

hourly = pd.read_csv(
    "research/processed_data/patient_hourly_vitals.csv",
    parse_dates=["hour"],
)

# Link ICU stays to their hospital outcomes.
cohort = icustays.merge(
    admissions[
        [
            "subject_id",
            "hadm_id",
            "hospital_expire_flag",
            "deathtime",
        ]
    ],
    on=["subject_id", "hadm_id"],
    how="left",
    validate="many_to_one",
)

# Restrict hourly records to the first 24 hours of each ICU stay.
hourly = hourly.merge(
    icustays[["subject_id", "stay_id", "intime"]],
    on=["subject_id", "stay_id"],
    how="inner",
    validate="many_to_one",
)

hourly["hours_since_icu_admission"] = (
    hourly["hour"] - hourly["intime"]
).dt.total_seconds() / 3600

first_24h = hourly[
    (hourly["hours_since_icu_admission"] >= 0)
    & (hourly["hours_since_icu_admission"] < 24)
].copy()

# Count observed hourly rows and available core vital signs.
core_vitals = ["heart_rate", "respiratory_rate", "spo2"]

coverage = (
    first_24h.groupby(["subject_id", "stay_id"])
    .agg(
        observed_hours=("hour", "nunique"),
        hours_with_all_core_vitals=(
            "hour",
            lambda times: first_24h.loc[
                times.index, core_vitals
            ].notna().all(axis=1).sum(),
        ),
    )
    .reset_index()
)

cohort = cohort.merge(
    coverage,
    on=["subject_id", "stay_id"],
    how="left",
    validate="one_to_one",
)

cohort["observed_hours"] = cohort["observed_hours"].fillna(0)
cohort["hours_with_all_core_vitals"] = (
    cohort["hours_with_all_core_vitals"].fillna(0)
)

# Check whether the death time falls before the end of the proposed window.
cohort["death_within_first_24h"] = (
    cohort["deathtime"].notna()
    & (cohort["deathtime"] >= cohort["intime"])
    & (
        cohort["deathtime"]
        < cohort["intime"] + pd.Timedelta(hours=24)
    )
)

print("\n=== FIRST 24-HOUR COVERAGE ===")
print(
    cohort.groupby("hospital_expire_flag", dropna=False)
    .agg(
        icu_stays=("stay_id", "nunique"),
        patients=("subject_id", "nunique"),
        median_observed_hours=("observed_hours", "median"),
        stays_with_24_observations=(
            "observed_hours",
            lambda s: (s >= 24).sum(),
        ),
        stays_with_18_or_more_observations=(
            "observed_hours",
            lambda s: (s >= 18).sum(),
        ),
        deaths_within_first_24h=("death_within_first_24h", "sum"),
    )
)

print("\n=== SAMPLE OF DEATHS WITHIN FIRST 24 HOURS ===")
print(
    cohort.loc[
        cohort["death_within_first_24h"],
        [
            "subject_id",
            "hadm_id",
            "stay_id",
            "intime",
            "outtime",
            "deathtime",
            "hospital_expire_flag",
            "observed_hours",
        ],
    ].to_string(index=False)
)

print("\n=== FIRST 24-HOUR COVERAGE DATA SAVED FOR REVIEW ===")
print("Audit complete.")