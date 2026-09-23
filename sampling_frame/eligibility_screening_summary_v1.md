# Eligibility Screening Summary v1

## Scope

The consolidated discovery frame contains **138 raw records** drawn from the original 84-record seed registry plus four discovery batches.

During screening, two non-independent records were identified:

1. **Navigate MN** is the former name of **Unidos MN** and should be merged with TC075.
2. **Monarca** appears to function as a program/initiative associated with **Unidos MN** rather than a separate organizational unit; preserve Monarca-branded communication as program-level material if verified, but do not count it as a separate organization.

This yields a current **deduplicated working universe of 136 distinct candidate organizational/program/network units** before resolving provisional cases.

## Screening outcomes across all 138 raw records

| Outcome | Raw records | Meaning |
|---|---:|---|
| Eligible | 91 | Meets current geography, population/mission, organizational-form, and study-period existence criteria |
| Probably eligible / verification needed | 23 | Plausible inclusion but requires one or more targeted checks |
| Excluded | 22 | Fails a defined criterion such as geography, organizational form, population relevance, or current program existence |
| Duplicate / alias / program merge | 2 | Do not count as independent organizational units |
| **Total** | **138** | Raw screening frame |

The operational communication-census universe therefore contains **114 eligible or probably eligible units (91 + 23)**. The 22 excluded records and 2 duplicate/alias/program-merge records remain in the audit trail but are not treated as independent units in the communication census.

## Important methodological rule

**Public communication availability is not an organizational eligibility criterion.**

The screening process intentionally separates:

1. **Organizational universe eligibility** — Is the organization/program/network a relevant Twin Cities immigrant/refugee or identifiable immigrant-origin civil-society actor?
2. **Communication availability** — Did it maintain an official website and/or official social-media account during the study period (**November 1, 2025–March 31, 2026**), and is study-period content retrievable?
3. **Content characteristics** — What did the organization communicate during the study period, including routine services, culture, fundraising, organizational updates, legal advocacy, crisis response, events, resources, newsletters, videos, and other dated public communication?
4. **Analytical coding** — After census construction, how do communication items vary in appraisal, emotion, intensity, function, action orientation, time, organizational role, and platform?

This prevents the sampling frame from being defined by the dependent phenomena of interest, such as whether an organization publicly communicated about immigration enforcement or used emotionally intense language.

## Communication-platform audit

For every eligible and probably eligible unit, maintain a platform registry with fields sufficient to distinguish account existence from archive retrievability. Relevant fields include:

- `org_id`
- `organization_name`
- `unit_of_analysis`
- `official_website`
- `website_active_study_period`
- `website_archive_or_news_section`
- `facebook_url`
- `instagram_url`
- `linkedin_url`
- `x_url`
- `youtube_url`
- `tiktok_url`
- `other_platform_url`
- `official_account_verified`
- `platform_active_study_period`
- `study_period_content_retrievable`
- `earliest_retrievable_study_period_date`
- `latest_retrievable_study_period_date`
- `retrieval_method`
- `archive_or_capture_notes`
- `communication_completeness_rating`

A verified account with an inaccessible or incompletely indexed historical archive must be recorded as `partial_archive` or an equivalent retrieval limitation; zero retrieved posts must not be interpreted as organizational silence.

## Communication-item unit

The emotion analysis should operate primarily at the **communication-item level** (post, webpage, statement, press release, video caption, newsletter item, etc.), not by labeling an organization itself as emotional.

Each included item can later be coded for:

- explicit and implicit emotional cues
- attributed emotion versus organizational voice
- appraisal dimensions (threat, injustice, responsibility, vulnerability, controllability, coping potential, etc.)
- emotion categories (fear, anxiety, anger, moral outrage, sadness/grief, compassion, empathy, hope, solidarity, care, reassurance, pride, defiance)
- emotional intensity (0–3 or another documented scale established through pilot coding)
- emotional function (mobilize, warn, reassure, regulate fear, build solidarity, generate empathy, moral evaluation, increase efficacy/control, comfort, resistance/defiance)
- action orientation (seek services, know rights, prepare, donate, volunteer, protest, contact officials, share information, support affected people, report enforcement activity, civic participation, etc.)

Cross-platform duplicates should remain separate observations and be linked through `crosspost_group_id` or `matched_message_id` so later analysis can compare platform adaptation without losing platform-specific exposures.

## Current methodological checkpoint — September 22, 2026

The project has moved beyond initial eligibility screening into full communication-census construction. The website census is substantively closed for the core TC001–TC084 registry, subject to ordinary QC and newly discovered omissions. Social-media census work is active across the 114 eligible/probably eligible universe, with official account identification and historical-post retrieval proceeding in parallel.

Current priorities are:

1. expand the social platform registry across all 114 eligible/probably eligible units;
2. collect all defensibly retrievable public social-media communication from **November 1, 2025 through March 31, 2026** without relevance or emotion filtering;
3. document partial archives and inaccessible historical platform records;
4. preserve unresolved candidates separately from verified items;
5. build website-social matched-message sets where the same underlying event or message appears across channels;
6. reconcile website and social data before emotional coding begins.
