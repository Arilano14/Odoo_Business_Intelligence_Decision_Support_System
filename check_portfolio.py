import sys
env = env
active_variants = env['product.product'].search([('active', '=', True)])
print('Active Variants:', len(active_variants))
portfolio_tags = env['product.tag'].search([])
print('Tags:', portfolio_tags.mapped('name'))
categories = env['product.category'].search([])
print('Categories:', categories.mapped('name'))
