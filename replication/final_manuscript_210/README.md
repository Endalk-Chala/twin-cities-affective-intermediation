# Manuscript-specific reliability replication: 210 communication items

**Status (2026-10-23):** Coding-score replication material released for transparency. **The author confirmed on October 23, 2026 that these were two independent human coders.** This is an author-provided account of coding provenance; the numeric score matrices independently reproduce the agreement estimates but cannot, by themselves, verify coder identities or independence.

## Which dataset does this represent?

This folder is associated with the article manuscript *Affective Intermediation: Emotional Attribution and Journalistic Relay During Minnesota’s Immigration Enforcement Crisis* (210 analyzed nonprofit communication items from 32 organizations; November 2025–March 2026). It is distinct from the **337-item/44-organization exploratory working corpus** documented in the repository root and `data/processed/full_corpus_coded_master_v1.csv`. Do **not** treat the datasets as interchangeable.

The author identified the linked dataset record as https://doi.org/10.5281/zenodo.23586832; **these paired coding matrices were not verified as part of that Zenodo deposit**. This GitHub folder is a separate publication of the coder-score replication material, not a claim that Zenodo already contains it. Verify the current Zenodo file inventory directly before any new data-availability statement.

## Files

- `Full_Coder_1_de_textualized_214.csv` and `Full_Coder_2_de_textualized_214.csv`: Two score matrices, each with **214 matched candidate item IDs** and **63 columns**. Each contains coding status and categorical/ordinal coded values only; organization names, names of research participants, URLs, original communications, quotation excerpts, free-text coding notes and coder identifiers have been excluded. Coder names in filenames distinguish the independent human coding passes as confirmed by the author; filenames and matrices alone do not independently verify that provenance.
- `compute_reliability.py`: Standalone computation of nominal/ordinal Krippendorff's alpha and raw pairwise agreement, using the score matrices.
- `historical_agreement_by_variable.csv`: Historical variable schema and reported coefficients used **for comparison**, not for computing new scores.
- `recomputed_reliability_summary.csv`: Independently recomputed output of the script (76 estimates).
- `SHA256SUMS.txt`: Hashes of these data/scripts for integrity checking.

## Reproduce the reliability coefficients

Install Python 3, `numpy`, and `pandas`, then from this directory run:

```bash
python compute_reliability.py
```

The script aligns records by `item_id`, limits the alpha calculation to items whose statuses are `complete` or `partial` in **both matrices**, derives binary emotion-presence variables from nonzero intensities, and applies ordinal alpha to intensities and nominal alpha to categorical variables. It writes `recomputed_reliability_summary.csv` and checks against historic rounded values.

**Verified locally on 2026-10-23:** 214 paired IDs; 210 codable by both; two coding-status disagreements; all 76 alpha point estimates reproduced to three-decimal rounding. Median alpha for 14 named emotion intensities was **0.864** (range **0.580–0.986**); reassurance was a notable lower-reliability variable (**0.580**). Other variables have different reliability values; read the full CSV instead of relying on a single median.

The **210-item statistical sample**, the **214 rows assessed for codability**, and the **56 matched nonprofit–news passages** are different denominators. These matrices reproduce *intercoder agreement* only, **not** the complete article figures, causal claims, matched-news analyses, or adjudicated final coding decisions.

## Provenance and ethics limitations

**Author confirmation:** The two coding passes were performed by two independent human coders. **Documentation boundary:** These de-textualized files do not themselves establish coder identities, independently document workflow separation, specify whether computational tools assisted coding, or establish permissions for disseminating coder records. Such matters should be documented through the author's research records and ethics review, not inferred from high alpha. The full unredacted coder sheets are retained privately and are **not published here**. Item IDs remain to allow alignment with the underlying study and may be linkable to public organizational texts. This is de-textualization, not a guarantee of anonymous records.

## Anonymous peer review

This is an author-identified public GitHub repository. **Do not link to this repository in an anonymized manuscript if the journal uses double-anonymous review.** Use the separate blinded supplementary package, with item IDs replaced by neutral keys and author-identifying metadata removed, supplied confidentially to the journal when appropriate. The package for anonymous review should not include a URL or DOI revealing the author during review.
