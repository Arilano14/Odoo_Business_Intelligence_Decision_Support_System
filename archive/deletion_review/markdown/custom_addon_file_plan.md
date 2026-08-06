# Custom Addon File Plan — Phase 11.2

**Date:** August 4, 2026  
**Status:** **FILE SPECIFICATION APPROVED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)  
**Target Addon Path:** `custom_addons/obidss_operational_bi/`

---

## 1. Directory Structure

```text
custom_addons/obidss_operational_bi/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── obidss_data_quality.py
├── views/
│   ├── menu_restructure.xml
│   ├── obidss_data_quality_views.xml
│   └── obidss_menus.xml
├── security/
│   ├── security_groups.xml
│   └── ir.model.access.csv
└── README.md
```

---

## 2. Detailed File Action Plan

| File Path | Exists Now | Action | Purpose & Technical Content | Dependency | Validation System |
|---|---|---|---|---|---|
| `__manifest__.py` | Yes | **MODIFY** | Updated manifest dependencies (`base`, `web`, `sale_management`, `purchase`, `stock`, `account`, `spreadsheet_dashboard`) and data order | Odoo Core | CLI Module Install Test |
| `__init__.py` | Yes | **MODIFY** | Import `models` directory | `__manifest__.py` | Python Import Check |
| `models/__init__.py` | Yes | **MODIFY** | Import `obidss_data_quality` model | `__init__.py` | Python Import Check |
| `models/obidss_data_quality.py` | Yes | **MODIFY** | SQL View model `obidss.data.quality` (`_auto = False`) comparing Odoo tables vs schema `mart` | SQLAlchemy / psycopg2 | DB View Existence |
| `security/security_groups.xml` | Yes | **MODIFY** | Defines 7 security groups (`group_obidss_user`, `sales`, `purchase`, `inventory`, `finance`, `reviewer`, `admin`) | `base` | XML Parsing & Group Test |
| `security/ir.model.access.csv` | Yes | **MODIFY** | Access rules for `obidss.data.quality` model across all 7 groups | `security_groups.xml` | ORM Permission Test |
| `views/menu_restructure.xml` | No | **CREATE [NEW]** | Reparents OBIDSS dashboards under `Dashboards` app (ID 177) and restricts launcher apps (`Discuss`, `Mass Mailing`, `Survey`, `HR`) | `security_groups.xml` | Menu Tree Verification |
| `views/obidss_menus.xml` | Yes | **MODIFY** | Defines live operational views for Sales, Purchase, Inventory, Finance, & Data Quality | `menu_restructure.xml` | XML ID & Action Check |
| `views/obidss_data_quality_views.xml` | Yes | **MODIFY** | Tree & Form view for data quality reconciliation bridge | `obidss_data_quality.py` | View Validation |
| `README.md` | No | **CREATE [NEW]** | Technical documentation & deployment instructions for Phase 11.2 | None | Documentation Audit |
