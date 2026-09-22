# AI/ML Model Card — Campus Helpdesk & Maintenance Tickets

This document tracks the baseline, evaluation, limitations, and fallback
behavior for every AI/data feature in this project, per the Common Pack
requirement: "Every AI feature needs a deterministic baseline and a fallback."

---

## 1. SLA Risk — Rule-Based Baseline

**Baseline:** Deterministic rule in `app/sla_risk.py` (`SLARiskModel.predict`).
Flags a ticket as at-risk if ANY of: high team workload, high/critical priority,
or ticket age above threshold (recall-centric design — one condition is
enough to trigger a flag, since missing a breaching ticket is worse than a
false alarm).

**Dataset:** `data/sla_risk/sla_risk_dataset (1).csv` — 3,000 synthetic tickets.
No train/test split used: this is a fixed rule, not a trained model, so it
is evaluated directly on the full dataset.

**Evaluation script:** `scripts/evaluate_sla_baseline.py`

**Metric:** Recall on breached tickets (per spec: "recall for breached tickets")

**Result:**

| Metric | Value |
|---|---|
| Recall | 0.9015 |
| Precision | 0.5852 |
| F1 | 0.7097 |
| Accuracy | 0.6207 |

**Limitations:**
- Workload thresholds (Low/Medium/High) are derived from dataset tertiles
  (Low ≤ 5, Medium ≤ 10, High > 10), not a business-defined cutoff — needs
  validation against real operational data.
- Precision is intentionally low (~58%) because the design goal is to
  minimize missed breaches (false negatives), not false alarms.

**Fallback:** No trained ML model exists yet for this feature — the
rule-based logic IS the production path, not a temporary fallback. There
is no external dependency that can fail.

---

## 2. Duplicate Detection — TF-IDF + Cosine Similarity

**Method:** `app/duplicate.py` (`DuplicateDetector`). Represents each
ticket's title + description as a TF-IDF vector and ranks the candidate
pool by cosine similarity to the query ticket.

**Dataset:** `data/duplicates/duplicate_dataset.csv` — 543 rows total,
100 ORIGINAL queries evaluated against a candidate pool of 443 tickets.

**Evaluation scripts:** `scripts/evaluate_duplicate_baseline.py`,
`scripts/check_hard_negative.py`

**Metric:** Precision@K (per spec: "precision@k for duplicates")

**Result:**

| K | Precision |
|---|---|
| 1 | 0.9600 |
| 3 | 0.8500 |
| 5 | 0.7600 |

Hard-negative false positive rate: **0.0000** (0/100 — tickets that look
similar but are NOT true duplicates were never falsely flagged as the
top-1 match).

**Limitations:**
- Tested only on synthetic, clean-language ticket clusters; real-world
  tickets with typos or mixed Arabic-English phrasing may reduce precision.
- Precision drops from 0.96 (K=1) to 0.76 (K=5), showing ranking quality
  degrades past the top result — acceptable if the UI only surfaces the
  single best match to agents.

**Fallback:** If the similarity service is unavailable, agents fall back
to manual search/filter by category + location (existing HLP-FR-06 queue
filters).

---

## 3. Ticket Category — Rule-Based Baseline vs. Trained Classifier

**Baseline:** Keyword-matching rules in `app/rules.py` / `app/rule_engine.py`
(impact × urgency style deterministic matching).

**Trained model:** TF-IDF + Logistic Regression, trained via
`scripts/train_category_model.py`. Saved to
`models/category/category_model.joblib` and
`models/category/category_vectorizer.joblib`.

**Dataset:** `data/classification/classification_dataset.csv` — 3,000
synthetic tickets *(pending re-evaluation on corrected dataset — see note
below)*. Evaluated using 5-fold cross-validation grouped by `cluster_id`
to prevent leakage between folds.

**Evaluation scripts:** `scripts/evaluate_category_baseline.py`,
`scripts/train_category_model.py`, `scripts/sanity_check_category_model.py`

**Metric:** Macro F1 (per spec: "macro F1 for category")

**Result (⚠️ from previous dataset version — re-run pending):**

| Method | Macro F1 |
|---|---|
| Rule-based baseline | 0.7711 |
| Trained model (5-fold CV) | 0.9983 |
| Verdict | ML model beats the rule-based baseline |

**Limitations:**
- The cross-validated score (0.9983) is very high, but a separate sanity
  check on unseen "keyword-trap" sentences (phrasing not seen during
  training) only scored **2/5 correct**. Examples of failures:
  - `"AC leaking water on floor"` → predicted `PLUMBING_WATER`, expected `HVAC_AC`
  - `"Projector won't power on"` → predicted `ELECTRICAL`, expected `AV_CLASSROOM_EQUIPMENT`
  - `"Broken door on network cabinet"` → predicted `FURNITURE_FIXTURES`, expected `BUILDING_STRUCTURE`
  
  This gap suggests the high CV score likely reflects strong lexical
  shortcuts in the synthetic dataset (e.g. category-specific keywords
  appearing directly in ticket text) rather than genuine semantic
  understanding — the model may not generalize well to real-world
  phrasing variation.
- Dataset is currently being corrected; final numbers will be updated
  after re-running the three evaluation scripts above.

**Fallback:** If the trained model is unavailable, or its prediction
confidence is below a set threshold, the system falls back to the
rule-based baseline (`app/rules.py`), which has no ML runtime dependency.

---

## Summary

| Feature | Baseline | Trained Model | Fallback Exists |
|---|---|---|---|
| SLA Risk | ✅ Rule-based (Recall 0.90) | Not built (not required for MVP) | ✅ (baseline is production path) |
| Duplicate Detection | ✅ TF-IDF + Cosine (P@1 = 0.96) | N/A (method is deterministic) | ✅ (manual filter/search) |
| Category | ✅ Rule-based (F1 = 0.77) | ✅ TF-IDF + LogReg (F1 = 0.998, CV) | ✅ (falls back to rule-based) |

*Last updated: pending re-evaluation of the classification dataset.*