import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "dashboard_assets" / "templates"
PIVOT_DIR = TEMPLATES_DIR / "pivot"
FALLBACK_DIR = TEMPLATES_DIR / "fallback"
REFERENCE_DIR = BASE_DIR / "dashboard_assets" / "reference"
