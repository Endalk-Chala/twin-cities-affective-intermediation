# Organizational Typology v2

## Purpose

This typology supports comparative analysis of how different Twin Cities immigrant/refugee-serving and immigrant-origin civil-society organizations mediate affect during crisis communication. It is designed for the fixed 114-unit operational universe and must not be used as an eligibility filter.

The typology is **multi-dimensional**. Organizations may occupy more than one functional and constituency position. A single mutually exclusive label would erase analytically important hybrids.

## Core analytical distinction

The study preserves three theoretically central organizational positions:

1. **Ethnocultural / community-rooted** organizations
2. **Advocacy / rights / organizing** organizations
3. **Service-provider** organizations

These are not assumed to be mutually exclusive. Hybrid organizations are expected and analytically valuable.

## Dimension A — Primary organizational role

Assign one `org_role_primary` based on the organization's dominant publicly stated institutional function during the study period.

Allowed values:

- `advocacy`
- `legal`
- `service`
- `faith`
- `ethnocultural`
- `media_information`
- `economic_development`
- `housing`
- `education`
- `coalition_network`
- `hybrid`
- `other`

Use `hybrid` only when no single role is defensibly dominant. Otherwise assign the best-supported primary role and use secondary-role fields.

## Dimension B — Secondary roles

Use separate binary fields rather than one free-text secondary label:

- `role_advocacy`
- `role_legal`
- `role_direct_service`
- `role_faith`
- `role_ethnocultural`
- `role_media_information`
- `role_economic_development`
- `role_housing`
- `role_education`
- `role_coalition_network`

These fields capture organizational hybridity explicitly.

## Dimension C — Community rootedness

`community_rootedness`:

- `0_not_identifiable` — no clear immigrant/refugee or ethnocultural constituency embeddedness beyond service targeting.
- `1_population_serving` — explicitly serves immigrant/refugee populations but is not evidently constituted by a specific community.
- `2_community_anchored` — strong ongoing organizational identification with one or more immigrant-origin communities.
- `3_community_constituted` — organization is substantially formed, governed, represented, or publicly identified as an institution of a specific immigrant-origin/ethnocultural community.

This variable should not be inferred solely from an organization's name. Use mission, governance, history, self-description, constituency, and program evidence.

## Dimension D — Advocacy intensity

`advocacy_orientation`:

- `0_none_or_incidental`
- `1_supportive` — occasional rights information, referrals, public education, or coalition participation.
- `2_regular` — recurring advocacy, policy communication, public accountability, organizing, or civic engagement.
- `3_core_mission` — advocacy, rights defense, organizing, campaigning, or policy change is a central institutional purpose.

Advocacy intensity is an organizational characteristic, not an item-level emotion score.

## Dimension E — Service intensity

`service_orientation`:

- `0_none_or_incidental`
- `1_referral_or_limited`
- `2_regular_direct_service`
- `3_core_mission_direct_service`

Direct service includes recurring material, legal, health, employment, education, housing, resettlement, navigation, food/basic-needs, or similar assistance delivered to clients/community members.

## Dimension F — Constituency breadth

`constituency_scope`:

- `specific_ethnocultural`
- `multiethnic_immigrant_refugee`
- `racialized_panethnic`
- `issue_based_immigrant`
- `general_population_with_immigrant_program`
- `faith_constituency`
- `other`

Where useful, add `constituency_notes` for named communities/languages.

## Dimension G — Institutional form

`institutional_form`:

- `nonprofit_organization`
- `community_association`
- `legal_services_org`
- `faith_based_org`
- `congregational_program`
- `coalition`
- `network`
- `mutual_aid_or_volunteer_network`
- `program_within_parent_org`
- `media_or_information_org`
- `other`

This field is analytically separate from function. For example, a coalition may primarily advocate; a faith-based organization may primarily provide services.

## Dimension H — Crisis-position hypothesis

This is a **descriptive organizational-position variable**, not an outcome and not a fixed claim about communication.

`crisis_position`:

- `proximate_community_intermediary` — institution embedded in communities directly exposed to crisis consequences.
- `rights_accountability_intermediary` — institution primarily positioned to interpret rights, law, power, policy, or accountability.
- `service_stabilization_intermediary` — institution primarily positioned to maintain services, resources, navigation, or material stability.
- `mobilization_intermediary` — institution primarily positioned to organize collective action.
- `institutional_bridge` — institution routinely connects immigrant/refugee publics to mainstream institutions, systems, or resources.
- `multi_position` — more than one position is central.

This field can later be tested against observed communication rather than used to predetermine it.

## Recommended comparison variables

For the main article, derive three nonexclusive indicators:

- `community_rooted_indicator = 1` when community rootedness >= 2 or ethnocultural role is present.
- `advocacy_indicator = 1` when advocacy orientation >= 2 or advocacy/legal organizing is core.
- `service_provider_indicator = 1` when service orientation >= 2.

Then derive an overlap pattern:

- `community_only`
- `advocacy_only`
- `service_only`
- `community_advocacy`
- `community_service`
- `advocacy_service`
- `community_advocacy_service`
- `other_or_unclassified`

This overlap variable is preferable to forcing organizations into a single mutually exclusive category.

## Why the overlap model matters theoretically

The study's concept of **affective intermediation** assumes that organizational position may shape what happens between crisis conditions and public communication.

A community-rooted organization may have greater exposure to community fear, grief, anger, solidarity, or practical uncertainty. A direct-service organization may be institutionally pushed toward reassurance, coping efficacy, resource provision, and stabilization. An advocacy organization may be positioned to translate affect into injustice claims, accountability, collective efficacy, protest, or policy demands.

These are hypotheses for empirical comparison, not coding assumptions. Communication items must still be coded from observable content only.

## Coding evidence hierarchy

Prefer, in order:

1. official mission/about/history/governance pages;
2. program descriptions and annual reports;
3. study-period public communication showing stable institutional function;
4. credible external descriptions when official material is incomplete.

Do not classify solely from one crisis post or from the emotional tone of communication.

## Reliability rule

For each organization, preserve:

- `typology_evidence_url`
- `typology_evidence_excerpt_or_summary`
- `typology_coder`
- `typology_date_checked`
- `typology_confidence` (`high`, `medium`, `low`)
- `typology_notes`

Low-confidence cases should remain revisable during QC.

## Relationship to item-level coding

Organizational typology and communication-item coding must remain separate tables linked through `org_id`.

Do not encode organizational type into emotional-intensity judgments. For example, advocacy organizations should not be presumed angrier, and service organizations should not be presumed reassuring. The purpose of the typology is to test whether such communication patterns emerge empirically.
