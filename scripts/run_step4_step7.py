#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

ORDER = [
    "step4_baseline_twfe.py",
    "step5_robustness.py",
    "step6_event_study.py",
    "step7_finalize.py",
]


def main() -> None:
    for s in ORDER:
        print(f"[RUN] {s}")
        subprocess.run([sys.executable, str(SCRIPTS / s)], check=True, cwd=ROOT)
    print("[OK] Step4-Step7 completed.")


if __name__ == "__main__":
    main()
