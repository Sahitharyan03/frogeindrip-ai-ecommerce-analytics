WITH base_rfm AS (
    SELECT
        customer_id,
        DATEDIFF('day', MAX(order_timestamp), DATE '2026-08-01') AS recency_days,
        COUNT(DISTINCT order_id) AS frequency,
        ROUND(SUM(net_amount), 2) AS monetary
    FROM {{ ref('stg_orders') }}
    WHERE status = 'completed'
    GROUP BY customer_id
),
scored_rfm AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        CASE
            WHEN frequency >= 3 THEN 5
            WHEN frequency = 2 THEN 4
            WHEN frequency = 1 THEN 2
            ELSE 1
        END AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM base_rfm
)
SELECT
    customer_id,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    CAST(r_score AS VARCHAR) || CAST(f_score AS VARCHAR) || CAST(m_score AS VARCHAR) AS rfm_code,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions / VIPs'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Recent New Customers'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At-Risk / High Potential'
        WHEN r_score <= 2 AND f_score <= 2 AND monetary >= 150 THEN 'At-Risk One-Time Big Spenders'
        ELSE 'Hibernating / Lost'
    END AS segment_label
FROM scored_rfm
