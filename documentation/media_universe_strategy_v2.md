# Media Universe Strategy v2

## Purpose
The news-media layer should capture not only whether sampled nonprofits appeared in news coverage, but how their visibility traveled across different parts of the media ecosystem during the fixed study window: **2025-11-01 through 2026-03-31 inclusive**.

The media universe is intentionally broader than a Twin Cities mainstream-news list. It is organized as a layered communication infrastructure.

## Layer 1: Community and ethnic media
Includes neighborhood, Black, Hmong, Somali, Latino/Spanish-language, African immigrant, Jewish, Native, multilingual community radio, and other community-rooted outlets.

Analytical purpose:
- identify organizations visible within community publics even when absent from major metro news;
- capture language/cultural proximity and resource routing;
- avoid treating mainstream-news absence as communicative invisibility;
- trace community-specific affective and practical frames.

## Layer 2: Local and regional media
Includes major Twin Cities television, metro newspapers, Minnesota public media, nonprofit state/local digital newsrooms, and metro newsletters.

Analytical purpose:
- identify recurring public sources during the crisis;
- compare legal, service, advocacy, witness, faith, and community-intermediary roles;
- measure prominence through observable components such as headline/lead presence, quotation, paraphrase, and primary-source status.

## Layer 3: National amplification
Includes wire services, national public media, major national newspapers, television/digital networks, and selected nonprofit national newsrooms.

Analytical purpose:
- trace when Minnesota organizations, spokespersons, events, or frames travel beyond the local media system;
- distinguish direct national sourcing from syndication of local/wire reporting;
- identify local-to-national amplification pathways rather than assuming national coverage is inherently more important.

## Search protocol
For each sampled organization, searches should combine:
1. canonical organization name;
2. common aliases/acronyms;
3. named spokespersons where known;
4. crisis terms (ICE, immigration enforcement, Operation Metro Surge, refugee, asylum, deportation, detention, immigration raid, federal agents, benefits, legal help, food, housing, protest, vigil, fundraiser, mutual aid);
5. outlet-specific searches across all three layers.

Each organization receives an auditable status:
- `verified_coverage`;
- `coverage_candidate_date_unresolved`;
- `coverage_candidate_nonlocal_or_secondary`;
- `searched_no_verified_coverage_yet`;
- `not_yet_fully_audited`.

Search misses must never be converted into zero coverage.

## Story architecture enabled by this design
This infrastructure permits several analyses:

### Source visibility
Which organizations become named, quoted, paraphrased, or primary sources?

### Role differentiation
Which organizations become legal experts, service intermediaries, advocates, community representatives, witnesses, mobilizers, or resource routers?

### Media-layer inequality
Are some organizations visible only in community media while others receive metro or national amplification?

### Cross-layer amplification
When a local/community frame travels nationally, what is preserved, attenuated, shifted, or amplified?

### Affective visibility
Which affective vocabularies attach to organizations through their own quotations versus journalist narration?

### Practical uptake
Which media layers carry legal guidance, safety information, fundraising, service routing, mobilization, or other action pathways?

## Planned network outputs
- organization × outlet bipartite network;
- organization × media-layer network;
- organization × source-role network;
- organization × affect-term network;
- affect-term co-occurrence network;
- local-to-national amplification paths;
- temporal network snapshots by crisis phase.

## Important limits
- Outlet inclusion defines a search universe, not proof of exhaustive capture.
- Syndicated copies should be separated from original reporting.
- Visibility is not equivalent to influence, endorsement, or public agreement.
- Community/ethnic media should not be treated as lower-value residual sources.
- Composite prominence scores should be derived only after inspecting the distribution and validity of the underlying visibility indicators.
