"""Unit tests for executive KPIs and financial metrics."""

from frogeindrip.analytics.kpis import get_executive_kpis, get_sales_by_time_dimensions


def test_executive_kpis_reconciliation(db_conn):
    """Verify that calculated KPIs follow core accounting identities."""
    kpis = get_executive_kpis(conn=db_conn)

    assert kpis["total_orders"] > 0
    assert kpis["unique_customers"] > 0
    assert kpis["total_net_sales"] > 0

    # Net Sales + Discounts == Gross Sales (within rounding)
    assert abs((kpis["total_net_sales"] + kpis["total_discounts"]) - kpis["total_gross_sales"]) < 0.10

    # Gross Profit == Net Sales - COGS
    assert abs((kpis["total_net_sales"] - kpis["total_cogs"]) - kpis["total_gross_profit"]) < 0.10

    # Realized Margin % between 0 and 100%
    assert 0.0 < kpis["gross_margin_pct"] < 100.0


def test_sales_by_time_dimensions(db_conn):
    """Verify day-of-week and hour-of-day distributions."""
    time_data = get_sales_by_time_dimensions(conn=db_conn)

    dow_df = time_data["day_of_week"]
    hour_df = time_data["hour_of_day"]
    monthly_df = time_data["monthly_trends"]

    assert len(dow_df) == 7  # 7 days in a week
    assert len(hour_df) > 0  # Hours with sales
    assert len(monthly_df) >= 10  # Months in simulation
