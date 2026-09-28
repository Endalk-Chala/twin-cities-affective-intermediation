from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim"
SAMPLING = ROOT / "sampling_frame"

ALL_REL = INTERIM / "organization_news_relations_master_v1.csv"
ELIG = SAMPLING / "eligibility_universe_reconciliation_v2.csv"
OUT = INTERIM / "organization_news_relations_primary_universe_v1.csv"
EXCLUDED = INTERIM / "organization_news_relations_outside_primary_universe_v1.csv"
SUMMARY = INTERIM / "network_summary_primary_universe_v1.csv"


def main():
    rel = pd.read_csv(ALL_REL, dtype=str).fillna("")
    elig = pd.read_csv(ELIG, dtype=str).fillna("")

    status = elig[["org_id", "organization_name", "screening_decision", "primary_universe_flag", "evidence_certainty"]].drop_duplicates("org_id")
    joined = rel.merge(status, on="org_id", how="left", validate="many_to_one")

    if joined["primary_universe_flag"].eq("").any():
        missing = sorted(joined.loc[joined["primary_universe_flag"].eq(""), "org_id"].unique())
        raise RuntimeError(f"Verified news relations contain org IDs absent from eligibility reconciliation: {missing}")

    primary = joined[joined["primary_universe_flag"].eq("1")].copy()
    outside = joined[~joined["primary_universe_flag"].eq("1")].copy()

    primary.to_csv(OUT, index=False)
    outside.to_csv(EXCLUDED, index=False)

    rows = []
    for layer, grp in primary.groupby("media_layer"):
        rows.append({"metric": "media_layer_edges", "entity": layer, "count": len(grp), "notes": "Primary analytical universe only."})
    rows.extend([
        {"metric": "corpus_total", "entity": "verified_edges_primary_universe", "count": len(primary), "notes": "Eligible + probably eligible organizations only."},
        {"metric": "corpus_total", "entity": "unique_stories_primary_universe", "count": primary["news_item_id"].nunique(), "notes": "Normalized story IDs."},
        {"metric": "corpus_total", "entity": "organizations_primary_with_news", "count": primary["org_id"].nunique(), "notes": "Primary-universe organizations with >=1 verified news relation."},
        {"metric": "corpus_total", "entity": "outlets_primary", "count": primary["outlet_id"].nunique(), "notes": "Mapped outlets represented."},
        {"metric": "audit_difference", "entity": "verified_edges_outside_primary_universe", "count": len(outside), "notes": "Retained for provenance, excluded from primary analysis."},
        {"metric": "audit_difference", "entity": "organizations_outside_primary_with_verified_news", "count": outside["org_id"].nunique(), "notes": ";".join(sorted(outside["org_id"].unique()))},
    ])
    pd.DataFrame(rows).to_csv(SUMMARY, index=False)

    print(f"Audit verified edges: {len(rel)}")
    print(f"Primary-universe verified edges: {len(primary)}")
    print(f"Outside-primary verified edges retained: {len(outside)}")
    print(f"Primary organizations with news: {primary['org_id'].nunique()}")


if __name__ == "__main__":
    main()
