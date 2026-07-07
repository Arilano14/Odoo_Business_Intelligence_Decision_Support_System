# 08. Visual Standard (Theme & Typography)

Untuk menyajikan nuansa **Enterprise**, Power BI Dashboard tidak boleh menggunakan skema warna default (*clashing colors*). Keseragaman warna membantu audiens (manajemen) membaca data lebih cepat secara intuitif.

## 1. Color Palette (Skema Warna)
Tema dashboard harus mencerminkan identitas korporat (industri berat/distributor).

- **Primary Color (Brand)**: `Dark Navy Blue` (#1C325B) — Untuk Header, Navigation Bar, dan aksen elemen utama.
- **Secondary Color (Neutral)**: `Steel Gray` (#7A8B99) — Untuk garis grid, teks sumbu (axis), dan border.
- **Background Color**: `Off-White` (#F4F7F6) — Untuk *canvas* agar mata tidak cepat lelah (jangan gunakan putih murni #FFFFFF).
- **Positive/Good**: `Teal Green` (#2E7D32) — Untuk pertumbuhan (Growth > 0), margin profit, status Optimal.
- **Negative/Bad**: `Crimson Red` (#C62828) — Untuk Stockout, Growth < 0, Poor Reliability.
- **Warning/Hold**: `Amber/Orange` (#F57C00) — Untuk Reorder Needed, Delay Warning.
- **Info/Hold**: `Light Blue` (#0277BD) — Untuk Overstock.

## 2. Typography (Tipografi)
Gunakan *font family* yang modern, bersih (sans-serif), dan memiliki hierarki bobot (*weight*) yang jelas.

- **Global Font**: `Segoe UI` (Bawaan Windows/Power BI terbaik) atau `DIN`.
- **Dashboard Title**: 24pt, Segoe UI Bold, Warna Putih (jika Header Biru Gelap).
- **Visual Title (Judul Grafik)**: 12pt, Segoe UI Semibold, Warna Hitam/Abu Tua.
- **Data Labels & Axis**: 9pt atau 10pt, Segoe UI Regular, Warna Steel Gray.
- **KPI Card Values**: 28pt-32pt, Segoe UI Light atau Bold (tergantung penekanan).

## 3. Visual Styling (Gaya Desain)
- **Shadows & Borders**: Aktifkan fitur *Shadow* pada semua *Visual Cards* (Background Putih, Shadow Abu-abu transparan, posisi Outer-Bottom-Right). Ini memberikan efek "Card" atau elevasi (Material Design) dari latar belakang *Off-White*.
- **Rounded Corners**: Ubah *Visual Border Radius* menjadi `4px` hingga `8px` agar desain tidak terlalu kaku dan kotak.
- **Blank Spaces**: Biarkan jarak (padding) antara satu grafik dengan grafik lain. Jangan menumpuk batas grafik tanpa jeda (*white space*).

## 4. Format Angka (Data Formatting)
- **Currency**: Gunakan awalan `Rp` atau `$` (jika data simulasi internasional), dengan singkatan jutaan/miliaran (contoh: `Rp 15.4M` atau `Rp 1.2B`). Di Power BI, atur *Display units* ke *Millions*.
- **Persentase**: Selalu gunakan 1 atau 2 angka di belakang koma (contoh: `12.5%`, bukan `12.5432%`).
- **Desimal (Kuantitas)**: Gunakan pembatas ribuan (`1,250`) tanpa desimal untuk barang berwujud (*physical units*).
