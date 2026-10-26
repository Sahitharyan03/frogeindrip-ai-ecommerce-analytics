-- 01_gross_net_sales.sql
-- Computes overall gross sales, promotional discounts, returns, net sales, taxes, and shipping
-- Granularity: Overall reporting window and channel breakdown

WITH sales_reconciliation AS (
    SELECT
        channel,
        payment_method,
        status,
        COUNT(order_id) AS total_orders,
        SUM(gross_amount) AS total_gross_sales,
        SUM(discount_amount) AS total_discounts,
        SUM(net_amount) AS total_net_sales,
        SUM(tax_amount) AS total_tax,
        SUM(shipping_amount) AS total_shipping,
        SUM(total_amount) AS total_customer_paid
    FROM raw_orders
    GROUP BY channel, payment_method, status
)
SELECT
    channel,
    payment_method,
    status,
    total_orders,
    ROUND(total_gross_sales, 2) AS total_gross_sales,
    ROUND(total_discounts, 2) AS total_discounts,
    ROUND(total_net_sales, 2) AS total_net_sales,
    ROUND((total_discounts / NULLIF(total_gross_sales, 0)) * 100, 2) AS discount_rate_pct,
    ROUND(total_tax, 2) AS total_tax,
    ROUND(total_shipping, 2) AS total_shipping,
    ROUND(total_customer_paid, 2) AS total_customer_paid
FROM sales_reconciliation
ORDER BY total_net_sales DESC;
