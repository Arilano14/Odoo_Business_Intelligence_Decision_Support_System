-- unlock_portfolio_4.sql
-- Delete synthetic account moves
DELETE FROM account_move_line WHERE (date::text LIKE '2024%' OR date::text LIKE '2026%');
DELETE FROM account_move WHERE (date::text LIKE '2024%' OR date::text LIKE '2026%');
