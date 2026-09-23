# News-Media Uptake Protocol v1

## Purpose

This protocol extends **Affective Intermediation in Twin Cities Nonprofit Communication** beyond organization-owned communication and social-media engagement to include **news-media uptake** within the local communication infrastructure.

News coverage is not treated as equivalent to public comments or reactions. Journalism is modeled as a distinct intermediary layer that can select, quote, paraphrase, contextualize, amplify, attenuate, contest, or reframe nonprofit communication before it reaches wider publics.

## Conceptual role

The extended process is:

`crisis/context -> community affect + organizational exposure -> organizational interpretation -> affective intermediation -> organizational communication -> uptake pathways -> circulation -> possible conversion/action`

Uptake pathways are analytically separated into:

1. **Networked public uptake** — comments, replies, reactions, shares/reposts, help seeking, help offering, contestation, coordination.
2. **News-media uptake** — local news mentions, quotations, paraphrases, sourcing, framing, and recirculation of nonprofit communication.

News media may therefore constitute a form of **second-order intermediation**: nonprofit organizations first interpret and translate community experience; journalists may then select and transform those organizational interpretations for broader public circulation.

## Unit of analysis

One row = one local news item published during the study window that meaningfully mentions, quotes, cites, or discusses at least one organization in the nonprofit sampling frame, or that can be confidently matched to an organization-owned communication item/event.

A news story mentioning multiple organizations remains one news-item row in the raw news table, with organization-story relations stored in a bridge table when needed.

## Study window

The news-media corpus uses the same temporal boundaries as the primary nonprofit communication corpus:

**2025-11-01 through 2026-03-31 inclusive.**

Only news items published within this window belong in the primary analytical news-media dataset. Coverage published before November 1, 2025 or after March 31, 2026 is excluded from the paper's primary news-media analysis, even when it retrospectively discusses the study-period crisis.

This rule keeps organizational communication, social-media uptake, news-media uptake, temporal phases, and crisis chronology analytically congruent.

## News ecosystem scope

Primary focus: Twin Cities and Minnesota local/regional news ecosystem.

Potential outlet classes:
- major metro newspapers;
- public radio/public television;
- local television news;
- nonprofit/local digital newsrooms;
- ethnic/immigrant/community media;
- neighborhood/community news outlets where retrievable.

Outlet inclusion should be documented in an outlet registry rather than improvised during analysis.

## Discovery strategy

Search by:
- organization name and known aliases;
- executive director/spokesperson names where relevant;
- key campaign/event names;
- matched nonprofit communication titles/phrases;
- immigration-enforcement crisis terms combined with organization names;
- site-specific searches for selected local outlets.

Discovery should be broad and reproducible. Search misses are not evidence that no coverage existed.

## Core coding dimensions

### 1. Organization visibility
- organization mentioned;
- organization quoted directly;
- organization paraphrased;
- spokesperson named;
- organization appears in headline/deck;
- organization is primary source vs secondary source vs passing mention.

### 2. Source function
Code how the organization functions in the story:
- service expert;
- legal expert;
- affected-community intermediary;
- advocacy source;
- crisis-response source;
- data/information source;
- witness/testimonial source;
- institutional actor;
- other.

### 3. Affective uptake
Code whether the news item carries forward organizationally mediated affect:
- fear/anxiety;
- anger/moral outrage;
- grief;
- solidarity;
- care/compassion;
- hope;
- reassurance;
- defiance;
- urgency.

These should be coded from the news text itself, distinguishing journalist narration from organization quotation.

### 4. Framing transformation
For matched organization-news pairs, code the relationship between the organization-owned message and the news representation:
- `preserved` — core emotional/appraisal frame substantially retained;
- `amplified` — emotional/appraisal intensity or prominence increased;
- `attenuated` — emotional/appraisal intensity reduced or proceduralized;
- `shifted` — dominant frame moves to a substantively different appraisal/function;
- `contested` — news item explicitly challenges or counterbalances the organization's framing;
- `mixed` — more than one transformation occurs;
- `not_assessable` — insufficient match or text.

### 5. Information/action carryover
Code whether the news item carries forward:
- legal information;
- service/resource information;
- safety guidance;
- donation/volunteer request;
- event/protest information;
- contact/reporting instructions;
- other action pathway.

### 6. Match to organization-owned communication
Where possible, link news coverage to one or more organization-owned items using:
- same event/topic;
- same spokesperson/quotation;
- same distinctive factual claim;
- same resource/campaign;
- temporal proximity;
- direct hyperlink/reference.

Match confidence:
- `high` — direct quote/link or unmistakable same message/event;
- `medium` — strong topical and temporal correspondence with several matching features;
- `low` — plausible but uncertain relationship;
- blank — no item-level match attempted.

## Evidence rules

- Preserve only short quotation fragments necessary for auditability.
- Store canonical article URL, outlet, headline, date, author/byline where available.
- Distinguish organization-authored claims from journalist narration.
- Do not infer organization intent from journalist framing.
- Do not infer audience response from article publication alone.
- News presence measures visibility/uptake, not persuasion or public agreement.

## Analytical questions

1. Which nonprofit organizations become visible sources in the local news ecosystem during the crisis?
2. Which organizational roles are most frequently quoted or cited?
3. Which emotions/appraisals/functions are most likely to survive into news coverage?
4. When nonprofit messages are covered, are their affective frames preserved, amplified, attenuated, shifted, or contested?
5. Does news coverage carry practical service/legal/action information into wider circulation?
6. How does news-media uptake differ from social/public uptake?
7. Do some organizations function as recurring affective intermediaries across both organizational and journalistic communication layers?

## Interpretation limits

- Search-based news recovery is not necessarily a complete census.
- Outlet archives differ in accessibility.
- Syndication and duplicate wire/local reposts must be deduplicated.
- A quotation does not imply journalist endorsement.
- News visibility does not equal public influence.
- Media uptake should be analyzed as an intermediary transformation layer, not collapsed into social engagement metrics.
