# Surrogate Key Plan

- All dimension tables will use a `sk_<dimension>_id` (Integer, Auto-increment/Identity) as the Primary Key.
- Natural keys from Odoo (e.g., `odoo_product_id`, `odoo_partner_id`) will be retained for traceability and Type 1/Type 2 SCD updates.
