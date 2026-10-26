"""Approved parameterized, read-only analytics tool registry for AI Copilot."""

from typing import Any

import duckdb

from frogeindrip.config import DB_PATH, VERIFIED_EVIDENCE


def get_verified_screenshot_evidence() -> dict[str, Any]:
    """Retrieve immutable baseline figures directly from verified Square screenshots."""
    return {
        "tool_name": "get_verified_screenshot_evidence",
        "evidence_tier": "Verified Screenshot Evidence",
        "reporting_period": "Sep 01, 2025 – Jul 31, 2026 (Group A) & Jul 01, 2025 – Jul 01, 2026 (Group B)",
        "provenance": "Square Analytics POS Console (Raw Capture)",
        "data": VERIFIED_EVIDENCE,
        "summary": (
            "Verified Square Evidence: Group A Net Sales = $46,271.26 (Sep 2025 – Jul 2026). "
            "Group B Gross Sales = $38,131.26 (Jul 2025 – Jul 2026) with peak volume in May 2026 ($8,397.00) "
            "and drop-off in July 2026 ($1,505.00). Prior year baseline was $0.00 (+100% initial launch tag)."
        ),
    }


def get_executive_overview() -> dict[str, Any]:
    """Retrieve high-level revenue, order volume, AOV, and margin totals."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        totals = conn.execute("""
            SELECT
                COUNT(DISTINCT order_id) AS total_orders,
                COUNT(DISTINCT customer_id) AS total_customers,
                ROUND(SUM(gross_amount), 2) AS total_gross_sales,
                ROUND(SUM(discount_amount), 2) AS total_discounts,
                ROUND(SUM(net_amount), 2) AS total_net_sales,
                ROUND(AVG(net_amount), 2) AS aov
            FROM raw_orders
            WHERE status = 'completed'
        """).fetchone()

        profit = conn.execute("""
            SELECT
                ROUND(SUM(item_cogs), 2) AS total_cogs,
                ROUND(SUM(item_gross_profit), 2) AS total_profit,
                SUM(quantity) AS units_sold
            FROM fct_sales
            WHERE order_status = 'completed'
        """).fetchone()

        net_sales = totals[4] or 0.0
        profit_val = profit[1] or 0.0
        margin_pct = round((profit_val / net_sales * 100), 2) if net_sales > 0 else 0.0

        metrics = {
            "total_orders": totals[0],
            "total_customers": totals[1],
            "total_gross_sales": totals[2],
            "total_discounts": totals[3],
            "total_net_sales": net_sales,
            "average_order_value": totals[5],
            "total_cogs": profit[0],
            "total_gross_profit": profit_val,
            "gross_margin_pct": margin_pct,
            "total_units_sold": profit[2],
        }

        return {
            "tool_name": "get_executive_overview",
            "evidence_tier": "Synthetic Demonstration (Deterministic Pipeline)",
            "reporting_period": "Sep 01, 2025 – Jul 31, 2026",
            "provenance": "DuckDB Marts (`fct_sales`, `raw_orders`)",
            "data": metrics,
            "summary": (
                f"Completed {metrics['total_orders']} orders across {metrics['total_customers']} customers. "
                f"Total Net Sales: ${metrics['total_net_sales']:,.2f} with AOV of ${metrics['average_order_value']:.2f}. "
                f"Gross Profit: ${metrics['total_gross_profit']:,.2f} ({metrics['gross_margin_pct']}% realized margin)."
            ),
        }
    finally:
        conn.close()


def get_monthly_revenue_and_mom() -> dict[str, Any]:
    """Retrieve monthly sales trends and Month-over-Month (MoM) growth rates."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        df = conn.execute("""
            SELECT
                year_month,
                total_orders,
                total_net_sales,
                average_order_value,
                total_gross_profit,
                gross_margin_pct,
                mom_growth_pct
            FROM mart_monthly_performance
            ORDER BY year_month ASC
        """).fetchdf()

        records = df.to_dict(orient="records")
        peak_row = df.loc[df["total_net_sales"].idxmax()]

        return {
            "tool_name": "get_monthly_revenue_and_mom",
            "evidence_tier": "Synthetic Demonstration",
            "reporting_period": "Sep 2025 – Jul 2026",
            "provenance": "DuckDB Mart: `mart_monthly_performance`",
            "data": records,
            "summary": (
                f"Peak sales occurred in {peak_row['year_month']} with ${peak_row['total_net_sales']:,.2f} net revenue. "
                f"Tracked {len(records)} continuous operating months."
            ),
        }
    finally:
        conn.close()


def get_repeat_buyer_contribution() -> dict[str, Any]:
    """Retrieve repeat customer rate and repeat GMV contribution under lifetime & point-in-time rules."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        row = conn.execute("""
            WITH sequenced AS (
                SELECT
                    order_id,
                    customer_id,
                    net_amount,
                    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS seq,
                    COUNT(order_id) OVER (PARTITION BY customer_id) AS lifetime_cnt
                FROM raw_orders
                WHERE status = 'completed'
            )
            SELECT
                COUNT(DISTINCT order_id) AS total_orders,
                COUNT(DISTINCT customer_id) AS total_customers,
                ROUND(SUM(net_amount), 2) AS total_gmv,
                -- Lifetime definition
                ROUND(SUM(CASE WHEN lifetime_cnt >= 2 THEN net_amount ELSE 0 END), 2) AS lifetime_repeat_gmv,
                ROUND((SUM(CASE WHEN lifetime_cnt >= 2 THEN net_amount ELSE 0 END) / SUM(net_amount)) * 100, 2) AS lifetime_repeat_pct,
                -- Point in time definition
                ROUND(SUM(CASE WHEN seq >= 2 THEN net_amount ELSE 0 END), 2) AS pit_repeat_gmv,
                ROUND((SUM(CASE WHEN seq >= 2 THEN net_amount ELSE 0 END) / SUM(net_amount)) * 100, 2) AS pit_repeat_pct
            FROM sequenced
        """).fetchone()

        data = {
            "total_orders": row[0],
            "total_customers": row[1],
            "total_gmv": row[2],
            "lifetime_repeat_buyer_gmv": row[3],
            "lifetime_repeat_buyer_gmv_share_pct": row[4],
            "point_in_time_repeat_gmv": row[5],
            "point_in_time_repeat_gmv_share_pct": row[6],
        }

        return {
            "tool_name": "get_repeat_buyer_contribution",
            "evidence_tier": "Synthetic Demonstration (Simulating Pending Resume Claim)",
            "reporting_period": "Sep 2025 – Jul 2026",
            "provenance": "DuckDB Mart (`dim_customers`, `fct_sales`)",
            "data": data,
            "summary": (
                f"Repeat Buyer Analysis: Under lifetime definition, repeat buyers account for {data['lifetime_repeat_buyer_gmv_share_pct']}% "
                f"of GMV (${data['lifetime_repeat_buyer_gmv']:,.2f}). Under strict non-leaking point-in-time calculation (orders >= 2), "
                f"repeat orders drive {data['point_in_time_repeat_gmv_share_pct']}% of total sales."
            ),
        }
    finally:
        conn.close()


def get_top_products_and_margins(limit: int = 5) -> dict[str, Any]:
    """Retrieve top-performing products ranked by net revenue and gross margin."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        df = conn.execute(f"""
            SELECT
                p.product_id,
                p.product_name,
                p.category,
                p.retail_price,
                p.cost_price,
                SUM(f.quantity) AS units_sold,
                ROUND(SUM(f.item_net_sales), 2) AS net_sales,
                ROUND(SUM(f.item_gross_profit), 2) AS gross_profit,
                ROUND((SUM(f.item_gross_profit) / NULLIF(SUM(f.item_net_sales), 0)) * 100, 2) AS realized_margin_pct
            FROM fct_sales f
            JOIN dim_products p ON f.product_id = p.product_id
            WHERE f.order_status = 'completed'
            GROUP BY 1, 2, 3, 4, 5
            ORDER BY gross_profit DESC
            LIMIT {limit}
        """).fetchdf()

        records = df.to_dict(orient="records")
        return {
            "tool_name": "get_top_products_and_margins",
            "evidence_tier": "Synthetic Demonstration",
            "reporting_period": "Sep 2025 – Jul 2026",
            "provenance": "DuckDB Marts (`fct_sales`, `dim_products`)",
            "data": records,
            "summary": f"Top product by profit is {records[0]['product_name']} generating ${records[0]['gross_profit']:,.2f} profit ({records[0]['realized_margin_pct']}% margin).",
        }
    finally:
        conn.close()


def get_rfm_segments() -> dict[str, Any]:
    """Retrieve RFM segment sizes, revenue shares, and average order frequency."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        df = conn.execute("""
            SELECT
                segment_label,
                COUNT(customer_id) AS customer_count,
                ROUND(SUM(monetary), 2) AS total_spend,
                ROUND((SUM(monetary) / SUM(SUM(monetary)) OVER ()) * 100, 2) AS gmv_share_pct,
                ROUND(AVG(monetary), 2) AS avg_spend,
                ROUND(AVG(frequency), 2) AS avg_frequency,
                ROUND(AVG(recency_days), 1) AS avg_recency_days
            FROM mart_rfm_segments
            GROUP BY segment_label
            ORDER BY total_spend DESC
        """).fetchdf()

        records = df.to_dict(orient="records")
        top_segment = records[0]

        return {
            "tool_name": "get_rfm_segments",
            "evidence_tier": "Synthetic Demonstration",
            "reporting_period": "As of Aug 01, 2026",
            "provenance": "DuckDB Mart: `mart_rfm_segments`",
            "data": records,
            "summary": f"Largest revenue segment is '{top_segment['segment_label']}' driving {top_segment['gmv_share_pct']}% of total brand GMV with ${top_segment['total_spend']:,.2f} spend.",
        }
    finally:
        conn.close()


def get_cohort_retention() -> dict[str, Any]:
    """Retrieve monthly cohort sizes and average retention rates over time."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        df = conn.execute("""
            SELECT
                cohort_month,
                cohort_size,
                period_number,
                active_customers,
                retention_rate_pct
            FROM mart_cohort_retention
            WHERE period_number <= 3
            ORDER BY cohort_month, period_number
        """).fetchdf()

        avg_m1 = conn.execute("""
            SELECT ROUND(AVG(retention_rate_pct), 2)
            FROM mart_cohort_retention
            WHERE period_number = 1
        """).fetchone()[0]

        return {
            "tool_name": "get_cohort_retention",
            "evidence_tier": "Synthetic Demonstration",
            "reporting_period": "Sep 2025 – Jul 2026",
            "provenance": "DuckDB Mart: `mart_cohort_retention`",
            "data": df.to_dict(orient="records"),
            "summary": f"Average Month-1 customer retention across all cohorts is {avg_m1}%.",
        }
    finally:
        conn.close()


# Registry of approved tools
APPROVED_TOOLS = {
    "get_verified_screenshot_evidence": get_verified_screenshot_evidence,
    "get_executive_overview": get_executive_overview,
    "get_monthly_revenue_and_mom": get_monthly_revenue_and_mom,
    "get_repeat_buyer_contribution": get_repeat_buyer_contribution,
    "get_top_products_and_margins": get_top_products_and_margins,
    "get_rfm_segments": get_rfm_segments,
    "get_cohort_retention": get_cohort_retention,
}
