# KPI Reconciliation Report — Phase 11.2 Stage 2A

**Date:** August 4, 2026  
**Status:** **100% RECONCILED ON CLONE**  
**Target Environment:** Clone Database `Business_Intelegent_Project_v2_phase11_2_clone`

---

## 1. Truth Query vs Dashboard Value Reconciliation

| KPI Business Name | Source Truth SQL Query | Source Truth Value | Dashboard Display Value | Difference | Status |
|---|---|---|---|---|---|
| **Confirmed Sales Revenue** | `SELECT SUM(amount_total) FROM sale_order WHERE company_id = 2 AND state = 'sale'` | Rp 17,552,025,691.43 | Rp 17,552,025,691.43 | Rp 0.00 | **PASS** |
| **Confirmed Purchase Value** | `SELECT SUM(amount_total) FROM purchase_order WHERE company_id = 2 AND state = 'purchase'` | Rp 30,088,422,406.50 | Rp 30,088,422,406.50 | Rp 0.00 | **PASS** |
| **Confirmed SO Count** | `SELECT COUNT(*) FROM sale_order WHERE company_id = 2 AND state = 'sale'` | 677 Orders | 677 Orders | 0 | **PASS** |
| **Confirmed PO Count** | `SELECT COUNT(*) FROM purchase_order WHERE company_id = 2 AND state = 'purchase'` | 225 Orders | 225 Orders | 0 | **PASS** |
| **Total SOs (All States)** | `SELECT COUNT(*) FROM sale_order WHERE company_id = 2` | 740 Orders | 740 Orders | 0 | **PASS** |
| **Total POs (All States)** | `SELECT COUNT(*) FROM purchase_order WHERE company_id = 2` | 251 Orders | 251 Orders | 0 | **PASS** |
| **Internal Transfers** | `SELECT COUNT(DISTINCT picking_id) FROM stock_move WHERE company_id = 2 AND ...` | 24 Transfers | 24 Transfers | 0 | **PASS** |
| **Scrap Operations** | `SELECT COUNT(*) FROM stock_scrap WHERE company_id = 2` | 12 Scraps | 12 Scraps | 0 | **PASS** |
| **Active Portfolio Products** | `SELECT COUNT(*) FROM product_product pp JOIN product_template pt ...` | 96 Variants | 96 Variants | 0 | **PASS** |
