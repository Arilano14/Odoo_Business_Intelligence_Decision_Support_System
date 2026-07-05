# Business Rules

## Data Filtering Rules (Odoo 18)
Berikut aturan bisnis yang diterapkan pada proses ETL untuk memastikan hanya data valid yang diproses.

| Rule | Table (Odoo) | Condition | Keterangan |
| :--- | :--- | :--- | :--- |
| BR-01 | sale_order | state = 'sale' | Hanya Sales Order yang sudah dikonfirmasi |
| BR-02 | purchase_order | state = 'purchase' | Hanya Purchase Order yang sudah dikonfirmasi |
| BR-03 | stock_move | state = 'done' | Hanya pergerakan stok yang sudah selesai |
| BR-04 | account_move | state = 'posted' | Hanya journal entry yang sudah diposting |
| BR-05 | product_product | active = True | Hanya produk aktif |
| BR-06 | res_partner | active = True | Hanya partner aktif |

## Calculation Rules

| Rule | Formula | Keterangan |
| :--- | :--- | :--- |
| CR-01 | Revenue = SUM(price_subtotal) | Dari sale_order_line |
| CR-02 | COGS = SUM(standard_price × qty) | Dari stock_move outgoing |
| CR-03 | Inventory Value = SUM(standard_price × quantity) | Dari stock_quant |
| CR-04 | Supplier Score = 0.40×Delivery + 0.35×Fulfillment + 0.25×Quality | Weighted Scoring |
