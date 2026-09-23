# Analysis Workflow Run Order

This file is the canonical execution order for moving from the frozen collection corpus to analysis in **Affective Intermediation in Twin Cities Nonprofit Communication**.

## 0. Preconditions
- Raw collection remains unchanged in `data/raw/`.
- Final analytical universe = 114 independent eligible/probably eligible units, with program-level restrictions and duplicate merges respected.
- Social archives are treated as partial public-web recoveries, not complete platform censuses.
- Engagement hidden/unavailable is NA, not zero.

## 1. Build analysis-ready corpus
Run:

```bash
python analysis/scripts/build_analysis_ready_dataset.py
```

Expected outputs:
- `data/processed/communication_master_all_verified_v1.csv`
- `data/processed/communication_master_primary_v1.csv`
- `data/processed/communication_candidates_unresolved_v1.csv`
- `data/processed/communication_master_qc_summary_v1.csv`

Inspect QC before proceeding.

## 2. Select reliability pilot
Run:

```bash
python analysis/scripts/select_reliability_pilot.py
```

Expected output:
- `data/processed/reliability_pilot_sample_v1.csv`

Target: 40 stratified items spanning platform, month, organization, and role where possible.

## 3. Prepare coding sheet
Run:

```bash
python analysis/scripts/prepare_and_merge_coding.py prepare
```

Expected output:
- `data/processed/manual_coding_sheet_v1.csv`

Use:
- `codebooks/affective_intermediation_coding_codebook_v1.md`
- `codebooks/temporal_emotion_arc_codebook.md`
- `codebooks/analysis_ready_master_schema_v1.md`

## 4. Code reliability pilot
Code the 40 pilot items first.

Do not inspect aggregate substantive results while refining coding rules.

Reliability protocol:
- `analysis/reliability_pilot_protocol_v1.md`

If definitions change, freeze revised codebook as v2 before full coding.

## 5. Full-corpus coding
After acceptable pilot reliability, complete all coding fields in `manual_coding_sheet_v1.csv` for the primary corpus.

Do not code unresolved candidates into the strict primary dataset unless they are independently validated first.

## 6. Merge completed coding
Run:

```bash
python analysis/scripts/prepare_and_merge_coding.py merge
```

Expected output:
- `data/processed/communication_master_coded_v1.csv`

## 7. Validate coded dataset
Run:

```bash
python analysis/scripts/validate_analysis_dataset.py
```

Do not proceed if validation reports errors.

Warnings must be reviewed, especially:
- hidden engagement encoded as zero;
- non-day dates assigned to weeks;
- duplicate item IDs;
- illegal 0–3 or binary code values.

## 8. Attach external event phases
Use:
- `analysis/external_event_chronology_v1.csv`

Recommended operational phases:
- `pre_escalation`: 2025-11-01 through 2025-11-30
- `escalation`: 2025-12-01 through 2026-01-06
- `peak`: 2026-01-07 through 2026-01-25
- `sustained_response`: 2026-01-26 through 2026-02-11
- `decline_normalization`: 2026-02-12 through 2026-03-31

These phase boundaries are external analytic definitions. They must not be adjusted after seeing emotion trajectories unless explicitly documented as a sensitivity analysis.

## 9. Run core analysis
Run:

```bash
python analysis/scripts/run_core_analysis.py
```

Outputs include:
- corpus summary
- emotion prevalence/intensity
- appraisal/function prevalence
- weekly emotional arc
- organizational-role summary
- platform summary
- engagement observability table
- weekly emotional-arc figure

## 10. Run matched-message and engagement analysis
Run:

```bash
python analysis/scripts/run_matched_engagement_analysis.py
```

Outputs include:
- matched-message differences
- observed-only engagement summaries
- public-uptake summary
- affective-conversion cases

## 11. Robustness checks
Required before manuscript claims:
- strict eligible only vs eligible + probably eligible
- item-weighted vs organization-normalized estimates
- website-only temporal benchmark
- day-precision only for weekly analyses
- high-confidence matches only
- alternative overall emotion measures
- exclude highest-volume organizations one at a time

## 12. Manuscript output sequence
Recommended empirical-results order:
1. Corpus and observability
2. Emotional repertoires
3. Temporal emotional arc
4. Organizational-role differences
5. Platform differences
6. Matched-message adaptations
7. Public uptake and circulation
8. Affective conversion / qualitative interaction cases
9. Integrated affective-intermediation model

## 13. Interpretation guardrails
- Do not equate communication volume with public salience.
- Do not equate engagement with emotion.
- Do not interpret missing social posts as silence.
- Do not infer public emotion from organization-authored content.
- Do not compare minimum-observed repost traces to official repost totals as equivalent measures.
- Do not make causal platform claims from unmatched descriptive differences.
- Do not treat visible commenters as representative of the wider public.

## Current project status
Collection is frozen for analysis as a bounded public-web corpus with comparatively strong website observability and partial social-platform archives. The next substantive task is the reliability pilot and coding, not additional broad retrieval.
