import sys
env = env
portfolio_categ = env['product.category'].search([('name', '=', 'Portfolio 2026')])
if portfolio_categ:
    # also get children
    categ_ids = env['product.category'].search([('id', 'child_of', portfolio_categ.id)]).ids
    portfolio_variants = env['product.product'].search([('categ_id', 'in', categ_ids), ('active', '=', True)])
    print('Portfolio 2026 Variants:', len(portfolio_variants))
    transacted = env['sale.report'].search([('company_id', '=', 2), ('state', 'in', ['sale', 'done']), ('date', '>=', '2026-01-01'), ('date', '<', '2027-01-01')]).mapped('product_id')
    transacted_portfolio = [p for p in transacted if p.id in portfolio_variants.ids]
    print('Transacted Portfolio Variants:', len(transacted_portfolio))
    non_transacted_portfolio = [p for p in portfolio_variants if p.id not in transacted.ids]
    print('Non-Transacted Portfolio Variants:', len(non_transacted_portfolio))
