# 10. Dashboard Validation (UAT Checklist)

Dokumen ini adalah lembar kerja validasi (User Acceptance Testing) untuk memastikan bahwa Dashboard Power BI tidak sekadar "cantik", namun menyajikan angka yang 100% akurat dan matematis sesuai dengan data dari Analytics Mart. 

Setiap langkah validasi harus dilakukan oleh analis/developer sebelum mendistribusikan `.pbix` ke level eksekutif.

---

## 1. Validasi Total Revenue (Executive Dashboard)
- **Metode Power BI**: Tarik `[Total Revenue]` ke sebuah Card Visual (tanpa filter).
- **Metode Database (PGAdmin)**: Jalankan query SQL berikut di database `mart`:
  ```sql
  SELECT SUM(revenue) FROM mart.fact_sales;
  ```
- **Kriteria Lulus**: Angka di Power BI harus identik sempurna (hingga 2 desimal jika dibutuhkan) dengan hasil SQL.
- **[ ] PASS** | **[ ] FAIL**

## 2. Validasi Inventory Value (Inventory Dashboard)
- **Metode Power BI**: Pastikan DAX `[Inventory Value]` aktif (Incoming - Outgoing).
- **Metode Database (PGAdmin)**:
  ```sql
  SELECT 
    SUM(CASE WHEN movement_type = 'incoming' THEN value ELSE 0 END) -
    SUM(CASE WHEN movement_type = 'outgoing' THEN value ELSE 0 END)
  FROM mart.fact_inventory;
  ```
- **Kriteria Lulus**: Saldo akhir inventaris harus sama dengan nilai agregat *stock valuation* di gudang.
- **[ ] PASS** | **[ ] FAIL**

## 3. Validasi Cross-Filtering Slicer Waktu (Sales Dashboard)
- **Metode Power BI**: Pilih `Month = "April"` di Filter Pane.
- **Perilaku yang Diharapkan**:
  - Total Revenue Card harus menampilkan hanya Revenue bulan April.
  - Bar Chart produk harus berubah urutannya menyesuaikan penjualan bulan April saja.
- **Metode Database**:
  ```sql
  SELECT SUM(f.revenue) 
  FROM mart.fact_sales f 
  JOIN mart.dim_date d ON f.date_id = d.date_id 
  WHERE d.month = 4;
  ```
- **Kriteria Lulus**: Hasil filter dan visualisasi selaras secara instan.
- **[ ] PASS** | **[ ] FAIL**

## 4. Validasi 3M Moving Average (Forecast Dashboard)
- **Metode Power BI**: Evaluasi bulan Agustus (Bulan 8). Nilai 3M MA Demand harus mencerminkan rata-rata dari Bulan 5, 6, dan 7.
- **Metode Database (Manual Cek)**:
  Jumlahkan Total Kuantitas Penjualan (Mei + Juni + Juli) lalu bagi 3. Bandingkan hasilnya dengan titik garis `3M MA Demand` di bulan Agustus pada Power BI.
- **Kriteria Lulus**: Selisih karena pembulatan dibiarkan, namun angka dasar harus presisi.
- **[ ] PASS** | **[ ] FAIL**

## 5. Validasi Decision Rules (Decision Dashboard)
- **Metode Power BI**: Filter (atau klik Bookmark) `Action Status = "🔴 Stockout - Urgent Order"`.
- **Perilaku yang Diharapkan**: Tabel visual hanya menampilkan produk-produk yang nilai `[Inventory Qty]`-nya benar-benar 0 atau < 0 (jika ada error sistem *negative stock*).
- **Kriteria Lulus**: Tidak boleh ada produk dengan stok 100 yang masuk ke dalam list *Stockout*. Logika DAX IF bertingkat berjalan sempurna.
- **[ ] PASS** | **[ ] FAIL**

---

> **Catatan Developer**: Jika Anda menemui hasil **FAIL** di bagian manapun, JANGAN ubah data di Postgres atau Odoo. Perbaiki **Relationship** (Star Schema) Anda di tab *Model View* Power BI, atau periksa kembali sintaks DAX Anda (terutama fungsi CALCULATE dan ALL).
