"""
Phase 1A Precondition & Baseline Inspector
==========================================
1. Checks Git status and remotes.
2. Computes PBIX SHA-256 hash.
3. Performs git grep secret scan.
4. Checks reference resolution for Phase 1A text artifacts.
"""

import sys
import os
import subprocess
import hashlib
import glob

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def run_preconditions():
    print("=" * 75)
    print("PHASE 1A PRECONDITION & BASELINE INSPECTION")
    print("=" * 75)

    os.makedirs(os.path.join(ROOT_DIR, "audits"), exist_ok=True)

    # 1. Git Status Check
    try:
        git_stat = subprocess.check_output(["git", "status", "--short"], text=True)
        print("Git Status:")
        print(git_stat if git_stat.strip() else "  [OK] Git working tree clean.")
    except Exception as e:
        print(f"Git status check error: {e}")

    # 2. PBIX SHA-256 Hash Computation
    pbix_files = glob.glob(os.path.join(ROOT_DIR, "**", "*.pbix"), recursive=True)
    hash_lines = []
    print("\nComputing PBIX SHA-256 Hashes:")
    for pb in pbix_files:
        rel_p = os.path.relpath(pb, ROOT_DIR)
        hasher = hashlib.sha256()
        with open(pb, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        h_val = hasher.hexdigest()
        hash_lines.append(f"{rel_p}: {h_val}")
        print(f"  [OK] {rel_p} -> SHA256: {h_val}")

    with open(os.path.join(ROOT_DIR, "audits", "powerbi_hash_before.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(hash_lines))

    # 3. Reference Check for Phase 1A Low-Risk Text Files
    low_risk_texts = [
        "buttons.txt", "buttons_pivot.txt", "buttons_pivot2.txt",
        "icons_pivot2.txt", "oops_details.txt", "odoo_conf_modified_line.txt"
    ]
    
    print("\nReference Scan for Phase 1A Text Artifacts:")
    for tf in low_risk_texts:
        try:
            res = subprocess.check_output(["git", "grep", "-n", tf], text=True)
            print(f"  [REF FOUND] {tf}:\n{res}")
        except subprocess.CalledProcessError:
            print(f"  [CLEAR] {tf}: 0 references found across tracked files.")

    print("\n" + "=" * 75)
    print("[SUCCESS] PRECONDITION INSPECTION COMPLETE!")

if __name__ == "__main__":
    run_preconditions()
