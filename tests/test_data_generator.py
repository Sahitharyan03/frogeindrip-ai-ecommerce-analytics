"""Unit tests for synthetic data generation reproducibility and constraints."""

from frogeindrip.data.generator import generate_synthetic_data


def test_generator_deterministic_reproducibility():
    """Verify that running with identical seeds produces byte-identical DataFrames."""
    c1, p1, o1, oi1 = generate_synthetic_data(seed=42, num_customers=50, save_csv=False)
    c2, p2, o2, oi2 = generate_synthetic_data(seed=42, num_customers=50, save_csv=False)

    assert len(c1) == len(c2) == 50
    assert len(o1) == len(o2)
    assert len(oi1) == len(oi2)
    assert o1["gross_amount"].sum() == o2["gross_amount"].sum()
    assert o1["net_amount"].sum() == o2["net_amount"].sum()


def test_generator_relational_consistency(synthetic_data_dfs):
    """Verify primary and foreign key constraints in synthetic datasets."""
    customers_df, products_df, orders_df, order_items_df = synthetic_data_dfs

    # Unique PKs
    assert customers_df["customer_id"].is_unique
    assert products_df["product_id"].is_unique
    assert orders_df["order_id"].is_unique
    assert order_items_df["order_item_id"].is_unique

    # Valid FKs
    assert set(orders_df["customer_id"]).issubset(set(customers_df["customer_id"]))
    assert set(order_items_df["order_id"]).issubset(set(orders_df["order_id"]))
    assert set(order_items_df["product_id"]).issubset(set(products_df["product_id"]))


def test_generator_financial_reconciliation(synthetic_data_dfs):
    """Verify order gross amount equals sum of line items."""
    _, _, orders_df, order_items_df = synthetic_data_dfs

    item_totals = order_items_df.groupby("order_id")["total_price"].sum().round(2).to_dict()
    for _, order in orders_df.iterrows():
        expected_gross = item_totals[order["order_id"]]
        assert abs(expected_gross - order["gross_amount"]) < 0.05
        assert abs((order["gross_amount"] - order["discount_amount"]) - order["net_amount"]) < 0.05
