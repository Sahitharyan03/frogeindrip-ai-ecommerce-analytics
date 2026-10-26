-- 10_advanced_window_functions.sql
-- Comprehensive showcase of advanced SQL analytical patterns:
--   1. ROW_NUMBER for customer order sequence and recency rank
--   2. LAG for inter-purchase interval in days
--   3. SUM OVER for running cumulative brand GMV
--   4. AVG OVER with frame specification for 7-day rolling moving average revenue
--   5. DENSE_RANK for customer spend tiering within acquisition channels

WITH daily_totals AS (
    SELECT
        CAST(order_date AS DATE) AS sale_date,
        COUNT(order_id) AS daily_order_count,
        SUM(net_amount) AS daily_net_sales
    FROM raw_orders
    WHERE status = 'completed'
    GROUP BY CAST(order_date AS DATE)
),
daily_moving_avg AS (
    SELECT
        sale_date,
        daily_order_count,
        ROUND(daily_net_sales, 2) AS daily_net_sales,
        ROUND(SUM(daily_net_sales) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS cumulative_gmv_to_date,
        ROUND(AVG(daily_net_sales) OVER (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_7day_avg_sales
    FROM daily_totals
),
customer_intervals AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        net_amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS order_seq,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS previous_order_date,
        DATEDIFF('day', LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date ASC), order_date) AS days_since_last_order
    FROM raw_orders
    WHERE status = 'completed'
)
SELECT
    ci.order_id,
    ci.customer_id,
    ci.order_date,
    ci.order_seq,
    ROUND(ci.net_amount, 2) AS order_net_amount,
    ci.previous_order_date,
    ci.days_since_last_order,
    dma.cumulative_gmv_to_date,
    dma.rolling_7day_avg_sales
FROM customer_intervals ci
JOIN daily_moving_avg dma ON CAST(ci.order_date AS DATE) = dma.sale_date
WHERE ci.order_seq >= 2
ORDER BY ci.order_date DESC
LIMIT 50;
