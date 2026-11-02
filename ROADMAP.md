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