#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_ANALYSIS = ROOT / "data_analysis"
OUTPUTS = ROOT / "outputs"
DOCS = ROOT / "docs"


def main() -> None:
    panel = pd.read_csv(DATA_ANALYSIS / "panel_annual_majorgroup.csv")
    panel = panel.sort_values(["major_group", "year"]).reset_index(drop=True)

    latest_year = int(panel["year"].max())
    latest = panel[panel["year"] == latest_year].copy()

    avg_growth = (
        panel.dropna(subset=["wage_growth_yoy"])
        .groupby("major_group", as_index=False)["wage_growth_yoy"]
        .mean()
        .rename(columns={"wage_growth_yoy": "avg_wage_growth_yoy"})
    )

    latest = latest.merge(avg_growth, on="major_group", how="left")
    latest.to_csv(OUTPUTS / "step3_group_latest_snapshot.csv", index=False)

    corr_latest_cum = float(latest["ai_exposure_mean"].corr(latest["cum_growth_since_start"]))
    corr_latest_avg = float(latest["ai_exposure_mean"].corr(latest["avg_wage_growth_yoy"]))
    pooled = panel.dropna(subset=["wage_growth_yoy"]).copy()
    corr_pooled = float(pooled["ai_exposure_mean"].corr(pooled["wage_growth_yoy"]))

    yearly_corr = (
        pooled.groupby("year")
        .apply(lambda g: g["ai_exposure_mean"].corr(g["wage_growth_yoy"]))
        .reset_index(name="corr_exposure_vs_wage_growth_yoy")
    )
    yearly_corr.to_csv(OUTPUTS / "step3_yearly_corr.csv", index=False)

    # Scatter plot (latest year)
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(latest["ai_exposure_mean"], latest["cum_growth_since_start"], s=70)
    for _, r in latest.iterrows():
        ax.annotate(r["major_group"], (r["ai_exposure_mean"], r["cum_growth_since_start"]), xytext=(5, 5), textcoords="offset points", fontsize=8)

    x = latest["ai_exposure_mean"].values
    y = latest["cum_growth_since_start"].values
    if len(np.unique(x)) > 1:
        slope, intercept = np.polyfit(x, y, 1)
        x_line = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_line, slope * x_line + intercept, linestyle="--")

    ax.set_title(f"AI Exposure vs Cumulative Wage Growth ({latest_year})")
    ax.set_xlabel("Mean AI Exposure (AIOE), major group")
    ax.set_ylabel("Cumulative nominal wage growth since start")
    fig.tight_layout()
    fig.savefig(OUTPUTS / "step3_exposure_vs_cum_growth_latest.png", dpi=150)
    plt.close(fig)

    metrics = {
        "latest_year": latest_year,
        "corr_latest_exposure_vs_cum_growth": corr_latest_cum,
        "corr_latest_exposure_vs_avg_growth": corr_latest_avg,
        "corr_pooled_exposure_vs_yoy_growth": corr_pooled,
        "n_groups_latest": int(latest.shape[0]),
        "n_obs_pooled": int(pooled.shape[0]),
    }
    with open(OUTPUTS / "step3_eda_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    note = f"""# Step 3 — EDA Note

## Scope
Exploratory diagnostics linking major-group AI exposure (AIOE) and nominal weekly wage growth outcomes.

## Key descriptive outputs
- Latest year in panel: **{latest_year}**
- Corr(exposure, cumulative growth in latest year): **{corr_latest_cum:.4f}**
- Corr(exposure, average YoY growth): **{corr_latest_avg:.4f}**
- Corr(exposure, pooled YoY growth): **{corr_pooled:.4f}**

## Artifacts
- `outputs/step3_group_latest_snapshot.csv`
- `outputs/step3_yearly_corr.csv`
- `outputs/step3_eda_metrics.json`
- `outputs/step3_exposure_vs_cum_growth_latest.png`

## Interpretation guardrails
- These are descriptive correlations over a very small cross-section (5 major groups).
- Exposure is capability-based and static; this does not identify realized AI adoption effects.
- Results should be treated as directional signal generation for later, richer designs.
"""
    (DOCS / "STEP3_eda_note.md").write_text(note)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
