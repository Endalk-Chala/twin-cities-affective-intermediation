"""Build and validate the primary coded master corpus.

Outputs
-------
data/processed/full_corpus_coded_master_v1.csv
analysis/reproducibility_report_v1.md

The primary corpus contains verified communication items only. Candidate-tier
records remain separate in data/processed/candidate_tier_inventory_v1.csv.
"""
from pathlib import Path
import hashlib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUT = PROCESSED / "full_corpus_coded_master_v1.csv"
REPORT = ROOT / "analysis" / "reproducibility_report_v1.md"

PILOT_FILES = [
    PROCESSED / "ai_coding_pilot_batch_01_items_01_10.csv",
    PROCESSED / "ai_coding_pilot_batch_02_items_11_20.csv",
    PROCESSED / "ai_coding_pilot_batch_03_items_21_30.csv",
    PROCESSED / "ai_coding_pilot_batch_04_items_31_40.csv",
]

EXPANDED_FILES = [
    PROCESSED / "full_corpus_coding_batch_01_MMLA_CLUES_24items.csv",
    PROCESSED / "full_corpus_coding_batch_02_MMLA_CLUES_remaining_27items.csv",
    PROCESSED / "full_corpus_coding_batch_03_Advocates_OCM_IDN_19items.csv",
    PROCESSED / "full_corpus_coding_batch_04_ICOM_ISAIAH_CAPI_KOM_MCC_Arrive_23items.csv",
    PROCESSED / "full_corpus_coding_batch_05_remaining_staged_27items.csv",
    PROCESSED / "full_corpus_coding_batch_06_new_verified_social_6items.csv",
    PROCESSED / "full_corpus_coding_batch_07_Groundwork_JCA_24items.csv",
    PROCESSED / "full_corpus_coding_batch_08_CedarRiverside_PPL_24items.csv",
    PROCESSED / "full_corpus_coding_batch_09_PRISM_VOA_VLN_Habitat_AVIVO_Missions_37items.csv",
    PROCESSED / "full_corpus_coding_batch_10_ACER_ACLUMN_Isuroon_Alight_new_22items.csv",
    PROCESSED / "full_corpus_coding_batch_11_ILCM_CVT_IIMN_new_23items.csv",
    PROCESSED / "full_corpus_coding_batch_12_COPAL_Unidos_CVTadditional_31items.csv",
    PROCESSED / "full_corpus_coding_batch_13_early_batches_new_unique_10items.csv",
]

TARGET_COLUMNS = [
    "item_id","org_id","organization","date","platform","org_role_primary","org_role_secondary","role_hybrid_flag",
    "threat_appraisal","harm_loss_appraisal","injustice_appraisal","uncertainty_appraisal","responsibility_blame_appraisal",
    "intentionality_appraisal","norm_violation_appraisal","vulnerability_appraisal","controllability_appraisal","coping_efficacy_appraisal",
    "collective_efficacy_appraisal","care_need_appraisal","opportunity_hope_appraisal","fear_intensity","anxiety_uncertainty_intensity",
    "anger_intensity","moral_outrage_intensity","grief_sadness_intensity","solidarity_intensity","care_compassion_intensity",
    "empathy_intensity","hope_intensity","gratitude_intensity","pride_intensity","reassurance_intensity","defiance_intensity",
    "urgency_emotion_intensity","other_emotion_intensity","emotion_explicitness","emotion_source_org","emotion_source_affected_public",
    "emotion_source_supporters_public","emotion_source_quoted_actor","function_inform","function_warn","function_reassure","function_regulate_fear",
    "function_mobilize","function_advocate","function_provide_service","function_fundraise","function_build_solidarity","function_generate_empathy",
    "function_moral_evaluation","function_increase_efficacy","function_mourn_commemorate","function_document_testify","function_celebrate",
    "function_encourage_defiance","function_other","action_orientation_present","action_type","action_specificity","action_immediacy","audience_primary",
    "direct_address","urgency_level","legal_information_present","service_information_present","resource_link_present","appraisal_notes","emotion_notes",
    "coder_id","coding_date","coder_confidence"
]
SERIES_COLUMNS = ["series_id","series_label","series_type","series_analysis_note"]


def normalize_pilot() -> pd.DataFrame:
    pilot = pd.concat([pd.read_csv(p) for p in PILOT_FILES], ignore_index=True)
    supplement = pd.read_csv(PROCESSED / "pilot_schema_supplement_v1.csv")
    pilot = pilot.merge(supplement, on="item_id", how="left", validate="one_to_one")
    if pilot["org_role_primary"].isna().any():
        missing = pilot.loc[pilot["org_role_primary"].isna(), "item_id"].tolist()
        raise ValueError(f"Pilot supplement missing item(s): {missing}")
    pilot["appraisal_notes"] = pilot["appraisal_evidence_notes"]
    pilot["emotion_notes"] = pilot["emotion_evidence_notes"]
    pilot["coder_id"] = "GPT-5.6-Sol_full_corpus_v1"
    pilot["coding_date"] = "2026-09-24"
    pilot["coder_confidence"] = pilot["ai_coding_confidence"]
    for col in TARGET_COLUMNS:
        if col not in pilot.columns:
            pilot[col] = pd.NA
    return pilot[TARGET_COLUMNS]


def validate(master: pd.DataFrame) -> None:
    if len(master) != 337:
        raise ValueError(f"Expected 337 primary verified rows; found {len(master)}")
    if master["item_id"].nunique() != 337:
        raise ValueError(f"Expected 337 unique item_ids; found {master['item_id'].nunique()}")
    dup = master[master.duplicated("item_id", keep=False)]
    if not dup.empty:
        raise ValueError("Duplicate item_id(s) found:\n" + dup[["item_id","organization","date","platform"]].to_string(index=False))
    dates = pd.to_datetime(master["date"], errors="raise")
    lo, hi = pd.Timestamp("2025-11-01"), pd.Timestamp("2026-03-31")
    bad = master.loc[(dates < lo) | (dates > hi), ["item_id","date"]]
    if not bad.empty:
        raise ValueError("Rows outside study window:\n" + bad.to_string(index=False))
    if master["organization"].nunique() != 44:
        raise ValueError(f"Expected 44 organizations; found {master['organization'].nunique()}")
    platform_counts = master["platform"].value_counts().to_dict()
    expected = {"website": 317, "LinkedIn": 20}
    if platform_counts != expected:
        raise ValueError(f"Expected platform counts {expected}; found {platform_counts}")


def write_report(master: pd.DataFrame) -> None:
    month_counts = master.assign(month=master["date"].str[:7])["month"].value_counts().sort_index()
    platform_counts = master["platform"].value_counts()
    org_counts = master.groupby("organization").size().sort_values(ascending=False)
    recurring = master["series_id"].notna().sum()
    missing = master.isna().sum().sort_values(ascending=False)
    missing = missing[missing > 0]
    sha256 = hashlib.sha256(OUT.read_bytes()).hexdigest()

    lines = [
        "# Reproducibility Report — Full Coded Corpus v1",
        "",
        "## Build result",
        "",
        f"- Primary verified rows: **{len(master)}**",
        f"- Unique item IDs: **{master['item_id'].nunique()}**",
        f"- Organizations: **{master['organization'].nunique()}**",
        f"- Study window: **{master['date'].min()} to {master['date'].max()}**",
        f"- Website items: **{int(platform_counts.get('website', 0))}**",
        f"- LinkedIn items: **{int(platform_counts.get('LinkedIn', 0))}**",
        f"- Rows flagged as members of recurring series: **{recurring}**",
        "- Candidate-tier records are excluded from this master and retained separately.",
        f"- SHA-256 of master CSV: `{sha256}`",
        "",
        "## Validation checks",
        "",
        "- PASS: 337 rows",
        "- PASS: 337 unique `item_id` values",
        "- PASS: no duplicate `item_id` values",
        "- PASS: all dates fall within 2025-11-01 through 2026-03-31",
        "- PASS: 44 organizations",
        "- PASS: platform counts = 317 website + 20 LinkedIn",
        "",
        "## Monthly coverage",
        "",
        "| Month | Items |",
        "|---|---:|",
    ]
    lines += [f"| {month} | {int(n)} |" for month, n in month_counts.items()]
    lines += ["", "## Organization coverage", "", "| Organization | Items |", "|---|---:|"]
    lines += [f"| {org.replace('|','/')} | {int(n)} |" for org, n in org_counts.items()]
    lines += ["", "## Missingness", "", "Blank/NA fields are retained as missing and are not recoded as zero unless the coding protocol explicitly defines zero as observed absence.", "", "| Field | Missing rows |", "|---|---:|"]
    if len(missing):
        lines += [f"| `{field}` | {int(n)} |" for field, n in missing.items()]
    else:
        lines += ["| None | 0 |"]
    lines += [
        "",
        "## Rebuild",
        "",
        "Run:",
        "",
        "```bash",
        "python -m pip install pandas",
        "python analysis/build_full_corpus_master.py",
        "```",
        "",
        "The build reads the four original pilot files, the pilot schema supplement, the thirteen expanded coding batches, and the recurring-series map. It then validates the corpus and rewrites both the master CSV and this report.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    pilot = normalize_pilot()
    expanded = pd.concat([pd.read_csv(p) for p in EXPANDED_FILES], ignore_index=True)
    missing_cols = sorted(set(TARGET_COLUMNS) - set(expanded.columns))
    if missing_cols:
        raise ValueError(f"Expanded batches missing required columns: {missing_cols}")
    expanded = expanded[TARGET_COLUMNS]
    master = pd.concat([pilot, expanded], ignore_index=True)
    master["date"] = pd.to_datetime(master["date"], errors="raise").dt.strftime("%Y-%m-%d")

    series = pd.read_csv(PROCESSED / "recurring_series_map_v1.csv")
    series = series.rename(columns={"analysis_note": "series_analysis_note"})
    series = series[["item_id","series_id","series_label","series_type","series_analysis_note"]]
    master = master.merge(series, on="item_id", how="left", validate="one_to_one")
    master["is_recurring_series"] = master["series_id"].notna().astype(int)

    validate(master)
    master = master.sort_values(["date","organization","platform","item_id"], kind="stable").reset_index(drop=True)
    master.to_csv(OUT, index=False)
    write_report(master)

    print(f"Wrote {OUT}")
    print(f"Wrote {REPORT}")
    print(f"Rows: {len(master)}")
    print(f"Organizations: {master['organization'].nunique()}")
    print(master["platform"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
