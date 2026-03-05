#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_analysis" / "panel_annual_majorgroup.csv"
OUT = ROOT / "outputs"
DOCS = ROOT / "docs"


def ols_hc1(X, y):
    m = np.isfinite(y) & np.isfinite(X).all(axis=1)
    X, y = X[m], y[m]
    n, k = X.shape
    inv = np.linalg.pinv(X.T @ X, rcond=1e-10)
    b = inv @ (X.T @ y)
    e = y - X @ b
    cov = (n / max(n - k, 1)) * (inv @ (X.T @ (X * (e[:, None] ** 2))) @ inv)
    se = np.sqrt(np.clip(np.diag(cov), 0, np.inf))
    return b, se, n


def fit(df, post_year, y_col="wage_growth_yoy"):
    groups = sorted(df["major_group"].unique())
    years = sorted(df["year"].unique())
    post = (df["year"] >= post_year).astype(float)
    xint = df["ai_exposure_mean"].to_numpy(float) * post.to_numpy(float)
    X = np.column_stack([
        np.ones(len(df)),
        xint,
        *[(df["major_group"] == g).astype(float).to_numpy() for g in groups[1:]],
        *[(df["year"] == y).astype(float).to_numpy() for y in years[1:]],
    ])
    y = df[y_col].to_numpy(float)
    b, se, n = ols_hc1(X, y)
    return {"post_year": post_year, "coef": float(b[1]), "se": float(se[1]), "t": float(b[1]/se[1]), "n_obs": int(n)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA).dropna(subset=["wage_growth_yoy", "ai_exposure_mean", "major_group", "year"]).copy()
    rows = []
    for y in [2018, 2020, 2022]:
        r = fit(df, y)
        r["spec"] = f"post_{y}"
        rows.append(r)

    # winsorized outcome robustness
    q1, q99 = df["wage_growth_yoy"].quantile([0.01, 0.99])
    df["wage_growth_yoy_w"] = df["wage_growth_yoy"].clip(lower=q1, upper=q99)
    rw = fit(df, 2022, y_col="wage_growth_yoy_w")
    rw["spec"] = "post_2022_winsorized"
    rows.append(rw)

    out = pd.DataFrame(rows)
    out.to_csv(OUT / "day5_robustness_results.csv", index=False)

    summary = {
        "n_specs": int(len(out)),
        "main_spec_coef": float(out.loc[out["spec"]=="post_2022", "coef"].iloc[0]),
        "main_spec_se": float(out.loc[out["spec"]=="post_2022", "se"].iloc[0]),
    }
    (OUT / "day5_robustness_summary.json").write_text(json.dumps(summary, indent=2))

    (DOCS / "DAY5_robustness_note.md").write_text(
        "# Day 5 — Robustness Note\n\n"
        "Ran threshold-placebo and winsorized-outcome robustness checks for the intensity TWFE design.\n"
        "See `outputs/day5_robustness_results.csv`.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
