#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for script in ["scripts/day2_ingest_build_panel.py", "scripts/day3_eda.py"]:
    subprocess.run([str(ROOT / script)], check=True)
