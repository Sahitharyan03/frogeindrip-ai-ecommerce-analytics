"""Script to compile and export the executive analytics markdown report."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

from frogeindrip.utils.export import generate_executive_markdown_report
from frogeindrip.config import REPORTS_DIR

if __name__ == "__main__":
    report_file = REPORTS_DIR / "executive_summary_report.md"
    print("📝 Generating executive markdown analytics report...")
    md = generate_executive_markdown_report(report_file)
    print(f"✅ Report successfully generated at {report_file} ({len(md)} characters)!")
