"""Customer Segmentation via K-Means Clustering on Behavioral Features."""

from dataclasses import dataclass

import duckdb
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler

from frogeindrip.config import DB_PATH, DEFAULT_RANDOM_SEED


@dataclass
class ClusteringResult:
    n_clusters: int
    silhouette: float
    davies_bouldin: float
    cluster_centers: pd.DataFrame
    cluster_summary: pd.DataFrame
    clustered_df: pd.DataFrame


def train_customer_clusters(
    k: int = 4,
    seed: int = DEFAULT_RANDOM_SEED,
    conn: duckdb.DuckDBPyConnection | None = None,
) -> ClusteringResult:
    """Train K-Means clustering on customer behavioral features."""
    close_conn = False
    if conn is None:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        close_conn = True

    try:
        # Extract customer features
        query = """
            SELECT
                r.customer_id,
                r.recency_days,
                r.frequency,
                r.monetary,
                COALESCE(c.lifetime_net_spend / NULLIF(c.lifetime_orders, 0), 0) AS avg_order_value,
                DATEDIFF('day', c.registered_at, DATE '2026-08-01') AS customer_tenure_days
            FROM mart_rfm_segments r
            JOIN dim_customers c ON r.customer_id = c.customer_id
            WHERE r.frequency > 0
        """
        df = conn.execute(query).fetchdf()

        feature_cols = [
            "recency_days",
            "frequency",
            "monetary",
            "avg_order_value",
            "customer_tenure_days",
        ]
        X = df[feature_cols].copy()

        # Log transform skewed monetary & frequency features
        X_trans = X.copy()
        X_trans["monetary"] = np.log1p(X_trans["monetary"])
        X_trans["avg_order_value"] = np.log1p(X_trans["avg_order_value"])

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_trans)

        kmeans = KMeans(n_clusters=k, random_state=seed, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        sil = float(silhouette_score(X_scaled, labels))
        db = float(davies_bouldin_score(X_scaled, labels))

        df["cluster"] = labels

        # Label interpretation based on cluster means
        means = df.groupby("cluster")[feature_cols].mean().round(2)
        sizes = df.groupby("cluster")["customer_id"].count()
        spend_shares = (df.groupby("cluster")["monetary"].sum() / df["monetary"].sum() * 100).round(2)

        summary = means.copy()
        summary["customer_count"] = sizes
        summary["gmv_share_pct"] = spend_shares

        # Assign descriptive segment names
        cluster_names = {}
        for c_idx, row in summary.iterrows():
            if row["frequency"] >= 2.5 and row["monetary"] >= 200:
                cluster_names[c_idx] = "Power VIP Repeaters"
            elif row["recency_days"] <= 60 and row["frequency"] <= 1.5:
                cluster_names[c_idx] = "Recent First-Time Drops"
            elif row["recency_days"] > 150:
                cluster_names[c_idx] = "Dormant / Lapsed Buyers"
            else:
                cluster_names[c_idx] = "Mid-Frequency Core"

        summary["cluster_name"] = summary.index.map(cluster_names)
        df["cluster_name"] = df["cluster"].map(cluster_names)

        centers_df = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=feature_cols)
        centers_df["monetary"] = np.expm1(centers_df["monetary"]).round(2)
        centers_df["avg_order_value"] = np.expm1(centers_df["avg_order_value"]).round(2)

        return ClusteringResult(
            n_clusters=k,
            silhouette=round(sil, 3),
            davies_bouldin=round(db, 3),
            cluster_centers=centers_df,
            cluster_summary=summary,
            clustered_df=df,
        )
    finally:
        if close_conn:
            conn.close()
