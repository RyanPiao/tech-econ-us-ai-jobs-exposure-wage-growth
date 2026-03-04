# Tech-Econ Study: US AI Jobs Exposure × Wage Growth

Canonical project repo for approved topic:
`tech-econ-us-ai-jobs-exposure-wage-growth`

## Status
- ✅ Day 1: problem framing
- ✅ Day 2: ingestion/spec lock/panel construction
- ✅ Day 3: exploratory analysis artifacts

## Folder structure
```text
.
├── README.md
├── requirements.txt
├── docs/
│   ├── DAY1_problem_framing.md
│   ├── DAY2_data_extraction_spec.md
│   ├── DAY2_preanalysis_lock.md
│   └── DAY3_eda_note.md
├── scripts/
│   ├── day2_ingest_build_panel.py
│   ├── day3_eda.py
│   └── run_day2_day3.py
├── data_raw/
├── data_analysis/
└── outputs/
```

## Data sources
- AIOE appendix (Felten, Raj, Seamans):
  - https://raw.githubusercontent.com/AIOE-Data/AIOE/main/AIOE_DataAppendix.xlsx
- FRED annual occupation earnings series:
  - LEU0254524600A
  - LEU0254543400A
  - LEU0254550200A
  - LEU0254557400A
  - LEU0254566200A

## Reproduce
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_day2_day3.py
```

## Notes
This phase is descriptive and reproducible, with no causal claims.
