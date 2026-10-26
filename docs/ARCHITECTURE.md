# Frogeindrip Platform Architecture & Technical Design
**System Name:** Frogeindrip AI-Powered Ecommerce Analytics & Business Intelligence Platform  
**Architecture Style:** Modern Analytical Lakehouse & Embedded AI Decision Support  

---

## 1. High-Level Architecture Diagram

```
                                      [ INGESTION LAYER ]
                                               │
               ┌───────────────────────────────┴───────────────────────────────┐
               ▼                                                               ▼
    [Verified Square Evidence]                                   [Deterministic Synthetic Data]
    • Screenshot Group A: $46,271.26 Net Sales                    • seed=42 Generator (`Faker` style)
    • Screenshot Group B: $38,131.26 Gross Sales                  • Customers, Products, Orders, Items
               │                                                               │
               └───────────────────────────────┬───────────────────────────────┘
                                               ▼
                                      [ DATA PIPELINE ]
                                               │
                                 [Pandera Schema Enforcement]
                                 • 12 Automated Integrity Checks
                                 • Financial Reconciliation Assertions
                                 • Uniqueness & Referential Constraints
                                               │
                                               ▼
                                   [ DuckDB Embedded Lakehouse ]
                                               │
               ┌───────────────────────────────┴───────────────────────────────┐
               ▼                                                               ▼
       [ dbt Core v1.12 ]                                            [ Standalone SQL Suite ]
    • Staging Views (`stg_*`)                                         • 10 Complex Analytical Queries
    • Dimensional Models (`dim_*`)                                    • Window Functions, CTEs, MoM
    • Analytical Marts (`mart_*`)                                     • Leakage-Free Repeat GMV
               │                                                               │
               └───────────────────────────────┬───────────────────────────────┘
                                               ▼
                                    [ SERVING & ANALYTICS ]
                                               │
               ┌───────────────────────────────┼───────────────────────────────┐
               ▼                               ▼                               ▼
    [ Interactive Streamlit BI ]   [ Scikit-Learn ML Engines ]     [ AI Decision Copilot ]
    • Executive Overview            • K-Means Segmentation (k=4)   • Natural Language Querying
    • Sales & Temporal Trends       • Repeat Purchase Prediction   • OpenAI Tool-Calling & Offline
    • Customer Intelligence         • Daily Sales Forecasting      • Provenance & Privacy Guards
    • Product Margin Matrix         • Baseline Comparisons         • Structured Insights (O-I-R)
```

---

## 2. Core Architectural Principles

1. **Separation of Evidence and Simulation:** Immutable client evidence (Square screenshots) is permanently insulated from synthetic simulation models. Every dashboard card and Copilot answer carries an explicit Provenance Badge.
2. **Zero-Leakage Temporal Feature Engineering:** In customer cohort analysis and ML classification, features are strictly computed prior to a fixed cutoff date ($T_0$). Future purchase events ($T_0 + \Delta t$) are never used to define retrospective segments.
3. **Defense-in-Depth AI Security:** The Generative AI Copilot is strictly isolated from arbitrary SQL query execution. It exclusively calls pre-approved, parameterized, read-only Python analytics functions.
4. **Offline Zero-Dependency Execution:** The platform is fully functional without internet access, third-party cloud database servers, or paid API keys. An OpenAI key unlocks LLM synthesis, but the deterministic offline engine delivers instant, accurate answers regardless.
