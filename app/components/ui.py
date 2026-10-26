"""Reusable UI components for Streamlit pages."""

import streamlit as st

from frogeindrip.config import PROJECT_ROOT


def inject_custom_css():
    """Inject modern styling into Streamlit app."""
    css_path = PROJECT_ROOT / "app" / "assets" / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, badge_type: str = "verified"):
    """Render standardized high-impact page header with evidence provenance badge."""
    inject_custom_css()

    badge_html = {
        "verified": '<span class="badge-verified">✓ Verified Screenshot Evidence</span>',
        "synthetic": '<span class="badge-synthetic">⚙ Synthetic Benchmark Demonstration</span>',
        "hybrid": '<span class="badge-verified">✓ Verified Evidence</span> &nbsp; <span class="badge-synthetic">⚙ Synthetic Mart</span>',
        "pending": '<span class="badge-pending">⏳ Pending Verification</span>',
    }.get(badge_type, '<span class="badge-synthetic">⚙ Synthetic Demonstration</span>')

    st.markdown(
        f"""
        <div style="margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #334155;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">
                    {title}
                </h1>
                <div>{badge_html}</div>
            </div>
            <p style="margin: 0; font-size: 1.05rem; color: #94a3b8; font-weight: 400;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, delta: str = None, delta_type: str = "positive"):
    """Render a card-style KPI block."""
    delta_class = "metric-delta-pos" if delta_type == "positive" else "metric-delta-neutral"
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ""

    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """


def render_sidebar():
    """Render consistent sidebar with navigation, brand info, and data provenance."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding: 12px 0 20px 0; border-bottom: 1px solid #334155;">
                <div style="font-size: 1.6rem; font-weight: 900; letter-spacing: -0.03em; color: #10b981;">
                    🐸 FROGEINDRIP
                </div>
                <div style="font-size: 0.8rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px;">
                    AI Analytics & BI Platform
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 📋 Evidence Governance")
        st.markdown(
            """
            - **Net Sales:** `$46,271.26` *(Verified)*
            - **Gross Sales:** `$38,131.26` *(Verified)*
            - **May 2026 Peak:** `$8,397.00` *(Verified)*
            - **Repeat GMV Share:** `~35%` *(Pending/Sim)*
            """
        )

        st.markdown("---")
        st.markdown("### 🛠️ Platform Architecture")
        st.markdown(
            """
            - **Engine:** Python, DuckDB, dbt Core
            - **Data Model:** Star Schema Marts
            - **Machine Learning:** Scikit-learn
            - **AI Copilot:** OpenAI Function Calling + Deterministic Offline Mode
            """
        )

        st.markdown("---")
        st.caption("Frogeindrip Analytics Platform v1.0.0 · Production Portfolio Edition")
