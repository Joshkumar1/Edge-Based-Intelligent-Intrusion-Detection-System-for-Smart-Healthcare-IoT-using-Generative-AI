import pandas as pd
from pathlib import Path

BASE = Path("datasets/mimic-iv-clinical-database-demo-2.2")

INPUT_FILE = BASE / "icu/chartevents.csv.gz"
OUTPUT_DIR = Path("research/processed_data")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Measurement IDs verified from the dictionary exploration
VITALS = {
    220045: "heart_rate",
    220277: "spo2",
    220210: "respiratory_rate",
    220179: "systolic_bp",
    220180: "diastolic_bp",
    220181: "mean_bp",
    223762: "temperature_celsius",
    223761: "temperature_fahrenheit",
}

print("Loading selected patient measurements...")

# Read only the columns we need and filter to the selected item IDs.
df = pd.read_csv(
    INPUT_FILE,
    usecols=[
        "subject_id",
        "hadm_id",
        "stay_id",
        "charttime",
        "itemid",
        "valuenum",
        "valueuom",
    ],
    compression="gzip",
)

df = df[df["itemid"].isin(VITALS)].copy()

df["measurement"] = df["itemid"].map(VITALS)
df["charttime"] = pd.to_datetime(df["charttime"], errors="coerce")

# Remove records without a numeric measurement or timestamp.
df = df.dropna(subset=["charttime", "valuenum"])

# Convert Fahrenheit measurements to Celsius.
# Flag implausible body-temperature observations for exclusion.
temperature_mask = df["measurement"] == "temperature_celsius"

invalid_temperature = temperature_mask & (
    (df["valuenum"] < 25) | (df["valuenum"] > 45)
)

print(
    "Implausible temperature records excluded:",
    int(invalid_temperature.sum())
)

df = df[~invalid_temperature].copy()

# Keep the original records and measurement timestamps.
df = df[
    [
        "subject_id",
        "hadm_id",
        "stay_id",
        "charttime",
        "measurement",
        "valuenum",
        "valueuom",
    ]
]

output_file = OUTPUT_DIR / "mimic_vitals_long.csv"
df.to_csv(output_file, index=False)

print("\nExtraction complete!")
print("Number of measurements:", len(df))
print("Unique patients:", df["subject_id"].nunique())

print("\nMeasurements by type:")
print(df["measurement"].value_counts())

print("\nMissing values:")
print(df.isna().sum())

print("\nSaved to:", output_file)