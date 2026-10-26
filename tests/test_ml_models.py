"""Unit tests for ML models: Clustering, Classification, and Forecasting."""

from frogeindrip.ml.classification import train_repeat_purchase_model
from frogeindrip.ml.clustering import train_customer_clusters
from frogeindrip.ml.forecasting import run_sales_forecast


def test_customer_clustering(db_conn):
    """Test K-Means customer segmentation clustering model."""
    res = train_customer_clusters(k=4, conn=db_conn)

    assert res.n_clusters == 4
    assert -1.0 <= res.silhouette <= 1.0
    assert len(res.cluster_summary) == 4
    assert len(res.clustered_df) > 0


def test_repeat_purchase_classification(db_conn):
    """Test time-aware repeat purchase prediction classification."""
    res = train_repeat_purchase_model(conn=db_conn)

    assert res.train_size > 0
    assert res.test_size > 0
    assert 0.0 <= res.baseline_accuracy <= 1.0
    assert 0.0 <= res.rf_metrics["roc_auc"] <= 1.0
    assert len(res.feature_importances) > 0


def test_sales_forecasting(db_conn):
    """Test daily sales forecasting and naive baseline metrics."""
    res = run_sales_forecast(conn=db_conn)

    assert res.train_days > 0
    assert res.test_days > 0
    assert res.naive_mae >= 0.0
    assert res.ml_mae >= 0.0
    assert res.ml_wape >= 0.0
    assert len(res.forecast_df) == res.test_days
