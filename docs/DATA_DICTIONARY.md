# Data Dictionary & Entity Catalog
**Project:** Frogeindrip Analytics Platform  
**Storage Engine:** DuckDB (`frogeindrip.duckdb`) / PostgreSQL Compatible  

---

## 1. Raw / Staging Tables

### `raw_customers` / `stg_customers`
- **Grain:** One row per customer.
- **Fields:**
  - `customer_id` (VARCHAR, PK): Unique identifier prefixed with `CUST-`.
  - `first_name` (VARCHAR): Customer first name.
  - `last_name` (VARCHAR): Customer last name.
  - `email` (VARCHAR): Contact email address.
  - `created_at` / `registered_at` (TIMESTAMP): Account registration timestamp.
  - `acquisition_channel` (VARCHAR): Marketing origin (`Instagram`, `TikTok`, `Organic Search`, `Referral`, `Paid Social`).
  - `city` (VARCHAR): Customer billing/shipping city.
  - `state` (VARCHAR, 2-letter): State code.
  - `country` (VARCHAR, 2-letter): `US` or `CA`.

### `raw_products` / `stg_products`
- **Grain:** One row per catalog SKU.
- **Fields:**
  - `product_id` (VARCHAR, PK): Unique product identifier prefixed with `PROD-`.
  - `product_name` (VARCHAR): Full catalog apparel name.
  - `category` (VARCHAR): Category taxonomy (`Hoodies & Sweats`, `Tops & Tees`, `Bottoms`, `Outerwear`, `Accessories`).
  - `cost_price` (DOUBLE): Unit cost of goods sold (COGS).
  - `retail_price` (DOUBLE): MSRP retail selling price.
  - `margin_pct` (DOUBLE): Theoretical margin percentage `(retail - cost) / retail`.
  - `is_active` (BOOLEAN): Active catalog status flag.

### `raw_orders` / `stg_orders`
- **Grain:** One row per checkout order transaction.
- **Fields:**
  - `order_id` (VARCHAR, PK): Order identifier prefixed with `ORD-`.
  - `customer_id` (VARCHAR, FK): References `raw_customers.customer_id`.
  - `order_date` / `order_timestamp` (TIMESTAMP): Transaction date and time.
  - `status` (VARCHAR): Settlement state (`completed`, `refunded`, `cancelled`, `processing`).
  - `gross_amount` (DOUBLE): Total item price before discounts. Reconciles with sum of line items.
  - `discount_amount` (DOUBLE): Promotional price reduction.
  - `net_amount` (DOUBLE): `gross_amount - discount_amount`.
  - `tax_amount` (DOUBLE): Sales tax collected (~7.25%).
  - `shipping_amount` (DOUBLE): Customer shipping fee ($0 if net $\ge$ $90, else $8.00).
  - `total_amount` (DOUBLE): Total billed to customer card.
  - `payment_method` (VARCHAR): `Square Online`, `Square POS`, `Apple Pay`, `Credit Card`, `Shop Pay`.
  - `channel` (VARCHAR): `Online Store` vs `Pop-up / Event POS`.

### `raw_order_items` / `stg_order_items`
- **Grain:** One row per individual item purchased in an order.
- **Fields:**
  - `order_item_id` (VARCHAR, PK): Line item identifier prefixed with `ITEM-`.
  - `order_id` (VARCHAR, FK): References `raw_orders.order_id`.
  - `product_id` (VARCHAR, FK): References `raw_products.product_id`.
  - `quantity` (INTEGER): Units purchased ($\ge 1$).
  - `unit_price` (DOUBLE): Selling price per unit.
  - `total_price` (DOUBLE): `quantity * unit_price`.
  - `unit_cost` (DOUBLE): Unit COGS.
  - `total_cost` (DOUBLE): `quantity * unit_cost`.
  - `gross_margin` (DOUBLE): `total_price - total_cost`.

---

## 2. Dimensional Lakehouse Tables

### `dim_customers`
Enriched customer dimension with lifetime purchase totals, first and latest order dates, and repeat buyer boolean flag (`is_repeat_buyer`).

### `dim_products`
Product catalog dimension with pricing, category, and standard margins.

### `dim_dates`
Continuous calendar table (2025-07-01 to 2026-08-31) containing day of week, day name, month name, year_month, quarter, and weekend indicator.

### `fct_sales`
Core analytical fact table at line item grain with allocated order discounts, net sales, COGS, and realized gross profit.

---

## 3. Analytical Data Marts

### `mart_monthly_performance`
Executive monthly performance containing total orders, active customers, gross sales, discounts, net sales, AOV, COGS, gross profit, margin %, and Month-over-Month (MoM) growth %.

### `mart_rfm_segments`
Customer RFM scores (1–5 quintile rankings) and assigned customer segments (`Champions / VIPs`, `Loyal Customers`, `Recent New Customers`, `At-Risk / High Potential`, `At-Risk One-Time Big Spenders`, `Hibernating / Lost`).

### `mart_cohort_retention`
Monthly customer cohort retention matrix tracking active buyers, retention rates %, and periodic cohort revenue across elapsed months (Month 0 through Month 4+).
