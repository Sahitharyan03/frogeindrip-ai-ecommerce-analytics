-- 03_aov_and_basket_size.sql
-- Computes Average Order Value (AOV), Average Units Per Order (UPT), and Average Item Price

WITH order_level AS (
    SELECT
        o.order_id,
        o.channel,
        o.payment_method,
        o.net_amount,
        SUM(oi.quantity) AS total_units,
        COUNT(oi.order_item_id) AS distinct_skus
    FROM raw_orders o
    JOIN raw_order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY o.order_id, o.channel, o.payment_method, o.net_amount
)
SELECT
    channel,
    payment_method,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(net_amount), 2) AS total_net_revenue,
    SUM(total_units) AS total_units_sold,
    ROUND(AVG(net_amount), 2) AS average_order_value_aov,
    ROUND(AVG(total_units), 2) AS units_per_transaction_upt,
    ROUND(AVG(distinct_skus), 2) AS avg_distinct_skus_per_order,
    ROUND(SUM(net_amount) / NULLIF(SUM(total_units), 0), 2) AS average_selling_price_asp
FROM order_level
GROUP BY channel, payment_method
ORDER BY total_net_revenue DESC;
