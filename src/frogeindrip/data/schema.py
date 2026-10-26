"""Data validation schemas using Pandera for Frogeindrip Analytics Platform."""

try:
    import pandera.pandas as pa
    from pandera.pandas import Check, Column, DataFrameSchema
except ImportError:
    import pandera as pa
    from pandera import Check, Column, DataFrameSchema

# Customer Table Schema
CustomerSchema = DataFrameSchema(
    columns={
        "customer_id": Column(str, Check.str_startswith("CUST-"), nullable=False, unique=True),
        "first_name": Column(str, nullable=False),
        "last_name": Column(str, nullable=False),
        "email": Column(str, Check.str_matches(r"^[\w\.-]+@[\w\.-]+\.\w+$"), nullable=False),
        "created_at": Column(pa.DateTime, nullable=False),
        "acquisition_channel": Column(
            str,
            Check.isin(["Instagram", "TikTok", "Organic Search", "Referral", "Paid Social"]),
            nullable=False,
        ),
        "city": Column(str, nullable=False),
        "state": Column(str, Check.str_length(2, 2), nullable=False),
        "country": Column(str, Check.isin(["US", "CA"]), nullable=False),
    },
    strict=False,
    coerce=True,
)

# Product Table Schema
ProductSchema = DataFrameSchema(
    columns={
        "product_id": Column(str, Check.str_startswith("PROD-"), nullable=False, unique=True),
        "product_name": Column(str, nullable=False),
        "category": Column(
            str,
            Check.isin(["Hoodies & Sweats", "Tops & Tees", "Bottoms", "Outerwear", "Accessories"]),
            nullable=False,
        ),
        "cost_price": Column(float, Check.greater_than(0.0), nullable=False),
        "retail_price": Column(float, Check.greater_than(0.0), nullable=False),
        "margin_pct": Column(float, Check.in_range(0.0, 1.0), nullable=False),
        "is_active": Column(bool, nullable=False),
    },
    checks=[
        Check(
            lambda df: (df["retail_price"] >= df["cost_price"]).all(),
            error="retail_price must be greater than or equal to cost_price",
        )
    ],
    strict=False,
    coerce=True,
)

# Order Table Schema
OrderSchema = DataFrameSchema(
    columns={
        "order_id": Column(str, Check.str_startswith("ORD-"), nullable=False, unique=True),
        "customer_id": Column(str, Check.str_startswith("CUST-"), nullable=False),
        "order_date": Column(pa.DateTime, nullable=False),
        "status": Column(
            str,
            Check.isin(["completed", "refunded", "cancelled", "processing"]),
            nullable=False,
        ),
        "gross_amount": Column(float, Check.greater_than_or_equal_to(0.0), nullable=False),
        "discount_amount": Column(float, Check.greater_than_or_equal_to(0.0), nullable=False),
        "net_amount": Column(float, Check.greater_than_or_equal_to(0.0), nullable=False),
        "tax_amount": Column(float, Check.greater_than_or_equal_to(0.0), nullable=False),
        "shipping_amount": Column(float, Check.greater_than_or_equal_to(0.0), nullable=False),
        "total_amount": Column(float, Check.greater_than_or_equal_to(0.0), nullable=False),
        "payment_method": Column(
            str,
            Check.isin(["Square POS", "Square Online", "Apple Pay", "Credit Card", "Shop Pay"]),
            nullable=False,
        ),
        "channel": Column(str, Check.isin(["Online Store", "Pop-up / Event POS"]), nullable=False),
    },
    checks=[
        Check(
            lambda df: (abs(df["gross_amount"] - df["discount_amount"] - df["net_amount"]) < 0.05).all(),
            error="net_amount must equal gross_amount - discount_amount",
        )
    ],
    strict=False,
    coerce=True,
)

# Order Item Table Schema
OrderItemSchema = DataFrameSchema(
    columns={
        "order_item_id": Column(str, Check.str_startswith("ITEM-"), nullable=False, unique=True),
        "order_id": Column(str, Check.str_startswith("ORD-"), nullable=False),
        "product_id": Column(str, Check.str_startswith("PROD-"), nullable=False),
        "quantity": Column(int, Check.greater_than_or_equal_to(1), nullable=False),
        "unit_price": Column(float, Check.greater_than(0.0), nullable=False),
        "total_price": Column(float, Check.greater_than(0.0), nullable=False),
        "unit_cost": Column(float, Check.greater_than(0.0), nullable=False),
        "total_cost": Column(float, Check.greater_than(0.0), nullable=False),
        "gross_margin": Column(float, nullable=False),
    },
    checks=[
        Check(
            lambda df: (abs(df["quantity"] * df["unit_price"] - df["total_price"]) < 0.05).all(),
            error="total_price must equal quantity * unit_price",
        )
    ],
    strict=False,
    coerce=True,
)
