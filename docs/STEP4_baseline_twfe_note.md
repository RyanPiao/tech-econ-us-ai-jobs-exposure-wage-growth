# Day 4 — Baseline TWFE Intensity DiD

Specification:
- Outcome: `wage_growth_yoy`
- Treatment intensity: `ai_exposure_mean × 1[year>=2022]`
- Fixed effects: major-group FE and year FE
- Inference: HC1 robust SE

Key coefficient (`ai_exposure_x_post2022`):
- Coef: **-0.001273**
- SE: **0.002836**
- t: **-0.449**
- 95% CI: **[-0.006830, 0.004285]**
- N: **125**
