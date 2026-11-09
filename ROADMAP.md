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
