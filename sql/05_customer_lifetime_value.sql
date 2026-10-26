-- 05_customer_lifetime_value.sql
-- Computes customer lifetime spend (LTV to date), acquisition channel distribution, and cumulative distribution

WITH customer_summary AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        c.acquisition_channel,
        c.city,
        c.state,
        c.registered_at,
        c.lifetime_orders,
        c.lifetime_net_spend,
        c.is_repeat_buyer
    FROM dim_customers c
    WHERE c.lifetime_orders > 0
),
ranked_customers AS (
    SELECT
        customer_id,
        customer_name,
        acquisition_channel,
        state,
        lifetime_orders,
        lifetime_net_spend,
        is_repeat_buyer,
        NTILE(10) OVER (ORDER BY lifetime_net_spend DESC) AS spend_decile,
        SUM(lifetime_net_spend) OVER (ORDER BY lifetime_net_spend DESC) AS running_cumulative_spend,
        SUM(lifetime_net_spend) OVER () AS total_platform_spend
    FROM customer_summary
)
SELECT
    customer_id,
    customer_name,
    acquisition_channel,
    state,
    lifetime_orders,
    ROUND(lifetime_net_spend, 2) AS lifetime_net_spend,
    is_repeat_buyer,
    spend_decile,
    ROUND(running_cumulative_spend, 2) AS running_cumulative_spend,
    ROUND((running_cumulative_spend / total_platform_spend) * 100, 2) AS cumulative_pct_of_gmv
FROM ranked_customers
ORDER BY lifetime_net_spend DESC
LIMIT 50;
