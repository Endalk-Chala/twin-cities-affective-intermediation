from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim"

REL = INTERIM / "organization_news_relations_primary_universe_v1.csv"
BASE_TYP_FILES = [
    INTERIM / "organization_typology_bridge_v1.csv",
    INTERIM / "organization_typology_bridge_media_visible_completion_v1.csv",
]
OUT = INTERIM / "role_organization_outlet_layer_edges_v1.csv"
SUMMARY = INTERIM / "role_media_layer_summary_v1.csv"
COVERAGE = INTERIM / "typology_network_coverage_v1.csv"


def main():
    rel = pd.read_csv(REL, dtype=str).fillna("")
    typ_files = BASE_TYP_FILES + sorted(INTERIM.glob("organization_typology_bridge_full_universe_*.csv"))
    typ_parts = [pd.read_csv(p, dtype=str).fillna("") for p in typ_files if p.exists()]
    if not typ_parts:
        raise SystemExit("No typology bridge files found")
    typ = pd.concat(typ_parts, ignore_index=True).drop_duplicates(
        subset=["org_id", "type_label", "type_status", "evidence_url", "evidence_note"]
    )

    verified_typ = typ[typ["type_status"].eq("verified")].copy()
    core = rel.merge(
        verified_typ[["org_id", "organization", "type_label"]],
        on="org_id",
        how="left",
    ).fillna("")

    role_edges = core[core["type_label"].ne("")].copy()
    role_edges = role_edges[[
        "type_label", "org_id", "organization", "relation_id", "news_item_id",
        "outlet_id", "media_layer", "visibility_type", "direct_quote",
        "source_prominence", "source_function_primary", "substantive_interpretation",
        "resource_routing", "mobilization_uptake", "fundraising_uptake",
        "service_uptake", "legal_information_uptake", "verification_status"
    ]].sort_values(["type_label", "org_id", "outlet_id", "news_item_id"])
    role_edges.to_csv(OUT, index=False)

    summary = (
        role_edges.groupby(["type_label", "media_layer"], dropna=False)
        .agg(
            edge_count=("relation_id", "count"),
            unique_organizations=("org_id", "nunique"),
            unique_outlets=("outlet_id", "nunique"),
            unique_stories=("news_item_id", "nunique"),
            direct_quote_edges=("direct_quote", lambda s: pd.to_numeric(s, errors="coerce").fillna(0).sum()),
        )
        .reset_index()
        .sort_values(["type_label", "media_layer"])
    )
    summary.to_csv(SUMMARY, index=False)

    all_orgs = sorted(rel["org_id"].unique())
    coded_orgs = set(verified_typ["org_id"].unique())
    coverage = []
    for org in all_orgs:
        grp = rel[rel["org_id"].eq(org)]
        labels = sorted(verified_typ.loc[verified_typ["org_id"].eq(org), "type_label"].unique())
        coverage.append({
            "org_id": org,
            "verified_news_edges": len(grp),
            "verified_typology_labels": ";".join(labels),
            "typology_label_count": len(labels),
            "typology_status_for_network": "coded" if org in coded_orgs else "not_yet_coded",
            "media_layer_count": grp["media_layer"].nunique(),
        })
    pd.DataFrame(coverage).to_csv(COVERAGE, index=False)

    print(f"Primary-universe news organizations: {len(all_orgs)}")
    print(f"Organizations with verified typology labels: {len(coded_orgs & set(all_orgs))}")
    print(f"Role-expanded multilayer edges: {len(role_edges)}")
    print(f"Role labels represented: {role_edges['type_label'].nunique()}")


if __name__ == "__main__":
    main()
