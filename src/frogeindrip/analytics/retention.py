"""Repeat buyer contribution, purchase intervals, and retention metrics."""

from typing import Any

import duckdb

from frogeindrip.config import DB_PATH


def get_repeat_buyer_analysis(conn: duckdb.DuckDBPyConnection | None = None) -> dict[str, Any]:
    """Retrieve detailed point-in-time vs lifetime repeat buyer GMV analysis."""
    close_conn = False
    if conn is None:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        close_conn = True

    try:
        # Comparison between Lifetime and Point-in-Time models
        method_comparison = conn.execute("""
            WITH sequenced_orders AS (
                SELECT
                    order_id,
                    customer_id,
                    order_date,
                    net_amount,
                    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS customer_order_seq,
                    COUNT(order_id) OVER (PARTITION BY customer_id) AS customer_lifetime_orders
                FROM raw_orders
                WHERE status = 'completed'
            )
            SELECT
                COUNT(DISTINCT order_id) AS total_orders,
                COUNT(DISTINCT customer_id) AS total_customers,
                ROUND(SUM(net_amount), 2) AS total_net_sales,
                -- Lifetime definition
                ROUND(SUM(CASE WHEN customer_lifetime_orders >= 2 THEN net_amount ELSE 0 END), 2) AS lifetime_repeat_gmv,
                ROUND((SUM(CASE WHEN customer_lifetime_orders >= 2 THEN net_amount ELSE 0 END) / SUM(net_amount)) * 100, 2) AS lifetime_repeat_gmv_pct,
                -- Point-in-Time definition (No lookahead leakage)
                ROUND(SUM(CASE WHEN customer_order_seq >= 2 THEN net_amount ELSE 0 END), 2) AS pit_repeat_gmv,
                ROUND((SUM(CASE WHEN customer_order_seq >= 2 THEN net_amount ELSE 0 END) / SUM(net_amount)) * 100, 2) AS pit_repeat_gmv_pct,
                COUNT(DISTINCT CASE WHEN customer_order_seq >= 2 THEN order_id END) AS pit_repeat_orders,
                ROUND((COUNT(DISTINCT CASE WHEN customer_order_seq >= 2 THEN order_id END) * 100.0) / COUNT(DISTINCT order_id), 2) AS pit_repeat_order_pct
            FROM sequenced_orders
        """).fetchone()

        # Inter-purchase interval distribution (days between order 1 and order 2)
        intervals_df = conn.execute("""
            WITH order_ranks AS (
                SELECT
                    customer_id,
                    order_id,
                    order_date,
                    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS seq,
                    LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS prev_date
                FROM raw_orders
                WHERE status = 'completed'
            )
            SELECT
                customer_id,
                order_id,
                seq,
                order_date,
                prev_date,
                DATEDIFF('day', prev_date, order_date) AS days_between_orders
            FROM order_ranks
            WHERE seq = 2
        """).fetchdf()

        avg_days = intervals_df["days_between_orders"].mean() if len(intervals_df) > 0 else 0
        median_days = intervals_df["days_between_orders"].median() if len(intervals_df) > 0 else 0

        # Frequency distribution
        freq_df = conn.execute("""
            SELECT
                lifetime_orders,
                COUNT(customer_id) AS customer_count,
                ROUND(SUM(lifetime_net_spend), 2) AS total_spend
            FROM dim_customers
            WHERE lifetime_orders > 0
            GROUP BY lifetime_orders
            ORDER BY lifetime_orders ASC
        """).fetchdf()

        return {
            "total_orders": method_comparison[0],
            "total_customers": method_comparison[1],
            "total_net_sales": method_comparison[2],
            "lifetime_repeat_gmv": method_comparison[3],
            "lifetime_repeat_gmv_pct": method_comparison[4],
            "point_in_time_repeat_gmv": method_comparison[5],
            "point_in_time_repeat_gmv_pct": method_comparison[6],
            "point_in_time_repeat_orders": method_comparison[7],
            "point_in_time_repeat_order_pct": method_comparison[8],
            "avg_days_to_repeat": round(float(avg_days), 1),
            "median_days_to_repeat": round(float(median_days), 1),
            "intervals": intervals_df,
            "frequency_distribution": freq_df,
        }
    finally:
        if close_conn:
            conn.close()
