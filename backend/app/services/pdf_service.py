import os
import re
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import fitz  # PyMuPDF
from pypdf import PdfReader

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../backend/uploads"))
DOCS_METADATA_FILE = os.path.join(UPLOAD_DIR, "documents.json")

# Ensure uploads folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


class PDFService:
    def __init__(self):
        self._ensure_default_document()

    def _ensure_default_document(self):
        """Seeds the default IEEE Research Paper if no documents exist."""
        docs = self._load_documents_metadata()
        if not docs:
            default_doc = self._create_default_ieee_paper()
            docs[default_doc["id"]] = default_doc
            self._save_documents_metadata(docs)

    def _load_documents_metadata(self) -> Dict[str, Any]:
        if os.path.exists(DOCS_METADATA_FILE):
            try:
                with open(DOCS_METADATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[!] Failed to read documents metadata: {e}")
        return {}

    def _save_documents_metadata(self, data: Dict[str, Any]):
        try:
            with open(DOCS_METADATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[!] Failed to save documents metadata: {e}")

    def _create_default_ieee_paper(self) -> Dict[str, Any]:
        """Creates pre-indexed content for the IEEE research paper."""
        doc_id = "DOC-IEEE-EDGESHIELD-2026"
        pages = [
            {
                "page_number": 1,
                "title": "Abstract & Introduction",
                "sections": [
                    {
                        "heading": "Abstract",
                        "content": (
                            "EdgeShield AI presents a privacy-preserving, dual-stage machine learning and "
                            "explainable Small Language Model (SLM) architecture engineered specifically for "
                            "smart healthcare Internet of Things (IoT) ecosystems. In life-critical hospital environments—"
                            "where infusion pumps, ICU patient monitors, smart ventilators, and DICOM radiology workstations "
                            "operate continuously—cryptic security alerts cause cognitive fatigue and dangerous response delays. "
                            "Our proposed framework achieves 99.24% macro precision, 98.91% macro recall, and 99.07% F1-score "
                            "with a sub-millisecond edge inference latency (< 1.2 ms) while guaranteeing zero data leakage by "
                            "executing local SLMs offline."
                        )
                    },
                    {
                        "heading": "I. Introduction",
                        "content": (
                            "The rapid proliferation of IoMT (Internet of Medical Things) devices has drastically expanded "
                            "the cyberattack surface of modern clinical facilities. Traditional cloud-based intrusion detection systems (IDS) "
                            "introduce severe network round-trip latencies (>250 ms), cloud dependencies during network outages, "
                            "and grave privacy non-compliance under HIPAA, HITECH, and GDPR mandates. EdgeShield AI is engineered "
                            "to execute entirely on edge gateways (such as NVIDIA Jetson and industrial x86 hardware) directly adjacent "
                            "to hospital local area networks."
                        )
                    }
                ]
            },
            {
                "page_number": 2,
                "title": "Smart Hospital Threat Taxonomy",
                "sections": [
                    {
                        "heading": "II. Healthcare Threat Vectors & Clinical Risks",
                        "content": (
                            "Smart hospital IoT networks exhibit unique protocol vulnerabilities across three distinct operational layers:\n"
                            "1. DICOM Image Ransomware: Attackers exploit TCP port 104 to transmit high-entropy encrypted payloads "
                            "into PACS (Picture Archiving and Communication System) servers, locking diagnostic CT/MRI scans and halting emergency surgery.\n"
                            "2. MQTT Telemetry Flooding (DoS): Distributed flood of malformed PUBLISH frames targeting MQTT brokers on ports 1883/8883, "
                            "causing vital sign telemetry delays on pediatric infusion pumps and central nursing station monitors.\n"
                            "3. Modbus Function Code Injection: Malicious unauthorized write commands (Function Codes 5, 6, 15, 16) targeting "
                            "smart ICU ventilators over port 502, attempting to manipulate oxygen delivery rates or silence alarms.\n"
                            "4. Man-in-the-Middle (ARP Spoofing): Forged ARP broadcasts poisoning router caches to intercept patient health information (PHI)."
                        )
                    }
                ]
            },
            {
                "page_number": 3,
                "title": "Dual-Stage Machine Learning Pipeline",
                "sections": [
                    {
                        "heading": "III. Detection Methodology: Why Isolation Forest Before XGBoost?",
                        "content": (
                            "A central contribution of EdgeShield AI is its hierarchical two-stage edge detection pipeline:\n"
                            "Stage 1 - Unsupervised Anomaly Isolation: An Isolation Forest model inspects high-dimensional network telemetry "
                            "(packet length, byte rate, flow duration, header length, entropy). Because zero-day attacks and polymorphic payloads "
                            "lack historical signatures, Isolation Forest isolates anomalous feature points without requiring prior labels.\n"
                            "Stage 2 - Supervised Multi-Class Threat Classification: Once an anomaly boundary is breached, the flow vector is passed "
                            "to an optimized XGBoost Classifier trained to categorize the specific attack vector (e.g. DICOM Ransomware vs MQTT Flood). "
                            "This dual architecture avoids running costly multi-class classification on normal baseline traffic, preserving "
                            "edge CPU cycles and achieving an average inference latency of 0.84 ms to 1.12 ms."
                        )
                    }
                ]
            },
            {
                "page_number": 4,
                "title": "Dataset & Feature Engineering",
                "sections": [
                    {
                        "heading": "IV. Dataset Methodology & Benchmark Corpora",
                        "content": (
                            "The EdgeShield ML engine was trained and cross-validated across three premier healthcare and industrial IoT benchmark datasets:\n"
                            "1. Edge-IIoTset: Realistic multi-protocol telemetry covering MQTT, Modbus, HTTP, and DNS with 14 distinct cyberattack categories.\n"
                            "2. N-BaIoT: Real IoT device traffic captured from commercial smart devices undergoing Mirai and BASHLITE botnet infections.\n"
                            "3. TON_IoT: Comprehensive telemetry collected from heterogeneous IoT telemetry testbeds.\n"
                            "Key extracted features include: packet_length, flow_duration, header_length, byte_rate, packet_rate, tcp_syn_flag, "
                            "mqtt_msg_rate, modbus_fn_code, and Shannon payload entropy."
                        )
                    }
                ]
            },
            {
                "page_number": 5,
                "title": "Experimental Evaluation & Latency Benchmarks",
                "sections": [
                    {
                        "heading": "V. Experimental Performance Metrics",
                        "content": (
                            "Evaluation across 10-fold cross-validation yielded the following benchmark performance:\n"
                            "- Macro Precision: 99.24% across all medical subnet flows.\n"
                            "- Macro Recall: 98.91%, demonstrating near-zero false negatives for life-critical anomalies.\n"
                            "- Macro F1-Score: 99.07% harmonic balance.\n"
                            "- Confusion Matrix Analysis: Zero false negatives for Modbus ventilator injection and DICOM ransomware.\n"
                            "- Latency Benchmark: Edge processing time averaged 0.92 ms on an NVIDIA Jetson Orin Nano (15W power envelope) "
                            "and 0.61 ms on an Intel Core i7 edge gateway, fully satisfying the < 5 ms real-time clinical threshold."
                        )
                    }
                ]
            },
            {
                "page_number": 6,
                "title": "Local Generative AI & Explainability Architecture",
                "sections": [
                    {
                        "heading": "VI. Local Privacy-Preserving GenAI (Ollama SLM)",
                        "content": (
                            "Hospital cybersecurity personnel and biomedical engineers often lack deep data science expertise. "
                            "EdgeShield integrates a local Small Language Model (SLM)—specifically Llama-3 8B or Phi-3 running via Ollama—"
                            "to synthesize mathematical feature contributions into actionable human explanations:\n"
                            "1. Clinical Threat Explanation: Explaining what the attack represents in clear terms.\n"
                            "2. Hospital Workflow Impact: Forecasting whether patient vitals or radiology scans are in jeopardy.\n"
                            "3. Containment Playbook: Providing step-by-step mitigation instructions (e.g., VLAN isolation, port blocking).\n"
                            "Crucially, the Generative AI engine never participates in intrusion detection or blocking decisions; "
                            "all detection is strictly deterministic to prevent hallucination in security-critical actions."
                        )
                    }
                ]
            },
            {
                "page_number": 7,
                "title": "Security Enforcement & Clinical Containment",
                "sections": [
                    {
                        "heading": "VII. Security Action Confirmation & Mitigation Workflows",
                        "content": (
                            "Edge-based intrusion detection must balance security containment against clinical availability. "
                            "Abruptly severing network connectivity to an active patient infusion pump or ventilator could introduce "
                            "immediate patient harm. EdgeShield implements a two-tier containment architecture:\n"
                            "- Automated Soft Mitigation: Rate limiting offending external IPs and flagging anomalous flows.\n"
                            "- Explicit Human-in-the-Loop Isolation: Before a medical device port is quarantined or switched to an isolated VLAN, "
                            "the system requires clinical IT confirmation detailing the specific target device, ward location, and clinical impact warning."
                        )
                    }
                ]
            },
            {
                "page_number": 8,
                "title": "Conclusion & Future Directions",
                "sections": [
                    {
                        "heading": "VIII. Conclusion",
                        "content": (
                            "EdgeShield AI proves that high-accuracy, sub-millisecond intrusion detection can be successfully combined with "
                            "explainable generative AI on edge hardware without compromising patient privacy or violating HIPAA standards. "
                            "By combining unsupervised Isolation Forest anomaly detection, supervised XGBoost multi-class threat classification, "
                            "and offline Ollama SLM reasoning, the system equips smart hospitals with an intelligent, autonomous 24/7 biomedical "
                            "cybersecurity defense copilot."
                        )
                    }
                ]
            }
        ]

        total_words = sum(
            len(s["content"].split())
            for p in pages
            for s in p["sections"]
        )

        return {
            "id": doc_id,
            "title": "EdgeShield AI: Intelligent Edge-Based Intrusion Detection for Smart Healthcare IoT",
            "filename": "EdgeShield_AI_IEEE_Publication_2026.pdf",
            "file_size_bytes": 142850,
            "total_pages": len(pages),
            "uploaded_at": "2026-03-15T10:00:00Z",
            "category": "IEEE Research Publication",
            "author": "Biomedical Cybersecurity Engineering Group",
            "summary": "Full research paper detailing the dual-stage ML detection pipeline (Isolation Forest + XGBoost), local Ollama SLM explainability, benchmark datasets (Edge-IIoTset, N-BaIoT, TON_IoT), and sub-millisecond edge latency evaluation.",
            "total_words": total_words,
            "is_default": True,
            "pages": pages
        }

    def list_documents(self) -> List[Dict[str, Any]]:
        """Returns metadata for all available documents."""
        docs = self._load_documents_metadata()
        result = []
        for d in docs.values():
            result.append({
                "id": d["id"],
                "title": d["title"],
                "filename": d["filename"],
                "file_size_bytes": d.get("file_size_bytes", 0),
                "total_pages": d["total_pages"],
                "uploaded_at": d["uploaded_at"],
                "category": d.get("category", "Uploaded Research Document"),
                "summary": d.get("summary", ""),
                "is_default": d.get("is_default", False)
            })
        return sorted(result, key=lambda x: (not x.get("is_default", False), x.get("uploaded_at", "")), reverse=True)

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Returns complete document with all pages and sections."""
        docs = self._load_documents_metadata()
        return docs.get(doc_id)

    def get_page(self, doc_id: str, page_num: int) -> Optional[Dict[str, Any]]:
        """Returns a single page of a document."""
        doc = self.get_document(doc_id)
        if not doc:
            return None
        pages = doc.get("pages", [])
        for p in pages:
            if p["page_number"] == page_num:
                return {
                    "doc_id": doc_id,
                    "doc_title": doc["title"],
                    "total_pages": doc["total_pages"],
                    **p
                }
        return None

    def search_document(self, doc_id: str, query: str) -> List[Dict[str, Any]]:
        """Searches within a document for query terms and returns matches with page/section citations."""
        doc = self.get_document(doc_id)
        if not doc or not query.strip():
            return []

        query_terms = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
        if not query_terms:
            return []

        matches = []
        for p in doc.get("pages", []):
            page_num = p["page_number"]
            for sec in p.get("sections", []):
                heading = sec.get("heading", "")
                content = sec.get("content", "")
                text_lower = (heading + " " + content).lower()

                match_count = sum(text_lower.count(term) for term in query_terms)
                if match_count > 0:
                    # Find first occurrence snippet
                    first_idx = min(
                        [text_lower.find(term) for term in query_terms if text_lower.find(term) != -1] or [0]
                    )
                    start = max(0, first_idx - 60)
                    end = min(len(content), first_idx + 180)
                    snippet = content[start:end].replace("\n", " ").strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(content):
                        snippet = snippet + "..."

                    matches.append({
                        "doc_id": doc_id,
                        "doc_title": doc["title"],
                        "page_number": page_num,
                        "section": heading,
                        "match_count": match_count,
                        "snippet": snippet
                    })

        matches.sort(key=lambda x: x["match_count"], reverse=True)
        return matches

    def retrieve_relevant_context(self, doc_id: Optional[str], query: str, top_k: int = 3) -> Tuple[List[Dict[str, Any]], str]:
        """
        RAG Context Retrieval Pipeline:
        Document -> Page Segmentation -> Index Matching -> Top-K Passages with citations.
        """
        docs = self._load_documents_metadata()
        if not docs:
            return [], ""

        target_doc = None
        if doc_id:
            if doc_id in docs:
                target_doc = docs[doc_id]
            else:
                return [], ""  # Requested doc does not exist
        else:
            # Pick default IEEE document or first document
            for d in docs.values():
                if d.get("is_default"):
                    target_doc = d
                    break
            if not target_doc and docs:
                target_doc = list(docs.values())[0]

        if not target_doc:
            return [], ""

        query_terms = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
        scored_sections = []

        for p in target_doc.get("pages", []):
            page_num = p["page_number"]
            for sec in p.get("sections", []):
                heading = sec.get("heading", "")
                content = sec.get("content", "")
                sec_text = (heading + " " + content).lower()

                score = 0
                for term in query_terms:
                    count = sec_text.count(term)
                    score += count * 2 if term in heading.lower() else count

                if score > 0:
                    scored_sections.append({
                        "score": score,
                        "doc_id": target_doc["id"],
                        "doc_title": target_doc["title"],
                        "page_number": page_num,
                        "section": heading,
                        "content": content
                    })

        if not scored_sections:
            return [], ""

        scored_sections.sort(key=lambda x: x["score"], reverse=True)
        top_passages = scored_sections[:top_k]

        context_string = ""
        for item in top_passages:
            context_string += (
                f"\n[Source: {item['doc_title']}, Page {item['page_number']}, Section '{item['section']}']\n"
                f"{item['content']}\n"
            )

        return top_passages, context_string

    def process_and_index_pdf(self, file_bytes: bytes, original_filename: str) -> Dict[str, Any]:
        """
        Extracts pages and text from an uploaded PDF, detects sections, and adds to index.
        """
        doc_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"
        file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{original_filename}")
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        pages = []
        try:
            # Use PyMuPDF for rich text extraction
            pdf = fitz.open(stream=file_bytes, filetype="pdf")
            total_pages = len(pdf)
            
            for page_idx in range(total_pages):
                page = pdf[page_idx]
                text = page.get_text("text").strip()
                
                # Split text into paragraphs or detect headings
                paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
                sections = []
                
                if paragraphs:
                    current_heading = f"Page {page_idx + 1} Content"
                    current_content = []
                    
                    for para in paragraphs:
                        # Simple heading heuristic: short line or all-caps or starts with Roman numerals/numbers
                        lines = para.split("\n")
                        first_line = lines[0].strip()
                        if len(first_line) < 60 and (
                            first_line.isupper() 
                            or re.match(r"^(I{1,3}|IV|V|VI{1,3}|IX|X|\d+)\.?\s+[A-Z]", first_line)
                            or first_line.endswith(":")
                        ):
                            if current_content:
                                sections.append({
                                    "heading": current_heading,
                                    "content": "\n".join(current_content)
                                })
                                current_content = []
                            current_heading = first_line
                            if len(lines) > 1:
                                current_content.append("\n".join(lines[1:]))
                        else:
                            current_content.append(para)
                            
                    if current_content:
                        sections.append({
                            "heading": current_heading,
                            "content": "\n".join(current_content)
                        })
                else:
                    sections.append({
                        "heading": f"Page {page_idx + 1}",
                        "content": text if text else "No text extracted from this page."
                    })

                pages.append({
                    "page_number": page_idx + 1,
                    "title": sections[0]["heading"] if sections else f"Page {page_idx + 1}",
                    "sections": sections
                })
        except Exception as e:
            print(f"[!] PyMuPDF extraction failed, falling back to pypdf: {e}")
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            for page_idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                pages.append({
                    "page_number": page_idx + 1,
                    "title": f"Page {page_idx + 1}",
                    "sections": [{
                        "heading": f"Section - Page {page_idx + 1}",
                        "content": text
                    }]
                })

        # Derive title from filename or first page
        title = original_filename.replace(".pdf", "").replace("_", " ").replace("-", " ").title()
        if pages and pages[0]["sections"]:
            first_heading = pages[0]["sections"][0]["heading"]
            if len(first_heading) > 10 and not first_heading.startswith("Page"):
                title = first_heading

        total_words = sum(
            len(s["content"].split())
            for p in pages
            for s in p.get("sections", [])
        )

        doc_meta = {
            "id": doc_id,
            "title": title,
            "filename": original_filename,
            "file_size_bytes": len(file_bytes),
            "total_pages": len(pages),
            "uploaded_at": datetime.utcnow().isoformat() + "Z",
            "category": "User Uploaded PDF",
            "author": "Hospital Security Analyst / Research Upload",
            "summary": f"Uploaded document containing {len(pages)} pages and {total_words} words indexed for EdgeShield AI context.",
            "total_words": total_words,
            "is_default": False,
            "pages": pages
        }

        docs = self._load_documents_metadata()
        docs[doc_id] = doc_meta
        self._save_documents_metadata(docs)

        return {
            "id": doc_id,
            "title": title,
            "filename": original_filename,
            "file_size_bytes": len(file_bytes),
            "total_pages": len(pages),
            "uploaded_at": doc_meta["uploaded_at"],
            "category": doc_meta["category"],
            "summary": doc_meta["summary"]
        }

    def delete_document(self, doc_id: str) -> bool:
        """Deletes an uploaded document (preventing deletion of default IEEE research paper)."""
        docs = self._load_documents_metadata()
        if doc_id not in docs:
            return False
        if docs[doc_id].get("is_default"):
            return False  # Protect default research document

        del docs[doc_id]
        self._save_documents_metadata(docs)
        return True


pdf_service = PDFService()
