"""Script to run the full ETL, data validation, and dbt transformations."""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

from frogeindrip.etl.pipeline import run_pipeline

if __name__ == "__main__":
    print("🚀 Running Frogeindrip Data Ingestion, Validation & Mart Pipeline...")
    res = run_pipeline()
    print("✅ Python ETL & DuckDB staging complete.")

    print("\n📦 Running dbt transformations...")
    dbt_dir = ROOT_DIR / "dbt"
    dbt_bin = ROOT_DIR / ".venv" / "bin" / "dbt"
    cmd = [str(dbt_bin) if dbt_bin.exists() else "dbt", "run", "--profiles-dir", "."]
    subprocess.run(cmd, cwd=dbt_dir, check=True)

    print("\n🧪 Running dbt automated tests...")
    test_cmd = [str(dbt_bin) if dbt_bin.exists() else "dbt", "test", "--profiles-dir", "."]
    subprocess.run(test_cmd, cwd=dbt_dir, check=True)

    print("\n🎉 Pipeline executed and verified successfully!")
