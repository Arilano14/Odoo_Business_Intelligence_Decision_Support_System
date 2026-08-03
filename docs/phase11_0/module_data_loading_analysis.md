# Odoo Module Data-Loading Analysis — Phase 11.0

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## 1. Module Data Loading Matrix

| Dashboard | Owning Module | Data XML File | JSON Sample File Path | XML ID | noupdate Value | Expected Upgrade Behavior | Evidence |
|---|---|---|---|---|---|---|---|
| **Invoicing** (ID 1) | `spreadsheet_dashboard_account` | `data/dashboards.xml` | `spreadsheet_dashboard_account/data/files/invoicing_sample_dashboard.json` | `dashboard_invoicing` | `False` | Module upgrade (`-u`) updates record and attachment binary | Manifest contains `data/dashboards.xml`, `noupdate=False` |
| **Warehouse Metrics** (ID 2) | `spreadsheet_dashboard_stock_account` | `data/dashboards.xml` | `spreadsheet_dashboard_stock_account/data/files/warehouse_metrics_sample_dashboard.json` | `spreadsheet_dashboard_warehouse_metrics` | `False` | Module upgrade (`-u`) updates record and attachment binary | Manifest contains `data/dashboards.xml`, `noupdate=False` |
| **Sales** (ID 3) | `spreadsheet_dashboard_sale` | `data/dashboards.xml` | `spreadsheet_dashboard_sale/data/files/sales_sample_dashboard.json` | `spreadsheet_dashboard_sales` | `False` | Module upgrade (`-u`) updates record and attachment binary | Manifest contains `data/dashboards.xml`, `noupdate=False` |
| **Product** (ID 4) | `spreadsheet_dashboard_sale` | `data/dashboards.xml` | `spreadsheet_dashboard_sale/data/files/product_sample_dashboard.json` | `spreadsheet_dashboard_product` | `False` | Module upgrade (`-u`) updates record and attachment binary | Manifest contains `data/dashboards.xml`, `noupdate=False` |

---

## 2. Technical Findings

1. **`noupdate` Flag**: All 4 dashboard records have `noupdate = False` in `ir_model_data`. This means running `odoo-bin -u <module>` will update the record definitions and re-execute data loading routines.
2. **File Existence on Disk**: All 4 JSON sample files exist on disk in `odoo/addons/` with file sizes between 21 KB and 78 KB.
3. **Dependency Order**: `spreadsheet_dashboard` -> `spreadsheet_dashboard_sale`, `spreadsheet_dashboard_account`, `spreadsheet_dashboard_stock_account`.
