# U.S. AI Job Exposure and Wage Growth

## Title & Abstract
This paper asks whether occupations that appear more exposed to artificial intelligence experienced meaningfully different wage-growth patterns in the United States after the recent acceleration of AI investment and adoption. Using a small occupation-level panel that combines a public AI exposure measure with annual wage data, the analysis estimates a two-way fixed-effects difference-in-differences style intensity design, then checks whether the pattern survives simple robustness tests and event-study inspection. The headline result is cautious rather than dramatic: more AI-exposed occupation groups do not show a large, cleanly identified post-2022 wage-growth break in this setting, which suggests that broad occupational exposure measures are useful as a screening tool but not yet strong enough on their own to settle the causal question.

## Introduction
The core causal question is straightforward: did higher AI exposure lead to different wage-growth outcomes across broad U.S. occupation groups once the economy moved into the post-2022 AI period? The outcome variable is year-over-year wage growth. The treatment variable is an occupation group's AI exposure intensity interacted with an indicator for the post-2022 period.

This question matters because the public debate around AI and labor markets is often framed in absolutes. One side expects a major productivity boom; the other expects rapid displacement and wage pressure. For workers, firms, and policymakers, the real issue is less rhetorical: are occupations that look more exposed to AI already diverging in pay dynamics, and if so, by how much? A careful reduced-form answer helps separate signal from narrative.

## Data & Institutional Context
The data combine a public occupation-level AI exposure measure from the AIOE appendix with annual wage series from FRED. The analysis maps these inputs into five major U.S. occupation groups and follows them over time in an annual panel running from 2000 through 2025. In practical terms, this is a deliberately transparent public-data design: the exposure measure provides a stable ranking of which broad occupation groups should be more or less exposed to AI-type task substitution or augmentation, while the wage panel provides a long-run view of compensation trends.

Institutionally, the setting is the early commercialization period of modern generative AI layered on top of a much longer process of automation, digitization, and occupational restructuring. That matters for interpretation. This is not a clean experiment in which one occupation suddenly adopts a single technology while another does not. It is a broad observational setting in which AI exposure is better understood as a structured measure of vulnerability or complementarity, rather than a literal switch that turns treatment on and off.

## Empirical Strategy
The empirical strategy is a two-way fixed-effects intensity design, which can be read as a plain-English difference-in-differences framework where treatment varies in degree rather than in a simple yes/no form. The model compares wage-growth changes before and after 2022 across occupation groups with different levels of AI exposure, while absorbing common year shocks and time-invariant group differences through fixed effects.

The design relies on a familiar identifying idea: absent the post-2022 AI shock, more- and less-exposed occupation groups would have continued on sufficiently similar wage-growth paths once common macro conditions and stable group characteristics are accounted for. That assumption is necessarily strong in a five-group aggregate panel. It means the estimates should be interpreted as disciplined reduced-form evidence, not as a definitive structural measure of AI adoption's causal effect on wages.

## Main Findings
The baseline coefficient on the post-2022 AI exposure interaction is approximately **-0.0013**, with a robust standard error of about **0.0028** and a 95 percent confidence interval spanning roughly **-0.0068 to 0.0043**. In plain English, the central estimate leans slightly negative, but it is small and statistically imprecise. The evidence does not support a large, clean post-2022 wage-growth divergence between more- and less-AI-exposed broad occupation groups in this sample.

For an ordinary reader, the practical meaning is that the data do not yet justify a strong claim that AI exposure has already produced a dramatic wage penalty or wage premium across these major occupational categories. If AI is affecting wages, the effect may be too small, too early, too heterogeneous, or too poorly measured at this level of aggregation to show up cleanly here.

The descriptive diagnostics point in the same cautious direction. By the latest year in the panel, the cross-sectional correlation between exposure and cumulative wage growth is positive but moderate, around **0.44**, which suggests some visible relationship in the raw data. But once the model asks the harder causal question—whether more-exposed groups break away after 2022 in a way consistent with the treatment story—that pattern does not become persuasive. The event-study figures reinforce that interpretation: the coefficients do not show a sharp discontinuity or a dramatic post-event departure.

## Robustness & Limitations
The robustness exercises do not overturn the basic story. Alternative threshold choices and winsorized outcome checks preserve the broad conclusion that the effect is modest and uncertain rather than large and decisive. In that sense, the negative result is itself informative: it survives enough specification movement to suggest that caution is the right stance.

At the same time, the design has real limits. The panel is small, with only five broad occupation groups and 125 observations. The treatment is an exposure measure rather than a direct adoption measure. The post-2022 period is short relative to the scale of labor-market adjustment. And broad occupation groups can hide offsetting within-group dynamics, where some workers are complemented by AI while others are displaced. These limits mean the paper is better read as a reproducible first-pass empirical screen than as the final word on AI and wages.

## Conclusion
The practical takeaway is not that AI has no labor-market consequences. It is that, in this public-data occupation-level framework, the wage effects are not yet large or clean enough to support sweeping claims. For researchers, that points to the need for sharper treatment measurement and richer microdata. For decision-makers, it suggests resisting both hype and panic: the current evidence is more consistent with gradual, uneven adjustment than with an immediate labor-market break.

## Appendix
### Repro steps
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_step2_step3.py
python scripts/run_step4_step7.py
```

### Evidence links
- Repo: https://github.com/RyanPiao/tech-econ-us-ai-jobs-exposure-wage-growth
- Step 4 baseline note: `docs/STEP4_baseline_twfe_note.md`
- Step 5 robustness note: `docs/STEP5_robustness_note.md`
- Step 6 event-study note: `docs/STEP6_event_study_note.md`
- Baseline results: `outputs/step4_twfe_baseline_results.csv`
- Robustness results: `outputs/step5_robustness_results.csv`
- Event-study coefficients: `outputs/step6_event_study_coefficients.csv`
- Event-study figure: `outputs/step6_event_study_plot.png`

### Citations
- Felten, Edward, Manav Raj, and Robert Seamans. AIOE Appendix / occupation-level AI exposure data.
- Federal Reserve Economic Data (FRED), annual occupation earnings series used in the panel.
