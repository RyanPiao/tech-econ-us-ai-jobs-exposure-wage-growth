# Step 3 — EDA Note

## Scope
Exploratory diagnostics linking major-group AI exposure (AIOE) and nominal weekly wage growth outcomes.

## Key descriptive outputs
- Latest year in panel: **2025**
- Corr(exposure, cumulative growth in latest year): **0.4369**
- Corr(exposure, average YoY growth): **0.4317**
- Corr(exposure, pooled YoY growth): **0.0495**

## Artifacts
- `outputs/step3_group_latest_snapshot.csv`
- `outputs/step3_yearly_corr.csv`
- `outputs/step3_eda_metrics.json`
- `outputs/step3_exposure_vs_cum_growth_latest.png`

## Interpretation guardrails
- These are descriptive correlations over a very small cross-section (5 major groups).
- Exposure is capability-based and static; this does not identify realized AI adoption effects.
- Results should be treated as directional signal generation for later, richer designs.
