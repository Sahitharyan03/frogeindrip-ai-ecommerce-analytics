WITH source AS (
    SELECT * FROM raw_order_items
)
SELECT
    order_item_id,
    order_id,
    product_id,
    CAST(quantity AS INTEGER) AS quantity,
    ROUND(CAST(unit_price AS DOUBLE), 2) AS unit_price,
    ROUND(CAST(total_price AS DOUBLE), 2) AS total_price,
    ROUND(CAST(unit_cost AS DOUBLE), 2) AS unit_cost,
    ROUND(CAST(total_cost AS DOUBLE), 2) AS total_cost,
    ROUND(CAST(gross_margin AS DOUBLE), 2) AS gross_margin
FROM source
