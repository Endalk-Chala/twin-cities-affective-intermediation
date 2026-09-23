#!/usr/bin/env python3
"""Build the analysis-ready communication dataset from repository raw/interim files.

Design principles:
- one row = one organization-owned communication item on one native platform;
- preserve raw files unchanged;
- include only verified communication_items_* files in the strict primary corpus;
- keep unresolved/candidate items in a separate candidate output;
- normalize platform/date/content type fields;
- attach sampling/inclusion status;
- join matched-message metadata, engagement snapshots, interaction aggregates,
  and recirculation evidence by item_id where available;
- never coerce hidden/unavailable engagement to zero.

Run from repository root:
    python analysis/scripts/build_analysis_ready_dataset.py
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
SAMPLING = ROOT / "sampling_frame"
REGISTRY = ROOT / "platform_registry"

STUDY_START = pd.Timestamp("2025-11-01")
STUDY_END = pd.Timestamp("2026-03-31")


def read_csv_flexible(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path, dtype=str, keep_default_na=False)
    except Exception:
        return pd.read_csv(path, dtype=str, keep_default_na=False, engine="python", on_bad_lines="warn")


def concat_files(paths: Iterable[Path]) -> pd.DataFrame:
    frames = []
    for p in sorted(paths):
        df = read_csv_flexible(p)
        df["source_file"] = p.name
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True, sort=False)


def norm_platform(value: str) -> str:
    x = (value or "").strip().lower()
    mapping = {
        "web": "website",
        "website": "website",
        "linkedin": "linkedin",
        "facebook": "facebook",
        "instagram": "instagram",
        "youtube": "youtube",
        "twitter": "x",
        "x/twitter": "x",
        "x": "x",
        "tiktok": "tiktok",
        "threads": "threads",
        "bluesky": "bluesky",
    }
    return mapping.get(x, x or "other")


def date_precision(value: str) -> str:
    x = (value or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", x):
        return "day"
    if re.fullmatch(r"\d{4}-\d{2}", x):
        return "month"
    if x:
        return "window_only"
    return "unknown"


def normalize_verified_items() -> pd.DataFrame:
    files = [
        p for p in RAW.glob("communication_items_*.csv")
        if "candidate" not in p.name.lower()
    ]
    df = concat_files(files)
    if df.empty:
        return df

    for col in [
        "item_id", "org_id", "organization", "date", "platform", "url",
        "content_type", "title_or_caption", "source_summary", "language",
        "media_type", "crosspost_group_id", "enforcement_relevance",
        "retrieval_date", "retrieval_status", "archive_or_capture_note",
        "collection_notes",
    ]:
        if col not in df.columns:
            df[col] = ""

    df["platform"] = df["platform"].map(norm_platform)
    df["platform_family"] = df["platform"].map(lambda x: "website" if x == "website" else "social")
    df["date_precision"] = df["date"].map(date_precision)
    df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")
    df["study_window"] = df["date_parsed"].between(STUDY_START, STUDY_END, inclusive="both")
    df["month"] = df["date_parsed"].dt.strftime("%Y-%m")
    day_mask = df["date_precision"].eq("day") & df["date_parsed"].notna()
    df["week_start"] = pd.NaT
    df.loc[day_mask, "week_start"] = (
        df.loc[day_mask, "date_parsed"]
        - pd.to_timedelta(df.loc[day_mask, "date_parsed"].dt.weekday, unit="D")
    )
    df["week_start"] = pd.to_datetime(df["week_start"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["date_basis"] = "publication_date"
    df["capture_date"] = df["retrieval_date"]
    return df


def load_candidates() -> pd.DataFrame:
    return concat_files(RAW.glob("communication_candidates_*.csv"))


def load_sampling_status() -> pd.DataFrame:
    screening = concat_files(SAMPLING.glob("eligibility_screening_batch_*.csv"))
    if screening.empty:
        screening = concat_files(SAMPLING.glob("*eligib*.csv"))
    if screening.empty:
        return pd.DataFrame(columns=["org_id", "sampling_status", "unit_of_analysis_note"])

    id_col = next((c for c in ["org_id", "record_id", "id"] if c in screening.columns), None)
    decision_col = next((c for c in ["screening_decision", "eligibility", "status"] if c in screening.columns), None)
    note_col = next((c for c in ["unit_of_analysis", "notes", "screening_notes"] if c in screening.columns), None)
    if not id_col or not decision_col:
        return pd.DataFrame(columns=["org_id", "sampling_status", "unit_of_analysis_note"])

    out = pd.DataFrame({
        "org_id": screening[id_col].astype(str).str.strip(),
        "sampling_status": screening[decision_col].astype(str).str.strip().str.lower(),
        "unit_of_analysis_note": screening[note_col].astype(str) if note_col else "",
    })
    return out.drop_duplicates("org_id", keep="last")


def derive_analysis_inclusion(df: pd.DataFrame) -> pd.DataFrame:
    status = df.get("sampling_status", pd.Series("", index=df.index)).fillna("").str.lower()
    df["analysis_inclusion_status"] = "include"
    df.loc[status.str.contains("excluded"), "analysis_inclusion_status"] = "exclude_from_primary_analysis"
    df.loc[status.str.contains("duplicate"), "analysis_inclusion_status"] = "duplicate_alias"
    df.loc[df["org_id"].eq("TC083"), "analysis_inclusion_status"] = "duplicate_alias"
    note = df.get("unit_of_analysis_note", pd.Series("", index=df.index)).fillna("").str.lower()
    program_mask = note.str.contains("program") & df["analysis_inclusion_status"].eq("include")
    df.loc[program_mask, "analysis_inclusion_status"] = "program_level_only"
    return df


def load_matched_messages() -> pd.DataFrame:
    p = INTERIM / "matched_message_candidates_v1.csv"
    if not p.exists():
        return pd.DataFrame()
    m = read_csv_flexible(p)
    if "item_id" not in m.columns:
        return pd.DataFrame()
    keep = [c for c in ["item_id", "matched_message_id", "match_confidence", "adaptation_type"] if c in m.columns]
    return m[keep].drop_duplicates("item_id", keep="last")


def load_engagement() -> pd.DataFrame:
    e = concat_files(RAW.glob("engagement_batch_*.csv"))
    if e.empty or "item_id" not in e.columns:
        return pd.DataFrame()
    keep = [c for c in [
        "item_id", "engagement_capture_date", "like_or_reaction_count", "comment_count",
        "share_or_repost_count", "view_count", "organization_reply_count", "public_reply_count",
        "engagement_visibility_status", "engagement_retrieval_status", "engagement_notes"
    ] if c in e.columns]
    return e[keep].drop_duplicates("item_id", keep="last")


def load_interaction_aggregates() -> pd.DataFrame:
    i = concat_files(RAW.glob("interaction_batch_*.csv"))
    if i.empty or "item_id" not in i.columns:
        return pd.DataFrame()

    rows = []
    for item_id, g in i.groupby("item_id", dropna=False):
        text = " ".join(g.get("emotion_or_stance_precode", pd.Series(dtype=str)).astype(str)).lower()
        notes = " ".join(g.get("interaction_summary", pd.Series(dtype=str)).astype(str)).lower()
        combined = f"{text} {notes}"
        rows.append({
            "item_id": item_id,
            "visible_interaction_rows": len(g),
            "uptake_validation_count": combined.count("validation") + combined.count("support"),
            "uptake_gratitude_count": combined.count("gratitude") + combined.count("thanks"),
            "uptake_practical_inquiry_count": combined.count("inquiry") + combined.count("asks whether"),
            "uptake_help_request_count": sum(str(x).lower() in {"yes", "1", "true"} for x in g.get("assistance_request", [])),
            "uptake_help_offer_count": sum(str(x).lower() in {"yes", "1", "true"} for x in g.get("assistance_offer", [])),
            "uptake_fear_count": combined.count("fear"),
            "uptake_grief_count": combined.count("grief"),
            "uptake_anger_count": combined.count("anger"),
            "uptake_solidarity_count": combined.count("solidarity"),
            "uptake_hope_count": combined.count("hope"),
            "uptake_contestation_count": combined.count("contestation") + combined.count("hostility"),
            "uptake_resource_sharing_count": combined.count("resource"),
            "uptake_coordination_count": combined.count("coordination"),
            "organization_response_visible": 1 if any(str(x).lower() in {"yes", "1", "true"} for x in g.get("organization_response_visible", [])) else 0,
        })
    return pd.DataFrame(rows)


def load_recirculation() -> pd.DataFrame:
    r = concat_files(RAW.glob("recirculation_batch_*.csv"))
    if r.empty or "item_id" not in r.columns:
        return pd.DataFrame()
    count_col = next((c for c in ["observed_recirculation_minimum", "minimum_observed_recirculation_count", "observed_trace_count"] if c in r.columns), None)
    if count_col:
        out = r[["item_id", count_col]].copy().rename(columns={count_col: "observed_recirculation_minimum"})
        return out.drop_duplicates("item_id", keep="last")
    return r.groupby("item_id").size().rename("observed_recirculation_minimum").reset_index()


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    items = normalize_verified_items()
    candidates = load_candidates()
    if items.empty:
        raise SystemExit("No verified communication_items_*.csv files found.")

    sampling = load_sampling_status()
    if not sampling.empty:
        items = items.merge(sampling, on="org_id", how="left")
    else:
        items["sampling_status"] = ""
        items["unit_of_analysis_note"] = ""

    items = derive_analysis_inclusion(items)
    for addon in [load_matched_messages(), load_engagement(), load_interaction_aggregates(), load_recirculation()]:
        if not addon.empty:
            items = items.merge(addon, on="item_id", how="left")

    strict = items[
        items["study_window"].fillna(False)
        & items["analysis_inclusion_status"].isin(["include", "program_level_only"])
        & items["item_id"].astype(str).ne("")
    ].copy()

    items.to_csv(PROCESSED / "communication_master_all_verified_v1.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    strict.to_csv(PROCESSED / "communication_master_primary_v1.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    if not candidates.empty:
        candidates.to_csv(PROCESSED / "communication_candidates_unresolved_v1.csv", index=False, quoting=csv.QUOTE_MINIMAL)

    qc = pd.DataFrame([
        {"metric": "verified_rows_all", "value": len(items)},
        {"metric": "primary_rows", "value": len(strict)},
        {"metric": "primary_organizations", "value": strict["org_id"].nunique()},
        {"metric": "primary_website_rows", "value": int((strict["platform_family"] == "website").sum())},
        {"metric": "primary_social_rows", "value": int((strict["platform_family"] == "social").sum())},
        {"metric": "day_precision_primary", "value": int((strict["date_precision"] == "day").sum())},
        {"metric": "non_day_precision_primary", "value": int((strict["date_precision"] != "day").sum())},
        {"metric": "excluded_or_duplicate_verified_rows", "value": int(items["analysis_inclusion_status"].isin(["exclude_from_primary_analysis", "duplicate_alias"]).sum())},
    ])
    qc.to_csv(PROCESSED / "communication_master_qc_summary_v1.csv", index=False)
    print(qc.to_string(index=False))


if __name__ == "__main__":
    main()
