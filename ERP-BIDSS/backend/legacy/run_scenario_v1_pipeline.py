"""
Phase 9 Main Orchestrator CLI.

Provides command line subcommands for Phase 9 execution gates:
- dry-run        : Runs Gate 9B full-year simulation without creating Odoo records
- january-pilot  : Runs Gate 9C (January pilot generation)
- scenario-pilot : Runs Gate 9D (Jan-May scenario generation)
- full-year      : Runs Gate 9E (Full-year Jan-Dec generation)
- validate       : Runs Gate 9F automated validation suite
- cleanup        : Safely reverses Phase 9 batch
"""

import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from odoo.connection import get_connection
from phase9.config import COMPANY_NAME, WAREHOUSE_CODE, TOTAL_SO_TARGET, TOTAL_PO_TARGET
from phase9.demand_planner import plan_product_demand
from phase9.customer_allocator import allocate_customers
from phase9.supplier_allocator import allocate_suppliers
from phase9.opening_inventory import generate_opening_inventory
from phase9.sales_generator import generate_sales_orders
from phase9.purchase_generator import generate_purchase_orders
from phase9.inventory_ops import generate_inventory_operations
from phase9.event_scheduler import schedule_events
from phase9.cleanup_phase9 import cleanup_phase9_batch

def load_master_data():
    uid, models, db, password = get_connection()

    # Load 48 customers
    custs = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
        [[('ref', '=like', 'PORTFOLIO_2026_V1-CUST-%'), ('active', '=', True)]],
        {'fields': ['id', 'name', 'ref']})

    # Load 24 suppliers
    supps = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
        [[('ref', '=like', 'PORTFOLIO_2026_V1-VEND-%'), ('active', '=', True)]],
        {'fields': ['id', 'name', 'ref']})

    # Load 240 product templates
    prods = models.execute_kw(db, uid, password, 'product.template', 'search_read',
        [[('default_code', '=like', 'PORTFOLIO_2026_V1-PROD-%'), ('active', '=', True)]],
        {'fields': ['id', 'name', 'default_code', 'categ_id', 'list_price', 'standard_price']})

    # Load categories
    cat_ids = list(set(p['categ_id'][0] for p in prods))
    cats = models.execute_kw(db, uid, password, 'product.category', 'search_read',
        [[('id', 'in', cat_ids)]], {'fields': ['id', 'name', 'complete_name']})
    cat_map = {}
    for c in cats:
        leaf_name = c['complete_name'].split(' / ')[-1] if ' / ' in c['complete_name'] else c['name']
        cat_map[c['id']] = leaf_name

    # Group products by category
    prods_by_cat = {}
    for p in prods:
        cat_name = cat_map.get(p['categ_id'][0], 'Consumables')
        if cat_name not in prods_by_cat:
            prods_by_cat[cat_name] = []
        prods_by_cat[cat_name].append(p)

    # Load supplierinfo mappings
    tmpl_ids = [p['id'] for p in prods]
    sinfos = models.execute_kw(db, uid, password, 'product.supplierinfo', 'search_read',
        [[('product_tmpl_id', 'in', tmpl_ids)]],
        {'fields': ['id', 'product_tmpl_id', 'partner_id', 'delay', 'price', 'sequence']})

    return {
        'uid': uid, 'models': models, 'db': db, 'password': password,
        'customers': custs,
        'suppliers': supps,
        'product_templates': prods,
        'categories': cat_map,
        'products_by_category': prods_by_cat,
        'supplierinfo': sinfos,
    }

def run_dry_run():
    print("=" * 70)
    print("PHASE 9 GATE 9B — FULL-YEAR DRY-RUN SIMULATION")
    print("=" * 70)

    data = load_master_data()
    print(f"Loaded Master Data Baseline:")
    print(f"  Customers: {len(data['customers'])}/48")
    print(f"  Suppliers: {len(data['suppliers'])}/24")
    print(f"  Product Templates: {len(data['product_templates'])}/240")
    print(f"  Supplier Mappings: {len(data['supplierinfo'])}/456")

    # 1. Demand Planning
    demand_plan = plan_product_demand(data['products_by_category'])
    print(f"\n[OK] Demand Plan created for {len(demand_plan)} products.")

    # 2. Customer Allocation
    cust_plan = allocate_customers(data['customers'])
    print(f"[OK] Customer Allocation plan created for 720 SOs across {len(cust_plan['annual_orders'])} customers.")

    # 3. Supplier Allocation
    supp_plan = allocate_suppliers(data['suppliers'], data['supplierinfo'])
    print(f"[OK] Supplier Allocation plan created for 240 POs across {len(supp_plan['annual_pos'])} suppliers.")

    # 4. Opening Inventory
    open_inv = generate_opening_inventory(data['models'], data['db'], data['uid'], data['password'], demand_plan, dry_run=True)

    # 5. Sales Orders
    so_summary = generate_sales_orders(data['models'], data['db'], data['uid'], data['password'],
        cust_plan['monthly_allocation'], data['customers'], data['product_templates'], data['categories'], dry_run=True)

    # 6. Purchase Orders
    po_summary = generate_purchase_orders(data['models'], data['db'], data['uid'], data['password'],
        supp_plan['monthly_allocation'], supp_plan['supplier_products'], data['product_templates'],
        data['categories'], data['supplierinfo'], dry_run=True)

    # 7. Inventory Ops
    ops_summary = generate_inventory_operations(data['models'], data['db'], data['uid'], data['password'],
        data['product_templates'], data['categories'], dry_run=True)

    # 8. Event Scheduler
    events, monthly_summary = schedule_events(so_summary, po_summary, ops_summary)

    print("\n--- Monthly Event Schedule Summary ---")
    print(f"{'Month':<8} | {'SO':<6} | {'PO':<6} | {'INT':<6} | {'SCRAP':<6} | {'TOTAL':<6}")
    print("-" * 50)
    for m in range(1, 13):
        row = monthly_summary[m]
        print(f"Month {m:<3} | {row['SO']:<6} | {row['PO']:<6} | {row['INT']:<6} | {row['SCRAP']:<6} | {row['TOTAL']:<6}")

    print("-" * 50)
    print(f"TOTAL    | {sum(r['SO'] for r in monthly_summary.values()):<6} | {sum(r['PO'] for r in monthly_summary.values()):<6} | {sum(r['INT'] for r in monthly_summary.values()):<6} | {sum(r['SCRAP'] for r in monthly_summary.values()):<6} | {sum(r['TOTAL'] for r in monthly_summary.values()):<6}")

    # Assert contract counts
    assert sum(r['SO'] for r in monthly_summary.values()) == TOTAL_SO_TARGET, f"SO total expected {TOTAL_SO_TARGET}"
    assert sum(r['PO'] for r in monthly_summary.values()) == TOTAL_PO_TARGET, f"PO total expected {TOTAL_PO_TARGET}"
    assert sum(r['INT'] for r in monthly_summary.values()) == 24, "INT total expected 24"
    assert sum(r['SCRAP'] for r in monthly_summary.values()) == 12, "SCRAP total expected 12"

    print("\n[GATE 9B DRY-RUN SUCCESS] All projected counts and contract constraints match 100%.")

def run_live_generation(months, gate_name):
    print("=" * 70)
    print(f"PHASE 9 {gate_name} — LIVE TRANSACTION GENERATION")
    print("=" * 70)

    data = load_master_data()
    demand_plan = plan_product_demand(data['products_by_category'])
    cust_plan = allocate_customers(data['customers'])
    supp_plan = allocate_suppliers(data['suppliers'], data['supplierinfo'])

    # 1. Opening inventory (always applies for 240 products on 2026-01-01)
    generate_opening_inventory(data['models'], data['db'], data['uid'], data['password'], demand_plan, dry_run=False)

    # 2. Sales Orders
    generate_sales_orders(data['models'], data['db'], data['uid'], data['password'],
        cust_plan['monthly_allocation'], data['customers'], data['product_templates'], data['categories'], dry_run=False, months=months)

    # 3. Purchase Orders
    generate_purchase_orders(data['models'], data['db'], data['uid'], data['password'],
        supp_plan['monthly_allocation'], supp_plan['supplier_products'], data['product_templates'],
        data['categories'], data['supplierinfo'], dry_run=False, months=months)

    # 4. Inventory Ops
    generate_inventory_operations(data['models'], data['db'], data['uid'], data['password'],
        data['product_templates'], data['categories'], dry_run=False, months=months)

    print(f"\n[{gate_name} SUCCESS] Live generation for months {months if months else '1-12'} completed.")

def run_validate():
    from validation.validate_phase9 import validate_phase9
    code = validate_phase9()
    if code != 0:
        sys.exit(code)

def main():
    parser = argparse.ArgumentParser(description="Phase 9 Orchestrator CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("dry-run", help="Run Gate 9B full-year simulation without modifying database")
    subparsers.add_parser("january-pilot", help="Run Gate 9C (January pilot live generation)")
    subparsers.add_parser("scenario-pilot", help="Run Gate 9D (Jan-May scenario live generation)")
    subparsers.add_parser("full-year", help="Run Gate 9E (Full-year live generation)")
    subparsers.add_parser("validate", help="Run Gate 9F automated validation suite")

    parser_cleanup = subparsers.add_parser("cleanup", help="Safely reverse Phase 9 transaction batch")
    parser_cleanup.add_argument("--apply", action="store_true", help="Apply cleanup deletion")

    args = parser.parse_args()

    if args.command == "dry-run":
        run_dry_run()
    elif args.command == "january-pilot":
        run_live_generation(months=[1], gate_name="GATE 9C (JANUARY PILOT)")
    elif args.command == "scenario-pilot":
        run_live_generation(months=[1, 2, 3, 4, 5], gate_name="GATE 9D (SCENARIO PILOT JAN-MAY)")
    elif args.command == "full-year":
        run_live_generation(months=list(range(1, 13)), gate_name="GATE 9E (FULL-YEAR JAN-DEC)")
    elif args.command == "validate":
        run_validate()
    elif args.command == "cleanup":
        cleanup_phase9_batch(dry_run=not args.apply)

if __name__ == "__main__":
    main()
