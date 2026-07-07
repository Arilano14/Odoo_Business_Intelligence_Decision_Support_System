# Deliverable 3: Dashboard Interpretation Report

Dokumen ini berisi hasil interpretasi layar (*insight*) dari setiap halaman Power BI Dashboard yang akan dimasukkan ke dalam Bab IV laporan tugas akhir/magang.

## 1. Executive Dashboard
**Insight Utama:** 
Dashboard secara jelas menangkap lonjakan pengeluaran (garis merah / *Purchase Value*) secara ekstrem di bulan April yang hampir menyentuh angka Rp 31 Miliar, berbanding terbalik dengan bulan-bulan biasa yang hanya berkisar di Rp 10-15 Miliar. Lonjakan anomali ini menyedot *cash flow* perusahaan secara masif dan mempersempit Margin kotor perusahaan pada bulan tersebut.

## 2. Sales Dashboard
**Insight Utama:** 
Pendapatan perusahaan sangat ditopang oleh Top 5 Pelanggan dari sektor perusahaan konstruksi berskala besar. Meski sempat terjadi penundaan penjualan di bulan Maret karena tidak ada barang (Stockout), perusahaan konstruksi tersebut kembali menyerap alat berat begitu *supply* kembali normal di kuartal berikutnya. 

## 3. Purchase Dashboard (Vendor Reliability)
**Insight Utama:** 
Melalui visualisasi *Scatter Plot*, terlihat adanya anomali pada salah satu/beberapa vendor internasional yang titiknya berada sangat tinggi di sumbu *Lead Time* (mencapai rata-rata di atas 10 hari pada bulan Maret). Vendor inilah yang menjadi pemicu efek domino dari krisis rantai pasok. Evaluasi kinerja vendor ini wajib dilakukan oleh departemen *Procurement*.

## 4. Inventory Dashboard
**Insight Utama:** 
Tabel *Days Inventory Outstanding (DIO)* menunjukkan banyak alat berat dan *spare part* (suku cadang) yang mengendap lebih dari 90 hari (Ditandai dengan indikator warna biru terang). Ini merupakan konfirmasi visual bahwa perusahaan mengalami *Overstock* parah akibat *Panic Buying* bulan April yang belum terserap habis oleh *market*.

## 5. Forecast Dashboard
**Insight Utama:** 
Garis biru (*3M MA Demand*) berjalan jauh lebih mulus dibandingkan garis batang historis penjualan. Hal ini membuktikan keampuhan metode *Moving Average*. Garis prediksi ini secara visual "menolak" untuk ikut panik saat terjadi lonjakan mendadak, memberikan gambaran *baseline demand* yang lebih rasional bagi manajemen untuk merencanakan belanja bulan depan.

## 6. Decision Dashboard
**Insight Utama:** 
Dashboard ini berhasil mengubah data reaktif menjadi tindakan preskriptif. Sistem tidak lagi hanya menampilkan grafik, tetapi secara harfiah mengeluarkan perintah *"Hold Order"*, *"Urgent Order"*, atau *"Reorder Needed"* untuk setiap baris produk (SKU). Fitur ini menjawab tuntutan kebutuhan *Decision Support System (DSS)* yang otomatis dan terkomputerisasi.
