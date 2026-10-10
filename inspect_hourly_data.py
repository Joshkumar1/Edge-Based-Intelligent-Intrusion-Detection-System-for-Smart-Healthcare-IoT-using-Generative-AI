import pandas as pd
from pathlib import Path

FILE = Path(
    "research/processed_data/patient_hourly_vitals.csv"
)

df = pd.read_csv(FILE)

vitals = [
    "heart_rate",
    "respiratory_rate",
    "spo2",
    "systolic_bp",
    "diastolic_bp",
    "mean_bp",
    "temperature_celsius",
]

print("\n=== DATASET SHAPE ===")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n=== DUPLICATE PATIENT-STAY-HOUR KEYS ===")
duplicates = df.duplicated(
    subset=["subject_id", "stay_id", "hour"]
).sum()
print(duplicates)

print("\n=== ROWS WITH ALL THREE CORE VITALS ===")
core = ["heart_rate", "respiratory_rate", "spo2"]
complete_core = df[core].notna().all(axis=1)

print("Rows with all three:", int(complete_core.sum()))
print(
    "Percentage:",
    round(complete_core.mean() * 100, 2),
    "%"
)

print("\n=== ROWS WITH NO VITAL MEASUREMENTS ===")
no_vitals = df[vitals].isna().all(axis=1)
print(int(no_vitals.sum()))

print("\n=== MEASUREMENTS AVAILABLE PER ROW ===")
print(df[vitals].notna().sum(axis=1).value_counts().sort_index())

print("\n=== HOURLY DATA SAMPLE ===")
print(df.head(10).to_string(index=False))