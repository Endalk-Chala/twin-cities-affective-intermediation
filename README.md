# Affective Intermediation in Twin Cities Nonprofit Communication

## Organizational emotion, public uptake, circulation, and action during immigration enforcement

**Status:** Active research project · primary corpus assembled, coded, and reproducibly validated  
**Author:** Endalkachew H. Chala  
**Study period:** November 1, 2025–March 31, 2026  
**Primary analytical universe:** 114 eligible/probably eligible organizational, program, and network units  
**Validated coded corpus:** 337 verified communication items from 44 canonical organizations

## Project overview

This repository is the standalone home for a longitudinal study of nonprofit and community communication during intensified immigration enforcement in the Twin Cities.

The project develops **affective intermediation** as a framework for examining how organizations interpret crisis, communicate emotion and appraisal, connect publics to resources and action, and how those messages are subsequently taken up, recirculated, contested, or converted into material or civic action.

`crisis → organizational appraisal → affective production → public uptake → affective circulation → possible conversion/action`

The project analyzes four linked empirical layers:

1. **Affective production** — what organizations communicate.
2. **Affective uptake** — how publics respond through visible comments and replies.
3. **Affective circulation** — how messages travel through shares, reposts, tagging, and cross-platform movement.
4. **Affective conversion** — observable movement toward helping, donating, volunteering, attending, protesting, seeking services, sharing resources, or other coordination/action.

## Sampling frame

The consolidated discovery frame contains **138 raw records**. Screening produced **91 eligible**, **23 probably eligible**, **22 excluded**, and **2 duplicate/alias/program-merge** records. The operational communication-census universe is therefore **114 independent eligible/probably eligible units**.

Communication availability is not an organizational eligibility criterion. A verified organization with incompletely retrievable historical platform content remains in the sampling universe.

## Validated primary corpus

The reproducible build currently produces:

- **337 verified coded communication items**
- **44 canonical organizations**
- **311 website items**
- **26 LinkedIn items**
- **41 recurring-series items flagged for robustness checks**

The master analytical file is `data/processed/full_corpus_coded_master_v1.csv`. The validation report is `analysis/reproducibility_report_v1.md`.

The build pipeline preserves source data, harmonizes legacy and current coding schemas, canonicalizes documented item-ID collisions while retaining original identifiers, normalizes organization labels, joins recurring-series metadata, checks dates and uniqueness, and writes a validated analysis-ready master file. A GitHub Actions workflow reruns the validation when relevant corpus files change.

Additional candidate-tier records remain separate when historical platform retrieval, exact dating, or verification is incomplete.

## Strategic communication relevance

The project treats strategic communication as an organizational process of interpretation, positioning, relationship management, resource provision, advocacy, reassurance, solidarity building, mobilization, and adaptation under crisis and uncertainty.

The analytical hierarchy is:

`Organization → Platform → Time → Affect/Appraisal → Communication Function → Action/Uptake`

This design supports comparative analysis of how service providers, advocacy groups, faith-based organizations, and community-rooted organizations communicate across stages of a crisis and how messages are taken up, recirculated, contested, or connected to observable action.

## Data architecture

```text
twin-cities-affective-intermediation/
├── sampling_frame/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── platform_registry/
├── protocols/
├── codebooks/
├── analysis/
│   ├── scripts/
│   ├── tables/
│   └── figures/
├── paper/
├── documentation/
└── archive/
```

Website communication is comparatively well observed. Historical social-media archives are uneven and platform-dependent; the social corpus is treated as a **bounded public-web recovery with partial historical archives**, not an exhaustive platform census. Hidden engagement is `NA`, not zero.

## Analytical coding

Communication items are coded for situational appraisal, emotion intensity (0–3), emotion source and explicitness, communication function, action orientation, audience, urgency, legal/service information, public uptake, circulation, and observable conversion-to-action signals.

**Engagement volume is not emotion intensity.** Reactions, comments, shares, reposts, and views are relational/circulation measures; emotional meaning is coded separately.

## Current research stage

The primary corpus is assembled and reproducibly validated. The next stage is substantive analysis, including:

1. organization-by-month communication trajectories;
2. organizational-role comparisons;
3. emotion and appraisal profiles;
4. communication-function analysis;
5. platform comparisons;
6. recurring-series robustness checks;
7. public-uptake and circulation analysis;
8. matched-message analysis where data permit.

## Rebuild

```bash
python -m pip install pandas
python analysis/build_full_corpus_master_v6.py
```

## Documentation for faculty applications

See:

- `documentation/strategic_communication_research_infrastructure.md`
- `documentation/job_application_framing_strategic_communication.md`

## Provenance

This project was developed initially inside `Endalk-Chala/mn-immigration-nonprofit-communication`. That repository remains intact as the historical precursor. This repository is the canonical standalone home for the Affective Intermediation project from September 2026 forward.

## Citation

> Chala, Endalkachew H. (2026). *Affective Intermediation in Twin Cities Nonprofit Communication*. GitHub research repository.
