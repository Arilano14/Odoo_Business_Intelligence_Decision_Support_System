# Dashboard Identity Reconciliation Report — Phase 11.0

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)  
**Database:** `Business_Intelegent_Project_v2`

---

## 1. Discrepancy Reconciliation Matrix

| Evidence Source | Database Name | Dashboard ID | Name | Exists in DB Now | XML ID | Owning Module | Explanation |
|---|---|---:|---|---|---|---|---|
| **RPC Error Traceback** | Legacy / Past Run | 8 | Unknown / Non-existent | **No** | None | Unknown | Record ID 8 was an artifact from a past legacy Odoo instance or pre-reset database build prior to Phase 8 cleanup. It does not exist in current `Business_Intelegent_Project_v2`. |
| **Browser URL Parameter** | `Business_Intelegent_Project_v2` | 3 | Sales | **Yes** | `spreadsheet_dashboard_sales` | `spreadsheet_dashboard_sale` | Active dashboard record for Sales Dashboard in current database. |
| **Database Audit (PostgreSQL)** | `Business_Intelegent_Project_v2` | 1 | Invoicing | **Yes** | `dashboard_invoicing` | `spreadsheet_dashboard_account` | Active record ID 1 for Invoicing Dashboard. |
| **Database Audit (PostgreSQL)** | `Business_Intelegent_Project_v2` | 2 | Warehouse Metrics | **Yes** | `spreadsheet_dashboard_warehouse_metrics` | `spreadsheet_dashboard_stock_account` | Active record ID 2 for Warehouse Metrics Dashboard. |
| **Database Audit (PostgreSQL)** | `Business_Intelegent_Project_v2` | 3 | Sales | **Yes** | `spreadsheet_dashboard_sales` | `spreadsheet_dashboard_sale` | Active record ID 3 for Sales Dashboard. |
| **Database Audit (PostgreSQL)** | `Business_Intelegent_Project_v2` | 4 | Product | **Yes** | `spreadsheet_dashboard_product` | `spreadsheet_dashboard_sale` | Active record ID 4 for Product Dashboard. |

---

## 2. Findings & Resolution

1. **Absence of ID 8**: Database queries on `spreadsheet_dashboard` and `ir_model_data` confirm 0 records exist with ID 8 (`SELECT * FROM spreadsheet_dashboard WHERE id=8` returns 0 rows).
2. **Active Canonical Records**: The current database contains exactly **4 active records** (IDs 1, 2, 3, 4).
3. **Resolution**: Recovery and rehearsal actions will focus exclusively on active records IDs 1, 2, 3, and 4. ID 8 is resolved as a stale historical error reference.
