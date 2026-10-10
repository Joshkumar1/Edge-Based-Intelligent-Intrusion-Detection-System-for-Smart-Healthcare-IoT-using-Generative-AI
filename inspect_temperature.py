import pandas as pd
from pathlib import Path

BASE = Path("datasets/mimic-iv-clinical-database-demo-2.2")

events = pd.read_csv(
    BASE / "icu/chartevents.csv.gz",
    usecols=[
        "subject_id",
        "stay_id",
        "charttime",
        "itemid",
        "value",
        "valuenum",
        "valueuom",
    ],
)

celsius = events[events["itemid"] == 223762].copy()

print("\n=== CELSIUS READINGS AT OR ABOVE 45°C ===")

suspicious = celsius[celsius["valuenum"] >= 45]

print(
    suspicious[
        [
            "subject_id",
            "stay_id",
            "charttime",
            "value",
            "valuenum",
            "valueuom",
        ]
    ].sort_values("valuenum", ascending=False).to_string(index=False)
)

print("\n=== CELSIUS VALUES ABOVE 42°C ===")
print("Count:", (celsius["valuenum"] > 42).sum())

print("\n=== CELSIUS VALUES BELOW 30°C ===")
print("Count:", (celsius["valuenum"] < 30).sum())