# Organization–News Relation Codebook v1

## Unit of analysis
One row = one verified relationship between one sampled organization and one news item.

This bridge table is the backbone of source-visibility analysis. A single story that includes three sampled organizations generates three relation rows. Story-level metadata belongs in the news-item table; organization-specific visibility and framing belong here.

## Core identifiers
- `relation_id`: unique relation key.
- `news_item_id`: joins to the raw/master news-item table.
- `org_id`: joins to the nonprofit sampling frame.
- `outlet_id`: joins to `platform_registry/news_outlet_registry_v2.csv`.

## Visibility variables
- `visibility_type`: `headline`, `lead`, `direct_quote`, `paraphrase`, `named_mention`, `resource_listing`, `beneficiary_or_partner`, `passing_mention`, `other`.
- `headline_presence`: 1/0.
- `lead_presence`: 1/0, organization appears in headline deck or opening paragraph/segment.
- `direct_quote`: 1/0.
- `quote_count`: count of distinct direct quotation segments attributable to the organization or named spokesperson.
- `paraphrased`: 1/0.
- `spokesperson_named`: 1/0.
- `spokesperson_name`: exact public name when available.
- `spokesperson_title`: exact title when available.
- `source_prominence`: `primary`, `secondary`, `supporting`, `passing`, `resource_only`.

Do not construct a composite prominence score in the raw relation table. Preserve observable components first.

## Source-function variables
`source_function_primary`:
- `service_expert`
- `legal_expert`
- `affected_community_intermediary`
- `advocacy_source`
- `crisis_response_source`
- `data_information_source`
- `witness_testimonial_source`
- `institutional_actor`
- `mobilization_source`
- `fundraising_source`
- `resource_router`
- `faith_community_source`
- `other`

`source_function_secondary` may contain a second role when analytically necessary.

## Uptake-function variables
Binary fields capture what the story does with the organization's communication:
- `substantive_interpretation`
- `resource_routing`
- `mobilization_uptake`
- `fundraising_uptake`
- `service_uptake`
- `legal_information_uptake`
- `safety_guidance_uptake`
- `testimonial_uptake`

These are not mutually exclusive.

## Affective/framing fields
- `org_affect_terms`: semicolon-separated terms attributable to organizational quotation/paraphrase only.
- `journalist_affect_terms`: semicolon-separated terms supplied by journalist narration in the organization's immediate context.
- `dominant_affect`: `fear_anxiety`, `anger_moral_outrage`, `grief`, `solidarity`, `care_compassion`, `hope`, `reassurance`, `defiance`, `urgency`, `mixed`, `none_not_assessable`.
- `frame_transformation`: `preserved`, `amplified`, `attenuated`, `shifted`, `contested`, `mixed`, `not_assessable`.

Keep organizational and journalistic affect separate so later emotive-word networks do not falsely attribute newsroom language to the nonprofit.

## Geographic amplification
- `media_layer`: inherited from outlet registry: `community_ethnic`, `local_regional`, or `national_amplification`.
- `local_to_national_amplification`: 1 when the same organization/event/message can be linked to a national outlet after local/community visibility.
- `amplification_path_id`: optional identifier for linked coverage chains.

## Matching and provenance
- `matched_org_item_id`: organization-owned message/event identifier when available.
- `match_confidence`: `high`, `medium`, `low`, blank if no item-level match attempted.
- `evidence_fragment`: short audit-only quotation fragment; avoid long copyrighted text.
- `verification_status`: `verified`, `candidate`, `excluded`.
- `coder_notes`: concise reasoning, including ambiguity or resource-only cases.

## Interpretation rules
1. Visibility is not equivalent to endorsement or persuasion.
2. Resource-directory inclusion counts as uptake only when the organization is explicitly routed to as a usable resource; keep it analytically distinct from substantive interpretation.
3. National pickup does not automatically indicate greater influence; it indicates broader media circulation.
4. Syndicated copies should not be treated as independent original reporting, but may be retained in a separate circulation table if syndication reach is analyzed.
5. Search failure is not evidence of zero coverage.
6. Community and ethnic media are analytically co-equal parts of the communication infrastructure, not residual outlets after mainstream searches.
