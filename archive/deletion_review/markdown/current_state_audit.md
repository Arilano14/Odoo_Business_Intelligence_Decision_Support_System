# Phase 8.0 — Current State Audit

## 1. Object Counts

| Objek | Jumlah sebelum | Masalah | Tindakan |
|---|---|---|---|
| Company | 2 | Terdapat perusahaan selain PT Prima Alat Nusantara | Hapus perusahaan ekstra, pertahankan 1 |
| Warehouse | 7 | Terdapat banyak warehouse yang tidak relevan | Hapus warehouse ekstra, pertahankan 1 main warehouse |
| Customer | 286 | Terlalu banyak (target 48) dan banyak demo/generic name | Hapus customer lama, buat ulang 48 customer relevan |
| Supplier | 286 | Terlalu banyak (target 24) dan banyak demo/generic name | Hapus supplier lama, buat ulang 24 supplier relevan |
| Product | 604 | Terdapat produk jasa, consumable non-relevan (target 240) | Hapus/arsip produk non-relevan, buat 240 SKU valid |
| Sale Order | 936 | Transaksi dummy dari 2024 & 2026 yang tipis | Hapus seluruh SO melalui ORM |
| Purchase Order | 1036 | Transaksi dummy dari 2024 & 2026 yang tipis | Hapus seluruh PO melalui ORM |
| Stock Picking | 1684 | Dokumen inventory usang dari transaksi 2024/2026 | Dihapus otomatis saat SO/PO dihapus via ORM (atau secara eksplisit) |
| Invoice/Bill | 1673 | Tagihan usang dari transaksi 2024/2026 | Dihapus melalui pembatalan invoice via ORM |
| Dashboard | 4 | Terdapat error RPC_ERROR id 11 dan referensi rusak | Periksa referensi ir.ui.menu/ir.actions.act_window dan hapus |

## 2. Codebase Audit
- Hardcoded Year: Ditemukan di ackend/scripts/dataset_generator.py (YEAR = 2024)
- Generator 2026: Ditemukan di ackend/generate_extra_transactions_v2.py (menambah data tipis di 2026)
- Dashboard Fix: Ditemukan ackend/fix_dashboard.py (mungkin terkait RPC_ERROR 11)
- Broken Reference: sale.order(19) tidak ada, ir_model_data spreadsheet.dashboard(11) tidak ada tapi mungkin ada di client action/menu.

Status Backup: DONE (Business_Intelegent_Project_v2_phase8_pre.dump)
Status Branch: DONE (phase8-master-data-realignment)
