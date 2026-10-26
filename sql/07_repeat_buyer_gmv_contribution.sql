-- 07_repeat_buyer_gmv_contribution.sql
-- Rigorous calculation of Repeat Buyer GMV Contribution comparing:
--   Method A: Lifetime Repeat Buyer Classification (Total GMV of all customers who ever placed >=2 orders)
--   Method B: Point-in-Time Sequence Classification (Orders where customer_order_sequence >= 2 at transaction time; NO forward leakage)

WITH sequenced_orders AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        net_amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date ASC) AS customer_order_seq,
        COUNT(order_id) OVER (PARTITION BY customer_id) AS customer_lifetime_orders
    FROM raw_orders
    WHERE status = 'completed'
),
summary_metrics AS (
    SELECT
        COUNT(DISTINCT order_id) AS total_completed_orders,
        COUNT(DISTINCT customer_id) AS total_unique_buyers,
        SUM(net_amount) AS total_completed_gmv,

        -- Method A: Lifetime definition (Customer ever placed >=2 orders)
        SUM(CASE WHEN customer_lifetime_orders >= 2 THEN net_amount ELSE 0.0 END) AS gmv_method_a_lifetime,
        COUNT(DISTINCT CASE WHEN customer_lifetime_orders >= 2 THEN customer_id END) AS customers_method_a,

        -- Method B: Point-in-Time definition (No lookahead leakage: strictly order 2, 3, etc.)
        SUM(CASE WHEN customer_order_seq >= 2 THEN net_amount ELSE 0.0 END) AS gmv_method_b_point_in_time,
        COUNT(DISTINCT CASE WHEN customer_order_seq >= 2 THEN order_id END) AS orders_method_b
    FROM sequenced_orders
)
SELECT
    total_completed_orders,
    total_unique_buyers,
    ROUND(total_completed_gmv, 2) AS total_completed_gmv,

    -- Method A Results
    ROUND(gmv_method_a_lifetime, 2) AS method_a_lifetime_repeat_gmv,
    ROUND((gmv_method_a_lifetime / total_completed_gmv) * 100, 2) AS method_a_repeat_gmv_pct,
    customers_method_a AS method_a_repeat_customer_count,
    ROUND((customers_method_a * 100.0) / total_unique_buyers, 2) AS method_a_repeat_customer_pct,

    -- Method B Results
    ROUND(gmv_method_b_point_in_time, 2) AS method_b_point_in_time_repeat_gmv,
    ROUND((gmv_method_b_point_in_time / total_completed_gmv) * 100, 2) AS method_b_repeat_gmv_pct,
    orders_method_b AS method_b_repeat_order_count,
    ROUND((orders_method_b * 100.0) / total_completed_orders, 2) AS method_b_repeat_order_pct
FROM summary_metrics;
