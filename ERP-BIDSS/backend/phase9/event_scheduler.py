"""
Phase 9 Event Scheduler Module.

Combines planned Sales Orders, Purchase Orders, Internal Transfers, and Scrap Operations
into a unified chronological event queue sorted strictly by date for FY 2026.
"""

from phase9.config import SCENARIO_YEAR, MONTHLY_TARGETS

def schedule_events(so_plan, po_plan, ops_plan):
    """
    Args:
        so_plan: dict output from sales_generator (contains 'records' list)
        po_plan: dict output from purchase_generator (contains 'records' list)
        ops_plan: dict output from inventory_ops (contains 'int_records' and 'scrap_records')
    Returns:
        chronological_queue: list of event dicts ordered by date:
            [{'event_type': 'SO'|'PO'|'INT'|'SCRAP', 'date': 'YYYY-MM-DD HH:MM:SS', 'ref': str, 'payload': dict}, ...]
        monthly_event_summary: dict mapping month (1..12) -> count breakdown
    """
    events = []

    # 1. Add Sales Orders
    for rec in so_plan.get('records', []):
        events.append({
            'event_type': 'SO',
            'date': rec['date_order'],
            'month': rec['month'],
            'ref': rec['ref'],
            'payload': rec,
        })

    # 2. Add Purchase Orders
    for rec in po_plan.get('records', []):
        events.append({
            'event_type': 'PO',
            'date': rec['date_order'],
            'month': rec['month'],
            'ref': rec['ref'],
            'payload': rec,
        })

    # 3. Add Internal Transfers
    for rec in ops_plan.get('int_records', []):
        events.append({
            'event_type': 'INT',
            'date': rec['date'],
            'month': int(rec['date'].split('-')[1]),
            'ref': rec['ref'],
            'payload': rec,
        })

    # 4. Add Scrap Operations
    for rec in ops_plan.get('scrap_records', []):
        events.append({
            'event_type': 'SCRAP',
            'date': rec['date'],
            'month': int(rec['date'].split('-')[1]),
            'ref': rec['ref'],
            'payload': rec,
        })

    # Sort strictly by date string (YYYY-MM-DD HH:MM:SS)
    events.sort(key=lambda x: (x['date'], x['ref']))

    # Build monthly summary
    monthly_summary = {m: {'SO': 0, 'PO': 0, 'INT': 0, 'SCRAP': 0, 'TOTAL': 0} for m in range(1, 13)}
    for ev in events:
        m = ev['month']
        etype = ev['event_type']
        monthly_summary[m][etype] += 1
        monthly_summary[m]['TOTAL'] += 1

    return events, monthly_summary
