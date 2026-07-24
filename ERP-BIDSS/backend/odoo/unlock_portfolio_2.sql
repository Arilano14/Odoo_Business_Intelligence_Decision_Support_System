-- unlock_portfolio_2.sql
DELETE FROM account_partial_reconcile;
UPDATE account_move_line SET reconciled = False, matching_number = NULL;
UPDATE account_move SET payment_state = 'not_paid' WHERE (date::text LIKE '2024%' OR date::text LIKE '2026%');
