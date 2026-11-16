# Training audit and three-height benchmark — 16 November 2026

## What the deployed calculator was trained on

It was **not trained on Berkeley, Oregon individual trajectories, or another longitudinal cohort**. All 20 original repository commits through `1472d6f` were inspected, including the initial predictor (`2b417d3`) and the prior change (`8b5dc77`). The initial model specified candidate curves and age priors manually. The Oregon change replaced the male age prior with a published mean of 13.54 years and SD 1.12 years from 51 boys; that is aggregate prior information, not model training. The female center remains 12 years with a 1.5-year prior SD. The roadmap explicitly identifies Berkeley training as future work. No learned cohort coefficients or training pipeline occur in this history.

The predictor fits/weights candidate curves against the heights entered for one person. This individual curve fitting must not be confused with training a predictive model on longitudinal cohort records. The displayed PHV-age estimate is the weighted median of the curve parameter `k`; `k` is not exactly the maximum of the complete velocity function because the function also has a declining logistic factor. The present benchmark evaluates the displayed output as implemented, without repairing or tuning it.

## Height-only restoration

`index.html` was restored to its state immediately before cephalometric inputs were added. Commit: `db43c7d`. The prediction functions are byte-identical to those before this restoration. The live GitHub Pages HTML was fetched and matched the restored page; the ceph panel is absent. The Oregon reference and 3+ height workflow remain.

## First independent benchmark

Source: the corrected `berkeley` dataset from CRAN's SITAR package (4,884 rows, 136 children). Downloaded 16 November 2026 from https://raw.githubusercontent.com/cran/sitar/master/data/berkeley.rda . Documentation: https://search.r-project.org/CRAN/refmans/sitar/html/berkeley.html . Original source: Tuddenham RD, Snyder MM (1954), Physical growth of California boys and girls from birth to eighteen years.

125 eligible children (63 boys, 62 girls), each evaluated at three prespecified age windows: 375 predictions, **not 375 independent participants**. Each prediction used exactly three actual measurements spaced six months apart. No later heights were passed to the predictor. No training or tuning occurred. This is independent of the deployed model's Oregon prior, but now that these results have been examined, Berkeley should not be represented as an untouched final test set for subsequent development.

Reference outcome: midpoint of the highest observed height-velocity interval over ages 8–18; tied maximum interval midpoints were averaged. Participants required at least 16 available heights, coverage from no later than 8.5 to at least 17 years, no gaps exceeding one year, plausible interval velocities (-0.5 to 18 cm/year), and an interior maximum. This is a sampled-interval PHV proxy, **not exact biological PHV**. Six-month averaging, occasional longer gaps, measurement noise and ties limit reference precision. Full-trajectory spline sensitivity was explored but not used as ground truth because boundary peaks can be unstable.

| Sex | Input ages (years) | N | Mean absolute timing error (months) | Within ±6 months | Within ±12 months | Mean signed error (months) |
|---|---|---:|---:|---:|---:|---:|
| Boys | 11, 11.5, 12 | 63 | 7.6 | 47.6% | 85.7% | +2.0 |
| Boys | 12, 12.5, 13 | 63 | 6.1 | 57.1% | 93.7% | +2.7 |
| Boys | 13, 13.5, 14 | 63 | 6.4 | 69.8% | 90.5% | -2.3 |
| Girls | 9, 9.5, 10 | 62 | 13.5 | 16.1% | 51.6% | +11.0 |
| Girls | 10, 10.5, 11 | 62 | 12.2 | 21.0% | 58.1% | +11.1 |
| Girls | 11, 11.5, 12 | 62 | 9.8 | 48.4% | 79.0% | +8.1 |

Positive signed error means predicted peak later than the reference. For comparison, predicting the fixed prior center for every child yields MAE 11.6 months in boys and 12.1 months in girls. Thus early girls' estimates do not improve meaningfully on the fixed prior baseline.

Some children had already passed the reference peak by the final input age. The full table mixes forecasting and retrospective identification. Restricting to children whose last input was before the reference peak gives, respectively: boys N=61/47/29 and MAE=7.7/5.8/10.6 months; girls N=56/44/19 and MAE=11.6/8.7/6.3 months. These subgroups differ, so they do not prove that later measurements improve forecasts in the same children.

## Interpretation and next independent cohort

The unchanged tool is an untrained prototype with measurable timing errors, particularly a later-than-observed bias in girls. This exploratory historical-cohort benchmark does not establish clinical reliability or calibrated probabilities. Eligibility selects more complete histories; historical Berkeley children are not representative of contemporary clinical populations. No sex-specific confidence intervals or probability calibration have been established.

Harpenden provides another accessible cohort: UK Data Service study 9330, openly downloadable without registration, CC BY-SA 4.0. Its catalogue describes 701 children and 8,188 observations. Not all will have adequate pubertal follow-up. https://datacatalogue.ukdataservice.ac.uk/studies/study/9330 . Harpenden was identified but **not downloaded or tested in this run**. Reserve it for external validation after a real Berkeley training/development pipeline is established, and check overlap with any reference data used during development.

## Reproduce

Install Python packages pandas, numpy and rdata, plus Node.js. From this checkout run `python validation/benchmark.py`. It downloads the public data, extracts the actual predictor functions from `index.html`, runs all cases in Node.js, and writes `validation/results.csv`. No participant-level data are committed in this report. For the audited predictor use restored commit `db43c7d` (README-only update `f79d4f9` has the same predictor).
