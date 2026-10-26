"""RFM (Recency, Frequency, Monetary) segmentation analysis module."""

from typing import Any

import duckdb

from frogeindrip.config import DB_PATH


def get_rfm_analysis(conn: duckdb.DuckDBPyConnection | None = None) -> dict[str, Any]:
    """Retrieve RFM segment distribution, metrics, and customer-level scores."""
    close_conn = False
    if conn is None:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        close_conn = True

    try:
        # Segment Level Aggregates
        segment_summary_df = conn.execute("""
            SELECT
                segment_label,
                COUNT(customer_id) AS customer_count,
                ROUND((COUNT(customer_id) * 100.0) / SUM(COUNT(customer_id)) OVER (), 2) AS customer_share_pct,
                ROUND(SUM(monetary), 2) AS total_segment_spend,
                ROUND((SUM(monetary) / SUM(SUM(monetary)) OVER ()) * 100, 2) AS gmv_share_pct,
                ROUND(AVG(monetary), 2) AS avg_customer_spend,
                ROUND(AVG(frequency), 2) AS avg_frequency,
                ROUND(AVG(recency_days), 1) AS avg_recency_days
            FROM mart_rfm_segments
            GROUP BY segment_label
            ORDER BY total_segment_spend DESC
        """).fetchdf()

        # Customer Level Details (Top 100)
        customer_rfm_df = conn.execute("""
            SELECT
                r.customer_id,
                c.first_name || ' ' || c.last_name AS customer_name,
                c.acquisition_channel,
                c.state,
                r.recency_days,
                r.frequency,
                r.monetary,
                r.r_score,
                r.f_score,
                r.m_score,
                r.rfm_code,
                r.segment_label
            FROM mart_rfm_segments r
            JOIN dim_customers c ON r.customer_id = c.customer_id
            ORDER BY r.monetary DESC
        """).fetchdf()

        return {
            "segment_summary": segment_summary_df,
            "customer_rfm": customer_rfm_df,
        }
    finally:
        if close_conn:
            conn.close()
