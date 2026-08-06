"""
Final Clean Restructure Engine
==============================
1. Cleans up docs/ subfolders (phase8, phase9, phase10, phase11*) -> archive/deletion_review/markdown/
   So docs/ contains ONLY:
   - ARCHITECTURE.md
   - SETUP.md
   - OPERATIONS.md
   - DATA_PIPELINE.md
   - POWERBI_MODEL.md
   - REPOSITORY_GOVERNANCE.md
   - history/ (BUILD_HISTORY.txt, TECHNICAL_ISSUES.txt, VALIDATION_RESULTS.txt, MIGRATION_HISTORY.txt, DEPRECATED_COMPONENTS.txt)
   - BUILD_HISTORY.txt, FILE_MIGRATION_MAP.txt, TECHNICAL_ISSUES.txt, VALIDATION_RESULTS.txt

2. Organizes root directory loose files:
   - Scripts -> scripts/
   - Audits/Reports -> audits/
   - Tools/Validators -> ERP-BIDSS/tools/ or dashboard_tools/
   - Logs -> audits/
   - Screenshots/Media -> audits/

3. Validates database row counts and PBIX SHA-256 hash.
"""

import sys
import os
import shutil
import glob
import hashlib
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), 'ERP-BIDSS', 'backend'))
from config.database import db
from sqlalchemy import text

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

EXPECTED = {
    'sale_order': 1456,
    'sale_order_line': 9792,
    'fact_sales': 7618,
    'fact_forecast_model_comparison': 17280,
    'fact_forecast_monthly': 2880,
    'pbix_hash': '2250127b86dfcb6ecf5e3aa6270dc444625035c4b14447b0f385ff4ff88178bf'
}

def run_clean():
    print("=" * 75)
    print("EXECUTING FINAL CLEAN RESTRUCTURE & DOCS PURGE")
    print("=" * 75)

    os.makedirs(os.path.join(ROOT_DIR, "audits"), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, "docs", "history"), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, "archive", "deletion_review", "markdown"), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, "archive", "deletion_review", "python"), exist_ok=True)

    # 1. Clean docs/ subdirectories (phase8, phase9, phase10, phase11*)
    docs_dir = os.path.join(ROOT_DIR, "docs")
    for item in os.listdir(docs_dir):
        item_path = os.path.join(docs_dir, item)
        if os.path.isdir(item_path) and item.startswith(("phase", "phase8", "phase9", "phase10", "phase11")):
            target = os.path.join(ROOT_DIR, "archive", "deletion_review", "markdown", item)
            if os.path.exists(target):
                shutil.rmtree(target)
            shutil.move(item_path, target)
            print(f"  [MOVED DOCS SUBDIR] docs/{item} -> archive/deletion_review/markdown/{item}")

    # 2. Move loose reports in root to audits/
    root_reports = [
        "database_baseline.txt", "deletion_candidates.txt", "dependency_map.txt",
        "hardcoded_path_report.txt", "odoo_configuration_report.txt", "powerbi_inventory.txt",
        "proposed_file_migration_map.txt", "python_import_map.txt", "repository_inventory.txt",
        "secret_scan_report.txt", "build_playwright.log", "clone_odoo.log", "clone_upgrade.log",
        "step1_pivot_loaded.png"
    ]
    for rr in root_reports:
        src = os.path.join(ROOT_DIR, rr)
        dst = os.path.join(ROOT_DIR, "audits", rr)
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                print(f"  [MOVED ROOT REPORT] {rr} -> audits/{rr}")
            except Exception:
                shutil.copy(src, dst)
                print(f"  [COPIED ACTIVE REPORT/LOG] {rr} -> audits/{rr}")

    # 3. Move loose Python/PowerShell/Batch scripts in root to scripts/ or ERP-BIDSS/tools/
    root_scripts_to_scripts = [
        "update_odoo_conf.ps1", "scratch_sync.bat", "scan_repository_inventory.py",
        "execute_phase1a_preconditions.py", "execute_phase1a.py", "execute_comprehensive_deep_scan_and_cleanup.py",
        "verify_and_generate_final_reports.py", "master_repository_restructure.py", "run_deep_analysis_scan.py"
    ]
    for rs in root_scripts_to_scripts:
        src = os.path.join(ROOT_DIR, rs)
        dst = os.path.join(ROOT_DIR, "scripts", rs)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"  [MOVED SCRIPT] {rs} -> scripts/{rs}")

    root_tools_to_bidss = [
        "check_fields.py", "check_portfolio.py", "check_portfolio2.py", "check_sales.py",
        "check_xml_ids.py", "clear_assets.py", "find_id1_xml.py", "gate1_sales_pilot.py",
        "query_dashboard.py", "reconcile_transacted.py", "test_granularity.py",
        "test_pivot_dump.py", "test_pivot5_evaluation.py", "test_positional.py", "verify_gate1.py"
    ]
    for rt in root_tools_to_bidss:
        src = os.path.join(ROOT_DIR, rt)
        dst = os.path.join(ROOT_DIR, "ERP-BIDSS", "tools", "diagnostics", rt)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"  [MOVED DIAGNOSTIC TOOL] {rt} -> ERP-BIDSS/tools/diagnostics/{rt}")

    # 4. Database & Power BI Hash Verification
    with db.source_engine.connect() as conn:
        so = pd.read_sql(text("SELECT COUNT(*) FROM sale_order"), conn).iloc[0, 0]
        sol = pd.read_sql(text("SELECT COUNT(*) FROM sale_order_line"), conn).iloc[0, 0]
    with db.target_engine.connect() as conn:
        fs = pd.read_sql(text("SELECT COUNT(*) FROM mart.fact_sales"), conn).iloc[0, 0]
        fmc = pd.read_sql(text("SELECT COUNT(*) FROM mart.fact_forecast_model_comparison"), conn).iloc[0, 0]
        fm = pd.read_sql(text("SELECT COUNT(*) FROM mart.fact_forecast_monthly"), conn).iloc[0, 0]

    assert so == EXPECTED['sale_order'] and sol == EXPECTED['sale_order_line'] and fs == EXPECTED['fact_sales'] and fmc == EXPECTED['fact_forecast_model_comparison'] and fm == EXPECTED['fact_forecast_monthly']

    pbix_files = glob.glob(os.path.join(ROOT_DIR, "**", "*.pbix"), recursive=True)
    for pb in pbix_files:
        hasher = hashlib.sha256()
        with open(pb, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        assert hasher.hexdigest() == EXPECTED['pbix_hash']

    print("\n" + "=" * 75)
    print("FINAL CLEAN RESTRUCTURE PASSED 100% CLEANLY!")
    print("=" * 75)

if __name__ == "__main__":
    run_clean()
