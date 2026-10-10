import pandas as pd
from pathlib import Path

BASE = Path("datasets/mimic-iv-clinical-database-demo-2.2")

FILES = {
    "patients": BASE / "hosp/patients.csv.gz",
    "admissions": BASE / "hosp/admissions.csv.gz",
    "diagnoses": BASE / "hosp/diagnoses_icd.csv.gz",
    "icustays": BASE / "icu/icustays.csv.gz",
}

for name, path in FILES.items():
    print("\n" + "=" * 60)
    print(f"TABLE: {name}")
    print("=" * 60)

    if not path.exists():
        print(f"File not found: {path}")
        continue

    df = pd.read_csv(path, compression="gzip", nrows=5)

    print("Columns:")
    print(df.columns.tolist())

    print("\nSample:")
    print(df.to_string(index=False))