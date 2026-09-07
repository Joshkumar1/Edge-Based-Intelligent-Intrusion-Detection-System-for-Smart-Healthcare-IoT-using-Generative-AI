import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
import joblib

# Set random seed for reproducibility
np.random.seed(42)

FEATURE_NAMES = [
    "packet_length",
    "flow_duration",
    "header_length",
    "byte_rate",
    "packet_rate",
    "tcp_syn_flag",
    "mqtt_msg_rate",
    "modbus_fn_code",
    "entropy"
]

LABELS = [
    "Normal",
    "DICOM Ransomware",
    "MQTT Flood DoS",
    "Modbus Command Injection",
    "ARP Spoofing MITM",
    "Port Scan Reconnaissance"
]


def generate_benchmark_iot_dataset(n_samples: int = 5000) -> pd.DataFrame:
    """
    Generates a synthetic IoT cybersecurity dataset modeled after Edge-IIoTset & N-BaIoT benchmarks
    customized for Smart Hospital Medical Devices (Infusion Pumps, ICU Monitors, DICOM Workstations).
    """
    data = []
    
    samples_per_class = n_samples // len(LABELS)
    
    for label_idx, label in enumerate(LABELS):
        for _ in range(samples_per_class):
            if label == "Normal":
                packet_length = np.random.normal(350, 50)
                flow_duration = np.random.uniform(0.1, 5.0)
                header_length = np.random.choice([20, 32, 40])
                byte_rate = np.random.normal(500, 100)
                packet_rate = np.random.normal(5, 2)
                tcp_syn_flag = 0
                mqtt_msg_rate = np.random.normal(2, 0.5)
                modbus_fn_code = np.random.choice([1, 2, 3, 4])  # Read functions only
                entropy = np.random.normal(3.8, 0.3)
                
            elif label == "DICOM Ransomware":
                # High entropy, large packets, encrypted burst payload targeting PACS Radiology
                packet_length = np.random.normal(1400, 100)
                flow_duration = np.random.uniform(10.0, 60.0)
                header_length = 40
                byte_rate = np.random.normal(25000, 5000)
                packet_rate = np.random.normal(80, 15)
                tcp_syn_flag = 0
                mqtt_msg_rate = 0.0
                modbus_fn_code = 0
                entropy = np.random.normal(7.8, 0.2)  # High encryption entropy
                
            elif label == "MQTT Flood DoS":
                # Massive message rate targeting smart infusion pumps
                packet_length = np.random.normal(120, 20)
                flow_duration = np.random.uniform(0.01, 1.0)
                header_length = 20
                byte_rate = np.random.normal(40000, 8000)
                packet_rate = np.random.normal(350, 50)
                tcp_syn_flag = 0
                mqtt_msg_rate = np.random.normal(400, 50)
                modbus_fn_code = 0
                entropy = np.random.normal(4.1, 0.4)
                
            elif label == "Modbus Command Injection":
                # Unauthorized write commands targeting ventilators or telemetry units
                packet_length = np.random.normal(90, 15)
                flow_duration = np.random.uniform(0.05, 0.5)
                header_length = 20
                byte_rate = np.random.normal(1200, 200)
                packet_rate = np.random.normal(15, 3)
                tcp_syn_flag = 0
                mqtt_msg_rate = 0.0
                modbus_fn_code = np.random.choice([5, 6, 15, 16])  # Force Single/Multiple Coils/Registers
                entropy = np.random.normal(2.9, 0.4)
                
            elif label == "ARP Spoofing MITM":
                # Duplicate IP/MAC traffic, high packet rates with moderate entropy
                packet_length = np.random.normal(60, 10)
                flow_duration = np.random.uniform(0.02, 0.2)
                header_length = 14
                byte_rate = np.random.normal(8000, 1500)
                packet_rate = np.random.normal(120, 20)
                tcp_syn_flag = 0
                mqtt_msg_rate = 0.0
                modbus_fn_code = 0
                entropy = np.random.normal(2.1, 0.3)
                
            elif label == "Port Scan Reconnaissance":
                # High TCP SYN flag rates with tiny packet lengths across sequential ports
                packet_length = np.random.normal(54, 5)
                flow_duration = np.random.uniform(0.001, 0.05)
                header_length = 40
                byte_rate = np.random.normal(15000, 3000)
                packet_rate = np.random.normal(250, 40)
                tcp_syn_flag = 1
                mqtt_msg_rate = 0.0
                modbus_fn_code = 0
                entropy = np.random.normal(1.8, 0.2)

            data.append({
                "packet_length": max(20.0, float(packet_length)),
                "flow_duration": max(0.001, float(flow_duration)),
                "header_length": max(14.0, float(header_length)),
                "byte_rate": max(0.0, float(byte_rate)),
                "packet_rate": max(0.0, float(packet_rate)),
                "tcp_syn_flag": int(tcp_syn_flag),
                "mqtt_msg_rate": max(0.0, float(mqtt_msg_rate)),
                "modbus_fn_code": int(modbus_fn_code),
                "entropy": min(8.0, max(0.0, float(entropy))),
                "label": label
            })
            
    return pd.DataFrame(data)


def train_models():
    print("==================================================")
    print("  EdgeShield AI - Training ML Intrusion Detector  ")
    print("==================================================")
    
    df = generate_benchmark_iot_dataset(n_samples=6000)
    
    X = df[FEATURE_NAMES]
    y = df["label"]
    
    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Fit Scaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 1. Train Unsupervised Isolation Forest (trained on Normal data for zero-day anomaly detection)
    X_train_normal = X_train_scaled[y_train == "Normal"]
    iso_forest = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    iso_forest.fit(X_train_normal)
    
    # 2. Train Multi-Class Threat Classifier (RandomForest / XGBoost)
    classifier = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    classifier.fit(X_train_scaled, y_train)
    
    # Evaluate Classifier
    y_pred = classifier.predict(X_test_scaled)
    
    macro_f1 = f1_score(y_test, y_pred, average="macro")
    macro_precision = precision_score(y_test, y_pred, average="macro")
    macro_recall = recall_score(y_test, y_pred, average="macro")
    
    print("\n[ML Evaluation Metrics]")
    print(f"-> Macro Precision : {macro_precision:.4f}")
    print(f"-> Macro Recall    : {macro_recall:.4f}")
    print(f"-> Macro F1-Score  : {macro_f1:.4f}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=LABELS))
    
    # Save artifacts
    output_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(output_dir, exist_ok=True)
    
    joblib.dump(scaler, os.path.join(output_dir, "scaler.joblib"))
    joblib.dump(iso_forest, os.path.join(output_dir, "isolation_forest.joblib"))
    joblib.dump(classifier, os.path.join(output_dir, "classifier.joblib"))
    
    metadata = {
        "features": FEATURE_NAMES,
        "labels": LABELS,
        "metrics": {
            "macro_precision": float(macro_precision),
            "macro_recall": float(macro_recall),
            "macro_f1": float(macro_f1)
        }
    }
    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"\n[+] Successfully saved trained ML models to {output_dir}")


if __name__ == "__main__":
    train_models()
