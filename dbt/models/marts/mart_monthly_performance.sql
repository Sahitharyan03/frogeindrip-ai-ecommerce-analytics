WITH monthly_orders AS (
    SELECT
        strftime(order_date, '%Y-%m') AS year_month,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS active_customers,
        ROUND(SUM(gross_amount), 2) AS total_gross_sales,
        ROUND(SUM(discount_amount), 2) AS total_discounts,
        ROUND(SUM(net_amount), 2) AS total_net_sales,
        ROUND(AVG(net_amount), 2) AS average_order_value
    FROM {{ ref('stg_orders') }}
    WHERE status = 'completed'
    GROUP BY 1
),
monthly_profit AS (
    SELECT
        strftime(order_timestamp, '%Y-%m') AS year_month,
        ROUND(SUM(item_cogs), 2) AS total_cogs,
        ROUND(SUM(item_gross_profit), 2) AS total_gross_profit
    FROM {{ ref('fct_sales') }}
    WHERE order_status = 'completed'
    GROUP BY 1
)
SELECT
    m.year_month,
    m.total_orders,
    m.active_customers,
    m.total_gross_sales,
    m.total_discounts,
    m.total_net_sales,
    m.average_order_value,
    p.total_cogs,
    p.total_gross_profit,
    ROUND((p.total_gross_profit / NULLIF(m.total_net_sales, 0)) * 100, 2) AS gross_margin_pct,
    ROUND(((m.total_net_sales - LAG(m.total_net_sales) OVER (ORDER BY m.year_month))
        / NULLIF(LAG(m.total_net_sales) OVER (ORDER BY m.year_month), 0)) * 100, 2) AS mom_growth_pct
FROM monthly_orders m
JOIN monthly_profit p ON m.year_month = p.year_month
ORDER BY m.year_month
