# Cross-Platform Matched-Message Protocol v1

## Purpose

This protocol governs how website and social-media communications will be linked after collection without collapsing platform-specific observations. The aim is to support within-organization comparison of how the same underlying communication is adapted across channels.

## Collection rule

Collect each public communication item as a separate observation on its native platform. Do not discard a Facebook, Instagram, LinkedIn, YouTube, TikTok, X/Twitter, or website item merely because substantively similar content appears elsewhere.

Collection remains a full census within the study window (2025-11-01 through 2026-03-31). Emotional relevance, enforcement relevance, and apparent theoretical importance are not inclusion criteria.

## Platform scope

Include as many defensibly verified official organizational channels as are active and publicly accessible, including:
- website;
- Facebook;
- Instagram;
- LinkedIn;
- YouTube;
- X/Twitter;
- TikTok;
- other official public channels discovered during platform audit.

An inaccessible or poorly indexed archive should be marked as a retrieval limitation or partial archive rather than interpreted as organizational silence.

## Matching principle

Two or more items may be assigned to the same matched-message set when they clearly communicate the same underlying organizational message, event, announcement, resource, campaign, crisis update, statement, fundraising appeal, program promotion, or call to action.

Textual identity is not required. Platform adaptation is itself an object of analysis.

## Matching evidence

Potential matching signals include:
- same or nearly identical headline/caption;
- same named event, campaign, report, resource, or initiative;
- social post linking directly to a website item;
- shared canonical URL;
- same image, graphic, video, or thumbnail;
- same quoted text or distinctive phrase;
- same named people/partners and substantive message;
- publication on the same day or within a plausible short adaptation window;
- explicit language such as “read our statement,” “learn more,” or “full story at link.”

Date proximity alone is not sufficient.

## Match-confidence field

Use a later processed-data field such as `match_confidence`:
- `high`: direct URL link, identical/near-identical content, identical asset, or unmistakably same announcement/event;
- `medium`: clearly same substantive message/event with meaningful adaptation but no direct linking evidence;
- `low`: plausible correspondence based on timing/topic but insufficient evidence for strong matching.

Low-confidence cases should remain reviewable and should not be used in strict paired analyses unless manually validated.

## Recommended identifiers

Preserve existing `crosspost_group_id` for direct or near-direct crossposts where useful. Add a broader `matched_message_id` during reconciliation for substantively corresponding communications that may be heavily adapted across platforms.

Suggested form:
`MM-<org_id>-<sequential_number>`

Example:
`MM-TC041-001`

## Separate observations

Every native-platform item remains one observation even after matching. A matched set may therefore contain:
- one website article;
- one Facebook post;
- one Instagram post;
- one LinkedIn post;
- one YouTube video.

The matched-message table links these observations but does not replace them.

## Variables for matched-message analysis

Where feasible, later reconciliation should record:
- `matched_message_id`;
- `match_confidence`;
- organization;
- platform;
- item_id;
- publication date/time if available;
- sequence/order of publication;
- direct link to another channel item yes/no;
- textual similarity or adaptation type;
- shared visual asset yes/no;
- shared video asset yes/no;
- headline/caption change;
- emotion change;
- emotional-intensity change;
- appraisal change;
- action-orientation change;
- urgency change;
- audience-address change;
- amount of contextual/legal/service information;
- notes.

## Adaptation types

Potential later categories:
1. `identical_crosspost` — substantially identical content across platforms;
2. `light_adaptation` — same message with minor shortening, hashtags, tagging, or formatting changes;
3. `platform_reframing` — same underlying message but meaningful change in framing, emotion, urgency, audience address, or call to action;
4. `website_expansion` — social post provides a short entry point to a fuller website item;
5. `social_expansion` — social version adds testimonial, visual, emotional, or mobilizing material not prominent on website;
6. `multimedia_adaptation` — underlying message transformed substantially through video/audio/visual form.

These categories are provisional and should be finalized only after pilot reconciliation.

## Timing

Matched-message identification should occur after substantial website and social collection, before emotional coding is finalized. Matching should not guide inclusion during collection.

## Analytical value

Matched-message analysis allows stronger inference about platform-conditioned communication because organizational mission and underlying issue are held relatively constant. The analysis can ask whether, for the same substantive message, social platforms intensify emotional language, urgency, relational address, visualization, or calls to action compared with the website version.

## Safeguards

- Do not infer a match only because two posts concern immigration or the same broad crisis.
- Do not discard platform duplicates from the raw corpus.
- Do not invent publication dates for undated content.
- Preserve blocked or inaccessible-channel status explicitly.
- Keep matched-message construction separate from external event chronology.
- Record uncertainty rather than forcing ambiguous matches.
