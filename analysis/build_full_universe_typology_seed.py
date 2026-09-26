from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim"
ELIG_PATH = ROOT / "sampling_frame" / "eligibility_universe_reconciliation_v2.csv"
OUT = INTERIM / "organization_typology_bridge_full_universe_seed_v1.csv"
COVERAGE = INTERIM / "organization_typology_full_universe_coverage_v1.csv"

# Conservative role assignments derived from explicit role/function language in the
# authoritative eligibility screening evidence. Existing manually reviewed typology
# files take precedence and are not duplicated here.
LABELS = {
"TC001":["education_workforce","immigrant_integration"],
"TC002":["education_workforce","immigrant_integration","community_rooted"],
"TC003":["community_rooted","ethnocultural","direct_service","immigrant_integration"],
"TC004":["community_rooted","ethnocultural","youth_family","immigrant_integration"],
"TC005":["education_workforce","immigrant_integration","direct_service"],
"TC006":["community_rooted","ethnocultural","youth_family","direct_service"],
"TC007":["direct_service"],
"TC008":["education_workforce","immigrant_integration"],
"TC010":["coalition_network","community_rooted","ethnocultural"],
"TC011":["community_rooted","direct_service","education_workforce","immigrant_integration"],
"TC012":["education_workforce","youth_family"],
"TC013":["community_rooted","ethnocultural","coalition_network"],
"TC014":["community_rooted","ethnocultural","youth_family","education_workforce","legal","direct_service"],
"TC017":["faith_based","direct_service","housing_economic","immigrant_integration"],
"TC021":["faith_based","direct_service","housing_economic","immigrant_integration"],
"TC022":["refugee_resettlement","immigrant_integration","direct_service","education_workforce","legal","faith_based"],
"TC023":["gender_based","direct_service","immigrant_integration"],
"TC024":["community_rooted","housing_economic","advocacy","immigrant_integration"],
"TC027":["faith_based","housing_economic","direct_service","immigrant_integration"],
"TC028":["community_rooted","ethnocultural","housing_economic","health_wellbeing","advocacy","organizing"],
"TC029":["community_rooted","ethnocultural","direct_service","housing_economic","education_workforce","immigrant_integration","advocacy"],
"TC030":["community_rooted","ethnocultural","housing_economic","education_workforce","direct_service"],
"TC031":["community_rooted","ethnocultural","housing_economic","education_workforce","direct_service"],
"TC032":["community_rooted","ethnocultural","direct_service"],
"TC033":["community_rooted","ethnocultural","direct_service","education_workforce","immigrant_integration","refugee_resettlement"],
"TC034":["faith_based","direct_service","housing_economic"],
"TC035":["refugee_resettlement","faith_based","direct_service","education_workforce","immigrant_integration","legal"],
"TC039":["faith_based","community_rooted","direct_service","education_workforce","immigrant_integration","legal"],
"TC040":["community_rooted","ethnocultural","gender_based","youth_family","health_wellbeing","education_workforce"],
"TC043":["community_rooted","ethnocultural","gender_based","health_wellbeing","advocacy","direct_service"],
"TC046":["community_rooted","ethnocultural","housing_economic","education_workforce","direct_service"],
"TC047":["community_rooted","ethnocultural","immigrant_integration","direct_service"],
"TC048":["education_workforce","immigrant_integration","direct_service"],
"TC051":["community_rooted","ethnocultural","refugee_resettlement","direct_service","immigrant_integration"],
"TC052":["community_rooted","ethnocultural","immigrant_integration","education_workforce","advocacy","direct_service"],
"TC053":["immigrant_integration","direct_service","legal","refugee_resettlement"],
"TC055":["community_rooted","direct_service","immigrant_integration"],
"TC056":["community_rooted","ethnocultural","direct_service","immigrant_integration"],
"TC059":["community_rooted","ethnocultural","gender_based","health_wellbeing","housing_economic","advocacy"],
"TC060":["community_rooted","ethnocultural","direct_service","refugee_resettlement","immigrant_integration"],
"TC061":["community_rooted","ethnocultural","refugee_resettlement","immigrant_integration","direct_service"],
"TC062":["direct_service","education_workforce","immigrant_integration"],
"TC063":["community_rooted","ethnocultural","direct_service","immigrant_integration","health_wellbeing","education_workforce"],
"TC066":["community_rooted","ethnocultural","direct_service","immigrant_integration","legal","advocacy"],
"TC067":["legal","faith_based","immigrant_integration","direct_service"],
"TC068":["legal","faith_based","immigrant_integration","direct_service","education_workforce"],
"TC069":["community_rooted","ethnocultural","education_workforce","immigrant_integration"],
"TC070":["community_rooted","ethnocultural","direct_service","education_workforce","immigrant_integration"],
"TC071":["community_rooted","ethnocultural","direct_service","immigrant_integration"],
"TC072":["community_rooted","ethnocultural","direct_service","immigrant_integration","legal"],
"TC076":["coalition_network","faith_based","advocacy","organizing","direct_service"],
"TC080":["faith_based","community_rooted","ethnocultural","advocacy","organizing","civil_rights_human_rights"],
"TC081":["community_rooted","advocacy","organizing","direct_service"],
"D1-01":["community_rooted","ethnocultural","direct_service","refugee_resettlement","immigrant_integration"],
"D2-04":["community_rooted","advocacy","organizing","direct_service","legal","civil_rights_human_rights"],
"D3-01":["community_rooted","direct_service","immigrant_integration","education_workforce","legal","health_wellbeing","refugee_resettlement"],
"D3-02":["community_rooted","ethnocultural","media_information"],
"D3-03":["community_rooted","ethnocultural","direct_service","education_workforce","immigrant_integration"],
"D3-04":["community_rooted","gender_based","direct_service","legal","immigrant_integration"],
"D3-05":["community_rooted","ethnocultural","advocacy"],
"D3-06":["community_rooted","ethnocultural","education_workforce","youth_family"],
"D3-07":["community_rooted","ethnocultural"],
"D3-08":["community_rooted","ethnocultural"],
"D3-09":["community_rooted","ethnocultural","youth_family","advocacy","organizing"],
"D3-10":["community_rooted","ethnocultural"],
"D3-11":["community_rooted","ethnocultural"],
"D3-12":["community_rooted","ethnocultural","direct_service","immigrant_integration"],
"D3-14":["coalition_network","community_rooted","ethnocultural","advocacy","education_workforce"],
"D3-15":["community_rooted","ethnocultural","advocacy"],
"D3-18":["media_information","community_rooted","ethnocultural","education_workforce"],
"D3-19":["community_rooted","ethnocultural","housing_economic","advocacy"],
"D3-20":["community_rooted","ethnocultural","education_workforce","youth_family"],
"D3-21":["faith_based","direct_service","immigrant_integration"],
"D4-01":["community_rooted","ethnocultural","direct_service","immigrant_integration","education_workforce","housing_economic","advocacy"],
"D4-03":["community_rooted","ethnocultural","direct_service","immigrant_integration"],
"D4-04":["community_rooted","ethnocultural","youth_family","health_wellbeing","direct_service"],
"D4-05":["community_rooted","ethnocultural","direct_service","immigrant_integration"],
"D4-06":["community_rooted","ethnocultural","health_wellbeing","direct_service"],
"D4-07":["community_rooted","ethnocultural","youth_family","education_workforce","advocacy","direct_service"],
"D4-08":["community_rooted","ethnocultural","health_wellbeing"],
"D4-09":["community_rooted","ethnocultural","housing_economic"],
"D4-10":["community_rooted","ethnocultural","direct_service","education_workforce","health_wellbeing","immigrant_integration","youth_family"],
"D4-11":["direct_service"],
}

# These organizations have enough evidence for a role hypothesis, but the screening
# record explicitly says current organizational/activity/form evidence remains weak.
# Their seed labels therefore remain candidate until source-level manual verification.
CANDIDATE_ROLE_ORGS = {
    "TC001", "TC004", "TC006", "TC032", "TC034", "TC080",
    "D3-07", "D3-08", "D3-10", "D3-19", "D4-08", "D4-09", "D4-11",
}


def evidence_basis(url: str) -> str:
    u = str(url).lower()
    if any(x in u for x in ["mn.gov", "state.mn.us", "ag.state.mn.us", "house.mn.gov", "revisor.mn.gov", "health.mn.gov", "health.state.mn.us"]):
        return "government_or_partner_listing"
    return "official_about_page"


def main():
    elig = pd.read_csv(ELIG_PATH, dtype=str).fillna("")
    primary = elig[elig["primary_universe_flag"].eq("1")].copy()

    existing_parts = []
    for p in [INTERIM / "organization_typology_bridge_v1.csv", INTERIM / "organization_typology_bridge_media_visible_completion_v1.csv"]:
        if p.exists():
            existing_parts.append(pd.read_csv(p, dtype=str).fillna(""))
    existing = pd.concat(existing_parts, ignore_index=True) if existing_parts else pd.DataFrame(columns=["org_id", "type_label", "type_status"])
    existing_primary_ids = set(existing["org_id"]) & set(primary["org_id"])

    missing_mapping = sorted(set(primary["org_id"]) - existing_primary_ids - set(LABELS))
    extra_mapping = sorted(set(LABELS) - set(primary["org_id"]))
    if missing_mapping:
        raise RuntimeError(f"Primary-universe organizations missing typology seed mapping: {missing_mapping}")
    if extra_mapping:
        raise RuntimeError(f"Typology seed mappings point outside primary universe: {extra_mapping}")

    rows = []
    for r in primary.itertuples(index=False):
        if r.org_id in existing_primary_ids:
            continue
        labels = LABELS.get(r.org_id, [])
        status = "candidate" if r.org_id in CANDIDATE_ROLE_ORGS else "verified"
        url = r.evidence_url_1 or r.evidence_url_2
        note_prefix = "Candidate role seed" if status == "candidate" else "Verified role seed"
        for label in labels:
            rows.append({
                "org_id": r.org_id,
                "organization": r.organization_name,
                "type_label": label,
                "type_status": status,
                "evidence_basis": evidence_basis(url),
                "evidence_url": url,
                "evidence_note": f"{note_prefix} from authoritative eligibility-screening evidence: {r.evidence_summary}",
                "coding_date": "2026-09-26",
            })

    seed = pd.DataFrame(rows).sort_values(["org_id", "type_label"])
    seed.to_csv(OUT, index=False)

    all_typ = pd.concat([existing, seed], ignore_index=True, sort=False).fillna("")
    coverage = []
    for r in primary.itertuples(index=False):
        grp = all_typ[all_typ["org_id"].eq(r.org_id)]
        verified = sorted(grp.loc[grp["type_status"].eq("verified"), "type_label"].unique())
        candidate = sorted(grp.loc[grp["type_status"].eq("candidate"), "type_label"].unique())
        coverage.append({
            "org_id": r.org_id,
            "organization": r.organization_name,
            "screening_decision": r.screening_decision,
            "verified_label_count": len(verified),
            "candidate_label_count": len(candidate),
            "verified_labels": ";".join(verified),
            "candidate_labels": ";".join(candidate),
            "typology_review_status": "verified_labels_present" if verified else "candidate_only_manual_review_needed",
        })
    cov = pd.DataFrame(coverage)
    if len(cov) != 114:
        raise RuntimeError(f"Expected 114 primary-universe organizations; got {len(cov)}")
    cov.to_csv(COVERAGE, index=False)

    print(f"Primary universe organizations: {len(cov)}")
    print(f"Organizations with >=1 verified label: {(cov['verified_label_count'] > 0).sum()}")
    print(f"Candidate-only organizations requiring manual role verification: {(cov['verified_label_count'] == 0).sum()}")
    print(f"Seed typology rows created: {len(seed)}")


if __name__ == "__main__":
    main()
