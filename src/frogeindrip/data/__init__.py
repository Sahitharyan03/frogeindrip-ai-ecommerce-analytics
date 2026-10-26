"""Data generation and schema validation module."""

from frogeindrip.data.generator import generate_synthetic_data
from frogeindrip.data.schema import (
    CustomerSchema,
    OrderItemSchema,
    OrderSchema,
    ProductSchema,
)

__all__ = [
    "CustomerSchema",
    "OrderItemSchema",
    "OrderSchema",
    "ProductSchema",
    "generate_synthetic_data",
]
