"""Cohort retention and customer decay analytics module."""

from typing import Any

import duckdb

from frogeindrip.config import DB_PATH


def get_cohort_matrix(conn: duckdb.DuckDBPyConnection | None = None) -> dict[str, Any]:
    """Retrieve cohort retention table and formatted pivot matrices."""
    close_conn = False
    if conn is None:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        close_conn = True

    try:
        raw_cohort_df = conn.execute("""
            SELECT
                cohort_month,
                cohort_size,
                period_number,
                active_customers,
                retention_rate_pct,
                cohort_period_revenue
            FROM mart_cohort_retention
            ORDER BY cohort_month, period_number
        """).fetchdf()

        # Pivot for Customer Retention Rate Heatmap
        retention_pivot = raw_cohort_df.pivot(
            index="cohort_month",
            columns="period_number",
            values="retention_rate_pct",
        )

        # Pivot for Active Customer Counts
        count_pivot = raw_cohort_df.pivot(
            index="cohort_month",
            columns="period_number",
            values="active_customers",
        )

        # Pivot for Period Revenue
        revenue_pivot = raw_cohort_df.pivot(
            index="cohort_month",
            columns="period_number",
            values="cohort_period_revenue",
        )

        # Overall Average Retention by Month Elapsed
        avg_retention_curve = raw_cohort_df.groupby("period_number")["retention_rate_pct"].mean().round(2).reset_index()

        return {
            "raw_cohort": raw_cohort_df,
            "retention_pivot": retention_pivot,
            "count_pivot": count_pivot,
            "revenue_pivot": revenue_pivot,
            "avg_retention_curve": avg_retention_curve,
        }
    finally:
        if close_conn:
            conn.close()
