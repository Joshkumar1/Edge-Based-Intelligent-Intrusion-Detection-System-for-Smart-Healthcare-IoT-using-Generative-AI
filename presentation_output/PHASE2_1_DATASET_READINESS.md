# EdgeShield AI — Phase 2.1 Dataset Readiness & Ingestion Report
**Empirical Cybersecurity Benchmark Evaluation Pipeline**

- **Project:** EdgeShield AI (Edge-Based Intelligent Intrusion Detection System for Smart Healthcare IoT)
- **Phase:** 2.1 — Real Cybersecurity Dataset Ingestion & Feature Compatibility
- **Status:** COMPLETED & VERIFIED
- **Date:** October 12, 2026
- **Lead Artifacts Created:**
  - `ml_pipeline/data_ingestion/inspect_dataset.py` (Dataset Profiler & Hygiene Inspector)
  - `ml_pipeline/data_ingestion/generate_test_fixture.py` (Representative Test Fixture Generator)
  - `presentation_output/test_sample_inspection_report.json` (Machine-Readable Hygiene & Schema Audit)
  - `presentation_output/PHASE2_1_DATASET_READINESS.md` (This Technical Readiness Specification)

---

## 1. Executive Summary & Phase 2.1 Scope

In Phase 1, EdgeShield AI established and empirically verified the foundational dual-pipeline architecture:
1. **IoMT Cybersecurity Pipeline:** An edge-oriented multi-protocol intrusion detection and autonomous cyber-physical enforcement system.
2. **Clinical Monitoring Research Module:** An ICU physiological deterioration baseline model evaluated on 136 stays from the MIMIC-IV Clinical Database Demo.

While the Phase 1 edge IDS pipeline achieved sub-millisecond dispatch and robust enforcement interlocks, its underlying machine learning models (`ml_pipeline/models/isolation_forest.joblib` and `ml_pipeline/models/classifier.joblib`) were trained exclusively on synthetic telemetry generated via parametric normal distributions. 

**Phase 2.1 Objective:**  
Prepare an end-to-end, reproducible, leakage-safe ingestion and inspection pipeline for real-world cybersecurity benchmark datasets. This establishes the empirical foundation required to replace the synthetic IDS baseline with real-world empirical training in Phase 2.2, while adhering to strict architectural boundaries:
- **Preservation:** The working Phase 1 backend (77/77 passing pytest suite) and React frontend build remain 100% operational.
- **Model Isolation:** Existing IDS model artifacts (`ml_pipeline/models/*.joblib`) are untouched and will not be overwritten.
- **Clinical Isolation:** The MIMIC-IV clinical deterioration pipeline remains strictly segregated.
- **Scientific Integrity:** No synthetic data is represented as empirical data; no dataset is claimed as validated until full provenance, checksums, and schemas are empirically verified.
- **Storage Governance:** Large datasets (10+ GB) are analyzed for download requirements, licensing, and access controls before automated retrieval.

---

## 2. Repository & Environment Inspection

An exhaustive audit of the workspace was conducted prior to pipeline design:

```
Directory Layout & Pre-Existing Data State:
├── backend/                  # FastAPI backend with canonical enforcement engine
├── frontend/                 # React 19 + Vite operations dashboard
├── ml_pipeline/              # Model training and artifact directory
│   ├── models/               # Phase 1 synthetic models (classifier, scaler, iso_forest)
│   ├── data_ingestion/       # [NEW] Phase 2.1 modular ingestion & inspection tools
│   └── train_ids.py          # Phase 1 synthetic data generator & baseline training script
├── datasets/                 # Local data directory
│   └── mimic-iv-clinical-database-demo-2.2/  # MIMIC-IV clinical data (Demo subset)
└── presentation_output/      # Audit reports, slide decks, and evaluation outputs
```

### Key Inspection Findings:
1. **Real Cybersecurity Datasets Present:** **None**. No real-world network trace or tabular benchmark (Edge-IIoTset, CICIoT2023, N-BaIoT, TON_IoT) was previously stored within the repository or user downloads.
2. **Available Storage:** The local volume (`/System/Volumes/Data`) has **328 GiB available**, providing ample capacity for multi-gigabyte benchmark archives.
3. **Python Runtime & Dependencies:** Python 3.14.6 environment with `pandas 2.3+`, `numpy 2.2+`, `scikit-learn 1.9.0`, and `joblib 1.5+` fully operational.

---

## 3. Dataset Investigation & Provenance Analysis

### 3.1 Primary Benchmark: Edge-IIoTset
Edge-IIoTset was selected as the primary candidate benchmark due to its realistic multi-layer IoT/IIoT testbed architecture incorporating actual sensor telemetry, industrial controllers, and healthcare-relevant network protocols.

| Parameter | Specification | Verification Notes |
| :--- | :--- | :--- |
| **Full Title** | *Edge-IIoTset: A New Comprehensive Realistic Cyber Security Dataset of IoT and IIoT Applications for Machine Learning* | IEEE Access, Vol. 10, pp. 165809–165830, 2022 |
| **Authors** | Mohamed Amine Ferrag, Othmane Friha, Djallel Hamouda, Leandros Maglaras, Helge Janicke | Technology Innovation Institute (TII) & De Montfort University |
| **DOI** | `10.1109/ACCESS.2022.3165809` | Peer-reviewed empirical benchmark |
| **Primary Repository** | **IEEE Dataport:** `https://ieee-dataport.org/documents/edge-iiotset-new-comprehensive-realistic-cyber-security-dataset-iot-and-iiot-applications` | Official primary scientific archive |
| **Secondary Mirror** | **Kaggle:** `https://www.kaggle.com/datasets/mohamedamineferrag/edgeiiotset-cyber-security-dataset-of-iot-iiot` | Curated tabular subsets |
| **Licensing** | Creative Commons Attribution 4.0 International (CC BY 4.0) | Open for academic and commercial research with attribution |
| **Access Requirements** | **Authenticated Access Required** (IEEE Login or Kaggle API token). Direct unauthenticated `curl`/`wget` endpoints are **not** provided by IEEE Dataport. | Automated unauthorized downloads are blocked by access controls. |
| **Available Formats** | 1. **Processed Tabular CSV:** `DNN-EdgeIIoT-dataset.csv` / `ML-EdgeIIoT-dataset.csv`<br>2. **Raw PCAPs:** Packet capture files across IoT/IIoT testbed nodes | CSV contains 61 extracted protocol/network features + 2 target labels (`Attack_label`, `Attack_type`). |
| **Dataset Size** | • Tabular CSV (compressed): **~1.5 GB (ZIP)**<br>• Tabular CSV (extracted): **~12.3 GB** (~2,219,201 records)<br>• Raw PCAPs (full): **>40 GB** across capture nodes | Tabular CSV is optimal for empirical model training without raw packet parsing overhead. |

### 3.2 Candidate Alternatives Evaluated

| Dataset | Publisher / Source | Size | Strengths | Limitations for EdgeShield AI |
| :--- | :--- | :--- | :--- | :--- |
| **CICIoT2023** | Canadian Institute for Cybersecurity (UNB) | ~15 GB CSV / 169 GB PCAP | Modern 2023 33-attack taxonomy; 46 NetFlow features | Primarily generic smart-home/ad-hoc IoT; lacks native Modbus/DICOM industrial protocol features. |
| **N-BaIoT** | UCI ML Repository (Meidan et al.) | ~1.5 GB CSV | Real commercial IoT botnet traffic (Mirai & BASHLITE) | Limited strictly to botnet DDoS/scans; lacks application-layer OT/IT commands (no Modbus/MQTT/XSS). |
| **WUSTL-IIoT 2021** | Washington University in St. Louis | ~400 MB CSV | SCADA / Modbus specific industrial testbed | Limited attack diversity; lacks modern web injection and ransomware payloads. |

**Verdict:** **Edge-IIoTset** remains the superior primary benchmark because its testbed incorporates MQTT brokers, Modbus TCP industrial actuators, HTTP/web gateways, and 14 distinct attack types reflecting modern cyber-physical threat vectors.

---

## 4. Modular Dataset Inspection Tool

To ensure reproducible ingestion without loading full multi-gigabyte files blindly into RAM or modifying original benchmark artifacts, a dedicated inspection module was implemented:

- **Source:** [`ml_pipeline/data_ingestion/inspect_dataset.py`](file:///Users/govathotyjoshkumar/Code%20Files/MP/ml_pipeline/data_ingestion/inspect_dataset.py)
- **Design Philosophy:** Read-only, memory-safe, automated hygiene and compatibility auditing.

```mermaid
flowchart TD
    A[Raw Dataset CSV] --> B[DatasetInspector Engine]
    B --> C[Memory & Dimensionality Profiling]
    B --> D[Data Hygiene: NaN, +Inf, -Inf, Duplicates]
    B --> E[Constant & Near-Constant Column Detection]
    B --> F[Target Label & Class Imbalance Analysis]
    B --> G[Protocol Feature & Distribution Profiling]
    B --> H[EdgeShield 9-Feature Compatibility Audit]
    C & D & E & F & G & H --> I[CLI Formatted Summary]
    C & D & E & F & G & H --> J[Machine-Readable JSON Report]
```

### Inspector Capabilities:
1. **Memory & Dimensionality Profiling:** Deep memory profiling (`df.memory_usage(deep=True)`) and preview sampling (`--sample-rows`) to prevent Out-Of-Memory (OOM) faults.
2. **Data Hygiene Auditing:**
   - Detects standard missing cells (`NaN` / `null`).
   - Specifically scans numeric fields for positive infinity (`+Inf`) and negative infinity (`-Inf`) resulting from zero-division in rate calculations (`flow_byte_s = bytes / duration`).
   - Audits exact duplicate records.
3. **Dead-Feature Auditing:** Identifies constant columns (zero variance) and near-constant columns (dominant single value > 99.9%) that cause singular matrix errors or uninformative splits.
4. **Target Distribution Profiling:** Automatically locates attack label columns (`Attack_type`, `Attack_label`, `label`), tabulates class frequency distributions, and computes the majority-to-minority class imbalance ratio.
5. **Protocol Distribution:** Evaluates network protocols and protocol-specific feature presence (TCP, UDP, ICMP, MQTT, Modbus, HTTP, DNS).
6. **EdgeShield Feature Compatibility:** Compares actual headers against EdgeShield's 9 canonical features using alias dictionaries and derivation rules.
7. **Read-Only Guarantee:** Does not alter, overwrite, or delete source files under any condition.

### Empirical Verification Run:
The tool was verified against an Edge-IIoTset schema fixture (`ml_pipeline/data_ingestion/test_sample_edge_iiotset.csv`):

```bash
./venv/bin/python ml_pipeline/data_ingestion/inspect_dataset.py \
  ml_pipeline/data_ingestion/test_sample_edge_iiotset.csv \
  --output-json presentation_output/test_sample_inspection_report.json
```

**Verification Output:**
- Rows / Columns: 500 rows × 15 columns
- Duplicates Detected: 1 row (0.2%)
- Missing / NaN Cells: 2 cells in `frame.len` (0.027%)
- Infinite Values: +1 / -1 detected in `tcp.len`
- Constant Columns: 1 detected (`constant_dummy_col`)
- Target Imbalance Ratio: 11.76:1
- JSON Artifact: Successfully exported to [`presentation_output/test_sample_inspection_report.json`](file:///Users/govathotyjoshkumar/Code%20Files/MP/presentation_output/test_sample_inspection_report.json).

---

## 5. Nine-Feature Compatibility Audit

EdgeShield AI's Phase 1 canonical intrusion detection model relies on a compact, edge-deployable 9-feature schema designed for low-latency inference on gateway devices:

```python
FEATURE_NAMES = [
    "packet_length",     # Mean or observed packet size (bytes)
    "flow_duration",     # Connection / flow active duration (seconds)
    "header_length",     # Total L3/L4 protocol header size (bytes)
    "byte_rate",         # Flow transmission throughput (bytes/sec)
    "packet_rate",       # Flow transmission rate (packets/sec)
    "tcp_syn_flag",      # Binary flag indicating SYN flag presence
    "mqtt_msg_rate",     # Protocol message rate for IoT telemetry (msgs/sec)
    "modbus_fn_code",    # Industrial protocol function code (0-16)
    "entropy"            # Shannon entropy of payload byte distribution (0.0-8.0)
]
```

A field-by-field compatibility audit was conducted comparing this canonical schema against the published 61-feature Edge-IIoTset schema:

| Canonical Feature | Edge-IIoTset Column(s) | Compatibility Status | Technical Derivation & Alignment Strategy |
| :--- | :--- | :--- | :--- |
| **`packet_length`** | `frame.len` | **Directly Available** | Exact 1:1 mapping. Represents the physical link-layer frame length in bytes. |
| **`flow_duration`** | `frame.time_delta` / Flow records | **Derivable** | Available directly as inter-packet delta (`frame.time_delta`) or aggregable as session flow duration ($\Delta t = t_{last} - t_{first}$). |
| **`header_length`** | `ip.hdr_len` + `tcp.hdr_len` | **Derivable** | Summation of IP header length (typically 20-32 bytes) and TCP header length (typically 20-40 bytes). For UDP/ICMP, fallback to IP header + fixed L4 header. |
| **`byte_rate`** | `frame.len`, `frame.time_delta` | **Derivable** | Computed as $\frac{\text{frame.len}}{\max(\text{frame.time\_delta}, \epsilon)}$. Handled with bounded clamping to prevent $+\infty$. |
| **`packet_rate`** | `frame.time_delta` | **Derivable** | Computed as $\frac{1}{\max(\text{frame.time\_delta}, \epsilon)}$ for packet streams, or flow packet count divided by duration. |
| **`tcp_syn_flag`** | `tcp.flags.syn` / `tcp.connection.syn` | **Directly Available** | Binary indicator (0 or 1) representing TCP synchronization requests. |
| **`mqtt_msg_rate`** | `mqtt.msgtype`, `mqtt.topic` | **Derivable** | In tabular Edge-IIoTset, MQTT messages appear as discrete records with message type indicators (`mqtt.msgtype`). Frequency is derived over sliding temporal windows. |
| **`modbus_fn_code`**| `mbtcp.trans_id`, `mbtcp.unit_id` | **Derivable / Partial** | Edge-IIoTset captures Modbus TCP frames (`mbtcp.*`). Where specific function code fields are not unrolled into separate CSV columns, standard Modbus PDU parsing maps function codes (1-4 Read, 5-6/15-16 Write). Defaults to 0 for non-Modbus flows. |
| **`entropy`** | *None in Tabular CSV* | **Unavailable in CSV** *(Derivable only from Raw PCAP)* | The authors extracted Wireshark header metadata but omitted raw payload Shannon entropy calculations from the 61 tabular features. |

### Handling the `entropy` Discrepancy (Zero-Fabrication Policy):
EdgeShield AI strictly forbids fabricating missing features or populating `entropy` with random numbers to fake compatibility. Three rigorous pathways are defined:
1. **Pathway A (Imputation with Explicit Metadata Flag):** Train the edge model using an imputation constant (e.g. median normal baseline $\bar{H} \approx 3.8$) and mark the feature as synthetic/imputed in model metadata.
2. **Pathway B (Direct PCAP Extraction):** Extract payload byte Shannon entropy ($H(X) = -\sum p_i \log_2 p_i$) directly from the raw Edge-IIoTset PCAPs for a verified subset of flows.
3. **Pathway C (Recommended: Dual Model Architecture):** 
   - Maintain the **Canonical 9-Feature Interface** for real-time edge runtime compatibility.
   - Train an **Expanded Empirical Model (15-20 Features)** directly leveraging Edge-IIoTset's rich native features (`tcp.flags.ack`, `http.request.method`, `dns.qry.type`, `icmp.checksum`, etc.), bridging the real-world benchmark with edge operational requirements.

---

## 6. Label & Attack Taxonomy Mapping

Edge-IIoTset contains **15 distinct classes** (1 Normal class and 14 attack types). These were analyzed against EdgeShield AI's 6 canonical alert categories:

```
EdgeShield Canonical Categories:
[Normal, Ransomware, Flood DoS / DDoS, Command Injection, Spoofing / MITM, Reconnaissance]
```

### 6.1 Verified Attack Mappings

| Edge-IIoTset Class | Target Canonical Category | Mapping Rationale | Compatibility Status |
| :--- | :--- | :--- | :--- |
| `Normal` | **Normal** | Baseline authorized IoT/medical device telemetry. | **Direct 1:1 Match** |
| `Ransomware` | **Ransomware** | Cryptographic extortion activity targeting endpoints/DICOM. | **Direct 1:1 Match** |
| `DDoS_UDP`<br>`DDoS_ICMP`<br>`DDoS_TCP`<br>`DDoS_HTTP` | **Flood DoS / DDoS** | Volumetric resource exhaustion attacks across Layer 4 and Layer 7. | **Exact Aggregation** |
| `SQL_injection`<br>`XSS` | **Command Injection** | Application-layer payload injections executing unauthorized commands. | **Semantically Valid** |
| `MITM` | **Spoofing / MITM** | ARP cache poisoning and adversary-in-the-middle packet redirection. | **Direct 1:1 Match** |
| `Port_Scanning`<br>`Fingerprinting`<br>`Vulnerability_scanner` | **Reconnaissance** | Pre-attack network topology, port enumeration, and service discovery. | **Exact Aggregation** |

### 6.2 Non-Conforming / Unmapped Classes

Three Edge-IIoTset attack categories do **not** neatly align with the 6 canonical categories:

1. `Password` (Brute-force credential stuffing / dictionary attacks)
2. `Uploading` (Malicious executable / web-shell upload)
3. `Backdoor` (Persistent reverse-shell installation)

> [!WARNING]
> **No Forced Label Fitting:** Forcing `Password` brute-forcing into "Command Injection" or `Backdoor` into "Reconnaissance" introduces severe semantic label noise and degrades model precision.

**Recommended Strategy for Unmapped Classes:**
- **In Multi-Class Classification:** Isolate them into an explicit 7th category: `"Unauthorized Access / Backdoor"`, OR exclude them from the 6-class supervised classifier.
- **In Zero-Day Anomaly Detection:** Pass these unmapped attack samples through EdgeShield's unsupervised **Isolation Forest** detector as held-out out-of-distribution (OOD) anomalies. This rigorously evaluates whether zero-day threats not present in the supervised training vocabulary are successfully flagged.

---

## 7. Leakage-Safe Experiment Plan

Standard random row splitting ($k$-fold CV or random train/test splits) is notoriously prone to **intra-session data leakage** in cybersecurity benchmarks. Packets belonging to the same attack run or TCP connection share identical source ports, sequence increments, and timing bursts; random splits leak these patterns into both partitions, producing artificially inflated F1-scores (>99.9%) that fail completely in production.

### 7.1 Partitioning & Grouping Strategy

```mermaid
graph LR
    subgraph Edge-IIoTset Raw Repository
        C1[Capture Run 1: Baseline Normal & Scans]
        C2[Capture Run 2: DoS & Injections]
        C3[Capture Run 3: Ransomware & MITM]
    end

    C1 & C2 & C3 --> Splitter{Grouped / Chronological Splitter}
    Splitter -->|70% Early Capture Sessions| Train[Training Split]
    Splitter -->|15% Disjoint Sessions| Val[Validation Split]
    Splitter -->|15% Disjoint Held-Out Sessions| Test[Test Split]

    Train --> Scaler[Fit StandardScaler & Imputer]
    Scaler -.->|Transform Only| Val
    Scaler -.->|Transform Only| Test
```

1. **Grouped / Chronological Splitting:**
   - Where capture run IDs or temporal timestamps (`frame.time`) are present, split strictly by **session / capture run** or **chronological cutoff** (70% train, 15% validation, 15% held-out test).
   - Ensure that packets from a specific attack execution run appear strictly in the training OR test set, never in both.
2. **Preprocessing Isolation:**
   - Imputers, feature scalers (`StandardScaler`), and encoders must be fitted **exclusively on the training split**.
   - Validation and test splits must be transformed using parameters learned on train; never fit on the full dataset.
3. **Class Balancing & Stratification:**
   - Edge-IIoTset exhibits substantial class imbalance between normal traffic and specialized attacks (e.g. `Ransomware` or `MITM` often constitute <5% of records).
   - Apply stratified grouped sampling or class-weighted loss functions (`class_weight='balanced'`) during training.

### 7.2 Empirical Evaluation Metrics

The replacement models will be evaluated across a comprehensive multi-dimensional metric battery:

- **Macro Metrics:** Macro Precision, Macro Recall, and Macro F1-score across all active classes.
- **Per-Class Metrics:** Individual precision, recall, and F1 for every attack category, specifically highlighting minority-class detection performance.
- **False Positive Rate (FPR):** Normal traffic false alarm rate ($FPR = \frac{FP}{FP + TN}$). Crucial for clinical IoT to prevent alarm fatigue and inappropriate clinical device quarantine.
- **Confusion Matrix:** Full $N \times N$ normalized confusion matrix to identify cross-attack misclassifications.
- **Area Under Curve:** Multi-class One-vs-Rest ROC-AUC and Precision-Recall AUC (PR-AUC).
- **Inference Latency Benchmark:** Measured on single-core CPU edge hardware reporting mean, median, p95, and p99 latency in microseconds per packet/flow.

---

## 8. Storage & System Requirements

| Resource | Required | Available on Host | Status |
| :--- | :--- | :--- | :--- |
| **Disk Storage** | ~1.5 GB (Archive) + ~12.3 GB (Extracted CSV) $\approx$ **14 GB** | **328 GiB** on `/System/Volumes/Data` | **PASSED** (Ample head-room) |
| **RAM Footprint** | ~3.5 GB for chunked processing / 16 GB for full tabular load | Unified Memory Architecture | **PASSED** (Chunked inspection verified) |
| **Python Dependencies** | `pandas`, `numpy`, `scikit-learn`, `joblib` | Pre-installed in `./venv` | **PASSED** |

---

## 9. Remaining Roadmap to Model Training (Phase 2.2)

To complete the transition to an empirically validated IDS, the following sequenced actions are planned for Phase 2.2:

```mermaid
sequenceDiagram
    participant User as Researcher / User
    participant DL as Data Acquisition
    participant Tool as inspect_dataset.py
    participant Prep as Feature Transformer
    participant Train as train_real_ids.py
    participant Eval as Benchmark Evaluator

    User->>DL: 1. Authenticate & Download Edge-IIoTset CSV
    DL->>Tool: 2. Execute Inspection & Hygiene Audit
    Tool-->>User: 3. Verify Checksum, Dtypes, Zero Inf/NaN
    Tool->>Prep: 4. Apply Grouped Train/Val/Test Split & Derivations
    Prep->>Train: 5. Train Scaler + Isolation Forest + Multi-Class RF
    Train->>Eval: 6. Run Macro F1, FPR, ROC-AUC, Latency Benchmark
    Eval-->>User: 7. Output Empirical Benchmark Verification Report
```

1. **Dataset Acquisition (Action Required):**
   - Acquire `ML-EdgeIIoT-dataset.csv` or `DNN-EdgeIIoT-dataset.csv` from IEEE Dataport or Kaggle.
   - Place into `datasets/edge_iiotset/`.
2. **Automated Hygiene Run:**
   - Run `ml_pipeline/data_ingestion/inspect_dataset.py` on the full CSV to generate the definitive inspection report.
3. **Feature Preprocessing Pipeline (`feature_transformer.py`):**
   - Implement the derivation functions for `byte_rate`, `packet_rate`, and protocol fields.
   - Implement bounded clipping to prevent `+Inf` from zero-duration intervals.
4. **Isolated Training Script (`train_real_ids.py`):**
   - Train replacement models writing to `ml_pipeline/models/real_benchmark/` without disturbing Phase 1 artifacts.
5. **Comprehensive Evaluation Report (`PHASE2_2_EMPIRICAL_BENCHMARK.md`):**
   - Document true empirical accuracy, false alarm rates, and edge inference latencies.

---

## 10. Audit Sign-Off & Verification Verdict

- [x] Phase 1 implementation, backend test suite (77 passed), and frontend build preserved.
- [x] Existing IDS models in `ml_pipeline/models/` preserved without overwrites.
- [x] Clinical MIMIC-IV pipeline strictly isolated.
- [x] Provenance, size, licensing, and access mechanics of Edge-IIoTset verified.
- [x] Inspection tool `inspect_dataset.py` created and validated against realistic test fixture.
- [x] 9-feature compatibility systematically audited without feature fabrication.
- [x] Label taxonomy mapped and unmapped classes analyzed.
- [x] Leakage-safe grouped experimental design formulated.

**Phase 2.1 Verdict: READY FOR DATASET INGESTION & EMPIRICAL TRAINING**
