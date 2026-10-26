-- 02_monthly_sales_and_mom.sql
-- Computes monthly sales, volume, and Month-over-Month (MoM) growth using LAG window function

WITH monthly_sales AS (
    SELECT
        strftime(order_date, '%Y-%m') AS year_month,
        COUNT(DISTINCT order_id) AS order_volume,
        COUNT(DISTINCT customer_id) AS active_buyers,
        SUM(gross_amount) AS gross_sales,
        SUM(discount_amount) AS discounts,
        SUM(net_amount) AS net_sales
    FROM raw_orders
    WHERE status = 'completed'
    GROUP BY strftime(order_date, '%Y-%m')
),
mom_calc AS (
    SELECT
        year_month,
        order_volume,
        active_buyers,
        ROUND(gross_sales, 2) AS gross_sales,
        ROUND(discounts, 2) AS discounts,
        ROUND(net_sales, 2) AS net_sales,
        ROUND(AVG(net_sales) OVER (), 2) AS overall_avg_monthly_net,
        LAG(net_sales, 1) OVER (ORDER BY year_month) AS prev_month_net_sales
    FROM monthly_sales
)
SELECT
    year_month,
    order_volume,
    active_buyers,
    gross_sales,
    discounts,
    net_sales,
    COALESCE(ROUND(prev_month_net_sales, 2), 0.0) AS prev_month_net_sales,
    ROUND(net_sales - prev_month_net_sales, 2) AS net_dollar_growth,
    ROUND(((net_sales - prev_month_net_sales) / NULLIF(prev_month_net_sales, 0)) * 100, 2) AS mom_growth_pct,
    ROUND((net_sales / overall_avg_monthly_net) * 100, 2) AS index_vs_avg_month
FROM mom_calc
ORDER BY year_month;
