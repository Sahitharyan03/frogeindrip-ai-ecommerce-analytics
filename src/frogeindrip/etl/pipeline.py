"""End-to-end ETL and Data Mart Pipeline for Frogeindrip Analytics Platform."""

import logging
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from frogeindrip.config import DB_PATH, DEFAULT_RANDOM_SEED, SYNTHETIC_DATA_DIR
from frogeindrip.data.generator import generate_synthetic_data
from frogeindrip.etl.validators import validate_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class FrogeindripETL:
    """Manages ingestion, schema validation, DuckDB loading, and analytics mart creation."""

    def __init__(self, db_path: Path | None = None, seed: int = DEFAULT_RANDOM_SEED):
        self.db_path = db_path or DB_PATH
        self.seed = seed
        self.conn: duckdb.DuckDBPyConnection | None = None

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        if self.conn is None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = duckdb.connect(str(self.db_path))
        return self.conn

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def load_or_generate_raw_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load raw CSV files if present, else generate fresh deterministic synthetic data."""
        cust_path = SYNTHETIC_DATA_DIR / "customers.csv"
        prod_path = SYNTHETIC_DATA_DIR / "products.csv"
        ord_path = SYNTHETIC_DATA_DIR / "orders.csv"
        item_path = SYNTHETIC_DATA_DIR / "order_items.csv"

        if cust_path.exists() and prod_path.exists() and ord_path.exists() and item_path.exists():
            logger.info("Loading existing synthetic CSV datasets from %s", SYNTHETIC_DATA_DIR)
            customers_df = pd.read_csv(cust_path, parse_dates=["created_at"])
            products_df = pd.read_csv(prod_path)
            orders_df = pd.read_csv(ord_path, parse_dates=["order_date"])
            order_items_df = pd.read_csv(item_path)
        else:
            logger.info("Generating deterministic synthetic data (seed=%d)...", self.seed)
            customers_df, products_df, orders_df, order_items_df = generate_synthetic_data(
                seed=self.seed, save_csv=True
            )

        # Type normalization
        orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
        customers_df["created_at"] = pd.to_datetime(customers_df["created_at"])

        return customers_df, products_df, orders_df, order_items_df

    def run(self) -> dict[str, Any]:
        """Execute full ETL lifecycle: Ingestion -> Validation -> DuckDB Storage -> Data Marts."""
        logger.info("Starting Frogeindrip ETL pipeline execution...")
        customers_df, products_df, orders_df, order_items_df = self.load_or_generate_raw_data()

        # Step 1: Automated Validation & Quality Assertions
        logger.info("Running automated schema and integrity validations...")
        validation_report = validate_dataset(customers_df, products_df, orders_df, order_items_df)

        if not validation_report.is_valid:
            logger.error("Validation errors encountered: %s", validation_report.errors)
            raise ValueError(f"ETL Aborted: Dataset validation failed: {validation_report.errors}")

        logger.info("All validation checks passed successfully (%d checks).", len(validation_report.passed_checks))

        # Step 2: Ingest into DuckDB Staging
        conn = self.get_connection()

        conn.register("df_customers", customers_df)
        conn.register("df_products", products_df)
        conn.register("df_orders", orders_df)
        conn.register("df_order_items", order_items_df)

        conn.execute("CREATE OR REPLACE TABLE raw_customers AS SELECT * FROM df_customers")
        conn.execute("CREATE OR REPLACE TABLE raw_products AS SELECT * FROM df_products")
        conn.execute("CREATE OR REPLACE TABLE raw_orders AS SELECT * FROM df_orders")
        conn.execute("CREATE OR REPLACE TABLE raw_order_items AS SELECT * FROM df_order_items")

        # Step 3: Build Dimension & Fact Tables (Star Schema)
        logger.info("Building Star-Schema Dimensions and Facts in DuckDB...")

        # 3a. dim_dates
        conn.execute("""
            CREATE OR REPLACE TABLE dim_dates AS
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
            FROM date_range;
        """)

        # 3b. dim_customers
        conn.execute("""
            CREATE OR REPLACE TABLE dim_customers AS
            WITH first_orders AS (
                SELECT
                    customer_id,
                    MIN(order_date) AS first_order_date,
                    MAX(order_date) AS latest_order_date,
                    COUNT(DISTINCT order_id) AS lifetime_orders,
                    SUM(net_amount) AS lifetime_net_spend
                FROM raw_orders
                WHERE status = 'completed'
                GROUP BY customer_id
            )
            SELECT
                c.customer_id,
                c.first_name,
                c.last_name,
                c.email,
                c.created_at AS registered_at,
                c.acquisition_channel,
                c.city,
                c.state,
                c.country,
                fo.first_order_date,
                fo.latest_order_date,
                COALESCE(fo.lifetime_orders, 0) AS lifetime_orders,
                ROUND(COALESCE(fo.lifetime_net_spend, 0.0), 2) AS lifetime_net_spend,
                CASE
                    WHEN COALESCE(fo.lifetime_orders, 0) > 1 THEN TRUE
                    ELSE FALSE
                END AS is_repeat_buyer
            FROM raw_customers c
            LEFT JOIN first_orders fo ON c.customer_id = fo.customer_id;
        """)

        # 3c. dim_products
        conn.execute("""
            CREATE OR REPLACE TABLE dim_products AS
            SELECT
                product_id,
                product_name,
                category,
                ROUND(cost_price, 2) AS cost_price,
                ROUND(retail_price, 2) AS retail_price,
                ROUND(margin_pct, 4) AS margin_pct,
                is_active
            FROM raw_products;
        """)

        # 3d. fct_sales (Order item grain with full attribution & margin reconciliation)
        conn.execute("""
            CREATE OR REPLACE TABLE fct_sales AS
            SELECT
                oi.order_item_id,
                o.order_id,
                o.customer_id,
                CAST(o.order_date AS DATE) AS date_id,
                o.order_date,
                o.status AS order_status,
                o.channel,
                o.payment_method,
                oi.product_id,
                p.category AS product_category,
                oi.quantity,
                oi.unit_price,
                oi.total_price AS item_gross_sales,
                -- Allocated discount per line item proportional to gross
                ROUND(CASE
                    WHEN o.gross_amount > 0 THEN (oi.total_price / o.gross_amount) * o.discount_amount
                    ELSE 0.0
                END, 2) AS item_allocated_discount,
                ROUND(oi.total_price - CASE
                    WHEN o.gross_amount > 0 THEN (oi.total_price / o.gross_amount) * o.discount_amount
                    ELSE 0.0
                END, 2) AS item_net_sales,
                oi.total_cost AS item_cogs,
                ROUND((oi.total_price - CASE
                    WHEN o.gross_amount > 0 THEN (oi.total_price / o.gross_amount) * o.discount_amount
                    ELSE 0.0
                END) - oi.total_cost, 2) AS item_gross_profit
            FROM raw_order_items oi
            JOIN raw_orders o ON oi.order_id = o.order_id
            JOIN raw_products p ON oi.product_id = p.product_id;
        """)

        # Step 4: Analytical Data Marts

        # 4a. Monthly Performance Mart
        conn.execute("""
            CREATE OR REPLACE TABLE mart_monthly_performance AS
            WITH monthly_agg AS (
                SELECT
                    strftime(order_date, '%Y-%m') AS year_month,
                    COUNT(DISTINCT order_id) AS total_orders,
                    COUNT(DISTINCT customer_id) AS active_customers,
                    ROUND(SUM(gross_amount), 2) AS total_gross_sales,
                    ROUND(SUM(discount_amount), 2) AS total_discounts,
                    ROUND(SUM(net_amount), 2) AS total_net_sales,
                    ROUND(AVG(net_amount), 2) AS average_order_value
                FROM raw_orders
                WHERE status = 'completed'
                GROUP BY 1
            ),
            monthly_profit AS (
                SELECT
                    strftime(order_date, '%Y-%m') AS year_month,
                    ROUND(SUM(item_cogs), 2) AS total_cogs,
                    ROUND(SUM(item_gross_profit), 2) AS total_gross_profit
                FROM fct_sales
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
            FROM monthly_agg m
            JOIN monthly_profit p ON m.year_month = p.year_month
            ORDER BY m.year_month;
        """)

        # 4b. RFM Segments Mart
        # Reference date set to 2026-08-01 (end of active launch observation window)
        conn.execute("""
            CREATE OR REPLACE TABLE mart_rfm_segments AS
            WITH base_rfm AS (
                SELECT
                    customer_id,
                    DATEDIFF('day', MAX(order_date), DATE '2026-08-01') AS recency_days,
                    COUNT(DISTINCT order_id) AS frequency,
                    ROUND(SUM(net_amount), 2) AS monetary
                FROM raw_orders
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
            FROM scored_rfm;
        """)

        # 4c. Cohort Retention Mart
        conn.execute("""
            CREATE OR REPLACE TABLE mart_cohort_retention AS
            WITH customer_cohort AS (
                SELECT
                    customer_id,
                    strftime(MIN(order_date), '%Y-%m') AS cohort_month
                FROM raw_orders
                WHERE status = 'completed'
                GROUP BY customer_id
            ),
            order_activities AS (
                SELECT
                    o.customer_id,
                    c.cohort_month,
                    strftime(o.order_date, '%Y-%m') AS order_month,
                    (EXTRACT(year FROM o.order_date) - EXTRACT(year FROM CAST(c.cohort_month || '-01' AS DATE))) * 12 +
                    (EXTRACT(month FROM o.order_date) - EXTRACT(month FROM CAST(c.cohort_month || '-01' AS DATE))) AS period_number,
                    o.net_amount
                FROM raw_orders o
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
            ORDER BY a.cohort_month, a.period_number;
        """)

        # Compile pipeline results
        res_summary = {
            "status": "SUCCESS",
            "validation": validation_report,
            "database_tables": [row[0] for row in conn.execute("SHOW TABLES").fetchall()],
            "total_orders": conn.execute("SELECT COUNT(*) FROM raw_orders WHERE status = 'completed'").fetchone()[0],
            "total_net_sales": conn.execute("SELECT ROUND(SUM(net_amount), 2) FROM raw_orders WHERE status = 'completed'").fetchone()[0],
            "repeat_buyer_count": conn.execute("SELECT COUNT(*) FROM dim_customers WHERE is_repeat_buyer = TRUE").fetchone()[0],
            "repeat_buyer_revenue": conn.execute("""
                SELECT ROUND(SUM(net_amount), 2)
                FROM raw_orders
                WHERE customer_id IN (SELECT customer_id FROM dim_customers WHERE is_repeat_buyer = TRUE)
                AND status = 'completed'
            """).fetchone()[0],
        }

        logger.info(
            "ETL Pipeline execution completed successfully. Database populated at %s", self.db_path
        )
        return res_summary


def run_pipeline() -> dict[str, Any]:
    """Convenience entry point for running the pipeline."""
    etl = FrogeindripETL()
    try:
        return etl.run()
    finally:
        etl.close()


if __name__ == "__main__":
    result = run_pipeline()
    print("ETL Result Summary:")
    for k, v in result.items():
        if k != "validation":
            print(f"  {k}: {v}")
