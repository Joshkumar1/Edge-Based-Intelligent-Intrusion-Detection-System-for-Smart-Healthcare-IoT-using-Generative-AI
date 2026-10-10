import pandas as pd
from pathlib import Path

FILE = Path("research/processed_data/mimic_vitals_long.csv")

df = pd.read_csv(FILE, parse_dates=["charttime"])

print("\n=== DATASET OVERVIEW ===")
print("Total measurements:", len(df))
print("Unique patients:", df["subject_id"].nunique())
print("Unique ICU stays:", df["stay_id"].nunique())

print("\n=== MEASUREMENT SUMMARY ===")
print(
    df.groupby("measurement")["valuenum"]
    .agg(["count", "min", "median", "max", "mean"])
    .round(2)
)

print("\n=== MEASUREMENTS PER PATIENT ===")
patient_counts = df.groupby("subject_id").size()

print(patient_counts.describe().round(2))

print("\n=== TIMESTAMP COVERAGE ===")
time_coverage = (
    df.groupby("subject_id")["charttime"]
    .agg(["min", "max"])
)

time_coverage["duration_hours"] = (
    time_coverage["max"] - time_coverage["min"]
).dt.total_seconds() / 3600

print(time_coverage["duration_hours"].describe().round(2))

print("\n=== RECORD COUNTS PER PATIENT AND MEASUREMENT ===")
counts = df.groupby(["subject_id", "measurement"]).size()

print(counts.groupby("measurement").describe().round(1))

print("\nValidation inspection complete.")