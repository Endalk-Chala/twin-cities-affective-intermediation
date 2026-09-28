from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
INTERIM_DIR = ROOT / "data" / "interim"
REGISTRY_PATH = ROOT / "platform_registry" / "news_outlet_registry_v2.csv"

MASTER_PATH = INTERIM_DIR / "organization_news_relations_master_v1.csv"
CROSSWALK_PATH = INTERIM_DIR / "news_item_id_crosswalk_v1.csv"
SUMMARY_PATH = INTERIM_DIR / "network_summary_full_v1.csv"
UNMAPPED_PATH = INTERIM_DIR / "news_network_qc_unmapped_outlets_v1.csv"
CANDIDATE_PATH = INTERIM_DIR / "organization_news_relations_candidates_v1.csv"

MASTER_COLUMNS = [
    "relation_id", "news_item_id", "org_id", "outlet_id", "media_layer",
    "visibility_type", "headline_presence", "lead_presence", "direct_quote",
    "quote_count", "paraphrased", "spokesperson_named", "spokesperson_name",
    "spokesperson_title", "source_prominence", "source_function_primary",
    "source_function_secondary", "substantive_interpretation", "resource_routing",
    "mobilization_uptake", "fundraising_uptake", "service_uptake",
    "legal_information_uptake", "safety_guidance_uptake", "testimonial_uptake",
    "org_affect_terms", "journalist_affect_terms", "dominant_affect",
    "frame_transformation", "local_to_national_amplification",
    "amplification_path_id", "matched_org_item_id", "match_confidence",
    "evidence_fragment", "verification_status", "coder_notes"
]

ALIASES = {
    "minnesota star tribune": "star tribune",
    "star tribune": "star tribune",
    "cbs minnesota / wcco": "cbs minnesota / wcco",
    "cbs minnesota/wcco": "cbs minnesota / wcco",
    "community reporter": "community reporter",
    "the imprint": "the imprint",
    "tc jewfolk": "tc jewfolk",
    "hmong daily news": "hmong daily news",
    "boreal community media": "boreal community media",
}


def norm_text(value: object) -> str:
    s = "" if value is None else str(value)
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def split_semicolon(value: object) -> list[str]:
    s = "" if value is None else str(value).strip()
    if not s or s.lower() == "nan":
        return []
    return [p.strip() for p in s.split(";") if p.strip()]


def truthy(value: object) -> int:
    s = norm_text(value)
    return 1 if s in {"1", "true", "yes", "y"} else 0


def canonical_outlet_name(name: str) -> str:
    n = norm_text(name)
    return ALIASES.get(n, n)


def story_id(date: str, outlet: str, headline: str, url: str) -> str:
    # Date + outlet + headline are intentionally primary: this collapses hosted copies
    # and duplicate raw IDs for the same journalistic item while preserving source IDs
    # in the crosswalk.
    key = "|".join([norm_text(date), canonical_outlet_name(outlet), norm_text(headline)])
    if not norm_text(headline):
        key += "|" + norm_text(url)
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12].upper()
    return f"STY-{digest}"


def visibility_type(raw_visibility: str, quoted: int) -> str:
    v = norm_text(raw_visibility)
    if quoted or "direct_quote" in v or "statement_quote" in v or "mixed_mention_and_quote" in v:
        return "direct_quote"
    if "paraphrase" in v:
        return "paraphrase"
    if any(x in v for x in ["resource", "cited_guidance"]):
        return "resource_listing"
    if any(x in v for x in ["beneficiary", "partner_visibility"]):
        return "beneficiary_or_partner"
    if "passing" in v:
        return "passing_mention"
    return "named_mention"


def prominence(raw_visibility: str) -> str:
    v = norm_text(raw_visibility)
    if "resource" in v:
        return "resource_only"
    if v.startswith("primary") or "primary_story_subject" in v or "primary_subject" in v:
        return "primary"
    if v.startswith("secondary"):
        return "secondary"
    if any(x in v for x in ["passing", "co_signatory", "participating_organization"]):
        return "passing"
    return "supporting"


def infer_mobilization(source_function: str, raw_visibility: str, action_info: int) -> int:
    s = norm_text(source_function + " " + raw_visibility)
    return 1 if action_info and any(x in s for x in ["mobil", "organizer", "collective_action", "advocacy", "coordination", "rally", "faith"]) else 0


def infer_fundraising(topic: str, notes: str, raw_visibility: str) -> int:
    s = norm_text(" ".join([topic, notes, raw_visibility]))
    return 1 if any(x in s for x in ["fundrais", "donat", "proceeds", "benefit concert", "recipient", "profits to", "give to the max"]) else 0


def pick_aligned(values: list[str], idx: int, n_orgs: int, *, repeat_last: bool = False, first_only: bool = False) -> str:
    if not values:
        return ""
    if len(values) == n_orgs:
        return values[idx]
    if len(values) == 1:
        if first_only and idx > 0:
            return ""
        return values[0]
    if idx < len(values):
        return values[idx]
    return values[-1] if repeat_last else ""


def load_registry() -> tuple[dict[str, dict[str, str]], pd.DataFrame]:
    reg = pd.read_csv(REGISTRY_PATH, dtype=str).fillna("")
    mapping: dict[str, dict[str, str]] = {}
    for _, r in reg.iterrows():
        mapping[canonical_outlet_name(r["outlet_name"])] = r.to_dict()
    return mapping, reg


def build() -> None:
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    outlet_map, registry = load_registry()

    batch_paths = sorted(RAW_DIR.glob("news_media_uptake_batch_*.csv"))
    expanded: list[dict[str, object]] = []
    crosswalk: list[dict[str, str]] = []
    unmapped: list[dict[str, str]] = []

    for path in batch_paths:
        try:
            df = pd.read_csv(path, dtype=str, keep_default_na=False)
        except Exception as exc:
            print(f"Skipping unreadable {path.name}: {exc}")
            continue
        required = {"news_item_id", "date", "outlet", "headline", "org_id", "organization", "collection_status"}
        if not required.issubset(df.columns):
            print(f"Skipping incompatible {path.name}")
            continue

        for _, row in df.iterrows():
            raw_id = row.get("news_item_id", "")
            normalized_story_id = story_id(row.get("date", ""), row.get("outlet", ""), row.get("headline", ""), row.get("url", ""))
            crosswalk.append({
                "source_batch": path.name,
                "source_news_item_id": raw_id,
                "normalized_news_item_id": normalized_story_id,
                "date": row.get("date", ""),
                "outlet": row.get("outlet", ""),
                "headline": row.get("headline", ""),
                "url": row.get("url", ""),
            })

            org_ids = split_semicolon(row.get("org_id", "")) or [row.get("org_id", "")]
            org_names = split_semicolon(row.get("organization", "")) or [row.get("organization", "")]
            spokespeople = split_semicolon(row.get("spokesperson", ""))
            functions = split_semicolon(row.get("source_function", ""))
            n_orgs = max(len(org_ids), len(org_names), 1)

            out_key = canonical_outlet_name(row.get("outlet", ""))
            out = outlet_map.get(out_key)
            outlet_id = out["outlet_id"] if out else ""
            media_layer = out["media_layer"] if out else "unmapped"
            if not out:
                unmapped.append({
                    "source_batch": path.name,
                    "source_news_item_id": raw_id,
                    "normalized_news_item_id": normalized_story_id,
                    "outlet": row.get("outlet", ""),
                    "date": row.get("date", ""),
                    "headline": row.get("headline", ""),
                    "collection_status": row.get("collection_status", ""),
                })

            for idx in range(n_orgs):
                org_id = pick_aligned(org_ids, idx, n_orgs, repeat_last=True)
                org_name = pick_aligned(org_names, idx, n_orgs, repeat_last=True)
                spokesperson = pick_aligned(spokespeople, idx, n_orgs, first_only=True)
                source_function = pick_aligned(functions, idx, n_orgs, repeat_last=True)
                quoted = truthy(row.get("organization_quoted", ""))
                raw_visibility = row.get("organization_visibility", "")
                legal = truthy(row.get("legal_info_carryover", ""))
                service = truthy(row.get("service_info_carryover", ""))
                action = truthy(row.get("action_info_carryover", ""))
                vtype = visibility_type(raw_visibility, quoted)
                prom = prominence(raw_visibility)
                substantive = 1 if (quoted or prom in {"primary", "secondary"}) and vtype != "resource_listing" else 0
                resource_routing = 1 if (service or vtype == "resource_listing") else 0
                mobilization = infer_mobilization(source_function, raw_visibility, action)
                fundraising = infer_fundraising(row.get("news_topic", ""), row.get("collection_notes", ""), raw_visibility)

                expanded.append({
                    "news_item_id": normalized_story_id,
                    "org_id": org_id,
                    "organization": org_name,
                    "outlet_id": outlet_id,
                    "outlet_name": row.get("outlet", ""),
                    "media_layer": media_layer,
                    "visibility_type": vtype,
                    "headline_presence": "",
                    "lead_presence": "",
                    "direct_quote": quoted,
                    "quote_count": "",
                    "paraphrased": 1 if vtype == "paraphrase" else 0,
                    "spokesperson_named": 1 if spokesperson else 0,
                    "spokesperson_name": spokesperson,
                    "spokesperson_title": "",
                    "source_prominence": prom,
                    "source_function_primary": source_function,
                    "source_function_secondary": "",
                    "substantive_interpretation": substantive,
                    "resource_routing": resource_routing,
                    "mobilization_uptake": mobilization,
                    "fundraising_uptake": fundraising,
                    "service_uptake": service,
                    "legal_information_uptake": legal,
                    "safety_guidance_uptake": "",
                    "testimonial_uptake": "",
                    "org_affect_terms": "",
                    "journalist_affect_terms": "",
                    "dominant_affect": "none_not_assessable",
                    "frame_transformation": "not_assessable" if norm_text(row.get("frame_transformation", "")) in {"", "not_yet_coded"} else row.get("frame_transformation", ""),
                    "local_to_national_amplification": 0,
                    "amplification_path_id": "",
                    "matched_org_item_id": row.get("matched_org_item_id", ""),
                    "match_confidence": row.get("match_confidence", ""),
                    "evidence_fragment": "",
                    "verification_status": row.get("collection_status", ""),
                    "coder_notes": f"source_batch={path.name}; source_news_item_id={raw_id}; {row.get('collection_notes', '')}",
                })

    edges = pd.DataFrame(expanded)
    if edges.empty:
        raise SystemExit("No news-media rows were loaded")

    # Deduplicate the same organization in the same normalized journalistic item.
    # Prefer verified rows, then rows with direct quotation, then substantive interpretation.
    edges["_verified_rank"] = edges["verification_status"].map(lambda x: 1 if norm_text(x) == "verified" else 0)
    edges["_quote_rank"] = pd.to_numeric(edges["direct_quote"], errors="coerce").fillna(0)
    edges["_substantive_rank"] = pd.to_numeric(edges["substantive_interpretation"], errors="coerce").fillna(0)
    edges = edges.sort_values(["news_item_id", "org_id", "_verified_rank", "_quote_rank", "_substantive_rank"], ascending=[True, True, False, False, False])
    edges = edges.drop_duplicates(subset=["news_item_id", "org_id"], keep="first")

    verified = edges[edges["verification_status"].map(norm_text) == "verified"].copy()
    candidates = edges[edges["verification_status"].map(norm_text) != "verified"].copy()

    verified = verified.sort_values(["news_item_id", "org_id"]).reset_index(drop=True)
    verified.insert(0, "relation_id", [f"R{i:04d}" for i in range(1, len(verified) + 1)])
    candidates = candidates.sort_values(["news_item_id", "org_id"]).reset_index(drop=True)
    candidates.insert(0, "relation_id", [f"C{i:04d}" for i in range(1, len(candidates) + 1)])

    for frame in (verified, candidates):
        frame.drop(columns=[c for c in ["organization", "outlet_name", "_verified_rank", "_quote_rank", "_substantive_rank"] if c in frame.columns], inplace=True)
        for c in MASTER_COLUMNS:
            if c not in frame.columns:
                frame[c] = ""
        frame = frame[MASTER_COLUMNS]

    verified = verified[MASTER_COLUMNS]
    candidates = candidates[MASTER_COLUMNS]
    verified.to_csv(MASTER_PATH, index=False, quoting=csv.QUOTE_MINIMAL)
    candidates.to_csv(CANDIDATE_PATH, index=False, quoting=csv.QUOTE_MINIMAL)

    cross = pd.DataFrame(crosswalk).drop_duplicates().sort_values(["normalized_news_item_id", "source_batch", "source_news_item_id"])
    cross.to_csv(CROSSWALK_PATH, index=False)

    unmapped_df = pd.DataFrame(unmapped).drop_duplicates()
    if not unmapped_df.empty:
        unmapped_df = unmapped_df.sort_values(["collection_status", "outlet", "date"])
    unmapped_df.to_csv(UNMAPPED_PATH, index=False)

    # Network summary: edge counts, unique-story counts, and distinct-layer reach.
    org_names: dict[str, str] = {}
    # Recover organization labels from source rows before they were removed.
    for r in expanded:
        if r.get("org_id") and r.get("organization"):
            org_names[str(r["org_id"])] = str(r["organization"])
    outlet_names = dict(zip(registry["outlet_id"], registry["outlet_name"]))

    summary_rows: list[dict[str, object]] = []
    for layer, count in verified["media_layer"].value_counts(dropna=False).items():
        summary_rows.append({"metric": "media_layer_edges", "entity_id": "", "entity_name": layer, "count": int(count), "notes": "Verified deduplicated organization-story edges."})

    for org_id, grp in verified.groupby("org_id"):
        summary_rows.append({"metric": "organization_edges", "entity_id": org_id, "entity_name": org_names.get(org_id, org_id), "count": len(grp), "notes": f"unique_stories={grp['news_item_id'].nunique()}; media_layers={grp['media_layer'].nunique()}"})

    mapped = verified[verified["outlet_id"] != ""]
    for outlet_id, grp in mapped.groupby("outlet_id"):
        summary_rows.append({"metric": "outlet_edges", "entity_id": outlet_id, "entity_name": outlet_names.get(outlet_id, outlet_id), "count": len(grp), "notes": f"unique_orgs={grp['org_id'].nunique()}; unique_stories={grp['news_item_id'].nunique()}"})

    summary_rows.extend([
        {"metric": "corpus_total", "entity_id": "", "entity_name": "verified_edges", "count": len(verified), "notes": "After story/org deduplication."},
        {"metric": "corpus_total", "entity_id": "", "entity_name": "verified_unique_stories", "count": verified["news_item_id"].nunique(), "notes": "Normalized by date + outlet + headline."},
        {"metric": "corpus_total", "entity_id": "", "entity_name": "verified_organizations", "count": verified["org_id"].nunique(), "notes": "Organizations with at least one verified news relation."},
        {"metric": "corpus_total", "entity_id": "", "entity_name": "verified_outlets_mapped", "count": mapped["outlet_id"].nunique(), "notes": "Registered outlets represented in verified network."},
        {"metric": "corpus_total", "entity_id": "", "entity_name": "unmapped_verified_edges", "count": int(((verified["outlet_id"] == "")).sum()), "notes": "Resolve before final network analysis."},
        {"metric": "corpus_total", "entity_id": "", "entity_name": "candidate_edges", "count": len(candidates), "notes": "Kept outside verified master counts."},
    ])
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(SUMMARY_PATH, index=False)

    print(f"Processed {len(batch_paths)} news batch files")
    print(f"Verified edges: {len(verified)}")
    print(f"Candidate/nonverified edges: {len(candidates)}")
    print(f"Unique verified stories: {verified['news_item_id'].nunique()}")
    print(f"Unmapped verified edges: {(verified['outlet_id'] == '').sum()}")


if __name__ == "__main__":
    build()
