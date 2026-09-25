# Reproducibility Report — Full Coded Corpus v1

## Build result

- Primary verified rows: **337**
- Unique item IDs: **337**
- Organizations: **45**
- Study window: **2025-11-01 to 2026-03-30**
- Website items: **311**
- LinkedIn items: **26**
- Recurring-series rows: **41**
- Candidate-tier records excluded and retained separately.
- SHA-256: `baaaef3f1c6c0edaf69eb69852aa5403f1098523fc25fa43d5f1bd35029b1ff8`

## Validation checks

- PASS: 337 rows
- PASS: 337 unique item IDs
- PASS: no duplicate item IDs
- PASS: all dates in study window
- PASS: 45 organizations
- PASS: 311 website + 26 LinkedIn

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
| Comunidades Latinas Unidas En Servicio (CLUES) | 23 |
| The Advocates for Human Rights | 21 |
| Center for Victims of Torture | 20 |
| Unidos MN | 20 |
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
| Missions Inc. Programs | 5 |
| Groundwork Legal | 5 |
| Isuroon | 4 |
| Al-Maa'uun | 4 |
| ACER | 4 |
| Oromo Community of Minnesota | 4 |
| African Economic Development Solutions (AEDS) | 4 |
| African Development Center of Minnesota | 3 |
| Aeon | 3 |
| CAPI USA | 3 |
| Minnesota Council of Churches | 3 |
| Volunteer Lawyers Network | 3 |
| CommonBond Communities | 3 |
| Ayada Leads | 2 |
| Bridging | 2 |
| ISAIAH | 2 |
| AVIVO | 1 |
| CLUES | 1 |
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
| `series_label` | 296 |
| `series_type` | 296 |
| `series_analysis_note` | 296 |

## Rebuild

```bash
python -m pip install pandas
python analysis/build_full_corpus_master_v3.py
```

All source coding CSVs are preserved unchanged. Structural CSV drift is repaired deterministically at build time using schema constraints and hard anchors. Candidate-tier records remain outside the primary quantitative corpus. Known legacy item-ID reuse is canonicalized at build time while preserving the original source_item_id.
