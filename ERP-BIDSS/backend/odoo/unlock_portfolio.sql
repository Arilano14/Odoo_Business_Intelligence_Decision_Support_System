-- unlock_portfolio.sql
-- Reset states to allow ORM deletion
UPDATE stock_picking SET state = 'cancel' WHERE state = 'done' AND (date::text LIKE '2024%' OR date::text LIKE '2026%');
UPDATE stock_move SET state = 'cancel' WHERE state = 'done' AND (date::text LIKE '2024%' OR date::text LIKE '2026%');
UPDATE stock_move_line SET state = 'cancel' WHERE state = 'done' AND (date::text LIKE '2024%' OR date::text LIKE '2026%');

UPDATE sale_order SET state = 'cancel' WHERE (date_order::text LIKE '2024%' OR date_order::text LIKE '2026%');
UPDATE purchase_order SET state = 'cancel' WHERE (date_order::text LIKE '2024%' OR date_order::text LIKE '2026%');
UPDATE account_move SET state = 'draft' WHERE state = 'posted' AND (date::text LIKE '2024%' OR date::text LIKE '2026%');
