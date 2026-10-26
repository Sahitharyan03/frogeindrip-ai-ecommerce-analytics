"""Page 4: Product Performance, Category Analysis & Margins."""

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

from app.components.ui import inject_custom_css, render_page_header, render_sidebar
from frogeindrip.config import DB_PATH

st.set_page_config(page_title="Product Performance | Frogeindrip", page_icon="🐸", layout="wide")
inject_custom_css()
render_sidebar()

render_page_header(
    title="Product & Category Intelligence",
    subtitle="SKU-level volume, realized gross margins, unit costs (COGS), and catalog profitability.",
    badge_type="synthetic",
)

conn = duckdb.connect(str(DB_PATH), read_only=True)
try:
    # Category summary
    cat_df = conn.execute("""
        SELECT
            p.category,
            COUNT(DISTINCT p.product_id) AS sku_count,
            SUM(f.quantity) AS units_sold,
            ROUND(SUM(f.item_net_sales), 2) AS net_revenue,
            ROUND(SUM(f.item_cogs), 2) AS total_cogs,
            ROUND(SUM(f.item_gross_profit), 2) AS gross_profit,
            ROUND((SUM(f.item_gross_profit) / NULLIF(SUM(f.item_net_sales), 0)) * 100, 2) AS margin_pct
        FROM fct_sales f
        JOIN dim_products p ON f.product_id = p.product_id
        WHERE f.order_status = 'completed'
        GROUP BY p.category
        ORDER BY net_revenue DESC;
    """).fetchdf()

    # Product level performance
    prod_df = conn.execute("""
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            p.retail_price,
            p.cost_price,
            SUM(f.quantity) AS units_sold,
            ROUND(SUM(f.item_net_sales), 2) AS net_sales,
            ROUND(SUM(f.item_gross_profit), 2) AS gross_profit,
            ROUND((SUM(f.item_gross_profit) / NULLIF(SUM(f.item_net_sales), 0)) * 100, 2) AS realized_margin_pct,
            ROUND((SUM(f.item_gross_profit) / SUM(SUM(f.item_gross_profit)) OVER ()) * 100, 2) AS profit_share_pct
        FROM fct_sales f
        JOIN dim_products p ON f.product_id = p.product_id
        WHERE f.order_status = 'completed'
        GROUP BY 1, 2, 3, 4, 5
        ORDER BY gross_profit DESC;
    """).fetchdf()

    # Category Breakdown Visuals
    st.markdown("### 🏷️ Apparel Category Performance")
    cat_c1, cat_c2 = st.columns([3, 2])

    with cat_c1:
        fig_cat = px.bar(
            cat_df,
            x="category",
            y="net_revenue",
            color="margin_pct",
            color_continuous_scale="Viridis",
            labels={"net_revenue": "Net Revenue ($)", "category": "Category", "margin_pct": "Margin (%)"},
            title="<b>Category Net Revenue & Gross Margin %</b>",
        )
        fig_cat.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.4)")
        st.plotly_chart(fig_cat, use_container_width=True)

    with cat_c2:
        st.markdown("#### Category Metrics")
        st.dataframe(cat_df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Product Performance Table
    st.markdown("### 👕 SKU-Level Profitability & Catalog Contribution")
    st.dataframe(prod_df, use_container_width=True, hide_index=True)

    # Margin vs Volume Matrix
    st.markdown("### 🎯 Price vs. Realized Gross Margin Matrix")
    fig_scatter = px.scatter(
        prod_df,
        x="retail_price",
        y="realized_margin_pct",
        size="units_sold",
        color="category",
        hover_name="product_name",
        labels={"retail_price": "MSRP Retail Price ($)", "realized_margin_pct": "Realized Gross Margin (%)"},
        title="<b>Product Pricing vs Margin Dynamics (Bubble Size: Units Sold)</b>",
    )
    fig_scatter.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.4)")
    st.plotly_chart(fig_scatter, use_container_width=True)

finally:
    conn.close()
