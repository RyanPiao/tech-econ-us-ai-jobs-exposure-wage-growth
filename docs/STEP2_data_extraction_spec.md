# Day 2 — Data Extraction Specification

## Public sources
1. **AIOE data appendix**
   - URL: https://raw.githubusercontent.com/AIOE-Data/AIOE/main/AIOE_DataAppendix.xlsx
   - Sheet used: `Appendix A`
   - Fields used: `SOC Code`, `Occupation Title`, `AIOE`

2. **FRED annual earnings series** (median usual weekly nominal earnings, second quartile)
   - Management/professional: `LEU0254524600A`
   - Service: `LEU0254543400A`
   - Sales/office: `LEU0254550200A`
   - Natural resources/construction/maintenance: `LEU0254557400A`
   - Production/transportation/material moving: `LEU0254566200A`

## Harmonization logic
- Parse first two digits from `SOC Code`.
- Map SOC major groups to the five FRED occupation group labels:
  - 11,13,15,17,19,21,23,25,27,29 → Management, professional, and related occupations
  - 31,33,35,37,39 → Service occupations
  - 41,43 → Sales and office occupations
  - 45,47,49 → Natural resources, construction, and maintenance occupations
  - 51,53 → Production, transportation, and material moving occupations

## Constructed variables
- `ai_exposure_mean` and `ai_exposure_median` by major group
- `weekly_nominal_earnings`
- `wage_growth_yoy`
- `cum_growth_since_start`

## Reproducibility
- All ingestion and transforms are in `scripts/day2_ingest_build_panel.py`
- Raw pulls are stored in `data_raw/`
- Analysis-ready panel is written to `data_analysis/panel_annual_majorgroup.csv`
