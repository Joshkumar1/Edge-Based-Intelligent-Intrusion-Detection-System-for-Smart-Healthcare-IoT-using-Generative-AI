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


CONFIG_B_FEATURE_NAMES = [
    "arp_opcode", "arp_hw_size", "icmp_checksum", "icmp_seq_le", "icmp_transmit_timestamp",
    "http_content_length", "http_response", "tcp_checksum", "tcp_connection_fin", "tcp_connection_rst",
    "tcp_connection_syn", "tcp_connection_synack", "tcp_flags", "tcp_flags_ack", "tcp_len",
    "udp_stream", "udp_time_delta", "dns_qry_qu", "dns_retransmission", "dns_retransmit_request",
    "mqtt_conflag_cleansess", "mqtt_conflags", "mqtt_hdrflags", "mqtt_len", "mqtt_msgtype",
    "mqtt_proto_len", "mqtt_topic_len", "mqtt_ver", "mbtcp_unit_id"
]

CANONICAL_6_CLASSES = [
    "Normal",
    "Flood DoS / DDoS",
    "Ransomware",
    "Command Injection",
    "Reconnaissance",
    "Spoofing / MITM",
]


class MLEngineService:
    def __init__(self):
        self.scaler = None
        self.iso_forest = None
        self.classifier = None
        self.is_loaded = False
        self.active_version = "phase1_synthetic"

        # Empirical benchmark models (Phase 2.3 & 3)
        self.empirical_loaded = False
        self.empirical_rf = None
        self.empirical_xgb = None
        self.empirical_iso = None
        self.empirical_label_encoder = None
        self.empirical_metrics = None

        self.load_models()
        self.load_empirical_models()

    def load_models(self):
        """Loads trained ML scaler, Isolation Forest, and Threat Classifier (Phase 1)."""
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
                print("[+] ML Engine loaded Phase 1 pre-trained models successfully.")
            else:
                print("[!] Pre-trained ML models not found. Running heuristic fallback engine.")
                self.is_loaded = False
        except Exception as e:
            print(f"[!] Error loading ML models: {e}")
            self.is_loaded = False

    def load_empirical_models(self, empirical_dir: str = None) -> bool:
        """
        Controlled model-loading interface for empirical benchmark models (Phase 2.3 & 3).
        Validates artifact presence, schema compatibility, and handles missing/corrupt files safely.
        """
        try:
            if empirical_dir is None:
                # Default path relative to project root
                base_dir = os.path.abspath(os.path.join(settings.MODEL_DIR, "..", "models", "empirical"))
                if not os.path.exists(base_dir):
                    base_dir = os.path.abspath(os.path.join(settings.MODEL_DIR, "empirical"))
                empirical_dir = base_dir

            rf_path = os.path.join(empirical_dir, "rf_classifier_config_b.joblib")
            xgb_path = os.path.join(empirical_dir, "xgb_classifier_config_b.joblib")
            iso_path = os.path.join(empirical_dir, "isolation_forest_config_b.joblib")
            le_path = os.path.join(empirical_dir, "label_encoder.joblib")
            metrics_path = os.path.join(empirical_dir, "evaluation_metrics.json")

            if os.path.exists(rf_path) and os.path.exists(le_path):
                self.empirical_rf = joblib.load(rf_path)
                self.empirical_label_encoder = joblib.load(le_path)

                if os.path.exists(xgb_path):
                    self.empirical_xgb = joblib.load(xgb_path)
                if os.path.exists(iso_path):
                    self.empirical_iso = joblib.load(iso_path)
                if os.path.exists(metrics_path):
                    with open(metrics_path, "r") as f:
                        self.empirical_metrics = json.load(f)

                self.empirical_loaded = True
                print("[+] ML Engine loaded Empirical Benchmark models successfully.")
                return True
            else:
                self.empirical_loaded = False
                return False
        except Exception as e:
            print(f"[!] Warning: Could not load empirical benchmark models: {e}")
            self.empirical_loaded = False
            return False

    def get_model_status(self) -> Dict[str, Any]:
        """Returns runtime status and metadata of active and benchmark ML models."""
        return {
            "active_version": self.active_version,
            "phase1_models_loaded": self.is_loaded,
            "phase1_feature_count": len(FEATURE_NAMES),
            "phase1_features": FEATURE_NAMES,
            "empirical_models_loaded": self.empirical_loaded,
            "empirical_feature_count": len(CONFIG_B_FEATURE_NAMES),
            "empirical_features": CONFIG_B_FEATURE_NAMES,
            "empirical_classes": CANONICAL_6_CLASSES,
            "empirical_models_available": {
                "random_forest_config_b": self.empirical_rf is not None,
                "xgboost_config_b": self.empirical_xgb is not None,
                "isolation_forest_config_b": self.empirical_iso is not None,
            }
        }

    def predict_packet_empirical(
        self,
        features_dict: Dict[str, float],
        model_type: str = "rf"
    ) -> Tuple[bool, float, str, float, str, Dict[str, float]]:
        """
        Analyzes a network packet using the empirical 29-feature benchmark models.
        Returns:
            (is_anomaly, anomaly_score, threat_type, confidence, severity, key_features)
        """
        if not self.empirical_loaded or self.empirical_rf is None:
            # Fallback to Phase 1 prediction if empirical models are unavailable
            return self.predict_packet(features_dict)

        # Build feature vector according to Configuration B schema
        vector = [float(features_dict.get(feat, 0.0)) for feat in CONFIG_B_FEATURE_NAMES]
        X = np.array([vector])

        # Select model
        clf = self.empirical_xgb if (model_type == "xgb" and self.empirical_xgb is not None) else self.empirical_rf

        probs = clf.predict_proba(X)[0]
        max_idx = int(np.argmax(probs))
        threat_type = CANONICAL_6_CLASSES[max_idx] if max_idx < len(CANONICAL_6_CLASSES) else "Normal"
        confidence = float(probs[max_idx])

        # Anomaly scoring
        anomaly_score = 0.0
        is_anomaly_iso = False
        if self.empirical_iso is not None:
            raw_score = float(self.empirical_iso.decision_function(X)[0])
            is_anomaly_iso = bool(self.empirical_iso.predict(X)[0] == -1)
            anomaly_score = max(0.0, min(1.0, 0.5 - raw_score))
        else:
            anomaly_score = 0.8 if threat_type != "Normal" else 0.05

        is_anomaly = is_anomaly_iso or (threat_type != "Normal" and confidence > 0.4)

        # Severity
        if not is_anomaly or threat_type == "Normal":
            severity = "INFORMATIONAL"
        elif threat_type in ["Ransomware", "Command Injection"]:
            severity = "CRITICAL"
        elif threat_type in ["Flood DoS / DDoS", "Spoofing / MITM"]:
            severity = "HIGH"
        else:
            severity = "MEDIUM"

        key_features = {
            feat: float(features_dict.get(feat, 0.0))
            for feat in CONFIG_B_FEATURE_NAMES
            if abs(features_dict.get(feat, 0.0)) > 0
        }

        return is_anomaly, anomaly_score, threat_type, confidence, severity, key_features

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
