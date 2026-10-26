import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

import streamlit as st

from app.components.ui import inject_custom_css, render_sidebar

st.set_page_config(
    page_title="Frogeindrip | AI Ecommerce Analytics",
    page_icon="🐸",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
render_sidebar()

# Hero Header
st.markdown(
    """
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(59, 130, 246, 0.15)); border: 1px solid #334155; border-radius: 16px; padding: 36px 32px; margin-bottom: 28px;">
        <div style="display: inline-block; background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 4px 12px; border-radius: 9999px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
            Production Portfolio & Business Intelligence Suite
        </div>
        <h1 style="font-size: 2.8rem; font-weight: 900; color: #f8fafc; margin: 0 0 12px 0; letter-spacing: -0.03em;">
            Frogeindrip Analytics & AI Decision Intelligence
        </h1>
        <p style="font-size: 1.15rem; color: #cbd5e1; max-width: 900px; margin: 0; line-height: 1.6;">
            A full-stack, enterprise-grade analytics platform built upon real freelance analytics engagement evidence for the DTC apparel brand <strong>Frogeindrip</strong>. Seamlessly integrates modern SQL data modeling, DuckDB & dbt marts, machine learning, and an AI Analytics Copilot with strict data governance.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Verified Evidence vs Benchmark Highlights
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Verified Net Sales (Group A)</div>
            <div class="metric-value">$46,271.26</div>
            <div class="badge-verified" style="margin-top: 8px;">✓ Square POS Screenshot</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Verified Gross Sales (Group B)</div>
            <div class="metric-value">$38,131.26</div>
            <div class="badge-verified" style="margin-top: 8px;">✓ 12-Mo Sales Trends</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Verified Peak Month (May '26)</div>
            <div class="metric-value">$8,397.00</div>
            <div class="badge-verified" style="margin-top: 8px;">✓ Spring Capsule Drop</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Repeat Buyer GMV Share</div>
            <div class="metric-value">~35.0%</div>
            <div class="badge-pending" style="margin-top: 8px;">⏳ Resume Claim / Modeled</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Architecture & Capabilities Showcase
st.markdown("### 🏛️ End-to-End Enterprise Data Architecture")

st.markdown(
    """
```
 [Primary Source Evidence] ──> [Deterministic Synthetic Generator]
       (Square POS)                    (seed=42 DTC Model)
                                              │
                                              ▼
                                 [Python ETL & Pandera Validation]
                                              │
                                              ▼
                                   [DuckDB Analytical Lakehouse]
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
            [dbt Staging & Marts]                             [Executable SQL Suite]
      (fct_sales, dim_customers, RFM)                   (Window funcs, CTEs, Cohorts)
                     │                                                 │
                     └────────────────────────┬────────────────────────┘
                                              ▼
                             [Streamlit BI Interactive App]
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
          [Scikit-learn ML Models]                           [AI Analytics Copilot]
      (Clustering, Churn, Forecast)                    (Function Calling & Governance)
```
"""
)

# Navigation Cards
st.markdown("### 🧭 Explore Platform Modules")

nav_c1, nav_c2, nav_c3 = st.columns(3)

with nav_c1:
    st.markdown(
        """
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: #10b981;">📊 Executive & Sales BI</h3>
            <p style="color: #94a3b8; font-size: 0.95rem;">
                Explore top-line net revenue, AOV, realized profit margins, MoM growth rates, and daily/hourly traffic patterns matching Square screenshot dimensions.
            </p>
            <p><a href="/Executive_Overview" target="_self" style="color: #38bdf8; font-weight: 600;">Go to Executive Overview →</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_c2:
    st.markdown(
        """
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: #3b82f6;">👥 Customer Intelligence</h3>
            <p style="color: #94a3b8; font-size: 0.95rem;">
                Dive into Quintile RFM segmentation, customer cohort retention heatmaps, and point-in-time repeat buyer GMV contribution analysis without forward-looking data leakage.
            </p>
            <p><a href="/Customer_Intelligence" target="_self" style="color: #38bdf8; font-weight: 600;">Go to Customer Intelligence →</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_c3:
    st.markdown(
        """
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: #8b5cf6;">🤖 AI Analytics Copilot</h3>
            <p style="color: #94a3b8; font-size: 0.95rem;">
                Ask natural-language ecommerce questions. The agent executes parameterized read-only analytics tools, enforces privacy firewalls, and requires zero API keys in offline mode.
            </p>
            <p><a href="/AI_Analytics_Copilot" target="_self" style="color: #38bdf8; font-weight: 600;">Launch AI Copilot →</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
