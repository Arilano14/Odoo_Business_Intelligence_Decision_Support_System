domain = [("company_id", "=", 2), ("state", "=", "sale"), ("date_order", ">=", "2026-01-01"), ("date_order", "<", "2027-01-01")]
total_untaxed = sum(env['sale.order'].search(domain).mapped('amount_untaxed'))
print(f"Total Confirmed Sales Value (Untaxed) for Company 2 in 2026 from sale.order: {total_untaxed}")

domain2 = [("company_id", "=", 2), ("state", "=", "sale")]
total_untaxed2 = sum(env['sale.order'].search(domain2).mapped('amount_untaxed'))
print(f"Total Confirmed Sales Value (Untaxed) for Company 2 ALL TIME from sale.order: {total_untaxed2}")

total_usd = sum(env['sale.order'].search([("company_id", "=", 2), ("currency_id.name", "=", "USD")]).mapped('amount_untaxed'))
total_idr = sum(env['sale.order'].search([("company_id", "=", 2), ("currency_id.name", "=", "IDR")]).mapped('amount_untaxed'))
print(f"Total USD: {total_usd}")
print(f"Total IDR: {total_idr}")
