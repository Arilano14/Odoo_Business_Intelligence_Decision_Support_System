# Grain Definition

## Definisi Grain per Fact Table

Setiap fact table memiliki grain (level of detail) yang jelas dan konsisten dengan transaksi Odoo 18.

### fact_sales
- **Grain:** 1 row = 1 sale_order_line (confirmed)
- **Filter Odoo:** `sale_order.state = 'sale'`
- **Makna Bisnis:** Setiap baris merepresentasikan satu item produk dalam satu Sales Order yang sudah dikonfirmasi pelanggan.
- **Contoh:** SO001 berisi 3 produk → 3 rows di fact_sales.

### fact_purchase
- **Grain:** 1 row = 1 purchase_order_line (confirmed)
- **Filter Odoo:** `purchase_order.state = 'purchase'`
- **Makna Bisnis:** Setiap baris merepresentasikan satu item produk dalam satu Purchase Order yang sudah dikonfirmasi ke vendor.
- **Contoh:** PO001 berisi 2 produk → 2 rows di fact_purchase.

### fact_inventory
- **Grain:** 1 row = 1 stock_move (done)
- **Filter Odoo:** `stock_move.state = 'done'`
- **Makna Bisnis:** Setiap baris merepresentasikan satu perpindahan stok yang sudah selesai (incoming atau outgoing).
- **Contoh:** Penerimaan barang dari PO001 → 1 row incoming. Pengiriman ke pelanggan → 1 row outgoing.

### fact_accounting
- **Grain:** 1 row = 1 account_move_line (posted)
- **Filter Odoo:** `account_move.state = 'posted'`
- **Makna Bisnis:** Setiap baris merepresentasikan satu journal entry line yang sudah diposting ke buku besar.
- **Contoh:** Invoice untuk SO001 → minimal 2 rows (debit piutang, credit pendapatan).
