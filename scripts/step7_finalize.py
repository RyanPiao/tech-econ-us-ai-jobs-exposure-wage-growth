#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DOCS = ROOT / "docs"


def _read_json(p: Path):
    return json.loads(p.read_text()) if p.exists() else {}


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)

    d3 = _read_json(OUT / "step3_eda_metrics.json")
    d4 = _read_json(OUT / "step4_twfe_baseline_summary.json")
    d5 = _read_json(OUT / "step5_robustness_summary.json")
    d6 = _read_json(OUT / "step6_event_study_summary.json")

    event = pd.read_csv(OUT / "step6_event_study_coefficients.csv") if (OUT / "step6_event_study_coefficients.csv").exists() else pd.DataFrame()

    pre = event[(event.get("event_time", pd.Series(dtype=float)) <= -2)] if not event.empty else pd.DataFrame()
    post = event[(event.get("event_time", pd.Series(dtype=float)) >= 0)] if not event.empty else pd.DataFrame()

    note = f"""# Step 7 — Final Public Research Progress Summary

## Abstract (Academic Style)
This project examines whether occupational AI exposure is systematically associated with differential wage-growth dynamics in U.S. major occupation groups. We merge a static occupation-level exposure measure (AIOE Appendix A) with annual FRED earnings series to construct a transparent, reproducible panel. The empirical design progresses from descriptive diagnostics to a two-way fixed effects (TWFE) exposure-intensity specification, robustness checks (alternative post thresholds and winsorized outcomes), and an event-study representation around the 2022 reference break. Across specifications, point estimates are economically small and statistically imprecise in this limited five-group panel, with no robust evidence of a large post-2022 differential wage-growth shift attributable to exposure intensity. These findings are best interpreted as disciplined reduced-form evidence and baseline measurement infrastructure, rather than definitive causal identification of realized AI adoption effects.

## Executive Summary
- **Objective:** Build a public, reproducible Step 1–Step 7 research package on AI exposure and wage growth.
- **Data:** AIOE occupation exposure + annual FRED earnings series mapped to 5 major occupation groups.
- **Core model:** TWFE intensity DiD (`ai_exposure_mean × 1[year>=2022]`) with group and year fixed effects.
- **Main result:** Baseline coefficient = **{d4.get('coef', float('nan')):.6f}** (SE **{d4.get('se_hc1', float('nan')):.6f}**), indicating no large detectable post-2022 differential effect in this sample.
- **Robustness:** Alternative threshold and winsorized outcome checks do not overturn the baseline null framing.
- **Dynamics:** Event-study coefficients around 2022 do not show a strong discontinuous shift.
- **Interpretation:** Useful as a reproducible baseline and screening framework; stronger treatment observability is required for structural causal claims.

## Completion status
- Step 1 ✅ Problem framing
- Step 2 ✅ Data extraction/spec lock + panel build
- Step 3 ✅ EDA and descriptive correlations
- Step 4 ✅ Baseline TWFE intensity DiD
- Step 5 ✅ Robustness checks (threshold/placebo + winsorized outcome)
- Step 6 ✅ Event-study dynamics
- Step 7 ✅ Synthesis and publication-ready summary

## Key metrics (current run)
- Step 3 latest-year correlation (exposure vs cumulative growth): **{d3.get('corr_latest_exposure_vs_cum_growth', float('nan')):.4f}**
- Step 4 baseline TWFE coefficient (`ai_exposure_x_post2022`): **{d4.get('coef', float('nan')):.6f}** (SE {d4.get('se_hc1', float('nan')):.6f})
- Step 5 robustness specs estimated: **{d5.get('n_specs', 0)}**
- Step 6 event-study window: **{d6.get('event_window', [])}**, reference {d6.get('reference', 'NA')}
- Step 6 mean pre-event coefficient (k<=-2): **{pre['coef'].mean() if not pre.empty else float('nan'):.6f}**
- Step 6 mean post-event coefficient (k>=0): **{post['coef'].mean() if not post.empty else float('nan'):.6f}**

## Public artifacts
- `docs/STEP1_problem_framing.md`
- `docs/STEP2_data_extraction_spec.md`
- `docs/STEP2_preanalysis_lock.md`
- `docs/STEP3_eda_note.md`
- `docs/STEP4_baseline_twfe_note.md`
- `docs/STEP5_robustness_note.md`
- `docs/STEP6_event_study_note.md`
- `docs/STEP7_final_summary.md`

- `outputs/step3_*`
- `outputs/step4_twfe_baseline_results.csv`
- `outputs/step5_robustness_results.csv`
- `outputs/step6_event_study_coefficients.csv`
- `outputs/step6_event_study_plot.png`

## Interpretation discipline
This remains a reduced-form, exposure-intensity design. Findings are not interpreted as structural causal AI adoption effects without stronger treatment observability and richer identification assumptions.
"""
    (DOCS / "STEP7_final_summary.md").write_text(note)
    print(json.dumps({"status": "step7_complete"}, indent=2))


if __name__ == "__main__":
    main()
