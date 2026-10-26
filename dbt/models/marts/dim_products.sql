SELECT
    product_id,
    product_name,
    category,
    cost_price,
    retail_price,
    margin_pct,
    is_active
FROM {{ ref('stg_products') }}
