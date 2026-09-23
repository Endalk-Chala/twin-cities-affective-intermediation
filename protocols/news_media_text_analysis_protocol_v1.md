# News-Media Text Analysis Protocol v1

## Purpose

This protocol extends the news-media uptake layer from a coverage audit into a **linked textual corpus** suitable for qualitative text analysis, discourse analysis, narrative analysis, and mixed-method comparison.

The key methodological shift is that a verified article URL is not itself the analytical evidence. For each verified organization-news relation, the project should preserve a structured, auditable representation of the **relevant text** through which the organization becomes visible, quoted, paraphrased, narrated, or transformed by journalism.

The text layer remains subordinate to the core theoretical contribution of **affective intermediation**. It is designed to show how organizational interpretations of crisis and community experience are selected and recirculated through journalism as a second-order intermediary layer.

## Linked corpus architecture

The study should maintain three analytically distinct but linkable levels:

1. **Organization-owned communication** — website posts, statements, social-media posts, resource pages, press releases, videos or other first-party communication.
2. **News-media uptake** — independent reporting that mentions, quotes, paraphrases, contextualizes or otherwise incorporates an organization.
3. **Text segments** — the specific passages within organization-owned or news texts that carry the relevant appraisal, affect, narrative role, practical information, or action pathway.

Recommended relation:

`organization -> organization_item -> news_item -> organization_news_relation -> text_segment`

Not every relation will have a matched organization-owned item. When no reliable first-party match exists, text analysis can still be conducted within the news item, but frame-transformation claims should be coded `not_assessable` rather than inferred.

## Unit of textual analysis

One row in the text-segment table = one analytically meaningful segment associated with one organization-news relation.

A segment may be:
- a short direct quotation from an organization representative;
- a journalist paraphrase explicitly attributed to the organization or spokesperson;
- journalist narration describing the organization’s role, actions or effects;
- a practical resource/action statement carried into the story;
- a short matched passage from an organization-owned item used for comparison.

Segments should be long enough to preserve meaning but short enough to remain focused and auditable. Do not archive entire copyrighted articles in the public repository. Store only brief quotation fragments where necessary, plus paraphrase/analytic memo fields and canonical URLs.

## Required fields

### Identification
- `text_segment_id`
- `news_item_id`
- `org_id`
- `organization`
- `source_type` (`news`, `organization_owned`)
- `source_url`
- `source_date`
- `speaker_or_voice`

### Text form
- `text_relation_type`
  - `direct_quote`
  - `attributed_paraphrase`
  - `journalist_narration`
  - `resource_or_action_text`
  - `headline_or_deck`
  - `organization_owned_text`
- `short_quote_fragment` — brief audit quotation only when necessary
- `researcher_paraphrase` — substantive summary in the researcher’s own words

### Affective-intermediation coding
- `affect_code`: fear/anxiety; anger/moral outrage; grief; solidarity; care/compassion; hope; reassurance; defiance; urgency; mixed; none_explicit
- `appraisal_code`: threat/danger; institutional abandonment; rights violation; vulnerability; collective efficacy; community care; resource scarcity; uncertainty; safety/protection; other
- `intermediation_function`: interpret; translate; validate; reassure; educate; provide_resources; mobilize; coordinate; witness; advocate; fundraise; route_services; other
- `source_function`: service_expert; legal_expert; affected_community_intermediary; advocacy_source; crisis_response_source; data_information_source; witness_testimonial_source; institutional_actor; other

### Narrative/discourse coding
- `narrative_role`
  - `problem_definition`
  - `causal_explanation`
  - `human_consequence`
  - `moral_evaluation`
  - `response_solution`
  - `collective_identity`
  - `agency_resistance`
  - `resource_pathway`
  - `background_context`
  - `other`
- `actor_positioning`: how the organization/community is positioned (expert, victim, protector, advocate, service provider, mobilizer, witness, etc.)
- `discursive_shift`: whether the journalistic text preserves, intensifies, attenuates, proceduralizes, individualizes, collectivizes, contests or otherwise shifts the organizational frame
- `analytic_memo`

## Recommended analytic strategy

### Stage 1: Descriptive uptake analysis
Establish which organizations become visible, how often, in which outlet types, and through which source functions. This is the coverage/visibility layer and should not be conflated with textual meaning.

### Stage 2: Qualitative content analysis
Code the text segments for affect, appraisal, intermediation function, source function and action/resource carryover. This allows structured comparison across organization types and outlet types.

### Stage 3: Narrative/discourse analysis
Use purposive subsets of high-information cases to examine how stories construct:
- the crisis and its causes;
- affected communities;
- nonprofit authority and legitimacy;
- fear, care, solidarity, urgency and resistance;
- institutional responsibility;
- pathways from emotion/appraisal to practical action.

This stage should focus on **how meaning is organized**, not simply word frequencies.

### Stage 4: Matched-message transformation analysis
Where an organization-owned item can be confidently matched to a news item, compare the two texts to assess whether the organizational frame is preserved, amplified, attenuated, shifted, contested or mixed.

This is the strongest direct test of **second-order affective intermediation**.

## Methodological recommendation

The project should describe the overall design as a **longitudinal comparative mixed-method communication study with linked qualitative text analysis**, rather than choosing only one label such as discourse analysis or narrative analysis for the entire project.

The empirical workflow combines:
1. systematic communication collection;
2. news-media uptake/visibility auditing;
3. linked text-segment coding;
4. qualitative content analysis across the corpus;
5. focused narrative/discourse analysis of theoretically important cases;
6. matched organization-news comparison where evidence permits.

This layered design is preferable because the project asks both **distributional questions** (who gets covered, where, how often, in what role) and **meaning questions** (what affective frames and interpretations survive, change, or disappear in journalistic recirculation).

## Copyright and reproducibility rule

The public repository should not store full copyrighted news articles. Reproducibility should rely on:
- article metadata and canonical URL;
- publication date/outlet/byline;
- brief quotation fragments only when analytically necessary;
- researcher paraphrases;
- structured coding;
- analytic memos;
- archived/access notes where lawful and appropriate.

A private research workspace may preserve additional notes needed for analysis, subject to copyright, licensing and institutional requirements.

## Interpretation limits

- Absence from retrieved coverage is not proof of no media coverage.
- News quotation is not equivalent to endorsement.
- A journalist’s paraphrase is analytically distinct from an organization’s own words.
- Textual prominence does not establish audience reception or persuasion.
- Word frequency alone should not be treated as affective intensity.
- Narrative/discourse claims should be grounded in textual patterns and selected cases, not inferred from metadata alone.
