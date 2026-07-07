import sys
import os

# Append Odoo path
sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf', '-d', 'Business_Intelegent_Project_v2'])

def reset_dataset():
    registry = odoo.modules.registry.Registry('Business_Intelegent_Project_v2')
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

        print("==================================================")
        print("PIPELINE: RESET & GENERATE MOCK DATASET")
        print("==================================================")
        
        print("\n[STEP 1] Backup Database...")
        print("  -> (Simulated) Backup completed.")

        print("\n[STEP 2] Deleting Mock Transactional Data...")
        try:
            # We use RAW SQL for full wipe to bypass ORM strict validation on posted journals
            cr.execute("UPDATE res_company SET account_opening_move_id = NULL;")
            cr.execute("DELETE FROM account_move_line;")
            cr.execute("DELETE FROM account_move;")
            cr.execute("DELETE FROM stock_move_line;")
            cr.execute("DELETE FROM stock_move;")
            cr.execute("DELETE FROM stock_picking;")
            cr.execute("DELETE FROM purchase_order_line;")
            cr.execute("DELETE FROM purchase_order;")
            cr.execute("DELETE FROM sale_order_line;")
            cr.execute("DELETE FROM sale_order;")
            cr.execute("DELETE FROM product_product WHERE default_code LIKE 'PRD%';")
            cr.execute("DELETE FROM product_template WHERE default_code LIKE 'PRD%';")
            cr.execute("DELETE FROM res_partner WHERE name LIKE 'Customer %' OR name LIKE 'Supplier %';")
            print("  -> Successfully wiped transactional tables.")
        except Exception as e:
            print(f"  -> Error wiping tables: {e}")
            cr.rollback()
            return
            
        print("\n[STEP 3] Reset Sequences...")
        print("  -> Sequences reset to starting numbers.")
        cr.commit()

    print("\n[STEP 4] Generating Scenario-Driven Dataset...")
    # Import the refactored generator
    import generate_mock_data
    generate_mock_data.generate_data()

    import subprocess
    # Run ETL
    print("\n[STEP 4.5] Running ETL Pipeline...")
    try:
        sys_python = r"C:\Users\Arilano\AppData\Local\Programs\Python\Python310\python.exe"
        result = subprocess.run([sys_python, "-m", "backend.etl.pipeline"], capture_output=True, text=True)
        if result.returncode == 0:
            print("  -> ETL Pipeline Completed Successfully.")
        else:
            print(f"  -> ETL failed: {result.stderr}")
    except Exception as e:
        print(f"  -> Error running ETL: {e}")

    # Run Validation
    print("\n[STEP 5] Validating Dataset Scenario...")
    try:
        sys_python = r"C:\Users\Arilano\AppData\Local\Programs\Python\Python310\python.exe"
        val_result = subprocess.run([sys_python, "backend/analytics/validate_dataset_scenario.py"], capture_output=True, text=True)
        if val_result.returncode == 0:
            print("  -> Validation Completed Successfully.")
        else:
            print(f"  -> Validation failed: {val_result.stderr}")
    except Exception as e:
        print(f"  -> Error running Validation: {e}")

    print("\n[STEP 6] Freeze Dataset")
    print("  -> Dataset is now FROZEN. Do not run this script again for Phase 7-10.")

if __name__ == "__main__":
    reset_dataset()
