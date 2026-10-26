WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),
completed_orders AS (
    SELECT
        customer_id,
        MIN(order_timestamp) AS first_order_date,
        MAX(order_timestamp) AS latest_order_date,
        COUNT(DISTINCT order_id) AS lifetime_orders,
        SUM(net_amount) AS lifetime_net_spend
    FROM {{ ref('stg_orders') }}
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.registered_at,
    c.acquisition_channel,
    c.city,
    c.state,
    c.country,
    co.first_order_date,
    co.latest_order_date,
    COALESCE(co.lifetime_orders, 0) AS lifetime_orders,
    ROUND(COALESCE(co.lifetime_net_spend, 0.0), 2) AS lifetime_net_spend,
    CASE
        WHEN COALESCE(co.lifetime_orders, 0) > 1 THEN TRUE
        ELSE FALSE
    END AS is_repeat_buyer
FROM customers c
LEFT JOIN completed_orders co ON c.customer_id = co.customer_id
