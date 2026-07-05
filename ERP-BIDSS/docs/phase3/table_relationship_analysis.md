# Table Relationship Analysis

## Core Relationships (Odoo 18)

### Sales Flow
```
res_partner (Customer) ←── sale_order.partner_id
sale_order ──→ sale_order_line (1:N via order_id)
sale_order_line ──→ product_product (N:1 via product_id)
product_product ──→ product_template (N:1 via product_tmpl_id)
product_template ──→ product_category (N:1 via categ_id)
```

### Purchase Flow
```
res_partner (Vendor) ←── purchase_order.partner_id
purchase_order ──→ purchase_order_line (1:N via order_id)
purchase_order_line ──→ product_product (N:1 via product_id)
```

### Inventory Flow
```
stock_picking ──→ stock_move (1:N via picking_id)
stock_move ──→ product_product (N:1 via product_id)
stock_quant ──→ product_product (N:1 via product_id)
stock_warehouse ──→ res_company (N:1 via company_id)
```

### Accounting Flow
```
account_move ──→ account_move_line (1:N via move_id)
account_move ──→ res_partner (N:1 via partner_id)
```

### Cross-Module
```
sale_order ──→ stock_picking (via procurement)
purchase_order ──→ stock_picking (via procurement)
sale_order ──→ account_move (via invoice)
purchase_order ──→ account_move (via vendor bill)
```
