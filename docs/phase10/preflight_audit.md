# Phase 10 — Preflight Audit & Patch Plan

**Date:** August 3, 2026  
**Auditor:** Senior Python Data Engineer & Odoo ERP Data Architect  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)  
**Company:** PT Prima Alat Nusantara (Company ID: 2)

---

## 1. Executive Preflight Audit (Gate 10A)

### 1.1 Inspected Files

1. `ERP-BIDSS/backend/config/settings.py` — Pipeline configuration constants & DB URLs
2. `ERP-BIDSS/backend/config/database.py` — SQLAlchemy dual DB connection engines
3. `ERP-BIDSS/backend/etl/extract.py` — SQL extraction queries from Odoo 18 PostgreSQL
4. `ERP-BIDSS/backend/etl/transform.py` — Dimensional model builders (Kimball methodology)
5. `ERP-BIDSS/backend/etl/load.py` — Loader to schema `mart`
6. `ERP-BIDSS/backend/etl/pipeline.py` — End-to-end ETL orchestrator
7. `ERP-BIDSS/backend/run_etl.py` — CLI entry point
8. `ERP-BIDSS/backend/analytics/validate_mart.py` — Mart validation suite
9. `ERP-BIDSS/backend/database/ddl/` — Star schema DDL specifications

### 1.2 Audit of 2024 References

A codebase scan for `2024` identified the following classifications:

| File | Context | Classification | Action Required |
|---|---|---|---|
| `backend/etl/transform.py:19` | `build_dim_date(start="2024-01-01", end="2024-12-31")` | **Active Code** | **Must patch to 2026** |
| `backend/etl/pipeline.py:38` | `build_dim_date("2024-01-01", "2024-12-31")` | **Active Code** | **Must patch to 2026** |
| `backend/analytics/build_dimension.py:17` | `start="2024-01-01"` | Active Code (Analytics) | Deferred to Phase 11 |
| `backend/analytics/build_aggregation.py:251` | `data_period_start = '2024-01-01'` | Active Code (Agg) | Deferred to Phase 11 |
| `generate_extra_transactions_v2.py:12` | `Odoo 18.0.20241229` | Build Version String | Preserve as-is |
| `backend/scripts/dataset_generator.py:12` | `YEAR = 2024` | Legacy Generator | Preserve as legacy reference |
| `backend/odoo/cleanup_portfolio_data.py` | `date_order =like '2024%'` | Cleanup Utility | Preserve as cleanup pattern |
| `backend/validation/validate_phase8.py` | `Zero 2024/2026 Sales Orders` | Phase 8 Validator | Preserve as historical test |

### 1.3 Database Preflight Audit State

#### Odoo 18 Source DB (`Business_Intelegent_Project_v2`):
- **Authentication**: XML-RPC Auth OK (UID: 2)
- **Company**: 1 main company (`PT Prima Alat Nusantara`, ID: 2) + 1 default system company (`My Company (San Francisco)`, ID: 1)
- **Active Products**: 283 active product variants (240 portfolio templates + standard defaults)
- **Portfolio Customers** (`PORTFOLIO_2026_V1-CUST-%`): 48
- **Portfolio Vendors** (`PORTFOLIO_2026_V1-VEND-%`): 24
- **Sales Orders**: Total 720 (Confirmed `sale`: 662, `draft`: 29, `cancel`: 29)
- **Purchase Orders**: Total 242 (Confirmed `purchase`: 221, `draft`: 12, `cancel`: 9)
- **Stock Moves**: Done: 32, Assigned: 1,093, Confirmed: 1,956
- **SO Date Range**: `2026-01-01` to `2026-12-28`
- **PO Date Range**: `2026-01-01` to `2026-12-28`

#### Target Mart Schema (`mart`):
- Current tables: `[]` (Empty / Clean schema ready for initial FY 2026 load)

### 1.4 Detected Risks & Defect Analysis
1. **Hardcoded Company SK**: `transform.py` hardcodes `company_sk = 1` and `warehouse_id = 1` instead of extracting actual `company_id = 2` (`PT Prima Alat Nusantara`) and warehouse ID `2` (`PAN`).
2. **Hardcoded Date Range**: `transform.py` and `pipeline.py` generate `dim_date` for 2024 instead of FY 2026 (`2026-01-01` to `2026-12-31`).
3. **Extraction Filters**: Queries in `extract.py` filter `so.state = 'sale'` and `po.state = 'purchase'`, but do not explicitly scope `company_id = 2` or portfolio partner references (`PORTFOLIO_2026_V1-CUST-%` / `PORTFOLIO_2026_V1-VEND-%`), risking cross-company or legacy data pull if present.
4. **Account Move Coverage**: `account_move` has 0 posted records in current phase dataset. `fact_accounting` builder must handle empty DataFrame gracefully without failing pipeline.

---

## 2. Configuration & Patch Plan (Gate 10B)

### 2.1 Centralized Configuration Source of Truth

We will add centralized period and company parameters in `ERP-BIDSS/backend/config/settings.py`:

```python
ANALYSIS_START_DATE = os.getenv("ANALYSIS_START_DATE", "2026-01-01")
ANALYSIS_END_DATE = os.getenv("ANALYSIS_END_DATE", "2026-12-31")
TARGET_COMPANY_ID = int(os.getenv("TARGET_COMPANY_ID", "2"))
CUSTOMER_REF_PREFIX = os.getenv("CUSTOMER_REF_PREFIX", "PORTFOLIO_2026_V1-CUST-")
VENDOR_REF_PREFIX = os.getenv("VENDOR_REF_PREFIX", "PORTFOLIO_2026_V1-VEND-")
```

### 2.2 File-by-File Patch Plan

#### File 1: `ERP-BIDSS/backend/config/settings.py`
- **Current Issue**: Lacks centralized FY 2026 analysis dates, company ID, and partner ref prefixes.
- **Required Change**: Add `ANALYSIS_START_DATE`, `ANALYSIS_END_DATE`, `TARGET_COMPANY_ID`, `CUSTOMER_REF_PREFIX`, `VENDOR_REF_PREFIX`.
- **Validation Method**: Import settings in python and verify values.

#### File 2: `ERP-BIDSS/backend/etl/extract.py`
- **Current Issue**: Queries lack company scope (`company_id = 2`) and explicit partner ref filtering.
- **Required Change**: 
  - Parameterize/filter queries with `company_id = settings.TARGET_COMPANY_ID`.
  - Filter customer query: `customer_rank > 0 AND ref LIKE 'PORTFOLIO_2026_V1-CUST-%'`.
  - Filter vendor query: `supplier_rank > 0 AND ref LIKE 'PORTFOLIO_2026_V1-VEND-%'`.
  - Filter warehouse query: `sw.company_id = settings.TARGET_COMPANY_ID`.
  - Filter company query: `rc.id = settings.TARGET_COMPANY_ID`.
- **Validation Method**: Test extraction functions and check DataFrame lengths & company IDs.

#### File 3: `ERP-BIDSS/backend/etl/transform.py`
- **Current Issue**:
  1. `build_dim_date` defaults to `2024-01-01` – `2024-12-31`.
  2. Fact builders use hardcoded `company_id = 1` or `warehouse_id = 1`.
  3. `build_fact_inventory` does not map actual `warehouse_id` from stock move/warehouse lookup.
- **Required Change**:
  1. Default `start` and `end` in `build_dim_date` to `settings.ANALYSIS_START_DATE` and `settings.ANALYSIS_END_DATE`.
  2. Map `company_id` from source `odoo_company_id` using `dim_company` surrogate key lookup.
  3. Map `warehouse_id` from source warehouse lookup.
- **Validation Method**: Inspect transformed DataFrames for surrogate keys and min/max date_ids.

#### File 4: `ERP-BIDSS/backend/etl/pipeline.py`
- **Current Issue**: Explicitly passes `"2024-01-01", "2024-12-31"` to `build_dim_date`.
- **Required Change**: Pass `settings.ANALYSIS_START_DATE, settings.ANALYSIS_END_DATE` or use defaults.
- **Validation Method**: Run pipeline and check `dim_date` row count equals 365 (FY 2026).

#### File 5: `ERP-BIDSS/backend/validation/validate_phase10.py`
- **Current Issue**: File does not exist yet.
- **Required Change**: Create comprehensive automated validation script checking 12 mandatory criteria.
- **Validation Method**: Execute `python backend/validation/validate_phase10.py` and verify zero errors (exit code 0).
