#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_analysis" / "panel_annual_majorgroup.csv"
OUT = ROOT / "outputs"
DOCS = ROOT / "docs"


def ols_hc1(X: np.ndarray, y: np.ndarray, names: list[str]) -> pd.DataFrame:
    m = np.isfinite(y) & np.isfinite(X).all(axis=1)
    X, y = X[m], y[m]
    n, k = X.shape
    inv = np.linalg.pinv(X.T @ X, rcond=1e-10)
    b = inv @ (X.T @ y)
    e = y - X @ b
    meat = X.T @ (X * (e[:, None] ** 2))
    cov = (n / max(n - k, 1)) * (inv @ meat @ inv)
    se = np.sqrt(np.clip(np.diag(cov), 0, np.inf))
    out = pd.DataFrame({"term": names, "coef": b, "se_hc1": se})
    out["t"] = out["coef"] / out["se_hc1"]
    out["ci95_low"] = out["coef"] - 1.96 * out["se_hc1"]
    out["ci95_high"] = out["coef"] + 1.96 * out["se_hc1"]
    out["n_obs"] = n
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA)
    df = df.dropna(subset=["wage_growth_yoy", "ai_exposure_mean", "year", "major_group"]).copy()
    df["post"] = (df["year"] >= 2022).astype(float)
    df["intensity_post"] = df["ai_exposure_mean"] * df["post"]

    # TWFE-style: include group FE + year FE; exposure level omitted (group-invariant).
    groups = sorted(df["major_group"].unique())
    years = sorted(df["year"].unique())
    g_dum = [ (df["major_group"] == g).astype(float).to_numpy() for g in groups[1:] ]
    t_dum = [ (df["year"] == y).astype(float).to_numpy() for y in years[1:] ]

    X = np.column_stack([
        np.ones(len(df)),
        df["intensity_post"].to_numpy(float),
        *g_dum,
        *t_dum,
    ])
    names = ["const", "ai_exposure_x_post2022", *[f"g_{g}" for g in groups[1:]], *[f"year_{y}" for y in years[1:]]]

    res = ols_hc1(X, df["wage_growth_yoy"].to_numpy(float), names)
    res.to_csv(OUT / "day4_twfe_baseline_results.csv", index=False)

    key = res.loc[res["term"] == "ai_exposure_x_post2022"].iloc[0].to_dict()
    summary = {
        "design": "TWFE intensity DiD",
        "post_start_year": 2022,
        "term": "ai_exposure_x_post2022",
        "coef": float(key["coef"]),
        "se_hc1": float(key["se_hc1"]),
        "t": float(key["t"]),
        "ci95_low": float(key["ci95_low"]),
        "ci95_high": float(key["ci95_high"]),
        "n_obs": int(key["n_obs"]),
    }
    (OUT / "day4_twfe_baseline_summary.json").write_text(json.dumps(summary, indent=2))

    note = f"""# Step 4 — Baseline TWFE Intensity DiD

Specification:
- Outcome: `wage_growth_yoy`
- Treatment intensity: `ai_exposure_mean × 1[year>=2022]`
- Fixed effects: major-group FE and year FE
- Inference: HC1 robust SE

Key coefficient (`ai_exposure_x_post2022`):
- Coef: **{summary['coef']:.6f}**
- SE: **{summary['se_hc1']:.6f}**
- t: **{summary['t']:.3f}**
- 95% CI: **[{summary['ci95_low']:.6f}, {summary['ci95_high']:.6f}]**
- N: **{summary['n_obs']}**
"""
    (DOCS / "DAY4_baseline_twfe_note.md").write_text(note)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
