import pandas as pd
from pathlib import Path

BASE = Path("datasets/mimic-iv-clinical-database-demo-2.2")

items = pd.read_csv(BASE / "icu/d_items.csv.gz")

search_terms = {
    "Heart Rate": r"^Heart Rate$",
    "Oxygen Saturation": r"oxygen saturation|O2 saturation|SpO2",
    "Respiratory Rate": r"^Respiratory Rate$|Respiratory Rate \(Total\)",
    "Blood Pressure": r"Non Invasive Blood Pressure (systolic|diastolic|mean)|Arterial Blood Pressure (systolic|diastolic|mean)",
    "Temperature": r"Temperature Celsius|Temperature Fahrenheit",
}

for category, pattern in search_terms.items():
    results = items[
        items["label"].str.contains(
            pattern, case=False, na=False, regex=True
        )
    ]

    print(f"\n{'=' * 20} {category} {'=' * 20}")

    if results.empty:
        print("No matching measurements found.")
    else:
        print(
            results[["itemid", "label", "unitname"]]
            .to_string(index=False)
        )