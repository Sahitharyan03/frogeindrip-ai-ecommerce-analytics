"""Page 5: Predictive Analytics & Machine Learning Models."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

import pandas as pd
import streamlit as st

from app.components.charts import build_cluster_scatter, build_forecast_plot
from app.components.ui import inject_custom_css, render_page_header, render_sidebar
from frogeindrip.ml.classification import train_repeat_purchase_model
from frogeindrip.ml.clustering import train_customer_clusters
from frogeindrip.ml.forecasting import run_sales_forecast

st.set_page_config(page_title="Predictive Analytics | Frogeindrip", page_icon="🐸", layout="wide")
inject_custom_css()
render_sidebar()

render_page_header(
    title="Predictive Analytics & Machine Learning",
    subtitle="Customer K-Means clustering, leakage-free repeat purchase classification, and sales forecasting.",
    badge_type="synthetic",
)

# ML Governance Notice
st.warning(
    """
    **Machine Learning Governance & Synthetic Data Disclosure:**  
    These models are trained on deterministic synthetic behavioral data simulating the Frogeindrip DTC launch. 
    While the modeling techniques enforce industry-best practices (strict time-based splits, zero future data leakage, baseline comparisons), 
    synthetic model performance does not guarantee identical real-world prediction accuracy.
    """
)

tabs = st.tabs(["🎯 1. Customer Clustering (K-Means)", "🔁 2. Repeat-Purchase Prediction", "📈 3. Sales Forecasting"])

# Tab 1: Clustering
with tabs[0]:
    st.markdown("### Customer Behavioral Segmentation via K-Means")
    st.caption("Segments customers based on Recency, Frequency, Monetary value, Average Order Value, and Customer Tenure.")

    k_val = st.slider("Select Number of Clusters (k)", min_value=3, max_value=6, value=4)
    c_res = train_customer_clusters(k=k_val)

    cl_c1, cl_c2 = st.columns(2)
    with cl_c1:
        st.metric("Silhouette Score (Clustering Quality)", f"{c_res.silhouette}")
    with cl_c2:
        st.metric("Davies-Bouldin Index", f"{c_res.davies_bouldin}")

    st.plotly_chart(build_cluster_scatter(c_res.clustered_df), use_container_width=True)

    st.markdown("#### Cluster Profiles & Feature Averages")
    st.dataframe(c_res.cluster_summary, use_container_width=True)

# Tab 2: Classification
with tabs[1]:
    st.markdown("### Time-Aware Repeat Purchase Prediction")
    st.caption("Predicts if a customer will place a repeat order in a 75-day future window using only pre-cutoff features.")

    clf_res = train_repeat_purchase_model()

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Naive Baseline Accuracy", f"{clf_res.baseline_accuracy * 100:.1f}%")
    with col_m2:
        st.metric("Random Forest ROC-AUC", f"{clf_res.rf_metrics['roc_auc']:.3f}")
    with col_m3:
        st.metric("Random Forest F1-Score", f"{clf_res.rf_metrics['f1']:.3f}")
    with col_m4:
        st.metric("Training Sample Size", f"{clf_res.train_size} customers")

    col_f1, col_f2 = st.columns([3, 2])
    with col_f1:
        st.markdown("#### Feature Importance (Random Forest)")
        st.bar_chart(clf_res.feature_importances.set_index("feature"))

    with col_f2:
        st.markdown("#### Model Comparison Matrix")
        comp_df = pd.DataFrame([
            {"Model": "Majority Baseline", "Accuracy": clf_res.baseline_accuracy, "Precision": 0.0, "Recall": 0.0, "F1": 0.0, "ROC-AUC": 0.50},
            {"Model": "Logistic Regression", **clf_res.lr_metrics},
            {"Model": "Random Forest", **clf_res.rf_metrics},
        ])
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        st.markdown("#### Confusion Matrix (Holdout Set)")
        cm_df = pd.DataFrame(clf_res.confusion_matrix_rf, columns=["Pred: No Repeat", "Pred: Repeat"], index=["Actual: No", "Actual: Yes"])
        st.dataframe(cm_df, use_container_width=True)

# Tab 3: Forecasting
with tabs[2]:
    st.markdown("### Daily Sales Forecasting vs. Naive Baseline")
    st.caption("Compares Gradient Boosting Regressor with lag & calendar features against a Naive 7-Day Lag Baseline.")

    fc_res = run_sales_forecast()

    f_c1, f_c2, f_c3 = st.columns(3)
    with f_c1:
        st.metric("ML Forecast MAE", f"${fc_res.ml_mae:.2f}", f"Baseline: ${fc_res.naive_mae:.2f}")
    with f_c2:
        st.metric("ML Forecast RMSE", f"${fc_res.ml_rmse:.2f}", f"Baseline: ${fc_res.naive_rmse:.2f}")
    with f_c3:
        st.metric("ML Forecast WAPE", f"{fc_res.ml_wape:.1f}%", f"Baseline: {fc_res.naive_wape:.1f}%")

    st.plotly_chart(build_forecast_plot(fc_res.forecast_df), use_container_width=True)

    st.markdown("#### Baseline vs. Machine Learning Forecast Evaluation")
    st.dataframe(fc_res.comparison_table, use_container_width=True, hide_index=True)
