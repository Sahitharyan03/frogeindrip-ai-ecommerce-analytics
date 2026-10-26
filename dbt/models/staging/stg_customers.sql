WITH source AS (
    SELECT * FROM raw_customers
)
SELECT
    customer_id,
    TRIM(first_name) AS first_name,
    TRIM(last_name) AS last_name,
    LOWER(TRIM(email)) AS email,
    CAST(created_at AS TIMESTAMP) AS registered_at,
    acquisition_channel,
    city,
    state,
    country
FROM source
