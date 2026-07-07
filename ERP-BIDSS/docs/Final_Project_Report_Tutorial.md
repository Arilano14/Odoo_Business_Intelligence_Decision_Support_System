# Laporan Lengkap & Panduan Praktis (End-to-End)
**Enterprise Intelligence Dashboard: Supply Chain Shock & Recovery (Odoo 18 & Power BI)**

Dokumen ini merupakan panduan komprehensif mulai dari pembentukan dataset (Odoo), pemrosesan data (ETL), hingga penyusunan *Business Intelligence Dashboard* (Power BI) langkah demi langkah.

---

## BAB 1: Persiapan dan Pembuatan Dataset (Odoo 18)

### 1. Skenario Bisnis (Studi Kasus)
Proyek ini didasarkan pada skenario krisis rantai pasok selama 12 bulan (Januari - Desember) di sebuah PT Distributor Alat Berat:
- **Kuartal 1 (Jan-Mar):** Bisnis berjalan normal (Baseline). Tiba-tiba terjadi masalah pada vendor besar ("Supplier Internasional") yang menyebabkan pengiriman alat berat tertunda (*Lead Time* melonjak).
- **Kuartal 2 (Apr-Jun):** Akibat barang telat datang, perusahaan mengalami *Stockout* (kehabisan barang) di bulan April. Kepanikan membuat manajemen melakukan *Panic Buying* (pembelian besar-besaran) di bulan Mei. Akibatnya, pada bulan Juni gudang mengalami *Overstock* (penumpukan barang).
- **Kuartal 3 & 4 (Jul-Des):** Fase pemulihan. Perusahaan mulai menggunakan prediksi (*Forecast*) dan *Reorder Point (ROP)* untuk menstabilkan kembali arus kas dan stok gudang.

### 2. Proses Pembuatan Data (Python ke Odoo)
Untuk mereplika skenario tersebut tanpa harus mengetik manual di Odoo, kita menggunakan *script* Python.
1. **Reset Database:** Skrip menghapus seluruh transaksi lama agar *database* bersih.
2. **Generate Master Data:** Skrip membuat daftar Produk (Alat Berat), Pelanggan (Perusahaan Konstruksi), dan Vendor.
3. **Generate Transaksi (Sales & Purchase):** Skrip memasukkan pesanan penjualan (SO) dan pembelian (PO) secara otomatis ke dalam PostgreSQL, menyesuaikan lonjakan angka sesuai skenario 12 bulan di atas.
4. **Verifikasi Odoo:** Setelah *script* selesai, kita dapat membuka Odoo (`http://localhost:8069`) dan melihat bahwa ribuan dokumen *Quotation*, *Sales Order*, dan *Purchase Order* telah terbentuk secara ajaib.

---

## BAB 2: Data Warehouse & ETL Pipeline (PostgreSQL)

Power BI tidak disarankan untuk langsung membaca tabel mentah Odoo (yang jumlahnya ratusan dan rumit). Oleh karena itu, kita memprosesnya melalui tahapan **ETL (Extract, Transform, Load)**:

1. **Extract:** Python membaca tabel operasional Odoo (seperti `sale_order_line`, `product_product`, dll).
2. **Transform:** Data dibersihkan dan dihitung (contoh: menghitung selisih tanggal untuk mencari *Lead Time Days*).
3. **Load (Skema Mart):** Data yang sudah bersih dimasukkan ke dalam skema baru bernama `mart` di PostgreSQL dengan struktur **Star Schema**:
   - **Tabel Dimensi (Master):** `dim_product`, `dim_customer`, `dim_vendor`, `dim_date`.
   - **Tabel Fakta (Transaksi):** `fact_sales`, `fact_purchase`, `fact_inventory`.

---

## BAB 3: Pembuatan Dashboard Power BI (Tahap demi Tahap)

### TAHAP A: Import Data & Relasi (Star Schema)
1. Buka **Power BI Desktop** > **Get Data** > Pilih **PostgreSQL database**.
2. Isi Server: `localhost` dan Database: `Business_Intelegent_Project_v2`. (User: `openpg`, Pass: `openpgpwd`).
3. Cari folder/skema **`mart`** dan centang tabel *fact* dan *dim*. Klik **Load**.
4. Buka **Model View** di Power BI. Tarik garis relasi (**1-to-Many / 1:***) dari tabel Dimension ke Fact.
   - *Contoh:* Tarik `sk_product_id` dari `mart dim_product` ke `product_id` di `mart fact_sales`.
   - *Penjelasan:* Relasi ini wajib agar saat kita menekan filter produk, data transaksi penjualan terpotong dengan benar tanpa duplikasi.

### TAHAP B: Pembuatan Rumus DAX (Data Analysis Expressions)
Buat *New Measure* satu per satu. Pastikan nama tabel selalu diapit tanda kutip tunggal jika ada spasi, contoh: `'mart fact_sales'`.

**1. Basic KPI (Keuangan Dasar)**
- `Total Revenue = SUM('mart fact_sales'[revenue])` *(Menghitung total uang masuk)*
- `Total Cost = SUM('mart fact_sales'[cost])` *(Menghitung modal/harga pokok penjualan)*
- `Total Margin = SUM('mart fact_sales'[margin])` *(Keuntungan kotor)*
- `Margin % = DIVIDE([Total Margin], [Total Revenue], 0)` *(Persentase profit)*
- `Total Purchase Value = SUM('mart fact_purchase'[subtotal])` *(Total uang keluar untuk beli barang)*

**2. Inventory & Supply Chain**
- `Avg Lead Time Days = AVERAGE('mart fact_purchase'[lead_time_days])` *(Rata-rata waktu tunggu barang datang)*
- `Total Sales Qty = SUM('mart fact_sales'[quantity])`
- `Total Purchase Qty = SUM('mart fact_purchase'[quantity])`
- `Inventory Qty`: *(Banyaknya barang fisik di gudang)*
  ```dax
  Inventory Qty = 
  CALCULATE(SUM('mart fact_inventory'[quantity]), 'mart fact_inventory'[movement_type] = "incoming") - 
  CALCULATE(SUM('mart fact_inventory'[quantity]), 'mart fact_inventory'[movement_type] = "outgoing")
  ```
- `Inventory Value`: *(Nilai Rupiah dari barang yang mengendap di gudang)*
  ```dax
  Inventory Value = 
  CALCULATE(SUM('mart fact_inventory'[value]), 'mart fact_inventory'[movement_type] = "incoming") - 
  CALCULATE(SUM('mart fact_inventory'[value]), 'mart fact_inventory'[movement_type] = "outgoing")
  ```

**3. Advanced Decision Logic (Sistem Pendukung Keputusan)**
Rangkaian *measure* ini membuat Power BI cerdas dalam memberikan rekomendasi order:
- `3M MA Demand`: *(Prediksi kebutuhan barang berdasarkan rata-rata 3 bulan ke belakang untuk mencegah Panic Buying)*
  ```dax
  3M MA Demand = 
  AVERAGEX(DATESINPERIOD('mart dim_date'[full_date], MAX('mart dim_date'[full_date]), -3, MONTH), [Total Sales Qty])
  ```
- `Avg Daily Sales = DIVIDE([3M MA Demand], 30, 0)`
- `Safety Stock = [Avg Daily Sales] * 5` *(Stok penyangga aman 5 hari)*
- `ROP (Reorder Point) = ([Avg Daily Sales] * [Avg Lead Time Days]) + [Safety Stock]` *(Batas minimum gudang sebelum harus beli lagi)*
- `Recommended Order`: *(Saran jumlah barang yang harus dibeli kepada manajemen)*
  ```dax
  Recommended Order = 
  IF([Inventory Qty] <= [ROP], MAX([3M MA Demand] - [Inventory Qty], 0), 0)
  ```
- `Action Status`: *(Label warna untuk visual)*
  ```dax
  Action Status = 
  IF([Inventory Qty] = 0, "🔴 Stockout - Urgent Order",
      IF([Inventory Qty] <= [ROP], "🟡 Reorder Needed",
          "🟢 Optimal"
      )
  )
  ```

### TAHAP C: Perakitan Visualisasi (6 Halaman Dashboard)

**Halaman 1: Executive Dashboard (Kesehatan Finansial)**
- **Slicer (Filter):** Masukkan `year` dan `month_name` dari `mart dim_date`.
- **Card KPI:** Tarik `Total Revenue`, `Total Margin`, dan `Total Purchase Value`.
- **Line Chart (Tren):** X-axis: `full_date`. Y-axis: Tarik `Total Revenue`. Secondary Y-axis: Tarik `Total Purchase Value`. (Ini akan memperlihatkan lonjakan grafik pembelian merah akibat kepanikan di bulan Mei).

**Halaman 2: Sales Dashboard (Produk & Klien Terlaris)**
- **Clustered Bar Chart:** Y-axis: `customer_name`. X-axis: `Total Revenue`. (Siapa klien terbesar kita).
- **Donut Chart:** Legend: `product_name`. Values: `Total Revenue`. Filter visual untuk **Top 5** produk saja agar tidak terlalu padat.

**Halaman 3: Purchase Dashboard (Kinerja Vendor)**
- **Scatter Plot:** X-axis: `Total Purchase Value`. Y-axis: `Avg Lead Time Days`. Values/Details: `vendor_name`. 
  *(Tip: Ubah X-axis ke Logarithmic Scale di menu Format. Vendor yang berada di posisi atas adalah vendor yang sering telat mengirim barang dan menyebabkan krisis!).*

**Halaman 4: Inventory Dashboard (Evaluasi Stok)**
- **Matrix (Tabel Silang):** Rows: `product_name`. Values: `Inventory Qty` dan `Inventory Value`.
- Berikan **Conditional Formatting** (Background Color) pada angka Inventory Value terbesar untuk menyoroti produk yang menyedot kas (*Overstock*).

**Halaman 5: Forecast Dashboard (Peredam Kepanikan)**
- **Line & Clustered Column Chart:** X-axis: `month_name`. Column y-axis: `Total Sales Qty`. Line y-axis: `3M MA Demand`.
- *(Grafik ini membuktikan bahwa manajemen seharusnya tidak melakukan pembelian berlebihan di bulan Mei, karena permintaan aktual (garis MA) sebenarnya stabil).*

**Halaman 6: Decision Dashboard (Rekomendasi Pintar)**
- **Table (Tabel Biasa):** Tarik secara berurutan: `product_name`, `Inventory Qty`, `ROP`, `Recommended Order`, dan `Action Status`.
- Lakukan **Conditional Formatting** (Background Color) pada kolom `Action Status`. Atur warna Merah jika *Stockout*, Kuning jika *Reorder Needed*.
- *(Halaman ini adalah produk akhir Sistem Pendukung Keputusan. Manajemen hanya perlu membuka tabel ini setiap hari untuk tahu barang apa yang harus dibeli!).*

---
*Dokumen ini merupakan hasil rangkuman utuh (End-to-End) pembuatan Product 2 - Business Intelligence Decision Support System.*
