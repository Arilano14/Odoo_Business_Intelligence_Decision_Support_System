"""
Phase 0 Read-Only Inventory & Repository Scanner
=================================================
Scans Project Odoo workspace to produce initial diagnostic inventory files:
1. repository_inventory.txt
2. dependency_map.txt
3. python_import_map.txt
4. hardcoded_path_report.txt
5. secret_scan_report.txt
6. database_baseline.txt
7. odoo_configuration_report.txt
8. powerbi_inventory.txt
9. proposed_file_migration_map.txt
10. deletion_candidates.txt
11. audits/deletion_manifest.csv
"""

import sys
import os
import re
import hashlib
import json
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), 'ERP-BIDSS', 'backend'))
from config.database import db
from sqlalchemy import text

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def run_scan():
    print("=" * 75)
    print("PHASE 0: READ-ONLY REPOSITORY INVENTORY & GOVERNANCE SCAN")
    print("=" * 75)

    os.makedirs(os.path.join(ROOT_DIR, "audits"), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, "docs"), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, "scripts"), exist_ok=True)

    # 1. Repository Inventory Scan
    inventory_items = []
    python_imports = []
    hardcoded_paths = []
    secrets = []
    powerbi_files = []
    deletion_candidates = []

    non_code_dirs = {'.git', '.venv', '__pycache__', 'clone_data_dir', 'clone_filestore', 'odoo_data'}
    
    forbidden_terms = ['final', 'perfect', 'approved', 'fix', 'revised', 'forensic', 'gate1', 'agent', 'ai', 'antigravity', 'gemini', 'scratch', 'brain']

    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in non_code_dirs]
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), ROOT_DIR)
            abs_path = os.path.join(root, f)
            size_b = os.path.getsize(abs_path)
            inventory_items.append(f"{rel_path} ({size_b} bytes)")

            # Check PBIX
            if f.endswith('.pbix'):
                powerbi_files.append({
                    'path': rel_path,
                    'size_bytes': size_b,
                    'mtime': os.path.getmtime(abs_path)
                })

            # Check forbidden terms in filename
            lower_name = f.lower()
            if any(term in lower_name for term in forbidden_terms):
                deletion_candidates.append({
                    'path': rel_path,
                    'reason': 'Contains non-professional or temporary terminology',
                    'action': 'SUMMARIZE_THEN_DELETE' if f.endswith('.md') or f.endswith('.txt') else 'RENAME_OR_QUARANTINE'
                })

            # Scan text contents of python, xml, conf, json, md, txt files
            if f.endswith(('.py', '.xml', '.conf', '.json', '.txt', '.md', '.bat', '.ps1')):
                try:
                    with open(abs_path, 'r', encoding='utf-8', errors='ignore') as file_in:
                        content = file_in.read()
                        
                        # Check Python imports
                        if f.endswith('.py'):
                            for line in content.splitlines():
                                if line.strip().startswith(('import ', 'from ')):
                                    python_imports.append(f"{rel_path}: {line.strip()}")
                        
                        # Check hardcoded paths (e.g. C:\Users...)
                        matches_path = re.findall(r'[C-Z]:\\[^\s"\']+', content)
                        for mp in matches_path:
                            hardcoded_paths.append(f"{rel_path}: {mp}")

                        # Secret scan (simple patterns)
                        if any(kw in content for kw in ['password =', 'secret =', 'api_key =', 'token =']):
                            for line in content.splitlines():
                                if any(kw in line.lower() for kw in ['password', 'secret', 'key', 'token']):
                                    secrets.append(f"{rel_path}: {line.strip()}")
                except Exception as e:
                    pass

    # Save 1. repository_inventory.txt
    with open(os.path.join(ROOT_DIR, "repository_inventory.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(inventory_items))
    print(f"[OK] Generated repository_inventory.txt ({len(inventory_items)} files tracked)")

    # Save 2. python_import_map.txt
    with open(os.path.join(ROOT_DIR, "python_import_map.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(python_imports))
    print(f"[OK] Generated python_import_map.txt ({len(python_imports)} import statements recorded)")

    # Save 3. hardcoded_path_report.txt
    with open(os.path.join(ROOT_DIR, "hardcoded_path_report.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(hardcoded_paths))
    print(f"[OK] Generated hardcoded_path_report.txt ({len(hardcoded_paths)} hardcoded paths detected)")

    # Save 4. secret_scan_report.txt
    with open(os.path.join(ROOT_DIR, "secret_scan_report.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(secrets))
    print(f"[OK] Generated secret_scan_report.txt ({len(secrets)} potential secret lines scanned)")

    # Save 5. powerbi_inventory.txt
    with open(os.path.join(ROOT_DIR, "powerbi_inventory.txt"), 'w', encoding='utf-8') as f:
        for pb in powerbi_files:
            f.write(f"File: {pb['path']} | Size: {pb['size_bytes']} bytes | Database Target: Business_Intelegent_Project_v2_fresh_clone / mart\n")
    print(f"[OK] Generated powerbi_inventory.txt ({len(powerbi_files)} PBIX files cataloged)")

    # 6. Database Baseline Scan (Read-only row counts)
    db_baseline_lines = []
    try:
        with db.source_engine.connect() as conn:
            so_cnt = pd.read_sql(text("SELECT COUNT(*) FROM sale_order"), conn).iloc[0, 0]
            sol_cnt = pd.read_sql(text("SELECT COUNT(*) FROM sale_order_line"), conn).iloc[0, 0]
            db_baseline_lines.append(f"Odoo Source Database: sale_order={so_cnt}, sale_order_line={sol_cnt}")
    except Exception as e:
        db_baseline_lines.append(f"Odoo Source Database Scan Error: {e}")

    try:
        with db.target_engine.connect() as conn:
            fs_cnt = pd.read_sql(text("SELECT COUNT(*) FROM mart.fact_sales"), conn).iloc[0, 0]
            fmc_cnt = pd.read_sql(text("SELECT COUNT(*) FROM mart.fact_forecast_model_comparison"), conn).iloc[0, 0]
            fm_cnt = pd.read_sql(text("SELECT COUNT(*) FROM mart.fact_forecast_monthly"), conn).iloc[0, 0]
            db_baseline_lines.append(f"Data Mart Schema 'mart': fact_sales={fs_cnt}, fact_forecast_model_comparison={fmc_cnt}, fact_forecast_monthly={fm_cnt}")
    except Exception as e:
        db_baseline_lines.append(f"Data Mart Database Scan Error: {e}")

    with open(os.path.join(ROOT_DIR, "database_baseline.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(db_baseline_lines))
    print(f"[OK] Generated database_baseline.txt:\n  " + "\n  ".join(db_baseline_lines))

    # 7. Odoo Configuration Report
    odoo_conf_lines = [
        "Main Odoo Config (odoo.conf): Port 8069, DB Business_Intelegent_Project_v2",
        "Clone Odoo Config (clone_odoo.conf): Port 8070, DB Business_Intelegent_Project_v2_fresh_clone",
        "Custom Addon Path: custom_addons/obidss_operational_bi"
    ]
    with open(os.path.join(ROOT_DIR, "odoo_configuration_report.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(odoo_conf_lines))
    print(f"[OK] Generated odoo_configuration_report.txt")

    # 8. Dependency Map & Deletion Candidates Manifest
    del_df = pd.DataFrame(deletion_candidates)
    if not del_df.empty:
        del_df.to_csv(os.path.join(ROOT_DIR, "audits", "deletion_manifest.csv"), index=False)
        with open(os.path.join(ROOT_DIR, "deletion_candidates.txt"), 'w', encoding='utf-8') as f:
            for idx, r in del_df.iterrows():
                f.write(f"File: {r['path']} | Action: {r['action']} | Reason: {r['reason']}\n")
    print(f"[OK] Generated deletion_candidates.txt and audits/deletion_manifest.csv ({len(deletion_candidates)} candidates identified)")

    # 9. Proposed File Migration Map
    migration_map_lines = [
        "PROPOSED RESTRUCTURING & FILE MIGRATION MAP (SAFETY_MODE=STRICT)",
        "================================================================",
        "Target Directory Structure:",
        "  - scripts/             : Scripts otomasi build, validate, & governance",
        "  - docs/                : Dokumentasi arsitektur, setup, & governance",
        "  - audits/              : Laporan audit, manifest penghapusan, & log",
        "",
        "Planned File Moves (Phase 1 Low-Risk Migration):",
        "  - generate_audited_artifacts.py -> scripts/generate_audited_artifacts.py",
        "  - generate_dashboard_artifacts.py -> scripts/generate_dashboard_artifacts.py",
        "  - generate_final_perfect_artifacts.py -> scripts/build_dashboard_spreadsheets.py",
        "  - build_sales_dashboard.py -> scripts/build_sales_dashboard.py",
        "  - product_scope_gate.py -> scripts/validate_product_scope.py",
        "  - verify_dashboards.py -> scripts/verify_dashboards.py",
        "  - verify_final_dashboards.py -> scripts/verify_final_dashboards.py",
        "  - audit_baselines.py -> scripts/audit_baselines.py",
        "  - inspect_models.py -> scripts/inspect_models.py",
        "  - investigate_scope.py -> scripts/investigate_scope.py",
        "  - check_portfolio.py -> scripts/check_portfolio.py",
        "  - check_portfolio2.py -> scripts/check_portfolio.py",
        "  - check_sales.py -> scripts/check_sales.py",
        "  - check_xml_ids.py -> scripts/check_xml_ids.py",
        "  - cleanup_duplicates.py -> scripts/cleanup_duplicates.py",
        "  - fix_dashboards.py -> scripts/fix_dashboards.py",
        "  - debug_monthly_forensics.py -> scripts/debug_monthly_forensics.py",
        "  - test_granularity.py -> scripts/test_granularity.py",
        "  - test_pivot5_evaluation.py -> scripts/test_pivot5_evaluation.py",
        "  - test_pivot_dump.py -> scripts/test_pivot_dump.py",
        "  - test_positional.py -> scripts/test_positional.py",
        "  - query_dashboard.py -> scripts/query_dashboard.py",
        "  - assign_group.py -> scripts/assign_group.py",
        "  - buttons.txt -> audits/buttons.txt",
        "  - buttons_pivot.txt -> audits/buttons_pivot.txt",
        "  - buttons_pivot2.txt -> audits/buttons_pivot2.txt",
        "  - icons_pivot2.txt -> audits/icons_pivot2.txt",
        "  - oops_details.txt -> audits/oops_details.txt",
        "  - odoo_conf_modified_line.txt -> audits/odoo_conf_modified_line.txt",
        "  - build_playwright.log -> audits/build_playwright.log",
        "  - clone_upgrade.log -> audits/clone_upgrade.log"
    ]
    with open(os.path.join(ROOT_DIR, "proposed_file_migration_map.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(migration_map_lines))
    print(f"[OK] Generated proposed_file_migration_map.txt")

    with open(os.path.join(ROOT_DIR, "dependency_map.txt"), 'w', encoding='utf-8') as f:
        f.write("DEPENDENCY MAP SUMMARY:\n" + "\n".join(hardcoded_paths))
    print(f"[OK] Generated dependency_map.txt")

    print("\n[SUCCESS] PHASE 0 READ-ONLY INVENTORY & DIAGNOSTICS COMPLETE!")

if __name__ == "__main__":
    run_scan()
