# PHV Calculator / Growth Phase Predictor

**Height-only research software. No clinical validity claim.**

- [Open the existing height-only calculator](https://brycebothwell.github.io/Growth-phase-predictor/)
- [Try the Berkeley + Harpenden trained beta](https://brycebothwell.github.io/Growth-phase-predictor/trained.html)
- [Read the current roadmap](ROADMAP.md)
- [Read the consolidated project history and requirements](PROJECT_CONTEXT.md)
- [Read actual training and test results](training/README.md)

## Current decision — 16 November 2026

The first model trained on both Berkeley and Harpenden is complete, but it **did not improve on the existing calculator on the same held-out three-point cases**. Its nominal 90% simultaneous uncertainty target was also missed. The current height-only calculator therefore remains the default; the trained model is a separate research beta.

| Same held-out test | Existing v1 MAE | Trained v2 MAE | Test children |
|---|---:|---:|---:|
| Boys, three heights | 8.6 months | 9.1 months | 22 |
| Girls, three heights | 8.9 months | 9.1 months | 15 |

The reference is a peak from a smoothed complete trajectory, not perfect biological ground truth. These figures use different participants, input windows and reference criteria from the first exploratory Berkeley report; compare models only within the same protocol. This project is separate from the OHSU master's thesis.

## What is and is not trained

**Default v1:** manually specified candidate curves fitted to the entered measurements. Its male PHV-age prior uses Grau's published Oregon summary (51 boys; mean 13.54 years, SD 1.12). V1 was not trained on individual Berkeley, Harpenden or Oregon records. Displayed weights are not calibrated clinical probabilities.

**Beta v2:** separate male/female random forests fitted to individual height histories in both Berkeley and Harpenden. Among 172 eligible children, 102 were used for training, 33 for calibration and 37 for testing, with all windows of a child kept together. Trees do not use cephalometric data, Tanner stages or future input heights. Reference outcomes use full histories only during offline research evaluation.

## Interface and privacy

Both interfaces use date of birth, reference sex and at least three dated heights. Cephalometric forms and mandibular forecasts are not active features. All entered data are processed in the browser, without upload or persistent storage. The beta supports up to seven recent heights within its documented age/spacing domain. Additional observations do not guarantee improvement.

## Research materials

- [Training pipeline and evaluation scripts](training/)
- [Prior v1 provenance audit and preliminary Berkeley benchmark](validation/)
- [Archived pre-v2 roadmap](archive/ROADMAP-pre-v2.md)
- [Oregon longitudinal data explorer](oregon-data-lab.html): descriptive import and quality checks, not a trained prediction model.
- [Oregon aggregate reference provenance](oregon-published-reference.json)

No individual Oregon height dataset has been imported. Source: https://digitalcollections.ohsu.edu/record/1721/files/2424_etd.pdf . Berkeley and Harpenden source details and exact data checksums are in the training report. Do not commit identifiable patient information or restricted records to this public repository.
