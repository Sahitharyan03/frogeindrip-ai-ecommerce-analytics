WITH customer_cohort AS (
    SELECT
        customer_id,
        strftime(MIN(order_timestamp), '%Y-%m') AS cohort_month
    FROM {{ ref('stg_orders') }}
    WHERE status = 'completed'
    GROUP BY customer_id
),
order_activities AS (
    SELECT
        o.customer_id,
        c.cohort_month,
        strftime(o.order_timestamp, '%Y-%m') AS order_month,
        (EXTRACT(year FROM o.order_timestamp) - EXTRACT(year FROM CAST(c.cohort_month || '-01' AS DATE))) * 12 +
        (EXTRACT(month FROM o.order_timestamp) - EXTRACT(month FROM CAST(c.cohort_month || '-01' AS DATE))) AS period_number,
        o.net_amount
    FROM {{ ref('stg_orders') }} o
    JOIN customer_cohort c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_cohort
    GROUP BY cohort_month
)
SELECT
    a.cohort_month,
    s.cohort_size,
    a.period_number,
    COUNT(DISTINCT a.customer_id) AS active_customers,
    ROUND((COUNT(DISTINCT a.customer_id) * 100.0) / s.cohort_size, 2) AS retention_rate_pct,
    ROUND(SUM(a.net_amount), 2) AS cohort_period_revenue
FROM order_activities a
JOIN cohort_sizes s ON a.cohort_month = s.cohort_month
GROUP BY a.cohort_month, s.cohort_size, a.period_number
ORDER BY a.cohort_month, a.period_number
