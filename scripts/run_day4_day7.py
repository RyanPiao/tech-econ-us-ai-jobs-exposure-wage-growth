#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

ORDER = [
    "day4_baseline_twfe.py",
    "day5_robustness.py",
    "day6_event_study.py",
    "day7_finalize.py",
]


def main() -> None:
    for s in ORDER:
        print(f"[RUN] {s}")
        subprocess.run([sys.executable, str(SCRIPTS / s)], check=True, cwd=ROOT)
    print("[OK] Day4-Day7 completed.")


if __name__ == "__main__":
    main()
