import pandas as pd
from pathlib import Path

INPUT_FILE = Path(
    "research/processed_data/mimic_vitals_quality_checked.csv"
)

OUTPUT_FILE = Path(
    "research/processed_data/mimic_vitals_normalized.csv"
)

df = pd.read_csv(INPUT_FILE)

# Convert Fahrenheit measurements into Celsius.
fahrenheit_mask = df["measurement"] == "temperature_fahrenheit"

df.loc[fahrenheit_mask, "valuenum"] = (
    df.loc[fahrenheit_mask, "valuenum"] - 32
) * 5 / 9

# Standardize the temperature measurement name.
df.loc[fahrenheit_mask, "measurement"] = "temperature_celsius"

# Standardize the temperature unit.
temperature_mask = df["measurement"] == "temperature_celsius"
df.loc[temperature_mask, "valueuom"] = "°C"

# Save a separate normalized dataset.
df.to_csv(OUTPUT_FILE, index=False)

print("\n=== NORMALIZATION SUMMARY ===")
print("Total measurements:", len(df))
print("Unique patients:", df["subject_id"].nunique())

print("\nMeasurements by type:")
print(df["measurement"].value_counts())

print("\nTemperature summary:")
print(
    df[df["measurement"] == "temperature_celsius"]["valuenum"]
    .describe()
    .round(2)
)

print("\nSaved to:", OUTPUT_FILE)