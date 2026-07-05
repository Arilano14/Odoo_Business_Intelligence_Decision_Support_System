# KPI Definition

## Konteks
Seluruh KPI berikut dirancang untuk menjawab permasalahan bisnis PT Prima Alat Nusantara yang teridentifikasi setelah implementasi ERP. Setiap KPI memiliki rumus, threshold, interpretasi, dan rekomendasi aksi.

---

### KPI 1: Revenue
- **Formula:** SUM(sale_order_line.price_subtotal) WHERE sale_order.state = 'sale'
- **Threshold:** Target ditentukan per periode oleh manajemen.
- **Interpretasi:** Total nilai penjualan bersih.
- **Rekomendasi:** Bandingkan dengan periode sebelumnya untuk mengukur pertumbuhan.

### KPI 2: Sales Growth
- **Formula:** (Revenue Bulan Ini - Revenue Bulan Lalu) / Revenue Bulan Lalu × 100%
- **Threshold:** > 0% (positif)
- **Interpretasi:** Persentase pertumbuhan penjualan.
- **Rekomendasi:** Jika negatif selama 2 bulan berturut-turut, evaluasi strategi penjualan.

### KPI 3: Inventory Turnover
- **Formula:** COGS / Average Inventory Value
- **Threshold:** Ideal ≥ 4 kali/tahun
- **Interpretasi:** Semakin tinggi semakin baik (persediaan berputar cepat).
- **Rekomendasi:** Jika < 2, kurangi pembelian dan lakukan promosi produk slow moving.

### KPI 4: Days Inventory Outstanding (DIO)
- **Formula:** (Average Inventory / COGS) × 365
- **Threshold:** Ideal ≤ 90 hari
- **Interpretasi:** Semakin kecil semakin baik (stok tidak terlalu lama di gudang).
- **Rekomendasi:** Jika > 120 hari, evaluasi kelayakan produk.

### KPI 5: Revenue Contribution
- **Formula:** Revenue Produk / Total Revenue × 100%
- **Threshold:** Produk dengan kontribusi < 5% dan DIO tinggi perlu dievaluasi.
- **Interpretasi:** Mengidentifikasi produk unggulan dan produk tidak produktif.

### KPI 6: Inventory Value
- **Formula:** SUM(product_template.standard_price × stock_quant.quantity)
- **Threshold:** Tidak boleh melebihi 40% dari total aset lancar (benchmark distribusi).
- **Interpretasi:** Nilai total persediaan yang tersimpan di gudang.

### KPI 7: Purchase Value
- **Formula:** SUM(purchase_order_line.price_subtotal) WHERE purchase_order.state = 'purchase'
- **Threshold:** Harus proporsional terhadap forecast demand.

### KPI 8: Purchase Growth
- **Formula:** (Purchase Bulan Ini - Purchase Bulan Lalu) / Purchase Bulan Lalu × 100%

### KPI 9: Reorder Point (ROP)
- **Formula:** Average Daily Demand × Lead Time (hari)
- **Threshold:** Jika stok aktual ≤ ROP, maka reorder harus dilakukan.
- **Rekomendasi:** Buat Purchase Order sesuai hasil EOQ.

### KPI 10: Economic Order Quantity (EOQ)
- **Formula:** √(2DS / H)
  - D = Annual Demand, S = Ordering Cost per order, H = Holding Cost per unit per year
- **Interpretasi:** Jumlah pembelian ekonomis yang meminimalkan total biaya.

### KPI 11: Supplier Performance Score
- **Metode:** Weighted Scoring
- **Formula:** (0.40 × Delivery Score) + (0.35 × Fulfillment Score) + (0.25 × Quality Score)
- **Kategori:**
  - ≥ 90: Sangat Baik
  - 80–89: Baik
  - 70–79: Perlu Evaluasi
  - < 70: Prioritas Perbaikan

### KPI 12: Demand Forecast
- **Metode:** Moving Average 3 Periode
- **Formula:** Forecast = (Bulan-1 + Bulan-2 + Bulan-3) / 3
- **Interpretasi:** Estimasi demand periode berikutnya berdasarkan data historis.
