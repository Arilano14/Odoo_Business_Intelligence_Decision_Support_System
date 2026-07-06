# Validation Report — Phase 5 Analytics Mart

## Self-Review Checklist

---

## TAG-P5-01 — Analytics Mart Scope

**Status: ✅ PASS**

**Evidence:**
- Dimension tables: 6 (dim_date, dim_product, dim_customer, dim_vendor, dim_company, dim_warehouse)
- Fact tables: 4 (fact_sales, fact_purchase, fact_inventory, fact_accounting)
- Total: 10 tables, sesuai target
- Tidak ada tabel di luar scope (tidak ada fact_forecast, fact_decision_support, atau tabel lain)
- DDL terdokumentasi di `backend/database/ddl/dimension.sql` dan `backend/database/ddl/fact.sql`

**Perlu Revisi:** Tidak

---

## TAG-P5-02 — Grain Validation

**Status: ✅ PASS**

**Evidence:**
| Fact | Grain | Odoo Source | Consistent? |
| :--- | :--- | :--- | :---: |
| fact_sales | 1 row = 1 sale_order_line | sale_order_line (confirmed) | ✅ |
| fact_purchase | 1 row = 1 purchase_order_line | purchase_order_line (confirmed) | ✅ |
| fact_inventory | 1 row = 1 stock_move | stock_move (done) | ✅ |
| fact_accounting | 1 row = 1 account_move_line | account_move_line (posted) | ✅ |

- Grain didokumentasikan di `docs/phase5/grain_definition.md`
- Setiap grain memiliki business meaning yang jelas

**Perlu Revisi:** Tidak

---

## TAG-P5-03 — Relationship Validation

**Status: ✅ PASS**

**Evidence:**
- 13 FK relationships terdefinisi di `backend/database/ddl/relationship.sql`
- Semua bertipe Many-to-One (Fact → Dimension)
- Tidak ada Fact-to-Fact relationship
- Validator script tersedia di `backend/analytics/build_relationship.py`
- Query orphan-key check tersedia untuk setiap FK

**Perlu Revisi:** Tidak

---

## TAG-P5-04 — Data Dictionary

**Status: ✅ PASS**

**Evidence:**
- Dimension Dictionary: `docs/phase5/dimension_dictionary.md` — 6 tabel, semua kolom memiliki nama, tipe data, deskripsi, dan Power BI role.
- Fact Dictionary: `docs/phase5/fact_dictionary.md` — 4 tabel, semua kolom memiliki nama, tipe data, FK reference, deskripsi, dan flag derived/direct.

**Perlu Revisi:** Tidak

---

## TAG-P5-05 — Business Consistency

**Status: ✅ PASS**

**Evidence:**
- Studi kasus: PT Prima Alat Nusantara (distributor alat berat)
- Modul ERP: Sales, Purchase, Inventory, Accounting — sesuai scope
- dim_product: menyimpan list_price (harga jual) dan standard_price (harga pokok) — sesuai Odoo
- dim_customer: menyimpan industry — sesuai segmen B2B (Konstruksi, Pertambangan, Perkebunan)
- dim_vendor: menyimpan vendor_name dan city — sesuai kebutuhan Supplier Performance
- fact_purchase: menyimpan lead_time_days — sesuai kebutuhan KPI Supplier
- Tidak ada atribut yang bertentangan dengan skenario bisnis

**Perlu Revisi:** Tidak

---

## TAG-P5-06 — KPI Readiness

**Status: ✅ PASS**

**Evidence:**

| KPI | Dapat dihitung dari mart? | Source |
| :--- | :---: | :--- |
| Revenue | ✅ | SUM(fact_sales.revenue) |
| Sales Growth | ✅ | fact_sales.revenue by dim_date.month |
| Inventory Turnover | ✅ | SUM(fact_sales.cost) / AVG(fact_inventory.value) |
| DIO | ✅ | (AVG inventory / COGS) × 365 |
| Revenue Contribution | ✅ | fact_sales.revenue per product / total |
| Inventory Value | ✅ | SUM(fact_inventory.value) WHERE incoming |
| Purchase Value | ✅ | SUM(fact_purchase.subtotal) |
| Purchase Growth | ✅ | fact_purchase.subtotal by dim_date.month |
| ROP | ✅ | AVG(fact_sales.quantity/day) × lead_time |
| EOQ | ✅ | √(2DS/H) dari fact_sales aggregation |
| Supplier Score | ✅ | fact_purchase by dim_vendor + lead_time_days |
| Demand Forecast | ✅ | MA3 on fact_sales monthly qty |

- Sample queries di `backend/database/ddl/sample_query.sql` membuktikan semua KPI executable
- Tidak perlu kembali ke tabel transaksi Odoo

**Perlu Revisi:** Tidak

---

## TAG-P5-07 — Magang S1 Compliance

**Status: ✅ PASS**

**Evidence:**
- Star Schema sederhana (4 fact + 6 dim) — bukan enterprise DW
- Tidak menggunakan: Snowflake, Galaxy, Bridge Table, SCD Type 2, OLAP Cube, CDC, Partition, Materialized View
- SCD Type 1 (overwrite) — sesuai MVP
- Full refresh strategy — sederhana dan cukup untuk ~30.000 rows
- Python + Pandas + SQLAlchemy — stack standar yang dipahami mahasiswa S1
- Total kode Python: ~400 baris — realistis untuk magang

**Perlu Revisi:** Tidak

---

## TAG-P5-08 — Product Integration

**Status: ✅ PASS**

**Evidence:**
- Analytics Mart mengambil data dari tabel Odoo 18 yang merupakan output dari implementasi ERP (Product 1)
- `extract.py` menggunakan SQL query terhadap tabel Odoo asli: sale_order, purchase_order, stock_move, account_move
- Hubungan: Product 1 (ERP Implementation) → Data Operasional → ETL → Analytics Mart (Product 2)
- Dashboard (Phase 8) akan mengonsumsi data dari mart ini, bukan langsung dari Odoo
- Narasi konsisten: dashboard merupakan luaran lanjutan dari implementasi ERP

**Perlu Revisi:** Tidak

---

## Summary

| TAG | Status | Catatan |
| :---: | :--- | :--- |
| P5-01 | ✅ PASS | 6 Dim + 4 Fact, tidak ada tabel di luar scope |
| P5-02 | ✅ PASS | Grain jelas dan konsisten dengan Odoo |
| P5-03 | ✅ PASS | 13 FK, validator script tersedia |
| P5-04 | ✅ PASS | Data dictionary lengkap |
| P5-05 | ✅ PASS | Konsisten dengan studi kasus |
| P5-06 | ✅ PASS | 12/12 KPI dapat dihitung dari mart |
| P5-07 | ✅ PASS | Realistis untuk magang S1 |
| P5-08 | ✅ PASS | Product 1 → Product 2 terhubung |

**Keputusan: Phase 5 SELESAI — siap masuk Phase 6 (Business Intelligence & KPI Development).**
