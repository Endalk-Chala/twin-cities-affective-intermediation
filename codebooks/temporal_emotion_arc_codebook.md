# Temporal Emotional Arc Coding Framework

## Purpose

This framework supports analysis of how the emotional intensity and composition of nonprofit communication changed over the immigration-enforcement surge. It is designed to preserve item-level emotion scores first and generate temporal aggregates only after coding.

## Core principle

Do **not** collapse all emotions into a single sentiment or intensity score during manual coding. Code each emotion separately at the item level. Overall emotional intensity is calculated later from the item-level emotion variables.

## Item-level temporal variables

Each communication item should include:

- `item_date` — publication date
- `week_id` — ISO-style or study-specific week identifier
- `days_from_study_start` — integer count from the study start
- `event_phase` — pre-surge / escalation / peak / sustained_response / decline_normalization / unknown
- `event_marker_primary` — nearest or directly referenced major enforcement event, if applicable
- `event_marker_distance_days` — days between item publication and event marker

Event phases must be assigned from documented enforcement and response events rather than inferred from emotional content.

## Emotion variables

Code each emotion on a 0–3 scale unless the final reliability pilot indicates a simpler scale is preferable:

- `fear_intensity`
- `anxiety_intensity`
- `anger_intensity`
- `moral_outrage_intensity`
- `sadness_grief_intensity`
- `compassion_intensity`
- `empathy_intensity`
- `solidarity_intensity`
- `reassurance_intensity`
- `hope_intensity`
- `care_intensity`
- `defiance_intensity`

### Intensity scale

- `0` — absent
- `1` — low or implicit
- `2` — clearly present / moderate
- `3` — dominant or highly explicit

Intensity should reflect the prominence of the emotional cue in the communication item, not the coder's personal reaction.

## Emotion-source variables

- `emotion_source_org` — organization expresses/evaluates emotion
- `emotion_source_affected_public` — emotion attributed to affected immigrants/refugees/families
- `emotion_source_supporters_public` — emotion attributed to supporters/general public
- `emotion_source_quoted_actor` — emotion appears in quoted speech/testimony

Multiple sources may be coded.

## Emotional function variables

Code whether the communication appears to perform one or more of the following functions:

- `function_mobilize`
- `function_warn`
- `function_reassure`
- `function_regulate_fear`
- `function_build_solidarity`
- `function_generate_empathy`
- `function_moral_evaluation`
- `function_increase_efficacy`
- `function_comfort`
- `function_encourage_defiance`

## Appraisal variables linked to temporal analysis

Retain item-level appraisal measures because changes in emotion over time may reflect changes in appraisal rather than simply changes in tone:

- `threat_appraisal`
- `harm_appraisal`
- `responsibility_attribution`
- `intentionality_appraisal`
- `norm_violation`
- `injustice_appraisal`
- `controllability_appraisal`
- `certainty_appraisal`
- `vulnerability_appraisal`
- `coping_potential`
- `collective_efficacy`

## Overall emotional intensity

Create the overall intensity measure only after item-level coding and reliability testing.

Primary candidate measure:

`overall_emotion_intensity = mean(nonmissing emotion intensity variables)`

Alternative robustness measures may include:

1. maximum emotion intensity in the item;
2. sum of emotion intensities;
3. mean of theoretically grouped emotions;
4. count of emotions present at intensity >= 1.

The manuscript should report which operationalization is used and test whether the temporal pattern is robust to reasonable alternatives.

## Weekly aggregation

For the main emotional-arc figure, aggregate communication by week.

Recommended weekly measures:

- mean overall emotional intensity;
- median overall emotional intensity;
- number of relevant communication items;
- mean intensity for each individual emotion;
- proportion of items containing each emotion;
- organization-normalized weekly mean to prevent high-volume organizations from dominating the trend.

The organization-normalized weekly mean should first calculate an organization's weekly average, then average across organizations active that week.

## Main planned figures

### Figure 1 — Overall emotional arc

Weekly overall emotional intensity across all eligible organizations, with major immigration-enforcement events marked on the timeline.

### Figure 2 — Emotional composition over time

Separate trajectories for theoretically important emotions. Initial focal set:

- fear/anxiety;
- anger/moral outrage;
- solidarity;
- reassurance/care;
- hope.

Related emotions may be combined only after theoretical justification and reliability/empirical inspection.

### Figure 3 — Organizational-role trajectories

Compare temporal emotional intensity across organizational orientations, initially:

- advocacy-oriented organizations;
- service-oriented organizations;
- hybrid organizations where sample size permits.

## Interpretation rules

Do not assume in advance that emotion rises during escalation or declines afterward. The temporal arc is an empirical question.

Do not infer audience feelings from organizational communication alone. The study measures emotional cues, appraisals, attributed emotions, emotional positioning, and organizational attempts at emotional mediation.

A decline in explicit emotional language should not automatically be interpreted as emotional disengagement. Service-oriented procedural communication may function as emotional regulation by increasing coping potential, certainty, or perceived control.

## Planned theoretical test

The temporal analysis is designed to examine whether nonprofit organizations perform different forms of emotional mediation across stages of an enforcement crisis. A possible pattern to test is whether advocacy-oriented organizations emphasize morally mobilizing emotions while service-oriented organizations increasingly emphasize reassurance, care, coping, and efficacy.

This pattern is a hypothesis/theoretical expectation, not a coding assumption.
