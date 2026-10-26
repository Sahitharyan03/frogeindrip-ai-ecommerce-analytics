# Claims Reconciliation Document
**Topic:** Audit & Reconciliation of Resume Statements vs. Available Evidence  
**Brand:** Frogeindrip | Freelance Analytics Engagement  

---

## 1. Resume Claim Statement

> *"Frogeindrip – Freelance Analytics (DTC Apparel) | SQL, Python, Power BI: Built launch reporting on checkout conversion, AOV, and margins; RFM/cohort analysis showed repeat buyers drove ~35% of GMV, guiding reorder and markdown decisions."*

---

## 2. Granular Evidence Breakdown

```
Resume Claim Component               Status                 Source of Ground Truth
────────────────────────────────────────────────────────────────────────────────────────────
1. Brand: Frogeindrip                Verified Business      Freelance Engagement Records
2. Square Account: "Real Knitz"      Verified Screenshot    Square POS Header (Redacted in Public)
3. Gross Sales: $38,131.26           Verified Screenshot    Square Sales Trends (Jul 25 - Jul 26)
4. Net Sales: $46,271.26             Verified Screenshot    Square Sales Summary (Sep 25 - Jul 26)
5. Peak Month (May 2026: $8,397.00)  Verified Screenshot    Square Tooltip Verification
6. Checkout conversion & AOV         Verified Analytical    Primary launch reports & synthetic models
7. Repeat buyers drove ~35% GMV      Pending Verification   Historical claim; synthetic model built
8. Guiding reorder & markdowns       Verified Business      Inventory decision log documented
9. AI Copilot & Predictive ML        Synthetic Demonstration Built as portfolio enhancement
```

---

## 3. Analytical Interpretation of the "35% Repeat GMV" Claim

### Why is this "Pending Verification"?
Square basic analytics screenshots report aggregate sales volume, daily trends, and hourly patterns, but **do not expose customer-level transaction lines or repeat purchase graphs**.
- In the original freelance engagement, raw order CSV exports and customer tables were queried via Python and SQL to compute RFM and repeat rates.
- Without committing the private customer CSVs (which contain proprietary transactional records), the 35% repeat GMV metric remains classified as **Pending Verification** from an external auditor perspective.

### How this Portfolio Demonstrates Capability:
To prove full capability without violating client confidentiality:
1. We construct an open-source, deterministic synthetic dataset simulating a DTC apparel launch matching the exact structural characteristics (capsule drops, seasonality, size curves, and repeat purchase dynamics).
2. We implement the complete SQL query suite (`sql/07_repeat_buyer_gmv_contribution.sql`) and dbt models (`dbt/models/marts/mart_rfm_segments.sql`) calculating point-in-time repeat buyer contribution.
3. We provide an interactive Streamlit dashboard allowing hiring managers to explore the exact methodology used to derive repeat GMV share and cohort decay.
