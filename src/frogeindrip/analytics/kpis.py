"""Core KPI calculation engine for Frogeindrip Analytics Platform."""

from typing import Any

import duckdb
import pandas as pd

from frogeindrip.config import DB_PATH


def get_executive_kpis(conn: duckdb.DuckDBPyConnection | None = None) -> dict[str, Any]:
    """Retrieve executive financial and operational KPIs from DuckDB marts."""
    close_conn = False
    if conn is None:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        close_conn = True

    try:
        # High-level totals
        totals = conn.execute("""
            SELECT
                COUNT(DISTINCT order_id) AS total_orders,
                COUNT(DISTINCT customer_id) AS unique_customers,
                ROUND(SUM(gross_amount), 2) AS total_gross_sales,
                ROUND(SUM(discount_amount), 2) AS total_discounts,
                ROUND(SUM(net_amount), 2) AS total_net_sales,
                ROUND(AVG(net_amount), 2) AS average_order_value,
                ROUND(SUM(tax_amount), 2) AS total_taxes,
                ROUND(SUM(shipping_amount), 2) AS total_shipping
            FROM raw_orders
            WHERE status = 'completed'
        """).fetchone()

        profit_totals = conn.execute("""
            SELECT
                ROUND(SUM(item_cogs), 2) AS total_cogs,
                ROUND(SUM(item_gross_profit), 2) AS total_gross_profit,
                SUM(quantity) AS total_units_sold
            FROM fct_sales
            WHERE order_status = 'completed'
        """).fetchone()

        status_counts = conn.execute("""
            SELECT
                status,
                COUNT(*) AS cnt,
                ROUND(SUM(net_amount), 2) AS amount
            FROM raw_orders
            GROUP BY status
        """).fetchall()

        repeat_metrics = conn.execute("""
            SELECT
                COUNT(DISTINCT CASE WHEN lifetime_orders > 1 THEN customer_id END) AS repeat_customers,
                COUNT(DISTINCT customer_id) AS total_customers,
                ROUND(SUM(CASE WHEN lifetime_orders > 1 THEN lifetime_net_spend ELSE 0 END), 2) AS repeat_spend,
                ROUND(SUM(lifetime_net_spend), 2) AS total_spend
            FROM dim_customers
            WHERE lifetime_orders > 0
        """).fetchone()

        gross_sales = totals[2] or 0.0
        net_sales = totals[4] or 0.0
        cogs = profit_totals[0] or 0.0
        gross_profit = profit_totals[1] or 0.0
        units_sold = profit_totals[2] or 0

        margin_pct = round((gross_profit / net_sales * 100), 2) if net_sales > 0 else 0.0
        repeat_cust_pct = round((repeat_metrics[0] / repeat_metrics[1] * 100), 2) if repeat_metrics[1] > 0 else 0.0
        repeat_gmv_pct = round((repeat_metrics[2] / repeat_metrics[3] * 100), 2) if repeat_metrics[3] > 0 else 0.0

        return {
            "total_orders": totals[0],
            "unique_customers": totals[1],
            "total_gross_sales": gross_sales,
            "total_discounts": totals[3] or 0.0,
            "total_net_sales": net_sales,
            "average_order_value": totals[5] or 0.0,
            "total_cogs": cogs,
            "total_gross_profit": gross_profit,
            "gross_margin_pct": margin_pct,
            "total_units_sold": units_sold,
            "repeat_customers": repeat_metrics[0],
            "repeat_customer_rate_pct": repeat_cust_pct,
            "repeat_buyer_gmv": repeat_metrics[2],
            "repeat_buyer_gmv_share_pct": repeat_gmv_pct,
            "status_breakdown": {row[0]: {"count": row[1], "amount": row[2]} for row in status_counts},
        }
    finally:
        if close_conn:
            conn.close()


def get_sales_by_time_dimensions(conn: duckdb.DuckDBPyConnection | None = None) -> dict[str, pd.DataFrame]:
    """Retrieve day-of-week, hour-of-day, and monthly sales trends."""
    close_conn = False
    if conn is None:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        close_conn = True

    try:
        # Day of week
        dow_df = conn.execute("""
            SELECT
                strftime(order_date, '%A') AS day_name,
                EXTRACT(isodow FROM order_date) AS day_num,
                COUNT(order_id) AS orders_count,
                ROUND(SUM(net_amount), 2) AS net_sales,
                ROUND(AVG(net_amount), 2) AS aov
            FROM raw_orders
            WHERE status = 'completed'
            GROUP BY 1, 2
            ORDER BY day_num ASC
        """).fetchdf()

        # Hour of day
        hour_df = conn.execute("""
            SELECT
                EXTRACT(hour FROM order_date) AS hour_of_day,
                COUNT(order_id) AS orders_count,
                ROUND(SUM(net_amount), 2) AS net_sales
            FROM raw_orders
            WHERE status = 'completed'
            GROUP BY 1
            ORDER BY hour_of_day ASC
        """).fetchdf()

        # Monthly performance
        monthly_df = conn.execute("""
            SELECT * FROM mart_monthly_performance ORDER BY year_month ASC
        """).fetchdf()

        return {
            "day_of_week": dow_df,
            "hour_of_day": hour_df,
            "monthly_trends": monthly_df,
        }
    finally:
        if close_conn:
            conn.close()
