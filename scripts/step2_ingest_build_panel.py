#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data_raw"
DATA_ANALYSIS = ROOT / "data_analysis"
OUTPUTS = ROOT / "outputs"
for p in [DATA_RAW, DATA_ANALYSIS, OUTPUTS]:
    p.mkdir(parents=True, exist_ok=True)

AIOE_URL = "https://raw.githubusercontent.com/AIOE-Data/AIOE/main/AIOE_DataAppendix.xlsx"

SERIES = {
    "Management, professional, and related occupations": "LEU0254524600A",
    "Service occupations": "LEU0254543400A",
    "Sales and office occupations": "LEU0254550200A",
    "Natural resources, construction, and maintenance occupations": "LEU0254557400A",
    "Production, transportation, and material moving occupations": "LEU0254566200A",
}

SOC_TO_MAJOR = {
    11: "Management, professional, and related occupations",
    13: "Management, professional, and related occupations",
    15: "Management, professional, and related occupations",
    17: "Management, professional, and related occupations",
    19: "Management, professional, and related occupations",
    21: "Management, professional, and related occupations",
    23: "Management, professional, and related occupations",
    25: "Management, professional, and related occupations",
    27: "Management, professional, and related occupations",
    29: "Management, professional, and related occupations",
    31: "Service occupations",
    33: "Service occupations",
    35: "Service occupations",
    37: "Service occupations",
    39: "Service occupations",
    41: "Sales and office occupations",
    43: "Sales and office occupations",
    45: "Natural resources, construction, and maintenance occupations",
    47: "Natural resources, construction, and maintenance occupations",
    49: "Natural resources, construction, and maintenance occupations",
    51: "Production, transportation, and material moving occupations",
    53: "Production, transportation, and material moving occupations",
}


def build_ai_exposure() -> pd.DataFrame:
    aioe = pd.read_excel(AIOE_URL, sheet_name="Appendix A")
    aioe.to_csv(DATA_RAW / "aioe_appendix_a_snapshot.csv", index=False)

    aioe["soc2"] = aioe["SOC Code"].astype(str).str.extract(r"^(\d{2})")
    aioe["soc2"] = pd.to_numeric(aioe["soc2"], errors="coerce")
    aioe["major_group"] = aioe["soc2"].map(SOC_TO_MAJOR)

    exposure = (
        aioe.dropna(subset=["major_group", "AIOE"])
        .groupby("major_group", as_index=False)
        .agg(
            ai_exposure_mean=("AIOE", "mean"),
            ai_exposure_median=("AIOE", "median"),
            n_soc_occupations=("AIOE", "count"),
        )
    )
    exposure.to_csv(DATA_ANALYSIS / "ai_exposure_by_major_group.csv", index=False)
    return exposure


def build_wage_panel() -> pd.DataFrame:
    frames = []
    for major_group, sid in SERIES.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
        df = pd.read_csv(url)
        df.to_csv(DATA_RAW / f"{sid}.csv", index=False)
        df.columns = ["date", "weekly_nominal_earnings"]
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["year"] = df["date"].dt.year
        df["weekly_nominal_earnings"] = pd.to_numeric(df["weekly_nominal_earnings"], errors="coerce")
        df = df[["year", "weekly_nominal_earnings"]].dropna()
        df["major_group"] = major_group
        df["series_id"] = sid
        frames.append(df)

    panel = pd.concat(frames, ignore_index=True)
    panel = panel.sort_values(["major_group", "year"]).reset_index(drop=True)
    return panel


def main() -> None:
    exposure = build_ai_exposure()
    wage_panel = build_wage_panel()

    panel = wage_panel.merge(exposure, on="major_group", how="left")
    panel["wage_growth_yoy"] = panel.groupby("major_group")["weekly_nominal_earnings"].pct_change()
    base = panel.groupby("major_group")["weekly_nominal_earnings"].transform("first")
    panel["cum_growth_since_start"] = panel["weekly_nominal_earnings"] / base - 1.0

    panel.to_csv(DATA_ANALYSIS / "panel_annual_majorgroup.csv", index=False)

    summary = {
        "n_rows": int(panel.shape[0]),
        "n_groups": int(panel["major_group"].nunique()),
        "year_min": int(panel["year"].min()),
        "year_max": int(panel["year"].max()),
        "series_used": SERIES,
        "source_aioe": AIOE_URL,
    }
    with open(OUTPUTS / "step2_panel_build_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
