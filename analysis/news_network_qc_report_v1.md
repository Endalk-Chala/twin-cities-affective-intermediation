# News Network QC Report v1

**Branch:** `media-universe-v2`  
**Study window:** 2025-11-01 through 2026-03-31  
**Build source:** all `data/raw/news_media_uptake_batch_*.csv` files  
**Generated network:** `data/interim/organization_news_relations_master_v1.csv`

## Current verified network

- 122 verified organization–story edges
- 104 normalized unique stories
- 33 organizations with at least one verified relation
- 31 registered outlets represented
- 88 local/regional edges
- 17 community/ethnic edges
- 17 national-amplification edges
- 0 unmapped verified outlet edges
- 25 candidate/nonverified relations retained separately

## QC checks completed

### 1. Legacy news-item ID collision check — resolved

Several raw batches reused `NM###` identifiers for different stories. Raw files remain unchanged for provenance. The normalized build assigns collision-proof `STY-*` story identifiers based primarily on date + canonical outlet + headline and preserves the original batch-level identifiers in `news_item_id_crosswalk_v1.csv`.

### 2. Multi-organization row expansion — resolved

Some legacy rows store multiple organizations in one story row. The normalized build expands these to one organization × story edge, consistent with the relation codebook. A story sourcing three sampled organizations therefore produces three separate network edges.

### 3. Duplicate story–organization relation check — resolved in derived master

The build deduplicates on normalized story ID + organization ID. When duplicate source rows exist, verified rows are preferred, followed by direct-quote and substantive-interpretation evidence.

### 4. Outlet registry join — clean for verified network

All verified relations now map to a registered outlet ID and media layer. Finance & Commerce was added as `NEWS054` after QC surfaced one previously unmapped verified edge.

### 5. Candidate leakage check — controlled

Only rows whose `collection_status` is exactly `verified` enter the primary master network. Candidate, unresolved, and `verified_external` records remain in `organization_news_relations_candidates_v1.csv` and do not contribute to primary network counts.

### 6. Raw provenance preservation — clean

Raw collection batches are not rewritten to repair legacy collisions or structure. Normalization occurs only in derived/interim files so original collection provenance remains auditable.

## Remaining QC limitations

1. Some normalized relations still have article-level metadata gaps such as missing canonical URLs or incomplete author fields. These do not affect node/edge identity where date, outlet, and headline are stable, but they should be resolved before publication-quality replication packages.
2. `headline_presence`, `lead_presence`, `quote_count`, affect terms, dominant affect, and frame transformation remain incompletely coded for many legacy rows. The current network is therefore structurally valid for organization–outlet–layer analysis but not yet complete for affect/frame multilayer analysis.
3. `verified_external` records are intentionally outside the current primary network. A later sensitivity analysis may include them under a separately documented rule.
4. Network degree is descriptive visibility, not organizational importance, influence, effectiveness, or endorsement.
5. Search failure remains distinct from zero coverage; audit logs should be consulted when interpreting organizations with no verified media edges.

## QC conclusion

The current verified organization–news network is suitable for descriptive network construction and for joining to the multi-label organizational typology. Affect/frame network layers should be treated as provisional until the corresponding relation fields are fully coded.
