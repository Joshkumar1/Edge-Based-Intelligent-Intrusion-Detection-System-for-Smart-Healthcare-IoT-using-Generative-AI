# EdgeShield AI — IEEE Conference LaTeX Submission Package

This package contains the complete, camera-ready LaTeX source code and publication-grade figures for:
**"EdgeShield AI: An Edge-Based Intelligent Intrusion Detection System for Smart Healthcare IoT Using Generative AI"**

---

## 📁 Package Contents

```
EdgeShield_AI_LaTeX/
├── major.tex                  # Primary IEEE conference manuscript
├── IEEEtran.cls               # Official IEEE Transactions/Conference LaTeX class (v1.8b)
├── README.md                  # Compilation instructions & metadata
└── figures/                   # 300 DPI high-resolution figures
    ├── fig1_architecture.png       # 4-Tier edge-native architecture & dual-pipeline decoupling
    ├── fig2_model_benchmark.png    # Empirical benchmark comparison across 4 classifiers
    ├── fig3_confusion_matrix.png   # Normalized confusion matrix (Random Forest, Config B)
    ├── fig4_per_class_f1.png       # Per-class F1-score breakdown across candidate models
    ├── fig5_ood_detection.png      # Out-of-distribution anomaly detection rates
    ├── fig6_clinical_flowchart.png # MIMIC-IV 24h prospective clinical cohort flowchart
    ├── fig7_clinical_roc.png       # Prospective mortality ROC curves (Held-out vs Grouped CV)
    ├── fig8_clinical_pr.png        # Prospective mortality Precision-Recall curves
    └── fig9_inference_latency.png  # Single-packet inference latency distribution (1,000 trials)
```

---

## ⚙️ Compilation Instructions

### 1. Overleaf (Recommended)
1. Zip this directory or use the provided `EdgeShield_AI_LaTeX_IEEE.zip`.
2. Go to [Overleaf](https://www.overleaf.com), click **New Project** $\rightarrow$ **Upload Project**.
3. Select `EdgeShield_AI_LaTeX_IEEE.zip`.
4. Overleaf automatically detects `major.tex` as the root document and compiles it directly using pdfLaTeX.

### 2. Local Command Line (macOS / Linux / Windows)
Using `pdflatex`:
```bash
pdflatex major.tex
pdflatex major.tex
```
*(Running twice resolves all cross-references, equation tags, figure labels, and citations).*

Or using `latexmk`:
```bash
latexmk -pdf major.tex
```

---

## 📜 IEEE Compliance & Citation Audit

- **Document Class:** `\documentclass[conference]{IEEEtran}` with standard 10pt two-column layout.
- **Author Block:** Canonical multi-author IEEE formatting without manual horizontal spacing hacks.
- **Citation Standard:** Sequential numeric citations `[1]` through `[12]` in strict chronological order upon first appearance in the manuscript.
- **Bibliography:** Formatted according to IEEE Transactions abbreviation guidelines (authors, title in quotes, italicized standard journal/proceeding abbreviations, volume, issue, page numbers, dates, and persistent DOIs/URLs).
- **Cross-Referencing:** 100% matched labels and references for all 9 figures (`Fig.~\ref{...}`), 5 tables (`Table~\ref{...}`), 3 equations (`(\ref{...})`), and 1 safety interlock algorithm (`Algorithm~\ref{...}`).
