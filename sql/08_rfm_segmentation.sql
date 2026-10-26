-- 08_rfm_segmentation.sql
-- Computes customer-level Recency, Frequency, Monetary metrics, Quintile ranks, and Segment taxonomy

WITH customer_rfm_raw AS (
    SELECT
        customer_id,
        DATEDIFF('day', MAX(order_date), DATE '2026-08-01') AS recency_days,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(net_amount) AS monetary
    FROM raw_orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
rfm_ranked AS (
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
    FROM customer_rfm_raw
),
rfm_segments AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        ROUND(monetary, 2) AS monetary,
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
        END AS segment_name
    FROM rfm_ranked
)
SELECT
    segment_name,
    COUNT(customer_id) AS customer_count,
    ROUND((COUNT(customer_id) * 100.0) / SUM(COUNT(customer_id)) OVER (), 2) AS pct_of_customers,
    ROUND(SUM(monetary), 2) AS total_segment_revenue,
    ROUND((SUM(monetary) / SUM(SUM(monetary)) OVER ()) * 100, 2) AS pct_of_total_gmv,
    ROUND(AVG(monetary), 2) AS avg_monetary_spend,
    ROUND(AVG(frequency), 2) AS avg_order_frequency,
    ROUND(AVG(recency_days), 1) AS avg_recency_days
FROM rfm_segments
GROUP BY segment_name
ORDER BY total_segment_revenue DESC;
