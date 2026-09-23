# Affective Intermediation Coding Codebook v1

## Purpose
This codebook operationalizes organizational affective production, appraisal, communication function, action orientation, public uptake, circulation, and conversion for the Twin Cities nonprofit communication study.

## Unit of analysis
Primary unit: one organization-owned communication item on one native platform.

Public comments/replies are separate interaction-level observations linked to the parent `item_id`.

## General coding principles
1. Code only what is observable in the item or linked public interaction.
2. Do not infer audience feelings from organizational language.
3. Do not infer organizational intent unless explicitly stated or strongly evidenced by the communication function.
4. Multiple emotions, appraisals, and functions may coexist.
5. Engagement volume is not emotion intensity.
6. Missing or hidden engagement is NA, never zero unless zero is explicitly observed.
7. Do not use enforcement relevance or emotionality as inclusion criteria.
8. When uncertain between adjacent intensity levels, use the lower level and note the ambiguity.

## Emotion intensity
Each emotion is coded 0–3.

### 0 — absent
No meaningful cue for the emotion.

### 1 — low / implicit
Emotion is implied, backgrounded, lightly signaled, or carried through restrained evaluative wording.

### 2 — moderate / explicit
Emotion is clearly expressed or attributed and materially shapes the item.

### 3 — dominant / highly explicit
Emotion is central, repeated, strongly foregrounded, or rhetorically organizes the item.

### Emotion categories
- `fear_intensity` — fear of harm, detention, loss, danger, or threat.
- `anxiety_uncertainty_intensity` — worry, uncertainty, instability, confusion, unpredictability.
- `anger_intensity` — anger, frustration, indignation.
- `moral_outrage_intensity` — anger explicitly tied to injustice, violation, abuse, illegitimacy, or moral condemnation.
- `grief_sadness_intensity` — mourning, sorrow, loss, sadness.
- `solidarity_intensity` — togetherness, standing with, collective identification, mutual support.
- `care_compassion_intensity` — care, compassion, protection, concern for wellbeing.
- `empathy_intensity` — perspective-taking or recognition of another person's suffering/experience.
- `hope_intensity` — optimism, possibility, future orientation, belief in improvement.
- `gratitude_intensity` — thanks, appreciation, recognition.
- `pride_intensity` — pride in community, staff, identity, achievement, resilience.
- `reassurance_intensity` — calming, stabilizing, reducing uncertainty or fear.
- `defiance_intensity` — refusal, resistance, resolve, determination against a threat or authority.
- `urgency_emotion_intensity` — affective urgency, immediacy, need to act now.
- `other_emotion_intensity` — emotion not captured above; specify in notes.

## Distinguishing close emotion categories
### Anger vs moral outrage
Use `anger` for frustration/anger without a clear normative judgment. Use `moral_outrage` when anger is tied to injustice, abuse, rights violation, illegitimacy, cruelty, or wrongdoing. Both may be coded.

### Care/compassion vs empathy
Care/compassion emphasizes helping, protecting, comforting, or concern. Empathy emphasizes recognizing or entering another person's perspective/experience.

### Fear vs anxiety/uncertainty
Fear is oriented toward a perceived threat/harm. Anxiety/uncertainty emphasizes unpredictability, worry, ambiguity, or not knowing what will happen.

### Solidarity vs pride
Solidarity is relational and collective support. Pride is positive valuation of identity, accomplishment, or resilience.

### Hope vs reassurance
Hope concerns positive future possibility. Reassurance reduces present fear/uncertainty or communicates stability/control.

## Emotion explicitness
- `none` — no emotion coded.
- `implicit` — emotion inferred from wording/framing without explicit affect terms.
- `explicit` — direct emotional/evaluative language.
- `mixed` — both explicit and implicit modes are prominent.

## Emotion source
Code 0/1 for each applicable source:
- `emotion_source_org`
- `emotion_source_affected_public`
- `emotion_source_supporters_public`
- `emotion_source_quoted_actor`

Do not collapse attributed public emotion into organizational emotion; source is analytically important.

# Situational Appraisal
Code 0/1. Multiple categories allowed.

- `threat_appraisal` — presents danger, risk, enforcement exposure, safety threat, or potential harm.
- `harm_loss_appraisal` — presents damage or loss that has already occurred.
- `injustice_appraisal` — frames the situation as unfair, unjust, discriminatory, abusive, or rights-violating.
- `uncertainty_appraisal` — emphasizes ambiguity, instability, unpredictability, confusion.
- `responsibility_blame_appraisal` — identifies an actor as responsible/blameworthy.
- `intentionality_appraisal` — characterizes an action as deliberate/targeted rather than accidental/systemic.
- `norm_violation_appraisal` — identifies breach of law, ethics, rights, norms, or expected conduct.
- `vulnerability_appraisal` — emphasizes exposure, precarity, lack of protection, or disproportionate risk.
- `controllability_appraisal` — assesses whether the situation can be controlled/managed.
- `coping_efficacy_appraisal` — communicates concrete ability to respond, prepare, seek help, or reduce risk.
- `collective_efficacy_appraisal` — communicates that collective/community action can make a difference.
- `care_need_appraisal` — identifies a need for protection, care, assistance, basic needs, or support.
- `opportunity_hope_appraisal` — identifies openings, improvements, successful intervention, or future possibility.

## Appraisal vs emotion
Appraisal describes how the situation is evaluated; emotion describes affective expression. A legal-rights post may strongly code coping efficacy with little explicit emotion.

# Communication function
Code 0/1. Multiple functions allowed.

- `function_inform` — provides facts, updates, explanations.
- `function_warn` — alerts to danger/risk.
- `function_reassure` — reduces fear/uncertainty, communicates stability/control.
- `function_regulate_fear` — specifically transforms fear into coping, preparation, or calm.
- `function_mobilize` — seeks collective participation or action.
- `function_advocate` — argues for policy, rights, institutional change, accountability.
- `function_provide_service` — connects audiences to direct services/support.
- `function_fundraise` — asks for financial support.
- `function_build_solidarity` — explicitly strengthens collective belonging/support.
- `function_generate_empathy` — invites recognition of another's experience/suffering.
- `function_moral_evaluation` — evaluates conduct as right/wrong, just/unjust, legitimate/illegitimate.
- `function_increase_efficacy` — provides steps/resources that increase ability to act.
- `function_mourn_commemorate` — mourns, remembers, memorializes.
- `function_document_testify` — records experience, evidence, testimony, or harm.
- `function_celebrate` — celebrates achievement, culture, resilience, milestones.
- `function_encourage_defiance` — encourages refusal/resistance.
- `function_other` — specify.

# Action orientation

## `action_orientation_present`
1 when the item asks, encourages, instructs, or clearly enables an audience action. Otherwise 0.

## `action_type`
Allow multiple values:
- `seek_legal_help`
- `use_resource`
- `attend_event`
- `protest`
- `contact_official`
- `donate`
- `volunteer`
- `share_information`
- `report_incident`
- `prepare_documents`
- `safety_plan`
- `support_business`
- `mutual_aid`
- `other`

## `action_specificity`
- `none` — no action.
- `general` — vague encouragement (e.g. support the community).
- `specific` — named action, link, place, date, procedure, contact, or concrete instruction.

## `action_immediacy`
- `none`
- `low` — no temporal pressure.
- `moderate` — near-term relevance.
- `high` — immediate/urgent action requested.

# Audience and informational content

## `audience_primary`
Choose the strongest observable target:
- immigrants_refugees
- general_public
- supporters_donors
- policymakers
- service_providers
- workers
- faith_community
- ethnocultural_community
- media
- other

## Additional binary fields
- `direct_address`
- `legal_information_present`
- `service_information_present`
- `resource_link_present`

## `urgency_level` 0–3
0 absent; 1 low; 2 clear; 3 dominant/immediate.

# Public uptake coding
Public comments/replies are coded separately from the organizational item.

A comment may receive multiple uptake codes.

- `validation_support` — endorses/affirms the organization/message.
- `gratitude` — thanks/appreciates.
- `practical_inquiry` — asks operational/service/legal/logistical question.
- `help_request` — asks for direct assistance or connection.
- `help_offer` — offers resources, labor, money, transportation, services, etc.
- `fear`
- `grief`
- `anger`
- `solidarity`
- `hope`
- `contestation` — disputes, challenges, rejects, or reframes the organizational message.
- `resource_sharing` — supplies link, phone number, service, organization, guidance.
- `coordination` — organizes people/actions/timing/logistics.
- `call_to_action` — commenter urges others to act.

## Organization response
Record whether the organization visibly replies to a public interaction. Do not infer unseen replies.

# Affective circulation

Circulation is distinct from emotion and uptake.

Capture where observable:
- official share/repost count;
- minimum observed repost traces;
- tagging of other people;
- tagging of organizations;
- cross-platform recirculation.

If the platform hides a total share count, record `observed_recirculation_minimum` only and clearly label it as a minimum.

# Affective conversion
Conversion requires observable movement from expression/interpretation toward action.

## `conversion_signal_present`
1 only when a public interaction provides observable action evidence or a concrete action-oriented coordination signal.

## `conversion_type`
- help_seeking
- help_offering
- donation
- volunteering
- event_attendance
- protest_participation
- service_connection
- resource_referral
- reporting_documentation
- other

## `conversion_evidence_level`
- `none` — no evidence.
- `weak` — stated intention or vague coordination.
- `moderate` — specific planning/request/offer tied to an action.
- `strong` — explicit evidence action occurred or direct documented connection/coordination.

Do not treat a like/reaction as conversion.

# Organizational role coding
Assign role using organizational mission and the communication unit being studied, not the tone of a particular post.

Primary categories:
- advocacy
- legal
- service
- faith
- ethnocultural
- media_information
- economic_development
- housing
- education
- coalition_network
- hybrid
- other

Where an organization has multiple major functions, use `hybrid` or a secondary role field. Broad parent organizations included only at a program level should be coded to the program role where required by sampling rules.

# Reliability procedure
Before full manual coding:
1. Draw a stratified pilot of at least 30–50 items spanning platform, organizational role, and study month.
2. Independently code the pilot twice or with a second coder where feasible.
3. Calculate agreement appropriate to the variable: Cohen's kappa for binary/nominal variables; weighted kappa or Krippendorff's alpha for ordinal intensity variables.
4. Review systematic disagreements.
5. Revise ambiguous category definitions before freezing the final codebook.
6. Do not change coding rules after inspecting hypothesis-test results without documenting the revision and rerunning affected coding.

# Derived measures
Derive after coding, not during manual coding:
- emotion presence = intensity >= 1
- emotional repertoire count
- mean emotion intensity
- maximum emotion intensity
- emotion sum
- appraisal count
- function count

Use multiple overall emotion operationalizations as robustness checks rather than treating one composite score as inherently correct.
