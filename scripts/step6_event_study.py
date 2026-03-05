#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA).dropna(subset=["wage_growth_yoy", "ai_exposure_mean", "major_group", "year"]).copy()
    event = df["year"] - 2022
    window = list(range(-6, 4))
    ref = -1
    terms = [k for k in window if k != ref]

    groups = sorted(df["major_group"].unique())
    years = sorted(df["year"].unique())

    Xcols = [np.ones(len(df))]
    names = ["const"]
    for k in terms:
        Xcols.append(((event == k).astype(float) * df["ai_exposure_mean"]).to_numpy())
        names.append(f"event_{k}")
    for g in groups[1:]:
        Xcols.append((df["major_group"] == g).astype(float).to_numpy())
        names.append(f"g_{g}")
    for y in years[1:]:
        Xcols.append((df["year"] == y).astype(float).to_numpy())
        names.append(f"year_{y}")

    X = np.column_stack(Xcols)
    b, se, n = ols_hc1(X, df["wage_growth_yoy"].to_numpy(float))
    res = pd.DataFrame({"term": names, "coef": b, "se": se})
    ev = res[res["term"].str.startswith("event_")].copy()
    ev["event_time"] = ev["term"].str.replace("event_", "", regex=False).astype(int)
    ev["ci95_low"] = ev["coef"] - 1.96 * ev["se"]
    ev["ci95_high"] = ev["coef"] + 1.96 * ev["se"]

    ref_row = pd.DataFrame([{"term": "reference", "coef": 0.0, "se": np.nan, "event_time": ref, "ci95_low": np.nan, "ci95_high": np.nan}])
    ev = pd.concat([ev, ref_row], ignore_index=True).sort_values("event_time")
    ev.to_csv(OUT / "day6_event_study_coefficients.csv", index=False)

    p = ev[ev["term"] != "reference"]
    plt.figure(figsize=(8, 5))
    plt.errorbar(p["event_time"], p["coef"], yerr=1.96 * p["se"], fmt="o", capsize=2)
    plt.axhline(0, color="black", linestyle="--", linewidth=1)
    plt.axvline(0, color="red", linestyle="--", linewidth=1)
    plt.title("Step 6 Event Study: Exposure-Scaled Effects")
    plt.xlabel("Event time (year relative to 2022)")
    plt.ylabel("Coefficient")
    plt.tight_layout()
    plt.savefig(OUT / "day6_event_study_plot.png", dpi=150)
    plt.close()

    summary = {"n_obs": int(n), "event_window": [min(window), max(window)], "reference": ref}
    (OUT / "day6_event_study_summary.json").write_text(json.dumps(summary, indent=2))
    (DOCS / "DAY6_event_study_note.md").write_text(
        "# Step 6 — Event-Study Note\n\n"
        "Estimated exposure-scaled event-time coefficients relative to reference year -1 (2021).\n"
        "See `outputs/day6_event_study_coefficients.csv` and `outputs/day6_event_study_plot.png`.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
