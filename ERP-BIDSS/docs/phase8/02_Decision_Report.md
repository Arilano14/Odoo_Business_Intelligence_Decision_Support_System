# Deliverable 2: Decision Report (DSS Output)

Tabel di bawah ini merupakan luaran langsung dari *Decision Dashboard* (Sistem Pendukung Keputusan) yang dirancang untuk mencegah *Overstock* dan *Stockout*. Angka di bawah ditarik langsung dari kondisi gudang riil Odoo di akhir tahun (Kuartal 4).

## Tabel Rekomendasi Keputusan (Top 10 Inventory)

| Product Name | Current Stock | 3M Demand (Forecast) | Avg Lead Time | ROP | Recommended Order (EOQ) | Decision Status | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Alat Berat Part 151** | 436 Unit | 3 Unit | 5.4 Hari | 1 Unit | 0 Unit | 🔵 **Overstock - Hold Order** | Stok saat ini (436) jauh melebihi batas aman (ROP = 1). Stop pembelian. |
| **Alat Berat Part 201** | 395 Unit | 0 Unit | 5.7 Hari | 0 Unit | 0 Unit | 🔵 **Overstock - Hold Order** | Barang lambat terjual (Slow Moving). Stop pembelian. |
| **Alat Berat Part 217** | 333 Unit | 9 Unit | 6.4 Hari | 2 Unit | 0 Unit | 🔵 **Overstock - Hold Order** | Stok sangat berlimpah melebihi rata-rata pergerakan 3 bulan terakhir. |
| **Alat Berat Part 76** | 326 Unit | 20 Unit | 5.7 Hari | 3 Unit | 0 Unit | 🔵 **Overstock - Hold Order** | Penjualan lumayan (20 unit/3 bln), tapi stok sisa panik (326) masih terlalu banyak. |
| **Alat Berat Part 183** | 326 Unit | 11 Unit | 6.5 Hari | 2 Unit | 0 Unit | 🔵 **Overstock - Hold Order** | Stok berlimpah, hold pembelian ke vendor terkait. |
| **... (Barang Kosong)*** | 0 Unit | 15 Unit | 5.0 Hari | 3 Unit | 15 Unit | 🔴 **Stockout - Urgent Order** | Barang habis total padahal ada *demand*. Sistem langsung merekomendasikan beli 15 unit. |
| **... (Barang Menipis)*** | 2 Unit | 12 Unit | 5.0 Hari | 3 Unit | 10 Unit | 🟡 **Reorder Needed** | Stok (2) sudah menyentuh batas ROP (3). Sistem menyuruh pesan 10 unit. |

*\*Catatan: 2 baris terbawah adalah contoh perilaku sistem jika data barang habis/menipis terdeteksi di gudang.*

**Analisis Riset:**
Dari tabel di atas, terbukti bahwa efek *Panic Buying* di bulan April meninggalkan **"Luka" (Overstock)** yang panjang hingga akhir tahun. Hampir seluruh barang di gudang terdeteksi berstatus 🔵 *Overstock* oleh sistem. Dengan adanya *Decision Dashboard* ini, manajemen akhirnya memiliki rem penahan yang berbasis data kuantitatif (*Reorder Point*), sehingga mereka tidak akan lagi membuang-buang uang kas untuk membeli barang yang masih menumpuk di gudang.
