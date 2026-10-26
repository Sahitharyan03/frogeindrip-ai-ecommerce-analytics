"""Plotly chart builder module with tailored executive styling."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def set_chart_theme(fig: go.Figure) -> go.Figure:
    """Apply unified dark-mode sleek aesthetics to Plotly charts."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.0)",
        plot_bgcolor="rgba(30, 41, 59, 0.4)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor="#334155", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#334155", zeroline=False),
    )
    return fig


def build_monthly_sales_chart(df: pd.DataFrame) -> go.Figure:
    """Build combo bar and line chart for monthly net revenue and MoM growth."""
    fig = go.Figure()

    # Net Sales Bars
    fig.add_trace(
        go.Bar(
            x=df["year_month"],
            y=df["total_net_sales"],
            name="Net Revenue ($)",
            marker=dict(color="#10b981", line=dict(color="#34d399", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Net Revenue: $%{y:,.2f}<extra></extra>",
        )
    )

    # Gross Margin Line
    if "gross_margin_pct" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["year_month"],
                y=df["gross_margin_pct"],
                name="Gross Margin (%)",
                yaxis="y2",
                mode="lines+markers",
                line=dict(color="#38bdf8", width=3),
                marker=dict(size=7, color="#0284c7"),
                hovertemplate="<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>",
            )
        )

    fig.update_layout(
        title="<b>Monthly Net Sales & Gross Margin Trajectory</b>",
        yaxis=dict(title="Net Revenue ($)", showgrid=True, gridcolor="#334155"),
        yaxis2=dict(
            title="Margin (%)",
            overlaying="y",
            side="right",
            showgrid=False,
            range=[0, 100],
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return set_chart_theme(fig)


def build_day_hour_charts(dow_df: pd.DataFrame, hour_df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    """Build Day-of-Week and Hour-of-Day distribution bar charts."""
    # Day of Week
    fig_dow = go.Figure(
        go.Bar(
            x=dow_df["day_name"],
            y=dow_df["net_sales"],
            marker=dict(color="#6366f1"),
            hovertemplate="<b>%{x}</b><br>Net Sales: $%{y:,.2f}<extra></extra>",
        )
    )
    fig_dow.update_layout(title="<b>Sales Distribution by Day of Week</b>", yaxis_title="Net Sales ($)")
    set_chart_theme(fig_dow)

    # Hour of Day
    fig_hour = go.Figure(
        go.Bar(
            x=hour_df["hour_of_day"],
            y=hour_df["net_sales"],
            marker=dict(color="#ec4899"),
            hovertemplate="<b>Hour %{x}:00</b><br>Net Sales: $%{y:,.2f}<extra></extra>",
        )
    )
    fig_hour.update_layout(
        title="<b>Sales Volume by Hour of Day (EST)</b>",
        xaxis_title="Hour of Day (0–23)",
        yaxis_title="Net Sales ($)",
    )
    set_chart_theme(fig_hour)

    return fig_dow, fig_hour


def build_rfm_treemap(df: pd.DataFrame) -> go.Figure:
    """Build RFM Treemap displaying segment sizes and monetary contributions."""
    fig = px.treemap(
        df,
        path=["segment_label"],
        values="total_segment_spend",
        color="avg_customer_spend",
        color_continuous_scale="Viridis",
        title="<b>Customer Segment Value Map (Size: Total GMV, Color: Avg Customer Spend)</b>",
    )
    fig.update_traces(
        textinfo="label+value+percent root",
        hovertemplate="<b>%{label}</b><br>Total GMV: $%{value:,.2f}<br>Avg Spend: $%{color:,.2f}<extra></extra>",
    )
    return set_chart_theme(fig)


def build_cohort_heatmap(pivot_df: pd.DataFrame) -> go.Figure:
    """Build Cohort Retention Heatmap."""
    fig = go.Figure(
        go.Heatmap(
            z=pivot_df.values,
            x=[f"Month {col}" for col in pivot_df.columns],
            y=pivot_df.index,
            colorscale="Teal",
            text=pivot_df.applymap(lambda v: f"{v:.1f}%" if pd.notnull(v) else "").values,
            texttemplate="%{text}",
            textfont=dict(size=12, color="#ffffff"),
            colorbar=dict(title="Retention %"),
            hoverongaps=False,
        )
    )
    fig.update_layout(
        title="<b>Monthly Customer Cohort Retention Heatmap (%)</b>",
        xaxis_title="Months Elapsed Since Acquisition",
        yaxis_title="Acquisition Cohort Month",
    )
    return set_chart_theme(fig)


def build_forecast_plot(df: pd.DataFrame) -> go.Figure:
    """Build sales forecast vs actuals with naive baseline comparisons."""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["sale_date"],
            y=df["net_sales"],
            name="Actual Holdout Sales",
            mode="lines+markers",
            line=dict(color="#f8fafc", width=2.5),
            marker=dict(size=5),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["sale_date"],
            y=df["ml_prediction"],
            name="Gradient Boosting Forecast",
            mode="lines",
            line=dict(color="#10b981", width=2.5, dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["sale_date"],
            y=df["naive_prediction"],
            name="Naive 7-Day Lag Baseline",
            mode="lines",
            line=dict(color="#94a3b8", width=1.5, dash="dot"),
        )
    )

    fig.update_layout(
        title="<b>Holdout Period Daily Sales: Actual vs ML Forecast vs Naive Baseline</b>",
        xaxis_title="Date",
        yaxis_title="Daily Net Sales ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return set_chart_theme(fig)


def build_cluster_scatter(df: pd.DataFrame) -> go.Figure:
    """Build 2D scatter of customer clusters across Recency and Monetary spend."""
    fig = px.scatter(
        df,
        x="recency_days",
        y="monetary",
        color="cluster_name",
        size="frequency",
        hover_data=["customer_id", "avg_order_value"],
        log_y=True,
        title="<b>Customer Behavioral Clusters (K-Means k=4)</b>",
        color_discrete_sequence=["#10b981", "#3b82f6", "#f59e0b", "#ec4899"],
    )
    fig.update_layout(
        xaxis_title="Recency (Days Since Last Order)",
        yaxis_title="Monetary Spend (Log Scale $)",
    )
    return set_chart_theme(fig)
