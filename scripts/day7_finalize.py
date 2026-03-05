#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DOCS = ROOT / "docs"


def _read_json(p: Path):
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    DOCS.mkdir(parents=True, exist_ok=True)

    d3 = _read_json(OUT / "day3_eda_metrics.json")
    d4 = _read_json(OUT / "day4_twfe_baseline_summary.json")
    d5 = _read_json(OUT / "day5_robustness_summary.json")
    d6 = _read_json(OUT / "day6_event_study_summary.json")

    robustness = pd.read_csv(OUT / "day5_robustness_results.csv") if (OUT / "day5_robustness_results.csv").exists() else pd.DataFrame()
    event = pd.read_csv(OUT / "day6_event_study_coefficients.csv") if (OUT / "day6_event_study_coefficients.csv").exists() else pd.DataFrame()

    pre = event[(event.get("event_time", pd.Series(dtype=float)) <= -2)] if not event.empty else pd.DataFrame()
    post = event[(event.get("event_time", pd.Series(dtype=float)) >= 0)] if not event.empty else pd.DataFrame()

    note = f"""# Day 7 — Final Public Research Progress Summary

## Completion status
- Day 1 ✅ Problem framing
- Day 2 ✅ Data extraction/spec lock + panel build
- Day 3 ✅ EDA and descriptive correlations
- Day 4 ✅ Baseline TWFE intensity DiD
- Day 5 ✅ Robustness checks (threshold/placebo + winsorized outcome)
- Day 6 ✅ Event-study dynamics
- Day 7 ✅ Synthesis and publication-ready summary

## Key metrics (current run)
- Day 3 latest-year correlation (exposure vs cumulative growth): **{d3.get('corr_latest_exposure_vs_cum_growth', float('nan')):.4f}**
- Day 4 baseline TWFE coefficient (`ai_exposure_x_post2022`): **{d4.get('coef', float('nan')):.6f}** (SE {d4.get('se_hc1', float('nan')):.6f})
- Day 5 robustness specs estimated: **{d5.get('n_specs', 0)}**
- Day 6 event-study window: **{d6.get('event_window', [])}**, reference {d6.get('reference', 'NA')}
- Day 6 mean pre-event coefficient (k<=-2): **{pre['coef'].mean() if not pre.empty else float('nan'):.6f}**
- Day 6 mean post-event coefficient (k>=0): **{post['coef'].mean() if not post.empty else float('nan'):.6f}**

## Public artifacts
- `docs/DAY1_problem_framing.md`
- `docs/DAY2_data_extraction_spec.md`
- `docs/DAY2_preanalysis_lock.md`
- `docs/DAY3_eda_note.md`
- `docs/DAY4_baseline_twfe_note.md`
- `docs/DAY5_robustness_note.md`
- `docs/DAY6_event_study_note.md`
- `docs/DAY7_final_summary.md`

- `outputs/day3_*`
- `outputs/day4_twfe_baseline_results.csv`
- `outputs/day5_robustness_results.csv`
- `outputs/day6_event_study_coefficients.csv`
- `outputs/day6_event_study_plot.png`

## Interpretation discipline
This remains a reduced-form, exposure-intensity design. Findings are not interpreted as structural causal AI adoption effects without stronger treatment observability and richer identification assumptions.
"""
    (DOCS / "DAY7_final_summary.md").write_text(note)
    print(json.dumps({"status": "day7_complete"}, indent=2))


if __name__ == "__main__":
    main()
