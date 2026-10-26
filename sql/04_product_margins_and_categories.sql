-- 04_product_margins_and_categories.sql
-- Evaluates product and category level revenue, COGS, gross margin, and share of total gross profit

WITH product_metrics AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.retail_price,
        p.cost_price,
        SUM(f.quantity) AS units_sold,
        SUM(f.item_gross_sales) AS gross_sales,
        SUM(f.item_allocated_discount) AS total_discounts,
        SUM(f.item_net_sales) AS net_sales,
        SUM(f.item_cogs) AS total_cogs,
        SUM(f.item_gross_profit) AS gross_profit
    FROM fct_sales f
    JOIN dim_products p ON f.product_id = p.product_id
    WHERE f.order_status = 'completed'
    GROUP BY p.product_id, p.product_name, p.category, p.retail_price, p.cost_price
)
SELECT
    product_id,
    product_name,
    category,
    retail_price,
    cost_price,
    units_sold,
    ROUND(net_sales, 2) AS net_sales,
    ROUND(total_cogs, 2) AS total_cogs,
    ROUND(gross_profit, 2) AS gross_profit,
    ROUND((gross_profit / NULLIF(net_sales, 0)) * 100, 2) AS realized_margin_pct,
    ROUND((gross_profit / SUM(gross_profit) OVER ()) * 100, 2) AS pct_share_of_total_brand_profit,
    DENSE_RANK() OVER (ORDER BY gross_profit DESC) AS profit_rank
FROM product_metrics
ORDER BY gross_profit DESC;
