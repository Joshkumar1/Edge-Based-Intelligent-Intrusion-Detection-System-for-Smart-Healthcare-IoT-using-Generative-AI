import pandas as pd
from pathlib import Path

FILE = Path("research/processed_data/mimic_vitals_long.csv")

df = pd.read_csv(FILE)

print("\n=== ZERO HEART RATE RECORDS ===")
print(
    df[
        (df["measurement"] == "heart_rate")
        & (df["valuenum"] == 0)
    ][
        ["subject_id", "stay_id", "charttime", "valuenum"]
    ].head(10).to_string(index=False)
)

print("\n=== ZERO RESPIRATORY RATE RECORDS ===")
print(
    df[
        (df["measurement"] == "respiratory_rate")
        & (df["valuenum"] == 0)
    ][
        ["subject_id", "stay_id", "charttime", "valuenum"]
    ].head(10).to_string(index=False)
)

print("\n=== EXTREMELY LOW SPO2 RECORDS ===")
print(
    df[
        (df["measurement"] == "spo2")
        & (df["valuenum"] < 70)
    ][
        ["subject_id", "stay_id", "charttime", "valuenum"]
    ].sort_values("valuenum").head(15).to_string(index=False)
)

print("\n=== EXTREME HEART RATE RECORDS ===")
print(
    df[
        (df["measurement"] == "heart_rate")
        & (
            (df["valuenum"] < 30)
            | (df["valuenum"] > 180)
        )
    ][
        ["subject_id", "stay_id", "charttime", "valuenum"]
    ].head(15).to_string(index=False)
)