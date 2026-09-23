# AI Coding and Human Validation Protocol

## Purpose

This protocol defines how AI-assisted coding will be used in **Affective Intermediation in Twin Cities Nonprofit Communication** without treating AI output as a human gold standard.

The AI-coded layer is analytically useful because it can code the full corpus consistently, but its validity must be evaluated against independently produced human coding.

## Core design

1. The AI codes the full eligible communication corpus first.
2. AI codes are stored in a separate file and never overwrite human coding.
3. The researcher later codes a fresh blind validation sample without seeing the AI codes.
4. Agreement is calculated variable-by-variable.
5. Low-confidence, ambiguous, and disagreement-heavy items are manually reviewed.
6. The final manuscript reports the role of AI in coding and the human-validation procedure transparently.

## Output files

Primary AI output:

`data/processed/ai_coding_v1.csv`

Human validation output:

`data/processed/human_validation_coding_v1.csv`

Comparison/reliability output:

`analysis/tables/ai_human_reliability_v1.csv`

Adjudicated/final coding should be saved separately rather than overwriting either source layer.

## Independence rule

The researcher should not inspect AI codes before completing the blind validation sample.

Because Pilot Item 1 has already been discussed jointly, it should not be included in the final blind reliability sample. A fresh stratified validation sample should be drawn after AI full-corpus coding.

## Coding evidence hierarchy

The AI must record what evidence was actually available for each item.

`coding_source_quality`:
- `full_text` — complete organization-authored communication available.
- `substantial_excerpt` — enough original text to code most dimensions confidently.
- `summary_plus_title` — repository title and substantive collection summary only.
- `title_only` — insufficient for most substantive coding.
- `unavailable` — no defensible communication content available.

Preferred evidence order:
1. full native organization-authored text;
2. archived/captured organization-authored text;
3. substantial source excerpt;
4. repository title plus collector summary;
5. title alone.

## Abstention rule

The AI must not force a zero when evidence is insufficient.

For substantive variables:
- use `0` only when the available content is sufficient to judge the feature absent;
- use blank/NA when the source evidence is too limited to determine presence or absence;
- use `coding_abstain = 1` when the item is globally too thin for reliable substantive coding.

This distinction is especially important for emotion intensity, appraisal, action orientation, and communication function.

## Coding-confidence fields

Each item receives:

- `ai_coder_id` — model/version identifier used for the coding pass.
- `coding_source_quality`.
- `ai_coding_confidence` — `high`, `medium`, or `low`.
- `coding_abstain` — 0/1.
- `ambiguity_flag` — 0/1.
- `ambiguity_notes` — concise explanation of borderline decisions.

Suggested confidence interpretation:
- `high` — full/substantial text and codebook fit is clear.
- `medium` — adequate evidence but one or more reasonable alternative codes exist.
- `low` — partial evidence, strong contextual dependence, or several uncertain judgments.

## Organizational role rule

Organizational role should be assigned from an organization-level role registry, not inferred independently from each communication item.

The communication item may perform functions different from the organization's primary role. For example, a service organization may publish an advocacy-oriented post without becoming an advocacy organization for coding purposes.

## Appraisal coding rule

Appraisals are coded only when communicated or clearly presupposed in the item.

Examples:
- `vulnerability_appraisal = 1` requires explicit or clearly described exposure, precarity, susceptibility, or inability to protect oneself; immigrant/refugee identity alone is not enough.
- `injustice_appraisal = 1` requires an unfairness, rights violation, discriminatory treatment, or analogous evaluative frame.
- `coping_efficacy_appraisal = 1` requires information/action that increases perceived ability to respond.
- `collective_efficacy_appraisal = 1` requires a credible collective pathway to action or support.

## Emotion coding rule

Emotion dimensions use the 0–3 codebook scale:
- 0 absent
- 1 low/implicit
- 2 clearly present/moderate
- 3 dominant/highly explicit

Important boundaries:
- `reassurance` requires reduction of fear, uncertainty, or perceived threat; positive language alone is insufficient.
- `moral_outrage` requires anger tied to perceived injustice, wrongdoing, violation, or moral condemnation.
- `solidarity` requires relational alignment/support with a group or collective cause, not generic positivity.
- `care_compassion` requires concern for wellbeing or suffering; it is not identical to empathy.
- `hope` concerns favorable future possibility; `reassurance` concerns reduced present uncertainty/threat.

## Function coding rule

Functions describe what the communication is doing, not merely its topic.

Important boundary:
- `function_advocate = 1` should require an attempt to influence policy, institutions, rights, public norms, or collective social change. Ordinary encouragement to patronize a business or attend a routine event does not automatically count as advocacy.

Multi-label coding is allowed.

## Action-orientation rule

Action orientation requires an observable requested or facilitated action.

Examples:
- seek legal help;
- use a resource;
- attend an event;
- protest;
- contact an official;
- donate;
- volunteer;
- share information;
- report an incident;
- prepare documents;
- safety plan;
- support a business;
- mutual aid.

`action_specificity`:
- `none`
- `general`
- `specific`

`action_immediacy`:
- `none`
- `low`
- `moderate`
- `high`

## Public-uptake and engagement rule

Engagement counts are not emotion measures.

The AI must not infer emotional intensity from likes, comments, shares, reposts, or views.

Visible comment/reply coding remains a separate interaction-level layer.

Hidden/unavailable engagement remains NA, never zero.

## Human validation sample

After full AI coding, draw a fresh stratified sample large enough to cover:
- website and social media;
- all study months;
- routine and crisis communication;
- major organizational-role categories;
- high-, medium-, and low-confidence AI cases;
- a range of emotional intensity levels.

Recommended minimum: 40 items, with expansion if reliability is unstable or category prevalence is low.

The researcher codes the validation items independently using the same codebook and without seeing AI codes.

## Reliability metrics

Calculate agreement variable-by-variable.

Recommended:
- Cohen's kappa or prevalence-adjusted alternatives for binary appraisal/function variables;
- weighted Cohen's kappa and/or Krippendorff's alpha for 0–3 ordinal emotion/intensity variables;
- percent agreement alongside chance-corrected measures;
- confusion matrices for theoretically central categories;
- explicit disagreement counts for low-prevalence codes.

Do not report a single universal reliability number across unlike variable types.

## Adjudication

After reliability is calculated:
1. inspect systematic disagreements;
2. revise definitions only if necessary and document the revision;
3. recode affected variables if definitions materially change;
4. manually review all low-confidence AI cases and major AI-human disagreements;
5. create a separate adjudicated/final dataset.

## Agent implementation principle

An automated coding agent may be developed after this protocol and the codebook are stable.

The agent should:
- ingest one communication item at a time;
- receive the frozen codebook;
- receive only the evidence available for that item;
- emit strict structured fields matching the coding schema;
- include confidence and evidence-quality metadata;
- be allowed to abstain;
- never use aggregate results or hypotheses to decide item-level codes;
- preserve a reproducible prompt/version identifier.

The agent's outputs should be treated as AI-generated annotations requiring validation, not as ground truth.
