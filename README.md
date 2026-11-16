# Growth Phase Predictor

### [Open the website](https://brycebothwell.github.io/Growth-phase-predictor/)

> Experimental research prototype. No validated phase confidence or clinical treatment recommendation.

## [Oregon Growth Study — research data lab](oregon-data-lab.html)

Import authorized deidentified individual height observations from the Oregon Growth Study (or other longitudinal cohorts) locally in your browser. No actual Oregon heights are currently bundled; the public AAOF archive primarily offers cephalometric records. [Blank CSV template](oregon-template.csv).

## 📌 [START HERE — PINNED ROADMAP and next steps for real longitudinal data](ROADMAP.md)

This GitHub repository is dedicated to the Growth Curve Calculator, separate from the Masters Research thesis.

Current phase: obtain longitudinal data, train the algorithm and calibrate probabilities. [Detailed data-access instructions](ROADMAP.md#next-step--real-longitudinal-growth-data).

Never upload patient identifiers or restricted longitudinal cohort records to this public repository.
## Oregon Growth Study pilot update (9 Nov 2026)

The published 1977 Oregon Child Study Clinic report by Jorge Grau provides an **actual male PHV age summary** from 51 boys (mean age 13.54 years, SD 1.12 years, plus an 11-bin age-at-peak distribution). It is now displayed in the [Oregon Data Lab](oregon-data-lab.html) and used only as an **experimental male PHV-age prior** in the main calculator. Source: https://digitalcollections.ohsu.edu/record/1721/files/2424_etd.pdf — see [machine-readable provenance](oregon-published-reference.json).

**The Oregon person-level stature trajectories are NOT yet publicly available in a usable dataset. No Oregon height-by-age rows have been imported and the model is NOT trained/validated on those individual records.** [Blank import schema](oregon-template.csv). Please request the original records from the OHSU/AAOF custodians before a true data-trained version.

## Height-only calculator (restored 16 Nov 2026)

The calculator accepts **3 or more dated height measurements**, date of birth and sex. It displays interval height velocities, height and velocity plots, and experimental PHV estimates. The cephalometric input panel and mandibular summaries have been removed by restoring the previous height-only interface. The height prediction algorithm is unchanged.

Older mandibular-development sections in the roadmap are historical proposals, outside the current scope.

