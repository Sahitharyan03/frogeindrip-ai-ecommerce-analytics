"""Automated data quality assertions and validation rules for Frogeindrip ETL."""

from dataclasses import dataclass, field

import pandas as pd
import pandera.errors

from frogeindrip.data.schema import (
    CustomerSchema,
    OrderItemSchema,
    OrderSchema,
    ProductSchema,
)


@dataclass
class ValidationReport:
    is_valid: bool = True
    passed_checks: list[str] = field(default_factory=list)
    failed_checks: list[str] = field(default_factory=list)
    errors: dict[str, list[str]] = field(default_factory=dict)
    summary_stats: dict[str, float] = field(default_factory=dict)


def validate_dataset(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    order_items_df: pd.DataFrame,
) -> ValidationReport:
    """Run comprehensive automated schema and business rule validations."""
    report = ValidationReport()

    # 1. Pandera Schema Validation
    schema_map = [
        ("Customers Schema", CustomerSchema, customers_df),
        ("Products Schema", ProductSchema, products_df),
        ("Orders Schema", OrderSchema, orders_df),
        ("Order Items Schema", OrderItemSchema, order_items_df),
    ]

    for name, schema, df in schema_map:
        try:
            schema.validate(df, lazy=True)
            report.passed_checks.append(f"{name} check passed")
        except pandera.errors.SchemaErrors as err:
            report.is_valid = False
            report.failed_checks.append(f"{name} check failed")
            report.errors[name] = [str(e) for e in err.failure_cases.head(10).to_dict(orient="records")]

    # 2. Referential Integrity Validations
    # Check that all order customer_ids exist in customers_df
    orphaned_orders = set(orders_df["customer_id"]) - set(customers_df["customer_id"])
    if not orphaned_orders:
        report.passed_checks.append("Referential Integrity: All orders map to existing customers")
    else:
        report.is_valid = False
        report.failed_checks.append("Referential Integrity: Orphaned orders found")
        report.errors["orphaned_orders"] = list(orphaned_orders)[:5]

    # Check that all order_item order_ids exist in orders_df
    orphaned_items = set(order_items_df["order_id"]) - set(orders_df["order_id"])
    if not orphaned_items:
        report.passed_checks.append("Referential Integrity: All order items map to existing orders")
    else:
        report.is_valid = False
        report.failed_checks.append("Referential Integrity: Orphaned order items found")
        report.errors["orphaned_items"] = list(orphaned_items)[:5]

    # Check that all product_ids in order_items exist in products_df
    orphaned_products = set(order_items_df["product_id"]) - set(products_df["product_id"])
    if not orphaned_products:
        report.passed_checks.append("Referential Integrity: All order items map to existing catalog products")
    else:
        report.is_valid = False
        report.failed_checks.append("Referential Integrity: Unknown product IDs found in order items")
        report.errors["orphaned_products"] = list(orphaned_products)[:5]

    # 3. Financial Reconciliation Validations
    # Reconcile order gross_amount with sum of item total_price
    item_sums = order_items_df.groupby("order_id")["total_price"].sum().round(2).to_dict()
    reconciliation_mismatches = []
    for _, order in orders_df.iterrows():
        expected_gross = item_sums.get(order["order_id"], 0.0)
        actual_gross = round(float(order["gross_amount"]), 2)
        if abs(expected_gross - actual_gross) > 0.05:
            reconciliation_mismatches.append(
                f"Order {order['order_id']}: Expected gross {expected_gross}, found {actual_gross}"
            )

    if not reconciliation_mismatches:
        report.passed_checks.append("Financial Reconciliation: Order gross amounts match item totals 100%")
    else:
        report.is_valid = False
        report.failed_checks.append("Financial Reconciliation: Mismatches between orders and items")
        report.errors["reconciliation_mismatches"] = reconciliation_mismatches[:5]

    # 4. Duplicate Checks
    for tbl_name, col, df in [
        ("customers", "customer_id", customers_df),
        ("products", "product_id", products_df),
        ("orders", "order_id", orders_df),
        ("order_items", "order_item_id", order_items_df),
    ]:
        dups = df[col].duplicated().sum()
        if dups == 0:
            report.passed_checks.append(f"Uniqueness: 0 duplicate {col} in {tbl_name}")
        else:
            report.is_valid = False
            report.failed_checks.append(f"Uniqueness: {dups} duplicate {col} in {tbl_name}")
            report.errors[f"{tbl_name}_dups"] = [f"Found {dups} duplicates"]

    # Summary Metrics
    report.summary_stats = {
        "customer_count": float(len(customers_df)),
        "product_count": float(len(products_df)),
        "order_count": float(len(orders_df)),
        "order_item_count": float(len(order_items_df)),
        "gross_sales_reconciled": float(orders_df["gross_amount"].sum()),
        "net_sales_reconciled": float(orders_df["net_amount"].sum()),
    }

    return report
