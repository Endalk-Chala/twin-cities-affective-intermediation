# Analysis Plan v1 — Affective Intermediation in Twin Cities Nonprofit Communication

## Analysis philosophy
The analysis separates four empirical layers:
1. **Affective production** — organizational communication.
2. **Affective uptake** — public responses visible in comments/replies.
3. **Affective circulation** — shares/reposts/tagging/cross-platform movement.
4. **Affective conversion** — observable movement toward material or civic action.

Website communication is comparatively well observed; social-media archives are partial and platform-dependent. Therefore, platform analyses must condition interpretation on observability rather than treating missing social posts as silence.

## Dataset hierarchy
### Primary communication corpus
Verified communication items in the study period belonging to eligible/probably eligible units, with program-level restrictions respected.

### Candidate corpus
Unresolved or indexed-only items retained for sensitivity/qualitative follow-up but excluded from strict primary counts until verified.

### Engagement corpus
Only items for which public engagement fields were observable. Missing engagement is not zero.

### Interaction corpus
Visible public comments/replies only. This is an observed-interaction sample, not a complete audience-response census.

### Matched-message corpus
High-confidence and, separately, medium-confidence same-message sets used for within-message platform comparison.

# Stage 1 — Corpus audit and descriptive statistics
Report:
- total verified primary communication items;
- number of organizations represented;
- items by month;
- items by platform;
- items by organizational role;
- retrieval/archive status;
- number and share of month-only or lower-precision dates;
- social-channel observability coverage;
- number of items with engagement snapshots;
- number of visible interaction rows;
- number of matched-message sets.

Purpose: make data availability transparent before substantive interpretation.

# Stage 2 — Emotional repertoire
For each emotion:
- prevalence: proportion of items with intensity >= 1;
- mean intensity among all items;
- mean intensity among items where present;
- distribution across 0/1/2/3.

Overall emotion measures for robustness:
1. mean across emotion-intensity variables;
2. maximum emotion intensity;
3. sum of intensities;
4. emotional repertoire count.

Do not collapse to positive/negative sentiment.

# Stage 3 — Appraisal and function structure
Describe prevalence of:
- threat
- harm/loss
- injustice
- uncertainty
- responsibility/blame
- vulnerability
- coping efficacy
- collective efficacy
- care need
- hope/opportunity

Describe functions:
- information
- warning
- reassurance/fear regulation
- mobilization
- advocacy
- service provision
- fundraising
- solidarity
- empathy
- moral evaluation
- efficacy building
- mourning
- documentation/testimony
- celebration
- defiance

Cross-tab theoretically important appraisal → emotion → function combinations.

# Stage 4 — Temporal analysis
Use day-precision items for weekly analysis. Month-only records remain in monthly/descriptive analyses.

Primary weekly measures:
- communication volume;
- mean and median overall emotion intensity;
- organization-normalized mean emotion intensity;
- proportion of items containing each focal emotion;
- mean intensity of focal emotions.

Focal emotional trajectories:
- fear/anxiety
- anger/moral outrage
- grief
- solidarity
- care/reassurance
- hope
- defiance

Major event phases/markers must come from an externally documented chronology and may not be inferred from the emotional corpus.

# Stage 5 — Organizational-role comparison
Compare emotion/appraisal/function profiles across roles.

Primary contrasts:
- advocacy/legal vs service
- ethnocultural/community vs legal/advocacy
- faith vs non-faith where sample permits
- hybrid vs single-role organizations

Do not interpret role differences without reporting item and organization counts.

Where high-volume organizations dominate, use organization-normalized estimates and robustness analyses.

# Stage 6 — Platform comparison
Because website is much more observable than social archives, run three forms of comparison:

### 6A. Descriptive platform comparison
All verified website vs all verified social items; clearly label selection/observability limitation.

### 6B. Within-organization comparison
Organizations with observed items on both website and social platforms.

### 6C. Matched-message comparison
Highest internal-validity platform comparison: same underlying message across platforms.

Compare:
- emotion intensity
- emotional repertoire
- urgency
- direct audience address
- action orientation
- legal/service contextual information
- mobilization
- solidarity/care framing

Do not claim platform causality from unmatched corpus differences alone.

# Stage 7 — Matched-message adaptation analysis
For high-confidence matched sets:
- calculate within-set change in each emotion intensity;
- change in urgency;
- change in action specificity;
- change in audience address;
- presence/absence of legal/service detail;
- adaptation type.

Use paired descriptive analysis first. If enough matched sets accumulate, use paired nonparametric tests or mixed-effects models as appropriate.

# Stage 8 — Engagement / affective uptake
Limit denominator to posts for which the relevant metric is observable.

Analyze separately:
- reactions/likes
- comments
- shares/reposts
- views

Never construct engagement totals by treating hidden fields as zero.

Primary questions:
- Are posts with different emotional repertoires associated with different observable engagement patterns?
- Are mobilizing/action-oriented posts associated with more comments or circulation?
- Do procedural coping-efficacy posts receive different uptake from moral-outrage/solidarity posts?

Given sparse and nonrandom observability, engagement analyses are primarily descriptive/exploratory unless coverage becomes sufficient.

# Stage 9 — Public interaction analysis
For visible comments/replies, analyze:
- validation/support
- gratitude
- practical inquiry
- help requests
- help offers
- fear/grief/anger/solidarity/hope
- contestation
- resource sharing
- coordination
- organization replies

Pair quantitative counts with qualitative interaction sequences.

Important: commenters are not representative of the wider public.

# Stage 10 — Affective circulation
Use:
- official share/repost counts where observable;
- minimum observed recirculation traces where official counts are hidden;
- tagging and cross-organizational movement.

Do not compare official share counts directly with minimum-observed traces as though they are equivalent metrics.

# Stage 11 — Affective conversion
Identify interactions that move toward:
- help seeking
- help offering
- donations
- volunteering
- event/protest attendance
- service connections
- resource referrals
- reporting/documentation

Primary output should be a typology plus qualitative cases. Quantification is secondary because conversion evidence is selectively observable.

# Stage 12 — Integrated affective-intermediation analysis
Examine chains such as:
`appraisal → organizational emotion/function → action orientation → public uptake → circulation → conversion`

Potential archetypes to test empirically:
- threat → fear/uncertainty → reassurance/coping → service seeking
- injustice → moral outrage → mobilization/defiance → civic participation
- harm/loss → grief → solidarity/care → mutual aid
- vulnerability → compassion/care → resource provision → help offering

These are hypotheses/interpretive patterns, not coding assumptions.

# Statistical strategy
Prioritize descriptive and multilevel-aware analysis over overfitted inference.

Possible models if sample size supports them:
- ordinal/multinomial models for emotion intensity;
- logistic models for emotion/function presence;
- count models for observable engagement metrics, restricted to observed denominators;
- mixed-effects models with organization random intercepts;
- organization-clustered standard errors;
- paired analyses for matched-message sets.

Report effect sizes and uncertainty, not only p-values.

# Robustness checks
- item-weighted vs organization-normalized estimates;
- strict eligible only vs eligible + probably eligible;
- day-precision only vs monthly-inclusive summaries;
- high-confidence matched sets only vs high+medium;
- alternative overall-emotion measures;
- excluding the highest-volume organization(s);
- website-only temporal trajectory as a high-observability benchmark.

# Primary manuscript figures
1. Corpus and observability overview.
2. Weekly communication volume and emotional arc.
3. Emotional composition over time.
4. Emotional/appraisal repertoires by organizational role.
5. Website vs social within-organization comparison.
6. Matched-message platform adaptation figure.
7. Affective-intermediation pathway/typology figure.

# Primary manuscript tables
1. Sample and corpus composition.
2. Codebook/reliability statistics.
3. Emotion/appraisal/function prevalence.
4. Organizational-role comparisons.
5. Matched-message cases and adaptation types.
6. Engagement/interaction observability summary.

# Interpretation limits
- Public-web archives are not equivalent across platforms.
- Social engagement snapshots were captured after original posting and represent accumulated visible counts at capture time.
- Comments are visible-platform traces, not representative audience opinion.
- Missing engagement cannot be interpreted as zero.
- Organizational emotion does not establish audience emotion.
- Observed conversion signals document visible coordination/action only; they do not capture offline action comprehensively.
