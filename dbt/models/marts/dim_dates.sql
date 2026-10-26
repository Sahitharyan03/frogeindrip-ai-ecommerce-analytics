WITH date_range AS (
    SELECT UNNEST(generate_series(DATE '2025-07-01', DATE '2026-08-31', INTERVAL '1 day')) AS date_actual
)
SELECT
    date_actual AS date_id,
    EXTRACT(year FROM date_actual) AS year,
    EXTRACT(month FROM date_actual) AS month,
    strftime(date_actual, '%B') AS month_name,
    strftime(date_actual, '%Y-%m') AS year_month,
    EXTRACT(day FROM date_actual) AS day_of_month,
    strftime(date_actual, '%A') AS day_name,
    EXTRACT(isodow FROM date_actual) AS day_of_week,
    CASE WHEN EXTRACT(isodow FROM date_actual) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend,
    EXTRACT(quarter FROM date_actual) AS quarter
FROM date_range
