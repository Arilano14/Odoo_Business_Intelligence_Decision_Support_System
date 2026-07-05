# Business Problem Definition

## Konteks
PT Prima Alat Nusantara merupakan perusahaan distributor alat berat yang telah mengimplementasikan Odoo ERP. Setelah sistem berjalan dan seluruh transaksi operasional tercatat, manajemen menghadapi kendala: data transaksi yang tersimpan di ERP belum dimanfaatkan secara optimal untuk mendukung pengambilan keputusan. Laporan masih disusun melalui ekspor data ke spreadsheet secara manual.

## Permasalahan

### Problem 1: Revenue Visibility
Sales meningkat, tetapi laba perusahaan tidak ikut meningkat. Manajemen tidak mengetahui produk mana yang memberikan kontribusi terbesar terhadap keuntungan.
- **Dampak:** Keputusan strategi produk tidak berbasis data.
- **Output BI:** Revenue Analysis, Product Contribution, Profit Contribution.

### Problem 2: Inventory Overstock
Gudang sering mengalami overstock. Nilai inventory meningkat dan biaya penyimpanan bertambah.
- **Dampak:** Modal tertahan di persediaan, biaya gudang tinggi.
- **Output BI:** Inventory Value, Inventory Turnover, Days Inventory Outstanding (DIO).

### Problem 3: Stockout pada Proyek Pelanggan
Beberapa proyek pelanggan terlambat karena stok produk tertentu kosong.
- **Dampak:** Kehilangan penjualan, kepuasan pelanggan menurun.
- **Output BI:** Stock Availability, Reorder Point (ROP), Safety Stock.

### Problem 4: Supplier Tidak Konsisten
Pembelian dari supplier tidak konsisten. Ada supplier yang sering terlambat mengirim barang.
- **Dampak:** Lead time tidak stabil, risiko rantai pasok meningkat.
- **Output BI:** Supplier Performance Score, Lead Time Analysis, Purchase Trend.

### Problem 5: Forecast Masih Manual
Estimasi kebutuhan pembelian masih menggunakan perkiraan tanpa dasar data historis.
- **Dampak:** Pembelian tidak optimal, risiko overstock atau stockout.
- **Output BI:** Demand Forecast (Moving Average), Purchase Forecast.
