# Traceability Matrix

Matriks ini memastikan setiap elemen Business Intelligence (Dashboard, KPI, Rekomendasi) dapat dilacak balik (*traceable*) ke tabel data operasional (Product 1 ERP) dan masalah bisnis awal. 
Tidak ada indikator yang dibuat secara "acak", semuanya merupakan solusi langsung atas *Business Problem* yang dialami PT Prima Alat Nusantara.

| Business Problem (Masalah Operasional) | KPI / Indikator (Solusi Analisis) | Sumber Data Odoo (ERP Output) | Analitik Mart (ETL Output) | Dashboard / Report Target | Algoritma / Rekomendasi (DSS) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kekosongan Stok (Stockout)** secara tiba-tiba karena tidak ada rekap harian yang akurat. | Stock Availability, Stockout Rate, Daily Demand | `sale_order`, `stock_move` | `fact_sales`, `fact_inventory` | Inventory Dashboard | **ROP (Reorder Point)**: Rekomendasi titik aman pembelian kembali. |
| **Penumpukan Barang (Overstock)** akibat kepanikan pemesanan tanpa perhitungan matang. | Inventory Turnover, Days Inventory Outstanding (DIO), Slow Moving Product | `stock_move`, `stock_quant` | `fact_inventory`, `fact_sales` | Inventory Dashboard | **EOQ (Economic Order Quantity)**: Rekomendasi jumlah pembelian optimal. |
| **Keterlambatan Supplier** yang merusak rantai pasok. Evaluasi supplier saat ini hanya berdasarkan memori. | Lead Time, Delivery Performance, Delay Frequency | `purchase_order`, `stock_move` | `fact_purchase`, `fact_inventory` | Purchase Dashboard | **Supplier Score & Alert**: Rekomendasi peninjauan kontrak. |
| **Fluktuasi Pendapatan (Revenue)** yang tidak bisa diprediksi. | Revenue Growth, Sales Trend (Monthly), Demand Forecast | `sale_order`, `sale_order_line` | `fact_sales` | Executive & Sales Dashboard | **3-Month Moving Average**: Prediksi permintaan (Forecast) 3 bulan ke depan. |
| **Proporsi Pembelian Tidak Terkontrol**, biaya pembelian melonjak untuk barang yang lambat terjual. | Purchase Growth, Purchase Value per Vendor | `purchase_order`, `purchase_order_line` | `fact_purchase` | Purchase Dashboard | **Forecast vs Purchase Comparison**: Sinkronisasi pembelian dengan prediksi. |
| **Sulit Mengetahui Kinerja Bisnis Keseluruhan**, laporan akhir bulan memakan waktu mingguan. | Total Revenue, Total Transaction, Revenue Contribution (Top Product) | `sale_order`, `sale_order_line` | `fact_sales` | Executive Dashboard | **Automated Aggregation (DAX)**: Info aktual secara real-time. |

## Analisis Lapisan (Layer Analysis)

Matriks di atas membuktikan pemisahan tanggung jawab yang telah kita bahas:

1. **ERP Output (Odoo) $\rightarrow$ ETL Output (Analytics Mart):**
   Ini adalah wilayah **Data Engineering (Phase 5)**. Mengubah data Odoo yang tersebar menjadi Fact dan Dimension tables.
2. **Algoritma / Rekomendasi (DSS):**
   Ini adalah wilayah **Data Science / Analytics Python (Phase 6)**. Menghitung EOQ, ROP, MA3, dan Supplier Score. Parameter ini tidak bisa (sangat tidak efisien) dihitung dinamis menggunakan DAX murni.
3. **Dashboard & KPI Dasar:**
   Ini adalah wilayah **Business Intelligence Power BI (Phase 7)**. Agregasi visual (Total Revenue, Total Cost, Turnover) dihitung menggunakan DAX (Data Analysis Expressions) dan dirender secara interaktif untuk manajemen.
