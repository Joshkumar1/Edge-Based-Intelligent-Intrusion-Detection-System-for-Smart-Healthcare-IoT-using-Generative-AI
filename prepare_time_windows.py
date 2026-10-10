import pandas as pd
from pathlib import Path

INPUT_FILE = Path(
    "research/processed_data/mimic_vitals_normalized.csv"
)

OUTPUT_FILE = Path(
    "research/processed_data/patient_hourly_vitals.csv"
)

df = pd.read_csv(INPUT_FILE)

df["charttime"] = pd.to_datetime(
    df["charttime"],
    errors="coerce"
)

df = df.dropna(
    subset=["subject_id", "stay_id", "charttime", "valuenum"]
).copy()

# Round timestamps down to the beginning of each hour.
df["hour"] = df["charttime"].dt.floor("h")

# Pivot measurements into separate columns.
hourly = df.pivot_table(
    index=["subject_id", "stay_id", "hour"],
    columns="measurement",
    values="valuenum",
    aggfunc="median"
).reset_index()

hourly.columns.name = None

# Sort records chronologically within each ICU stay.
hourly = hourly.sort_values(
    ["subject_id", "stay_id", "hour"]
).reset_index(drop=True)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

hourly.to_csv(OUTPUT_FILE, index=False)

print("\n=== HOURLY DATASET SUMMARY ===")
print("Hourly rows:", len(hourly))
print("Unique patients:", hourly["subject_id"].nunique())
print("Unique ICU stays:", hourly["stay_id"].nunique())

print("\nColumns:")
print(hourly.columns.tolist())

vital_columns = [
    column for column in hourly.columns
    if column not in ["subject_id", "stay_id", "hour"]
]

print("\n=== MISSING VALUES PER VITAL SIGN ===")
print(hourly[vital_columns].isna().sum())

print("\nSaved to:", OUTPUT_FILE)