# Business Traceability Matrix

Matriks ini memastikan setiap elemen Business Intelligence (Dashboard, KPI, Rekomendasi) dapat dilacak balik (*traceable*) secara eksplisit mulai dari masalah bisnis yang mendasarinya, transaksi sistem ERP yang merekamnya, hingga keputusan manajerial yang harus diambil. 

Ini adalah penghubung utama antara **Product 1 (Laporan Implementasi ERP)** dan **Product 2 (Business Intelligence)**.

## 1. Flow: Mengatasi Keterlambatan Rantai Pasok

```mermaid
graph TD
    A[Business Problem: Supplier Sering Terlambat] --> B[ERP Transaction: purchase_order]
    B --> C[Analytics Mart: fact_purchase]
    C --> D[KPI: Lead Time & Fulfillment Rate]
    D --> E[Dashboard: Purchase Dashboard]
    E --> F[Recommendation: Supplier Score < 70]
    F --> G[Business Decision: Review & Ganti Supplier]
```

## 2. Flow: Mencegah Kehabisan Stok (Stockout)

```mermaid
graph TD
    A[Business Problem: Kehabisan Stok Tiba-Tiba] --> B[ERP Transaction: sale_order & stock_move]
    B --> C[Analytics Mart: fact_sales & fact_inventory]
    C --> D[KPI: Daily Demand & Stock Availability]
    D --> E[Dashboard: Inventory Dashboard]
    E --> F[Recommendation: Current Stock <= ROP]
    F --> G[Business Decision: Buat Draft PO Baru]
```

## 3. Flow: Mengatasi Penumpukan Barang (Overstock)

```mermaid
graph TD
    A[Business Problem: Penumpukan Barang di Gudang] --> B[ERP Transaction: stock_move & purchase_order]
    B --> C[Analytics Mart: fact_inventory & fact_purchase]
    C --> D[KPI: Inventory Turnover & DIO]
    D --> E[Dashboard: Inventory Dashboard]
    E --> F[Recommendation: Slow Moving Product]
    F --> G[Business Decision: Tunda Pembelian & Buat Promosi]
```

## 4. Flow: Memprediksi Permintaan Pasar

```mermaid
graph TD
    A[Business Problem: Fluktuasi Pendapatan Sulit Ditebak] --> B[ERP Transaction: sale_order_line]
    B --> C[Analytics Mart: fact_sales]
    C --> D[KPI: Revenue Trend & Demand Forecast]
    D --> E[Dashboard: Executive & Sales Dashboard]
    E --> F[Recommendation: Forecast Error Check]
    F --> G[Business Decision: Sesuaikan Safety Stock & Target Sales]
```

---

## Analisis Lapisan (Layer Analysis)

Traceability Matrix di atas menegaskan pembagian kerja teknis yang telah kita terapkan:

1. **ERP Output (Odoo) $\rightarrow$ ETL Output (Analytics Mart):**
   *(Phase 5 - Data Engineering)* Mengekstrak transaksi *raw* Odoo menjadi struktur *Fact* dan *Dimension*.
2. **Algoritma / Rekomendasi (DSS):**
   *(Phase 6 - Python Analytics)* Menghitung logika *prescriptive* (EOQ, ROP, MA3, Supplier Score). Parameter tingkat lanjut yang terlalu berat jika dihitung secara dinamis hanya menggunakan rumus BI biasa.
3. **Dashboard & KPI Dasar:**
   *(Phase 7 - Power BI)* Menyajikan agregasi visual interaktif (Sales, Growth, Margin) melalui DAX untuk konsumsi manajemen puncak.
