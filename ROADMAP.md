# Growth Phase Predictor — Project Roadmap

**Live website:** https://brycebothwell.github.io/Growth-phase-predictor/
**Research status:** V1 uses literature-informed candidate growth curves and has NOT been trained or externally validated. Growth velocity arithmetic is descriptive; phase weights are NOT calibrated probabilities. Do not use predictions for clinical decisions.

## Milestones
- [x] V1 — Published interactive website for birth date, sex and 3+ dates/heights with velocity calculations and provisional growth-phase outputs.
- [ ] V2 — Train on real individual longitudinal growth data, starting with publicly available Berkeley height trajectories.
- [ ] V2 — Apply for large-cohort ALSPAC and NIH BioLINCC NGHS records; confirm access terms and deidentification.
- [ ] V3 — Validate with participant-level holdouts, truncating records to 3/4/5 time points at different intervals.
- [ ] V3 — Calibrate PHV phase probabilities and PHV date uncertainty intervals; examine error and fairness across subgroups.
- [ ] V4 — Optimize interface, privacy and quality flags; produce transparent clinical research reports.
- [ ] V5 — Separately test whether estimated statural PHV predicts mandibular growth or orthodontic growth-modification outcomes. This requires orthopedic/cephalometric outcome data.

## NEXT STEP — Real longitudinal growth data

### A. Begin with open Berkeley data
Documentation: https://search.r-project.org/CRAN/refmans/bsitar/html/berkeley.html
bsitar describes a Berkeley dataset with 136 children and 4,884 observations including subject id, age, height and sex. A DIFFERENT Berkeley dataset variant with 93 children is also publicly described; check versions and do not treat them as identical.
In R: install.packages('bsitar'); data('berkeley', package='bsitar'); str(berkeley)
Convert to a long table: anonymous subject_id | sex | age_years | height_cm. Review duplicates, gaps and measurement quality. Keep participant-level training/test separation.

### B. Apply for ALSPAC longitudinal measurements
Official access instructions: https://www.bristol.ac.uk/alspac/researchers/access/
Explore variable catalogue: https://www.bristol.ac.uk/alspac/researchers/our-data/
Request pseudonymous participant ID, sex, age/date at each examination, repeated standing height from childhood through late adolescence, measurement precision/method and available maturation indicators.
Proposed title: Predicting individual peak height velocity from sparse longitudinal stature observations for orthodontic research.
Submit a research proposal through their online application. Review associated costs, policies and data access agreements. Contact alspac-data@bristol.ac.uk with questions. The site says initial response within 10 working days.

### C. Request NIH BioLINCC NGHS
Data source: https://biolincc.nhlbi.nih.gov/studies/nghs/
Use its Request Data workflow for repeated height measurements, participant ID and visit age. NGHS is a longitudinal cohort of girls, so use a separate male cohort for sex-specific predictions. Follow data-use rules.

## Statistical design
1. Learn individual growth tempo, size and pubertal timing from full individual trajectories, comparing SITAR, Bayesian mixed models and simpler baselines.
2. Define reference peak-height-velocity from full trajectory with a prespecified smoothing and age window.
3. In validation, mask later visits and show model only the first 3, 4 or 5 measurements; never put visits from the same child in both training and test splits.
4. Estimate prepeak / within 6 months of PHV / postpeak and an uncertainty interval for PHV age.
5. Evaluate calibration, phase accuracy, PHV timing MAE, interval coverage, and abstention on insufficient data; externally validate on separate cohorts.

## Scientific caveat: midpalatal suture
No validated direct rule maps height velocity (cm/year), age relative to PHV, or this tool's phase output to midpalatal suture fusion or conventional RME success. Suture stage, skeletal maturity and resistance to expansion are not equivalent.
Angelieri et al. 2013: https://pubmed.ncbi.nlm.nih.gov/24182592/
CVM/MPS study 2023: https://pmc.ncbi.nlm.nih.gov/articles/PMC10360312/
MPS/age study 2024: https://pubmed.ncbi.nlm.nih.gov/38311670/

## Separation and privacy
This repository is the GROWTH CURVE CALCULATOR project only. Keep Masters Research thesis, ANS, EMG and individual cephalometric research files in their separate project. This repository is PUBLIC; never upload identifiable patient records or restricted cohort data. Confirm IRB and data-use requirements before research with patients.

## Oregon Growth Study data ingestion (added November 2026)

- **[Open local Oregon longitudinal-stature data lab](oregon-data-lab.html)** (works through GitHub Pages at https://brycebothwell.github.io/Growth-phase-predictor/oregon-data-lab.html)
- **[Blank import CSV schema](oregon-template.csv)**: subject_id,sex,age_years,height_cm. Anonymous subject IDs only; no names or DOB.
- The AAOF public Legacy Collection serves Oregon cephalograms and mostly cephalometric numerical measurements. It does **not** currently provide a verified downloadable set of participant-level serial standing heights. We have therefore **not trained a stature model on Oregon data**.
- Historical research describes actual physical measurements including standing height in the Oregon cohort (Savara's Child Clinic Study). These must be requested from the Oregon archive/collection curator before any data-trained output can be produced.
- Contact AAOF Website Administrator: info@aaoflegacycollection.org; https://www.aaoflegacycollection.org/aaof_aboutsite.html
- Because this is an OHSU-origin study, inquire through the OHSU Department of Orthodontics about access to original longitudinal stature charts and digitized records. Historic sources identify David A. Covell Jr. as the collection curator; confirm current stewardship before directing the request to a particular person.
- Ask for each participant's anonymized study ID, sex, date or precise age at each height observation, standing height and measurement units, and if available Tanner or skeletal maturity annotations. Ask about completeness, digitization, copyright/data-use agreements, authorization to derive and release trained model coefficients.
- Only use authorized records for analyses and retain deidentified datasets outside this public repository.
- After obtaining records, assess coverage around pubertal growth, deduplicate visits, flag physiologically implausible intervals, estimate individual PHV retrospectively, then split by subject and validate sparse-history 3/4/5 point predictions before modifying the clinical-facing predictor.

## Oregon Growth Study pilot update (9 Nov 2026)

The published 1977 Oregon Child Study Clinic report by Jorge Grau provides an **actual male PHV age summary** from 51 boys (mean age 13.54 years, SD 1.12 years, plus an 11-bin age-at-peak distribution). It is now displayed in the [Oregon Data Lab](oregon-data-lab.html) and used only as an **experimental male PHV-age prior** in the main calculator. Source: https://digitalcollections.ohsu.edu/record/1721/files/2424_etd.pdf — see [machine-readable provenance](oregon-published-reference.json).

**The Oregon person-level stature trajectories are NOT yet publicly available in a usable dataset. No Oregon height-by-age rows have been imported and the model is NOT trained/validated on those individual records.** [Blank import schema](oregon-template.csv). Please request the original records from the OHSU/AAOF custodians before a true data-trained version.

## Target product: ONE cephalogram + THREE standing-height observations

**Clinical inference specification (revised 9 Nov 2026):** at least three heights with measurement dates, patient age and sex; **zero cephalograms** for height-only PHV analysis, or **one or more optional existing lateral cephalograms** for the eventual mandibular growth module. Predict the additional Co–Gn and Co–Go growth expected by a clearly defined postpubertal/adult endpoint, plus estimated final length and calibrated 50%/90% prediction intervals. A single ceph at inference is not the same as single ceph in training: training must have cephalometric follow-up outcomes.

For the first version, accept **human-entered measurements** from one ceph (Co–Gn, Co–Go; consider MPA, face heights, and optional CVM); add image upload/auto-landmark tracing only after image calibration, landmark accuracy, privacy, and regulatory evaluation. Compute two intervisit height velocities from three visits, warn when measurements are very closely spaced or inconsistent, and abstain if predictions are not supported. Age/sex are necessary contextual inputs.

### Strong newly published normative cephalometric resource

Oh H et al. (2026), *Craniofacial growth percentile curves: A clinical tool from the Craniofacial Growth Consortium Study*, analyzed **2,100 people and 17,290 longitudinal lateral cephalograms** spanning ages 2.5–31.3 y, with **Co–Gn and Co–Go** among 24 dimensions. See https://pmc.ncbi.nlm.nih.gov/articles/PMC13138386/ and https://www.aaoflegacycollection.org/aaof_craniofacialGrowth.html. The study provides age-/sex-referenced percentile growth curves; those are **not equivalent to individual trained forecasts from one ceph + three heights**. Confirm whether model coefficients/supplementary curves can be reused legally and with correct attribution.

### Mandatory research validation

- Obtain longitudinal *linked* stature and ceph records for the **same participants**. An external height-only cohort (Berkeley) plus an external ceph-only cohort (CGCS) permits separate priors, but cannot measure whether the combined 3-height+ceph input actually improves individual prediction.
- Determine horizon/endpoints (for example Co–Gn at fixed future ages, not guaranteed biologic "final length"), untreated status, and imaging enlargement correction; do not predict functional appliance effects from untreated controls.
- Compare three models: age/sex+single ceph; age/sex+three heights; and combined. Include normative CGCS curves as an explicitly labeled baseline/prior where licensed.
- In validation, show each index case only **one ceph + the three preceding height records**, hold future cephs for outcome truth, and split by participant. Report MAE (mm), prediction-interval coverage, calibration, bias and failure modes; additionally validate in an independent historical cohort if possible.
- Three heights yield **two observed velocities** and do not uniquely identify the individual's true PHV. Phase probabilities must be calibrated and may require uncertainty/abstention, particularly with short intervals. The AAP discourages over-interpreting intervals under six months: https://eqipp.aap.org/courses/growth2/mn/clinical-guide/popups/growth-velocity
- **Research-only** until training, validation and ethical requirements are met. No synthetic/unvalidated outputs labeled clinical estimates.

Implementation issue: https://github.com/brycebothwell/Growth-phase-predictor/issues/3

## Flexible observation counts (implemented Nov 2026)

The prototype now accepts **3 or more dated heights** and independently **1 or more dated lateral-ceph measurement sets** (Co–Gn, Co–Go and optionally mandibular plane angle). The patient can add or remove observations, summarize *observed* cephalometric changes in mm/year when 2+ cephs exist, and export ceph measurements as CSV. At present, ceph data are for descriptive history only and do **not** affect the experimental statural-PHV output. The mandibular forecast has NOT been trained or released. Never take additional cephalograms solely to improve this research prototype; use existing clinically justified radiographs.

### Planned evidence-based adaptation to additional observations

- **Base workflow:** at least 3 dated heights, age and sex. The first ceph is OPTIONAL; 0 cephs means statural growth-phase results only. When a ceph exists, allow 1+ dated ceph records for mandibular modules.
- **Optional histories:** 4–8+ heights and 2–4+ existing cephs, with irregular visit dates accepted after appropriate quality checks, modality corrections and temporal synchronization.
- Model needs to **handle missing additional measurements gracefully**, so users with only the minimum aren't excluded, and still use all valid past information available to the prediction date without leaking later outcomes.
- Validate performance separately in held-out patients with 3, 4, 5, 6+ prior heights and with 1, 2, 3+ prior cephs. Compare incremental mm MAE and calibrated prediction interval coverage vs a constant minimal-input baseline on **the same patients**, to avoid differences in patient selection driving claimed improvement.
- More points may reduce uncertainty but do **not** guarantee better individual predictions. Scan technique, landmark reproducibility, time gaps, treatment status, radiographic magnification and variable timing matter. Longer observation span can be more informative than simply more closely spaced heights.
- Future repeated cephs should allow estimating individual observed skeletal growth tempo, in addition to current Co–Gn and Co–Go. Maintain a distinct untreated-versus-treated analysis and update forecasts as new data become clinically available.
- The current HTML form does not transmit data; no cloud storage, accounts, or patient-record persistence. For future production, add authorized privacy/security and data governance separately.

### Optional cephalogram UX implemented

As of 9 Nov 2026, the cephalometric panel opens collapsed and contains **zero rows** by default. Users may supply no ceph, or add/remove existing ceph measurements (including removal of the last one). The original 3+ heights workflow continues independently and shows stature growth velocity, height curve, and provisional PHV stage as before. One or more optional cephs can be summarized as observed measurements, and two or more can yield historical Co–Gn / Co–Go changes. A combined, validated mandibular forecast remains a future research milestone; ceph observations do not affect the current height-phase calculation.
