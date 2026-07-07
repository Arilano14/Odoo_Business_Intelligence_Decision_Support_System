# Deliverable 1: Business Findings Report

Dokumen ini berisi hasil temuan riset (Evidence) berdasarkan ekstraksi data nyata dari database Odoo (skema `mart`) yang telah ditarik ke dalam Power BI. Angka-angka di bawah ini adalah bukti valid dari berjalannya skenario krisis rantai pasok.

## A. Temuan KPI Utama (Monthly Breakdown)

### 1. Revenue (Pendapatan)
*   **Januari:** Rp 412.8 Juta *(Kondisi Baseline/Normal)*
*   **Februari:** Rp 472.7 Juta *(Mengalami kenaikan penjualan)*
*   **Maret:** Rp 344.1 Juta *(Terjadi penurunan akibat barang sulit didapat / Supplier Delay)*
*   **April:** Rp 455.1 Juta *(Mulai pulih seiring barang datang)*

**Interpretasi:** Penurunan drastis di bulan Maret membuktikan bahwa kendala *supply* secara langsung memukul *revenue* perusahaan karena tidak ada barang yang bisa dijual ke pelanggan.

### 2. Average Lead Time (Rata-rata Waktu Kedatangan Barang)
*   **Januari:** 5.08 Hari *(Normal)*
*   **Februari:** 5.68 Hari *(Normal)*
*   **Maret:** 10.35 Hari *(Spike / Keterlambatan)*
*   **April:** 6.70 Hari *(Mulai stabil)*

**Interpretasi:** Ini adalah pemicu utama (Root Cause) krisis. Keterlambatan vendor di bulan Maret terekam jelas secara kuantitatif (waktu tunggu melonjak hampir 2x lipat dari ~5 hari menjadi 10 hari).

### 3. Purchase Quantity (Jumlah Barang Dibeli)
*   **Januari:** 7.360 Unit
*   **Februari:** 6.961 Unit
*   **Maret:** 7.075 Unit
*   **April:** 14.383 Unit *(Spike / Panic Buying)*
*   **Mei:** 4.264 Unit *(Hold Order)*

**Interpretasi:** Akibat keterlambatan di bulan Maret, manajemen panik dan melakukan pembelian besar-besaran di bulan April (melonjak hingga 14 ribu unit). Hal ini membuktikan perilaku psikologis perusahaan (*Panic Buying*) saat rantai pasok terganggu.

### 4. Inventory Turnover Ratio & Overstock (Siklus Gudang)
Akibat *Panic Buying* di bulan April:
*   **April & Mei:** Gudang kelebihan kapasitas (Overstock).
*   **Dampak:** Biaya penyimpanan menumpuk dan rasio perputaran persediaan (ITR) melambat karena barang yang masuk (14 ribu unit) tidak sebanding dengan kecepatan penjualan historis.

---
**Kesimpulan Riset:**
Sistem *Business Intelligence* berhasil menangkap, mengkuantifikasi, dan memvisualisasikan fenomena *Supply Shock* (Maret) dan *Bullwhip Effect* (Panic Buying di April) dengan sangat akurat menggunakan data transaksional Odoo.
