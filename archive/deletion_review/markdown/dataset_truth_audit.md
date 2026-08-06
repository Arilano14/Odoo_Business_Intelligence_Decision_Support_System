# Dataset Truth Audit Report — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **READ-ONLY DATASET TRUTH AUDITED & VERIFIED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)  
**Database:** `Business_Intelegent_Project_v2`

---

## 1. Executive Summary & Authoritative Dataset Counts

An empirical read-only audit of the PostgreSQL database `Business_Intelegent_Project_v2` was conducted to resolve all discrepancies between initial contract targets and actual database counts.

| Entity Name | Original Target | Database Total | Valid Portfolio Total | Excluded / Non-Portfolio | Unknown / Under Review | Explanation & Audit Status |
|---|---:|---:|---:|---:|---:|---|
| **Sales Orders (SO)** | 720 Orders | **740 Orders** | **677 Confirmed SOs** | 63 (33 Drafts, 29 Cancelled, 1 Sent) | 0 | **RESOLVED**: 740 is the database total across ALL order states (`sale` = 677, `draft` = 33, `cancel` = 29, `sent` = 1). Confirmed portfolio sales total Rp 17.55B across 677 orders. |
| **Purchase Orders (PO)** | 240 Orders | **251 Orders** | **225 Confirmed POs** | 26 (16 Drafts, 9 Cancelled, 1 Sent) | 0 | **RESOLVED**: 251 is the database total across ALL PO states (`purchase` = 225, `draft` = 16, `cancel` = 9, `sent` = 1). Confirmed portfolio purchases total Rp 30.08B across 225 orders. |
| **Product Templates** | 240 Templates | **277 Templates** | **96 Portfolio Templates** | 181 Default Odoo Templates | 0 | **RESOLVED**: 277 total active templates exist, of which 96 belong specifically to the heavy equipment & consumables portfolio and 181 to base Odoo modules. |
| **Product Variants** | 283 Variants | **283 Variants** | **96 Portfolio Variants** | 187 Default Odoo Variants | 0 | **RESOLVED**: 283 total active product variants exist in `product_product`. |
| **Portfolio Customers** | 48 Customers | **48 Customers** | **48 Customers** | 0 | 0 | **EXACT MATCH (100%)** |
| **Portfolio Vendors** | 24 Suppliers | **24 Suppliers** | **24 Suppliers** | 0 | 0 | **EXACT MATCH (100%)** |
| **Internal Transfers** | 24 Transfers | **24 Transfers** | **24 Transfers** | 0 | 0 | **EXACT MATCH (100%)** |
| **Scrap Operations** | 12 Scraps | **12 Scraps** | **12 Scraps** | 0 | 0 | **EXACT MATCH (100%)** |

---

## 2. Sales Order Breakdown by State & Pattern

```sql
SELECT state, COUNT(*), SUM(amount_total) 
FROM sale_order 
WHERE company_id = 2 
GROUP BY state;
```

* `state = 'sale'` (Confirmed Orders): **677 Orders** | Subtotal: **Rp 17,552,025,691.43**
* `state = 'draft'` (Quotations): **33 Orders** | Subtotal: **Rp 755,771,465.12**
* `state = 'cancel'` (Cancelled Orders): **29 Orders** | Subtotal: **Rp 604,307,965.87**
* `state = 'sent'` (Sent Quotations): **1 Order** | Subtotal: **Rp 1,740.00**
* **Total Database Sales Orders**: **740 Orders**

---

## 3. Purchase Order Breakdown by State & Pattern

```sql
SELECT state, COUNT(*), SUM(amount_total) 
FROM purchase_order 
WHERE company_id = 2 
GROUP BY state;
```

* `state = 'purchase'` (Confirmed Orders): **225 Orders** | Subtotal: **Rp 30,088,422,406.50**
* `state = 'draft'` (RFQs / Drafts): **16 Orders** | Subtotal: **Rp 1,111,549,592.00**
* `state = 'cancel'` (Cancelled POs): **9 Orders** | Subtotal: **Rp 1,348,766,000.00**
* `state = 'sent'` (Sent RFQs): **1 Order** | Subtotal: **Rp 14,563.00**
* **Total Database Purchase Orders**: **251 Orders**
