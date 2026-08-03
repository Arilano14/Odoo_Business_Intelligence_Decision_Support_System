# Module & Model Inventory Report — Phase 11.1

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## 1. Custom Addon Inventory

- **Addon Name**: `obidss_operational_bi`
- **Location**: `custom_addons/obidss_operational_bi/`
- **License**: LGPL-3
- **Dependencies**: `base`, `web`, `sale_management`, `purchase`, `stock`, `account`, `spreadsheet_dashboard`

---

## 2. Models Inventory

| Model Name | Model Type | Purpose | Access Groups |
|---|---|---|---|
| `obidss.data.quality` | SQL View (`_auto = False`) | Real-time reporting bridge for Odoo source vs DW schema `mart` reconciliation | `group_obidss_reviewer`, `group_obidss_admin` |
| `sale.order` | Odoo Native Model | Source for Confirmed Sales Value & Order Count | `group_obidss_user` |
| `purchase.order` | Odoo Native Model | Source for Confirmed Purchase Value, PO Count & Lead Times | `group_obidss_user` |
| `stock.move` | Odoo Native Model | Source for Inventory Movements, Transfers & Scrap | `group_obidss_user` |
| `account.move` | Odoo Native Model | Source for Invoices & Vendor Bills | `group_obidss_manager` |
