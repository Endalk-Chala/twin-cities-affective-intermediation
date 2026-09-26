# Eligibility-Universe Reconciliation v2

## Purpose

This note reconciles the project's discovery-frame denominator with the later operational audit denominator so that the organizational universe is transparent before typology coding and communication analysis proceed.

## Stable analytical universe

The current operational communication-census universe remains **114 independent eligible or probably eligible organizational units**.

The study window remains **November 1, 2025 through March 31, 2026, inclusive**.

Public communication availability, immigration-enforcement relevance, emotionality, and communication intensity are **not** organizational eligibility criteria.

## Why two denominators appear in project records

Two legitimate but different frames have been used during project construction:

### 1. Discovery frame

The consolidated discovery registry contains **138 raw records**.

The original screening summary classified these as:

- 91 eligible;
- 23 probably eligible / verification needed;
- 22 excluded;
- 2 duplicate / alias / program-merge records.

This produces the same 114-unit operational universe: **91 + 23 = 114**.

The 138 denominator therefore describes the full discovery history, not the final analytical universe.

### 2. Later eligibility-audit frame

A subsequent working checkpoint recorded **126 rows checked**, with:

- 114 retained as independent eligible/probably eligible units;
- 11 formally excluded rows;
- 1 duplicate alias row.

This 126-row denominator describes the later audit table/checking workflow, not the complete discovery history.

The two denominators should therefore not be presented as competing estimates of the universe. They represent different stages of sampling-frame construction.

## Reconciliation rule

For all analysis and collection trackers, use:

- `discovery_frame_n = 138` when describing the complete raw discovery history;
- `audit_frame_n = 126` only when describing the later checked-row audit workflow;
- `operational_universe_n = 114` for the communication census and organizational comparisons.

Until the 12-record difference between the 138-row discovery frame and 126-row later audit table is row-by-row documented, do **not** infer that those 12 records were excluded, duplicates, inactive, or otherwise analytically irrelevant. Preserve the difference as a provenance/QC issue.

## Known unit-resolution decisions

- **Navigate MN** is an alias/former-name record for **Unidos MN** and is not an independent organizational unit.
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
- `provenance_frame` (`discovery_138`, `audit_126`, or both)
- `reconciliation_notes`

## Analytical implication

Organizational typology must be assigned only after unit identity is resolved. Typology categories describe **what kind of organization an included unit is**; they must never be used to decide whether communication is eligible for collection.

The typology therefore operates on the stable **114-unit organizational universe**, while communication-item coding operates on all defensibly retrievable organization-owned public communication within the fixed study window.

## Outstanding QC

1. Identify the exact 12 raw discovery records not represented in the later 126-row audit frame.
2. Reconcile any previously collected website or social-media items belonging to excluded, alias, or program-level records against the 114-unit universe.
3. Preserve unresolved communication candidates separately from verified items.
4. Do not update claims of corpus completeness until platform-level archive limitations are recorded.
