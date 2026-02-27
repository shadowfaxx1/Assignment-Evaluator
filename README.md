# Assignment Evaluator
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![AssignmentEval](https://img.shields.io/badge/Assignment-Eval-purple.svg)](LICENSE)

Automated student assignment evaluation using NLP — reduces manual grading effort and provides data-driven insights for educators.

---

## Quick Start

```sh
git clone <repository_url>
pip install -r requirements.txt
streamlit run main.py
```

---

## What It Evaluates

| Metric | Details |
|--------|---------|
|  Sentiment | Polarity, subjectivity, positive/negative scoring |
|  Language Complexity | Fog index, sentence length, complex word % |
|  Structure | Word count, paragraph organisation, coherence |
|  Plagiarism | Algorithmic similarity scoring |
|  Hypothesis Testing | Zero-shot classification via HuggingFace |

---

## Usage

Log in to the **admin panel** → view assignment summaries → click any assignment for a full breakdown. Navigate to **Student-wise Report** for per-student metrics. All results are stored in SQLite and visualised as bar charts and scatter plots.

---

## Stack
Python 3 · Streamlit · NLTK · HuggingFace Transformers · SQLite

---
*Licensed under [MIT](LICENSE).*
