# Role–Media Visibility Descriptive Analysis v1

**Unit:** organization in the 114-unit primary analytical universe  
**Media outcome:** at least one verified organization–news relation in the currently collected corpus  
**Important:** absence of a verified edge is an observability result, not proof that an organization received no media coverage.

## Universe-level descriptive picture

- Primary analytical organizations: **114**
- Organizations with at least one verified media edge: **31** (27.2%)
- Organizations with no verified edge in the current corpus: **83** (72.8%)
- Organizations observed across more than one media layer: **13**
- Organizations observed in the national-amplification layer: **11**

## Role-level patterns

The following rows are descriptive and restricted to role categories represented by at least five organizations. They should not be read as causal effects or as rankings of organizational effectiveness.

- `civil_rights_human_rights`: 13/15 organizations (86.7%) have at least one verified media edge; 8 cross media layers; 6 reach the national-amplification layer.
- `organizing`: 10/16 organizations (62.5%) have at least one verified media edge; 5 cross media layers; 5 reach the national-amplification layer.
- `advocacy`: 21/40 organizations (52.5%) have at least one verified media edge; 9 cross media layers; 7 reach the national-amplification layer.
- `coalition_network`: 3/7 organizations (42.9%) have at least one verified media edge; 2 cross media layers; 1 reach the national-amplification layer.
- `legal`: 8/20 organizations (40.0%) have at least one verified media edge; 4 cross media layers; 3 reach the national-amplification layer.
- `media_information`: 2/5 organizations (40.0%) have at least one verified media edge; 1 cross media layers; 1 reach the national-amplification layer.
- `housing_economic`: 9/23 organizations (39.1%) have at least one verified media edge; 2 cross media layers; 2 reach the national-amplification layer.
- `gender_based`: 3/8 organizations (37.5%) have at least one verified media edge; 0 cross media layers; 0 reach the national-amplification layer.

## Role-pair patterns

Role combinations are multi-label co-memberships. The automated callout below requires at least five organizations in the pair; the CSV retains smaller pairs with `small_n_flag = 1` for audit rather than interpretation.

- `civil_rights_human_rights` + `direct_service`: 7/8 organizations (87.5%) have a verified media edge; 6 are cross-layer and 4 reach national amplification.
- `civil_rights_human_rights` + `legal`: 7/8 organizations (87.5%) have a verified media edge; 4 are cross-layer and 3 reach national amplification.
- `advocacy` + `civil_rights_human_rights`: 10/12 organizations (83.3%) have a verified media edge; 6 are cross-layer and 5 reach national amplification.
- `advocacy` + `legal`: 5/7 organizations (71.4%) have a verified media edge; 3 are cross-layer and 3 reach national amplification.
- `health_wellbeing` + `housing_economic`: 5/8 organizations (62.5%) have a verified media edge; 1 are cross-layer and 1 reach national amplification.
- `community_rooted` + `organizing`: 8/13 organizations (61.5%) have a verified media edge; 4 are cross-layer and 4 reach national amplification.
- `advocacy` + `organizing`: 9/15 organizations (60.0%) have a verified media edge; 5 are cross-layer and 4 reach national amplification.
- `advocacy` + `coalition_network`: 3/5 organizations (60.0%) have a verified media edge; 2 are cross-layer and 1 reach national amplification.

## Interpretation guardrails

1. A verified media edge measures observed visibility in the collected corpus, not the full universe of actual coverage.
2. Search misses, inaccessible archives, and uneven historical platform observability can suppress observed visibility.
3. Multi-label roles are equal-weight memberships. An organization contributes to every verified role it carries, so role-level edge totals are intentionally non-additive.
4. National amplification signals broader circulation, not greater organizational quality, legitimacy, influence, or effectiveness.
5. These tables are descriptive infrastructure. Statistical modeling should wait until outlet/organization audit completeness is coded sufficiently to distinguish an audited zero from an unaudited absence.

## Generated files

- `analysis/role_visibility_summary_v1.csv`
- `analysis/role_pair_visibility_summary_v1.csv`
- `analysis/screening_status_visibility_summary_v1.csv`
- `data/processed/organization_role_media_visibility_v1.csv`
