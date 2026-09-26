# Eligibility Universe Reconciliation v2

Authoritative row-level reconstruction from the 14 eligibility-screening batches in the historical precursor repository.

## Reconciled counts

- Raw screened records: **138**
- Eligible: **91**
- Probably eligible / verification needed: **23**
- Excluded: **22**
- Duplicate/alias/program merges: **2**
- Primary analytical universe (eligible + probably eligible): **114**

## Analytical rule

`primary_universe_flag = 1` only for `eligible` and `probably_eligible`. Excluded and merged records remain in the reconciliation file for auditability but must not be treated as independent primary-universe organizations.

## Excluded records

- `TC015` — Aeon
- `TC016` — Bridging
- `TC018` — East African Housing Services
- `TC020` — Greater Metropolitan Housing Corporation
- `TC025` — Twin Cities Habitat for Humanity
- `TC026` — Volunteers of America Minnesota and Wisconsin
- `TC036` — Catholic Charities Twin Cities
- `TC037` — CommonBond Communities
- `TC049` — PRISM
- `TC050` — Project for Pride in Living
- `TC079` — Fe y Justicia MN
- `D1-02` — CHW Solutions
- `D1-03` — ESHARA - Ethnic Self-Help Alliance for Refugee Assistance
- `D1-04` — Center for African Immigrants and Refugees Organization (CAIRO)
- `D1-05` — Intercultural Mutual Assistance Association (IMAA)
- `D1-06` — CAPLP - Lakes & Prairies Community Action Partnership
- `D1-07` — United Community Action Partnership (UCAP)
- `D1-08` — Southwest Minnesota Private Industry Council (SWMNPIC)
- `D3-17` — Alliance of Chicanos Hispanics and Latin Americans (ACHLA)
- `D3-22` — Church of St. Leonard of Port Maurice - refugee co-sponsorship
- `D3-23` — Church of the Holy Name - refugee co-sponsorship
- `D4-12` — Power of People Leadership Institute

## Merged / non-independent records

- `TC083` — Navigate MN (`duplicate_alias`)
- `D2-09` — Monarca (`duplicate_program_candidate`)

## Provenance

Source: `Endalk-Chala/mn-immigration-nonprofit-communication`, `research_workspace/01_sampling_frame/eligibility_screening_batch_01...14`.

This file closes a migration gap in the standalone repository: the earlier summary retained the aggregate 114-unit logic, but the row-level screening batches had not yet been migrated into one canonical reconciliation table.
