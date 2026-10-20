# Public data release v0.1 — 210-item manuscript corpus

**Status:** Provisional; revised public data package prepared for Zenodo. This page is a release guide, not a claim that the dataset CSV has been uploaded to GitHub or that Zenodo has minted a DOI.

## Validated release facts
- 210 distinct item IDs from 32 organizations; 188 website and 22 LinkedIn items.
- 207 completely coded, three partially coded.
- Public version excludes free-text source passages, item source URLs, individual coder notes, original source captures, and copyright-sensitive text.
- The 14 focal emotion categories are separate from residual `other_emotion`.
- The supplied agreement summary reports median emotion alpha ~.85, but raw coder sheets and calculation code were not provided for independent recalculation.
- Reassurance alpha ~.58 misses the report's minimum threshold.
- Sum of adjudication cells in the released analytical table is 690; the report describes 744. Investigate before certifying human coder agreement or publishing a final analysis.
- Historical root corpus is 337 items from 44 organizations; it is **not** the current manuscript's analytical corpus.

## Provisional Zenodo archive contents
`analysis_210_coded_public_v0_1.csv`, `Codebook_v1.2_frozen_rules.md`, `full_corpus_agreement_report.md`, `full_corpus_agreement_by_variable.csv`, `DATA_CHECKS.json`, `README.md`, `ZENODO_DEPOSIT_METADATA.json`, `SHA256SUMS.json`.

The attached draft package is prepared separately. Do not claim that it is in this repository until it has been uploaded and checked.

## Next
1. Upload and publish the reviewed archive on Zenodo, receiving an actual DOI.
2. Upload the curated public CSV and documentation to this repository, with an exact version identifier.
3. Align a tagged GitHub release with the published Zenodo dataset.
4. Obtain and audit both human coder sheets and statistical scripts; issue a corrected release version.
