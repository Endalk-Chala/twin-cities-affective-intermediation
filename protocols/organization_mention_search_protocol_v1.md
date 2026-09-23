# Organization Mention Search Protocol v1

## Purpose

Ensure that every organization retained in the sampling frame receives a documented, comparable search for communicative visibility across the study window (2025-11-01 through 2026-03-31), without allowing high-visibility organizations to dominate the corpus simply because they are easier to find.

## Core rule

Every organization must receive a mention-search record. A search result is not required to be substantive news coverage. When available, preserve the strongest recoverable evidence while keeping source types analytically distinct.

Do not manufacture coverage. If no mention is found after a documented search, record `searched_no_recoverable_mention_yet` rather than treating the organization as having zero communication or zero visibility.

## Mention evidence hierarchy

For each organization, search for and classify recoverable evidence as one or more of:

1. `substantive_independent_news` — organization is quoted, paraphrased, discussed, or used as a meaningful source.
2. `passing_independent_news_mention` — organization is named but does not substantively shape the story.
3. `national_regional_external_coverage` — substantive or passing coverage outside the Minnesota-local news layer.
4. `community_ethnic_media_mention` — coverage in ethnic, immigrant, faith, neighborhood, or community media.
5. `partner_funder_secondary_reference` — mention in partner, coalition, funder, or institutional commentary that is not independent journalism.
6. `first_party_crisis_communication` — organization-owned website, social, newsletter, statement, event, toolkit, resource, or campaign communication.
7. `government_or_directory_reference` — government listings, service directories, grant/resource pages, licensing lists, or official registries.
8. `out_of_window_context` — substantively relevant mention outside the fixed study period.
9. `date_unresolved_candidate` — substantive item whose publication date cannot be verified sufficiently for primary temporal analysis.
10. `searched_no_recoverable_mention_yet` — documented search completed but no usable mention recovered.

## Balanced search requirement

Search effort should be distributed across the sampling frame rather than proportional to prior visibility. Each organization should receive, at minimum:

- exact-name search;
- alias/acronym search where relevant;
- leader/spokesperson search where known;
- crisis-term combination search;
- local Minnesota/Twin Cities news search;
- community/ethnic/specialized outlet search where appropriate;
- national/regional search;
- first-party website search;
- targeted social/platform search when available.

Additional searching can follow evidence, but the minimum pass should be comparable across organizations.

## Evidence preservation

For each recovered mention, preserve when available:

- organization ID and canonical name;
- date;
- outlet/source;
- source scale: local, Minnesota-regional, national, non-Minnesota regional, community/ethnic, first-party, partner/funder, government/directory;
- headline/title;
- canonical URL;
- author/byline;
- mention type;
- whether the organization is quoted;
- spokesperson;
- short text fragment or paraphrase sufficient for later qualitative analysis;
- crisis/topic relevance;
- study-window status;
- syndication/duplicate status;
- verification notes.

## Interpretation rule

A lack of substantive news coverage is not equivalent to lack of organizational communication. The design must preserve distinctions among organizational activity, journalistic uptake, secondary institutional visibility, and recoverability.

The analytical corpus may later be filtered by evidence class, but the collection layer should retain these weaker forms of visibility so that organizations with limited press access are not erased from the dataset.
