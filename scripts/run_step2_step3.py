#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for script in ["scripts/step2_ingest_build_panel.py", "scripts/step3_eda.py"]:
    subprocess.run([sys.executable, str(ROOT / script)], check=True)
