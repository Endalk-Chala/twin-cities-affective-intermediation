# Strategic Communication Research Infrastructure

## Affective Intermediation in Twin Cities Nonprofit Communication

This project demonstrates a reproducible research infrastructure for studying how organizations communicate under conditions of crisis, uncertainty, and heightened public attention.

The infrastructure links organizational position, platform, time, appraisal, emotion, communication function, action orientation, public uptake, and circulation in a single longitudinal design. It is intended to support both substantive strategic communication research and transparent, reusable methodological practice.

## What the infrastructure contains

### 1. Organizational sampling frame
A documented organizational universe with eligibility decisions, aliases, exclusions, and provenance retained separately from communication availability.

### 2. Longitudinal communication corpus
A validated primary corpus of 337 verified communication items from 44 organizations, spanning November 2025 through March 2026.

Platform coverage in the validated master corpus:
- 311 website items
- 26 LinkedIn items

Additional partially verified or historically incomplete platform records are preserved in a separate candidate tier rather than treated as confirmed observations.

### 3. Theory-driven coding architecture
Communication items are coded for:
- situational appraisal;
- emotion intensity;
- emotion source and explicitness;
- communication function;
- audience;
- action orientation;
- legal/service/resource information;
- visible public uptake;
- circulation and recirculation;
- observable movement toward action.

The analytical hierarchy is:

`Organization → Platform → Time → Affect/Appraisal → Communication Function → Action/Uptake`

### 4. Reproducible data pipeline
The project uses scripted corpus assembly and validation rather than a manually maintained final spreadsheet.

The current pipeline:
1. reads original coding batches;
2. harmonizes legacy and current schemas;
3. preserves source data while repairing documented CSV structure problems at build time;
4. canonicalizes known legacy identifiers while retaining original identifiers;
5. normalizes organization labels while preserving source labels;
6. joins recurring-series metadata;
7. validates dates, item IDs, organization counts, and platform counts;
8. writes a single analysis-ready master file;
9. generates a reproducibility report;
10. runs automatically through GitHub Actions when relevant source files change.

Validated build result:
- 337 rows
- 337 unique canonical item IDs
- 44 canonical organizations
- 311 website items
- 26 LinkedIn items
- 41 recurring-series items flagged

### 5. Explicit treatment of missingness and platform observability
The project distinguishes between:
- verified absence;
- missing or hidden engagement;
- incomplete historical platform retrieval;
- unresolved candidate records.

Missing or hidden engagement is retained as `NA`, not recoded as zero. Social-media recovery limitations are documented rather than hidden.

### 6. Repetition and robustness controls
Recurring event or service-announcement series are explicitly flagged so repeated calendar content does not mechanically dominate organization-level estimates. This supports full-corpus analysis alongside robustness checks that down-weight or isolate recurring series.

### 7. Public uptake as a separate analytical layer
Visible comments, replies, reposts, and reactions are not treated as direct measures of emotion. They are modeled separately as uptake and circulation evidence, allowing analysis of how organizational communication is received, amplified, contested, or converted into observable action.

## Relevance to strategic communication research

The project treats strategic communication as an organizational process involving interpretation, positioning, relationship management, resource provision, public engagement, mobilization, and adaptation over time.

It therefore supports research questions such as:
- How do organizations change communication strategies across stages of a crisis?
- How do organizational roles shape emotional framing and action orientation?
- How do service, advocacy, faith-based, and community-rooted organizations communicate differently?
- When do organizations move from information provision to reassurance, advocacy, solidarity building, or mobilization?
- How do platform affordances shape organizational communication?
- How do publics respond to, recirculate, contest, or act on organizational messages?
- How can strategic communication scholarship integrate organizational texts, temporal context, public response, and reproducible computational methods?

## Research and teaching value

The infrastructure can support:
- peer-reviewed research in strategic communication, public relations, organizational communication, digital media, and crisis communication;
- student training in content analysis and computational communication research;
- methods courses covering reproducibility, coding design, data provenance, and validation;
- collaborative research involving community organizations and public-facing communication;
- future comparative extensions across cities, crises, organizations, and platforms.

## Core reproducibility files

- `data/processed/full_corpus_coded_master_v1.csv`
- `analysis/reproducibility_report_v1.md`
- `analysis/build_full_corpus_master_v6.py`
- `codebooks/affective_intermediation_coding_codebook_v1.md`
- `data/processed/recurring_series_map_v1.csv`
- `data/processed/candidate_tier_inventory_v1.csv`

This infrastructure is designed so that the substantive argument can evolve without losing the underlying audit trail, coding provenance, and reproducibility of the corpus.
