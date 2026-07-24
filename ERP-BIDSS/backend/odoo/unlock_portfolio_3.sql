-- unlock_portfolio_3.sql
-- Force delete stock pickings, moves, and valuation layers for 2024/2026 synthetic data
DELETE FROM stock_valuation_layer WHERE (create_date::text LIKE '2024%' OR create_date::text LIKE '2026%');
DELETE FROM stock_move_line WHERE (date::text LIKE '2024%' OR date::text LIKE '2026%');
DELETE FROM stock_move WHERE (date::text LIKE '2024%' OR date::text LIKE '2026%');
DELETE FROM stock_picking WHERE (date::text LIKE '2024%' OR date::text LIKE '2026%');

-- Delete old portfolio partners and products
DELETE FROM res_partner WHERE ref LIKE 'BIDSS-CUST-%' OR ref LIKE 'BIDSS-VEND-%';
-- Product deletion is tricky due to product_product and product_template, but we can try
DELETE FROM product_product WHERE default_code LIKE 'BIDSS-HE-%';
DELETE FROM product_template WHERE default_code LIKE 'BIDSS-HE-%';
