"""Page 2: Sales Analytics, Temporal Breakdown & MoM Growth."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

import duckdb
import plotly.express as px
import streamlit as st

from app.components.charts import build_day_hour_charts
from app.components.ui import inject_custom_css, render_page_header, render_sidebar
from frogeindrip.analytics.kpis import get_sales_by_time_dimensions
from frogeindrip.config import DB_PATH

st.set_page_config(page_title="Sales Analytics | Frogeindrip", page_icon="🐸", layout="wide")
inject_custom_css()
render_sidebar()

render_page_header(
    title="Sales Analytics & Temporal Patterns",
    subtitle="Deep-dive into Month-over-Month (MoM) growth, day-of-week, and hourly sales patterns.",
    badge_type="hybrid",
)

time_data = get_sales_by_time_dimensions()
monthly_df = time_data["monthly_trends"]

# Monthly Table & MoM Growth
st.markdown("### 📅 Monthly Financial Performance Table")
st.dataframe(
    monthly_df[[
        "year_month", "total_orders", "active_customers", "total_gross_sales",
        "total_discounts", "total_net_sales", "average_order_value",
        "total_gross_profit", "gross_margin_pct", "mom_growth_pct"
    ]],
    use_container_width=True,
    hide_index=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# Day of Week & Hour of Day Distribution (matching Square Screenshot dimensions)
st.markdown("### ⏰ Temporal Patterns (Matching Square Sales Summary Dimensions)")
st.caption("Captures consumer shopping behavior across day-of-week and hour-of-day traffic spikes.")

fig_dow, fig_hour = build_day_hour_charts(time_data["day_of_week"], time_data["hour_of_day"])

col_d1, col_d2 = st.columns(2)
with col_d1:
    st.plotly_chart(fig_dow, use_container_width=True)
with col_d2:
    st.plotly_chart(fig_hour, use_container_width=True)

# Cumulative GMV & 7-Day Moving Average
st.markdown("### 📈 Cumulative Brand GMV & 7-Day Rolling Moving Average")
conn = duckdb.connect(str(DB_PATH), read_only=True)
try:
    daily_query = """
        WITH daily_totals AS (
            SELECT
                CAST(order_date AS DATE) AS sale_date,
                SUM(net_amount) AS daily_net_sales
            FROM raw_orders
            WHERE status = 'completed'
            GROUP BY 1
        )
        SELECT
            sale_date,
            ROUND(daily_net_sales, 2) AS daily_net_sales,
            ROUND(SUM(daily_net_sales) OVER (ORDER BY sale_date), 2) AS cumulative_gmv,
            ROUND(AVG(daily_net_sales) OVER (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_7day_avg
        FROM daily_totals
        ORDER BY sale_date ASC;
    """
    daily_df = conn.execute(daily_query).fetchdf()

    fig_cum = px.line(
        daily_df,
        x="sale_date",
        y=["cumulative_gmv", "rolling_7day_avg"],
        labels={"value": "Amount ($)", "sale_date": "Date", "variable": "Metric"},
        title="<b>Cumulative Revenue Growth & 7-Day Rolling Trend</b>",
        color_discrete_map={"cumulative_gmv": "#10b981", "rolling_7day_avg": "#38bdf8"},
    )
    fig_cum.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.4)")
    st.plotly_chart(fig_cum, use_container_width=True)
finally:
    conn.close()
