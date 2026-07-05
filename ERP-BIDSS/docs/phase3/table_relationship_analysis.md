# Table Relationship Analysis

## Core Relationships
- `sale_order` 1:N `sale_order_line`
- `sale_order_line` N:1 `product_product`
- `sale_order` N:1 `res_partner`
- `purchase_order` 1:N `purchase_order_line`
- `stock_picking` 1:N `stock_move`
