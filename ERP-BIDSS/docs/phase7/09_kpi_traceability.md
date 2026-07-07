# 09. KPI Traceability (Business Flow)

Dokumen ini adalah bukti akuntabilitas akademis dan profesional dari setiap grafik yang tampil di Dashboard. Jika manajemen (atau penguji magang) mempertanyakan "Dari mana angka ini berasal?", tabel ini adalah jawabannya.

Tujuan pelacakan (Traceability): **Odoo ERP Transaction → Fact Table → DAX Measure → Visualization → Business Insight → Decision.**

---

## 1. Traceability: Vendor Reliability (Purchase Dashboard)

| Tahapan | Bukti (Trace) | Deskripsi Teknis / Konteks Bisnis |
| :--- | :--- | :--- |
| **ERP Transaction** | `purchase.order` | Admin Procurement membuat PO di Odoo 18. Terdapat field `date_order` (Kapan dipesan) dan `date_planned` (Janji kapan tiba). |
| **Fact Table** | `mart.fact_purchase` | ETL Pipeline mengekstrak selisih hari antara `date_planned` dan `date_order` menjadi kolom `lead_time_days`. |
| **DAX Measure** | `[Avg Lead Time Days]` | Power BI menghitung rata-rata dari kolom tersebut per Vendor: `AVERAGE(fact_purchase[lead_time_days])`. |
| **Visualization** | Scatter Plot | Sumbu X = Total Nilai Pembelian, Sumbu Y = Avg Lead Time. |
| **Business Insight** | Titik Pencilan (*Outlier*) | Terlihat bahwa "Vendor A" mendapat pesanan bernilai tinggi namun sering telat (Avg Lead Time 10 hari). Ini adalah akar masalah (*root cause*) Stockout di bulan April. |
| **Decision** | Review Vendor | Kurangi kuota belanja dari Vendor A, cari *Supplier* lokal alternatif, atau kenakan penalti kontrak (SLA). |

---

## 2. Traceability: Slow Moving Product (Inventory Dashboard)

| Tahapan | Bukti (Trace) | Deskripsi Teknis / Konteks Bisnis |
| :--- | :--- | :--- |
| **ERP Transaction** | `stock.move` | Modul Inventory Odoo mencatat barang masuk (Receipt) dan barang keluar (Delivery) secara absolut saat divalidasi oleh kepala gudang. |
| **Fact Table** | `mart.fact_inventory` | ETL mengklasifikasikan `stock_move` menjadi `movement_type = incoming / outgoing`. Menghitung nilai aset absolut harian. |
| **DAX Measure** | `[ITR]` & `[DIO]` | `Total Cost` tahunan dibagi `[Inventory Value]` menghasilkan *Inventory Turnover Ratio*. Dikonversi ke hari (DIO = 365 / ITR). |
| **Visualization** | Matrix Table | Baris berisi Produk. Kolom berisi DIO. |
| **Business Insight** | Barang Menumpuk | Produk "Alat Berat Part 12" memiliki DIO 140 hari. Artinya, stok barang ini tidak bergerak selama hampir 5 bulan setelah diborong secara *panic buying* di bulan Mei. |
| **Decision** | Clearance / Promo | Berikan diskon khusus untuk produk tersebut agar segera menjadi kas tunai (*Cash Conversion*). |

---

## 3. Traceability: Predictive Procurement (Forecast Dashboard)

| Tahapan | Bukti (Trace) | Deskripsi Teknis / Konteks Bisnis |
| :--- | :--- | :--- |
| **ERP Transaction** | `sale.order.line` | Riwayat penjualan lampau terekam di Odoo setiap kali *Salesperson* mencetak invoice (*state = done*). |
| **Fact Table** | `mart.fact_sales` | Kolom `quantity` yang diagregasi per produk per tanggal (`date_id`). |
| **DAX Measure** | `[3M MA Demand]` | Fungsi `AVERAGEX` pada 3 bulan ke belakang untuk mencari tren rata-rata penjualan tanpa dipengaruhi *spike* sesaat. |
| **Visualization** | Line vs Column Chart | Grafik tren prediksi (garis) bersinggungan dengan penjualan asli (batang). |
| **Business Insight** | Prediksi Akurat | Daripada menebak kebutuhan belanja bulan depan, manajer melihat prediksi kebutuhan yang logis dan objektif sebesar 3.500 unit. |
| **Decision** | Data-Driven PO | Menggunakan angka prediksi tersebut sebagai *input* utama untuk membuat PO bulan depan (Reorder Point & EOQ) demi mencegah overstock dan stockout terulang. |

---

## 4. Traceability: Reorder Action (Decision Dashboard)

| Tahapan | Bukti (Trace) | Deskripsi Teknis / Konteks Bisnis |
| :--- | :--- | :--- |
| **ERP Transaction** | *Kombinasi* | Data dari Sales, Purchase, dan Stock digabungkan (Cross-Module). |
| **Fact Table** | *Star Schema Relations* | Relasi melalui tabel `dim_product`. |
| **DAX Measure** | `[Action Status]` | Logika kondisional berlapis (IF) yang membandingkan `[Inventory Qty]` saat ini terhadap `[ROP]`. |
| **Visualization** | Conditional Format Table | Warna sel (Merah/Kuning/Hijau) pada daftar produk di halaman Decision. |
| **Business Insight** | Operational Urgency | Mengetahui secara presisi dan seketika (Real-time) produk mana saja yang telah mencapai ambang batas kritis (Safety Stock). |
| **Decision** | Eksekusi Pengadaan | Staf *Purchasing* tidak perlu lagi menyusun Excel secara manual setiap sore. Mereka cukup memfilter status "🟡 Reorder Needed", melihat vendor terbaik dari *Supplier Score*, dan menekan tombol *Create PO* di Odoo. |
