# Analysis Freeze and Handoff Protocol v1

## Goal

Move the project quickly from collection to analysis and writing without allowing data collection to remain open-ended.

## Version 1 stopping rule

Freeze the first analysis corpus once every retained sampling-frame organization has received a documented minimum search pass across the relevant layers:

1. organization name and aliases;
2. known leader/spokesperson names where available;
3. local Minnesota/Twin Cities news;
4. community/ethnic/specialized media where relevant;
5. national or non-Minnesota regional media;
6. first-party website communication;
7. targeted social/platform evidence when recoverable;
8. crisis-term combinations covering the fixed study window, 2025-11-01 through 2026-03-31.

Organizations may have very different numbers of resulting items. The stopping rule applies to search effort, not to number of mentions.

## Freeze statuses

- `v1_ready_verified`: minimum search completed; at least one verified in-window evidence item recovered.
- `v1_ready_no_verified_item`: minimum search completed; no verified in-window item recovered.
- `v1_ready_context_only`: minimum search completed; only out-of-window, date-unresolved, directory, funder/partner, or other contextual evidence recovered.
- `needs_minimum_pass`: organization still requires one or more minimum search layers.

## Analysis-ready outputs

### 1. organization_analysis_master_v1.csv
One row per organization.

Core fields:
- org_id
- organization
- organization_type
- geography
- minimum_search_complete
- freeze_status
- verified_local_news_n
- verified_national_external_n
- verified_community_ethnic_media_n
- first_party_items_n
- secondary_reference_n
- top_1_type / top_1_source / top_1_date / top_1_summary
- top_2_type / top_2_source / top_2_date / top_2_summary
- top_3_type / top_3_source / top_3_date / top_3_summary
- local_to_national_bridge_flag
- analysis_priority

### 2. media_item_master_v1.csv
One row per organization-story relation, preserving story-level deduplication keys.

Core fields:
- news_item_id
- story_id
- org_id
- organization
- date
- outlet
- source_scale
- outlet_type
- headline
- canonical_url
- author
- organization_visibility
- organization_quoted
- spokesperson
- source_function
- news_topic
- local_national_layer
- matched_org_item_id
- match_confidence
- frame_transformation
- affective_frame
- action_carryover
- legal_info_carryover
- service_info_carryover
- collection_status
- syndication_group

### 3. local_national_bridge_v1.csv
One row per organization with evidence at more than one communication scale.

Core fields:
- org_id
- organization
- owned_item_id
- local_news_item_id
- national_news_item_id
- bridge_type
- local_role
- national_role
- frame_preserved
- frame_amplified
- frame_attenuated
- frame_shifted
- individualized
- collectivized
- politicized
- proceduralized
- action_pathway_preserved
- notes

### 4. qualitative_text_corpus_v1.csv
A text-focused corpus for later discourse/narrative analysis.

Core fields:
- text_id
- org_id
- source_item_id
- source_layer
- date
- source/outlet
- speaker/author
- text_type
- short_relevant_excerpt
- paraphrase
- affective_terms
- action_language
- community_reference
- institutional_reference
- coding_notes

## Immediate analysis sequence after freeze

1. Descriptive visibility by organization and source scale.
2. Local vs national uptake comparison.
3. Organization role comparison: service provider, legal expert, affected-community intermediary, advocacy source, mobilization actor, witness/testimonial, institutional actor.
4. Affective-frame distribution and transformation.
5. Action-information carryover.
6. Matched-message analysis: owned communication -> local news -> national news.
7. Focused narrative/discourse analysis of theoretically rich cases.

## Writing handoff

Once Version 1 outputs are built, analysis should begin immediately. New evidence found after the freeze can be logged as `v2_candidate` rather than reopening Version 1. This preserves a stable empirical base for tables, figures, interpretation, drafting and submission.
