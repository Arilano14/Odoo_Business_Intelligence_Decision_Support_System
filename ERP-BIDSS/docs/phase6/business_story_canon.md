# Business Story Canon
**Proyek:** OBIDSS (Odoo Business Intelligence Decision Support System)
**Klien:** PT Prima Alat Nusantara (Distributor Alat Berat & Tambang)

*Dokumen ini merupakan "Single Source of Truth" (Satu Versi Kebenaran) untuk seluruh dataset simulasi, analisis, dan dashboard dalam proyek ini.*

## Latar Belakang
PT Prima Alat Nusantara telah menggunakan Odoo ERP selama 12 bulan terakhir. Seluruh transaksi terekam dengan baik, namun manajemen membutuhkan wawasan analitik (dashboard) untuk mengevaluasi masalah operasional yang terjadi sepanjang tahun tersebut.

## Timeline Skenario (Januari – Desember)

| Bulan | Fase / Peristiwa | Revenue (Sales) | Purchase | Inventory | Lead Time Supplier | Catatan Operasional |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Januari** | Baseline (Go Live) | Baseline | Baseline | Normal | 5 hari | Operasional stabil, semua baseline dimulai dari sini. |
| **Februari** | Penjualan Naik | +8% | +5% | Stabil | 5 hari | Permintaan alat berat mulai meningkat, inventory masih cukup menampung. |
| **Maret** | **Krisis: Supplier Telat & Stockout** | **-5% (Turun)** | +5% | **-20% (Kritis)** | **10 hari (Telat)** | Supplier utama terlambat mengirim. Stockout terjadi. Penjualan tertahan karena barang kosong. |
| **April** | **Reaksi: Purchase Besar-besaran** | +10% | **+40% (Besar)**| +10% | 6 hari | Manajemen panik akibat stockout bulan lalu, memesan barang jauh melebihi kebutuhan normal. |
| **Mei** | **Dampak: Overstock Mulai Terjadi** | -10% (Turun) | -5% | **+30% (Naik)** | 5 hari | Permintaan pasar turun. Barang pesanan bulan lalu tiba, mengakibatkan gudang penuh. |
| **Juni** | Puncak Overstock | Stabil (0%) | Stabil (0%) | **+35% (Puncak)** | 5 hari | Gudang penuh. Biaya simpan (Inventory Value) sangat tinggi. Inventory Turnover anjlok. |
| **Juli** | Kebutuhan Dashboard Muncul | +5% | +5% | +20% | 5 hari | Manajemen menyadari masalah dan meminta pembuatan Enterprise Intelligence Dashboard. |
| **Agustus** | BI Development | +5% | -10% (Ditahan) | +10% | 5 hari | Pembelian ditahan untuk menghabiskan stok lambat (Slow Moving). |
| **September**| Dashboard Digunakan | +10% | -5% | Stabil | 5 hari | Insight mulai didapat. Pembelian menjadi lebih selektif. |
| **Oktober** | Penerapan Forecast | +12% | +10% (Sesuai) | Stabil | 5 hari | Mulai menggunakan Forecast. Pembelian sinkron dengan prediksi demand. |
| **November** | Penerapan EOQ & ROP | +15% | +12% | Stabil | 5 hari | Level inventory seimbang dan efisien. Stockout hampir nol. |
| **Desember** | Optimal | **+20% (Puncak)** | +15% | Optimal | 5 hari | Kondisi paling sehat. Revenue tertinggi sepanjang tahun, Turnover maksimal. |

## Parameter Kunci yang Dievaluasi Manajemen
1. **Stockout Rate (Maret):** Kehilangan pendapatan akibat barang tidak ada.
2. **Overstock / Slow Moving (Mei - Juni):** Pembengkakan nilai aset (Inventory Value) akibat pembelian reaktif di bulan April.
3. **Supplier Delivery Performance (Maret):** Keterlambatan pengiriman yang memicu seluruh *bullwhip effect* ini.

Seluruh data yang dihasilkan oleh *Data Generator* dan diolah oleh *Analytics Mart* **WAJIB** mencerminkan fluktuasi statistik dari tabel di atas.
