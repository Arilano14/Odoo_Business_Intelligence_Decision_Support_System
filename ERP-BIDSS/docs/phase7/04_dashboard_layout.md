# 04. Dashboard Layout

Dokumen ini mendefinisikan *wireframe* atau *grid system* untuk setiap halaman dashboard Power BI. Grid system yang rapi (Z-Pattern atau F-Pattern) penting agar *eye-tracking* pengguna (manajer/eksekutif) langsung tertuju pada KPI utama, lalu turun ke detail analitik.

## Global Layout (Konsisten untuk Semua Halaman)

Setiap halaman (kecuali diinstruksikan lain) harus mengikuti tata letak standar berikut:

### 1. Header (Top Bar - Tinggi: 10%)
- **Kiri**: Logo Perusahaan / Nama Aplikasi (e.g., *OBIDSS Enterprise Intelligence*).
- **Tengah**: Judul Halaman (e.g., *Executive Dashboard*, *Inventory Dashboard*).
- **Kanan**: Timestamp Update Terakhir & Slicer Global (Year, Month).

### 2. Navigation Sidebar (Left Bar - Lebar: 10-15%)
- Berisi ikon navigasi ke 6 halaman utama (Executive, Sales, Purchase, Inventory, Forecast, Decision).
- Berfungsi ganda sebagai *Visual Filter* jika dibutuhkan (menggunakan fitur *Page Navigation* dari *Buttons*).

### 3. KPI Banner (Atas, di bawah Header - Tinggi: 15-20%)
- Terdiri dari 4-5 elemen **Card Visual**.
- Selalu letakkan matriks terpenting di paling kiri (Z-Pattern).
- Contoh: `[ Total Revenue ]` `[ Total Margin ]` `[ Total Purchase ]` `[ Inventory Value ]` `[ YTD Growth ]`

### 4. Main Canvas (Tengah & Bawah - Sisa Ruang)
- **Top Half (Visual Makro/Tren)**: Biasanya Line Chart, Area Chart, atau Waterfall Chart yang memakan ruang horizontal lebar untuk melihat fluktuasi waktu.
- **Bottom Half (Visual Mikro/Detail)**: Bar Chart (Top 10), Matrix/Tabel rincian, atau Scatter Plot. Dibagi menjadi 2 atau 3 kolom.

---

## Wireframe per Halaman

### Halaman 1: Executive Dashboard
- **Top (KPI)**: Revenue, Margin, Purchase, Inventory Value.
- **Middle (Trend)**: Line Chart (Revenue vs Purchase by Month).
- **Bottom-Left**: Waterfall Chart (Margin by Month).
- **Bottom-Right**: Donut Chart (Revenue by Category).

### Halaman 2: Sales Dashboard
- **Top (KPI)**: Total Sales, Total Customer, Avg Ticket Size, Growth MoM.
- **Middle (Trend)**: Pareto Chart (Top Products 80/20 Rule).
- **Bottom-Left**: Horizontal Bar Chart (Top 10 Customers).
- **Bottom-Right**: Matrix Table (Sales Detail).

### Halaman 3: Purchase Dashboard
- **Top (KPI)**: Total Purchase Qty, Total Purchase Value, Avg Lead Time, Outstanding PO.
- **Middle (Trend)**: Area Chart (Purchase Quantity over Time - sorot lonjakan bulan Mei).
- **Bottom-Left**: Horizontal Bar (Top 10 Vendors).
- **Bottom-Right**: Scatter Plot (Vendor Volume vs Lead Time Risk).

### Halaman 4: Inventory Dashboard
- **Top (KPI)**: Inventory Value, ITR (Inventory Turnover), DIO (Days Inventory Outstanding), Total Items.
- **Middle (Trend)**: Line Chart (ITR and DIO Trend per Month - sorot kejatuhan di Juli).
- **Bottom-Left**: Gauge Chart (Current DIO vs Target 30).
- **Bottom-Right**: Matrix (Slow Moving & Dead Stock List).

### Halaman 5: Forecast Dashboard
- **Top (KPI)**: 3M MA Demand, Forecast Purchase, Variance, Accuracy %.
- **Middle (Trend)**: Line & Clustered Column (Historical Sales vs 3M MA Forecast).
- **Bottom (Table)**: Forecast Output Table (Bulan Depan, Prediksi Kebutuhan, Estimasi Modal).

### Halaman 6: Decision Dashboard (Actionable Board)
- **Top (Text)**: Smart Narrative ("Peringatan: 5 Produk Stockout, 12 Produk butuh Reorder").
- **Main Body**: Matriks Besar / Tabel Conditional Formatting.
  - Kolom: Product, Current Stock, ROP, EOQ, Recommended Order, **Action Status**.
  - Warna: Merah (Urgent), Kuning (Warning), Hijau (Safe), Biru (Hold/Overstock).
- **Bottom Panel**: Vendor Recommendation (Siapa yang harus dihubungi untuk pemesanan darurat berdasarkan *Reliability Score*).
