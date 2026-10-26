# Evidence Validation Matrix
**Project:** Frogeindrip AI-Powered Ecommerce Analytics & Business Intelligence  
**Classification Standards:** Verified Screenshot Evidence, Verified Analytical Evidence, Pending Verification, Synthetic Demonstration  

---

## 1. Evidence Classification Framework

To uphold strict corporate governance, data privacy, and analytical integrity, every metric, claim, and visualization in this platform is tagged with one of four formal tiers:

| Tier | Category | Description | Source / Provenance |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Verified Screenshot Evidence** | Directly visible in the primary Square Analytics screenshots. Immutable baseline figures. | Raw Square POS / Dashboard captures |
| **Tier 2** | **Verified Analytical Evidence** | Calculated via reproducible code (SQL / Python / dbt) directly from primary raw client logs (when available). | Reproducible scripts on primary records |
| **Tier 3** | **Pending Verification** | Historical resume or client claims awaiting client transaction export logs. | Freelance resume bullet statements |
| **Tier 4** | **Synthetic Demonstration** | Deterministically generated mock datasets used to demonstrate end-to-end data pipelines, ML models, and interactive BI dashboards. | Seeded synthetic generator (`seed=42`) |

---

## 2. Comprehensive Metric & Claim Reconciliation Table

| Metric / Claim | Figure / Statement | Evidence Tier | Verified Source & Exact Context | Notes & Limitations |
| :--- | :--- | :--- | :--- | :--- |
| **Group A: Net Sales** | $46,271.26 | **Verified Screenshot Evidence** | Square Sales Summary: `Sep 01, 2025 – Jul 31, 2026` | 11-month reporting window across all active channels. |
| **Group A: Day/Hour Patterns** | Daily & hourly distributions | **Verified Screenshot Evidence** | Square Sales Summary: Day-of-week & Hour-of-day charts | Peak traffic concentrated in afternoon/evening hours (EST). |
| **Group B: Gross Sales** | $38,131.26 | **Verified Screenshot Evidence** | Square Sales Trends: `Jul 01, 2025 – Jul 01, 2026` | 12-month rolling period. Excludes subsequent July 2026 days. |
| **Group B: May 2026 Peak** | $8,397.00 gross sales | **Verified Screenshot Evidence** | Square Sales Trends tooltip: `May 2026` | Highest monthly volume observed during spring drop. |
| **Group B: July 2026 Volume** | $1,505.00 gross sales | **Verified Screenshot Evidence** | Square Sales Trends tooltip: `Jul 2026` | Partial month capture reflecting drop-off/launch cycle end. |
| **Prior Year Baseline** | $0.00 (`Jun 30, 2024 – Jun 30, 2025`) | **Verified Screenshot Evidence** | Square comparison line in Trends | Indicates brand launch occurred in late 2025; no prior-year history. |
| **"+100%" Growth Badge** | Displayed in Square UI | **Verified Screenshot Evidence** | UI comparison tag | **Statistical Caveat:** Artefact of comparing positive revenue against a $0.00 baseline; not organic YoY CAGR. |
| **Repeat Buyer GMV Share** | ~35% of GMV from repeat buyers | **Pending Verification** | Resume bullet claim from freelance engagement | Requires raw order-item ledger with hashed customer IDs to verify. |
| **Customer LTV & Retention** | Multi-month cohort curves | **Synthetic Demonstration** | Python Data Generator (`src/frogeindrip/data/generator.py`) | Deterministic demonstration of SQL/dbt cohort modeling. |
| **Predictive ML Scores** | K-Means clusters & Churn/Repeat AUC | **Synthetic Demonstration** | Scikit-learn pipelines in `src/frogeindrip/ml/` | Trained on synthetic cohort data to showcase ML engineering. |
| **AI Copilot Responses** | Natural language insights & summaries | **Synthetic Demonstration** | Grounded LLM function-calling layer | Discloses provenance and prevents hallucinations. |

---

## 3. Discrepancy & Periodicity Analysis

### A. Group A vs. Group B Reconciled
- **Group A (Sales Summary):** Covers **Sep 01, 2025 to Jul 31, 2026** showing **Net Sales of $46,271.26**.
- **Group B (Sales Trends):** Covers **Jul 01, 2025 to Jul 01, 2026** showing **Gross Sales of $38,131.26**.
- **Analytical Distinction:** Net Sales accounts for returns, discounts, and fee deductions. Gross Sales is pre-discount item volume. Because the reporting periods and metrics differ, **these two totals must never be added together or treated as interchangeable**.

### B. Baseline Growth Indicator
Square displays a `+100%` green growth indicator. In standard accounting and BI reporting, a transition from $0 to any positive number is undefined ($\Delta / 0$). Square caps this presentationally at 100%. In our analytics and documentation, we clearly note this as a **New Venture Launch Baseline**, not a 100% year-over-year operational expansion.

---

## 4. Privacy & Anonymization Audit

1. **Account Identification:** The Square account holder name ("Real Knitz") has been redacted in all public presentation materials and documentation. The business brand is exclusively referenced as **Frogeindrip**.
2. **PII Protection:** No personal email addresses, billing addresses, credit card numbers, or customer telephone numbers exist in this repository.
3. **Synthetic Data Firewall:** All granular transaction files in `data/synthetic/` are generated via pseudo-random simulation with deterministic seeds to prevent accidental exposure of proprietary records.
