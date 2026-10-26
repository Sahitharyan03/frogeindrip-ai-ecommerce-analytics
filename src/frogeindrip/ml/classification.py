"""Leakage-free Repeat Purchase Prediction via Time-Aware Split Classification."""

from dataclasses import dataclass

import duckdb
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from frogeindrip.config import DB_PATH, DEFAULT_RANDOM_SEED


@dataclass
class ClassificationResult:
    cutoff_date: str
    target_window_days: int
    train_size: int
    test_size: int
    positive_rate: float
    baseline_accuracy: float
    lr_metrics: dict[str, float]
    rf_metrics: dict[str, float]
    feature_importances: pd.DataFrame
    confusion_matrix_rf: list[list[int]]


def train_repeat_purchase_model(
    cutoff_date: str = "2026-04-01",
    window_days: int = 75,
    seed: int = DEFAULT_RANDOM_SEED,
    conn: duckdb.DuckDBPyConnection | None = None,
) -> ClassificationResult:
    """Train time-aware classification model predicting if a customer repeats within window_days.

    Strict leakage prevention:
    - Features are computed ONLY using orders strictly before `cutoff_date`.
    - Labels (y = 1/0) are computed ONLY from orders occurring between `cutoff_date` and `cutoff_date + window_days`.
    """
    close_conn = False
    if conn is None:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        close_conn = True

    try:
        # Extract pre-cutoff behavioral features
        query = f"""
            WITH pre_cutoff_orders AS (
                SELECT
                    customer_id,
                    order_date,
                    net_amount
                FROM raw_orders
                WHERE status = 'completed'
                  AND order_date < DATE '{cutoff_date}'
            ),
            customer_features AS (
                SELECT
                    c.customer_id,
                    c.acquisition_channel,
                    COUNT(p.order_date) AS pre_cutoff_orders,
                    COALESCE(SUM(p.net_amount), 0.0) AS pre_cutoff_spend,
                    COALESCE(AVG(p.net_amount), 0.0) AS pre_cutoff_aov,
                    DATEDIFF('day', MIN(p.order_date), DATE '{cutoff_date}') AS days_as_customer,
                    DATEDIFF('day', MAX(p.order_date), DATE '{cutoff_date}') AS days_since_last_order
                FROM dim_customers c
                JOIN pre_cutoff_orders p ON c.customer_id = p.customer_id
                GROUP BY c.customer_id, c.acquisition_channel
            ),
            future_repeat_labels AS (
                SELECT
                    DISTINCT customer_id,
                    1 AS will_repeat_in_window
                FROM raw_orders
                WHERE status = 'completed'
                  AND order_date >= DATE '{cutoff_date}'
                  AND order_date < DATE '{cutoff_date}' + INTERVAL '{window_days} days'
            )
            SELECT
                cf.customer_id,
                cf.acquisition_channel,
                cf.pre_cutoff_orders,
                cf.pre_cutoff_spend,
                cf.pre_cutoff_aov,
                cf.days_as_customer,
                cf.days_since_last_order,
                COALESCE(fl.will_repeat_in_window, 0) AS target_repeat
            FROM customer_features cf
            LEFT JOIN future_repeat_labels fl ON cf.customer_id = fl.customer_id;
        """
        df = conn.execute(query).fetchdf()

        # One-hot encode acquisition channel
        df_encoded = pd.get_dummies(df, columns=["acquisition_channel"], drop_first=True)

        feature_cols = [c for c in df_encoded.columns if c not in ["customer_id", "target_repeat"]]
        X = df_encoded[feature_cols]
        y = df_encoded["target_repeat"]

        # Train / Test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=seed, stratify=y
        )

        # Baseline: Predict majority class
        majority_class = y_train.mode()[0]
        baseline_acc = float(accuracy_score(y_test, np.full_like(y_test, majority_class)))

        # 1. Logistic Regression Model
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        lr = LogisticRegression(random_state=seed, max_iter=500, class_weight="balanced")
        lr.fit(X_train_scaled, y_train)
        lr_preds = lr.predict(X_test_scaled)
        lr_probs = lr.predict_proba(X_test_scaled)[:, 1]

        lr_metrics = {
            "accuracy": round(float(accuracy_score(y_test, lr_preds)), 3),
            "precision": round(float(precision_score(y_test, lr_preds, zero_division=0)), 3),
            "recall": round(float(recall_score(y_test, lr_preds, zero_division=0)), 3),
            "f1": round(float(f1_score(y_test, lr_preds, zero_division=0)), 3),
            "roc_auc": round(float(roc_auc_score(y_test, lr_probs)), 3),
        }

        # 2. Random Forest Classifier
        rf = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=seed, class_weight="balanced")
        rf.fit(X_train, y_train)
        rf_preds = rf.predict(X_test)
        rf_probs = rf.predict_proba(X_test)[:, 1]

        rf_metrics = {
            "accuracy": round(float(accuracy_score(y_test, rf_preds)), 3),
            "precision": round(float(precision_score(y_test, rf_preds, zero_division=0)), 3),
            "recall": round(float(recall_score(y_test, rf_preds, zero_division=0)), 3),
            "f1": round(float(f1_score(y_test, rf_preds, zero_division=0)), 3),
            "roc_auc": round(float(roc_auc_score(y_test, rf_probs)), 3),
        }

        # Feature Importance from Random Forest
        importances_df = pd.DataFrame(
            {"feature": feature_cols, "importance": rf.feature_importances_}
        ).sort_values("importance", ascending=False).reset_index(drop=True)
        importances_df["importance"] = importances_df["importance"].round(4)

        cm = confusion_matrix(y_test, rf_preds).tolist()

        return ClassificationResult(
            cutoff_date=cutoff_date,
            target_window_days=window_days,
            train_size=len(X_train),
            test_size=len(X_test),
            positive_rate=round(float(y.mean()), 3),
            baseline_accuracy=round(baseline_acc, 3),
            lr_metrics=lr_metrics,
            rf_metrics=rf_metrics,
            feature_importances=importances_df,
            confusion_matrix_rf=cm,
        )
    finally:
        if close_conn:
            conn.close()
