-- 06_repeat_purchase_rate.sql
-- Computes the overall brand repeat-purchase rate and order frequency breakdown

WITH order_counts AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS orders_count,
        SUM(net_amount) AS customer_net_spend
    FROM raw_orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
distribution AS (
    SELECT
        orders_count,
        COUNT(customer_id) AS customers_in_tier,
        SUM(customer_net_spend) AS tier_net_spend
    FROM order_counts
    GROUP BY orders_count
)
SELECT
    orders_count,
    customers_in_tier,
    ROUND((customers_in_tier * 100.0) / SUM(customers_in_tier) OVER (), 2) AS pct_of_customer_base,
    ROUND(tier_net_spend, 2) AS tier_net_spend,
    ROUND((tier_net_spend * 100.0) / SUM(tier_net_spend) OVER (), 2) AS pct_of_total_gmv,
    ROUND(tier_net_spend / NULLIF(customers_in_tier, 0), 2) AS avg_spend_per_customer
FROM distribution
ORDER BY orders_count ASC;
