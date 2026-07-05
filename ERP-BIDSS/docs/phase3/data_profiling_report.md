# Data Profiling Report

## Dataset Simulasi — PT Prima Alat Nusantara

| Dataset | Target Rows | Source Table (Odoo 18) |
| :--- | :--- | :--- |
| Product (Master) | 500 | product_product + product_template |
| Customer (Master) | 300 | res_partner (customer_rank > 0) |
| Vendor (Master) | 300 | res_partner (supplier_rank > 0) |
| Warehouse (Master) | 5 | stock_warehouse |
| Company (Master) | 1 | res_company |
| Sales Order | 2.000 | sale_order |
| Sales Order Line | ~8.000 | sale_order_line |
| Purchase Order | 2.000 | purchase_order |
| Purchase Order Line | ~8.000 | purchase_order_line |
| Stock Movement | 10.000 | stock_move |
| Journal Entry | 15.000 | account_move + account_move_line |

**Total Volume:** ≈ 30.000 records

**Catatan:** Seluruh data merupakan dataset simulasi berbasis skenario bisnis selama 12 bulan operasional (Januari–Desember). Distribusi transaksi mengikuti pola scenario-driven, bukan random.
