# Day 1 — Problem Framing

## Topic
**US AI Jobs Exposure × Wage Growth**

## Research question
Do occupation groups with higher measured exposure to AI capabilities also show different wage growth trajectories in recent US data?

## Unit of analysis
- Occupation major groups (CPS/BLS major occupation buckets used by FRED earnings series)
- Annual observations (2000–latest available)

## Data strategy (public real data only)
1. **AI exposure by occupation**
   - Source: Felten-Raj-Seamans AIOE dataset (public repository)
   - Measure: AIOE score by 6-digit SOC code, aggregated to major occupation groups using SOC first two digits.
2. **Wage outcomes**
   - Source: FRED series for median usual weekly nominal earnings by major occupation group (annual).

## Planned outputs for Day 1–3
- Day 2: reproducible ingestion + harmonization pipeline and analysis-ready panel.
- Day 3: exploratory analysis (cross-sectional and pooled correlations), plots, and interpretation note.

## Risks / limitations recognized up front
- Small cross-section (five major groups) for top-line comparisons.
- Exposure measure is static and capability-based, not realized adoption.
- Nominal earnings are not inflation-adjusted in this first pass.
- Major-group aggregation may mask within-group heterogeneity.
