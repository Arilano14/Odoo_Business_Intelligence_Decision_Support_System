# Business Assumption Table

Untuk menjaga agar seluruh perhitungan pada layer Decision Support System (DSS) berbasis saintifik dan realistis, berikut adalah daftar asumsi bisnis yang disepakati untuk kasus PT Prima Alat Nusantara (Distributor Alat Berat).

Seluruh algoritma Python (Phase 6 DSS) akan menggunakan konstanta ini.

## 1. Inventory & Supply Chain Parameters

| Parameter | Nilai / Formula | Alasan / Sumber Acuan |
| :--- | :--- | :--- |
| **Ordering Cost (S)** | **Rp 500.000 / PO** | Estimasi biaya administratif, komunikasi supplier, inspeksi, dan biaya logistik per dokumen pemesanan. Angka ini lazim untuk industri distributor alat. |
| **Holding Cost (H)** | **20% dari Standard Price / tahun** | Mengacu pada literatur manajemen persediaan (rata-rata 15%-25%), meliputi biaya asuransi, depresiasi, opportunity cost, dan biaya gudang fisik. |
| **Working Days** | **300 Hari / tahun** | 25 hari kerja efektif per bulan (Minggu libur). Digunakan untuk menghitung rata-rata harian (Daily Demand). |
| **Service Level Target** | **95%** | Industri B2B alat berat sangat menghindari stockout, namun tidak realistis menargetkan 100%. |
| **Safety Factor (Z)** | **1.65** | Nilai statistik (Z-Score) untuk tingkat keyakinan (Service Level) 95% pada distribusi normal. Digunakan dalam perhitungan Safety Stock. |

## 2. Supplier Performance Scoring (Weights)

Supplier Performance dievaluasi bukan hanya dari keterlambatan pengiriman, tetapi dari 4 dimensi (Delivery, Price, Fulfillment, Delay Frequency) dengan bobot berikut:

| Kriteria (Parameter) | Bobot | Deskripsi Pengukuran |
| :--- | :--- | :--- |
| **Delivery Speed (Lama Kirim)** | **40%** | Diukur dari selisih `date_planned` dan `date_order`. Skor lebih tinggi jika rata-rata hari (Lead Time) lebih rendah dari standar (5 hari). |
| **Order Fulfillment (Pemenuhan)** | **30%** | Persentase kuantitas yang diterima (receipt) dibandingkan yang dipesan (ordered). |
| **Price Consistency** | **20%** | Variasi harga riil pada PO dibandingkan dengan *standard_price* master data. Jika naik, skor turun. |
| **Delay Frequency (Frekuensi Telat)** | **10%** | Persentase berapa kali PO terlambat dari *date_planned*. |

## 3. Threshold (Ambang Batas) Bisnis

Aturan logika bisnis (*Business Rules*) yang menentukan status (Alerts/Recommendations).

| Skenario | Logika (If Statement) | Status / Rekomendasi |
| :--- | :--- | :--- |
| **Slow Moving** | Inventory Turnover < 2 (dalam setahun) | "Slow Moving - Tunda Pembelian" |
| **Reorder Alert** | Stock on Hand $\le$ ROP (Reorder Point) | "Reorder - Buat Draft PO" |
| **Supplier Alert** | Delay Frequency > 10% ATAU Score < 70 | "Review Supplier - Evaluasi Kontrak" |
| **Forecast Alert** | Forecast Error (MAPE) > 20% | "Forecast Error - Gunakan Safety Stock" |
| **Business Alert** | Revenue turun $\ge$ 2 bulan berturut-turut | "Business Alert - Cek Penjualan" |

## Implementasi Sistem
Tabel asumsi ini dimasukkan ke dalam kode Python (sebagai konstanta di dalam config atau class parameter) agar algoritma dapat memproses perhitungan EOQ, ROP, Safety Stock, dan Supplier Score secara otomatis terhadap data dari Analytics Mart.
