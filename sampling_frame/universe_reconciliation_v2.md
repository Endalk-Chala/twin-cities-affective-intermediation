# Eligibility-Universe Reconciliation v2

## Purpose

This note clarifies the project denominator before organizational typology coding and communication analysis proceed.

## Stable analytical universe

The current operational communication-census universe is **114 independent eligible or probably eligible organizational units**.

The study window remains **November 1, 2025 through March 31, 2026, inclusive**.

Public communication availability, immigration-enforcement relevance, emotionality, and communication intensity are **not** organizational eligibility criteria.

## Canonical discovery frame

The consolidated discovery registry contains **138 raw records**.

The original screening summary classified these as:

- 91 eligible;
- 23 probably eligible / verification needed;
- 22 excluded;
- 2 duplicate / alias / program-merge records.

This produces the operational universe of **114 eligible or probably eligible units (91 + 23)**.

The 138 denominator describes the complete discovery history. The 114 denominator describes the organizational universe used for communication-census construction and organizational comparison.

## Reconciliation rule

For all analysis and collection trackers, use:

- `discovery_frame_n = 138` when describing the complete raw discovery history;
- `operational_universe_n = 114` for the communication census and organizational comparisons.

Do not introduce an intermediate denominator unless a repository artifact documents its row-level composition and provenance.

## Known unit-resolution decisions

- **Navigate MN** is the former-name/alias record for **Unidos MN** and is not counted as an independent organizational unit.
- **Monarca** is treated as program-level material associated with **Unidos MN**, not as a separate organization; Monarca-branded communication may be retained as program-level communication when verified.
- Organizations that fail the project's immigrant/refugee-population, geography, organizational-form, or study-period existence criteria remain in the audit trail but outside the 114-unit communication census.

## Required status fields

Every organizational record used downstream should preserve at least:

- `org_id`
- `organization_name`
- `sampling_status`
- `analysis_inclusion_status`
- `independent_unit_flag`
- `merge_into_org_id`
- `program_level_only`
- `eligibility_basis`
- `eligibility_evidence`
- `eligibility_last_checked`
- `provenance_frame`
- `reconciliation_notes`

## Analytical implication

Organizational typology must be assigned only after unit identity is resolved. Typology categories describe **what kind of organization an included unit is**; they must never be used to decide whether communication is eligible for collection.

The typology therefore operates on the stable **114-unit organizational universe**, while communication-item coding operates on all defensibly retrievable organization-owned public communication within the fixed study window.

## Current corpus relationship

The validated coded communication corpus currently contains **337 verified items from 44 canonical organizations**. These 44 organizations are an observed subset of the larger 114-unit organizational universe; presence in the coded corpus is a communication-retrieval outcome, not a separate organizational-eligibility rule.

## Outstanding QC

1. Produce a row-level organizational-universe table carrying final eligibility and unit-resolution fields for all 138 discovery records.
2. Reconcile previously collected website or social-media items belonging to excluded, alias, or program-level records against the 114-unit universe.
3. Preserve unresolved communication candidates separately from verified items.
4. Do not update claims of corpus completeness until platform-level archive limitations are recorded.
5. Keep organizational typology in a separate organization-level table linked to item-level data through `org_id`.
