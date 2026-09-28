from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
SAMPLING = ROOT / "sampling_frame"

ELIG = SAMPLING / "eligibility_universe_reconciliation_v2.csv"
REL = INTERIM / "organization_news_relations_primary_universe_v1.csv"
TYPOLOGY_COVERAGE = INTERIM / "organization_typology_full_universe_coverage_v1.csv"
OUT = PROCESSED / "organization_role_media_visibility_v1.csv"


def numeric_sum(series: pd.Series) -> int:
    return int(pd.to_numeric(series, errors="coerce").fillna(0).sum())


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    elig = pd.read_csv(ELIG, dtype=str).fillna("")
    elig = elig[elig["primary_universe_flag"].eq("1")].copy()
    rel = pd.read_csv(REL, dtype=str).fillna("")
    typ = pd.read_csv(TYPOLOGY_COVERAGE, dtype=str).fillna("")

    rows = []
    for e in elig.itertuples(index=False):
        grp = rel[rel["org_id"].eq(e.org_id)]
        t = typ[typ["org_id"].eq(e.org_id)]
        if len(t) != 1:
            raise RuntimeError(f"Expected exactly one typology coverage row for {e.org_id}; got {len(t)}")
        tr = t.iloc[0]

        layers = sorted([x for x in grp["media_layer"].unique() if x])
        outlets = sorted([x for x in grp["outlet_id"].unique() if x])
        rows.append({
            "org_id": e.org_id,
            "organization": e.organization_name,
            "screening_decision": e.screening_decision,
            "screening_evidence_certainty": e.evidence_certainty,
            "verified_typology_labels": tr["verified_labels"],
            "typology_label_count": int(tr["verified_label_count"]),
            "verified_news_edge_count": len(grp),
            "unique_news_story_count": grp["news_item_id"].nunique(),
            "unique_outlet_count": grp["outlet_id"].replace("", pd.NA).dropna().nunique(),
            "media_layer_count": len(layers),
            "media_layers_observed": ";".join(layers),
            "community_ethnic_edge_count": int(grp["media_layer"].eq("community_ethnic").sum()),
            "local_regional_edge_count": int(grp["media_layer"].eq("local_regional").sum()),
            "national_amplification_edge_count": int(grp["media_layer"].eq("national_amplification").sum()),
            "national_amplification_observed": 1 if grp["media_layer"].eq("national_amplification").any() else 0,
            "cross_layer_observed": 1 if len(layers) >= 2 else 0,
            "three_layer_observed": 1 if len(layers) >= 3 else 0,
            "direct_quote_edge_count": numeric_sum(grp["direct_quote"]) if len(grp) else 0,
            "substantive_interpretation_edge_count": numeric_sum(grp["substantive_interpretation"]) if len(grp) else 0,
            "resource_routing_edge_count": numeric_sum(grp["resource_routing"]) if len(grp) else 0,
            "mobilization_uptake_edge_count": numeric_sum(grp["mobilization_uptake"]) if len(grp) else 0,
            "legal_information_uptake_edge_count": numeric_sum(grp["legal_information_uptake"]) if len(grp) else 0,
            "service_uptake_edge_count": numeric_sum(grp["service_uptake"]) if len(grp) else 0,
            "media_visibility_status": "verified_edge_observed" if len(grp) else "no_verified_edge_in_current_corpus",
            "interpretation_note": "A zero edge count means no verified relation in the current collected corpus; it is not proof of zero media coverage.",
        })

    out = pd.DataFrame(rows).sort_values("org_id").reset_index(drop=True)
    if len(out) != 114:
        raise RuntimeError(f"Expected 114 organization rows; got {len(out)}")
    if (out["typology_label_count"] < 1).any():
        raise RuntimeError("Every primary-universe organization must have at least one verified typology label")
    out.to_csv(OUT, index=False)

    visible = int(out["verified_news_edge_count"].gt(0).sum())
    not_observed = int(out["verified_news_edge_count"].eq(0).sum())
    print(f"Organizations: {len(out)}")
    print(f"Verified media edge observed: {visible}")
    print(f"No verified edge in current corpus: {not_observed}")


if __name__ == "__main__":
    main()
