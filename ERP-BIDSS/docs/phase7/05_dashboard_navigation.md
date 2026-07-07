# 05. Dashboard Navigation & Interaction

Dokumen ini menjelaskan alur interaksi pengguna (UX/UI Interaction) di dalam Power BI, memastikan bahwa seluruh dashboard dapat ditelusuri (*drilled down*) hingga ke akar masalah (Root Cause).

## 1. Page Navigation (Left Sidebar)
Navigasi antar halaman dilakukan melalui panel kiri. Setiap tombol di sidebar menggunakan *Action Type: Page Navigation* di Power BI.
- **🏠 Executive**
- **📈 Sales**
- **🛒 Purchase**
- **📦 Inventory**
- **🔮 Forecast**
- **💡 Decision**

## 2. Global Slicers (Sync Slicers)
Slicer berikut diletakkan di *Executive Dashboard* dan disinkronkan (*Sync Slicers*) ke halaman lain agar konteks waktu & kategori tidak hilang saat pengguna berpindah halaman.
- **Year** (dari `dim_date[year]`)
- **Month** (dari `dim_date[month_name]`)
- **Category** (dari `dim_product[category]`)

## 3. Cross-Filtering & Cross-Highlighting
Standard interaksi Power BI di mana mengklik satu elemen di grafik akan memfilter grafik lain.
- *Aturan Khusus*: Pada **Purchase Dashboard**, klik pada batang *Vendor Name* (di Bar Chart) harus melakukan **Cross-Filter** (bukan sekadar *Highlight*) pada Scatter Plot (Lead Time) untuk mengisolasi titik vendor tersebut agar mudah dibaca. Edit interaksi ini melalui `Format > Edit Interactions`.

## 4. Drill Through
Fitur ini memungkinkan manajemen melihat level transaksi mentah langsung dari grafik agregat.
- **Target Page**: Buat satu *Hidden Page* bernama `[Detail Transaksi]`.
- **Drill Through Fields**: `Product Name`, `Customer Name`, `Vendor Name`.
- **Skenario Penggunaan**:
  1. Di *Inventory Dashboard*, manajer melihat produk "Bulldozer" mengalami Overstock.
  2. Klik Kanan pada "Bulldozer" > Drill Through > *Detail Transaksi*.
  3. Halaman berpindah ke tabel mentah (Fact Table) yang memperlihatkan daftar tanggal pembelian (PO) dan penjualan (SO) historis untuk Bulldozer.

## 5. Tooltips (Custom Page Tooltips)
Jangan gunakan Tooltip bawaan yang hanya menampilkan angka monoton.
- **Custom Tooltip 1 (Sales Info)**: Saat *hover* di Bar Chart produk, munculkan tooltip berisi gambar produk (opsional), Margin %, dan tren penjualan 3 bulan terakhir.
- **Custom Tooltip 2 (Vendor Info)**: Saat *hover* di Vendor, munculkan *Average Lead Time* dan *Reliability Status*.

## 6. Bookmarks (State Saving)
- Di *Decision Dashboard*, buat 3 tombol Bookmark untuk mengubah filter cepat di Matrix Tabel:
  - Tombol **[Urgent (Stockout)]**: Mengaktifkan bookmark dengan filter `Action Status = "🔴 Stockout - Urgent Order"`.
  - Tombol **[Warning (Reorder)]**: Bookmark untuk filter `🟡 Reorder Needed`.
  - Tombol **[Overstock]**: Bookmark untuk filter `🔵 Overstock - Hold Order`.
- Ini mempermudah eksekutif tanpa harus mencari menu *Filter Pane* di samping.
