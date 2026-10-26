-- 09_cohort_retention_matrix.sql
-- Generates a multi-month customer cohort retention matrix (Month 0 through Month 6+)

WITH customer_first_order AS (
    SELECT
        customer_id,
        strftime(MIN(order_date), '%Y-%m') AS cohort_month
    FROM raw_orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
cohort_size AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS total_cohort_size
    FROM customer_first_order
    GROUP BY cohort_month
),
monthly_activity AS (
    SELECT
        o.customer_id,
        c.cohort_month,
        (EXTRACT(year FROM o.order_date) - EXTRACT(year FROM CAST(c.cohort_month || '-01' AS DATE))) * 12 +
        (EXTRACT(month FROM o.order_date) - EXTRACT(month FROM CAST(c.cohort_month || '-01' AS DATE))) AS month_number,
        o.net_amount
    FROM raw_orders o
    JOIN customer_first_order c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
)
SELECT
    a.cohort_month,
    s.total_cohort_size,
    a.month_number,
    COUNT(DISTINCT a.customer_id) AS active_retained_customers,
    ROUND((COUNT(DISTINCT a.customer_id) * 100.0) / s.total_cohort_size, 2) AS retention_rate_pct,
    ROUND(SUM(a.net_amount), 2) AS period_net_spend
FROM monthly_activity a
JOIN cohort_size s ON a.cohort_month = s.cohort_month
GROUP BY a.cohort_month, s.total_cohort_size, a.month_number
ORDER BY a.cohort_month, a.month_number;
