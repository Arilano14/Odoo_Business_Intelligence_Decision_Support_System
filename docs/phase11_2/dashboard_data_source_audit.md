# Dashboard Data Source Audit Report — Phase 11.2

**Date:** August 4, 2026  
**Status:** **READ-ONLY AUDIT PASSED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Existing Spreadsheet Dashboard Records Inventory

| Dashboard Name | ID | XML ID | Module Owner | Data Size | JSON Schema Status | Pivot Sources | List Sources | Hardcoded Sample Cells | Data Source Status |
|---|---:|---|---|---:|---|---|---|---|---|
| **Invoicing** | 1 | `spreadsheet_dashboard_account.spreadsheet_dashboard_invoicing` | `spreadsheet_dashboard_account` | 26,525 B | Valid Core Version 21 | `account.invoice.report` | None | Sample Mock Accounts | Contains Mock Sample Values |
| **Warehouse Metrics** | 2 | `spreadsheet_dashboard_stock_account.spreadsheet_dashboard_warehouse_metrics` | `spreadsheet_dashboard_stock_account` | 31,509 B | Valid Core Version 21 | `stock.valuation.layer` | None | Sample Mock Warehouse | Contains Mock Sample Values |
| **Sales** | 3 | `spreadsheet_dashboard_sale.spreadsheet_dashboard_sales` | `spreadsheet_dashboard_sale` | 37,291 B | Valid Core Version 21 | `sale.report` | None | Sample Mock Products | Contains Mock Sample Values |
| **Product** | 4 | `spreadsheet_dashboard_sale.spreadsheet_dashboard_product` | `spreadsheet_dashboard_sale` | 23,673 B | Valid Core Version 21 | `sale.report` | None | Sample Mock Items (Gaming Chair/Mouse) | Contains Mock Sample Values |

---

## 2. Visual-Level Diagnosis Matrix

| Dashboard | Visual Component | Data Type | Target Odoo Model | Domain Filter | Date Filter | Company Scope | Result Rows | Reason Blank / Sample Mock |
|---|---|---|---|---|---|---|---:|---|
| **Sales** | Top Quotations | Pivot | `sale.report` | `state IN ('draft', 'sent')` | Relative (`=TODAY()`) | `company_id = 1` | 0 | All FY 2026 orders are in `state = 'sale'` (confirmed) on `company_id = 2`. Filter returned 0 rows. |
| **Sales** | Top Orders | Pivot | `sale.report` | `state = 'sale'` | Relative (`=EDATE(TODAY(), -12)`) | Unassigned | 0 | Dates out of bounds (FY 2026 is fixed 2026-01-01 to 2026-12-31). Relative dates shifted query outside 2026. |
| **Product** | Best Seller | Hardcoded | None | None | None | None | 0 | Sample JSON contains hardcoded string `"GlideSync Wireless Mouse"`. Not in PT Prima Alat Nusantara database. |
| **Product** | Best Category | Hardcoded | None | None | None | None | 0 | Sample JSON contains hardcoded string `"TitanForge Gaming Chair"`. Not in heavy equipment portfolio. |
| **Invoicing** | Revenue Graph | Pivot | `account.invoice.report` | `state = 'posted'` | Relative (`=TODAY()`) | `company_id = 1` | 0 | Odoo standard invoices are unposted or locked to `company_id = 1`. |
| **Warehouse** | On-Hand Stock | Pivot | `stock.valuation.layer` | `quantity > 0` | Relative | `company_id = 1` | 0 | Stock moves for PT Prima Alat Nusantara are registered under `location_id.usage = 'internal'` for `company_id = 2`. |
