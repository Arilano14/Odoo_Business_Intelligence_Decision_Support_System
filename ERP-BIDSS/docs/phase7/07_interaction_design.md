# 07. Interaction Design & User Experience

Dokumen ini menjelaskan rancangan UI/UX (User Interface / User Experience) lanjutan di dalam Power BI agar dashboard terasa seperti sebuah aplikasi *Enterprise*, bukan sekadar kumpulan lembar grafik statis.

## 1. Global Filter Panel (Slicer Pane)
Jangan menebar filter di sembarang tempat. 
- Buat sebuah **Filter Pane** (panel khusus filter) di sebelah kiri atau kanan halaman (bisa menggunakan bentuk/Shape memanjang sebagai *background*).
- Panel ini berisi:
  1. `Year` (Dropdown)
  2. `Month` (Dropdown)
  3. `Product Category` (Dropdown)
  4. `Supplier Name` (Dropdown)
  5. `Customer Name` (Dropdown)
- **Advanced UX (Expand/Collapse)**: Gunakan fitur *Bookmarks* dan *Buttons* (Ikon Filter) untuk memunculkan (Show) atau menyembunyikan (Hide) panel filter ini guna menghemat ruang kanvas utama.

## 2. Cross-Highlighting vs Cross-Filtering
- **Default Power BI**: Mengklik batang A pada grafik B akan "meredupkan" (Highlight) data yang tidak relevan.
- **Rekomendasi OBIDSS**: Ubah interaksi default menjadi **Cross-Filtering** (Format > Edit Interactions > Pilih ikon Filter). Ini membuat grafik lain benar-benar disaring (*resize*) sehingga tren lebih jelas terbaca tanpa warna redup yang membingungkan.

## 3. Custom Tooltips (Report Page Tooltips)
Tooltips standar Power BI kotak hitam dinilai kurang informatif.
- Buat halaman khusus (Hidden Page) dengan *Page Size: Tooltip*.
- **Tujuan**: Saat eksekutif meng-*hover* mouse ke atas sebuah produk di "Top 10 Products Bar Chart", sebuah mini-dashboard akan melayang (pop-up).
- **Isi Tooltip Pop-up**:
  - Nama Produk & Kategori.
  - Line Chart tren pendapatan (Revenue) produk tersebut selama 3 bulan terakhir.
  - Margin %.
- Aktifkan ini di visual utama melalui `Format > General > Tooltips > Page: [Nama Halaman Tooltip]`.

## 4. Conditional Formatting (Visual Cues)
Pengguna tidak boleh dibiarkan menebak apakah angka 1.5M itu "Bagus" atau "Buruk".
- **Matrix Tabel**: Gunakan *Background Color* atau *Font Color* pada kolom `Action Status`.
  - `Stockout` = Merah Muda
  - `Reorder` = Kuning Muda
  - `Optimal` = Hijau Muda
  - `Overstock` = Biru Muda
- **KPI Card**: Angka `Growth %` harus berwarna Hijau jika > 0, dan Merah jika < 0.

## 5. Drill Through (Root Cause Analysis)
Sediakan jalur penelusuran (traceability) dari Grafik Agregat ke Tabel Transaksional.
- Eksekutif melihat "PT Tambang Konstruksi 1" memiliki kontribusi *Revenue* menurun.
- Ia **Klik Kanan > Drill Through > Transaction Detail**.
- Membuka halaman tersembunyi yang berisi tabel *flat* (Fact Table records): `Date | SO Number | Product | Qty | Price | Subtotal`.
- Hal ini menjembatani gap antara "Business Insight" dan "ERP Transaction".
