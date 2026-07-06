# KPI Catalog (Phase 6)

Katalog ini merangkum seluruh KPI yang akan ditampilkan di Business Intelligence Dashboard, memisahkan logika kalkulasi antara algoritma Python (DSS Engine) dan Data Analysis Expressions (DAX) di Power BI.

## 1. Prescriptive Analytics (Python DSS)
Dihitung oleh script backend (`calculate_decision_support.py` & `calculate_supplier_score.py`) dan disimpan di tabel fakta (`fact_decision_support` dan `fact_supplier_score`).

| Metric Name | Formula / Logika | Tujuan Bisnis | Output Table |
| :--- | :--- | :--- | :--- |
| **Safety Stock** | `(Max Demand * Max Lead Time) - (Avg Demand * Avg Lead Time)` | Mengantisipasi lonjakan permintaan & keterlambatan supplier. | `fact_decision_support` |
| **Reorder Point (ROP)** | `(Avg Daily Demand * Avg Lead Time) + Safety Stock` | Menentukan titik kapan purchasing harus membuat PO baru. | `fact_decision_support` |
| **Economic Order Quantity (EOQ)** | `sqrt((2 * Annual Demand * Ordering Cost) / Holding Cost)` | Menentukan jumlah pesanan ideal yang menekan biaya total. | `fact_decision_support` |
| **Forecast (3-Month MA)** | Rata-rata pergerakan permintaan 3 bulan terakhir. | Mengatasi fluktuasi demand yang tidak terprediksi. | *Included in BI Dashboard directly or via Python* |
| **Supplier Score** | 40% Delivery + 30% Fulfillment + 20% Price + 10% Delay Freq | Mengevaluasi kinerja pemasok secara objektif. | `fact_supplier_score` |
| **Business Recommendation** | If-Else Logic berdasarkan threshold (e.g., *Reorder*, *Slow Moving*, *Review Supplier*). | Memberikan panduan aksi instan kepada eksekutif. | Keduanya |

## 2. Descriptive Analytics (Power BI / DAX)
Dihitung dinamis (On-the-fly) oleh Power BI ketika user berinteraksi dengan dashboard. Menggunakan layer semantik langsung dari Analytics Mart.

| Metric Name | DAX Formula (Simulasi) | Tujuan Bisnis | Dashboard |
| :--- | :--- | :--- | :--- |
| **Total Revenue** | `SUM('fact_sales'[total_revenue])` | Mengukur total pendapatan aktual. | Executive |
| **Total Margin (Rp)** | `SUM('fact_sales'[margin])` | Mengukur total keuntungan kotor. | Executive |
| **Revenue Growth (% MoM)** | `DIVIDE([Total Revenue] - [Prev Month Revenue], [Prev Month Revenue])` | Memantau laju pertumbuhan bulanan. | Executive |
| **Inventory Value** | `SUMX('fact_inventory', 'fact_inventory'[quantity] * 'dim_product'[standard_price])` | Menilai jumlah aset mengendap di gudang. | Inventory |
| **Days Inventory Outstanding (DIO)** | `365 / [Inventory Turnover]` | Rata-rata hari barang disimpan sebelum terjual. | Inventory |
| **Purchase Delay Rate** | `DIVIDE(CALCULATE(COUNTROWS('fact_purchase'), 'fact_purchase'[lead_time_days] > 5), COUNTROWS('fact_purchase'))` | % PO yang datang terlambat dari SLA. | Purchase |
| **Top 5 Slow Moving Product** | `TOPN(5, SUMMARIZE(dim_product...), [Inventory Turnover], ASC)` | Menemukan barang yang paling macet di gudang. | Inventory |

---
**Pemisahan Tanggung Jawab:**
* Power BI tidak menghitung EOQ atau ROP karena memakan resource CPU besar untuk kalkulasi kompleks iteratif dan tidak efisien ditulis dalam DAX murni.
* Python tidak menghitung Total Revenue aggregat karena Dashboard harus bisa difilter dinamis berdasarkan Region, Waktu, atau Kategori.
