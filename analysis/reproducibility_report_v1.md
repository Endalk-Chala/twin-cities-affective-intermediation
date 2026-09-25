# Reproducibility Report — Full Coded Corpus v1

## Build result

- Primary verified rows: **337**
- Unique item IDs: **337**
- Organizations: **44**
- Study window: **2025-11-01 to 2026-03-30**
- Website items: **311**
- LinkedIn items: **26**
- Recurring-series rows: **41**
- Candidate-tier records excluded and retained separately.
- SHA-256: `85333eb6cb1edd35139bc50353020ede3c3159d0bd8484b3c4f3e455025391bd`

## Validation checks

- PASS: 337 rows
- PASS: 337 unique item IDs
- PASS: no duplicate item IDs
- PASS: all dates in study window
- PASS: 44 canonical organizations
- PASS: 311 website + 26 LinkedIn items
- PASS: organization labels normalized (including CLUES)

## Monthly coverage

| Month | Items |
|---|---:|
| 2025-11 | 44 |
| 2025-12 | 40 |
| 2026-01 | 95 |
| 2026-02 | 84 |
| 2026-03 | 74 |

## Organization coverage

| Organization | Items |
|---|---:|
| Mid-Minnesota Legal Aid | 28 |
| International Institute of Minnesota | 25 |
| Comunidades Latinas Unidas En Servicio (CLUES) | 24 |
| The Advocates for Human Rights | 21 |
| Unidos MN | 20 |
| Center for Victims of Torture | 20 |
| Jewish Community Action | 19 |
| Project for Pride in Living | 18 |
| ACLU of Minnesota | 13 |
| Alight | 13 |
| Twin Cities Habitat for Humanity | 13 |
| COPAL | 12 |
| Cedar Riverside Adult Education Collaborative | 10 |
| Volunteers of America Minnesota and Wisconsin | 10 |
| Minnesota Interfaith Coalition on Immigration | 8 |
| Immigrant Law Center of Minnesota | 8 |
| Arrive Ministries | 6 |
| PRISM | 5 |
| Groundwork Legal | 5 |
| Missions Inc. Programs | 5 |
| ACER | 4 |
| Isuroon | 4 |
| Oromo Community of Minnesota | 4 |
| Al-Maa'uun | 4 |
| African Economic Development Solutions (AEDS) | 4 |
| African Development Center of Minnesota | 3 |
| Aeon | 3 |
| CAPI USA | 3 |
| Volunteer Lawyers Network | 3 |
| CommonBond Communities | 3 |
| Minnesota Council of Churches | 3 |
| Ayada Leads | 2 |
| ISAIAH | 2 |
| Bridging | 2 |
| AVIVO | 1 |
| Catholic Charities Twin Cities | 1 |
| Immigrant Defense Network | 1 |
| IAFR Jonathan House | 1 |
| Hmong American Partnership | 1 |
| Esperanza United | 1 |
| Centro Tyrone Guzman | 1 |
| Literacy Minnesota | 1 |
| Karen Organization of Minnesota | 1 |
| SEWA-AIFW | 1 |

## Missingness

Missing values remain NA; they are not silently converted to zero.

| Field | Missing rows |
|---|---:|
| `series_id` | 296 |
| `series_analysis_note` | 296 |
| `series_type` | 296 |
| `series_label` | 296 |

## Rebuild

```bash
python -m pip install pandas
python analysis/build_full_corpus_master_v6.py
```

All source coding CSVs are preserved unchanged. Structural CSV drift is repaired deterministically at build time using schema constraints and hard anchors. Known legacy item-ID reuse is canonicalized while preserving `source_item_id`. Organization labels are canonicalized while preserving `source_organization`. Candidate-tier records remain outside the primary quantitative corpus.
