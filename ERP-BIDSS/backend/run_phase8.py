import argparse
import sys
from odoo.audit_logic import run_audit
from odoo.repair_odoo_records import repair_integrity
from odoo.cleanup_portfolio_data import perform_cleanup

def audit():
    print("[PHASE 8] Running Audit...")
    run_audit()

def repair(dry_run):
    repair_integrity(dry_run)

def cleanup(dry_run, apply, confirm):
    perform_cleanup(dry_run, confirm)

def setup_master():
    print("[PHASE 8] Running Master Setup...")

def validate():
    print("[PHASE 8] Running Validation...")

def idempotency_test():
    print("[PHASE 8] Running Idempotency Test...")

def main():
    parser = argparse.ArgumentParser(description="Phase 8 Orchestrator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Audit subcommand
    parser_audit = subparsers.add_parser("audit", help="Run audit and generate cleanup candidate manifest")

    # Repair subcommand
    parser_repair = subparsers.add_parser("repair", help="Repair Odoo integrity (e.g. broken dashboards)")
    parser_repair.add_argument("--dry-run", action="store_true", help="Perform a dry run")

    # Cleanup subcommand
    parser_cleanup = subparsers.add_parser("cleanup", help="Cleanup synthetic portfolio data")
    parser_cleanup.add_argument("--dry-run", action="store_true", help="Perform a dry run")
    parser_cleanup.add_argument("--apply", action="store_true", help="Apply cleanup")
    parser_cleanup.add_argument("--confirm", type=str, help="Confirmation token")

    # Setup subcommand
    parser_setup = subparsers.add_parser("setup-master", help="Setup 2026 portfolio master data")

    # Validate subcommand
    parser_validate = subparsers.add_parser("validate", help="Validate master data constraints")

    # Idempotency test subcommand
    parser_idempotency = subparsers.add_parser("idempotency-test", help="Test script idempotency")

    args = parser.parse_args()

    if args.command == "audit":
        audit()
    elif args.command == "repair":
        dry_run = not args.dry_run == False # Meaning if --dry-run is omitted it defaults to False, but we want default dry run? We can just pass args.dry_run
        repair(args.dry_run)
    elif args.command == "cleanup":
        if args.apply and args.confirm != "PHASE8-WIPE-APPROVED":
            print("ERROR: --apply requires --confirm PHASE8-WIPE-APPROVED")
            sys.exit(1)
        dry_run = not args.apply
        cleanup(dry_run, args.apply, args.confirm)
    elif args.command == "setup-master":
        setup_master()
    elif args.command == "validate":
        validate()
    elif args.command == "idempotency-test":
        idempotency_test()

if __name__ == "__main__":
    main()
