WITH source AS (
    SELECT * FROM raw_products
)
SELECT
    product_id,
    TRIM(product_name) AS product_name,
    category,
    ROUND(CAST(cost_price AS DOUBLE), 2) AS cost_price,
    ROUND(CAST(retail_price AS DOUBLE), 2) AS retail_price,
    ROUND(CAST(margin_pct AS DOUBLE), 4) AS margin_pct,
    is_active
FROM source
