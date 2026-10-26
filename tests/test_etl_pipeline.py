"""Unit tests for the end-to-end ETL and database mart creation."""

import duckdb

from frogeindrip.etl.pipeline import FrogeindripETL


def test_etl_pipeline_run(tmp_path):
    """Test full ETL run and verify creation of dimensional tables and data marts."""
    db_file = tmp_path / "test_run.duckdb"
    etl = FrogeindripETL(db_path=db_file, seed=42)

    result = etl.run()
    assert result["status"] == "SUCCESS"
    assert result["total_orders"] > 0
    assert result["total_net_sales"] > 0
    etl.close()

    # Reconnect and verify table schema
    conn = duckdb.connect(str(db_file), read_only=True)
    tables = [r[0] for r in conn.execute("SHOW TABLES").fetchall()]
    conn.close()

    expected_tables = [
        "raw_customers",
        "raw_products",
        "raw_orders",
        "raw_order_items",
        "dim_customers",
        "dim_products",
        "dim_dates",
        "fct_sales",
        "mart_monthly_performance",
        "mart_rfm_segments",
        "mart_cohort_retention",
    ]

    for tbl in expected_tables:
        assert tbl in tables, f"Expected table {tbl} was not created"
