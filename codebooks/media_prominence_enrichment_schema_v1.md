# Media Prominence Enrichment Schema v1

## Purpose

This schema enriches the existing news-media uptake corpus for network analysis of nonprofit visibility, sourcing, amplification, and second-order affective intermediation.

It is an enrichment layer on the existing verified news corpus, not a new discovery frame.

## Unit of analysis

One row = one organization–news-item relation.

A single news article that includes three sampled organizations therefore contributes three organization–news relations, linked by the same `news_item_id`.

## Core prominence variables

### Mention and sourcing

- `organization_mentioned` — 1 when the organization is substantively identified in the news item.
- `organization_quoted_directly` — 1 when an organizational representative is directly quoted.
- `organization_paraphrased` — 1 when the organization's position, action, information, or claim is paraphrased without a direct quotation.
- `spokesperson_named` — 1 when a named representative is identified.
- `organization_primary_source` — 1 when the organization functions as one of the principal sources or actors structuring the story.
- `organization_headline_or_deck` — 1 when the organization or named representative appears in the headline, deck/subheadline, or equivalent prominent display text.
- `organization_first_third` — 1 when the organization appears in the first third of the article/transcript, where this can be defensibly established.

Do not infer missing placement from snippets or search-result previews.

### Source function

Preserve one primary source function and optional secondary functions:

- `service_expert`
- `legal_expert`
- `affected_community_intermediary`
- `advocacy_source`
- `crisis_response_source`
- `data_information_source`
- `witness_testimonial_source`
- `mobilization_source`
- `institutional_actor`
- `other`

### Outlet characteristics

Join from the canonical news-outlet registry:

- `outlet_id`
- `outlet_type`
- `geographic_scope`
- `priority_tier`

Do not treat outlet priority tier as journalistic quality or ideological value. It records the project's search/audit priority only.

## Prominence weights

Store the component variables separately. A composite score may be derived for visualization but should never replace the underlying measures.

Recommended descriptive prominence score:

`prominence_score = 1*mentioned + 2*paraphrased + 3*direct_quote + 2*spokesperson_named + 3*primary_source + 2*headline_or_deck + 1*first_third`

The score is a transparent analytic convenience for edge weighting, not a measure of organizational influence, legitimacy, effectiveness, or persuasion.

Primary network analyses should also report unweighted relation counts and outlet breadth so conclusions do not depend on one weighting scheme.

## Media-network measures

For each nonprofit organization derive:

- `verified_news_relations` — number of verified organization–news-item relations.
- `distinct_news_items` — number of unique news items.
- `distinct_outlets` — outlet breadth.
- `direct_quote_count`.
- `primary_source_count`.
- `headline_deck_count`.
- `prominence_score_sum`.
- `prominence_score_mean`.
- `outlet_type_diversity` — number of distinct outlet types.

For the bipartite nonprofit–outlet network:

- edge existence = at least one verified organization–outlet relation;
- `relation_count` = number of verified items linking organization and outlet;
- `weighted_prominence` = summed prominence score across those relations;
- `direct_quote_weight` = number of direct-quote relations;
- `primary_source_weight` = number of primary-source relations.

## Second-order affective intermediation variables

For organization-owned items that can be matched to news coverage, preserve:

- `matched_org_item_id`
- `match_confidence`
- `frame_transformation`
  - `preserved`
  - `amplified`
  - `attenuated`
  - `shifted`
  - `contested`
  - `mixed`
  - `not_assessable`
- `legal_info_carryover`
- `service_info_carryover`
- `action_info_carryover`

Where text supports it, code news-level affect separately from organization-level affect. Never copy organization emotion scores directly into the news row.

## Interpretation rules

- Media visibility is not equivalent to public influence.
- Direct quotation does not imply journalistic endorsement.
- More media relations do not mean an organization is more effective or important.
- Search-based recovery is an observed-media-uptake network, not a complete census of all journalism.
- Organizations with no verified relations remain analytically meaningful as zero-observed-uptake cases only when they were actually searched/audited; unknown/unsearched cases must not be coded as zero.
- Syndicated or duplicated versions of the same article should not mechanically inflate prominence.

## Data-enrichment stopping rule

The news-media layer is frozen when:

1. all already-verified primary news relations have the core prominence variables coded;
2. canonical outlet IDs/types are joined;
3. duplicate/syndicated items are reconciled;
4. existing high- or medium-confidence matched organization–news pairs have `frame_transformation` coded where assessable;
5. audited no-coverage and unresolved cases remain documented as such.

After freeze, no broad additional media searching is required for the primary paper. New items are added only to correct a clear omission, resolve a known candidate, or address a reviewer-requested robustness concern.
