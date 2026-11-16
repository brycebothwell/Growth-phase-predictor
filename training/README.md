# Berkeley + Harpenden training and evaluation — v2 research beta

16 November 2026. **Decision: do not replace the default v1 calculator.** The first fitted model did not improve on v1 on the same held-out three-height cases. It also failed to achieve its intended simultaneous uncertainty coverage. It is available as a separate research beta, not a clinical predictor.

This report supersedes “training not yet completed” statements for the **v2 beta only**. The default v1 remains the literature-informed, untrained calculator. This project is separate from the OHSU master's thesis and does not predict mandibular growth.

## Sources and harmonization

- **Berkeley:** corrected `berkeley` data in SITAR, package DESCRIPTION version 1.5.0 when retrieved. 136 children (66 boys, 70 girls), 4,884 rows. ID, sex, decimal age in years and height in cm. Source: https://raw.githubusercontent.com/cran/sitar/master/data/berkeley.rda ; documentation: https://search.r-project.org/CRAN/refmans/sitar/html/berkeley.html . This is not the smaller 93-child variant. Tuddenham RD, Snyder MM (1954), *Physical growth of California boys and girls from birth to eighteen years*. SITAR is distributed under GPL (>=2); retain source attribution and consult source terms for reuse.
- **Harpenden:** UK Data Service study 9330, first edition, TAB archive retrieved 16 November 2026. 701 children (419 boys, 282 girls). Sex coding 1=boy, 2=girl; age in decimal years; `ht` in cm, verified against the supplied data dictionary. The actual downloaded TAB has **8,098 rows**, whereas the catalogue/guide says 8,188. The analysis uses actual file contents; this discrepancy is recorded rather than silently assuming agreement. Johnson W (2024), *Harpenden Growth Study, 1949–1969*, Tanner JM, SN 9330, DOI 10.5255/UKDA-SN-9330-1. Open download, CC BY-SA 4.0. https://datacatalogue.ukdataservice.ac.uk/studies/study/9330 . No Tanner or skeletal-age fields were used as predictors.
- Dataset identity is retained with each child, and cohort + original ID are combined to prevent collisions. Numerical row ages/heights were harmonized without fabricating missing visits. SHA-256 hashes are recorded in [report.json](report.json). Raw data and individual reference/prediction tables are not committed; scripts regenerate them locally.

## Reference outcome and exclusions

The target is age at the maximum derivative of a cubic smoothing spline fitted to a child's sufficiently complete trajectory. It is an estimated retrospective reference, not perfectly observed biological PHV.

Within ages 7–19, split histories at gaps >1.1 years. An eligible segment needs at least 8 heights over >=4 years; begins by age 11.5 for boys / 10.5 for girls and ends by or after 15.5 / 14 respectively. Reject non-increasing ages and implausible interval velocities outside -1 to 18 cm/year. Fit splines with residual-SD settings 0.2, 0.3 and 0.5 cm; use 0.3 cm for the primary reference. Search in the interior; require a peak >=1 year from segment ends, final interior velocity <=3.5 cm/year and peak velocity >=6 cm/year for boys / >=5 for girls. Require reference peak ages across smoothing settings to span <=0.75 years. These are explicit research eligibility choices, not clinical definitions of normal growth. They select complete, stable trajectories and may exclude late/atypical maturers.

| Cohort | Included | Coverage failure | Unbracketed peak | Unstable peak | Implausible velocity |
|---|---:|---:|---:|---:|---:|
| Berkeley | 101 | 0 | 8 | 27 | 0 |
| Harpenden | 71 | 587 | 27 | 12 | 4 |

Only **172 of 837** source participants qualified. The two cohorts were not treated as a pooled collection of interchangeable visits. Coverage and cohort differences substantially limit representativeness.

## Training, tuning and calibration

Separate male/female random-forest regression models predict PHV age. Nine features describe the *visible* heights: latest age and height, overall velocity, latest and previous interval velocities, their change, total observation span, number of heights and residual SD around a fitted height line. No reference PHV, later height, Tanner stage or cephalogram is passed as an inference feature.

Input windows contain 3–7 actual measurements at ages 8–17, with intervals 0.2–1.1 years and total span 0.5–3.01 years. Adjacent and alternate visits provide irregular and different-length windows. Windows are chosen by observed age/spacing, not by reference peak. Complete trajectories are used only to construct offline reference outcomes.

Fixed seed 20261116; deterministic roughly 60/20/20 split stratified by cohort and sex. All windows of a child stay in one group. Parameter selection uses four-fold GroupKFold **inside training children only**, testing depth 3/5/7 and leaf-size 10/20; 100 trees, selected depth 7 and leaf size 10 for both sexes. Each child's windows sum to weight one. Random-forest row bootstrapping still means this is a conventional weighted forest, not a full longitudinal generative model.

| Sex / cohort | Training | Calibration | Test |
|---|---:|---:|---:|
| Boys / Berkeley | 33 | 11 | 12 |
| Boys / Harpenden | 26 | 8 | 10 |
| Girls / Berkeley | 27 | 9 | 9 |
| Girls / Harpenden | 16 | 5 | 6 |
| **Total** | **102** | **33** | **37** |

Test children were excluded from coefficient fitting and hyperparameter selection. However, Berkeley had been explored in the earlier v1 audit, so this is not a claim of pristine confirmatory external validation. Both cohorts have now been used in development. Subsequent changes require a new evaluation design or new cohort.

## Three-height results on held-out participants

Each child's mean is weighted equally, irrespective of number of windows. Window counts are not independent sample sizes. MAE confidence intervals use 2,000 bootstrap samples of children. Phase is pre/near/post with a prespecified ±0.5-year near window.

| Sex | Children / windows | MAE months | RMSE months | Bias months | Within 3 mo | Within 6 mo | Within 12 mo | Phase accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Boys | 22 / 690 | 9.1 | 13.4 | -2.4 | 32.0% | 51.5% | 76.6% | 83.9% |
| Girls | 15 / 448 | 9.1 | 12.5 | +0.6 | 24.7% | 45.7% | 76.8% | 85.8% |

Overall phase accuracy includes many clearly pre/post-peak windows and must not be interpreted as near-peak sensitivity or probability calibration. The interface therefore labels phase as a point estimate and reports indeterminate phase when the timing range spans multiple phases. No calibrated phase probabilities are emitted.

**Boys:** bootstrap 95% MAE interval 6.3–12.9 months. Near-PHV sensitivity 64.4%; near-PHV specificity 91.0%.

Raw window-count confusion matrix (rows reference, columns predicted; repeated windows are correlated):

| Reference / predicted | Pre | Near | Post |
|---|---:|---:|---:|
| Pre | 316 | 23 | 22 |
| Near | 11 | 67 | 27 |
| Post | 0 | 28 | 196 |

**Girls:** bootstrap 95% MAE interval 6.0–12.6 months. Near-PHV sensitivity 47.0%; near-PHV specificity 92.6%.

Raw window-count confusion matrix (rows reference, columns predicted; repeated windows are correlated):

| Reference / predicted | Pre | Near | Post |
|---|---:|---:|---:|
| Pre | 62 | 12 | 1 |
| Near | 8 | 30 | 24 |
| Post | 0 | 16 | 295 |

Full subject-weighted confusion matrices, sensitivities/specificities, prospective-only performance, cohort, maturation, age, spacing and span results are in [extended-metrics.json](extended-metrics.json). Fixed descriptive maturation cutoffs are center 13.5 years for boys / 11.5 for girls ±1 year; these are not clinical classifications. Some cells have few children and cannot support generalization.

## Direct comparison with the previous calculator

Both models used exactly the same 1,138 three-height windows from the same 37 test children and the same spline reference. No tuning occurred after this comparison.

| Sex | Existing v1 MAE | Trained v2 MAE | v2 minus v1 | Paired child-bootstrap 95% interval |
|---|---:|---:|---:|---:|
| Boys | 8.61 mo | 9.12 mo | +0.50 mo | -1.17 to +2.93 mo |
| Girls | 8.92 mo | 9.06 mo | +0.14 mo | -2.34 to +3.07 mo |

The trained model was numerically worse; both paired intervals include zero. **There is no demonstrated improvement**, let alone a statistically supported improvement, over v1. It did improve over the simpler training-sex-mean baseline (~12 months MAE), but that is not the appropriate product replacement criterion.

The previous 125-child Berkeley benchmark used fixed age windows and the midpoint of the largest observed interval velocity. Its 6.1–7.6 / 9.8–13.5 month errors are not directly comparable with this spline-target study. That earlier executable benchmark remains in `validation/benchmark.py`. Its highest-interval approach is historical exploratory evidence, not the primary v2 target.

## Cross-cohort transport experiments

For each direction, tune on source-cohort children only using grouped CV, fit all eligible source children, and evaluate three-point windows in the other cohort. These are separate research experiments, not the pooled beta's final test. No person occurs in both cohorts, and no destination outcome is used for that direction's fitting/tuning. These cohorts are already known from development, so a new untouched cohort is still needed for final confirmation.

| Sex | Train → evaluate | Source / destination children | MAE months | Bias months |
|---|---|---:|---:|---:|
| Boys | Berkeley → Harpenden | 56 / 44 | 8.2 | -0.7 |
| Boys | Harpenden → Berkeley | 44 / 56 | 8.2 | +2.7 |
| Girls | Berkeley → Harpenden | 45 / 27 | 10.1 | -8.6 |
| Girls | Harpenden → Berkeley | 27 / 45 | 8.6 | +6.2 |

Female transfer bias differs materially by direction, showing that pooling more historical measurements is not a substitute for population validation. [Full cross-cohort results](cross-cohort-results.json).

## Additional heights and uncertainty

Matched comparisons pair the same child and index date at 3 versus 4/5/6/7 heights. Every paired bootstrap interval for change in MAE includes zero. The first model therefore **does not demonstrate a reliable benefit from extra heights**. The analysis still allows differences in observation spacing and history length; it is not a randomized measurement experiment.

Calibration used each child's maximum absolute error over all eligible windows, then a finite-sample upper quantile targeting 90% simultaneous coverage. Radii were ±24.6 months for boys (19 calibration children) and ±26.9 months for girls (14). Observed simultaneous coverage across all windows was only **77.3% of test boys and 73.3% of test girls**. Three-point per-window, subject-weighted coverage was 91.6% and 94.8%, respectively; that easier metric must not conceal failure of the simultaneous target. Intervals are broad and not validated for modern clinical use. The beta discloses both the intended target and its observed failure.

## Technical checks and reproducibility

Python-to-JavaScript inference matched exactly on 141 sampled held-out cases, including float32 feature conversion for tree traversal. Duplicate ages, insufficient spacing, unsupported ages and the seven-point selection limit were tested. JavaScript syntax and UI element references were checked. The environment blocked local Chromium startup. Subsequent live cloud-browser testing succeeded after publication: the trained beta loaded its model, produced the example result, recalculated after changing sex, hid stale output on input changes, and rejected an incomplete added observation. The original default calculator was also exercised successfully and the beta link verified. Mobile viewport rendering was not separately verified.

```
python -m pip install numpy pandas scipy scikit-learn rdata
python training/train.py --download
node training/test-engine.cjs
node training/comparison.cjs
python training/evaluate.py
python training/cross-cohort.py
```

To use already downloaded files, omit `--download`. `train.py` regenerates model JSON, report, local split/reference manifest, held-out predictions and parity fixtures. `comparison.cjs` evaluates the archived exact v1 functions on the same three-point inputs. Extended metrics and cross-cohort scripts do not retune the published beta. Seed and source file hashes are in `report.json`; preserve hashes or source archives to reproduce exactly if upstream packages change. Raw source files, personal-level research outputs and generated test fixtures are ignored by Git. No patient input is uploaded by the website.

## Remaining work and limits

The random forest is a first regularized machine-learning baseline, not SITAR or a longitudinal mixed-effects growth model. No claim is made that all appropriate model families have been exhausted. Future work should compare defensible longitudinal/hierarchical approaches, examine retrospective peak labeling and selected-sample bias, handle measurement error, and obtain new participants for final evaluation. Avoid repeated tuning to this now-observed test set. Historical cohort composition, exclusion of incomplete/unstable trajectories, small subgroups and imperfect reference peaks limit all findings.

A future height trajectory and calibrated phase probabilities remain unimplemented in the beta. Its graphs show measured history and observed velocities. Statural PHV does not determine mandibular peak timing, suture maturation or treatment success. No cephalometric module is included.

## Attribution

Harpenden data: Johnson W (2024), Tanner JM, UK Data Service SN 9330, DOI 10.5255/UKDA-SN-9330-1; CC BY-SA 4.0. Changes: harmonized stature columns, quality selection, spline-derived research outcomes and aggregate fitted model. Berkeley: Tuddenham and Snyder (1954), corrected data distributed by SITAR (Cole), version 1.5.0 at retrieval. Original data are not bundled. Preserve these attributions with downstream model/report reuse. The generated model and this report are shared under CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/ . Source-data and software-package terms remain applicable to their respective materials.
