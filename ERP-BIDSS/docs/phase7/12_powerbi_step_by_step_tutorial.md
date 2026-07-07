# 12. Tutorial Lengkap Pembuatan Dashboard Power BI (Dari Nol hingga Selesai)

Dokumen ini adalah panduan *"Click-by-Click"* (langkah demi langkah) yang sangat mudah dipahami untuk merakit **Enterprise Intelligence Dashboard** PT Penjualan Alat Berat di Power BI Desktop. Anda tidak perlu jago *coding*, cukup ikuti panduan ini dari Langkah 1 sampai Selesai!

---

## TAHAP 1: Menghubungkan Data (Get Data)
Tujuan: Memasukkan tabel dari database PostgreSQL ke dalam Power BI.

1. Buka aplikasi **Power BI Desktop**.
2. Klik tombol **Get Data** (ikon database) di menu atas.
3. Klik **More...** di paling bawah, lalu ketik `PostgreSQL` di kotak pencarian.
4. Pilih **PostgreSQL database** dan klik **Connect**.
5. Isi kotak yang muncul dengan:
   - **Server**: `localhost`
   - **Database**: `Business_Intelegent_Project_v2`
   - **Data Connectivity mode**: Pilih **Import**.
6. Klik **OK**. Jika diminta *Username* dan *Password*, gunakan tab **Database** (bukan Windows), lalu isi:
   - **User name**: `openpg`
   - **Password**: `openpgpwd`
7. Jendela *Navigator* akan muncul. Buka folder database Anda, lalu cari folder/skema bernama **`mart`**.
8. **Centang 10 tabel berikut**:
   - `dim_company`, `dim_customer`, `dim_date`, `dim_product`, `dim_vendor`, `dim_warehouse`
   - `fact_accounting`, `fact_inventory`, `fact_purchase`, `fact_sales`
9. Klik tombol **Load** di kanan bawah. Tunggu proses *loading* selesai.

---

## TAHAP 2: Menghubungkan Tabel (Star Schema)
Tujuan: Memberitahu Power BI bagaimana tabel-tabel tersebut saling berhubungan.

1. Lihat deretan 3 ikon di sisi kiri layar Power BI. Klik ikon yang paling bawah (**Model view** / ikon susunan kotak).
2. Anda akan melihat kotak-kotak tabel Anda berserakan. Letakkan tabel berawalan **`fact_`** di tengah, dan tabel berawalan **`dim_`** mengelilinginya.
3. **Cara menyambungkan (Relasi 1-to-Many / 1:*)**: Klik, tahan (drag), lalu lepaskan (drop) nama kolom dari tabel `dim_` ke tabel `fact_`. Tarik garis-garis berikut:
   - Tarik `date_id` dari **dim_date** ke `date_id` di **fact_sales**
   - Tarik `date_id` dari **dim_date** ke `date_id` di **fact_purchase**
   - Tarik `date_id` dari **dim_date** ke `date_id` di **fact_inventory**
   - Tarik `sk_product_id` dari **dim_product** ke `product_id` di **fact_sales**
   - Tarik `sk_product_id` dari **dim_product** ke `product_id` di **fact_purchase**
   - Tarik `sk_product_id` dari **dim_product** ke `product_id` di **fact_inventory**
   - Tarik `sk_customer_id` dari **dim_customer** ke `customer_id` di **fact_sales**
   - Tarik `sk_vendor_id` dari **dim_vendor** ke `vendor_id` di **fact_purchase**
4. **Validasi Kardinalitas (Cardinality)**: Pastikan semua garis relasi yang terbentuk memiliki angka **1** di sisi tabel Dimension (`dim_`) dan tanda bintang **(*)** di sisi tabel Fact (`fact_`). Arah panah (Cross filter direction) harus menunjuk dari Dimension ke Fact (Single).
   - *Alasan*: Tabel Dimension berisi data master yang unik (satu baris per produk/tanggal = **1**). Sedangkan tabel Fact berisi data transaksi di mana satu produk bisa terjual berkali-kali (banyak baris = **\***). Relasi **1-to-Many (1:*)** ini wajib dipatuhi (*best practice* Star Schema) agar saat Anda melakukan filter (misalnya filter Kategori Produk), filter tersebut mengalir searah dengan benar ke tabel transaksi tanpa menimbulkan error *many-to-many* atau duplikasi angka.
5. Selesai! Power BI sekarang mengerti bahwa data transaksi terhubung dengan data master secara hirarkis.

---

## TAHAP 3: Membuat Rumus Perhitungan (DAX Measures)
Tujuan: Membuat kalkulator otomatis untuk Revenue, Margin, dll.

1. Kembali ke **Report view** (ikon paling atas di sisi kiri).
2. Di panel **Data** sebelah kanan, klik Kanan pada tabel **`mart fact_sales`**, lalu pilih **New measure**.
3. Di *formula bar* (bagian atas kanvas), ketik/paste rumus berikut, lalu tekan Enter:
   `Total Revenue = SUM('mart fact_sales'[revenue])`
4. Ulangi langkah (Klik Kanan > New Measure) untuk rumus-rumus penting berikut (Anda bisa menaruhnya di tabel *Fact* mana saja, tapi disarankan sesuai konteksnya):
   - `Total Margin = SUM('mart fact_sales'[margin])`
   - `Margin % = DIVIDE([Total Margin], [Total Revenue], 0)`
   - `Total Purchase Qty = SUM('mart fact_purchase'[quantity])`
   - `Total Sales Qty = SUM('mart fact_sales'[quantity])`

> **💡 PENJELASAN ERROR "TIDAK DITEMUKAN"**: 
> Karena kita meng-import data dari skema `mart` di PostgreSQL, Power BI secara otomatis menempelkan kata `mart ` (dengan spasi) di depan semua nama tabel Anda. Oleh karena itu, nama tabel aslinya di Power BI adalah **`mart fact_sales`**, BUKAN `fact_sales`. Anda wajib menggunakan tanda kutip tunggal (`'mart fact_sales'`) di dalam rumus DAX Anda.
5. *(Untuk kumpulan rumus lengkap seperti Inventory Value, ROP, dan Forecast, silakan copy-paste dari file `02_dax_measure_catalog.md`)*.

---

## TAHAP 4: Membuat 6 Halaman Dashboard (Drag & Drop Visual)

Di bagian bawah layar, Anda bisa menekan tombol **(+)** untuk membuat halaman baru. Ganti nama halamannya.

### Halaman 1: Executive Dashboard
**Cerita:** Halaman ini melihat kesehatan perusahaan (Revenue vs Purchase).
1. **Buat Filter Global**: 
   - Klik ikon **Slicer** (visual berbentuk corong/filter) di panel Visualizations.
   - Tarik kolom `year` dan `month_name` dari tabel `dim_date` ke dalam slicer tersebut.
2. **Buat KPI Card (Angka Besar)**: 
   - Klik ikon **Card** (visual berlambang angka 123).
   - Tarik measure `Total Revenue` ke bagian Fields. Ulangi membuat kotak Card untuk `Total Margin` dan `Total Purchase`.
3. **Buat Grafik Tren**: 
   - Klik ikon **Line Chart**.
   - Tarik `full_date` (atau `month_name`) ke **X-axis**.
   - Tarik `Total Revenue` dan `Total Purchase` ke **Y-axis**. *(Catatan: Tarik keduanya ke dalam kotak Y-axis yang sama secara berurutan. Jika ditolak, pastikan kotak **Legend** kosong. Jika masih tidak bisa, tarik salah satunya ke **Secondary y-axis**).*
   *(Di sini Anda akan melihat fenomena lonjakan garis pembelian merah di bulan Mei)*.

### Halaman 2: Sales Dashboard
**Cerita:** Siapa pelanggan dan produk yang paling laku?
1. **Buat Bar Chart Pelanggan**:
   - Klik ikon **Clustered Bar Chart** (Batang horizontal).
   - Tarik `customer_name` (dari `dim_customer`) ke **Y-axis**.
   - Tarik `Total Revenue` ke **X-axis**.
2. **Buat Donut Chart Kategori**:
   - Klik ikon **Donut Chart**.
   - Tarik `category` (dari `dim_product`) ke **Legend**, dan `Total Revenue` ke **Values**.

### Halaman 3: Purchase Dashboard
**Cerita:** Kenapa barang telat? Siapa Vendornya?
1. **Buat Scatter Plot (Titik Koordinat)**:
   - Klik ikon **Scatter chart**.
   - Tarik `Total Purchase Value` ke **X-axis**.
   - Tarik `Avg Lead Time Days` (buat measure-nya dulu) ke **Y-axis**.
   - Tarik `vendor_name` ke **Values/Details**.
   *(Titik yang berada di kanan atas adalah vendor besar yang sering telat/bahaya! Ini adalah penyebab krisis di bulan Maret).*

### Halaman 4: Inventory Dashboard
**Cerita:** Barang apa yang menumpuk di gudang setelah panik belanja?
1. **Buat Tabel Evaluasi (Matrix)**:
   - Klik ikon **Matrix**.
   - Tarik `product_name` ke **Rows**.
   - Tarik `Inventory Qty` dan `DIO` (Days Inventory Outstanding) ke **Values**.
2. **Warnai Tabel (Conditional Formatting)**:
   - Klik kanan panah kecil di sebelah `DIO` di kotak Values > **Conditional formatting** > **Background color**.
   - Atur jika lebih besar dari `90` hari, beri warna Biru Terang (Tanda Overstock/Barang Mandek).

### Halaman 5: Forecast Dashboard
**Cerita:** Apa yang harus dibeli bulan depan agar tidak panik lagi?
1. **Buat Line & Clustered Column Chart**:
   - Tarik `month_name` ke **X-axis**.
   - Tarik `Total Sales Qty` ke **Column y-axis** (Ini data historis asli).
   - Tarik measure `3M MA Demand` ke **Line y-axis** (Ini adalah prediksi Moving Average).
   *(Garis ini memuluskan spike, memberi gambaran prediksi normal tanpa terbawa kepanikan bulan April).*

### Halaman 6: Decision Dashboard
**Cerita:** Keputusan Final! Beli atau Tahan?
1. **Buat Tabel Rekomendasi (Table)**:
   - Klik ikon **Table** (Tabel biasa).
   - Masukkan ke kotak **Columns** secara berurutan: `product_name`, `Inventory Qty`, `ROP`, `Recommended Order`, dan `Action Status`.
2. **Beri Warna Status (UX)**:
   - Lakukan *Conditional Formatting* pada kolom `Action Status`.
   - Atur aturan (Rules): Jika isi kolom sama dengan `"🔴 Stockout - Urgent Order"`, warnai latar menjadi Merah. Jika `"🟡 Reorder Needed"`, warnai Kuning.

---

## TAHAP 5: Finishing (Polesan Profesional)
1. **Tema Warna**: Buka tab **View** di menu atas Power BI, buka *Themes*, pilih tema biru gelap (seperti *City Park* atau *Executive*) agar lebih korporat.
2. **Interaksi (Cross-Filter)**: Coba klik salah satu bulan (misal: "April") di Filter. Perhatikan bagaimana *semua* grafik angka penjualan dan pembelian seketika merespons (turun/naik) secara otomatis. Inilah magisnya Power BI!
3. **Simpan Laporan**: Tekan **Ctrl + S** dan simpan dengan nama `Enterprise_Intelligence_Dashboard.pbix`.

**Selamat! Anda baru saja menyelesaikan sebuah Enterprise Intelligence Dashboard end-to-end yang mengisahkan Supply Shock & Recovery!**
