import pandas as pd
from pathlib import Path

BASE = Path("datasets/mimic-iv-clinical-database-demo-2.2")

# Load hourly vital signs.
hourly = pd.read_csv(
    "research/processed_data/patient_hourly_vitals.csv",
    parse_dates=["hour"],
)

# Load ICU stay and hospital outcome information.
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

# Join each ICU stay to its hospital admission outcome.
cohort = icustays.merge(
    admissions[
        [
            "subject_id",
            "hadm_id",
            "admittime",
            "dischtime",
            "deathtime",
            "hospital_expire_flag",
        ]
    ],
    on=["subject_id", "hadm_id"],
    how="left",
    validate="many_to_one",
)

# Calculate the observation duration available in each ICU stay.
coverage = (
    hourly.groupby(["subject_id", "stay_id"], as_index=False)
    .agg(
        first_observation=("hour", "min"),
        last_observation=("hour", "max"),
        hourly_rows=("hour", "nunique"),
    )
)

coverage["observed_hours"] = (
    coverage["last_observation"] - coverage["first_observation"]
).dt.total_seconds() / 3600

cohort = cohort.merge(
    coverage,
    on=["subject_id", "stay_id"],
    how="left",
    validate="one_to_one",
)

# Check the available cohort.
print("\n=== COHORT COUNTS ===")
print("ICU stays:", cohort["stay_id"].nunique())
print("Stays with linked outcomes:", cohort["hospital_expire_flag"].notna().sum())
print("Stays with at least 24 hours between first and last observation:",
      (cohort["observed_hours"] >= 24).sum())

print("\n=== HOSPITAL OUTCOME BY OBSERVATION COVERAGE ===")
print(
    cohort.groupby("hospital_expire_flag", dropna=False)
    .agg(
        stays=("stay_id", "nunique"),
        patients=("subject_id", "nunique"),
        median_observed_hours=("observed_hours", "median"),
        stays_with_24h=("observed_hours", lambda s: (s >= 24).sum()),
    )
)

print("\n=== DEATH TIMING RELATIVE TO ICU STAY ===")
has_death_time = cohort["deathtime"].notna()

death_during_icu = (
    has_death_time
    & (cohort["deathtime"] >= cohort["intime"])
    & (cohort["deathtime"] <= cohort["outtime"])
)

print("Admissions with a recorded death time:", int(has_death_time.sum()))
print("ICU stays whose interval contains the recorded death time:",
      int(death_during_icu.sum()))

print("\n=== SAMPLE COHORT RECORDS ===")
print(
    cohort[
        [
            "subject_id",
            "hadm_id",
            "stay_id",
            "intime",
            "outtime",
            "hospital_expire_flag",
            "deathtime",
            "observed_hours",
        ]
    ].head(15).to_string(index=False)
)