"""Unit tests for Pandera schema validations and data quality assertions."""

from frogeindrip.etl.validators import validate_dataset


def test_validation_passes_on_clean_data(synthetic_data_dfs):
    """Verify that unmodified synthetic data passes 100% of validation assertions."""
    c, p, o, oi = synthetic_data_dfs
    report = validate_dataset(c, p, o, oi)

    assert report.is_valid is True
    assert len(report.failed_checks) == 0
    assert len(report.passed_checks) >= 10


def test_validation_catches_orphaned_orders(synthetic_data_dfs):
    """Verify that orphaned orders with non-existent customers are caught."""
    c, p, o, oi = [df.copy() for df in synthetic_data_dfs]
    # Introduce an orphaned customer_id in an order
    o.loc[0, "customer_id"] = "CUST-9999"

    report = validate_dataset(c, p, o, oi)
    assert report.is_valid is False
    assert any("Orphaned orders found" in check for check in report.failed_checks)


def test_validation_catches_financial_discrepancy(synthetic_data_dfs):
    """Verify that mismatched order gross and item sums are detected."""
    c, p, o, oi = [df.copy() for df in synthetic_data_dfs]
    # Modify an order gross without changing the item
    o.loc[0, "gross_amount"] = o.loc[0, "gross_amount"] + 50.0

    report = validate_dataset(c, p, o, oi)
    assert report.is_valid is False
    assert any("Mismatches between orders and items" in check for check in report.failed_checks)
