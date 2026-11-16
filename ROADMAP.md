# PHV calculator — active roadmap

Updated 16 November 2026. Scope: standing height and statural PHV only. Start with [the consolidated project record](PROJECT_CONTEXT.md). The [earlier roadmap](archive/ROADMAP-pre-v2.md) is preserved for history; its cephalometric and mandibular proposals are superseded.

## Completed

- [x] Separate calculator work from the master's thesis.
- [x] Restore the height-only default calculator and retain support for 3+ measurements.
- [x] Audit v1 provenance: no prior Berkeley training; only hand-specified curves and an Oregon aggregate male prior.
- [x] Run an exploratory three-height Berkeley benchmark of v1.
- [x] Acquire corrected Berkeley and open Harpenden participant-level stature data.
- [x] Check sex coding, units, longitudinal coverage, implausible intervals, peak bracketing and smoothing sensitivity.
- [x] Train separate sex-specific v2 models on both cohorts, with child-level separation for tuning/calibration/testing.
- [x] Evaluate three-point and additional-point predictions, forecasts before peak, cohort differences, baseline comparisons and uncertainty coverage.
- [x] Run a direct same-case comparison with the existing v1 predictor.
- [x] Implement browser inference matching Python predictions; expose the model as a clearly labeled research beta.
- [x] Consolidate recovered project decisions, source provenance, current limitations and roadmap.

## Current decision: keep v2 as beta

The first trained model has not improved on v1 on the same held-out three-point cases, and the nominal 90% simultaneous calibration target was missed. Training alone is not evidence of improved accuracy. Preserve the height-only v1 default and make v2 available for transparent research review. Do not deploy an accuracy claim, clinical recommendation or calibrated phase probability.

## Next model-development milestone

1. Freeze this evaluation as a development result; do not repeatedly tune against its test children and continue calling that an untouched test.
2. Compare a longitudinal growth-curve model (for example sex-specific SITAR or another justified nonlinear mixed-effects approach) with the current supervised timing model. Consider remaining time to peak, minimum useful observation span, measurement error and early/late maturation explicitly.
3. Improve reference-peak ascertainment with prespecified full-trajectory fits and sensitivity analysis. Review exclusions, especially incomplete Harpenden histories and unstable peaks. Avoid inventing absent measurements or using reference outcomes to select the predictor's input window.
4. Use nested participant-level evaluation for new development; reserve a new cohort or untouched prospective sample for final evaluation. Both Berkeley and Harpenden have now been inspected and used in development.
5. Evaluate additional measurements on matched children and matched index dates. The current 3 versus 4+ comparison does not establish a causal benefit of more points.
6. Recalibrate uncertainty on fresh participants; test both per-prediction and simultaneous-per-child coverage. Assess whether abstention is needed with very uncertain inputs.
7. Test clinically realistic measurement noise and irregular timing; stratify by sex, cohort, input ages and maturation timing. Audit representativeness for modern patients.
8. Replace the default only if a prespecified evaluation supports improvement and the interface communicates remaining uncertainty accurately.

## Later data expansion

- ALSPAC or another modern, appropriately authorized longitudinal cohort could help with contemporary validation. Access has not been obtained.
- Oregon person-level stature records remain an acquisition task. The existing summary histogram is not individual training data.
- No cephalometric or mandibular module is part of this active plan.

## User inputs currently supported by the trained beta

Age 8–17, dated heights in cm, at least 3 observations; latest up to 7 observations within 3 years; intervals approximately 2.4–13.2 months; minimum total span 6 months. These bounds reflect this first training setup, not biological rules. The beta reports when older points are excluded. All entered data are processed locally in the browser.
