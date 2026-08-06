"""
Organize Remaining Root Scripts
==============================
Moves:
- execute_final_clean_restructure.py -> scripts/execute_final_clean_restructure.py
- inspect_models.py -> ERP-BIDSS/tools/inspection/inspect_odoo_models.py
- investigate_scope.py -> ERP-BIDSS/tools/diagnostics/investigate_product_scope.py
"""

import sys
import os
import shutil

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def organize():
    os.makedirs(os.path.join(ROOT_DIR, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, "ERP-BIDSS", "tools", "inspection"), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, "ERP-BIDSS", "tools", "diagnostics"), exist_ok=True)

    moves = [
        ("execute_final_clean_restructure.py", "scripts/execute_final_clean_restructure.py"),
        ("inspect_models.py", "ERP-BIDSS/tools/inspection/inspect_odoo_models.py"),
        ("investigate_scope.py", "ERP-BIDSS/tools/diagnostics/investigate_product_scope.py")
    ]

    for src_name, dst_rel in moves:
        src = os.path.join(ROOT_DIR, src_name)
        dst = os.path.join(ROOT_DIR, dst_rel)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"  [MOVED] {src_name} -> {dst_rel}")

    print("\n[SUCCESS] Root scripts organized cleanly!")

if __name__ == "__main__":
    organize()
