WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),
products AS (
    SELECT * FROM {{ ref('stg_products') }}
)
SELECT
    i.order_item_id,
    o.order_id,
    o.customer_id,
    o.order_date AS date_id,
    o.order_timestamp,
    o.status AS order_status,
    o.channel,
    o.payment_method,
    i.product_id,
    p.category AS product_category,
    i.quantity,
    i.unit_price,
    i.total_price AS item_gross_sales,
    ROUND(CASE
        WHEN o.gross_amount > 0 THEN (i.total_price / o.gross_amount) * o.discount_amount
        ELSE 0.0
    END, 2) AS item_allocated_discount,
    ROUND(i.total_price - CASE
        WHEN o.gross_amount > 0 THEN (i.total_price / o.gross_amount) * o.discount_amount
        ELSE 0.0
    END, 2) AS item_net_sales,
    i.total_cost AS item_cogs,
    ROUND((i.total_price - CASE
        WHEN o.gross_amount > 0 THEN (i.total_price / o.gross_amount) * o.discount_amount
        ELSE 0.0
    END) - i.total_cost, 2) AS item_gross_profit
FROM items i
JOIN orders o ON i.order_id = o.order_id
JOIN products p ON i.product_id = p.product_id
