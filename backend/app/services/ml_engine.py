import os
import json
import numpy as np
import joblib
from typing import Dict, Any, Tuple
from app.core.config import settings

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


class MLEngineService:
    def __init__(self):
        self.scaler = None
        self.iso_forest = None
        self.classifier = None
        self.is_loaded = False
        self.load_models()

    def load_models(self):
        """Loads trained ML scaler, Isolation Forest, and Threat Classifier."""
        try:
            model_dir = os.path.abspath(settings.MODEL_DIR)
            scaler_path = os.path.join(model_dir, "scaler.joblib")
            iso_path = os.path.join(model_dir, "isolation_forest.joblib")
            clf_path = os.path.join(model_dir, "classifier.joblib")

            if os.path.exists(scaler_path) and os.path.exists(iso_path) and os.path.exists(clf_path):
                self.scaler = joblib.load(scaler_path)
                self.iso_forest = joblib.load(iso_path)
                self.classifier = joblib.load(clf_path)
                self.is_loaded = True
                print("[+] ML Engine loaded pre-trained models successfully.")
            else:
                print("[!] Pre-trained ML models not found. Running heuristic fallback engine.")
                self.is_loaded = False
        except Exception as e:
            print(f"[!] Error loading ML models: {e}")
            self.is_loaded = False

    def predict_packet(self, features_dict: Dict[str, float]) -> Tuple[bool, float, str, float, str, Dict[str, float]]:
        """
        Analyzes a network packet feature dictionary.
        Returns:
            (is_anomaly, anomaly_score, threat_type, confidence, severity, key_features)
        """
        # Extract features vector
        vector = [features_dict.get(feat, 0.0) for feat in FEATURE_NAMES]
        
        if self.is_loaded and self.scaler and self.classifier:
            X_scaled = self.scaler.transform([vector])
            
            # 1. Isolation Forest Anomaly Score
            raw_anomaly_score = float(self.iso_forest.decision_function(X_scaled)[0])
            is_anomaly_iso = bool(self.iso_forest.predict(X_scaled)[0] == -1)
            
            # Normalize anomaly score to [0.0, 1.0] scale (higher = more anomalous)
            anomaly_score = max(0.0, min(1.0, 0.5 - raw_anomaly_score))
            
            # 2. Multi-Class Classifier
            probs = self.classifier.predict_proba(X_scaled)[0]
            max_idx = int(np.argmax(probs))
            threat_type = str(self.classifier.classes_[max_idx])
            confidence = float(probs[max_idx])
            
            is_anomaly = is_anomaly_iso or (threat_type != "Normal" and confidence > 0.4)
        else:
            # Fallback heuristic rules if model artifacts are not yet saved
            is_anomaly, anomaly_score, threat_type, confidence = self._heuristic_fallback(features_dict)

        # Determine Severity Level
        if not is_anomaly or threat_type == "Normal":
            severity = "INFORMATIONAL"
        elif threat_type in ["DICOM Ransomware", "Modbus Command Injection"] or anomaly_score > 0.8:
            severity = "CRITICAL"
        elif threat_type in ["MQTT Flood DoS", "ARP Spoofing MITM"] or anomaly_score > 0.6:
            severity = "HIGH"
        else:
            severity = "MEDIUM"

        # Calculate Key Feature Contributions (Top deviating features)
        key_features = {
            feat: float(features_dict.get(feat, 0.0))
            for feat in FEATURE_NAMES
            if features_dict.get(feat, 0.0) > 0
        }

        return is_anomaly, anomaly_score, threat_type, confidence, severity, key_features

    def _heuristic_fallback(self, features_dict: Dict[str, float]) -> Tuple[bool, float, str, float]:
        packet_len = features_dict.get("packet_length", 0.0)
        byte_rate = features_dict.get("byte_rate", 0.0)
        packet_rate = features_dict.get("packet_rate", 0.0)
        syn_flag = features_dict.get("tcp_syn_flag", 0)
        mqtt_rate = features_dict.get("mqtt_msg_rate", 0.0)
        modbus_code = features_dict.get("modbus_fn_code", 0)
        entropy = features_dict.get("entropy", 0.0)

        if entropy > 7.0 and packet_len > 1000:
            return True, 0.92, "DICOM Ransomware", 0.95
        elif mqtt_rate > 100 or packet_rate > 200:
            return True, 0.85, "MQTT Flood DoS", 0.91
        elif modbus_code in [5, 6, 15, 16]:
            return True, 0.88, "Modbus Command Injection", 0.89
        elif syn_flag == 1 and packet_rate > 150:
            return True, 0.78, "Port Scan Reconnaissance", 0.86
        elif byte_rate > 5000 and packet_len < 100:
            return True, 0.75, "ARP Spoofing MITM", 0.82
        else:
            return False, 0.05, "Normal", 0.99


ml_engine = MLEngineService()
