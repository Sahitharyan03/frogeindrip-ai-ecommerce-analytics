"""Unit tests for RFM scoring, cohort retention, and repeat buyer contribution."""

from frogeindrip.analytics.cohorts import get_cohort_matrix
from frogeindrip.analytics.retention import get_repeat_buyer_analysis
from frogeindrip.analytics.rfm import get_rfm_analysis


def test_rfm_analysis_structure(db_conn):
    """Verify RFM segment distributions and scoring bounds."""
    rfm = get_rfm_analysis(conn=db_conn)
    summary = rfm["segment_summary"]
    customers = rfm["customer_rfm"]

    assert len(summary) > 0
    # Customer share percentages sum to 100%
    assert abs(summary["customer_share_pct"].sum() - 100.0) < 1.0

    # Scores within 1 to 5
    assert customers["r_score"].between(1, 5).all()
    assert customers["f_score"].between(1, 5).all()
    assert customers["m_score"].between(1, 5).all()


def test_cohort_matrix_integrity(db_conn):
    """Verify cohort retention table structure and decay behavior."""
    cohort_data = get_cohort_matrix(conn=db_conn)
    pivot = cohort_data["retention_pivot"]

    # Month 0 retention is always 100%
    assert (pivot[0] == 100.0).all()

    # Retention in subsequent months should be <= 100%
    if 1 in pivot.columns:
        m1_vals = pivot[1].dropna()
        assert (m1_vals <= 100.0).all()


def test_repeat_buyer_reconciliation(db_conn):
    """Verify Method A and Method B repeat buyer GMV contributions."""
    repeat = get_repeat_buyer_analysis(conn=db_conn)

    assert repeat["total_orders"] > 0
    assert repeat["total_customers"] > 0
    assert 0.0 <= repeat["lifetime_repeat_gmv_pct"] <= 100.0
    assert 0.0 <= repeat["point_in_time_repeat_gmv_pct"] <= 100.0

    # Strict point-in-time repeat spend must be <= lifetime repeat spend
    assert repeat["point_in_time_repeat_gmv"] <= repeat["lifetime_repeat_gmv"]
