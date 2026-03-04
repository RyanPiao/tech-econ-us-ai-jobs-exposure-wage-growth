# Day 2 — Preanalysis Lock (Exploratory Phase)

This lock records the plan before Day 3 interpretation.

## Outcome
- Primary: annual YoY growth in median weekly nominal earnings (`wage_growth_yoy`)
- Secondary: cumulative growth since first available year (`cum_growth_since_start`)

## Exposure
- `ai_exposure_mean` (major-group average AIOE)

## Planned Day 3 diagnostics
1. Cross-sectional association in latest year:
   - Corr(`ai_exposure_mean`, `cum_growth_since_start`)
2. Cross-sectional association of long-run average growth:
   - Corr(`ai_exposure_mean`, mean annual `wage_growth_yoy`)
3. Pooled association (group-year panel, descriptive):
   - Corr(`ai_exposure_mean`, `wage_growth_yoy`)

## Non-goals for this phase
- No causal claims
- No policy inference beyond descriptive patterns
