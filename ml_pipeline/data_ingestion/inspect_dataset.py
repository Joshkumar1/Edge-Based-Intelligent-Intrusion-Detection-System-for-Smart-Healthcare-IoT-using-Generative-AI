#!/usr/bin/env python3
"""
EdgeShield AI — Phase 2.1: Real Cybersecurity Dataset Ingestion & Inspection
Script: ml_pipeline/data_ingestion/inspect_dataset.py

Purpose:
- Ingest and inspect candidate real-world cybersecurity benchmark datasets (Edge-IIoTset, CICIoT2023, N-BaIoT).
- Inspect dimensions, memory consumption, column types, and data hygiene (NaN, +Inf, -Inf, duplicates).
- Analyze constant and near-constant columns to prevent dead features.
- Summarize class balance, attack distributions, and protocol frequencies.
- Evaluate compatibility with EdgeShield AI's 9 canonical edge IDS features.
- Generate a machine-readable JSON report without modifying the original dataset.
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("edgeshield.dataset_inspector")

# EdgeShield AI Canonical IDS Features
CANONICAL_IDS_FEATURES = [
    "packet_length",
    "flow_duration",
    "header_length",
    "byte_rate",
    "packet_rate",
    "tcp_syn_flag",
    "mqtt_msg_rate",
    "modbus_fn_code",
    "entropy",
]

# Candidate alias mappings for benchmark datasets (e.g. Edge-IIoTset, CIC-IoMT, Zeek/Tshark formats)
FEATURE_ALIASES: Dict[str, List[str]] = {
    "packet_length": ["frame.len", "packet_length", "tot_len", "fwd_pkt_len_mean", "pkt_len", "Length", "length"],
    "flow_duration": ["flow_duration", "duration", "Flow Duration", "frame.time_delta", "time_delta", "Duration"],
    "header_length": ["header_length", "fwd_header_len", "bwd_header_len", "ip.hdr_len", "tcp.hdr_len"],
    "byte_rate": ["byte_rate", "flow_byte_s", "Flow Bytes/s", "bytes_per_sec", "byte_rate_s"],
    "packet_rate": ["packet_rate", "flow_pkt_s", "Flow Packets/s", "packets_per_sec", "pkt_rate_s"],
    "tcp_syn_flag": ["tcp.flags.syn", "tcp_syn_flag", "tcp.connection.syn", "SYN Flag Count", "syn_flag", "tcp.flags"],
    "mqtt_msg_rate": ["mqtt_msg_rate", "mqtt.msg_rate", "mqtt_msg_count"],
    # CRITICAL: mbtcp.trans_id and mbtcp.unit_id are transaction/unit IDs, NOT function codes!
    # Only genuine Modbus function code fields are valid:
    "modbus_fn_code": ["modbus_fn_code", "modbus.fn_code", "modbus.func_code", "modbus.function_code", "mbtcp.modbus_function_code"],
    "entropy": ["entropy", "payload_entropy", "byte_entropy", "Entropy"],
}

# EdgeShield Canonical Threat Categories
CANONICAL_ATTACK_CATEGORIES = [
    "Normal",
    "Ransomware",
    "Flood DoS / DDoS",
    "Command Injection",
    "Spoofing / MITM",
    "Reconnaissance",
]


class DatasetInspector:
    def __init__(
        self,
        filepath: str,
        target_col: Optional[str] = None,
        sample_rows: Optional[int] = None,
        chunk_size: int = 100_000,
    ):
        self.filepath = Path(filepath)
        self.target_col = target_col
        self.sample_rows = sample_rows
        self.chunk_size = chunk_size

        if not self.filepath.exists():
            raise FileNotFoundError(f"Dataset file not found at: {self.filepath}")

    def inspect(self) -> Dict[str, Any]:
        logger.info(f"Starting inspection of: {self.filepath}")
        file_size_bytes = self.filepath.stat().st_size
        file_size_mb = round(file_size_bytes / (1024 * 1024), 2)
        file_size_gb = round(file_size_bytes / (1024 * 1024 * 1024), 3)

        # 1. Read dataset (or preview sample)
        logger.info(f"Reading dataset (File size: {file_size_mb} MB)...")
        if self.sample_rows:
            df = pd.read_csv(self.filepath, nrows=self.sample_rows, low_memory=False)
            is_sampled = True
        else:
            df = pd.read_csv(self.filepath, low_memory=False)
            is_sampled = False

        total_rows = len(df)
        total_cols = len(df.columns)
        memory_usage_mb = round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)

        logger.info(f"Dataset loaded: {total_rows:,} rows, {total_cols} columns ({memory_usage_mb} MB in RAM).")

        # 2. Schema and Data Types
        dtypes_summary: Dict[str, int] = {}
        column_details: List[Dict[str, Any]] = []

        for col in df.columns:
            dtype_str = str(df[col].dtype)
            dtypes_summary[dtype_str] = dtypes_summary.get(dtype_str, 0) + 1

        # 3. Missing, NaN, and Infinite Values Analysis
        logger.info("Analyzing missingness, NaN, and positive/negative infinity...")
        null_counts = df.isna().sum()
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        inf_pos_counts: Dict[str, int] = {}
        inf_neg_counts: Dict[str, int] = {}

        for col in numeric_cols:
            pos_inf = int(np.isposinf(df[col]).sum())
            neg_inf = int(np.isneginf(df[col]).sum())
            if pos_inf > 0:
                inf_pos_counts[col] = pos_inf
            if neg_inf > 0:
                inf_neg_counts[col] = neg_inf

        total_nan_cells = int(null_counts.sum())
        total_pos_inf_cells = int(sum(inf_pos_counts.values()))
        total_neg_inf_cells = int(sum(inf_neg_counts.values()))
        total_cells = total_rows * total_cols
        nan_cell_ratio = round((total_nan_cells / total_cells) * 100, 3) if total_cells > 0 else 0.0

        # Detailed column-level quality
        columns_with_missing: List[Dict[str, Any]] = []
        for col in df.columns:
            n_missing = int(null_counts[col])
            n_pos_inf = inf_pos_counts.get(col, 0)
            n_neg_inf = inf_neg_counts.get(col, 0)
            if n_missing > 0 or n_pos_inf > 0 or n_neg_inf > 0:
                columns_with_missing.append({
                    "column": col,
                    "missing_count": n_missing,
                    "missing_pct": round((n_missing / total_rows) * 100, 2),
                    "pos_inf_count": n_pos_inf,
                    "neg_inf_count": n_neg_inf,
                })

        # 4. Duplicate Rows Analysis
        logger.info("Checking for duplicate rows...")
        duplicate_count = int(df.duplicated().sum())
        duplicate_pct = round((duplicate_count / total_rows) * 100, 2) if total_rows > 0 else 0.0

        # 5. Constant and Near-Constant Columns
        logger.info("Identifying constant and near-constant columns...")
        constant_columns: List[str] = []
        near_constant_columns: List[Dict[str, Any]] = []

        for col in df.columns:
            n_unique = df[col].nunique(dropna=False)
            if n_unique <= 1:
                constant_columns.append(col)
            elif total_rows > 0:
                top_freq = df[col].value_counts(normalize=True, dropna=False).iloc[0]
                if top_freq >= 0.999:
                    near_constant_columns.append({
                        "column": col,
                        "unique_count": n_unique,
                        "dominant_value": str(df[col].mode().iloc[0]) if not df[col].mode().empty else "None",
                        "dominant_pct": round(top_freq * 100, 2),
                    })

        # 6. Target Label & Class Imbalance Analysis
        logger.info("Detecting target label column and analyzing class balance...")
        target_column_found = None
        candidate_labels = ["Attack_type", "Attack_label", "attack_type", "attack_label", "label", "Label", "class", "Class", "target"]

        if self.target_col and self.target_col in df.columns:
            target_column_found = self.target_col
        else:
            for cand in candidate_labels:
                if cand in df.columns:
                    target_column_found = cand
                    break

        label_summary: Dict[str, Any] = {}
        if target_column_found:
            counts = df[target_column_found].value_counts(dropna=False)
            total_labeled = int(counts.sum())
            dist: List[Dict[str, Any]] = []
            for label_val, count in counts.items():
                label_name = str(label_val)
                pct = round((count / total_labeled) * 100, 2)
                dist.append({
                    "label": label_name,
                    "count": int(count),
                    "percentage": pct,
                })

            majority_count = counts.iloc[0]
            minority_count = counts.iloc[-1]
            imbalance_ratio = round(majority_count / max(1, minority_count), 2)

            label_summary = {
                "detected_target_column": target_column_found,
                "num_classes": len(counts),
                "distribution": dist,
                "imbalance_ratio_majority_to_minority": imbalance_ratio,
            }
        else:
            label_summary = {
                "detected_target_column": None,
                "warning": "No standard attack label column automatically recognized.",
            }

        # 7. Protocol Distribution Analysis
        logger.info("Analyzing protocol distributions...")
        protocol_summary: Dict[str, Any] = {}
        proto_cols = ["proto", "protocol", "ip.proto", "ip.protocol", "Protocol", "frame.protocols"]
        found_proto_col = None
        for p in proto_cols:
            if p in df.columns:
                found_proto_col = p
                break

        if found_proto_col:
            proto_counts = df[found_proto_col].value_counts(dropna=False).head(15)
            protocol_summary = {
                "protocol_column": found_proto_col,
                "top_protocols": [
                    {"protocol": str(k), "count": int(v), "pct": round((v / total_rows) * 100, 2)}
                    for k, v in proto_counts.items()
                ],
            }
        else:
            # Check for protocol specific flag columns (e.g. MQTT, Modbus, TCP, UDP, HTTP)
            proto_indicators = {}
            for proto_name in ["tcp", "udp", "icmp", "http", "mqtt", "modbus", "dns"]:
                matches = [c for c in df.columns if proto_name in c.lower()]
                if matches:
                    proto_indicators[proto_name] = len(matches)
            protocol_summary = {
                "protocol_column": None,
                "protocol_feature_signatures": proto_indicators,
            }

        # 8. EdgeShield 9-Feature Compatibility Audit
        logger.info("Auditing compatibility against EdgeShield's 9 canonical IDS features...")
        feature_compatibility: Dict[str, Any] = {}
        for feat in CANONICAL_IDS_FEATURES:
            aliases = FEATURE_ALIASES.get(feat, [])
            direct_match = feat if feat in df.columns else None
            alias_match = None
            if not direct_match:
                for a in aliases:
                    if a in df.columns:
                        alias_match = a
                        break

            if direct_match:
                status = "DIRECTLY_AVAILABLE"
                mapped_col = direct_match
                notes = "Column name exactly matches canonical feature."
            elif alias_match:
                status = "DERIVABLE_OR_ALIASED"
                mapped_col = alias_match
                notes = f"Matches candidate alias '{alias_match}'."
            else:
                # Assess whether derivable or unavailable
                if feat in ["byte_rate", "packet_rate"]:
                    status = "DERIVABLE"
                    mapped_col = None
                    notes = "Derivable from byte/packet count and flow_duration."
                elif feat == "entropy":
                    status = "UNAVAILABLE"
                    mapped_col = None
                    notes = (
                        "Payload Shannon entropy is UNAVAILABLE in source tabular CSV. "
                        "Must NOT be imputed with arbitrary constant in empirical benchmark. "
                        "Config A requires documented missingness indicator; Config B excludes it."
                    )
                elif feat == "modbus_fn_code":
                    status = "UNAVAILABLE"
                    mapped_col = None
                    notes = (
                        "Valid Modbus function code field absent. mbtcp.trans_id/unit_id are "
                        "identifiers and cannot be used as function codes. Non-Modbus records "
                        "require protocol-specific encoding documentation."
                    )
                elif feat == "mqtt_msg_rate":
                    status = "DERIVABLE" if any("mqtt" in c.lower() for c in df.columns) else "UNAVAILABLE"
                    mapped_col = None
                    notes = "Derivable from MQTT flow counts or protocol timestamps."
                else:
                    status = "UNAVAILABLE"
                    mapped_col = None
                    notes = "No matching header or flow field found in dataset schema."

            feature_compatibility[feat] = {
                "status": status,
                "matched_column": mapped_col,
                "notes": notes,
            }

        # 9. Potential Target & Scenario Leakage Analysis
        logger.info("Auditing potential scenario and target leakage sources in column schema...")
        leakage_risks: List[Dict[str, str]] = []
        high_risk_patterns = [
            ("ip.src", "Source IP address leaks specific testbed attacking or victim subnets."),
            ("ip.dst", "Destination IP address leaks target server or IoT device identities."),
            ("mac", "Hardware MAC address uniquely identifies testbed interface cards."),
            ("port", "Fixed ephemeral or target port numbers can memorize specific attack tool runs."),
            ("frame.time", "Absolute capture timestamp leaks chronological scenario ordering."),
            ("attack", "Direct label or secondary attack classification flag."),
            ("label", "Direct ground-truth label flag.")
        ]
        for col in df.columns:
            col_l = col.lower()
            for pattern, reason in high_risk_patterns:
                if pattern in col_l:
                    # Ignore the designated target column itself from warning as it is the target
                    if col == target_column_found:
                        continue
                    leakage_risks.append({
                        "column": col,
                        "risk_type": pattern,
                        "warning": reason
                    })
                    break

        # 10. Distinct Feature Configurations
        config_a_canonical = {
            "name": "Configuration A (Canonical Edge Model)",
            "description": "Preserves 9-feature runtime interface for edge sensor gateways.",
            "features": CANONICAL_IDS_FEATURES,
            "unavailable_features": [f for f, r in feature_compatibility.items() if r["status"] == "UNAVAILABLE"],
            "missingness_policy": "Explicit missingness indicator or training-fitted imputation; entropy marked unavailable.",
        }
        
        # Candidate features genuinely available in typical tabular network captures
        candidate_b_features = [
            c for c in df.columns 
            if c not in [r["column"] for r in leakage_risks] 
            and c != target_column_found 
            and c not in constant_columns
            and not df[c].dtype == object
        ]
        config_b_empirical = {
            "name": "Configuration B (Expanded Empirical Benchmark)",
            "description": "Uses strictly genuine, non-leaking features available in the dataset without fabrication.",
            "candidate_feature_count": len(candidate_b_features),
            "candidate_features": candidate_b_features[:15],
            "missingness_policy": "No synthetic constants; fitted imputation strictly on training split.",
        }

        # Summary assembly
        inspection_report: Dict[str, Any] = {
            "dataset_provenance": {
                "filepath": str(self.filepath.resolve()),
                "filename": self.filepath.name,
                "file_size_mb": file_size_mb,
                "file_size_gb": file_size_gb,
                "is_sampled": is_sampled,
                "analyzed_rows": total_rows,
                "total_columns": total_cols,
                "memory_footprint_mb": memory_usage_mb,
            },
            "data_hygiene": {
                "duplicate_rows": duplicate_count,
                "duplicate_pct": duplicate_pct,
                "total_nan_cells": total_nan_cells,
                "nan_cell_ratio_pct": nan_cell_ratio,
                "total_pos_inf_cells": total_pos_inf_cells,
                "total_neg_inf_cells": total_neg_inf_cells,
                "columns_with_missing_or_inf_count": len(columns_with_missing),
                "columns_with_missing_details": columns_with_missing[:20],  # top 20
                "constant_columns": constant_columns,
                "near_constant_columns": near_constant_columns,
            },
            "labels_and_classes": label_summary,
            "protocol_analysis": protocol_summary,
            "canonical_features_compatibility": feature_compatibility,
            "leakage_risk_audit": {
                "total_flagged_columns": len(leakage_risks),
                "flagged_columns": leakage_risks,
            },
            "feature_configurations": {
                "configuration_a": config_a_canonical,
                "configuration_b": config_b_empirical,
            },
            "column_inventory": [
                {"name": col, "dtype": str(df[col].dtype)} for col in df.columns
            ],
        }

        return inspection_report


def print_cli_summary(report: Dict[str, Any]):
    prov = report["dataset_provenance"]
    hyg = report["data_hygiene"]
    lbl = report["labels_and_classes"]
    compat = report["canonical_features_compatibility"]

    print("\n" + "=" * 70)
    print("  EDGESHIELD AI — CYBERSECURITY DATASET INSPECTION REPORT")
    print("=" * 70)
    print(f"File:        {prov['filename']} ({prov['file_size_mb']} MB)")
    print(f"Dimensions:  {prov['analyzed_rows']:,} rows × {prov['total_columns']} columns")
    print(f"RAM Usage:   {prov['memory_footprint_mb']} MB (Deep memory profile)")
    print(f"Duplicates:  {hyg['duplicate_rows']:,} rows ({hyg['duplicate_pct']}%)")
    print(f"NaN Cells:   {hyg['total_nan_cells']:,} ({hyg['nan_cell_ratio_pct']}%)")
    print(f"+/- Inf:     +{hyg['total_pos_inf_cells']:,} / -{hyg['total_neg_inf_cells']:,}")
    print(f"Constant:    {len(hyg['constant_columns'])} columns")
    print(f"Near-Const:  {len(hyg['near_constant_columns'])} columns (>99.9% single value)")

    print("\n[Target Label & Class Distribution]")
    if lbl.get("detected_target_column"):
        print(f"Target Column: '{lbl['detected_target_column']}' ({lbl['num_classes']} unique classes)")
        print(f"Imbalance Ratio (Majority / Minority): {lbl['imbalance_ratio_majority_to_minority']}:1")
        for item in lbl["distribution"][:10]:
            print(f"  • {item['label']:<28} {item['count']:>8,} ({item['percentage']:>5.2f}%)")
        if len(lbl["distribution"]) > 10:
            print(f"  ... ({len(lbl['distribution']) - 10} additional classes)")
    else:
        print("  [!] No standard target column automatically detected.")

    print("\n[EdgeShield 9 Canonical IDS Features Compatibility]")
    print(f"{'Feature':<20} | {'Status':<24} | {'Matched Column / Note'}")
    print("-" * 70)
    for feat, res in compat.items():
        matched = res["matched_column"] or res["notes"]
        print(f"{feat:<20} | {res['status']:<24} | {matched}")

    leak = report.get("leakage_risk_audit", {})
    if leak.get("total_flagged_columns", 0) > 0:
        print(f"\n[Scenario & Target Leakage Risks: {leak['total_flagged_columns']} columns flagged]")
        for item in leak["flagged_columns"][:5]:
            print(f"  [!] {item['column']:<20}: {item['warning']}")
        if len(leak["flagged_columns"]) > 5:
            print(f"  ... ({len(leak['flagged_columns']) - 5} additional flagged columns in JSON)")

    configs = report.get("feature_configurations", {})
    if configs:
        cfg_a = configs.get("configuration_a", {})
        cfg_b = configs.get("configuration_b", {})
        print("\n[Dual Feature Configurations]")
        print(f"  • {cfg_a.get('name', 'Config A')}: {len(cfg_a.get('unavailable_features', []))} unavailable features.")
        print(f"  • {cfg_b.get('name', 'Config B')}: {cfg_b.get('candidate_feature_count', 0)} non-leaking native features available.")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="EdgeShield AI: Cybersecurity Benchmark Dataset Inspector"
    )
    parser.add_argument(
        "dataset_path",
        type=str,
        help="Path to local dataset CSV file (e.g., Edge-IIoTset, CICIoT2023, N-BaIoT).",
    )
    parser.add_argument(
        "--target-col",
        type=str,
        default=None,
        help="Explicit name of the label / attack type column.",
    )
    parser.add_argument(
        "--sample-rows",
        type=int,
        default=None,
        help="Optional row limit to preview large datasets without high RAM usage.",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default=None,
        help="Path to save machine-readable JSON inspection report.",
    )

    args = parser.parse_args()

    inspector = DatasetInspector(
        filepath=args.dataset_path,
        target_col=args.target_col,
        sample_rows=args.sample_rows,
    )

    report = inspector.inspect()
    print_cli_summary(report)

    output_path = args.output_json
    if not output_path:
        base_name = Path(args.dataset_path).stem
        output_path = f"presentation_output/{base_name}_inspection_report.json"

    out_p = Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_p, "w") as f:
        json.dump(report, f, indent=2)

    logger.info(f"Machine-readable inspection report saved to: {out_p.resolve()}")


if __name__ == "__main__":
    main()
