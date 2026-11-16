# PHV calculator — consolidated project context

Updated 16 November 2026. This is a decision and history summary recovered from the earlier growth-calculator conversation and checked against the repository. It is **not a verbatim import or merger of chat transcripts**. Use this file and ROADMAP.md as the durable handoff for future work. The user supplied a complete 17-section project handoff in this conversation during the 16 November run; it is the requirements/history reference. Statements in that handoff saying training was not yet complete describe the earlier/default v1 state, not the subsequently trained separate v2 beta.

## Current goal and scope

- Build a height-only calculator for statural peak height velocity (PHV): where the child is relative to the growth peak, estimated peak timing, and honest uncertainty.
- Start from date of birth, sex and at least three dated standing heights in centimeters. Support more observations where the model has evidence for them; do not promise that adding points necessarily improves accuracy.
- Cephalometric inputs and mandibular-growth forecasts were explicitly removed on 16 November 2026. Earlier requests for optional cephalograms, remaining mandibular growth and final mandibular dimensions are superseded and outside current scope.
- Keep this calculator separate from the orthodontic master's thesis. Correlations in the thesis do not validate this predictive tool.
- Keep the default height-only calculator available while developing a genuinely trained model. Do not label illustrative curve weights as clinical probabilities.

## Recovered decisions and verified history

| Period | Decision or implementation | Verified status |
|---|---|---|
| 2 November 2026 | Publish an interactive growth-phase prototype on GitHub Pages | Implemented; hand-specified candidate curves, not cohort-trained |
| Early November 2026 | Separate thesis and calculator projects; keep a prominent roadmap and real-data acquisition instructions | Implemented in repository documentation |
| 9 November 2026 | Investigate Oregon Growth Study stature records | Individual records were not acquired. Only a published male age-at-PHV summary was used as a weak prior |
| 9 November 2026 | Begin future training with accessible Berkeley trajectories; later consider Harpenden, ALSPAC and Oregon external validation | Planned then; no Berkeley training occurred in v1 |
| 9 November 2026 | Permit optional cephalograms and additional heights; eventually explore mandibular forecasts | Ceph descriptive panel was implemented, predictive mandibular model was not. This scope is now superseded |
| 16 November 2026 | Restore height-only version and audit actual training provenance | Completed; live interface reverted and no prior cohort training was found |
| 16 November 2026 | Test three-height v1 estimates using Berkeley children | Exploratory benchmark completed, with substantial errors and female timing bias; see validation/README.md |
| 16 November 2026 | Train a height-only model using Berkeley and Harpenden | v2 research beta trained with participant-separated development, calibration and testing; see training/README.md |

## Current artifacts

- Default calculator: https://brycebothwell.github.io/Growth-phase-predictor/
- Trained beta: https://brycebothwell.github.io/Growth-phase-predictor/trained.html
- Current plan: [ROADMAP.md](ROADMAP.md)
- Model report: [training/README.md](training/README.md)
- Reproducible pipeline: [training/train.py](training/train.py)
- Earlier v1 audit and exploratory test: [validation/README.md](validation/README.md)
- Preserved earlier roadmap: [archive/ROADMAP-pre-v2.md](archive/ROADMAP-pre-v2.md)

## Scientific guardrails retained from earlier work

Split by child, never by row; never expose future heights to the predictor. Keep training, tuning, calibration and evaluation distinct. Evaluate timing error, bias, phase discrimination, interval coverage, early/late maturers and uncertainty with three versus additional measurements. Prefer real longitudinal trajectories to cross-sectional reference centiles for individual PHV validation. Three heights supply only two interval velocities and cannot uniquely establish a biological peak.

The v2 report has a different reference outcome and test population from the first Berkeley benchmark, so the raw error tables cannot be compared directly. A same-case comparison was therefore run. It found no improvement over v1, so the beta does not replace the default calculator.

## Chat organization request

The user requested this conversation be named **phv calculator**, pinned, and used as the home for this project. The available tools cannot rename/pin this conversation or move complete transcripts. The recovered decisions and roadmap have instead been consolidated here, with a summary supplied in the current conversation. No claim that the chat itself was renamed, pinned or merged is made.

## Requirements carried forward from the supplied handoff

The intended outputs include height trajectory, observed interval velocities, latest velocity, acceleration/deceleration, experimental PHV age and time offset, phase classification, calibrated phase probabilities only when justified, uncertainty and CSV export. The existing default interface is preserved. The beta displays observed graphs, not an invented future-height curve; calibrated phase probabilities remain unimplemented.

The acceptance question is whether a genuinely trained model improves three-height prediction over the existing literature-informed calculator, with participant-level separation and transparent evidence. Required evaluation includes MAE, RMSE, signed bias, errors within 3/6/12 months, phase confusion matrices/sensitivity/specificity, uncertainty coverage, early/middle/late maturers, index age, observation count/spacing/span, both cohorts, and both cross-cohort directions. Reports distinguish completed analyses from pending probability calibration and prospective validation.

Additional potential resources named in the handoff are ALSPAC, NHLBI Growth and Health Study, Fels, and Oregon stature records. Access and usability have not been established in this run. Historical craniofacial issue discussions (#2 and #3) remain outside active scope.

For future work, read the current GitHub README, ROADMAP and index.html before edits; also read trained.html, phv-engine.js and training/README.md for the beta. Repository source is authoritative for implemented behavior. Do not replace the default engine until a prespecified evaluation supports an actual improvement.
