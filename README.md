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

## Flexible clinical input prototype

The [live website](https://brycebothwell.github.io/Growth-phase-predictor/) now supports **3+ dated height observations with zero cephalograms required**; an optional collapsed panel accepts **1 or more existing cephalometric measurement sets** (Co–Gn, Co–Go, optional mandibular plane angle). The ceph history summarizes *observed* changes only; a **validated future mandibular forecast is not yet available**. Do not obtain radiographs solely for this research tool. [Evaluation roadmap](ROADMAP.md#flexible-observation-counts-implemented-nov-2026).

### Height-only default

When no cephalometric records are entered, the application continues to provide its original height-velocity intervals, plots and experimental PHV-phase results. Ceph inputs are optional and are not required by the height algorithm. The ceph panel starts collapsed with zero observations. If one or more existing cephs are added, their historical measurements can be summarized separately; **cephs are not yet used in a trained mandibular growth forecast**.
