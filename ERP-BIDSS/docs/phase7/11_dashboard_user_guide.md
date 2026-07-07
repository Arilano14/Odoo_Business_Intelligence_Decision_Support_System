# 11. Dashboard User Guide

Selamat datang di **OBIDSS Enterprise Intelligence Dashboard**. 
Panduan ini dirancang untuk tim Manajemen dan Eksekutif agar dapat memaksimalkan penggunaan dashboard dalam mengambil keputusan strategis sehari-hari, bukan sekadar melihat laporan lampau.

## Memulai Navigasi
Saat pertama kali membuka Dashboard (atau melihatnya melalui proyektor/layar presentasi), Anda akan disambut oleh **Executive Dashboard**.
- Di sisi **Kiri**, terdapat deretan Ikon Navigasi. Klik ikon tersebut untuk berpindah antar halaman secara mulus layaknya sebuah aplikasi website.
- Di **Pojok Kanan Atas**, terdapat **Global Filter**. Gunakan filter ini untuk menyaring laporan berdasarkan Tahun atau Bulan tertentu. Filter ini akan *terbawa* ke halaman lain secara otomatis.

---

## Panduan per Peran (Role-Based Usage)

### 1. Untuk Direktur Utama (C-Level Executive)
**Halaman Favorit:** `Executive Dashboard`
- **Cara Baca:** Fokus pada 4 angka besar (KPI Cards) di bagian atas. Ini adalah detak jantung perusahaan Anda.
- **Tindakan (Action):** Jika garis tren antara *Revenue* (Biru) dan *Purchase* (Merah) di grafik tengah saling menjauh tak wajar (seperti kejadian di bulan Mei), segera panggil Manajer Pembelian dan Penjualan untuk klarifikasi.

### 2. Untuk Manajer Penjualan (Sales Manager)
**Halaman Favorit:** `Sales Dashboard`
- **Cara Baca:** Perhatikan *Pareto Chart* di tengah. Itu adalah 20% produk unggulan yang menghidupi perusahaan.
- **Fitur Khusus (Drill Through):** Jika melihat seorang Klien/Customer tiba-tiba pembeliannya menurun, klik kanan pada nama pelanggan tersebut lalu pilih **Drill Through > Detail Transaksi**. Anda dapat melihat histori nota pembeliannya dan meneruskannya ke tim Sales lapangan untuk dilakukan *follow-up/retention call*.

### 3. Untuk Manajer Pengadaan (Procurement Manager)
**Halaman Favorit:** `Purchase Dashboard` & `Decision Dashboard`
- **Cara Baca:** Anda tidak perlu lagi menebak jumlah barang yang akan habis. Buka *Decision Dashboard* setiap pagi hari.
- **Tindakan Cepat:** 
  1. Klik tombol **[Urgent / Warning]** di bagian atas halaman Decision.
  2. Tabel akan menyusut hanya menampilkan produk yang harus dipesan HARI INI (karena sudah menyentuh *Reorder Point* / ROP).
  3. Lihat kolom *Recommended Order*. Itulah jumlah spesifik (EOQ) yang harus diinput ke dalam sistem Odoo ERP Anda.
  4. Lihat tabel *Supplier Score* di bawahnya untuk menghindari memesan dari Vendor yang rawan terlambat (*High Risk*).

### 4. Untuk Manajer Gudang (Warehouse Manager)
**Halaman Favorit:** `Inventory Dashboard`
- **Cara Baca:** Fokus pada *Gauge Chart* (DIO - Days Inventory Outstanding). Angka normal industri adalah 30-45 hari. Jika jarum menunjuk angka > 90 hari, gudang Anda macet.
- **Tindakan (Action):** Lihat tabel *Slow Moving* di pojok kanan bawah. Cetak daftar tersebut dan berikan kepada tim *Sales* atau *Marketing* sebagai daftar produk yang wajib segera dihabiskan via promosi cuci gudang (*clearance*), agar ruang fisik gudang lega kembali.

---

## Tips & Trik Interaktivitas

1. **Gunakan Cross-Filtering:** Jangan ragu untuk meng-klik batang (*bar*), irisan (*pie slice*), atau titik pada grafik. Power BI secara ajaib akan mengubah seluruh tampilan di halaman tersebut agar fokus hanya pada elemen yang Anda klik. Klik kembali elemen tersebut untuk membatalkan filter (Reset).
2. **Hover Tooltips:** Arahkan kursor (*mouse*) diam di atas elemen visual yang menarik. Sebuah kotak kecil akan muncul memberikan rincian tambahan (seperti persentase margin atau riwayat 3 bulan) tanpa perlu pindah halaman.
3. **Reset to Default:** Jika layar menjadi kosong atau terlalu sempit karena terlalu banyak filter, gunakan ikon/tombol "Reset Filter" di pojok kanan atas untuk mengembalikan tampilan ke keadaan semula (menampilkan seluruh data).
