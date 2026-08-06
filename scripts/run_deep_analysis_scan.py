"""
Deep Analysis Data Generator for 24-Step Workflow
=================================================
Scans repository to gather exact empirical numbers for the 24-step analysis report.
"""

import sys
import os
import hashlib
import glob
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), 'ERP-BIDSS', 'backend'))
from config.database import db
from sqlalchemy import text

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def analyze():
    print("=" * 75)
    print("DEEP ANALYSIS METRIC SCANNER (24 STEPS)")
    print("=" * 75)

    # Markdown count
    md_files = [os.path.relpath(p, ROOT_DIR) for p in glob.glob(os.path.join(ROOT_DIR, "**", "*.md"), recursive=True) if ".venv" not in p and "clone_data_dir" not in p]
    print(f"Total Active Markdown Files ({len(md_files)}):")
    for m in md_files:
        print(f"  - {m}")

    # Python count
    py_files = [os.path.relpath(p, ROOT_DIR) for p in glob.glob(os.path.join(ROOT_DIR, "**", "*.py"), recursive=True) if ".venv" not in p and "clone_data_dir" not in p]
    print(f"\nTotal Python Files Tracked ({len(py_files)})")

    # JSON count
    json_files = [os.path.relpath(p, ROOT_DIR) for p in glob.glob(os.path.join(ROOT_DIR, "**", "*.json"), recursive=True) if ".venv" not in p and "clone_data_dir" not in p]
    print(f"\nTotal JSON Assets Tracked ({len(json_files)})")

    # Database Baseline
    with db.source_engine.connect() as conn:
        so = pd.read_sql(text("SELECT COUNT(*) FROM sale_order"), conn).iloc[0, 0]
        sol = pd.read_sql(text("SELECT COUNT(*) FROM sale_order_line"), conn).iloc[0, 0]
    with db.target_engine.connect() as conn:
        fs = pd.read_sql(text("SELECT COUNT(*) FROM mart.fact_sales"), conn).iloc[0, 0]
        fmc = pd.read_sql(text("SELECT COUNT(*) FROM mart.fact_forecast_model_comparison"), conn).iloc[0, 0]
        fm = pd.read_sql(text("SELECT COUNT(*) FROM mart.fact_forecast_monthly"), conn).iloc[0, 0]

    print(f"\nDatabase Row Counts: sale_order={so}, sale_order_line={sol}, fact_sales={fs}, fmc={fmc}, fm={fm}")

    # PBIX Hash
    pbix_files = glob.glob(os.path.join(ROOT_DIR, "**", "*.pbix"), recursive=True)
    for pb in pbix_files:
        hasher = hashlib.sha256()
        with open(pb, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        print(f"PBIX SHA256: {hasher.hexdigest()}")

if __name__ == "__main__":
    analyze()
