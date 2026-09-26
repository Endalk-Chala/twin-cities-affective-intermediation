"""Build the bounded media-prominence enrichment seed for Version 1 analysis.

This script consolidates the existing news_media_uptake_batch_*.csv files. It does
NOT discover new media items. It protects against legacy ID collisions, flags
multi-organization rows that require manual splitting, derives only conservative
source-prominence indicators, and creates a priority queue for matched-message
frame-transformation review.

Outputs
-------
data/interim/media_prominence_enrichment_seed_v1.csv
data/interim/media_frame_transformation_priority_v1.csv
analysis/media_prominence_enrichment_qc_v1.md
"""

from __future__ import annotations

import glob
import hashlib
import os
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import pandas as pd

RAW_GLOB = "data/raw/news_media_uptake_batch_*.csv"
OUT_MASTER = Path("data/interim/media_prominence_enrichment_seed_v1.csv")
OUT_FRAME = Path("data/interim/media_frame_transformation_priority_v1.csv")
OUT_QC = Path("analysis/media_prominence_enrichment_qc_v1.md")
OUTLET_REGISTRY = Path("platform_registry/news_outlet_registry_v1.csv")

FINAL_TRANSFORM_CODES = {
    "preserved", "amplified", "attenuated", "shifted", "contested", "mixed", "not_assessable"
}

PRIMARY_VISIBILITY = {
    "primary_story_subject", "primary_report_subject", "primary_subject",
    "primary_event_organizer", "primary_advocacy_source", "primary_expert_source",
    "primary_community_source", "primary_legal_source", "primary_nonprofit_source",
}

DIRECT_RELATION_TYPES = {
    "direct_quote", "direct_statement_quote", "direct_interview", "direct_statement_republication"
}

OUTLET_ALIASES = {
    "Minnesota Star Tribune": "Star Tribune",
    "Minnesota Spokesman-Recorder": "Spokesman-Recorder",
}


def clean_str(x) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip()


def norm_url(url: str) -> str:
    url = clean_str(url)
    if not url:
        return ""
    try:
        parts = urlsplit(url)
        path = re.sub(r"/+$", "", parts.path)
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))
    except Exception:
        return url.rstrip("/")


def stable_id(prefix: str, text: str, n: int = 14) -> str:
    h = hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]
    return f"{prefix}{h}"


def binary_numeric(x):
    s = clean_str(x).lower()
    if s in {"1", "1.0", "true", "yes"}:
        return 1
    if s in {"0", "0.0", "false", "no"}:
        return 0
    return pd.NA


def headline_match(organization: str, headline: str):
    """Conservative literal match only; otherwise leave missing for manual review."""
    org = clean_str(organization)
    head = clean_str(headline)
    if not org or not head or ";" in org:
        return pd.NA
    org_norm = re.sub(r"[^a-z0-9 ]+", " ", org.lower())
    head_norm = re.sub(r"[^a-z0-9 ]+", " ", head.lower())
    org_norm = re.sub(r"\s+", " ", org_norm).strip()
    head_norm = re.sub(r"\s+", " ", head_norm).strip()
    # Require a meaningful literal organization-name match. Acronyms and aliases are manual.
    if len(org_norm) >= 7 and org_norm in head_norm:
        return 1
    return pd.NA


def main():
    files = sorted(glob.glob(RAW_GLOB))
    if not files:
        raise FileNotFoundError(f"No files matched {RAW_GLOB}")

    frames = []
    for f in files:
        df = pd.read_csv(f, dtype=str, keep_default_na=False)
        df["source_batch"] = os.path.basename(f)
        df["source_row"] = range(2, len(df) + 2)  # header is row 1
        frames.append(df)

    d = pd.concat(frames, ignore_index=True, sort=False)

    # Preserve legacy identifiers but never treat them as globally unique.
    d["legacy_news_item_id"] = d.get("news_item_id", "").map(clean_str)
    legacy_counts = d["legacy_news_item_id"].value_counts()
    d["legacy_id_collision_flag"] = d["legacy_news_item_id"].map(legacy_counts).gt(1).astype(int)

    d["canonical_url"] = d.get("url", "").map(norm_url)
    fallback_story = (
        d.get("date", "").map(clean_str) + "|" +
        d.get("outlet", "").map(clean_str) + "|" +
        d.get("headline", "").map(clean_str)
    )
    story_key = d["canonical_url"].where(d["canonical_url"].ne(""), fallback_story)
    d["story_id"] = story_key.map(lambda x: stable_id("STORY_", x))

    d["multi_org_relation_needs_split_review"] = d.get("org_id", "").map(lambda x: int(";" in clean_str(x)))
    relation_key = (
        d["story_id"] + "|" + d.get("org_id", "").map(clean_str) + "|" +
        d["source_batch"] + "|" + d["source_row"].astype(str)
    )
    d["media_relation_id"] = relation_key.map(lambda x: stable_id("MR_", x))

    # Normalize outlet labels while preserving original values.
    d["outlet_original"] = d.get("outlet", "").map(clean_str)
    d["outlet_canonical"] = d["outlet_original"].replace(OUTLET_ALIASES)

    # Join the local/regional outlet registry when possible.
    registry = pd.read_csv(OUTLET_REGISTRY, dtype=str, keep_default_na=False)
    registry["outlet_canonical"] = registry["outlet_name"].replace(OUTLET_ALIASES)
    reg_cols = ["outlet_canonical", "outlet_id", "outlet_type", "geographic_scope", "priority_tier"]
    registry = registry[reg_cols].drop_duplicates("outlet_canonical")
    d = d.merge(registry, on="outlet_canonical", how="left", suffixes=("_raw", "_registry"))
    d["registry_match_status"] = d["outlet_id"].map(lambda x: "matched_local_registry" if clean_str(x) else "not_in_local_registry")

    # Keep national/external amplification analytically separate from local/regional prominence.
    collection_status = d.get("collection_status", "").map(clean_str).str.lower()
    relation_type = d.get("media_relation_type", "").map(clean_str).str.lower()
    d["local_national_layer"] = "local_regional"
    external = collection_status.eq("verified_external") | relation_type.eq("earned_editorial_external")
    d.loc[external, "local_national_layer"] = "national_external"

    # Conservative prominence components.
    d["organization_mentioned"] = 1
    quoted_existing = d.get("organization_quoted", "").map(binary_numeric)
    direct_type = d.get("organization_visibility", "").map(clean_str).str.lower().isin(DIRECT_RELATION_TYPES)
    d["organization_quoted_directly"] = quoted_existing
    d.loc[d["organization_quoted_directly"].isna() & direct_type, "organization_quoted_directly"] = 1

    d["spokesperson_named"] = d.get("spokesperson", "").map(lambda x: int(bool(clean_str(x))))
    visibility = d.get("organization_visibility", "").map(clean_str).str.lower()
    d["organization_primary_source"] = visibility.isin(PRIMARY_VISIBILITY).astype(int)

    # Paraphrase cannot be safely inferred for all relation types from metadata alone.
    d["organization_paraphrased"] = pd.NA
    likely_paraphrase = visibility.isin({
        "cited_guidance", "secondary_legal_source", "resource_citation", "partner_visibility",
        "substantive_mention", "substantive_organizational_visibility", "substantive_program_partner",
        "statement_carryover"
    }) & d["organization_quoted_directly"].fillna(0).eq(0)
    d.loc[likely_paraphrase, "organization_paraphrased"] = 1

    d["organization_headline_or_deck"] = [
        headline_match(o, h) for o, h in zip(d.get("organization", ""), d.get("headline", ""))
    ]
    d["organization_first_third"] = pd.NA

    # Partial score: only directly observable/defensibly derived components. The complete flag
    # remains 0 until headline/deck, first-third, and paraphrase fields are manually resolved.
    components = {
        "organization_mentioned": 1,
        "organization_paraphrased": 2,
        "organization_quoted_directly": 3,
        "spokesperson_named": 2,
        "organization_primary_source": 3,
        "organization_headline_or_deck": 2,
        "organization_first_third": 1,
    }
    score = pd.Series(0.0, index=d.index)
    for col, weight in components.items():
        score += pd.to_numeric(d[col], errors="coerce").fillna(0) * weight
    d["partial_prominence_score"] = score
    d["prominence_complete_flag"] = (
        d[["organization_paraphrased", "organization_headline_or_deck", "organization_first_third"]]
        .notna().all(axis=1).astype(int)
    )

    # Frame transformation review queue. Never infer a transformation from notes alone.
    transform = d.get("frame_transformation", "").map(clean_str).str.lower()
    matched = d.get("matched_org_item_id", "").map(clean_str).ne("")
    confidence = d.get("match_confidence", "").map(clean_str).str.lower()
    d["frame_transformation_review_status"] = "manual_review_optional"
    d.loc[transform.isin(FINAL_TRANSFORM_CODES), "frame_transformation_review_status"] = "coded"
    d.loc[~matched & ~transform.isin(FINAL_TRANSFORM_CODES), "frame_transformation_review_status"] = "not_assessable_without_match"
    d.loc[matched & confidence.isin({"high", "medium"}) & ~transform.isin(FINAL_TRANSFORM_CODES),
          "frame_transformation_review_status"] = "priority_manual_review"

    d["frame_transformation_final"] = transform.where(transform.isin(FINAL_TRANSFORM_CODES), "")
    d["frame_transformation_coding_rule"] = (
        "Compare matched organization-owned and news text; do not infer from metadata/notes alone."
    )

    # Story-level duplicate indicators based on canonical URL; organization-story relations remain distinct.
    d["story_relation_duplicate_count"] = d.groupby(["story_id", "org_id"], dropna=False)["media_relation_id"].transform("size")
    d["possible_duplicate_org_story_flag"] = d["story_relation_duplicate_count"].gt(1).astype(int)

    # Known ambiguous multi-org rows stay intact until attribution is manually split.
    d["network_include_flag"] = 1
    d.loc[d["multi_org_relation_needs_split_review"].eq(1), "network_include_flag"] = 0
    d["network_exclusion_reason"] = ""
    d.loc[d["multi_org_relation_needs_split_review"].eq(1), "network_exclusion_reason"] = "multi_org_relation_requires_attribution_split"

    OUT_MASTER.parent.mkdir(parents=True, exist_ok=True)
    OUT_QC.parent.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT_MASTER, index=False)

    priority = d.loc[d["frame_transformation_review_status"].eq("priority_manual_review")].copy()
    priority_cols = [
        "media_relation_id", "story_id", "legacy_news_item_id", "source_batch", "date",
        "local_national_layer", "outlet_original", "org_id", "organization", "headline",
        "canonical_url", "organization_visibility", "organization_quoted", "spokesperson",
        "source_function", "matched_org_item_id", "match_confidence", "collection_notes",
        "frame_transformation_final", "frame_transformation_review_status"
    ]
    priority[priority_cols].to_csv(OUT_FRAME, index=False)

    # QC report documents the bounded handoff and known issues.
    qc = f"""# Media Prominence Enrichment QC v1

This report is generated by `analysis/build_media_prominence_enriched_v1.py`.

## Scope

- Input batches: **{len(files)}** existing `news_media_uptake_batch_*.csv` files.
- Raw organization/news rows: **{len(d)}**.
- Unique canonical story IDs: **{d['story_id'].nunique()}**.
- Local/regional rows: **{int((d['local_national_layer'] == 'local_regional').sum())}**.
- National/external rows: **{int((d['local_national_layer'] == 'national_external').sum())}**.
- Rows with legacy `news_item_id` collisions: **{int(d['legacy_id_collision_flag'].sum())}**.
- Multi-organization rows requiring attribution split before network use: **{int(d['multi_org_relation_needs_split_review'].sum())}**.
- High/medium matched relations prioritized for frame-transformation review: **{len(priority)}**.

## Safeguards

1. Legacy `news_item_id` is preserved but is **not** treated as globally unique.
2. `story_id` is derived primarily from canonical URL; `media_relation_id` is separately created for each organization-story relation.
3. Multi-organization rows are excluded from network-ready output until their quote/source attribution is manually split.
4. Local/regional and national/external amplification are kept as separate analytical layers.
5. The prominence score is explicitly **partial** until manual paraphrase, headline/deck, and first-third coding is complete.
6. Frame transformation is never inferred from collection notes. High/medium matched pairs are routed to manual comparative review; unmatched pairs are marked `not_assessable_without_match`.

## Freeze rule

Version 1 media enrichment stops after the already-verified relations receive the core prominence fields, duplicate/syndication issues are reconciled, and priority matched pairs receive defensible transformation codes. New broad media discovery is outside Version 1 unless it corrects a clear omission or addresses a reviewer-requested robustness issue.
"""
    OUT_QC.write_text(qc, encoding="utf-8")

    print(qc)


if __name__ == "__main__":
    main()
