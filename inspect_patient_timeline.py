import pandas as pd
from pathlib import Path

FILE = Path("research/processed_data/mimic_vitals_long.csv")

df = pd.read_csv(FILE)
df["charttime"] = pd.to_datetime(df["charttime"], errors="coerce")

# Events we want to investigate
events_to_check = [
    {
        "subject_id": 10004720,
        "stay_id": 35009126,
        "time": "2186-11-17 18:23:00",
        "reason": "Zero heart rate and low SpO2",
    },
    {
        "subject_id": 10005348,
        "stay_id": 34629895,
        "time": "2130-10-27 20:15:00",
        "reason": "Zero respiratory rate",
    },
    {
        "subject_id": 10037861,
        "stay_id": 34531557,
        "time": "2117-03-24 23:08:00",
        "reason": "Low SpO2 and zero heart rate",
    },
]

for event in events_to_check:
    target_time = pd.Timestamp(event["time"])

    nearby = df[
        (df["subject_id"] == event["subject_id"])
        & (df["stay_id"] == event["stay_id"])
        & (
            (df["charttime"] >= target_time - pd.Timedelta(minutes=30))
            & (df["charttime"] <= target_time + pd.Timedelta(minutes=30))
        )
    ].sort_values(["charttime", "measurement"])

    print("\n" + "=" * 75)
    print(event["reason"])
    print(
        f"Patient: {event['subject_id']} | "
        f"Stay: {event['stay_id']} | "
        f"Time: {target_time}"
    )
    print("=" * 75)

    print(
        nearby[
            ["charttime", "measurement", "valuenum", "valueuom"]
        ].to_string(index=False)
    )