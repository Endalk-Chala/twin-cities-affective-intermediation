# Codebook v1.2: frozen coding rules

Status: frozen 2026-10-11 for the fresh-sample test. Read `original_codebook_v1.md` first: its categories, labels and field definitions all stay in force. This document replaces v1's level definitions and adds binding rules wherever v1 is silent. Do not change these rules during coding. Record any case they do not settle in `emotion_notes` and in your ambiguity log; the rules are revised only after the test.

---

## A. Text and item scope

**A1. Code the captured text only.** Each item's evidence is its verbatim text file in `text_capture/`. Do not open the live page, and do not use memory or other sources.

**A2. What counts as the item:** the item's headline, body, captions and image text recorded in the capture, any item-specific call to action, and the organization's own wording in a repost or teaser.

**A3. What is never evidence:** navigation; footers; site-wide donate or newsletter boxes and taglines repeated across the site (e.g. "Your gift unlocks bright futures!"); Share, Join and Donate widgets; related-content modules and sidebars; comments; and the content of linked or summarized outside works (news articles, films, books, reports). A block counts only if the capture places it in the item body *and* it is specific to this item.

**A4. Teasers and reposts.** Code the organization's own headline and teaser wording. Unseen outside text is out of scope, not missing: code the item as complete. Feelings of people or characters described in an outside work are not coded, unless the organization restates them in its own voice.

**A5. Missing or incomplete text.** If the capture is a stub (title or date only), set `coding_status = not_codable` and leave every code blank. If part of the item is unreadable (an embedded video or PDF that carries the message), set `coding_status = partial` and leave the affected codes blank with a note. Never convert missing text to zero.

**A6. Identical text.** Recurring listings whose text is identical must receive identical codes. Code the first instance, copy it, and note "identical to <item_id>".

## B. Emotion intensity (0–3)

**B0. Absent.** No identifiable cue in the item's wording. Topic, mission, a service, or a threatening event on its own does not establish an emotion.

**B1. Low.** A specific but restrained or passing cue, grounded in actual wording, framing, or a described communicative act.

**B2. Moderate.** The emotion is clearly expressed or attributed **and** either recurs in at least two distinct parts of the item or carries its main argument. Cues confined to one paragraph, one quote, or one mission sentence stay at 1. Explicit wording alone does not make a 2.

**B3. Dominant.** Both conditions must hold: (a) the emotion is the item's headline frame or stated purpose, and (b) it recurs in most substantive parts (logistics and contact lines excluded).
- Short items can reach 3 when both hold. A single headline word or one forceful phrase stays at 2, however short the item.
- Condolence and tribute letters: the genre's opening and closing formulas alone do not reach 3. The emotion must recur beyond them.
- Long analytic or explanatory pieces: 3 only if the emotion recurs in most sections. An explainer headline ("What is X?") fails condition (a).

**B4. When uncertain between adjacent levels, take the lower one** and note it.

**B5. No caps, no targets.** Code as many emotions as the text supports. Do not aim for any prevalence.

**B6. One passage, one emotion.** A passage may ground two emotions only if it carries a distinct cue for each.

**B7. Evidence for every nonzero code.** In `emotion_evidence`, give one entry per nonzero emotion, separated by " | ":
`emotion=N: "verbatim passage" [attribution: org / quoted actor (role) / affected public / supporters] (why N: short justification)`
Passages must be copied from the captured text. If every emotion is 0, write `none (all emotions coded 0)`.

## C. Category boundaries (binding)

- **Fear:** a person or group is expressed or attributed as afraid of a threat to themselves or others. A threat described without any fear response is `threat_appraisal` only. A derisive description of an institution as alarmed ("DHS, spooked by fraud") counts toward moral evaluation or outrage, not fear.
- **Anxiety/uncertainty:** expressed or attributed worry. A cost or risk warning, or unpredictability on its own, is an appraisal only.
- **Moral outrage:** condemnatory affect tied to a normative violation, carried by affect-laden words, sarcasm, exclamation, or narrated condemnatory acts. Measured analytic or legal critique is an appraisal (injustice, norm violation) only.
- **Anger:** needs its own cue of frustration or hostility beyond condemnation (e.g., "furious", exasperation at delay). It is never added automatically alongside outrage.
- **Grief/sadness:** mourning, sorrow, loss, or loneliness, expressed or attributed.
- **Solidarity:** standing with others, shared fate, or mutual identification. Invitations, sociability, plural pronouns, partner lists, and addressing "the nation" do not count.
- **Care/compassion:** the organization expresses concern, protection, or comfort (condolences count). Describing what a service is for, or stating care as an organizational value, does not count.
- **Empathy:** the item names or describes another person's experience or perspective. Care alone is not empathy. In a condolence letter, code empathy only when the bereaved person's experience is described.
- **Hope:** a projected positive future state for people or a situation. Mission or strategy statements, institutional "momentum", future dates, and formulaic "We hope you'll join us!" do not count; use `opportunity_hope_appraisal` if warranted.
- **Gratitude:** thanks or appreciation tied to a benefit received. Praise without a benefit is pride.
- **Pride:** positive valuation of identity, achievement, effort, or resilience. Metrics count only with evaluative wording. Superlative self-claims ("most comprehensive ever") are pride 1 unless developed.
- **Satisfaction at an achieved outcome** ("we are pleased", "a significant victory"): code `other_emotion` (satisfaction/relief). Wording that values the organization's own effort or quality is pride. Code hope only if further improvement is projected.
- **Reassurance:** calming or stabilizing language ("you have rights", "we are here for you", "legal protections remain in place"). Operational information alone (times, steps, "in just 4 classes") is not reassurance.
- **Defiance:** refusal, resistance, or resolve against a threat or authority, stated or enacted (e.g., "we filed suit to stop…").
- **Urgency (emotion):** affective pressure in the wording ("now more than ever", "we cannot wait"). An ordinary deadline is not urgency.
- **other_emotion:** only for a discrete emotion outside the list, named in `emotion_notes` from this closed set: reverence/love, joy/excitement, awe/being moved, satisfaction/relief, shock/dismay. Promotional upbeat tone counts as joy/excitement only when the organization states its own feeling ("we are excited"), and stays at most 1 unless excitement is the item's stated frame. Values (courage, humility, "care" as a value) are not emotions.

## D. Emotion source and explicitness

- **D1. Staff voice.** Named staff, leaders, board members, and spokespeople of the coded organization count as `emotion_source_org`, including in coverage the organization reposts. `emotion_source_quoted_actor` is reserved for non-organization speakers: officials, courts, partner organizations, outside experts, cited authors, and clients quoted by name. A quotation an organization speaker uses to make her own point belongs to that speaker.
- **D2. Other sources.** `emotion_source_affected_public` covers emotion attributed to affected people or communities. `emotion_source_supporters_public` requires supporters' own words. Slogans the organization prints count as org.
- **D3. Explicitness.** Judge using the emotions coded 2 or higher; if there are none, use all coded emotions.
  - `explicit`: all of them rest on direct affect or evaluative wording, including performative statements such as thanks, condolences, or "we're here to support you".
  - `implicit`: all of them rest on framing or described acts.
  - `mixed`: both modes occur.
  - `none`: no emotion is coded.

## E. Appraisals

- **responsibility_blame:** an actor or program is named as causing harm, even without blame words.
- **coping_efficacy:** the audience's ability to prepare, protect themselves, seek help, or reduce a named risk. Generic skill-building is `opportunity_hope`; advocacy steps are `collective_efficacy`.
- **controllability:** the item assesses whether the situation itself can be controlled. Offers of guidance and rhetorical questions do not count.
- **opportunity_hope:** an opening or improvement is identified for a situation. Praise of a program is pride, not this appraisal.
- **care_need:** includes routing a group to legal or other help in response to a named threat.

## F. Functions

- **inform:** any factual update or explanation (a low threshold).
- **warn:** an explicit alert about a risk, including a financial one, directed at the audience.
- **regulate_fear:** acknowledged fear is redirected into coping or calm.
- **mobilize:** an appeal for collective civic, advocacy, volunteer, or community action. Attending a class or celebration does not count.
- **moral_evaluation:** the organization's voice characterizes conduct as wrong, unjust, unlawful, or illegitimate. No emotion is needed.
- **increase_efficacy:** how-to steps, tools, trainings, or templates. A bare donate or read-more link does not count.
- **celebrate:** celebration is a purpose of the item. A formulaic "proud to announce" does not count.
- **other:** stewardship or acknowledgement, when thanking supporters is a stated purpose. Otherwise use it only when no named function fits, and specify it in the notes.

## G. Action, audience, links

- **G1. action_type:**
  - Registering for or attending a dated class, workshop, orientation, banquet, or event is `attend_event` only.
  - `use_resource` means using a service, tool, guide, template, or rights document.
  - Reading or downloading the organization's own reports, stories, or decisions is `other`.
  - Link labels that only open more content ("Read the story") are not actions, and neither are site widgets.
  - Sub-steps of one action (register, dress warmly) are not separate actions.
  - When there is no action, set `action_orientation_present = 0` and `action_type = none`.
  - List multiple values in codebook order.
- **G2. action_immediacy:** `low` = recurring, undated, or no time cue; `moderate` = a one-off dated event or a near-term deadline, or an explicit "now" cue; `high` = act immediately or today, or an emergency request; `none` = no action.
- **G3. urgency_level (0–3):** how pressing the item presents the situation or request in time (emerging threat, closing window). It is independent of affective wording. Routine dates, recurring schedules, and seasonal windows alone are 0.
- **G4. audience_primary:** use only explicit address or named target groups.
  - Unspecified = `general_public`.
  - A named group with no label = `other`, with the group named in the notes.
  - Press releases and media advisories with no other addressee = `media`.
  - `policymakers` only when the item addresses officials or asks something of them.
  - Language of publication and the organization's identity do not establish `ethnocultural_community`.
- **G5. resource_link_present = 1** only for a hyperlink to an audience-usable service, document, tool, hotline, application, or registration or sign-up page. Permalinks, the item's own event page, read-more links, news stories, directories, calendars, navigation, and plain email addresses or phone numbers count as 0.
- **G6. service_information_present** and **function_provide_service** require a direct service (intake, clinic, program, hotline) with access details. Documents alone are resources.
- **G7. direct_address = 1** when the body addresses the reader in second person or with imperative verbs. Button labels alone do not count.

## H. Organizational role

Copy `org_role_primary` and `org_role_secondary` from `org_role_table_v1.2.csv`; never judge them from the post. Set `role_hybrid_flag = 1` exactly when the table lists a secondary role. Use `none` when there is no secondary role.

## I. Blank cells

A blank cell always means pending or missing. Fields that do not apply take their `none` value: `action_type`, `action_specificity`, `action_immediacy`, `org_role_secondary`, `emotion_explicitness`, and `emotion_evidence`.