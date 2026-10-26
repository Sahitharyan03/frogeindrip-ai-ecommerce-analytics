"""Configuration management for Frogeindrip Analytics Platform."""

import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src" / "frogeindrip"
DATA_DIR = PROJECT_ROOT / "data"
SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"
DB_PATH = DATA_DIR / "frogeindrip.duckdb"
DOCS_DIR = PROJECT_ROOT / "docs"
REPORTS_DIR = PROJECT_ROOT / "reports"
EVIDENCE_DIR = PROJECT_ROOT / "evidence"

# Ensure directories exist
for p in [DATA_DIR, SYNTHETIC_DATA_DIR, REPORTS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Analytics & Modeling Configuration
DEFAULT_RANDOM_SEED = 42
SIMULATION_START_DATE = "2025-09-01"
SIMULATION_END_DATE = "2026-07-31"

# Evidence Constants from Verified Screenshots
VERIFIED_EVIDENCE = {
    "group_a": {
        "title": "Sales Summary (Sep 01, 2025 – Jul 31, 2026)",
        "net_sales": 46271.26,
        "date_range": "2025-09-01 to 2026-07-31",
        "channels": "All Channels / Location 1",
        "provenance": "Square POS Sales Summary Report",
    },
    "group_b": {
        "title": "Sales Trends (Jul 01, 2025 – Jul 01, 2026)",
        "gross_sales": 38131.26,
        "prior_year_gross_sales": 0.00,
        "growth_badge": "100%",
        "may_2026_gross": 8397.00,
        "july_2026_gross": 1505.00,
        "date_range": "2025-07-01 to 2026-07-01",
        "provenance": "Square POS Sales Trends Tooltip Analysis",
    },
    "pending_claims": {
        "repeat_buyer_gmv_share": 0.35,
        "description": "Resume claim: repeat buyers drove ~35% of GMV.",
        "status": "Pending Verification (Simulated in Synthetic Demo)",
    },
}

# OpenAI API Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
