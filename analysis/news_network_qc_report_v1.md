# News Network QC Report v1

**Branch:** `media-universe-v2`  
**Study window:** 2025-11-01 through 2026-03-31  
**Build source:** all `data/raw/news_media_uptake_batch_*.csv` files

## Two network products

The repository now preserves two distinct verified-news products:

1. **Audit/provenance corpus** — `data/interim/organization_news_relations_master_v1.csv`
2. **Primary analytical network** — `data/interim/organization_news_relations_primary_universe_v1.csv`

The distinction is necessary because verified news coverage can exist for organizations that were later excluded by the final sampling rules. Coverage evidence is preserved; sampling inclusion is enforced at the analysis stage.

## Audit/provenance corpus

- 122 verified organization–story edges
- 104 normalized unique stories
- 33 organizations with at least one verified relation
- 31 registered outlets represented
- 88 local/regional edges
- 17 community/ethnic edges
- 17 national-amplification edges
- 0 unmapped verified outlet edges
- 25 candidate/nonverified relations retained separately

## Primary analytical network

Eligibility is reconstructed from the 14 authoritative screening batches and yields exactly 114 primary-universe organizations: 91 `eligible` plus 23 `probably_eligible`.

After applying that sampling filter to the verified news corpus:

- 120 verified organization–story edges
- 102 normalized unique stories
- 31 primary-universe organizations with at least one verified news relation
- 31 registered outlets represented
- 87 local/regional edges
- 17 community/ethnic edges
- 16 national-amplification edges

Two verified audit edges belong to organizations excluded from the final analytical universe:

- `TC025` — Twin Cities Habitat for Humanity
- `TC050` — Project for Pride in Living

Those relations remain in the audit corpus and are written separately to `organization_news_relations_outside_primary_universe_v1.csv`, but they do not enter primary network analyses.

## QC checks completed

### 1. Eligibility-universe reconstruction — resolved

The standalone repository previously retained the aggregate 114-unit logic without a canonical row-level ledger. `analysis/build_eligibility_universe.py` now reconstructs the universe from the 14 authoritative screening files in the historical precursor repository and asserts the expected counts:

- 138 raw screened records
- 91 eligible
- 23 probably eligible
- 22 excluded
- 2 duplicate/merge records
- 114 primary analytical units

The generated reconciliation files are `sampling_frame/eligibility_universe_reconciliation_v2.csv` and `.md`.

### 2. Legacy news-item ID collision check — resolved

Several raw batches reused `NM###` identifiers for different stories. Raw files remain unchanged for provenance. The normalized build assigns collision-proof `STY-*` story identifiers based primarily on date + canonical outlet + headline and preserves the original batch-level identifiers in `news_item_id_crosswalk_v1.csv`.

### 3. Multi-organization row expansion — resolved

Some legacy rows store multiple organizations in one story row. The normalized build expands these to one organization × story edge, consistent with the relation codebook. A story sourcing three sampled organizations therefore produces three separate network edges.

### 4. Duplicate story–organization relation check — resolved in derived master

The build deduplicates on normalized story ID + organization ID. When duplicate source rows exist, verified rows are preferred, followed by direct-quote and substantive-interpretation evidence.

### 5. Outlet registry join — clean for verified network

All verified relations now map to a registered outlet ID and media layer. Finance & Commerce was added as `NEWS054` after QC surfaced one previously unmapped verified edge.

### 6. Candidate leakage check — controlled

Only rows whose `collection_status` is exactly `verified` enter the verified audit master. Candidate, unresolved, and `verified_external` records remain in `organization_news_relations_candidates_v1.csv` and do not contribute to primary network counts.

### 7. Raw provenance preservation — clean

Raw collection batches are not rewritten to repair legacy collisions or structure. Normalization occurs only in derived/interim files so original collection provenance remains auditable.

## Typology status

The organizational typology now covers the complete 114-unit primary universe. Every primary-universe organization has at least one `verified` role label. Labels remain multi-label and equal-weight at the infrastructure stage.

The build preserves separate provenance tranches for manually coded media-visible organizations, screening-evidence role seeds, and targeted manual verification of initially ambiguous cases.

## Remaining QC limitations

1. Some normalized relations still have article-level metadata gaps such as missing canonical URLs or incomplete author fields. These do not affect node/edge identity where date, outlet, and headline are stable, but they should be resolved before publication-quality replication packages.
2. `headline_presence`, `lead_presence`, `quote_count`, affect terms, dominant affect, and frame transformation remain incompletely coded for many legacy rows. The current network is therefore structurally valid for organization–outlet–layer analysis but not yet complete for affect/frame multilayer analysis.
3. `verified_external` records are intentionally outside the current primary network. A later sensitivity analysis may include them under a separately documented rule.
4. Network degree is descriptive visibility, not organizational importance, influence, effectiveness, or endorsement.
5. Search failure remains distinct from zero coverage; audit logs should be consulted when interpreting organizations with no verified media edges.
6. The 83 primary-universe organizations without a verified news edge should be described as having **no verified edge in the current collected corpus**, not as having received no media coverage.

## QC conclusion

The primary verified organization–news network is suitable for descriptive organization–outlet–media-layer analysis and for comparison against the complete 114-unit multi-label organizational typology. The 122-edge audit corpus should remain available for provenance and sensitivity work. Affect/frame layers should remain provisional until relation-level affective coding is complete.
