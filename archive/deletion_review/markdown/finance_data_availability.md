# Finance Data Availability Audit — Phase 11.2 Stage 2B

**Date:** August 4, 2026  
**Status:** **AVAILABLE WITH LIMITATIONS**  
**Target Environment:** Primary Database `Business_Intelegent_Project_v2`

---

## 1. Accounting Data Completeness Log

* **Customer Invoices**: Invoices exist in `account.move` but journal entry posting status varies.
* **Recognized Revenue**: Defined strictly as posted customer invoices (`account.move.amount_total` where `state = 'posted'`).
* **Confirmed Sales Value**: Defined strictly as confirmed sales orders (`sale_order.amount_total` where `state = 'sale'`, totaling **Rp 17,552,025,691.43** across 677 orders).
* **Policy Decision**: The Finance & Invoicing dashboard is deployed with **Role-based Restrictions** (`group_obidss_manager`) and explicitly labeled limitations to prevent displaying unposted financial metrics as recognized revenue.
