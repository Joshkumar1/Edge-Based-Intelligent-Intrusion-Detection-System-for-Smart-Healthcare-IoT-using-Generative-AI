#!/usr/bin/env python3
"""
Unit tests for EdgeShield AI Phase 2 Feature Extraction and Inspection Pipeline
Test suite: ml_pipeline/data_ingestion/test_feature_extractor.py
"""

import os
import shutil
import tempfile
import numpy as np
import pandas as pd
import pytest

from ml_pipeline.data_ingestion.feature_extractor import FeatureExtractor, compute_sha256
from ml_pipeline.data_ingestion.inspect_dataset import DatasetInspector


@pytest.fixture
def sample_test_csv(tmp_path):
    """Generates a small test dataset with known edge cases."""
    csv_file = tmp_path / "test_data.csv"
    data = {
        "frame.len": [100.0, 500.0, np.nan, 1400.0, 64.0, 1200.0, 300.0, 450.0, 80.0, 1500.0],
        "frame.time_delta": [0.01, 0.0, 0.5, 1.2, 0.001, 0.05, 0.1, 0.2, 0.02, 0.8],  # includes 0.0 for division by zero test
        "ip.hdr_len": [20, 20, 20, 32, 20, 20, 20, 20, 20, 20],
        "tcp.hdr_len": [20, 32, 20, 32, 20, 20, 20, 20, 20, 20],
        "tcp.flags.syn": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        "tcp.flags.ack": [0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        "tcp.len": [60.0, 448.0, 0.0, np.inf, 24.0, 1160.0, -np.inf, 410.0, 40.0, 1460.0],  # includes +inf and -inf
        "mqtt.msgtype": [0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
        "mqtt.len": [0, 0, 32, 0, 0, 64, 0, 0, 0, 0],
        "mbtcp.unit_id": [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        "Attack_type": [
            "Normal",
            "DDoS_UDP",
            "SQL_injection",
            "Ransomware",
            "Port_Scanning",
            "MITM",
            "Password",  # OOD class
            "Uploading", # OOD class
            "Normal",
            "Normal",
        ],
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    return csv_file


def test_sha256_checksum(sample_test_csv):
    checksum = compute_sha256(sample_test_csv)
    assert isinstance(checksum, str)
    assert len(checksum) == 64


def test_config_a_extraction_and_entropy_policy(sample_test_csv, tmp_path):
    out_dir = tmp_path / "out_features"
    extractor = FeatureExtractor(input_csv=str(sample_test_csv), output_dir=str(out_dir))
    df = pd.read_csv(sample_test_csv)
    
    extracted, meta = extractor.extract_config_a(df)
    
    # 1. 9 Canonical columns present
    for col in ["packet_length", "flow_duration", "header_length", "byte_rate", "packet_rate", "tcp_syn_flag", "mqtt_msg_rate", "modbus_fn_code"]:
        assert col in extracted.columns
    
    # 2. Entropy policy: Must NOT be imputed with constant 3.8
    assert "entropy" in extracted.columns
    assert extracted["entropy"].isna().all(), "Raw extracted entropy must be NaN/missing, not fabricated constant"
    assert "entropy_is_missing" in extracted.columns
    assert (extracted["entropy_is_missing"] == 1.0).all()

    # 3. Modbus function code integrity: mbtcp.unit_id must NOT be mapped as modbus_fn_code
    assert meta["modbus_fn_code_status"] == "UNAVAILABLE_ENCODED_ZERO"
    assert (extracted["modbus_fn_code"] == 0).all()

    # 4. Division by zero in byte_rate and packet_rate must be safely clamped and finite
    assert np.isfinite(extracted["byte_rate"]).all()
    assert np.isfinite(extracted["packet_rate"]).all()
    assert (extracted["byte_rate"] >= 0.0).all()


def test_config_b_extraction(sample_test_csv, tmp_path):
    out_dir = tmp_path / "out_features"
    extractor = FeatureExtractor(input_csv=str(sample_test_csv), output_dir=str(out_dir))
    df = pd.read_csv(sample_test_csv)
    
    extracted, meta = extractor.extract_config_b(df)
    
    # Check that genuine fields exist
    assert "frame_length" in extracted.columns
    assert "tcp_flags_syn" in extracted.columns
    assert "tcp_len" in extracted.columns
    # Check that infinite tcp.len was clamped and is finite
    assert np.isfinite(extracted["tcp_len"]).all()


def test_label_mapping_and_ood_isolation(sample_test_csv, tmp_path):
    out_dir = tmp_path / "out_features"
    extractor = FeatureExtractor(input_csv=str(sample_test_csv), output_dir=str(out_dir))
    df = pd.read_csv(sample_test_csv)
    
    canonical_y, is_ood = extractor.map_labels(df["Attack_type"])
    
    # Normal -> Normal
    assert canonical_y[0] == "Normal"
    # DDoS_UDP -> Flood DoS / DDoS
    assert canonical_y[1] == "Flood DoS / DDoS"
    # SQL_injection -> Command Injection
    assert canonical_y[2] == "Command Injection"
    # Password & Uploading -> Marked as OOD, NOT forced into canonical classes
    assert is_ood[6] == True
    assert is_ood[7] == True
    assert pd.isna(canonical_y[6])
    assert pd.isna(canonical_y[7])


def test_dataset_inspector_on_sample(sample_test_csv):
    inspector = DatasetInspector(filepath=str(sample_test_csv))
    report = inspector.inspect()
    
    assert report["dataset_provenance"]["analyzed_rows"] == 10
    assert report["data_hygiene"]["total_pos_inf_cells"] == 1
    assert report["data_hygiene"]["total_neg_inf_cells"] == 1
    assert report["canonical_features_compatibility"]["entropy"]["status"] == "UNAVAILABLE"
    assert report["canonical_features_compatibility"]["modbus_fn_code"]["status"] == "UNAVAILABLE"


def test_real_dataset_audit_and_checksum():
    real_path = "datasets/edge_iiotset/selected_ml/ML-EdgeIIoT-dataset.csv"
    if not os.path.exists(real_path):
        pytest.skip("Real dataset not present locally.")
        
    checksum = compute_sha256(real_path)
    assert checksum == "53101fad091af20bee815860962a5016b802ee45d456a141042f6183094c3c1a"
    
    df_sample = pd.read_csv(real_path, nrows=50, low_memory=False)
    assert len(df_sample.columns) == 63
    assert "Attack_type" in df_sample.columns
    assert "Attack_label" in df_sample.columns
    
    extractor = FeatureExtractor(input_csv=real_path)
    extracted_b, meta_b = extractor.extract_config_b(df_sample)
    assert len(extracted_b.columns) >= 20
    assert np.isfinite(extracted_b.values).all()
