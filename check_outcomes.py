import pandas as pd
from pathlib import Path

BASE = Path("datasets/mimic-iv-clinical-database-demo-2.2")

admissions = pd.read_csv(
    BASE / "hosp/admissions.csv.gz",
    compression="gzip"
)

icustays = pd.read_csv(
    BASE / "icu/icustays.csv.gz",
    compression="gzip"
)

print("\n=== HOSPITAL MORTALITY ===")
print(admissions["hospital_expire_flag"].value_counts(dropna=False))

print("\n=== HOSPITAL MORTALITY RATE ===")
print(
    admissions["hospital_expire_flag"]
    .value_counts(normalize=True, dropna=False)
    .mul(100)
    .round(2)
)

print("\n=== DEATH TIME AVAILABILITY ===")
print(admissions["deathtime"].notna().value_counts())

print("\n=== ICU STAY COUNTS ===")
print("Unique ICU stays:", icustays["stay_id"].nunique())
print("Unique patients:", icustays["subject_id"].nunique())

print("\n=== ICU STAYS LINKED TO HOSPITAL OUTCOMES ===")

merged = icustays.merge(
    admissions[
        [
            "subject_id",
            "hadm_id",
            "hospital_expire_flag",
            "deathtime",
            "admittime",
            "dischtime",
        ]
    ],
    on=["subject_id", "hadm_id"],
    how="left",
    validate="many_to_one",
)

print(
    merged[
        [
            "subject_id",
            "hadm_id",
            "stay_id",
            "intime",
            "outtime",
            "hospital_expire_flag",
            "deathtime",
        ]
    ].head(15).to_string(index=False)
)

print("\n=== ICU STAYS BY HOSPITAL OUTCOME ===")
print(
    merged.groupby("hospital_expire_flag", dropna=False)
    .agg(
        icu_stays=("stay_id", "nunique"),
        patients=("subject_id", "nunique"),
    )
)