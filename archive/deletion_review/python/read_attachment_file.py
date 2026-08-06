import sys
import os

filestore_dir = r"c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo_data\filestore\Business_Intelegent_Project_v2"
fname = os.path.join(filestore_dir, "91", "916e55a53c15462d7288b31e8bf53874b17c01ff")

if os.path.exists(fname):
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
        print("Attachment File Content (First 500 chars):")
        print(content[:500])
else:
    print("File not found:", fname)
