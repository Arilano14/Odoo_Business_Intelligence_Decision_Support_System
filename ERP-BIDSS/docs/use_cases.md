# Use Cases

## Konteks
Use case berikut muncul dari kebutuhan manajemen PT Prima Alat Nusantara setelah implementasi ERP Odoo berjalan dan data transaksi operasional telah tersedia.

### UC1: Executive Performance Monitoring
**Aktor:** CEO / Executive Manager
**Kebutuhan:** Melihat performa perusahaan secara menyeluruh (Revenue, Purchase Value, Inventory Value, Growth).
**Kondisi Sebelumnya:** Data harus diekspor dari beberapa modul Odoo dan diolah manual di Excel.
**Solusi:** Executive Dashboard menampilkan seluruh KPI dalam satu tampilan.

### UC2: Inventory Optimization
**Aktor:** Inventory Manager
**Kebutuhan:** Mengetahui produk mana yang slow moving, fast moving, dan kapan harus melakukan reorder.
**Kondisi Sebelumnya:** Inventory manager harus membuka menu Stock Move di Odoo dan menghitung manual.
**Solusi:** Inventory Dashboard dengan kalkulasi otomatis Inventory Turnover, DIO, ROP, dan EOQ.

### UC3: Demand Forecasting
**Aktor:** Sales Manager / Procurement Manager
**Kebutuhan:** Memperkirakan demand bulan depan untuk menyusun rencana pembelian.
**Kondisi Sebelumnya:** Estimasi berdasarkan pengalaman, bukan data historis.
**Solusi:** Forecast Dashboard menggunakan Moving Average 3 Periode.

### UC4: Supplier Evaluation
**Aktor:** Procurement Manager
**Kebutuhan:** Mengevaluasi kinerja supplier secara objektif berdasarkan ketepatan waktu, fulfillment rate, dan kualitas.
**Kondisi Sebelumnya:** Tidak ada sistem evaluasi terstruktur.
**Solusi:** Purchase Dashboard dengan Supplier Performance Score (Weighted Scoring).

### UC5: Purchase Decision Support
**Aktor:** Procurement Manager
**Kebutuhan:** Menentukan jumlah pembelian ekonomis (EOQ) dan waktu reorder (ROP).
**Kondisi Sebelumnya:** Pembelian dilakukan berdasarkan perkiraan.
**Solusi:** Decision Dashboard dengan kalkulasi EOQ dan ROP otomatis.
