# Deliverable 4: Traceability Report (Alur Validitas Data)

Salah satu nilai jual terkuat dari *Product 2* ini di mata akademik (Dosen Penguji) adalah kemampuannya menelusuri akar sebuah keputusan bisnis (*Traceability*). Tabel ini membuktikan bahwa Dashboard yang dibuat bukanlah sekadar gambar grafik acak, melainkan artefak yang saling mengunci dari hulu (Odoo) ke hilir (Rekomendasi).

## Matriks Penelusuran (Traceability Matrix)

| Business Story (Skenario) | Sumber Dataset (Odoo) | Indikator Utama (KPI) | Lokasi Visualisasi (Dashboard) | Luaran Keputusan (DSS) |
| :--- | :--- | :--- | :--- | :--- |
| **Supplier Delay** (Maret) | `purchase_order`, `stock_picking` | Avg Lead Time Days | **Purchase Dashboard** (Scatter Plot) | **Supplier Evaluation** (Bisa diputus kontrak jika melanggar SLA terus-menerus). |
| **Panic Buying** (April) | `purchase_order_line` | Total Purchase Qty & Value | **Executive Dashboard** (Line Chart lonjakan merah) | **Warning System** (Peringatan bahwa kas perusahaan tersedot). |
| **Overstock** (Juni - Des) | `stock_move`, `stock_quant` | ITR, DIO (Days Inventory Out) | **Inventory Dashboard** (Matrix biru menyala > 90 hari) | **Hold Order** (Sistem melarang pembelian barang yang DIO-nya tinggi). |
| **Pemulihan & Stabilitas** | `sale_order_line` | 3M MA Demand, ROP | **Forecast Dashboard** & **Decision Dashboard** | **Reorder Needed / Optimal** (Sistem memandu otomatis kapan waktu yang tepat untuk beli). |

---
**Kesimpulan Penelusuran:**
Dengan adanya matriks ini, Bab IV di laporan magang akan sangat kokoh. Mahasiswa bisa menjelaskan: *"Ketika kita melihat status **Overstock** pada layar Decision Dashboard, kita bisa menelusuri balik bahwa itu disebabkan oleh **DIO yang tinggi** di Inventory Dashboard, yang mana hal tersebut merupakan imbas dari tingginya angka **Purchase Qty** di Executive Dashboard bulan April, yang awalnya dipicu oleh masalah **Lead Time** di Purchase Dashboard bulan Maret."* 

Semua tabel saling berbicara satu sama lain membentuk satu cerita investigasi *Supply Chain* yang sempurna.
