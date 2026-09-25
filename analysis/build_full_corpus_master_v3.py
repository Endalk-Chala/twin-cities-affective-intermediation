"""Build and validate the primary coded master corpus (v3).

All coding CSVs are parsed with deterministic schema alignment. This preserves
source files unchanged while repairing only structural CSV drift (missing fields
or unquoted commas) according to documented field types and hard anchors.
"""
from pathlib import Path
from functools import lru_cache
import csv, hashlib, re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"
OUT = P / "full_corpus_coded_master_v1.csv"
REPORT = ROOT / "analysis" / "reproducibility_report_v1.md"

PILOT_FILES = [P/f"ai_coding_pilot_batch_0{i}_items_{1+(i-1)*10:02d}_{i*10:02d}.csv" for i in range(1,5)]
EXPANDED_FILES = [
P/"full_corpus_coding_batch_01_MMLA_CLUES_24items.csv",
P/"full_corpus_coding_batch_02_MMLA_CLUES_remaining_27items.csv",
P/"full_corpus_coding_batch_03_Advocates_OCM_IDN_19items.csv",
P/"full_corpus_coding_batch_04_ICOM_ISAIAH_CAPI_KOM_MCC_Arrive_23items.csv",
P/"full_corpus_coding_batch_05_remaining_staged_27items.csv",
P/"full_corpus_coding_batch_06_new_verified_social_6items.csv",
P/"full_corpus_coding_batch_07_Groundwork_JCA_24items.csv",
P/"full_corpus_coding_batch_08_CedarRiverside_PPL_24items.csv",
P/"full_corpus_coding_batch_09_PRISM_VOA_VLN_Habitat_AVIVO_Missions_37items.csv",
P/"full_corpus_coding_batch_10_ACER_ACLUMN_Isuroon_Alight_new_22items.csv",
P/"full_corpus_coding_batch_11_ILCM_CVT_IIMN_new_23items.csv",
P/"full_corpus_coding_batch_12_COPAL_Unidos_CVTadditional_31items.csv",
P/"full_corpus_coding_batch_13_early_batches_new_unique_10items.csv"]

TARGET = ["item_id","org_id","organization","date","platform","org_role_primary","org_role_secondary","role_hybrid_flag","threat_appraisal","harm_loss_appraisal","injustice_appraisal","uncertainty_appraisal","responsibility_blame_appraisal","intentionality_appraisal","norm_violation_appraisal","vulnerability_appraisal","controllability_appraisal","coping_efficacy_appraisal","collective_efficacy_appraisal","care_need_appraisal","opportunity_hope_appraisal","fear_intensity","anxiety_uncertainty_intensity","anger_intensity","moral_outrage_intensity","grief_sadness_intensity","solidarity_intensity","care_compassion_intensity","empathy_intensity","hope_intensity","gratitude_intensity","pride_intensity","reassurance_intensity","defiance_intensity","urgency_emotion_intensity","other_emotion_intensity","emotion_explicitness","emotion_source_org","emotion_source_affected_public","emotion_source_supporters_public","emotion_source_quoted_actor","function_inform","function_warn","function_reassure","function_regulate_fear","function_mobilize","function_advocate","function_provide_service","function_fundraise","function_build_solidarity","function_generate_empathy","function_moral_evaluation","function_increase_efficacy","function_mourn_commemorate","function_document_testify","function_celebrate","function_encourage_defiance","function_other","action_orientation_present","action_type","action_specificity","action_immediacy","audience_primary","direct_address","urgency_level","legal_information_present","service_information_present","resource_link_present","appraisal_notes","emotion_notes","coder_id","coding_date","coder_confidence"]

BINARY = {x for x in TARGET if x.endswith("_appraisal") or x.startswith("function_")} | {"role_hybrid_flag","emotion_source_org","emotion_source_affected_public","emotion_source_supporters_public","emotion_source_quoted_actor","action_orientation_present","direct_address","legal_information_present","service_information_present","resource_link_present","coding_abstain","ambiguity_flag"}
INTENSITY = {x for x in TARGET if x.endswith("_intensity")} | {"urgency_level"}

def score(name,v):
    v="" if v is None else str(v)
    if name=="pilot_order": return 20 if re.fullmatch(r"\d+",v) else -40
    if name=="date": return 20 if re.fullmatch(r"\d{4}-\d{2}-\d{2}",v) else -40
    if name=="platform": return 20 if v in {"website","LinkedIn"} else -40
    if name=="item_id": return 8 if v else -20
    if name=="org_id": return 6 if v else -15
    if name in BINARY: return 8 if v in {"0","1",""} else -15
    if name in INTENSITY: return 8 if v in {"0","1","2","3",""} else -15
    if name=="emotion_explicitness": return 8 if v in {"none","implicit","explicit","mixed",""} else -10
    if name=="action_specificity": return 8 if v in {"none","general","specific",""} else -10
    if name=="action_immediacy": return 8 if v in {"none","low","moderate","high",""} else -10
    if name in {"ai_coding_confidence","coder_confidence"}: return 8 if v in {"high","medium","low",""} else -10
    if name=="coding_source_quality": return 8 if v in {"summary_plus_title","full_text","title_only",""} else -10
    if name in {"ai_coder_id","coder_id"}: return 6 if (v.startswith("GPT-") or v=="") else -8
    return 1

def align(header,tokens,path,line):
    H,T=len(header),len(tokens)
    @lru_cache(None)
    def dp(i,j):
        if i==H and j==T: return (0,())
        if i==H: return None
        rh,rt=H-i,T-j
        if rt>rh+8 or rh>rt+8: return None
        c=[]
        if j<T:
            z=dp(i+1,j+1)
            if z: c.append((score(header[i],tokens[j])+z[0],(tokens[j],)+z[1]))
        z=dp(i+1,j)
        if z: c.append((score(header[i],"")-6+z[0],("",)+z[1]))
        if j+1<T:
            m=tokens[j]+","+tokens[j+1]; z=dp(i+1,j+2)
            if z: c.append((score(header[i],m)-3+z[0],(m,)+z[1]))
        if not c:return None
        c.sort(key=lambda q:q[0],reverse=True);return c[0]
    r=dp(0,0)
    if not r: raise ValueError(f"Cannot align {path}:{line}: {T} tokens/{H} fields")
    row=list(r[1]); d=dict(zip(header,row))
    if "date" in d and not re.fullmatch(r"\d{4}-\d{2}-\d{2}",d["date"]): raise ValueError(f"Bad date after alignment {path}:{line}: {d['date']}")
    if "platform" in d and d["platform"] not in {"website","LinkedIn"}: raise ValueError(f"Bad platform after alignment {path}:{line}: {d['platform']}")
    if "item_id" in d and not d["item_id"]: raise ValueError(f"Missing item_id {path}:{line}")
    if len(tokens)!=H: print(f"Schema repair {path}:{line}: tokens={T}, fields={H}, score={r[0]}")
    return row

def read_aligned(path):
    with path.open("r",encoding="utf-8",newline="") as f: rows=list(csv.reader(f))
    h=rows[0]; data=[align(h,r,path.name,n) for n,r in enumerate(rows[1:],2)]
    return pd.DataFrame(data,columns=h)

def normalize_pilot():
    x=pd.concat([read_aligned(p) for p in PILOT_FILES],ignore_index=True)
    s=pd.read_csv(P/"pilot_schema_supplement_v1.csv")
    x=x.merge(s,on="item_id",how="left",validate="one_to_one")
    if x["org_role_primary"].isna().any(): raise ValueError("Pilot schema supplement incomplete")
    x["appraisal_notes"]=x["appraisal_evidence_notes"]
    x["emotion_notes"]=x["emotion_evidence_notes"]
    x["coder_id"]="GPT-5.6-Sol_full_corpus_v1"; x["coding_date"]="2026-09-24"; x["coder_confidence"]=x["ai_coding_confidence"]
    for c in TARGET:
        if c not in x:x[c]=pd.NA
    return x[TARGET]

def validate(m):
    dates=pd.to_datetime(m.date,errors="raise")
    checks={"rows":len(m)==337,"unique_ids":m.item_id.nunique()==337,"no_duplicate_ids":not m.item_id.duplicated().any(),"dates_in_window":((dates>=pd.Timestamp("2025-11-01"))&(dates<=pd.Timestamp("2026-03-31"))).all(),"organizations":m.organization.nunique()==44,"platform_counts":m.platform.value_counts().to_dict()=={"website":317,"LinkedIn":20}}
    bad=[k for k,v in checks.items() if not v]
    if bad: raise ValueError(f"Validation failed {bad}; rows={len(m)}, ids={m.item_id.nunique()}, orgs={m.organization.nunique()}, platforms={m.platform.value_counts().to_dict()}")

def report(m):
    mon=m.assign(month=m.date.str[:7]).month.value_counts().sort_index(); org=m.groupby("organization").size().sort_values(ascending=False); miss=m.isna().sum(); miss=miss[miss>0].sort_values(ascending=False); sha=hashlib.sha256(OUT.read_bytes()).hexdigest()
    L=["# Reproducibility Report — Full Coded Corpus v1","","## Build result","",f"- Primary verified rows: **{len(m)}**",f"- Unique item IDs: **{m.item_id.nunique()}**",f"- Organizations: **{m.organization.nunique()}**",f"- Study window: **{m.date.min()} to {m.date.max()}**",f"- Website items: **{int((m.platform=='website').sum())}**",f"- LinkedIn items: **{int((m.platform=='LinkedIn').sum())}**",f"- Recurring-series rows: **{int(m.series_id.notna().sum())}**","- Candidate-tier records excluded and retained separately.",f"- SHA-256: `{sha}`","","## Validation checks","","- PASS: 337 rows","- PASS: 337 unique item IDs","- PASS: no duplicate item IDs","- PASS: all dates in study window","- PASS: 44 organizations","- PASS: 317 website + 20 LinkedIn","","## Monthly coverage","","| Month | Items |","|---|---:|"]
    L += [f"| {k} | {int(v)} |" for k,v in mon.items()]+["","## Organization coverage","","| Organization | Items |","|---|---:|"]+[f"| {k.replace('|','/')} | {int(v)} |" for k,v in org.items()]+["","## Missingness","","Missing values remain NA; they are not silently converted to zero.","","| Field | Missing rows |","|---|---:|"]+[f"| `{k}` | {int(v)} |" for k,v in miss.items()]+["","## Rebuild","","```bash","python -m pip install pandas","python analysis/build_full_corpus_master_v3.py","```","","All source coding CSVs are preserved unchanged. Structural CSV drift is repaired deterministically at build time using schema constraints and hard anchors. Candidate-tier records remain outside the primary quantitative corpus."]
    REPORT.write_text("\n".join(L)+"\n",encoding="utf-8")

def main():
    pilot=normalize_pilot()
    expanded=pd.concat([read_aligned(p) for p in EXPANDED_FILES],ignore_index=True)
    missing=sorted(set(TARGET)-set(expanded.columns))
    if missing: raise ValueError(f"Expanded schema missing columns: {missing}")
    m=pd.concat([pilot,expanded[TARGET]],ignore_index=True)
    m.date=pd.to_datetime(m.date,errors="raise").dt.strftime("%Y-%m-%d")
    s=pd.read_csv(P/"recurring_series_map_v1.csv").rename(columns={"analysis_note":"series_analysis_note"})[["item_id","series_id","series_label","series_type","series_analysis_note"]]
    m=m.merge(s,on="item_id",how="left",validate="one_to_one"); m["is_recurring_series"]=m.series_id.notna().astype(int)
    validate(m); m=m.sort_values(["date","organization","platform","item_id"],kind="stable").reset_index(drop=True); m.to_csv(OUT,index=False); report(m)
    print(f"PASS rows={len(m)} unique_ids={m.item_id.nunique()} organizations={m.organization.nunique()}"); print(m.platform.value_counts().to_string())
if __name__=="__main__": main()
