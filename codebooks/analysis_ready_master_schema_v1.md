# Analysis-Ready Master Schema v1

## Purpose
This schema defines the final row structure for the analysis-ready communication dataset. One row = one organization-owned communication item on one native platform. Website and social-media versions remain separate observations even when matched to the same underlying message.

## Core identifiers
- `item_id` — unique communication-item identifier.
- `org_id` — final analytical organization/unit identifier.
- `organization` — standardized organization name.
- `analysis_inclusion_status` — `include`, `exclude_from_primary_analysis`, `program_level_only`, `duplicate_alias`.
- `sampling_status` — `eligible`, `probably_eligible`, `excluded`, `duplicate_merge`.
- `unit_of_analysis_note` — program-level or organizational restrictions.

## Time
- `date` — publication date where defensibly known.
- `date_precision` — `day`, `month`, `window_only`, `unknown`.
- `date_basis` — `publication_date`, `event_date`, `program_start_date`, `indexed_date`, `other`.
- `week_start` — Monday week start derived only for day-precision dates.
- `month` — YYYY-MM.
- `study_window` — boolean for 2025-11-01 through 2026-03-31.

## Platform and source
- `platform` — standardized: `website`, `linkedin`, `facebook`, `instagram`, `youtube`, `x`, `tiktok`, `threads`, `bluesky`, `other`.
- `platform_family` — `website` or `social`.
- `url` — canonical/native URL if available.
- `content_type` — normalized type such as `news`, `statement`, `event`, `resource`, `newsletter`, `post`, `video`, `fundraising`, `legal_guidance`, `service_update`, `other`.
- `title_or_caption` — source title/caption.
- `source_summary` — collection summary.
- `language` — observed primary language; multilingual allowed.
- `media_type` — `text`, `image`, `video`, `audio`, `mixed`, `unknown`.

## Retrieval and observability
- `retrieval_status` — `verified`, `partial`, `candidate`, `blocked`, `unresolved`, `unavailable`.
- `archive_status` — `complete_or_near_complete`, `partial_archive`, `not_enumerable`, `unknown`.
- `observability_weight_class` — descriptive only: `high`, `medium`, `low`; never used as a statistical weight unless separately justified.
- `capture_date` — date item was collected/verified.
- `collection_notes` — retrieval limitations and provenance.

## Matching and cross-platform correspondence
- `crosspost_group_id` — direct/near-direct crosspost group where available.
- `matched_message_id` — broader same-underlying-message identifier.
- `match_confidence` — `high`, `medium`, `low`, blank if unmatched.
- `adaptation_type` — `identical_crosspost`, `light_adaptation`, `platform_reframing`, `website_expansion`, `social_expansion`, `multimedia_adaptation`, blank.
- `publication_sequence` — within matched set, if known.

## Organizational role
- `org_role_primary` — `advocacy`, `legal`, `service`, `faith`, `ethnocultural`, `media_information`, `economic_development`, `housing`, `education`, `coalition_network`, `hybrid`, `other`.
- `org_role_secondary` — optional second role.
- `role_hybrid_flag` — boolean.

## Situational appraisal coding
Code each 0/1, with multiple appraisals allowed:
- `threat_appraisal`
- `harm_loss_appraisal`
- `injustice_appraisal`
- `uncertainty_appraisal`
- `responsibility_blame_appraisal`
- `intentionality_appraisal`
- `norm_violation_appraisal`
- `vulnerability_appraisal`
- `controllability_appraisal`
- `coping_efficacy_appraisal`
- `collective_efficacy_appraisal`
- `care_need_appraisal`
- `opportunity_hope_appraisal`
- `appraisal_notes`

## Emotion coding
Each emotion is coded on a 0–3 prominence/intensity scale:
- `fear_intensity`
- `anxiety_uncertainty_intensity`
- `anger_intensity`
- `moral_outrage_intensity`
- `grief_sadness_intensity`
- `solidarity_intensity`
- `care_compassion_intensity`
- `empathy_intensity`
- `hope_intensity`
- `gratitude_intensity`
- `pride_intensity`
- `reassurance_intensity`
- `defiance_intensity`
- `urgency_emotion_intensity`
- `other_emotion_intensity`

Intensity scale:
- `0` absent
- `1` low or implicit
- `2` clearly present / moderate
- `3` dominant, highly explicit, or central to the item

Derived later rather than manually coded:
- binary emotion-presence indicators (`*_present = intensity >= 1`)
- `emotional_repertoire_count`
- overall intensity alternatives (mean, max, sum, count)

Additional emotion fields:
- `emotion_explicitness` — `explicit`, `implicit`, `mixed`, `none`.
- `emotion_source_org` — 0/1.
- `emotion_source_affected_public` — 0/1.
- `emotion_source_supporters_public` — 0/1.
- `emotion_source_quoted_actor` — 0/1.
- `emotion_notes` — brief rationale; quotation fragments should remain short.

## Communication function
Multi-label 0/1 fields:
- `function_inform`
- `function_warn`
- `function_reassure`
- `function_regulate_fear`
- `function_mobilize`
- `function_advocate`
- `function_provide_service`
- `function_fundraise`
- `function_build_solidarity`
- `function_generate_empathy`
- `function_moral_evaluation`
- `function_increase_efficacy`
- `function_mourn_commemorate`
- `function_document_testify`
- `function_celebrate`
- `function_encourage_defiance`
- `function_other`

## Action orientation
- `action_orientation_present` — 0/1.
- `action_type` — multi-value normalized list drawn from: `seek_legal_help`, `use_resource`, `attend_event`, `protest`, `contact_official`, `donate`, `volunteer`, `share_information`, `report_incident`, `prepare_documents`, `safety_plan`, `support_business`, `mutual_aid`, `other`.
- `action_specificity` — `none`, `general`, `specific`.
- `action_immediacy` — `none`, `low`, `moderate`, `high`.

## Audience and tone
- `audience_primary` — `immigrants_refugees`, `general_public`, `supporters_donors`, `policymakers`, `service_providers`, `workers`, `faith_community`, `ethnocultural_community`, `media`, `other`.
- `direct_address` — 0/1.
- `urgency_level` — 0–3.
- `legal_information_present` — 0/1.
- `service_information_present` — 0/1.
- `resource_link_present` — 0/1.

## Temporal/event variables
- `event_phase` — `pre_escalation`, `escalation`, `peak`, `sustained_response`, `decline_normalization`, `unknown`.
- `event_marker_primary` — documented event marker if analytically linked.
- `event_marker_distance_days` — item-to-event distance where applicable.

Event phases must be assigned from an external documented chronology, never inferred from emotion.

## Engagement snapshot
Joined by `item_id` where publicly observable:
- `engagement_capture_date`
- `like_or_reaction_count`
- `comment_count`
- `share_or_repost_count`
- `view_count`
- `organization_reply_count`
- `public_reply_count`
- `engagement_visibility_status`
- `engagement_retrieval_status`

Important: missing/hidden engagement is NA, not zero.

## Public uptake aggregates
Derived from interaction-level data:
- `visible_interaction_rows`
- `uptake_validation_count`
- `uptake_gratitude_count`
- `uptake_practical_inquiry_count`
- `uptake_help_request_count`
- `uptake_help_offer_count`
- `uptake_fear_count`
- `uptake_grief_count`
- `uptake_anger_count`
- `uptake_solidarity_count`
- `uptake_hope_count`
- `uptake_contestation_count`
- `uptake_resource_sharing_count`
- `uptake_coordination_count`
- `organization_response_visible` — 0/1/NA.

## Circulation
- `observed_recirculation_minimum` — minimum documented public repost/share traces when official count unavailable.
- `official_repost_share_count_available` — 0/1.
- `tagging_present` — 0/1/NA.
- `cross_org_tagging_present` — 0/1/NA.
- `circulation_notes`.

## Affective conversion
- `conversion_signal_present` — 0/1.
- `conversion_type` — normalized multi-value: `help_seeking`, `help_offering`, `donation`, `volunteering`, `event_attendance`, `protest_participation`, `service_connection`, `resource_referral`, `reporting_documentation`, `other`.
- `conversion_evidence_level` — `none`, `weak`, `moderate`, `strong`; based on observable interaction only, not inferred intention.

## Derived analytical fields
- `emotional_repertoire_count` — number of emotion dimensions with intensity >= 1.
- `overall_emotion_mean` — mean of nonmissing emotion-intensity variables.
- `overall_emotion_max` — maximum emotion intensity in item.
- `overall_emotion_sum` — sum of emotion-intensity variables.
- `appraisal_count` — number of appraisal categories present.
- `function_count` — number of communication functions present.
- `engagement_total_observed` — sum only of metrics actually observed; do not impute hidden values.
- `enforcement_relevance` — coded after collection, never used for inclusion.
- `heightened_enforcement_period` — chronology-based indicator applied after collection.

## Missing-data rules
- Blank/NA means not observed, not retrievable, or not applicable depending on companion status field.
- Numeric zero is used only when the platform explicitly shows zero or complete observation supports zero.
- Never convert hidden comments/shares into zero.
- Month-only records are excluded from weekly analyses but may remain in monthly/descriptive analyses.
- Candidate/unresolved items remain outside strict primary analyses until validated.
