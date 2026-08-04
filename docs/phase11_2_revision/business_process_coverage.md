# Business Process Coverage & KPI Feasibility Audit — Phase 11.2 Revision

**Date:** August 4, 2026  
**Status:** **COVERAGE AUDITED**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Process Coverage & Availability Matrix

| Business Process Area | Expected Records | Actual Valid Records | Coverage Ratio | Available Operational KPIs | KPI Feasibility Status |
|---|---:|---:|---:|---|---|
| **Sales Operations** | 720 SOs | **740 SOs** (677 Confirmed) | 100.0% | Confirmed Sales Value, SO Count, Monthly Sales Trend, Top Products, Top Customers | **AVAILABLE** |
| **Purchase & Procurement** | 240 POs | **251 POs** (225 Confirmed) | 100.0% | Confirmed Purchase Value, PO Count, Top Suppliers, Planned/Actual Lead Time | **AVAILABLE** |
| **Inventory & Warehouse** | 24 INT / 12 SCRAP | **24 INT / 12 SCRAP / 3,081 Moves** | 100.0% | On-Hand Quantity, Stock Movements, Internal Transfers, Scrap Quantity | **AVAILABLE** |
| **Finance & Invoicing** | 740 Invoices | **Unposted Journal Entries** | 30.0% | Customer Invoices, Vendor Bills, Payment Status | **AVAILABLE WITH LIMITATIONS** |

---

## 2. Decision Rule for Finance Dashboard

* **Audit Finding**: Customer Invoices and Vendor Bills exist in `account.move` but accounting journal entry posting depends on standard Odoo workflow execution.
* **Decision**: Enable Finance & Invoicing dashboard **with limitations** (showing real unposted/posted draft move counts) or restrict visibility to `group_obidss_finance` users, without generating fake accounting data.
