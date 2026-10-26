WITH source AS (
    SELECT * FROM raw_orders
)
SELECT
    order_id,
    customer_id,
    CAST(order_date AS TIMESTAMP) AS order_timestamp,
    CAST(order_date AS DATE) AS order_date,
    status,
    ROUND(CAST(gross_amount AS DOUBLE), 2) AS gross_amount,
    ROUND(CAST(discount_amount AS DOUBLE), 2) AS discount_amount,
    ROUND(CAST(net_amount AS DOUBLE), 2) AS net_amount,
    ROUND(CAST(tax_amount AS DOUBLE), 2) AS tax_amount,
    ROUND(CAST(shipping_amount AS DOUBLE), 2) AS shipping_amount,
    ROUND(CAST(total_amount AS DOUBLE), 2) AS total_amount,
    payment_method,
    channel
FROM source
