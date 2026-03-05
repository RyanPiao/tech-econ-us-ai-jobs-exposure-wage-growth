# Day 7 — Final Public Research Progress Summary

## Abstract (Academic Style)
This project examines whether occupational AI exposure is systematically associated with differential wage-growth dynamics in U.S. major occupation groups. We merge a static occupation-level exposure measure (AIOE Appendix A) with annual FRED earnings series to construct a transparent, reproducible panel. The empirical design progresses from descriptive diagnostics to a two-way fixed effects (TWFE) exposure-intensity specification, robustness checks (alternative post thresholds and winsorized outcomes), and an event-study representation around the 2022 reference break. Across specifications, point estimates are economically small and statistically imprecise in this limited five-group panel, with no robust evidence of a large post-2022 differential wage-growth shift attributable to exposure intensity. These findings are best interpreted as disciplined reduced-form evidence and baseline measurement infrastructure, rather than definitive causal identification of realized AI adoption effects.

## Executive Summary
- **Objective:** Build a public, reproducible Day 1–Day 7 research package on AI exposure and wage growth.
- **Data:** AIOE occupation exposure + annual FRED earnings series mapped to 5 major occupation groups.
- **Core model:** TWFE intensity DiD (`ai_exposure_mean × 1[year>=2022]`) with group and year fixed effects.
- **Main result:** Baseline coefficient = **-0.001273** (SE **0.002836**), indicating no large detectable post-2022 differential effect in this sample.
- **Robustness:** Alternative threshold and winsorized outcome checks do not overturn the baseline null framing.
- **Dynamics:** Event-study coefficients around 2022 do not show a strong discontinuous shift.
- **Interpretation:** Useful as a reproducible baseline and screening framework; stronger treatment observability is required for structural causal claims.

## Completion status
- Day 1 ✅ Problem framing
- Day 2 ✅ Data extraction/spec lock + panel build
- Day 3 ✅ EDA and descriptive correlations
- Day 4 ✅ Baseline TWFE intensity DiD
- Day 5 ✅ Robustness checks (threshold/placebo + winsorized outcome)
- Day 6 ✅ Event-study dynamics
- Day 7 ✅ Synthesis and publication-ready summary

## Key metrics (current run)
- Day 3 latest-year correlation (exposure vs cumulative growth): **0.4369**
- Day 4 baseline TWFE coefficient (`ai_exposure_x_post2022`): **-0.001273** (SE 0.002836)
- Day 5 robustness specs estimated: **4**
- Day 6 event-study window: **[-6, 3]**, reference -1
- Day 6 mean pre-event coefficient (k<=-2): **-0.000447**
- Day 6 mean post-event coefficient (k>=0): **-0.001379**

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
