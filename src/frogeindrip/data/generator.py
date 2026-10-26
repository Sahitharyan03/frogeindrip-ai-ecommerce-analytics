"""Deterministic synthetic data generator for Frogeindrip DTC apparel analytics."""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from frogeindrip.config import DEFAULT_RANDOM_SEED, SYNTHETIC_DATA_DIR


def generate_synthetic_data(
    seed: int = DEFAULT_RANDOM_SEED,
    num_customers: int = 450,
    save_csv: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generate deterministic, relational synthetic ecommerce data for Frogeindrip.

    Returns:
        Tuple of (customers_df, products_df, orders_df, order_items_df)
    """
    random.seed(seed)
    np.random.seed(seed)

    # 1. Products Definition (Realistic DTC Streetwear Catalog)
    products_catalog = [
        ("PROD-001", "Froge Heavyweight Boxy Hoodie - Forest", "Hoodies & Sweats", 32.00, 88.00),
        ("PROD-002", "Froge Heavyweight Boxy Hoodie - Onyx", "Hoodies & Sweats", 32.00, 88.00),
        ("PROD-003", "Froge Heavyweight Boxy Hoodie - Vintage Grey", "Hoodies & Sweats", 32.00, 88.00),
        ("PROD-004", "Froge Oversized Acid Wash Tee - Mineral", "Tops & Tees", 11.50, 42.00),
        ("PROD-005", "Froge Oversized Acid Wash Tee - Washed Black", "Tops & Tees", 11.50, 42.00),
        ("PROD-006", "Froge Classic Logo Drop Tee - White", "Tops & Tees", 9.00, 36.00),
        ("PROD-007", "Froge Tactical Cargo Pants - Olive", "Bottoms", 28.00, 95.00),
        ("PROD-008", "Froge Tactical Cargo Pants - Black", "Bottoms", 28.00, 95.00),
        ("PROD-009", "Froge Heavyweight Fleece Sweatpants - Heather", "Bottoms", 22.00, 75.00),
        ("PROD-010", "Froge Ripstop Windbreaker Coach Jacket", "Outerwear", 38.00, 115.00),
        ("PROD-011", "Froge Quilted Puffer Vest - Cypress", "Outerwear", 36.00, 105.00),
        ("PROD-012", "Froge Embroidered Ribbed Beanie - Hunter Green", "Accessories", 6.50, 28.00),
        ("PROD-013", "Froge Embroidered Ribbed Beanie - Black", "Accessories", 6.50, 28.00),
        ("PROD-014", "Froge Corduroy 6-Panel Snapback", "Accessories", 8.00, 34.00),
        ("PROD-015", "Froge Jacquard Heavy Sock 3-Pack", "Accessories", 5.00, 22.00),
        ("PROD-016", "Froge Canvas Heavy Tote Bag", "Accessories", 7.00, 26.00),
    ]

    products_data = []
    for pid, name, cat, cost, retail in products_catalog:
        margin = round((retail - cost) / retail, 4)
        products_data.append(
            {
                "product_id": pid,
                "product_name": name,
                "category": cat,
                "cost_price": cost,
                "retail_price": retail,
                "margin_pct": margin,
                "is_active": True,
            }
        )
    products_df = pd.DataFrame(products_data)

    # 2. Customers Generation
    first_names = [
        "Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley", "Casey", "Avery",
        "Jesse", "Logan", "Jamie", "Dakota", "Reese", "Cameron", "Hayden", "Skyler", "Rowan", "Peyton",
        "Kai", "River", "Emerson", "Kendall", "Finley", "Harley", "Eden", "Elliott", "Milan", "Sage"
    ]
    last_names = [
        "Chen", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
        "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
    ]
    cities_states = [
        ("New York", "NY"), ("Brooklyn", "NY"), ("Los Angeles", "CA"), ("San Francisco", "CA"),
        ("Chicago", "IL"), ("Austin", "TX"), ("Seattle", "WA"), ("Atlanta", "GA"),
        ("Miami", "FL"), ("Denver", "CO"), ("Portland", "OR"), ("Boston", "MA"),
        ("Toronto", "ON"), ("Philadelphia", "PA"), ("Dallas", "TX"), ("San Diego", "CA")
    ]
    channels = ["Instagram", "TikTok", "Organic Search", "Referral", "Paid Social"]
    channel_weights = [0.40, 0.25, 0.15, 0.10, 0.10]

    customers_data = []
    base_start = datetime(2025, 9, 1, 10, 0, 0)
    total_days = (datetime(2026, 7, 31) - datetime(2025, 9, 1)).days

    for i in range(1, num_customers + 1):
        cid = f"CUST-{i:04d}"
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        email = f"{fn.lower()}.{ln.lower()}{i}@example.com"
        # Customer creation spread over the active period
        days_offset = int(np.random.beta(a=2.0, b=2.2) * total_days)
        cust_created = base_start + timedelta(days=days_offset, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        city, state = random.choice(cities_states)
        country = "CA" if state == "ON" else "US"
        channel = random.choices(channels, weights=channel_weights, k=1)[0]

        customers_data.append(
            {
                "customer_id": cid,
                "first_name": fn,
                "last_name": ln,
                "email": email,
                "created_at": cust_created,
                "acquisition_channel": channel,
                "city": city,
                "state": state,
                "country": country,
            }
        )
    customers_df = pd.DataFrame(customers_data).sort_values("created_at").reset_index(drop=True)

    # 3. Orders & Order Items Generation
    # Simulate realistic DTC drop dynamics (capsule drops, spring peak May 2026, clearance July 2026)
    orders_data = []
    order_items_data = []
    order_counter = 10001
    item_counter = 50001

    payment_methods = ["Square Online", "Square POS", "Apple Pay", "Credit Card", "Shop Pay"]
    pm_weights = [0.45, 0.15, 0.25, 0.10, 0.05]

    for _, cust in customers_df.iterrows():
        cid = cust["customer_id"]
        c_time = cust["created_at"]

        # Determine number of purchases for this customer (modeled repeat dynamics)
        # ~68% 1 order, ~22% 2 orders, ~8% 3 orders, ~2% 4+ orders
        order_count_prob = random.random()
        if order_count_prob < 0.68:
            n_orders = 1
        elif order_count_prob < 0.90:
            n_orders = 2
        elif order_count_prob < 0.98:
            n_orders = 3
        else:
            n_orders = 4

        current_order_date = c_time + timedelta(minutes=random.randint(5, 120))

        for o_idx in range(n_orders):
            if current_order_date > datetime(2026, 7, 31, 23, 59, 59):
                break

            oid = f"ORD-{order_counter}"
            order_counter += 1

            # Order channel & payment method
            channel = "Pop-up / Event POS" if random.random() < 0.15 else "Online Store"
            pm = "Square POS" if channel == "Pop-up / Event POS" else random.choices(payment_methods, weights=pm_weights, k=1)[0]

            # Basket generation: 1 to 4 distinct items
            basket_size = random.choices([1, 2, 3, 4], weights=[0.55, 0.30, 0.10, 0.05], k=1)[0]
            sampled_products = products_df.sample(n=basket_size, replace=False)

            order_gross = 0.0
            order_cost = 0.0

            for _, prod in sampled_products.iterrows():
                item_id = f"ITEM-{item_counter}"
                item_counter += 1

                qty = random.choices([1, 2, 3], weights=[0.85, 0.12, 0.03], k=1)[0]
                unit_price = float(prod["retail_price"])
                unit_cost = float(prod["cost_price"])
                total_price = round(qty * unit_price, 2)
                total_cost = round(qty * unit_cost, 2)
                margin = round(total_price - total_cost, 2)

                order_gross += total_price
                order_cost += total_cost

                order_items_data.append(
                    {
                        "order_item_id": item_id,
                        "order_id": oid,
                        "product_id": prod["product_id"],
                        "quantity": qty,
                        "unit_price": unit_price,
                        "total_price": total_price,
                        "unit_cost": unit_cost,
                        "total_cost": total_cost,
                        "gross_margin": margin,
                    }
                )

            order_gross = round(order_gross, 2)
            # Discounts: 20% of orders get a 10% promo discount
            if random.random() < 0.20:
                discount_amount = round(order_gross * 0.10, 2)
            else:
                discount_amount = 0.00

            net_amount = round(order_gross - discount_amount, 2)
            # Tax ~7.25%
            tax_amount = round(net_amount * 0.0725, 2)
            # Shipping: Free shipping over $90, else $8.00 flat
            shipping_amount = 0.00 if net_amount >= 90.00 else 8.00
            total_amount = round(net_amount + tax_amount + shipping_amount, 2)

            # Order Status: 95% completed, 3% refunded, 2% cancelled
            status_rand = random.random()
            if status_rand < 0.95:
                status = "completed"
            elif status_rand < 0.98:
                status = "refunded"
            else:
                status = "cancelled"

            orders_data.append(
                {
                    "order_id": oid,
                    "customer_id": cid,
                    "order_date": current_order_date,
                    "status": status,
                    "gross_amount": order_gross,
                    "discount_amount": discount_amount,
                    "net_amount": net_amount,
                    "tax_amount": tax_amount,
                    "shipping_amount": shipping_amount,
                    "total_amount": total_amount,
                    "payment_method": pm,
                    "channel": channel,
                }
            )

            # Interval to next repeat order (typically 25 to 80 days later)
            gap_days = random.randint(25, 80)
            current_order_date = current_order_date + timedelta(days=gap_days, hours=random.randint(-4, 4))

    orders_df = pd.DataFrame(orders_data).sort_values("order_date").reset_index(drop=True)
    order_items_df = pd.DataFrame(order_items_data)

    if save_csv:
        SYNTHETIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
        customers_df.to_csv(SYNTHETIC_DATA_DIR / "customers.csv", index=False)
        products_df.to_csv(SYNTHETIC_DATA_DIR / "products.csv", index=False)
        orders_df.to_csv(SYNTHETIC_DATA_DIR / "orders.csv", index=False)
        order_items_df.to_csv(SYNTHETIC_DATA_DIR / "order_items.csv", index=False)

    return customers_df, products_df, orders_df, order_items_df


if __name__ == "__main__":
    c_df, p_df, o_df, oi_df = generate_synthetic_data()
    print(f"Generated {len(c_df)} customers, {len(p_df)} products, {len(o_df)} orders, {len(oi_df)} order items.")
    print(f"Total Gross Sales: ${o_df['gross_amount'].sum():,.2f}")
    print(f"Total Net Sales: ${o_df['net_amount'].sum():,.2f}")
