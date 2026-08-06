# PROFESSIONAL REPOSITORY CODING TREE AND DEPENDENCY IMPACT ANALYSIS

> **Canonical Repository**: `https://github.com/Arilano14/Odoo_Business_Intelligence_Decision_Support_System.git`  
> **Maintainer & Code Owner**: `@Arilano14`  
> **Status**: `READY_FOR_OWNER_REVIEW` (Phases 1B through 10 & 24-Step Deep Cleanup 100% PASS)

---

## 1. REPOSITORY CODING TREE VISUALIZATION (FULLY REFINED & CLEANED)

```text
Project Odoo/
├── .github/
│   ├── CODEOWNERS                             (Attribution and approval rules)
│   └── workflows/
│       └── repository-integrity.yml           (GitHub Actions CI static check)
├── archive/
│   └── deletion_review/
│       ├── phase_1b/                          (Retired raw text log artifacts)
│       ├── markdown/                          (Quarantined historical phase Markdown files)
│       ├── python/                            (Quarantined scratch Python scripts)
│       └── html/                              (Quarantined HTML page dumps)
├── audits/
│   ├── database_baseline.txt                  (Database baseline report)
│   ├── deletion_candidates.txt                (Deletion candidate inventory)
│   ├── dependency_map.txt                     (Dependency mapping report)
│   ├── final_database_reconciliation.txt      (Database row counts baseline)
│   ├── final_deletion_manifest.csv            (Manifest of audited file retirements)
│   ├── final_file_migration_map.txt           (Complete file migration mapping)
│   ├── final_file_tree.txt                    (Complete repository file inventory)
│   ├── final_powerbi_hash.txt                 (Power BI SHA-256 baseline)
│   ├── final_repository_validation.txt        (Post-validation suite report)
│   ├── hardcoded_path_report.txt              (Hardcoded path audit report)
│   ├── markdown_classification.csv            (Classification manifest of 118 Markdown files)
│   ├── odoo_configuration_report.txt          (Odoo server port configuration report)
│   ├── powerbi_inventory.txt                  (Power BI asset inventory)
│   ├── proposed_file_migration_map.txt        (Proposed file migration plan)
│   ├── python_import_map.txt                  (Python import statement inventory)
│   ├── repository_inventory.txt               (Complete repository inventory log)
│   ├── script_classification.csv              (Static classification of Python scripts)
│   ├── secret_scan_report.txt                 (Secret scanning audit log)
│   └── TECHNICAL_ISSUES.txt                   (Technical issues & resolution log)
├── custom_addons/
│   └── obidss_operational_bi/                 (Custom Odoo 18 BI Addon)
│       ├── __manifest__.py                    (Addon manifest & metadata)
│       ├── __init__.py                        (Python package initializer)
│       ├── hooks.py                           (Post-init Odoo database hooks)
│       ├── models/
│       │   ├── __init__.py
│       │   └── dashboard_pivot_fix.py         (Spreadsheet monthly date granularity patch)
│       ├── views/
│       │   └── menu_views.xml                 (Odoo menu action definitions)
│       └── data/
│           └── dashboard_data.xml             (Dashboard XML records)
├── dashboard_assets/
│   ├── reference/
│   │   └── verified_portfolio_product_ids.txt (240 Verified Portfolio Product ID list)
│   └── templates/
│       ├── pivot/                             (Pivot-enabled spreadsheet templates)
│       │   ├── executive.json
│       │   ├── sales.json
│       │   ├── purchase.json
│       │   └── inventory.json
│       └── fallback/                          (Standard spreadsheet fallback templates)
│           ├── executive.json
│           ├── sales.json
│           ├── purchase.json
│           ├── inventory.json
│           ├── finance.json
│           └── data_quality.json
├── dashboard_tools/                           (Dashboard Tooling Suite)
│   ├── __init__.py
│   ├── paths.py                               (Central repository-relative path resolver)
│   ├── builders/
│   │   ├── build_dashboard_artifacts.py
│   │   ├── build_verified_dashboard_artifacts.py
│   │   ├── build_monthly_dashboard_artifacts.py
│   │   └── build_sales_dashboard.py
│   ├── validators/
│   │   ├── validate_dashboard_schema.py
│   │   ├── validate_dashboard_rendering.py
│   │   ├── validate_product_scope.py
│   │   └── reconcile_financial_baselines.py
│   ├── diagnostics/
│   │   ├── diagnose_monthly_pivot_dates.py
│   │   └── investigate_dashboard_date_axis.py
│   └── maintenance/
│       ├── repair_dashboard_artifacts.py
│       ├── remove_duplicate_dashboard_records.py
│       └── assign_dashboard_group.py
├── docs/                                      (Professional Project Documentation)
│   ├── ARCHITECTURE.md                        (System architecture overview)
│   ├── DATA_PIPELINE.md                       (ETL & forecasting data pipeline)
│   ├── OPERATIONS.md                          (Odoo & ETL operational guide)
│   ├── POWERBI_MODEL.md                       (Power BI model & DAX specification)
│   ├── REPOSITORY_GOVERNANCE.md               (GitHub governance & branch security)
│   ├── SETUP.md                               (Setup & installation guide)
│   └── history/                               (Historical Technical Records in TXT)
│       ├── BUILD_HISTORY.txt                  (Chronological technical build milestones)
│       ├── TECHNICAL_ISSUES.txt               (Technical issues & root causes)
│       ├── VALIDATION_HISTORY.txt             (Accuracy & reconciliation audit history)
│       ├── MIGRATION_HISTORY.txt              (File migration & restructuring history)
│       └── DEPRECATED_COMPONENTS.txt          (Retired component log)
├── ERP-BIDSS/                                 (BI Decision Support System Engine)
│   ├── backend/
│   │   ├── analytics/
│   │   │   ├── calculate_decision_support.py  (Inventory replenishment analytics)
│   │   │   └── benchmark_forecast_models.py   (6-Model rolling horizon engine)
│   │   ├── config/
│   │   │   ├── database.py                    (PostgreSQL connection manager)
│   │   │   └── settings.py                    (Environment settings & DB URLs)
│   │   ├── odoo/
│   │   │   └── connection.py                  (Odoo XML-RPC ORM client)
│   │   ├── pipelines/
│   │   │   └── run_scenario_v2_pipeline.py    (Phase 11.4 full pipeline orchestration)
│   │   └── scenarios/
│   │       ├── scenario_v1/                   (Legacy scenario generator)
│   │       └── scenario_v2/                   (Phase 11.4 Scenario V2 demand generator)
│   │           ├── generate_demand.py
│   │           └── materialize_odoo_orders.py
│   ├── tests/                                 (Automated Test Suites)
│   │   └── integration/
│   │       ├── test_odoo_xmlrpc_connection.py
│   │       └── test_portfolio_scope.py
│   └── tools/                                 (Standalone Diagnostic Tools)
│       ├── inspection/
│       │   └── inspect_data_mart_schema.py
│       ├── monitoring/
│       │   └── check_scenario_v2_progress.py
│       └── diagnostics/
│           ├── check_fields.py
│           ├── check_portfolio.py
│           ├── check_portfolio2.py
│           ├── check_sales.py
│           ├── check_xml_ids.py
│           ├── clear_assets.py
│           ├── find_id1_xml.py
│           ├── gate1_sales_pilot.py
│           ├── query_dashboard.py
│           ├── reconcile_transacted.py
│           ├── test_granularity.py
│           ├── test_pivot_dump.py
│           ├── test_pivot5_evaluation.py
│           ├── test_positional.py
│           └── verify_gate1.py
├── PowerBI/
│   └── Odoo DSS_Arilano Excelovell Pinem_2304140070.pbix (Power BI Desktop Report)
├── scripts/                                   (Governance & Maintenance Scripts)
│   ├── configure_repository_remotes.ps1       (PowerShell remote configuration script)
│   ├── validate_repository_identity.ps1       (Repository attribution validator script)
│   ├── scan_repository_inventory.py           (Repository scanner)
│   ├── execute_phase1a.py                     (Phase 1A migration script)
│   ├── execute_phase1a_preconditions.py       (Phase 1A precondition inspector)
│   ├── execute_comprehensive_deep_scan_and_cleanup.py (Deep scan & cleanup engine)
│   ├── verify_and_generate_final_reports.py   (Final report generator)
│   ├── master_repository_restructure.py       (Master restructuring engine)
│   ├── run_deep_analysis_scan.py              (Metric scanner)
│   ├── update_odoo_conf.ps1                   (Odoo configuration updater)
│   └── scratch_sync.bat                       (Scratch sync utility)
├── .env.example                               (Environment variable template)
├── .gitignore                                 (Git untracked exclusions)
├── CHANGELOG.md                               (Project version history)
├── CITATION.cff                               (Citation metadata)
├── NOTICE                                     (Legal copyright attribution)
├── README.md                                  (Main repository README)
├── SECURITY.md                                (Vulnerability reporting policy)
├── odoo.conf                                  (Main Odoo configuration - Port 8069)
└── clone_odoo.conf                            (Clone Odoo configuration - Port 8070)
```

---

## 2. DETAILED RESTRUCTURING SUMMARY

### A. Cleaning of `docs/` Directory
- All 13 legacy phase subfolders (`phase8`, `phase9`, `phase10`, `phase11`, `phase11_0`, `phase11_1`, `phase11_2`, `phase11_2_execution`, `phase11_2_live`, `phase11_2_primary`, `phase11_2_programmatic`, `phase11_2_repair`, `phase11_2_revision`) have been moved out of `docs/` into `archive/deletion_review/markdown/`.
- `docs/` now contains **ONLY** professional Markdown documentation (`ARCHITECTURE.md`, `SETUP.md`, `OPERATIONS.md`, `DATA_PIPELINE.md`, `POWERBI_MODEL.md`, `REPOSITORY_GOVERNANCE.md`) and structured historical TXT records under `docs/history/`.

### B. Cleaning of Root Directory
- All loose diagnostic/validation scripts in root have been organized into `ERP-BIDSS/tools/diagnostics/`.
- All helper/governance/utility scripts in root have been organized into `scripts/`.
- All audit reports, inventory scans, logs, and screenshots have been organized into `audits/`.

### C. System Baseline Reconciliation
- **PostgreSQL Row Counts**: `sale_order = 1456`, `sale_order_line = 9792`, `fact_sales = 7618`, `fact_forecast_model_comparison = 17280`, `fact_forecast_monthly = 2880` (100% MATCH).
- **Power BI SHA-256 Hash**: `2250127b86dfcb6ecf5e3aa6270dc444625035c4b14447b0f385ff4ff88178bf` (100% MATCH).
