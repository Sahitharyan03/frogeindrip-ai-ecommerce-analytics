"""Page 3: Customer Intelligence, RFM Segmentation, & Cohort Retention."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

import plotly.express as px
import streamlit as st

from app.components.charts import build_cohort_heatmap, build_rfm_treemap
from app.components.ui import inject_custom_css, render_page_header, render_sidebar
from frogeindrip.analytics.cohorts import get_cohort_matrix
from frogeindrip.analytics.retention import get_repeat_buyer_analysis
from frogeindrip.analytics.rfm import get_rfm_analysis
from frogeindrip.utils.formatting import format_currency

st.set_page_config(page_title="Customer Intelligence | Frogeindrip", page_icon="🐸", layout="wide")
inject_custom_css()
render_sidebar()

render_page_header(
    title="Customer Intelligence & Retention",
    subtitle="RFM segmentation, customer cohort retention heatmaps, and leak-free repeat buyer economics.",
    badge_type="synthetic",
)

# Repeat Buyer Highlight Callout Box
repeat_data = get_repeat_buyer_analysis()

st.markdown("### 🔁 Repeat Buyer GMV Contribution Audit")
st.caption("Detailed comparison of lifetime definition vs. strict point-in-time sequence (no lookahead data leakage).")

rep_c1, rep_c2, rep_c3, rep_c4 = st.columns(4)

with rep_c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Repeat GMV (Lifetime Method A)</div>
            <div class="metric-value">{repeat_data['lifetime_repeat_gmv_pct']}%</div>
            <div class="metric-delta-pos">{format_currency(repeat_data['lifetime_repeat_gmv'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with rep_c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Repeat GMV (Point-in-Time Method B)</div>
            <div class="metric-value">{repeat_data['point_in_time_repeat_gmv_pct']}%</div>
            <div class="metric-delta-pos">{format_currency(repeat_data['point_in_time_repeat_gmv'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with rep_c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Avg Days to 2nd Order</div>
            <div class="metric-value">{repeat_data['avg_days_to_repeat']} d</div>
            <div class="metric-delta-neutral">Median: {repeat_data['median_days_to_repeat']} days</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with rep_c4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Repeat Orders Count</div>
            <div class="metric-value">{repeat_data['point_in_time_repeat_orders']}</div>
            <div class="metric-delta-neutral">{repeat_data['point_in_time_repeat_order_pct']}% of all orders</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.expander("ℹ️ Methodological Note: Avoiding Data Leakage in Repeat Buyer GMV"):
    st.markdown(
        """
        - **Method A (Lifetime Definition):** Attributes 100% of a customer's spend (including their first order) to the 'repeat' category if that customer eventually places $\\ge 2$ orders during the total observation window. While common in retrospective marketing briefs, this introduces lookahead bias when analyzing early months.
        - **Method B (Point-in-Time Definition):** Strictly attributes revenue to repeat buyers **only for transactions where order sequence $\\ge 2$ at the time the order was placed**. This is the mathematically rigorous, leak-free standard for production financial accounting.
        """
    )

st.markdown("<br>", unsafe_allow_html=True)

# RFM Segmentation Section
st.markdown("### 🎯 Quintile RFM Customer Segmentation")
rfm_data = get_rfm_analysis()

rfm_col1, rfm_col2 = st.columns([3, 2])
with rfm_col1:
    st.plotly_chart(build_rfm_treemap(rfm_data["segment_summary"]), use_container_width=True)

with rfm_col2:
    st.markdown("#### Segment Revenue & Strategy")
    st.dataframe(
        rfm_data["segment_summary"][[
            "segment_label", "customer_count", "customer_share_pct",
            "total_segment_spend", "gmv_share_pct", "avg_customer_spend"
        ]],
        use_container_width=True,
        hide_index=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Cohort Retention Matrix
st.markdown("### 🧬 Customer Cohort Retention Matrix")
st.caption("Tracks percentage of active returning buyers across monthly acquisition cohorts.")
cohort_data = get_cohort_matrix()

st.plotly_chart(build_cohort_heatmap(cohort_data["retention_pivot"]), use_container_width=True)

# Retention Decay Curve
fig_decay = px.line(
    cohort_data["avg_retention_curve"],
    x="period_number",
    y="retention_rate_pct",
    markers=True,
    title="<b>Average Cohort Retention Decay Curve Across Elapsed Months</b>",
    labels={"period_number": "Months Elapsed Since First Purchase", "retention_rate_pct": "Average Retention Rate (%)"},
)
fig_decay.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.4)")
st.plotly_chart(fig_decay, use_container_width=True)
