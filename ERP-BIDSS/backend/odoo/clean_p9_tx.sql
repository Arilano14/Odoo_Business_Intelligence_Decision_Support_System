-- Delete ALL transactional records to restore 100% clean Phase 8 baseline
DELETE FROM sale_order_line;
DELETE FROM sale_order;

DELETE FROM purchase_order_line;
DELETE FROM purchase_order;

DELETE FROM stock_move_line;
DELETE FROM stock_move;
DELETE FROM stock_picking;

DELETE FROM stock_scrap;

DELETE FROM account_move_line WHERE move_id IN (SELECT id FROM account_move WHERE move_type != 'entry');
DELETE FROM account_move WHERE move_type != 'entry';
