-- fix_duplicates.sql
DELETE FROM product_supplierinfo;
DELETE FROM product_product WHERE default_code LIKE 'PORTFOLIO_2026_V1-PROD-%';
DELETE FROM product_template WHERE default_code LIKE 'PORTFOLIO_2026_V1-PROD-%';
