# Migration Provenance

## Canonical project

**Affective Intermediation in Twin Cities Nonprofit Communication**

Canonical repository from September 22, 2026 forward:

`Endalk-Chala/twin-cities-affective-intermediation`

Historical precursor repository:

`Endalk-Chala/mn-immigration-nonprofit-communication`

The precursor repository remains intact. The standalone repository reorganizes the Affective Intermediation study into a clean research-project structure while preserving methodological provenance.

## Path mapping

| Precursor path | Standalone path |
|---|---|
| `research_workspace/01_sampling_frame/` | `sampling_frame/` |
| `research_workspace/02_protocols/` | `protocols/` |
| `research_workspace/03_platform_registry/` | `platform_registry/` |
| `research_workspace/05_data/raw/` | `data/raw/` |
| `research_workspace/05_data/interim/` | `data/interim/` |
| `research_workspace/05_data/processed/` | `data/processed/` |
| `research_workspace/06_codebooks/` | `codebooks/` |
| `research_workspace/07_analysis/` | `analysis/` and `analysis/scripts/` |
| `research_workspace/09_notes/` | `documentation/` or `paper/` as appropriate |

## Migrated core assets

The following core materials have been migrated into the standalone repository:

- standalone project README and formal title;
- consolidated 138-record sampling frame;
- eligibility screening summary and 114-unit analytical-universe logic;
- affective-intermediation coding codebook;
- analysis-ready master schema;
- temporal emotion-arc framework;
- manual coding template;
- 40-item reliability pilot sample;
- analysis plan;
- workflow run order;
- external event chronology;
- refactored analysis-ready dataset builder;
- social census analysis-scope file;
- matched-message candidate table;
- public engagement/affective uptake protocol;
- cross-platform matched-message protocol;
- ILCM January 8 engagement snapshot;
- ILCM January 8 anonymized interaction data;
- ILCM January 8 recirculation evidence;
- ILCM February 12 engagement-observability record;
- IIMN December 19 engagement snapshot.

## Raw communication corpus migration status

The precursor repository contains more than 60 communication-item and unresolved-candidate CSV batches. These files remain authoritative raw provenance until each file is copied byte-for-byte into `data/raw/` in the standalone repository.

The standalone repository must not be described as containing the complete raw communication census until that transfer is complete and checked.

Excluded organizations may remain in the migrated raw audit trail, but primary analysis must respect the final sampling decisions. Examples include PPL, Aeon, Bridging, CommonBond, PRISM, Twin Cities Habitat for Humanity, VOA Minnesota/Wisconsin, and Catholic Charities Twin Cities where applicable under the final screening rules.

## Reproducibility rule

Scripts in the standalone repository should use standalone paths only. The standalone analysis workflow must not require live reads from the precursor repository once raw migration is complete.

## Data integrity rules during migration

1. Do not alter raw item text, dates, URLs, retrieval status, or collection notes during migration.
2. Preserve original filenames unless a documented normalization is necessary.
3. Do not convert missing/hidden engagement fields to zero.
4. Preserve unresolved candidates separately from verified communication items.
5. Preserve excluded-organization data for auditability, but mark analysis inclusion status explicitly.
6. Keep commenter identities anonymized where the precursor data were intentionally anonymized.
7. Preserve source-repository commit history through this provenance record even though the new repository has its own Git history.

## Current analytical status

Broad collection is frozen as a bounded public-web corpus. Website observability is substantially stronger than social-platform historical observability. The next substantive empirical stage is reliability-pilot coding and codebook freeze, followed by full-corpus coding and analysis.
