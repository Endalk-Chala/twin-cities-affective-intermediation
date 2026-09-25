"""Build and validate the primary coded master corpus (v2).

This version includes a deterministic schema-alignment parser for the four
legacy pilot CSVs. The legacy files contain occasional missing/split CSV fields;
they are preserved unchanged. The parser aligns each parsed row to the 74-column
pilot schema using field-type constraints, allowing explicit blank insertion and
adjacent-token merging only when needed.

Outputs:
  data/processed/full_corpus_coded_master_v1.csv
  analysis/reproducibility_report_v1.md
"""
from pathlib import Path
from functools import lru_cache
import csv
import hashlib
import re
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

BINARY = {
    "coding_abstain","ambiguity_flag","threat_appraisal","harm_loss_appraisal","injustice_appraisal",
    "uncertainty_appraisal","responsibility_blame_appraisal","intentionality_appraisal","norm_violation_appraisal",
    "vulnerability_appraisal","controllability_appraisal","coping_efficacy_appraisal","collective_efficacy_appraisal",
    "care_need_appraisal","opportunity_hope_appraisal","function_inform","function_warn","function_reassure",
    "function_regulate_fear","function_mobilize","function_advocate","function_provide_service","function_fundraise",
    "function_build_solidarity","function_generate_empathy","function_moral_evaluation","function_increase_efficacy",
    "function_mourn_commemorate","function_document_testify","function_celebrate","function_encourage_defiance",
    "function_other","action_orientation_present","direct_address","legal_information_present","service_information_present",
    "resource_link_present"
}
INTENSITY = {
    "fear_intensity","anxiety_uncertainty_intensity","anger_intensity","moral_outrage_intensity","grief_sadness_intensity",
    "solidarity_intensity","care_compassion_intensity","empathy_intensity","hope_intensity","gratitude_intensity","pride_intensity",
    "reassurance_intensity","defiance_intensity","urgency_emotion_intensity","other_emotion_intensity","urgency_level"
}


def field_score(name, value):
    v = "" if value is None else str(value)
    if name == "pilot_order": return 15 if re.fullmatch(r"\d+", v) else -30
    if name == "date": return 15 if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) else -30
    if name == "platform": return 15 if v in {"website","LinkedIn"} else -30
    if name == "coding_source_quality": return 10 if v in {"summary_plus_title","full_text","title_only"} else -15
    if name == "ai_coding_confidence": return 10 if v in {"high","medium","low"} else -15
    if name in BINARY: return 7 if v in {"0","1",""} else -12
    if name in INTENSITY: return 7 if v in {"0","1","2","3",""} else -12
    if name == "action_specificity": return 8 if v in {"none","general","specific",""} else -12
    if name == "action_immediacy": return 8 if v in {"none","low","moderate","high",""} else -12
    if name == "ai_coder_id": return 8 if (v.startswith("GPT-") or v == "") else -8
    if name in {"item_id","org_id","organization","title","audience_primary","action_type"}: return 2 if v != "" else 0
    return 1


def align_row(header, tokens, path_name, line_no):
    """Align a legacy row to header using normal, blank-insert, and merge steps."""
    H, T = len(header), len(tokens)

    @lru_cache(None)
    def dp(i, j):
        if i == H and j == T:
            return (0, ())
        if i == H:
            return None
        remaining_h, remaining_t = H - i, T - j
        # At most a few malformed positions exist per row; prune impossible states.
        if remaining_t > remaining_h + 4 or remaining_h > remaining_t + 4:
            return None
        choices = []
        # normal mapping
        if j < T:
            tail = dp(i + 1, j + 1)
            if tail is not None:
                choices.append((field_score(header[i], tokens[j]) + tail[0], (tokens[j],) + tail[1]))
        # insert an explicit missing field; penalize so it is used only when needed
        tail = dp(i + 1, j)
        if tail is not None:
            choices.append((field_score(header[i], "") - 5 + tail[0], ("",) + tail[1]))
        # merge two adjacent parsed tokens into one field; penalize slightly
        if j + 1 < T:
            merged = tokens[j] + "," + tokens[j + 1]
            tail = dp(i + 1, j + 2)
            if tail is not None:
                choices.append((field_score(header[i], merged) - 3 + tail[0], (merged,) + tail[1]))
        if not choices:
            return None
        choices.sort(key=lambda x: x[0], reverse=True)
        return choices[0]

    result = dp(0, 0)
    if result is None or len(result[1]) != H:
        raise ValueError(f"Could not align legacy row {path_name}:{line_no} ({T} tokens to {H} fields)")
    score, aligned = result
    # hard validation of stable anchors
    d = dict(zip(header, aligned))
    required = {
        "pilot_order": r"\d+",
        "date": r"\d{4}-\d{2}-\d{2}",
    }
    for name, pattern in required.items():
        if not re.fullmatch(pattern, str(d.get(name, ""))):
            raise ValueError(f"Legacy alignment failed anchor {name} for {path_name}:{line_no}")
    if d.get("platform") not in {"website","LinkedIn"}:
        raise ValueError(f"Legacy alignment failed platform for {path_name}:{line_no}")
    print(f"Legacy aligned {path_name}:{line_no}: tokens={T}, fields={H}, score={score}")
    return list(aligned)


def read_legacy_pilot(path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    header = rows[0]
    aligned = [align_row(header, row, path.name, n) for n, row in enumerate(rows[1:], start=2)]
    return pd.DataFrame(aligned, columns=header)


def normalize_pilot():
    pilot = pd.concat([read_legacy_pilot(p) for p in PILOT_FILES], ignore_index=True)
    supplement = pd.read_csv(PROCESSED / "pilot_schema_supplement_v1.csv")
    pilot = pilot.merge(supplement, on="item_id", how="left", validate="one_to_one")
    if pilot["org_role_primary"].isna().any():
        missing = pilot.loc[pilot["org_role_primary"].isna(), "item_id"].tolist()
        raise ValueError(f"Pilot supplement missing item(s): {missing}")
    pilot["appraisal_notes"] = pilot.get("appraisal_evidence_notes", pd.Series(pd.NA, index=pilot.index))
    pilot["emotion_notes"] = pilot.get("emotion_evidence_notes", pd.Series(pd.NA, index=pilot.index))
    pilot["coder_id"] = "GPT-5.6-Sol_full_corpus_v1"
    pilot["coding_date"] = "2026-09-24"
    pilot["coder_confidence"] = pilot["ai_coding_confidence"]
    for col in TARGET_COLUMNS:
        if col not in pilot.columns:
            pilot[col] = pd.NA
    return pilot[TARGET_COLUMNS]


def validate(master):
    checks = []
    checks.append((len(master) == 337, f"rows={len(master)} expected=337"))
    checks.append((master["item_id"].nunique() == 337, f"unique_item_ids={master['item_id'].nunique()} expected=337"))
    checks.append((not master["item_id"].duplicated().any(), "duplicate item_id check"))
    dates = pd.to_datetime(master["date"], errors="raise")
    checks.append((((dates >= pd.Timestamp("2025-11-01")) & (dates <= pd.Timestamp("2026-03-31"))).all(), "study-window date check"))
    checks.append((master["organization"].nunique() == 44, f"organizations={master['organization'].nunique()} expected=44"))
    pc = master["platform"].value_counts().to_dict()
    checks.append((pc == {"website":317,"LinkedIn":20}, f"platform_counts={pc}"))
    failed = [msg for ok, msg in checks if not ok]
    if failed:
        raise ValueError("Validation failed: " + "; ".join(failed))


def write_report(master):
    month_counts = master.assign(month=master["date"].str[:7])["month"].value_counts().sort_index()
    platform_counts = master["platform"].value_counts()
    org_counts = master.groupby("organization").size().sort_values(ascending=False)
    recurring = int(master["series_id"].notna().sum())
    missing = master.isna().sum().sort_values(ascending=False)
    missing = missing[missing > 0]
    sha256 = hashlib.sha256(OUT.read_bytes()).hexdigest()
    lines = [
        "# Reproducibility Report — Full Coded Corpus v1","","## Build result","",
        f"- Primary verified rows: **{len(master)}**",
        f"- Unique item IDs: **{master['item_id'].nunique()}**",
        f"- Organizations: **{master['organization'].nunique()}**",
        f"- Study window: **{master['date'].min()} to {master['date'].max()}**",
        f"- Website items: **{int(platform_counts.get('website',0))}**",
        f"- LinkedIn items: **{int(platform_counts.get('LinkedIn',0))}**",
        f"- Rows flagged as recurring-series members: **{recurring}**",
        "- Candidate-tier records are excluded from the primary master and retained separately.",
        f"- SHA-256: `{sha256}`","","## Validation checks","",
        "- PASS: 337 rows","- PASS: 337 unique item IDs","- PASS: no duplicate item IDs",
        "- PASS: all dates within 2025-11-01 through 2026-03-31","- PASS: 44 organizations",
        "- PASS: 317 website + 20 LinkedIn items","","## Monthly coverage","","| Month | Items |","|---|---:|",
    ]
    lines += [f"| {m} | {int(n)} |" for m,n in month_counts.items()]
    lines += ["","## Organization coverage","","| Organization | Items |","|---|---:|"]
    lines += [f"| {org.replace('|','/')} | {int(n)} |" for org,n in org_counts.items()]
    lines += ["","## Missingness","","NA remains missing; it is never silently converted to zero.","","| Field | Missing rows |","|---|---:|"]
    lines += [f"| `{f}` | {int(n)} |" for f,n in missing.items()] if len(missing) else ["| None | 0 |"]
    lines += ["","## Rebuild","","```bash","python -m pip install pandas","python analysis/build_full_corpus_master_v2.py","```","","The four legacy pilot CSVs are preserved unchanged and aligned deterministically to their documented schema during the build. The 22 candidate-tier records are not included in the primary quantitative corpus."]
    REPORT.write_text("\n".join(lines)+"\n", encoding="utf-8")


def main():
    pilot = normalize_pilot()
    expanded = pd.concat([pd.read_csv(p) for p in EXPANDED_FILES], ignore_index=True)
    missing_cols = sorted(set(TARGET_COLUMNS) - set(expanded.columns))
    if missing_cols:
        raise ValueError(f"Expanded batches missing required columns: {missing_cols}")
    master = pd.concat([pilot, expanded[TARGET_COLUMNS]], ignore_index=True)
    master["date"] = pd.to_datetime(master["date"], errors="raise").dt.strftime("%Y-%m-%d")
    series = pd.read_csv(PROCESSED / "recurring_series_map_v1.csv").rename(columns={"analysis_note":"series_analysis_note"})
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
    print(master["platform"].value_counts().to_string())

if __name__ == "__main__":
    main()
