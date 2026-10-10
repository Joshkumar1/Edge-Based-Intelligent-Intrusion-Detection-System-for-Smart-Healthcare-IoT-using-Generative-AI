import pandas as pd
from pathlib import Path

BASE = Path("datasets/mimic-iv-clinical-database-demo-2.2")

file_path = BASE / "icu/chartevents.csv.gz"

df = pd.read_csv(file_path, nrows=10)

print("Columns:")
print(df.columns.tolist())

print("\nSample records:")
print(df.to_string(index=False))