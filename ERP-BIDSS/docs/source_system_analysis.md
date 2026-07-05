# Source System Analysis

## Source System
- **ERP:** Odoo 18 Community Edition
- **Database Engine:** PostgreSQL
- **Data Owner:** ERP Administrator
- **Update Frequency:** Real-time (setiap transaksi dicatat oleh Odoo)
- **Extraction Method:** Python ETL Pipeline (batch, scheduled)

## Odoo 18 Core Tables

### Sales Module
- sale_order
- sale_order_line

### Purchase Module
- purchase_order
- purchase_order_line

### Inventory Module
- stock_move
- stock_quant
- stock_picking
- stock_warehouse

### Accounting Module
- account_move
- account_move_line

### Master Data
- product_product
- product_template
- product_category
- res_partner
- res_company

## Dataset Simulasi
Seluruh data merupakan dataset simulasi berbasis skenario bisnis perusahaan distributor alat berat. Data di-generate menggunakan Python (Faker + custom logic) dan dimasukkan ke PostgreSQL mengikuti struktur tabel Odoo 18.
