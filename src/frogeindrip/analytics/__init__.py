"""Analytics and KPI computation module."""

from frogeindrip.analytics.cohorts import get_cohort_matrix
from frogeindrip.analytics.kpis import get_executive_kpis, get_sales_by_time_dimensions
from frogeindrip.analytics.retention import get_repeat_buyer_analysis
from frogeindrip.analytics.rfm import get_rfm_analysis

__all__ = [
    "get_cohort_matrix",
    "get_executive_kpis",
    "get_repeat_buyer_analysis",
    "get_rfm_analysis",
    "get_sales_by_time_dimensions",
]
