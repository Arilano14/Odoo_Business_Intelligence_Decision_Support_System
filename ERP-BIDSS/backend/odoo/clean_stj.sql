-- Delete leftover stock journal entries from legacy cleanup
DELETE FROM account_move_line WHERE move_id IN (SELECT id FROM account_move WHERE ref LIKE 'Product Quantity Updated%');
DELETE FROM account_move WHERE ref LIKE 'Product Quantity Updated%';
