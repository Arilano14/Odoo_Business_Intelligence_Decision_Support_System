import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db
from sqlalchemy import text

query = """
INSERT INTO ir_module_module (name, state, author, website, summary, description, license, application, auto_install)
VALUES ('obidss_operational_bi', 'installed', 'Senior Odoo BI Engineer', 'https://github.com/Arilano14', '{"en_US": "OBIDSS Operational BI"}'::jsonb, '{"en_US": "OBIDSS App"}'::jsonb, 'LGPL-3', true, false)
ON CONFLICT (name) DO UPDATE SET state = 'installed';
"""

with db.source_engine.connect() as conn:
    conn.execute(text(query))
    conn.commit()
    print("Successfully inserted/updated obidss_operational_bi in ir_module_module!")
