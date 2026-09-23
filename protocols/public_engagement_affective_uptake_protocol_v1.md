# Public Engagement and Affective Uptake Protocol v1

## Purpose

This protocol extends the communication census beyond organizational production to observable public response, recirculation, interpretation, and possible movement toward material or civic action.

The analytical sequence is:

`organizational communication -> public uptake -> affective circulation -> possible conversion into action`

A broader process model is:

`crisis -> organizational communication -> public emotional response -> engagement/recirculation -> collective interpretation -> material or civic action`

The aim is to examine affective intermediation as a relational process rather than a one-way organizational communication process.

## Core conceptual distinctions

### Affective production
What the organization communicates: appraisal, emotional framing, intensity, relational address, information, resources, and calls to action.

### Affective uptake
How publics respond to organizational communication through comments, replies, testimony, questions, emotional expression, agreement, disagreement, requests, offers, or other interaction.

### Affective circulation
How organizational communication travels through sharing, reposting, tagging, linking, quoting, cross-platform recirculation, or references by other actors.

### Affective conversion
Observable movement from expression or interpretation toward action, such as volunteering, attending an event or protest, donating, requesting assistance, offering assistance, reporting an incident, sharing practical resources, connecting another person to help, or coordinating activity.

## Critical measurement rule

**High engagement does not equal high emotion.**

Likes, reactions, comments, shares, reposts, views, and other platform metrics are relational/circulation indicators. They must not be treated as direct measures of emotional intensity or emotional valence.

Emotion must be coded separately from the content and context of posts, comments, replies, and interaction.

A heavily shared informational post may have high circulation and low explicit emotion. A low-engagement post may contain extremely intense emotional communication.

## Unit linkage

Public-response data must be linked to the organizational communication item through `item_id`.

One organizational post may therefore generate:

1. one row in the communication-item corpus;
2. one post-level engagement snapshot row;
3. zero or more comment/reply rows;
4. zero or more recirculation/action evidence rows where observable.

Do not collapse comments into the parent post text.

## Post-level engagement fields

Where publicly observable and technically retrievable, collect:

- `item_id`
- `org_id`
- `platform`
- `post_url`
- `engagement_capture_date`
- `like_or_reaction_count`
- `comment_count`
- `share_or_repost_count`
- `view_count`
- `reaction_breakdown` if the platform publicly exposes reaction types
- `organization_reply_count`
- `public_reply_count`
- `engagement_visibility_status`
- `engagement_retrieval_status`
- `engagement_notes`

If a metric is hidden, unavailable, login-gated, or not supported by the platform, record it as unavailable rather than zero.

## Comment/reply collection

Where publicly accessible, collect comments and reply chains as separate observations.

Recommended fields:

- `interaction_id`
- `item_id`
- `parent_interaction_id`
- `org_id`
- `platform`
- `interaction_type` (`comment`, `reply`, `organization_reply`)
- `interaction_date_time` if visible
- `author_type` (`organization`, `public_user`, `partner_org`, `public_official`, `media`, `unknown`)
- `author_identifier_hash_or_pseudonym`
- `interaction_text`
- `language`
- `contains_tag`
- `tagged_actor_type`
- `contains_external_link`
- `contains_resource_link`
- `retrieval_date`
- `retrieval_status`

Avoid collecting unnecessary personally identifying information. Usernames should not be treated as analytically necessary identifiers unless a public institutional identity matters to the analysis. When possible, pseudonymize or hash ordinary public-user identifiers in processed data.

## Later coding dimensions for public interactions

Do not use these categories to filter collection. They are coding dimensions applied after collection.

### Emotional expression
Possible categories include:

- fear/anxiety
- grief/sadness
- anger/outrage
- solidarity
- gratitude
- hope
- compassion/empathy
- reassurance
- pride
- defiance/resistance
- uncertainty/confusion
- no explicit emotional expression
- other/ambiguous

Multiple emotions may be coded when warranted.

### Interpretive response

- validates organizational framing
- intensifies organizational framing
- challenges/disputes framing
- redirects/reframes issue
- asks for clarification
- provides testimony/personal experience
- supplies additional information
- counters misinformation or contested claim
- other

### Action/coordination indicators

Code observable evidence of:

- request for assistance
- offer of assistance
- request for legal/service information
- resource referral
- donation intent/action
- volunteer intent/action
- event/protest attendance intent/action
- contact-official/civic action
- reporting enforcement or incident information
- transportation/food/housing/material coordination
- connecting another person to services
- tagging an organization/person for help or amplification
- sharing/linking practical resources
- other material or civic coordination

## Organizational response

Capture whether and how the organization replies to public interaction.

Later coding may distinguish organization replies that:

- provide information;
- correct or clarify;
- reassure;
- acknowledge emotion or testimony;
- provide a service/resource referral;
- redirect to private contact;
- encourage participation;
- thank or affirm;
- moderate/de-escalate;
- do not respond.

Organizational response is analytically important because it may represent a second stage of affective intermediation rather than merely audience reaction.

## Recirculation evidence

Where observable, record:

- native platform share/repost count;
- quoted reposts or public reshares when retrievable;
- public posts by partner organizations linking or reposting the item;
- tags of other actors in comments/replies;
- cross-platform references to the same organizational message;
- shared resource links or event links;
- evidence that a message migrated from organization communication into broader network discussion.

Do not infer unseen sharing from engagement counts alone.

## Public-response sampling rule

The communication-item census remains the primary census. For engagement:

- collect post-level engagement metrics for every retrievable social post where public metrics are available;
- collect all publicly retrievable comments/replies when feasible;
- if a platform exposes very large comment volumes that cannot be completely recovered, document the retrieval limit and preserve a transparent sampling rule rather than silently truncating;
- do not preferentially retain only emotional, supportive, hostile, or enforcement-related comments.

If complete comment recovery is technically impossible, later sampling should preserve temporal and conversational structure, including reply chains where possible.

## Temporal caveat

Engagement metrics are dynamic. A count observed on September 22, 2026 is not necessarily the count visible during the original study period.

Therefore every engagement metric must include `engagement_capture_date` and should be interpreted as a later observable accumulation unless contemporaneous archived counts are available.

Do not use present-day engagement counts as if they measured immediate response at publication time.

## Platform comparability caveat

Platforms expose different metrics and interaction architectures. Facebook reactions, Instagram likes, LinkedIn reactions, YouTube views/comments, X reposts/quotes, and TikTok views/shares are not directly equivalent.

Raw engagement counts should therefore be analyzed platform-specifically or normalized only under a clearly justified procedure. Do not create a single universal engagement score by simply adding unlike metrics.

## Ethical safeguards

- Collect only publicly accessible interactions.
- Do not access private groups, private profiles, closed messaging channels, or nonpublic Signal/WhatsApp/Telegram conversations for this dataset.
- Minimize personally identifying data from ordinary commenters.
- Preserve public institutional identity only when analytically relevant.
- Treat comments describing immigration status, legal vulnerability, location, or other potentially sensitive personal circumstances with heightened care in processed/public datasets.
- Raw public comments may require restricted storage or redaction before data sharing.

## Analytical model

The engagement layer enables analysis of:

`organizational expression -> public uptake -> affective circulation -> possible conversion into action`

This supports the proposition that affective intermediation is not only what organizations do with emotion, but also what publics do with organizationally mediated emotion once it enters networked communication.

The empirical analysis should distinguish at least four levels:

1. organizational production;
2. public emotional/interpretive uptake;
3. circulation and recirculation;
4. observable conversion toward material or civic action.

These levels should remain analytically distinct even when they occur within the same interaction thread.
