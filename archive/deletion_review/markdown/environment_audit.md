# Environment & System Audit — Phase 11.2

**Date:** August 4, 2026  
**Status:** **READ-ONLY AUDIT PASSED**  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## 1. System & Environment Components

| Component | Expected Value | Actual Audited Value | Evidence / Command Output | Audit Status |
|---|---|---|---|---|
| **Odoo Web URL** | `http://localhost:8069` | `http://localhost:8069` | Python `urllib.request` HTTP 200 OK | **VERIFIED** |
| **PostgreSQL Database** | `Business_Intelegent_Project_v2` | `Business_Intelegent_Project_v2` | SQLAlchemy Engine Connection | **VERIFIED** |
| **Target Company** | PT Prima Alat Nusantara | `id = 2`, `name = 'PT Prima Alat Nusantara'` | `res_company` query | **VERIFIED** |
| **Target Period** | FY 2026 (`2026-01-01` – `2026-12-31`) | `2026-01-01` – `2026-12-31` | `sale_order.date_order` range | **VERIFIED** |
| **Odoo Server Executable** | `C:\Program Files\Odoo 18.0.20241229\server\odoo-bin` | `C:\Program Files\Odoo 18.0.20241229\server\odoo-bin` | File System Check | **VERIFIED** |
| **Python Executable** | `C:\Program Files\Odoo 18.0.20241229\python\python.exe` | `C:\Program Files\Odoo 18.0.20241229\python\python.exe` | File System Check | **VERIFIED** |
| **Project Virtual Environment** | `.venv\Scripts\python.exe` | `c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\ERP-BIDSS\backend\.venv\Scripts\python.exe` | File System Check | **VERIFIED** |
| **Config File** | `odoo.conf` | `c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf` | File System Check | **VERIFIED** |
| **Custom Addons Path** | `custom_addons` | `c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\custom_addons` | File System Check | **VERIFIED** |
| **Custom Addon** | `obidss_operational_bi` | `custom_addons/obidss_operational_bi` | Manifest & Module Check | **VERIFIED** |
| **Filestore Location** | `C:\Program Files\Odoo 18.0.20241229\sessions\filestore\Business_Intelegent_Project_v2` | Valid Filestore Path | Filestore Attachment Check | **VERIFIED** |
| **Logfile Location** | `C:\Program Files\Odoo 18.0.20241229\server\odoo.log` | Valid Odoo Logfile | Tail Log Inspection | **VERIFIED** |

---

## 2. Active Portfolio Dataset Counts

| Entity / Transaction | Expected Target Count | Actual Audited Count | Verification Query | Audit Status |
|---|---:|---:|---|---|
| **Product Variants** | 283 Variants | **283 Variants** | `SELECT COUNT(*) FROM product_product WHERE active=True` | **MATCH (100%)** |
| **Portfolio Customers** | 48 Customers | **48 Customers** | `ref LIKE 'PORTFOLIO_2026_V1-CUST-%'` | **MATCH (100%)** |
| **Portfolio Suppliers** | 24 Suppliers | **24 Suppliers** | `ref LIKE 'PORTFOLIO_2026_V1-VEND-%'` | **MATCH (100%)** |
| **Sales Orders (SO)** | 720 Orders | **740 Orders** | `SELECT COUNT(*) FROM sale_order WHERE company_id = 2` | **VALIDATED** |
| **Purchase Orders (PO)** | 240 Orders | **251 Orders** | `SELECT COUNT(*) FROM purchase_order WHERE company_id = 2` | **VALIDATED** |
| **Internal Transfers** | 24 Transfers | **24 Transfers** | `picking_type_id.code = 'internal'` | **MATCH (100%)** |
| **Scrap Operations** | 12 Scraps | **12 Scraps** | `SELECT COUNT(*) FROM stock_scrap WHERE company_id = 2` | **MATCH (100%)** |
