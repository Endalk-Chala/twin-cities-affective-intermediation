"""Apply organization-specific corrections to ambiguous multi-organization media rows.

The raw media batches remain immutable. This script creates a normalized relation
layer by replacing only those source rows explicitly documented in
`data/interim/media_multi_org_split_corrections_v1.csv`.

Output:
    data/processed/media_relations_normalized_v1.csv

This normalized table is the appropriate input for prominence/network analysis.
"""

from __future__ import annotations

import glob
import os
from pathlib import Path

import pandas as pd

RAW_GLOB = "data/raw/news_media_uptake_batch_*.csv"
CORRECTIONS = Path("data/interim/media_multi_org_split_corrections_v1.csv")
OUT = Path("data/processed/media_relations_normalized_v1.csv")


def clean(x):
    if pd.isna(x):
        return ""
    return str(x).strip()


def main():
    files = sorted(glob.glob(RAW_GLOB))
    if not files:
        raise FileNotFoundError(RAW_GLOB)
    if not CORRECTIONS.exists():
        raise FileNotFoundError(CORRECTIONS)

    frames = []
    for f in files:
        df = pd.read_csv(f, dtype=str, keep_default_na=False)
        df["source_batch"] = os.path.basename(f)
        frames.append(df)
    raw = pd.concat(frames, ignore_index=True, sort=False)

    corr = pd.read_csv(CORRECTIONS, dtype=str, keep_default_na=False)
    key_cols = ["source_batch", "legacy_news_item_id", "url"]

    # Mark raw rows replaced by an explicit correction entry.
    corr_keys = set(
        zip(
            corr["source_batch"].map(clean),
            corr["legacy_news_item_id"].map(clean),
            corr["url"].map(clean),
        )
    )
    raw_keys = list(
        zip(
            raw["source_batch"].map(clean),
            raw["news_item_id"].map(clean),
            raw["url"].map(clean),
        )
    )
    raw["replaced_by_split_correction"] = [int(k in corr_keys) for k in raw_keys]
    keep = raw.loc[raw["replaced_by_split_correction"].eq(0)].copy()

    # Convert correction rows to the raw relation schema while preserving audit fields.
    base_cols = [c for c in raw.columns if c not in {"replaced_by_split_correction"}]
    out_corr = pd.DataFrame(columns=base_cols)
    for col in base_cols:
        if col in corr.columns:
            out_corr[col] = corr[col]
        else:
            out_corr[col] = ""

    # Map correction field names to raw schema.
    out_corr["news_item_id"] = corr["legacy_news_item_id"]
    out_corr["media_relation_type"] = "earned_editorial"
    out_corr["paid_sponsored_flag"] = "0"
    out_corr["news_topic"] = ""
    out_corr["frame_transformation"] = "not_yet_coded"
    out_corr["legal_info_carryover"] = ""
    out_corr["service_info_carryover"] = ""
    out_corr["action_info_carryover"] = ""
    out_corr["collection_status"] = "verified"
    out_corr["collection_notes"] = corr["split_notes"]
    out_corr["source_batch"] = corr["source_batch"]

    normalized = pd.concat([keep[base_cols], out_corr[base_cols]], ignore_index=True, sort=False)

    # Stable audit markers.
    normalized["relation_normalization_status"] = "raw_single_org_relation"
    corrected_mask = normalized["source_batch"].isin(corr["source_batch"]) & normalized["url"].isin(corr["url"])
    normalized.loc[corrected_mask, "relation_normalization_status"] = "split_multi_org_relation"

    # No semicolon-combined org_id should survive from corrected source rows.
    unresolved = normalized[normalized["org_id"].map(lambda x: ";" in clean(x))]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    normalized.to_csv(OUT, index=False)

    print(f"raw_rows={len(raw)}")
    print(f"replaced_ambiguous_rows={int(raw['replaced_by_split_correction'].sum())}")
    print(f"inserted_split_relations={len(out_corr)}")
    print(f"normalized_rows={len(normalized)}")
    print(f"remaining_multi_org_rows={len(unresolved)}")


if __name__ == "__main__":
    main()
