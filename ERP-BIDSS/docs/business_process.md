# Business Process

## Alur Proses Bisnis PT Prima Alat Nusantara (Simulasi)

### Sales Process
1. Customer mengirimkan permintaan penawaran.
2. Sales membuat Quotation di Odoo (sale.order, state='draft').
3. Quotation dikonfirmasi menjadi Sales Order (state='sale').
4. Barang dikirim dari gudang (stock.picking, stock.move).
5. Invoice dibuat (account.move, move_type='out_invoice').
6. Pembayaran diterima.

### Purchase Process
1. Inventory Manager mengidentifikasi kebutuhan reorder.
2. Procurement membuat Request for Quotation (purchase.order, state='draft').
3. RFQ dikonfirmasi menjadi Purchase Order (state='purchase').
4. Barang diterima di gudang (stock.picking, stock.move).
5. Vendor Bill dibuat (account.move, move_type='in_invoice').
6. Pembayaran dilakukan.

### Inventory Process
1. Barang masuk dicatat sebagai stock.move (incoming).
2. Barang keluar dicatat sebagai stock.move (outgoing).
3. Stok aktual tercatat di stock.quant.
4. Valuasi persediaan dihitung berdasarkan standard_price × quantity.

### Accounting Process
1. Setiap transaksi sales/purchase menghasilkan journal entry (account.move).
2. Debit dan credit dicatat di account.move.line.
3. Laporan keuangan dihasilkan dari aggregasi journal entries.
