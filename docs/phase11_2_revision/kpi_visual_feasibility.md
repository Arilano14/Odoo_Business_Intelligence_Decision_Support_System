# KPI & Visual Feasibility Contract — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **FEASIBILITY AUDITED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Feasibility Audit Matrix

| Dashboard Area | KPI Name | Source Model | Required Fields | Data Available in DB | Limitation / Notes | Feasibility Decision |
|---|---|---|---|---|---|---|
| **Executive** | Confirmed Sales Value | `sale.order` | `amount_total`, `state`, `company_id` | 🟢 Yes | `state = 'sale'` (677 SOs, Rp 17.55B) | **APPROVED** |
| **Executive** | Confirmed Purchase Value | `purchase.order` | `amount_total`, `state`, `company_id` | 🟢 Yes | `state = 'purchase'` (225 POs, Rp 30.08B) | **APPROVED** |
| **Executive** | SO Count | `sale.order` | `id`, `company_id` | 🟢 Yes | 740 Total SOs in DB | **APPROVED** |
| **Executive** | PO Count | `purchase.order` | `id`, `company_id` | 🟢 Yes | 251 Total POs in DB | **APPROVED** |
| **Sales** | Average Order Value | `sale.order` | `amount_total`, `state` | 🟢 Yes | Calculated as Total Revenue / Confirmed SO Count | **APPROVED** |
| **Sales** | Cancelled SO Rate | `sale.order` | `state` | 🟢 Yes | 29 Cancelled SOs / 740 Total SOs (3.92%) | **APPROVED** |
| **Purchase** | Planned Lead Time | `purchase.order` | `date_planned`, `date_order` | 🟢 Yes | Average 14.2 Days | **APPROVED** |
| **Purchase** | Actual Lead Time | `stock.move` + `purchase.order` | Receipt Date - Approval Date | 🟢 Yes | Calculated from completed stock receipts | **APPROVED** |
| **Inventory** | On-Hand Quantity | `stock.quant` | `quantity`, `location_id` | 🟢 Yes | 283 Product Variants | **APPROVED** |
| **Inventory** | Internal Transfers | `stock.move` | `picking_type_id.code` | 🟢 Yes | 24 Internal Transfers | **APPROVED** |
| **Inventory** | Scrap Quantity | `stock.scrap` | `scrap_qty` | 🟢 Yes | 12 Scrap Operations | **APPROVED** |
| **Finance** | Posted Invoice Value | `account.move` | `amount_total`, `state` | 🟡 Partial | Pending journal entry posting status | **CONDITIONALLY APPROVED** |
