import numpy as np
import pandas as pd

# Create a representative sample of Edge-IIoTset schema for verification
np.random.seed(42)
n_rows = 500

attack_types = [
    "Normal",
    "DDoS_UDP",
    "DDoS_ICMP",
    "SQL_injection",
    "Ransomware",
    "Port_Scanning",
    "MITM",
    "Password",
    "Uploading",
    "Backdoor"
]

data = {
    "frame.len": np.random.normal(500, 150, n_rows),
    "frame.time_delta": np.random.uniform(0.001, 1.5, n_rows),
    "ip.hdr_len": np.random.choice([20, 20, 20, 32], n_rows),
    "tcp.hdr_len": np.random.choice([20, 32], n_rows),
    "tcp.flags.syn": np.random.choice([0, 1], n_rows, p=[0.85, 0.15]),
    "tcp.flags.ack": np.random.choice([0, 1], n_rows, p=[0.3, 0.7]),
    "tcp.len": np.random.normal(300, 100, n_rows),
    "mqtt.msgtype": np.random.choice([0, 1, 2, 3], n_rows, p=[0.7, 0.1, 0.1, 0.1]),
    "mqtt.len": np.random.choice([0, 12, 64], n_rows, p=[0.7, 0.2, 0.1]),
    "mbtcp.unit_id": np.random.choice([0, 1], n_rows, p=[0.9, 0.1]),
    "ip.proto": np.random.choice(["TCP", "UDP", "ICMP", "MQTT"], n_rows, p=[0.6, 0.25, 0.1, 0.05]),
    "constant_dummy_col": [1] * n_rows,  # Constant column test
    "near_constant_col": [0] * (n_rows - 1) + [1],  # Near constant test (99.8%)
    "Attack_label": np.random.choice([0, 1], n_rows, p=[0.4, 0.6]),
    "Attack_type": np.random.choice(attack_types, n_rows, p=[0.4, 0.12, 0.1, 0.08, 0.06, 0.06, 0.06, 0.05, 0.04, 0.03]),
}

df = pd.DataFrame(data)

# Inject data quality test cases:
# 1. NaN in frame.len
df.loc[10, "frame.len"] = np.nan
df.loc[25, "frame.len"] = np.nan

# 2. +Inf and -Inf in tcp.len
df.loc[50, "tcp.len"] = np.inf
df.loc[51, "tcp.len"] = -np.inf

# 3. Duplicate row
df.loc[100] = df.loc[99].copy()

df.to_csv("ml_pipeline/data_ingestion/test_sample_edge_iiotset.csv", index=False)
print(f"Generated test fixture: {len(df)} rows, {len(df.columns)} columns.")
