# 06. Dashboard Storytelling

Dokumen ini berisi narasi skenario bisnis (*Business Story*) selama 12 bulan yang harus tergambar jelas di dalam Power BI, mengubah data mentah menjadi *Actionable Insights*. Format bercerita menggunakan kerangka **Situation → Evidence → Analysis → Recommendation**.

## Q1: Januari - Februari (The Baseline)
- **Situation**: Operasional bisnis berjalan normal dan stabil pasca implementasi ERP.
- **Evidence**: 
  - *Sales Dashboard*: Revenue tumbuh moderat (8% di bulan Februari). 
  - *Purchase Dashboard*: Lead Time pengiriman dari vendor berada di angka standar (5 hari).
- **Analysis**: Permintaan pasar sesuai dengan proyeksi awal tahun. Tidak ada *bottleneck* pada sisi pasokan.
- **Recommendation**: Pertahankan level pemesanan standar (EOQ) dan fokus pada retensi *Top Customers*.

## Q2: Maret - April (The Supply Shock)
- **Situation**: Terjadi guncangan pasokan (Supply Shock) yang berujung pada kekosongan stok.
- **Evidence**: 
  - *Purchase Dashboard*: Avg Lead Time melonjak menjadi 10+ hari di bulan Maret.
  - *Inventory Dashboard*: Current Inventory Qty jatuh tajam mendekati 0.
  - *Sales Dashboard*: Revenue di bulan Maret drop drastis (hanya tercapai ~78% dari target).
- **Analysis**: Keterlambatan pengiriman dari vendor internasional di bulan Maret menyebabkan perusahaan kehabisan stok (*Stockout*). Akibatnya, pesanan pelanggan di akhir Maret hingga awal April tidak dapat dipenuhi (Lost Sales), yang secara langsung memukul *Revenue* dan *Margin*.
- **Recommendation**: Aktifkan protokol *Emergency Procurement* segera. Manajemen harus mengevaluasi *Supplier Reliability Score* dan mempertimbangkan vendor alternatif (sekalipun lebih mahal) demi menyelamatkan *Service Level*.

## Q2-Q3: Mei - Juli (The Whiplash Effect)
- **Situation**: Reaksi berlebihan dari tim *Purchasing* (Panic Buying) menyebabkan penumpukan barang (Overstock).
- **Evidence**:
  - *Purchase Dashboard*: Total Purchase Qty melonjak hampir 200% di bulan April/Mei.
  - *Inventory Dashboard*: ITR (Inventory Turnover) anjlok ke angka < 2.0, dan DIO (Days Inventory Outstanding) melonjak melebihi 90 hari pada bulan Juni-Juli.
- **Analysis**: Merespons krisis di bulan April, perusahaan melakukan pembelian gila-gilaan (Whiplash Effect). Masalahnya, permintaan (Demand) di bulan Mei-Juli sebenarnya sedang melambat secara alamiah (slow season). Hasilnya: barang menumpuk di gudang, modal kerja (*working capital*) terperangkap dalam bentuk inventaris, dan biaya penyimpanan (*holding cost*) meningkat tajam.
- **Recommendation**: Hentikan sementara (Hold) semua pengadaan baru (status "🔵 Overstock"). Luncurkan kampanye promosi atau diskon (Marketing push) untuk cuci gudang (*clearance*) produk-produk yang teridentifikasi sebagai *Slow Moving* di matriks Inventory Dashboard.

## Q3-Q4: Agustus - Oktober (The Stabilization)
- **Situation**: Upaya penyeimbangan stok (Rebalancing) mulai menunjukkan hasil.
- **Evidence**:
  - *Sales Dashboard*: Revenue melonjak naik (Peak Promotion) di bulan Agustus.
  - *Inventory Dashboard*: Tren DIO mulai menurun perlahan mendekati target 30-45 hari.
- **Analysis**: Diskon besar-besaran berhasil mencairkan produk *Slow Moving*, mengubah inventaris mati menjadi kas (*Cash Flow* recovery). Operasional gudang mulai bernapas lega.
- **Recommendation**: Lakukan transisi kebijakan *Purchasing* dari intuisi manual menuju *Data-Driven Procurement* (memanfaatkan formula ROP dan Safety Stock).

## Q4: November - Desember (The Data-Driven Future)
- **Situation**: Musim puncak tambang (*Peak Mining Project*) di akhir tahun dapat dikelola tanpa insiden *stockout* atau *overstock*.
- **Evidence**:
  - *Forecast Dashboard*: Garis Aktual (Sales) berjalan selaras (Variance kecil) dengan garis *3M MA Demand*.
  - *Decision Dashboard*: Status pemesanan didominasi oleh "🟢 Optimal" dan "🟡 Reorder Needed" secara berkala, tanpa ada "🔴 Stockout" dadakan.
- **Analysis**: Dengan mengikuti angka rekomendasi pada *Decision Dashboard* (Forecast Purchase Qty, EOQ, dan ROP), perusahaan berhasil menghadapi lonjakan *demand* akhir tahun secara proporsional.
- **Recommendation**: Jadikan *Decision Dashboard* sebagai SOP resmi harian bagi divisi *Procurement* mulai tahun depan.
