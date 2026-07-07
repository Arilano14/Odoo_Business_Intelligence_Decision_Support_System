# Dataset Canon (v1.0)

Dokumen ini adalah **spesifikasi resmi tunggal** untuk dataset simulasi yang digunakan dalam proyek ini. Setelah divalidasi, dataset ini dikunci (*Frozen*) dan menjadi satu-satunya sumber data untuk Phase 7 (Power BI), repositori GitHub, serta penyusunan Bab IV Laporan Magang.

## 1. Identitas Dataset
- **Version:** v1.0 (Frozen)
- **Scenario:** PT Prima Alat Nusantara (Distribusi Alat Berat)
- **Period:** 1 Januari 2024 – 31 Desember 2024 (12 Bulan)
- **Generator Version:** `generate_mock_data.py` (v2.0 - Scenario Driven)

## 2. Business Timeline Canon (Target)
| Bulan | Business Event | Dampak Target Data |
| :--- | :--- | :--- |
| **Januari** | Go Live ERP | Baseline Normal |
| **Februari** | Permintaan stabil, sedikit naik | Sales naik ~8% |
| **Maret** | Supplier Terlambat | Lead Time naik menjadi ~10 hari (Target normal 5 hari) |
| **April** | Emergency Procurement (Panic Buying) | Purchase Quantity melonjak tajam (+40%) |
| **Mei** | Overstock (Imbas pembelian April) | Inventory level sangat tinggi |
| **Juni** | Warehouse Full | Holding cost membengkak |
| **Juli** | Slow Moving | Sales melambat |
| **Agustus** | Promosi & Obral | Sales mulai terdorong naik |
| **September** | Recovery | Stock kembali stabil |
| **Oktober** | Operasional Stabil | - |
| **November** | Peak Mining Project | Sales & Purchase mencapai puncak |
| **Desember** | Year End Closing | Volume transaksi dijaga tinggi |

## 3. Data Volume Target (Estimasi)
- **Products:** 500
- **Vendors:** 300
- **Customers:** 300
- **Sales Orders:** ~400
- **Purchase Orders:** ~400
- **Stock Moves:** ~7.000+
- **Accounting Journal Items:** ~10.000+

## 4. Status Kunci (Lock Status)
```json
{
  "scenario_locked": true,
  "data_generation_validated": false,
  "ready_for_power_bi": false
}
```
*(Status `data_generation_validated` dan `ready_for_power_bi` akan diubah menjadi `true` setelah eksekusi reset dan validasi tuntas).*
