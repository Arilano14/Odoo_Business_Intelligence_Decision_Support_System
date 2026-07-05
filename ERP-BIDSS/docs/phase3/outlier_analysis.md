# Outlier Analysis

## Analisis Outlier pada Data Simulasi

| Field | Table | Temuan | Validitas |
| :--- | :--- | :--- | :--- |
| product_uom_qty (Sales) | sale_order_line | Qty > 50 unit/order pada produk excavator | Valid (B2B bulk order alat berat) |
| price_unit (Sales) | sale_order_line | Harga > Rp 500 juta per unit | Valid (alat berat memiliki harga tinggi) |
| product_uom_qty (Inventory) | stock_move | Qty > 100 pada sparepart | Valid (sparepart memiliki volume tinggi) |
| amount_total (Purchase) | purchase_order | PO > Rp 2 miliar | Valid (pembelian batch excavator) |

## Kesimpulan
Seluruh outlier yang ditemukan merupakan karakteristik natural dari industri distribusi alat berat, bukan data error. Outlier dipertahankan karena merepresentasikan transaksi B2B yang sah.
