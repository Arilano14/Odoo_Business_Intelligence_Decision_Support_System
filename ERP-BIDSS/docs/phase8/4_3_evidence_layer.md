# BAB IV: HASIL PENELITIAN DAN PEMBAHASAN (Evidence Layer)

Dokumen ini berisi draf substansi yang bisa Anda masukkan ke dalam Laporan Magang Anda. Seluruh angka di dalam laporan ini adalah **angka asli (valid)** hasil dari *Data Generation* Odoo dan proses ELT (*Extract, Load, Transform*) dari *Study Case* Perusahaan Alat Berat (PT. BIDSS).

---

## 4.3.1 Business Scenario
Dalam studi kasus ini, perusahaan fiktif alat berat yang dirancang menghadapi beberapa anomali operasional yang harus dapat dideteksi oleh *Decision Support System* (DSS). Skenario bisnis yang diterapkan selama tahun 2024 meliputi:
1. **Normal Operations (Januari - Februari):** Transaksi berjalan lancar dengan rata-rata *lead time* yang wajar dan omset stabil.
2. **Supplier Delay (Maret):** Keterlambatan pengiriman material dari penyuplai internasional, yang mengakibatkan ketersediaan barang (stok) menipis dan *revenue* merosot tajam.
3. **Panic Buying (April):** Merespons krisis di bulan Maret, perusahaan melakukan pembelian gila-gilaan (*Panic Buying*) untuk mengamankan stok yang menyebabkan lonjakan drastis pada beban *Purchase Order* (PO).
4. **Overstock & Low Sales (Mei - Juli):** Imbas dari *Panic Buying* menyebabkan gudang kepenuhan (Overstock), padahal tren penjualan sedang melambat.
5. **Recovery (Agustus - Desember):** Stabilitas pasokan perlahan kembali normal hingga penghujung tahun.

## 4.3.2 Dataset Generation (Proses Odoo)
Untuk mensimulasikan lingkungan ERP yang nyata, proses pembuatan dataset dilakukan secara sistematis langsung di atas sistem **Odoo 18**:
* **Modul yang Digunakan:** Sales, Purchase, Inventory, Invoicing, dan Accounting.
* **Volume Data:** Diciptakan 604 SKU Produk Alat Berat & *Spareparts* (seperti Komatsu, Caterpillar, Hitachi), dengan 286 Customer dan Vendor. 
* **Automasi Transaksi:** Total **3.253 baris Sales** dan **4.372 baris Purchase Order** dicetak satu per satu secara *chronological* (berurutan per hari). Odoo ORM (Object-Relational Mapping) digunakan untuk memastikan setiap Quote dikonfirmasi menjadi Sales Order, setiap pengiriman diverifikasi (*Stock Pickings*), dan setiap Invoice lunas dibayar hingga menghasilkan lebih dari **30.937 entri jurnal akuntansi (Accounting Moves)**.
* **Realisme Fluktuatif:** Mempertimbangkan hari libur atau akhir pekan dengan 20% probabilitas nol transaksi, serta volume harian acak (0 hingga 8 pesanan per hari) demi mencegah data terlihat statis atau sintetis.

## 4.3.3 ETL Pipeline (Extract, Transform, Load)
Proses ETL dirancang untuk mengekstraksi data relasional dari Odoo ke dalam bentuk *Analytics Mart*:
1. **Extract:** Data mentah diambil menggunakan pustaka *SQLAlchemy* dan *Pandas* langsung dari tabel inti Odoo (seperti `sale_order_line`, `purchase_order_line`, `stock_valuation_layer`, `account_move_line`).
2. **Transform:** Melakukan pembersihan data, konversi zona waktu ke kalender standar, menghitung HPP (COGS) riil dari valuasi stok, serta menghitung *Lead Time Days* (selisih tanggal rencana dengan tanggal masuk riil).
3. **Load:** Memuat *DataFrame* Pandas ke dalam skema `mart` di PostgreSQL menggunakan fungsi `to_sql()`.

## 4.3.4 Analytics Mart (Star Schema)
Data yang telah dibersihkan distrukturkan menggunakan metode dimensional modeling (*Star Schema*) yang terdiri dari:
* **Dimension Tables:** `dim_product`, `dim_customer`, `dim_vendor`, `dim_date`, `dim_warehouse`, dan `dim_company`.
* **Fact Tables:** 
   - `fact_sales` (mencatat revenue dan cost of goods sold).
   - `fact_purchase` (mencatat kuantitas pembelian dan lead time).
   - `fact_inventory` (mencatat mutasi persediaan fisik).
   - `fact_accounting` (mencatat semua jurnal GL).

## 4.3.5 Proses Pembuatan Power BI (Import & Measures)
Pembuatan *Dashboard* di Power BI melalui tahapan berikut:
1. **Import Database:** Memilih konektor PostgreSQL Database, memasukkan kredensial (`localhost`, database `Business_Intelegent_Project_v2`), dan menarik tabel-tabel di dalam skema `mart`.
2. **Data Modeling:** Membangun relasi *One-to-Many* dengan *Cross Filter Direction* diatur *Single* dari tabel Dimensi ke tabel Fakta, berpusat pada `dim_date` sebagai *Role-Playing Dimension*.
3. **DAX Measures (KPI):** 
   Beberapa formula krusial (*Measures*) yang diimplementasikan:
   * **Total Revenue:** `SUM(fact_sales[revenue])`
   * **Total Margin (Laba Kotor):** `SUM(fact_sales[margin])`
   * **Gross Profit Margin (%):** `DIVIDE([Total Margin], [Total Revenue], 0)`
   * **Average Lead Time (Days):** `AVERAGE(fact_purchase[lead_time_days])`

## 4.3.6 Decision Support System (DSS)
Lapis kecerdasan buatan (*Business Intelligence*) diformulasikan ke dalam dua tabel fakta DSS, di mana Power BI langsung membaca matrik ini:
1. **Forecast (Peramalan):** Dihitung menggunakan algoritma *3-Month Moving Average* pada Python (`calculate_decision_support.py`) yang merekam prediksi permintaan barang di bulan selanjutnya.
2. **Supplier Performance Score:** Memberikan penilaian (*Scoring*) berbasis komputasi untuk *On-time Delivery* (40%), *Fulfillment* (35%), dan *Lead Time Stability* (25%). Menghasilkan status rekomendasi "Baik - Pertahankan" atau "Review Supplier".

## 4.3.7 Power BI Dashboard Visualization
*Dashboard* dibagi menjadi 3 halaman interaktif:
* **Executive Summary:** Menampilkan KPI *Cards* ringkasan (Revenue, Profit, Margin), grafik *Area Chart* untuk tren bulanan, dan *Decomposition Tree* untuk menelusuri profitabilitas per merek/kategori.
* **Supply Chain & Inventory:** Berfokus pada analisis krisis. Menunjukkan metrik *Inventory Turnover* dan matriks keterlambatan pengiriman menggunakan *Scatter Plot* (Keterlambatan vs Harga).
* **DSS Recommendation:** Tabel matriks interaktif menyorot *Forecast* barang vs Stok saat ini, serta status peringatan merah untuk pemasok bermasalah.

## 4.3.8 Business Findings (Temuan Laporan)
Dari hasil interaksi dengan *Dashboard*, DSS berhasil mengungkapkan fenomena operasional berikut (Sesuai dengan *Study Case*):
1. **Krisis Pasokan Maret (Supply Shock):** Revenue perusahaan pada bulan Februari mencapai tingkat wajar yaitu **Rp 237,6 Miliar**. Namun memasuki bulan Maret, revenue anjlok drastis ke angka **Rp 125,9 Miliar** (turun 47%). Ini terdeteksi akibat *Average Lead Time* (keterlambatan vendor) yang meningkat drastis, sehingga perusahaan kehabisan barang (*Out of Stock*) untuk dijual.
2. **Tragedi Panic Buying April:** Sebagai respons kepanikan atas krisis pasokan Maret, *Dashboard Supply Chain* mendeteksi bahwa pengeluaran *Purchase* bulan April meledak mencapai **Rp 1,29 Triliun** dalam kurun satu bulan, menyedot mayoritas proporsi pengadaan selama setahun penuh (total omset setahun Rp 2,16 Triliun).
3. **Kualitas Pemasok:** Dari evaluasi DSS terhadap 286 pemasok (*vendors*), sistem membuktikan bahwa **228 Pemasok** menerima peringatan keras (status: *"Review Supplier - Evaluasi Kontrak"*) akibat gagalnya mereka mempertahankan stabilitas *Lead Time* di Q1 2024.

## 4.3.9 Rekomendasi Keputusan
Berlandaskan dari temuan *Business Intelligence* di atas, maka tindakan yang direkomendasikan adalah:
1. **Diversifikasi Rantai Pasok:** Karena dominasi 228 pemasok berada di zona rawan (*Review Contract*), perusahaan alat berat ini wajib mengevaluasi ulang SLA (*Service Level Agreement*) dan mencari manufaktur substitusi.
2. **Pembatasan Plafon Pembelian (Safety Stock Limit):** Mencegah terulangnya pengeluaran modal tak terkendali (Rp 1,29 Triliun dalam sebulan), perusahaan harus memberlakukan sistem validasi PO bertingkat apabila persediaan sudah menyentuh rasio batas aman (*Safety Stock*).
3. **Adopsi Forecasting:** Menggunakan data `fact_forecast_monthly` dari DSS sebagai acuan dasar pengadaan bulan berjalan ketimbang merespons *panic order* secara emosional.
