import pandas as pd
from pathlib import Path

INPUT_FILE = Path("research/processed_data/mimic_vitals_long.csv")
OUTPUT_FILE = Path(
    "research/processed_data/mimic_vitals_quality_checked.csv"
)

df = pd.read_csv(INPUT_FILE)

# Preserve the original values.
df["quality_flag"] = "reviewed"

# Flag zero heart-rate and respiratory-rate readings.
zero_measurements = {
    "heart_rate",
    "respiratory_rate",
}

zero_mask = (
    df["measurement"].isin(zero_measurements)
    & (df["valuenum"] == 0)
)

df.loc[zero_mask, "quality_flag"] = "review_zero_value"

# Flag unusually low oxygen-saturation readings.
spo2_mask = (
    (df["measurement"] == "spo2")
    & (df["valuenum"] < 70)
)

df.loc[spo2_mask, "quality_flag"] = "review_low_spo2"

# Flag unusually low or high heart rates for investigation.
heart_rate_mask = (
    (df["measurement"] == "heart_rate")
    & (
        (df["valuenum"] < 30)
        | (df["valuenum"] > 180)
    )
)

df.loc[heart_rate_mask, "quality_flag"] = "review_extreme_heart_rate"

# Save a separate file so the original extracted dataset is unchanged.
df.to_csv(OUTPUT_FILE, index=False)

print("\n=== QUALITY FLAG COUNTS ===")
print(df["quality_flag"].value_counts())

print("\n=== FLAGGED RECORDS ===")
flagged = df[df["quality_flag"] != "reviewed"]

print(
    flagged[
        [
            "subject_id",
            "stay_id",
            "charttime",
            "measurement",
            "valuenum",
            "quality_flag",
        ]
    ].sort_values(["subject_id", "charttime"]).to_string(index=False)
)

print(f"\nSaved quality-checked dataset to: {OUTPUT_FILE}")