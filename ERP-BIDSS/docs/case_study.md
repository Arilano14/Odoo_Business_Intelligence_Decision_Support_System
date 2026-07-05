# Case Study — PT Prima Alat Nusantara

## Profil Perusahaan
PT Prima Alat Nusantara merupakan perusahaan distributor alat berat yang menjual excavator, bulldozer, wheel loader, forklift, dan sparepart kepada perusahaan konstruksi, pertambangan, dan perkebunan.

## Latar Belakang
Perusahaan telah mengimplementasikan ERP Odoo 18 untuk mengelola seluruh proses bisnis mulai dari penjualan, pembelian, persediaan, hingga pencatatan keuangan.

Selama implementasi ERP berlangsung, dilakukan requirement gathering, konfigurasi sistem, System Integration Testing (SIT), User Acceptance Testing (UAT), pelatihan pengguna, serta persiapan Go Live. Setelah sistem mulai digunakan, seluruh transaksi operasional telah tercatat dengan baik.

Namun, manajemen menghadapi kendala baru. Walaupun data transaksi sudah tersedia di ERP, informasi yang dibutuhkan untuk mendukung pengambilan keputusan masih harus diperoleh melalui proses ekspor data ke spreadsheet dan pengolahan manual. Akibatnya, penyusunan laporan membutuhkan waktu yang cukup lama dan belum mampu memberikan analisis maupun rekomendasi secara cepat.

Berdasarkan kondisi tersebut dikembangkan **Enterprise Intelligence Dashboard** yang memanfaatkan data ERP untuk menghasilkan informasi analitis dan rekomendasi bagi manajemen.

---

## Timeline Skenario Bisnis (12 Bulan)

| Bulan | Event | Dampak |
| :--- | :--- | :--- |
| **Januari** | ERP Go Live. Semua transaksi mulai dicatat. | Baseline data terbentuk. |
| **Februari** | Penjualan meningkat. Inventory stabil. | Revenue naik. |
| **Maret** | Supplier A terlambat. Stock excavator habis. | Stockout, revenue turun. |
| **April** | Purchase besar dilakukan untuk antisipasi. | Inventory meningkat tajam. |
| **Mei** | Permintaan turun. Inventory menumpuk. | Overstock, slow moving muncul. |
| **Juni** | Gudang penuh. Inventory value meningkat. | Biaya penyimpanan naik. |
| **Juli** | Manajemen kesulitan membaca performa. Laporan masih Excel. | Kebutuhan dashboard teridentifikasi. |
| **Agustus** | Enterprise Intelligence Dashboard mulai dikembangkan. | ETL dan Analytics Mart dibangun. |
| **September** | Dashboard mulai digunakan. | KPI tersedia secara real-time. |
| **Oktober** | Forecast diterapkan. | Rencana pembelian berbasis data. |
| **November** | EOQ dan ROP diterapkan. | Pembelian lebih efisien. |
| **Desember** | Dashboard aktif mendukung keputusan. | Inventory stabil, revenue meningkat. |

---

## Permasalahan Bisnis

| No | Permasalahan | Indikator | Output BI |
| :--- | :--- | :--- | :--- |
| 1 | Sales meningkat tetapi laba tidak ikut naik | Revenue, Profit Contribution | Revenue Analysis, Product Contribution |
| 2 | Gudang sering overstock | Inventory Value, Turnover | Inventory Turnover, DIO |
| 3 | Proyek pelanggan terlambat karena stok kosong | Stock Availability | ROP, Safety Stock |
| 4 | Supplier sering terlambat mengirim barang | Delivery Score | Supplier Performance Score |
| 5 | Forecast pembelian masih berdasarkan perkiraan | — | Demand Forecast (Moving Average) |

---

## Hubungan Produk 1 dan Produk 2

```
Produk 1: Odoo ERP Implementation Validation Kit
├── Requirement Gathering
├── Business Process Mapping
├── ERP Configuration
├── System Integration Testing (SIT)
├── User Acceptance Testing (UAT)
├── User Manual
└── Go Live Preparation
         │
         ▼
Data transaksi ERP terkumpul (konsisten & tervalidasi)
         │
         ▼
Produk 2: Enterprise Intelligence Dashboard
├── ETL Development (Python)
├── Data Warehouse (Star Schema)
├── KPI Calculation
├── Demand Forecast (Moving Average)
├── Decision Support (EOQ, ROP, Supplier Score)
└── Power BI Dashboard
```

---

## Output Dashboard

| Dashboard | Visualisasi |
| :--- | :--- |
| Executive Dashboard | Revenue, Purchase, Inventory Value, Transaction, Growth |
| Sales Dashboard | Sales Trend, Revenue Contribution, Top Product, Top Customer |
| Purchase Dashboard | Purchase Trend, Top Vendor, Lead Time, Outstanding PO |
| Inventory Dashboard | Inventory Value, Turnover, Slow/Fast Moving, DIO, Stock Availability |
| Forecast & Decision Dashboard | Demand Forecast, EOQ, ROP, Supplier Performance, Recommendation |

---

## Rekomendasi Berbasis Analisis

| Temuan Analisis | Indikator | Rekomendasi |
| :--- | :--- | :--- |
| Inventory Turnover < 2 kali/tahun | Persediaan bergerak lambat | Kurangi pembelian dan lakukan promosi produk |
| Stok aktual ≤ Reorder Point | Risiko stockout | Buat Purchase Order sesuai hasil EOQ |
| Supplier Score < 70 | Kinerja pemasok rendah | Evaluasi SLA atau pertimbangkan pemasok alternatif |
| Forecast permintaan meningkat > 15% | Tren permintaan naik | Tingkatkan rencana pembelian untuk periode berikutnya |
| Revenue Contribution < 5% dan DIO tinggi | Produk kurang produktif | Evaluasi kelayakan produk atau kurangi stok |
