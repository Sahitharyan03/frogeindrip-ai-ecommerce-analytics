"""Time-series sales forecasting and baseline comparison module."""

from dataclasses import dataclass

import duckdb
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from frogeindrip.config import DB_PATH, DEFAULT_RANDOM_SEED


@dataclass
class ForecastResult:
    train_days: int
    test_days: int
    split_date: str
    naive_mae: float
    naive_rmse: float
    naive_wape: float
    ml_mae: float
    ml_rmse: float
    ml_wape: float
    comparison_table: pd.DataFrame
    forecast_df: pd.DataFrame


def run_sales_forecast(
    split_date: str = "2026-06-01",
    seed: int = DEFAULT_RANDOM_SEED,
    conn: duckdb.DuckDBPyConnection | None = None,
) -> ForecastResult:
    """Run daily revenue forecasting with lag features and compare against naive baselines."""
    close_conn = False
    if conn is None:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        close_conn = True

    try:
        # Extract daily continuous sales series
        daily_query = """
            WITH date_spine AS (
                SELECT UNNEST(generate_series(DATE '2025-09-01', DATE '2026-07-31', INTERVAL '1 day')) AS sale_date
            ),
            actual_sales AS (
                SELECT
                    CAST(order_date AS DATE) AS sale_date,
                    COUNT(order_id) AS order_count,
                    SUM(net_amount) AS net_sales
                FROM raw_orders
                WHERE status = 'completed'
                GROUP BY 1
            )
            SELECT
                d.sale_date,
                COALESCE(s.order_count, 0) AS order_count,
                ROUND(COALESCE(s.net_sales, 0.0), 2) AS net_sales
            FROM date_spine d
            LEFT JOIN actual_sales s ON d.sale_date = s.sale_date
            ORDER BY d.sale_date ASC;
        """
        df = conn.execute(daily_query).fetchdf()
        df["sale_date"] = pd.to_datetime(df["sale_date"])

        # Feature Engineering: Lags and calendar features
        df["day_of_week"] = df["sale_date"].dt.day_of_week
        df["day_of_month"] = df["sale_date"].dt.day
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

        # Lags
        df["lag_1"] = df["net_sales"].shift(1)
        df["lag_7"] = df["net_sales"].shift(7)
        df["lag_14"] = df["net_sales"].shift(14)
        df["rolling_mean_7"] = df["net_sales"].shift(1).rolling(7).mean()
        df["rolling_mean_14"] = df["net_sales"].shift(1).rolling(14).mean()

        # Drop warm-up null rows
        clean_df = df.dropna().copy().reset_index(drop=True)

        # Time-based Train / Test Split
        split_ts = pd.to_datetime(split_date)
        train_df = clean_df[clean_df["sale_date"] < split_ts].copy()
        test_df = clean_df[clean_df["sale_date"] >= split_ts].copy()

        features = ["day_of_week", "day_of_month", "is_weekend", "lag_1", "lag_7", "lag_14", "rolling_mean_7", "rolling_mean_14"]
        X_train = train_df[features]
        y_train = train_df["net_sales"]
        X_test = test_df[features]
        y_test = test_df["net_sales"]

        # Baseline: Naive 7-day lag (predict what happened 7 days ago)
        y_naive = test_df["lag_7"]

        naive_mae = mean_absolute_error(y_test, y_naive)
        naive_rmse = np.sqrt(mean_squared_error(y_test, y_naive))
        naive_wape = (np.sum(np.abs(y_test - y_naive)) / np.sum(y_test)) * 100

        # ML Model: Gradient Boosting Regressor
        gbr = GradientBoostingRegressor(n_estimators=80, max_depth=3, random_state=seed, learning_rate=0.08)
        gbr.fit(X_train, y_train)
        y_ml = np.clip(gbr.predict(X_test), 0, None)

        ml_mae = mean_absolute_error(y_test, y_ml)
        ml_rmse = np.sqrt(mean_squared_error(y_test, y_ml))
        ml_wape = (np.sum(np.abs(y_test - y_ml)) / np.sum(y_test)) * 100

        comparison = pd.DataFrame(
            [
                {
                    "Model": "Naive 7-Day Lag Baseline",
                    "MAE ($)": round(naive_mae, 2),
                    "RMSE ($)": round(naive_rmse, 2),
                    "WAPE (%)": round(naive_wape, 2),
                },
                {
                    "Model": "Gradient Boosting Regressor",
                    "MAE ($)": round(ml_mae, 2),
                    "RMSE ($)": round(ml_rmse, 2),
                    "WAPE (%)": round(ml_wape, 2),
                },
            ]
        )

        test_df["naive_prediction"] = y_naive.values
        test_df["ml_prediction"] = np.round(y_ml, 2)

        return ForecastResult(
            train_days=len(train_df),
            test_days=len(test_df),
            split_date=split_date,
            naive_mae=round(naive_mae, 2),
            naive_rmse=round(naive_rmse, 2),
            naive_wape=round(naive_wape, 2),
            ml_mae=round(ml_mae, 2),
            ml_rmse=round(ml_rmse, 2),
            ml_wape=round(ml_wape, 2),
            comparison_table=comparison,
            forecast_df=test_df[["sale_date", "net_sales", "naive_prediction", "ml_prediction"]],
        )
    finally:
        if close_conn:
            conn.close()
