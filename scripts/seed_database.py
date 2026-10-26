"""Script to generate synthetic data and seed DuckDB database."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

from frogeindrip.etl.pipeline import run_pipeline

if __name__ == "__main__":
    print("🌱 Seeding Frogeindrip database with deterministic synthetic data (seed=42)...")
    summary = run_pipeline()
    print("✅ Database successfully seeded at data/frogeindrip.duckdb!")
    print(f"   Total Orders: {summary['total_orders']}")
    print(f"   Total Net Sales: ${summary['total_net_sales']:,.2f}")
    print(f"   Repeat Buyers: {summary['repeat_buyer_count']}")
