"""Page 7: Evidence, Data Methodology, and Privacy Governance."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

import pandas as pd
import streamlit as st

from app.components.ui import inject_custom_css, render_page_header, render_sidebar
from frogeindrip.utils.export import generate_executive_markdown_report

st.set_page_config(page_title="Evidence & Methodology | Frogeindrip", page_icon="🐸", layout="wide")
inject_custom_css()
render_sidebar()

render_page_header(
    title="Evidence Validation & Methodology",
    subtitle="Audit framework, screenshot inspection, claims reconciliation, and data privacy governance.",
    badge_type="verified",
)

# Export Full Executive Report
report_md = generate_executive_markdown_report()
st.download_button(
    label="📥 Download Executive Analytics Report (.md)",
    data=report_md,
    file_name="frogeindrip_executive_report.md",
    mime="text/markdown",
    help="Download comprehensive audit and analytical report in markdown format.",
)

st.markdown("<br>", unsafe_allow_html=True)

# 1. Four-Tier Governance Matrix
st.markdown("### 🏛️ Evidence Classification Framework")
evidence_matrix_df = pd.DataFrame([
    {
        "Tier": "Tier 1: Verified Screenshot Evidence",
        "Scope": "Group A Net Sales ($46,271.26) & Group B Gross Sales ($38,131.26)",
        "Source": "Square POS Analytics Dashboard Screenshots",
        "Integrity": "Immutable Client Baseline",
    },
    {
        "Tier": "Tier 2: Verified Analytical Evidence",
        "Scope": "Checkout conversion & AOV initial client reporting",
        "Source": "Freelance SQL & Python client engagement logs",
        "Integrity": "Reproducible on client exports",
    },
    {
        "Tier": "Tier 3: Pending Verification",
        "Scope": "~35% Repeat Buyer GMV Contribution",
        "Source": "Freelance resume bullet claim",
        "Integrity": "Simulated in portfolio pending raw order log access",
    },
    {
        "Tier": "Tier 4: Synthetic Demonstration",
        "Scope": "End-to-end DuckDB Lakehouse, dbt Marts, ML & AI Copilot",
        "Source": "Deterministic Synthetic Generator (seed=42)",
        "Integrity": "100% Open-Source & Reproducible",
    },
])
st.dataframe(evidence_matrix_df, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. Detailed Screenshot Analysis & Visual Proof
st.markdown("### 📸 Primary Square POS Visual Evidence")

screenshot_dir = ROOT_DIR / "evidence" / "screenshots"
tab1, tab2, tab3 = st.tabs([
    "📈 12-Month Sales Trend ($38,131.26)",
    "🏔️ May 2026 Peak Tooltip ($8,397.00)",
    "📉 July 2026 Run-Rate ($1,505.00)",
])

with tab1:
    img1 = screenshot_dir / "01_square_gross_sales_trend_overview.png"
    if img1.exists():
        st.image(str(img1), caption="Figure 1: Square Analytics Gross Sales Trend Overview (Jul 01, 2025 – Jul 01, 2026) — Verified Gross Sales $38,131.26 vs $0 Baseline.", use_container_width=True)
    st.markdown(
        """
        - **Active Period:** `Jul 01, 2025 – Jul 01, 2026` (366 days)
        - **Verified Metric:** Gross Sales = **$38,131.26**
        - **Prior Period Baseline:** `$0.00` (*Jun 30, 2024 – Jun 30, 2025*)
        - **Account Privacy:** Redacted internal profile identifier (`[REDACTED ACCOUNT]`) to preserve client confidentiality.
        """
    )

with tab2:
    img2 = screenshot_dir / "02_square_may_2026_peak_sales_tooltip.png"
    if img2.exists():
        st.image(str(img2), caption="Figure 2: Square Analytics May 2026 Peak Month Tooltip ($8,397.00 item sales including modifiers).", use_container_width=True)
    st.markdown(
        """
        - **Peak Month Reported:** **May 2026 = $8,397.00**
        - **Revenue Contribution:** **22.02%** of 12-month rolling gross revenue ($8,397.00 / $38,131.26).
        - **Context:** Represents the primary seasonal capsule collection drop.
        """
    )

with tab3:
    img3 = screenshot_dir / "03_square_july_2026_run_rate_tooltip.png"
    if img3.exists():
        st.image(str(img3), caption="Figure 3: Square Analytics July 2026 Post-Peak Tooltip ($1,505.00 run-rate).", use_container_width=True)
    st.markdown(
        """
        - **Post-Peak Contraction:** **July 2026 = $1,505.00**
        - **Significance:** Documents sell-through dynamics and marketing taper post-campaign.
        """
    )

st.markdown("<br>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    st.markdown(
        """
        #### Screenshot Group A: Sales Summary
        - **Metric Reported:** Net Sales = **$46,271.26**
        - **Active Period:** `Sep 01, 2025 – Jul 31, 2026` (11 calendar months)
        - **Account Name:** `[REDACTED ACCOUNT]` (Brand: Frogeindrip)
        - **Reporting Grain:** Hourly, daily, and day-of-week aggregations
        - **Key Observation:** Captures full revenue across all operating channels through late July 2026.
        """
    )

with col_b:
    st.markdown(
        """
        #### Screenshot Group B: Sales Trends (12-Mo)
        - **Metric Reported:** Gross Sales = **$38,131.26**
        - **Active Period:** `Jul 01, 2025 – Jul 01, 2026` (366 days)
        - **Prior Year:** `$0.00` (*June 30, 2024 – June 30, 2025*)
        - **Growth Tag:** `▲ 100%` (*Mathematical artifact of zero baseline*)
        - **Peak Month:** **May 2026 = $8,397.00**
        - **Contracted Month:** **July 2026 = $1,505.00**
        """
    )

# 3. Discrepancy & Statistical Analysis
st.markdown("### ⚖️ Statistical Reconciliations & Caveats")

st.markdown(
    """
    1. **Why do Net Sales ($46.2k) exceed Gross Sales ($38.1k)?**
       - **Different Date Windows:** Group A runs through **July 31, 2026**, capturing a full extra month of active apparel sales, whereas Group B cuts off on **July 01, 2026**.
       - **Different Metrics:** Net Sales accounts for post-discount settlements across all locations. **These figures must not be added together.**
    2. **The `+100%` Baseline Growth Indicator:**
       - Square displays a green `+100%` badge against a `$0.00` prior year baseline. In finance, percent change from zero is mathematically undefined. Square truncates this to 100%. In our documentation, this is properly classified as a **Venture Launch Marker**, not an operational year-over-year growth rate.
    3. **Privacy & Redaction Compliance:**
       - The internal account name ("Real Knitz") displayed in the top-left navigation of the Square account is redacted in all public presentation materials.
       - The business and brand is strictly identified as **Frogeindrip**.
    """
)
