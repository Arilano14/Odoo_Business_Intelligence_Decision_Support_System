# 03. Visualization Mapping

Dokumen ini memetakan tujuan bisnis (Business Goals) ke dalam bentuk representasi visual di Power BI. Sesuai prinsip *Business Intelligence*, pemilihan chart/visual tidak boleh acak, melainkan harus memiliki tujuan analitis yang jelas.

## A. Halaman 1: Executive Dashboard

| Business Question | Visual Type | Data Fields / Measures | Analisis & Tujuan |
| :--- | :--- | :--- | :--- |
| Bagaimana kesehatan finansial secara makro? | **KPI Card / Multi-row Card** | Total Revenue, Total Purchase, Inventory Value, Margin % | Memberikan pandangan langsung (*at-a-glance*) tentang skala bisnis saat ini. |
| Bagaimana tren pertumbuhan dari waktu ke waktu? | **Line Chart** | X: Month<br>Y1: Total Revenue<br>Y2: Total Purchase | Melihat korelasi waktu antara tren penjualan vs pembelian. (Diharapkan melihat *spike* purchase di bulan Mei). |
| Apakah profitabilitas terjaga tiap bulannya? | **Waterfall Chart** | Category: Month<br>Y: Margin | Menunjukkan kontribusi naik/turun margin per bulan. |

---

## B. Halaman 2: Sales Dashboard

| Business Question | Visual Type | Data Fields / Measures | Analisis & Tujuan |
| :--- | :--- | :--- | :--- |
| Produk mana yang menjadi tulang punggung penjualan? | **Pareto Chart (Line and Clustered Column)** | X: Product Name<br>Column: Total Revenue<br>Line: % Cumulative | Mengidentifikasi 20% produk yang menyumbang 80% pendapatan (Hukum Pareto). |
| Siapa pelanggan terbesar perusahaan? | **Bar Chart (Horizontal)** | Y: Customer Name<br>X: Total Revenue | Fokus retensi pelanggan B2B (Top 10 Customers). |
| Bagaimana komposisi pendapatan per kategori produk? | **Donut Chart** | Legend: Category<br>Values: Total Revenue | Melihat porsi *market share* dari kategori produk tambang/konstruksi. |

---

## C. Halaman 3: Purchase Dashboard

| Business Question | Visual Type | Data Fields / Measures | Analisis & Tujuan |
| :--- | :--- | :--- | :--- |
| Vendor mana yang paling diandalkan? | **Bar Chart (Horizontal)** | Y: Vendor Name<br>X: Total Purchase Value | Identifikasi ketergantungan pada vendor tertentu. |
| Apakah ada anomali pembelian (Panic Buying)? | **Area Chart** | X: Month<br>Y: Total Purchase Qty | Mengidentifikasi bulan terjadinya *over-purchasing* (seperti Mei-Juni) akibat ketakutan stok kosong. |
| Berapa lama rata-rata Lead Time per Vendor? | **Scatter Plot** | X: Total Purchase Value<br>Y: Avg Lead Time<br>Details: Vendor Name | Menentukan vendor mana yang transaksinya besar tapi sering terlambat (*high risk*). |

---

## D. Halaman 4: Inventory Dashboard

| Business Question | Visual Type | Data Fields / Measures | Analisis & Tujuan |
| :--- | :--- | :--- | :--- |
| Apakah persediaan terlalu menumpuk (Overstock)? | **Gauge Chart** | Value: DIO<br>Target: 30 days (Max 60) | Memantau *Days Inventory Outstanding*. Jika > 90 hari, modal tertahan. |
| Seberapa cepat barang keluar dari gudang? | **Line Chart** | X: Month<br>Y: ITR (Inventory Turnover) | Tren kecepatan perputaran stok. Menurun saat *overstock* di bulan Juli. |
| Produk apa saja yang terjebak di gudang (Slow Moving)? | **Matrix (Table)** | Rows: Product Name<br>Values: Inventory Qty, DIO | Daftar *actionable* bagi tim gudang untuk melihat produk apa yang macet. |

---

## E. Halaman 5: Forecast Dashboard

| Business Question | Visual Type | Data Fields / Measures | Analisis & Tujuan |
| :--- | :--- | :--- | :--- |
| Apa estimasi permintaan bulan depan? | **Line Chart (dengan Forecast Line)** | X: Month<br>Y: 3M MA Demand | Menggunakan *Moving Average* untuk menghaluskan fluktuasi *spike* (seperti April) agar prediksi lebih stabil. |
| Bagaimana perbandingan Historis vs Prediksi? | **Clustered Column Chart** | X: Month<br>Y1: Total Sales Qty<br>Y2: 3M MA Demand | Evaluasi visual dari akurasi peramalan. |

---

## F. Halaman 6: Decision Dashboard

| Business Question | Visual Type | Data Fields / Measures | Analisis & Tujuan |
| :--- | :--- | :--- | :--- |
| Produk apa yang harus segera dibeli hari ini? | **Table (Conditional Formatting)** | Rows: Product Name<br>Values: Inventory Qty, ROP, Recommended Order, Action Status | Matriks keputusan utama. Jika Action Status = "🟡 Reorder Needed", warna kuning. "🔴 Stockout" merah. |
| Vendor mana yang harus dihindari/ditegur? | **Table** | Rows: Vendor Name<br>Values: Avg Lead Time, Supplier Reliability | Menyortir vendor dengan status "Poor (Delay Risk)" untuk dilakukan pembinaan. |
| Narasi Rekomendasi Eksekutif | **Smart Narrative / Text Box** | [Teks Dinamis] | Rangkuman tertulis otomatis: "Saat ini ada X produk mengalami Stockout, dan Y produk butuh Reorder." |
