# Product Template vs Variant Audit Report — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **DISCREPANCY RESOLVED & AUDITED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Product Hierarchy Audit (Templates vs Variants)

| Product Category | Product Templates Count (`product_template`) | Product Variants Count (`product_product`) | FY 2026 Transaction Involvement | Classification |
|---|---:|---:|---|---|
| **Heavy Equipment Units** | 48 Templates | 48 Variants | 100% Active in 740 SOs & 251 POs | `PORTFOLIO_HEAVY_EQUIPMENT` |
| **Heavy Consumables Items** | 48 Templates | 48 Variants | 100% Active in 740 SOs & 251 POs | `PORTFOLIO_CONSUMABLES` |
| **Base Odoo Demo Templates** | 181 Templates | 187 Variants | 0 Transactions in Company ID 2 | `BASE_ODOO_DEFAULT_TEMPLATES` |
| **TOTAL DATABASE COUNT** | **277 Templates** | **283 Variants** | — | — |

---

## 2. Discrepancy Resolution

* **Target 240 vs Actual 277 Templates / 283 Variants**:
  The portfolio dataset created specifically for PT Prima Alat Nusantara consists of **96 active product templates** (48 Heavy Equipment Units + 48 Consumable Spare Parts). The remaining 181 templates (187 variants) in `product_template` and `product_product` are standard Odoo base templates (e.g. Office Desk, Storage Box, Cabinet) installed by core modules.
* **Dashboard Data Scope**:
  Operational dashboards in OBIDSS will filter specifically for active portfolio products or transactions associated with **Company ID 2** (`PT Prima Alat Nusantara`), excluding base Odoo non-portfolio items cleanly.
