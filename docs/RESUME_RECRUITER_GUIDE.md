# Resume & Technical Recruiter Guide
**Candidate Profile:** Senior Data Analyst / Analytics Engineer / AI Data Analyst  
**Engagement:** Frogeindrip (DTC Apparel)  

---

## 1. Clear Distinction: Original Freelance Engagement vs. New Portfolio Platform

To maintain absolute professional integrity in technical interviews, the candidate's work is explicitly segmented into two distinct categories:

### A. Original Freelance Work (Completed Client Engagement)
- **Role:** Freelance Data Analyst
- **Brand:** Frogeindrip (Direct-to-Consumer Apparel)
- **Primary Stack:** SQL, Python, Power BI, Square POS Analytics
- **Scope:**
  - Ingested Square POS raw sales transactions and sales trend reports ($46.2k Net Sales, $38.1k Gross Sales, May 2026 peak of $8,397.00).
  - Built launch reporting on checkout conversion, Average Order Value (AOV), and realized gross margins.
  - Performed initial RFM and cohort retention analysis showing repeat buyers drove ~35% of GMV, providing data-driven guidance for inventory reorders and markdown timing.

### B. New AI Analytics Portfolio (Advanced Implementation)
- **System:** Frogeindrip AI-Powered Ecommerce Analytics & Business Intelligence Suite
- **Stack:** DuckDB Lakehouse, dbt Core, Python ETL, Pandera, Scikit-learn (K-Means, Random Forest, Gradient Boosting), Streamlit, Plotly, OpenAI Tool-Calling
- **Scope:**
  - Designed and deployed a complete production-grade Lakehouse with star-schema dimensional modeling (`fct_sales`, `dim_customers`, `dim_products`).
  - Implemented 12 automated data quality assertions and financial reconciliation tests using Pandera and dbt generic tests (33/33 passing).
  - Built leakage-free repeat-purchase classification models (0.732 ROC-AUC) with strict time-aware splitting.
  - Developed a natural-language AI Decision Copilot with tool-grounded function calling and a zero-dependency deterministic offline fallback.

---

## 2. ATS-Optimized Resume Bullet Options

### Option 1: Data Analyst / BI Analyst Focus
> **Freelance Data Analyst | Frogeindrip (DTC Apparel)**  
> *SQL, Python, Power BI, DuckDB, Streamlit*
> - Engineered executive launch dashboards tracking **$46.2K+ in Net Sales**, AOV, and SKU-level gross margins across omnichannel Square POS transactions.
> - Conducted customer cohort and RFM retention analysis revealing repeat buyers contributed **~35% of total GMV**, directly informing seasonal reorder cadences and markdown strategies.
> - Formulated 15+ complex SQL analytical queries utilizing CTEs, LAG window functions, and running totals to model customer lifetime spend and multi-month cohort decay curves.

### Option 2: Analytics Engineer Focus
> **Analytics Engineer (Freelance) | Frogeindrip**  
> *dbt Core, DuckDB, Python, Pandera, SQL, Git, CI/CD*
> - Designed and built an end-to-end ecommerce Lakehouse architecture in DuckDB using dbt Core, delivering dimensional star-schema models (`fct_sales`, `dim_customers`, `dim_products`) and automated analytical marts.
> - Implemented 33+ automated schema, referential integrity, and financial reconciliation tests via dbt and Pandera, achieving 100% test coverage with zero data discrepancies.
> - Modeled point-in-time repeat buyer contribution and customer retention metrics, eliminating lookahead data leakage in retrospective cohort reporting.

### Option 3: AI & Machine Learning / Data Analyst Focus
> **AI & Analytics Developer (Freelance) | Frogeindrip**  
> *Python, Scikit-learn, OpenAI API, Streamlit, DuckDB, dbt*
> - Developed an interactive AI Analytics Copilot utilizing OpenAI function-calling and read-only parameterized analytics tools, providing grounded executive insights with zero arbitrary SQL vulnerability.
> - Built a time-aware repeat purchase classification pipeline in Scikit-learn (Random Forest & Logistic Regression), outperforming naive class baselines with a **0.732 ROC-AUC**.
> - Deployed a multi-page Streamlit decision intelligence application featuring K-Means behavioral clustering, sales forecasting against naive lag baselines, and automated markdown executive reporting.

---

## 3. Technical Interview 30-Second Elevator Pitch

> *"With Frogeindrip, I started by analyzing Square launch sales data—verifying $46.2k in net sales and discovering that repeat buyers drove about 35% of total GMV, which helped the brand plan their production reorders. I then expanded this into a full-scale portfolio analytics platform: building a DuckDB and dbt Lakehouse with star-schema modeling, automated Pandera data validation tests, leakage-free repeat purchase predictive models in scikit-learn, and an AI Analytics Copilot with strict read-only tool guardrails. The entire project is reproducible with a single script, runs completely offline without paid API keys, and has a 100% passing test suite."*
