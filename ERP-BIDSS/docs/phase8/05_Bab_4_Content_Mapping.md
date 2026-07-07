# Pemetaan Konten Bab 4 Laporan Implementasi
**Struktur: 4.3 Implementasi Business Intelligence Decision Support System (BIDSS)**

Dokumen ini berisi panduan dan referensi data riil (valid dari *database* studi kasus) yang dapat Anda masukkan (*copy-paste*) ke dalam subbab Laporan Magang / Skripsi Anda.

---

### 4.3.1 Business Scenario (Skenario Bisnis)
**Tujuan Subbab:** Menjelaskan latar belakang data yang digunakan.
**Isi yang bisa dimasukkan:**
- **Narasi Kasus:** Perusahaan distributor alat berat mengalami guncangan rantai pasok (*Supply Shock*).
- **Timeline:**
  - *Jan-Feb:* Penjualan dan pasokan berjalan normal.
  - *Maret:* Vendor utama (Supplier Internasional) mengalami masalah pengiriman (Lead Time melonjak).
  - *April:* Kepanikan manajemen memicu *Panic Buying* (pembelian besar-besaran).
  - *Mei-Desember:* Pembelian dihentikan sementara karena gudang mengalami *Overstock*.
- **Aset Pendukung:** Tidak perlu *screenshot*, cukup tabel kronologi skenario bisnis.

### 4.3.2 Dataset Generation (Pembentukan Dataset)
**Tujuan Subbab:** Membuktikan bahwa data tidak diketik manual, melainkan di-*generate* menggunakan metode terkomputerisasi.
**Isi yang bisa dimasukkan:**
- **Metode:** Penggunaan modul *Python* dan *Odoo 18 ORM (Object-Relational Mapping)* untuk memalsukan data transaksional.
- **Hasil Data (Valid dari PostgreSQL):**
  - **Master Data:** Terbentuk 554 Produk (Alat Berat & Suku Cadang), 302 Pelanggan (Perusahaan Konstruksi), dan 301 Vendor (Supplier Internasional & Lokal).
  - **Transactional Data:** Terbentuk ribuan transaksi (3.382 baris *Sales Order Line*, 3.409 baris *Purchase Order Line*, dan 6.791 pergerakan gudang/ *Stock Move*).
- **Aset Pendukung:** *Screenshot* halaman *Sales* atau *Purchase* di *browser* Odoo Anda yang menampilkan ribuan transaksi.

### 4.3.3 ETL Pipeline (Proses ETL)
**Tujuan Subbab:** Menjelaskan bagaimana data kotor dari Odoo dipindahkan dan dibersihkan.
**Isi yang bisa dimasukkan:**
- **Alur Kerja:** 
  1. *Extract:* Menarik data mentah Odoo menggunakan SQL (`psycopg2`).
  2. *Transform:* Membersihkan data dan melakukan kalkulasi turunan (contoh: Menarik kolom `standard_price` yang tersembunyi di JSON Odoo 18 untuk menghitung harga pokok / *Cost*).
  3. *Load:* Memasukkan data ke skema `mart` secara otomatis menggunakan *Pandas DataFrame*.
- **Aset Pendukung:** Potongan kode (Snippet) `transform.py` atau *screenshot* *log* terminal saat proses ETL berjalan ("ETL Pipeline COMPLETED. Total rows loaded: 23.486").

### 4.3.4 Analytics Mart (Gudang Data Analitik)
**Tujuan Subbab:** Memperlihatkan desain arsitektur data (*Data Modeling*).
**Isi yang bisa dimasukkan:**
- **Konsep:** Penggunaan arsitektur **Star Schema** (Skema Bintang).
- **Tabel Dimensi (Master):** `dim_date`, `dim_product`, `dim_customer`, `dim_vendor`, `dim_warehouse`.
- **Tabel Fakta (Transaksi):** `fact_sales` (Pendapatan & HPP), `fact_purchase` (Pembelian & Lead Time), `fact_inventory` (Keluar Masuk Gudang).
- **Aset Pendukung:** *Screenshot* "Model View" (Skema relasi garis penghubung tabel 1-to-Many) dari dalam Power BI Anda.

### 4.3.5 KPI Bisnis (Indikator Kinerja Utama)
**Tujuan Subbab:** Memaparkan metrik apa saja yang diukur untuk mengevaluasi kesehatan perusahaan.
**Isi yang bisa dimasukkan:**
- **Daftar KPI & Formula DAX-nya:**
  - *Revenue & Margin* (Kesehatan Finansial)
  - *Avg Lead Time Days* (Kinerja Vendor)
  - *Inventory Turnover Ratio / ITR* (Kecepatan perputaran barang)
  - *Days Inventory Outstanding / DIO* (Lama barang mengendap di gudang).
- **Aset Pendukung:** Anda bisa melampirkan 2-3 rumus DAX inti (*copy-paste* dari `12_powerbi_step_by_step_tutorial.md` atau `02_dax_measure_catalog.md`).

### 4.3.6 Decision Support System (Sistem Pendukung Keputusan)
**Tujuan Subbab:** Menjelaskan logika otomasi rekomendasi (*Prescriptive Analytics*).
**Isi yang bisa dimasukkan:**
- **Logika Sistem:** Sistem tidak sekadar menampilkan data, tapi memberikan rekomendasi beli/tahan.
- **Formula Keputusan:**
  1. *3M Moving Average Demand* (Menghitung rata-rata jualan 3 bulan agar tidak ikut panik).
  2. *Reorder Point (ROP)* = (Avg Daily Sales × Avg Lead Time) + Safety Stock.
  3. *Aturan Keputusan:* JIKA *Inventory Qty* <= *ROP*, MAKA Sistem mengeluarkan label "🟡 Reorder Needed" atau "🔴 Urgent Order". Jika tidak, statusnya "🔵 Overstock / Optimal".
- **Aset Pendukung:** Rumus IF *Action Status* (DAX).

### 4.3.7 Power BI Dashboard (Antarmuka Pengguna)
**Tujuan Subbab:** Menampilkan hasil akhir visualisasi.
**Isi yang bisa dimasukkan:**
- Penjelasan bahwa *Dashboard* dibagi menjadi 6 halaman komprehensif.
- **Aset Pendukung:** *Screenshot* utuh (layar penuh) dari Power BI Desktop Anda untuk setiap halaman (Figure 4.x Executive Dashboard, Figure 4.y Sales Dashboard, dsb).

### 4.3.8 Business Findings (Temuan Investigasi Bisnis)
**Tujuan Subbab:** Menginterpretasikan hasil dari *Dashboard* ke dalam bahasa bisnis riil berdasarkan data di sistem.
**Isi yang bisa dimasukkan:**
*(Gunakan data asli hasil kalkulasi PostgreSQL berikut untuk mengisi teks di Laporan Anda):*
- **Penemuan Krisis (Maret):** Ditemukan lonjakan Rata-Rata Waktu Pengiriman (*Lead Time*) secara drastis dari **5 hari (Jan-Feb)** menjadi **10.3 hari di bulan Maret**. Imbasnya, Revenue perusahaan di bulan Maret langsung anjlok ke angka **Rp 344.1 Juta**.
- **Penemuan Panic Buying (April):** Karena panik kehabisan stok, volume pembelian (*Purchase Qty*) yang biasanya hanya **7.000 unit/bulan**, tiba-tiba meroket hingga **14.383 unit** pada bulan April. Nilai belanja (*Purchase Value*) melonjak tajam.
- **Penemuan Overstock (Pasca-Krisis):** Akibat pembelian berlebih, metrik DIO (*Days Inventory Outstanding*) berubah menjadi zona merah (>90 hari), menandakan barang menumpuk mati di gudang (Bullwhip Effect).
- **Aset Pendukung:** Anda bisa memotong/mengambil *screenshot* secara spesifik pada bagian grafik garis (*Line Chart*) di Executive Dashboard yang menanjak naik di bulan April.

### 4.3.9 Rekomendasi Keputusan (Final DSS Output)
**Tujuan Subbab:** Membuktikan bahwa sistem mampu menghentikan kepanikan manajer *Purchasing*.
**Isi yang bisa dimasukkan:**
- *Dashboard* secara cerdas menyelamatkan keuangan perusahaan dengan mencegat pembelian lebih lanjut.
- **Tabel Bukti Keputusan Sistem (Data Valid Kuartal 4):**

| Product Name | Current Stock | 3M MA Demand | ROP | Decision Status |
| :--- | :--- | :--- | :--- | :--- |
| Alat Berat Part 151 | 436 Unit | 3 Unit | 1 Unit | 🔵 **Overstock - Hold Order** |
| Alat Berat Part 217 | 333 Unit | 9 Unit | 2 Unit | 🔵 **Overstock - Hold Order** |
| Alat Berat Part 76 | 326 Unit | 20 Unit | 3 Unit | 🔵 **Overstock - Hold Order** |

- **Analisis Akhir:** Dengan *Decision Support System* ini, sistem dengan tegas menyuruh departemen *Purchasing* untuk menahan pesanan (*Hold Order*) karena batas ROP (contoh Part 151 hanya butuh 1 unit) sangat jauh di bawah sisa stok yang menumpuk (436 unit). Tanpa sistem ini, departemen *Purchasing* mungkin akan terus berbelanja secara buta.
- **Aset Pendukung:** *Screenshot* Tabel "Decision Dashboard" (Halaman 6) dari Power BI Anda.
