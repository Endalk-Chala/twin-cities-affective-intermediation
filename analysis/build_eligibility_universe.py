from __future__ import annotations

import io
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sampling_frame" / "eligibility_universe_reconciliation_v2.csv"
SUMMARY = ROOT / "sampling_frame" / "eligibility_universe_reconciliation_v2.md"

BASE = "https://raw.githubusercontent.com/Endalk-Chala/mn-immigration-nonprofit-communication/main/research_workspace/01_sampling_frame/"
FILES = [
    "eligibility_screening_batch_01_TC001_TC010.csv",
    "eligibility_screening_batch_02_TC011_TC020.csv",
    "eligibility_screening_batch_03_TC021_TC030.csv",
    "eligibility_screening_batch_04_TC031_TC040.csv",
    "eligibility_screening_batch_05_TC041_TC050.csv",
    "eligibility_screening_batch_06_TC051_TC060.csv",
    "eligibility_screening_batch_07_TC061_TC070.csv",
    "eligibility_screening_batch_08_TC071_TC080.csv",
    "eligibility_screening_batch_09_TC081_TC084.csv",
    "eligibility_screening_batch_10_D1_state_resettlement_legal.csv",
    "eligibility_screening_batch_11_D2_advocacy_networks.csv",
    "eligibility_screening_batch_12_D3_faith_ethnocultural_part1.csv",
    "eligibility_screening_batch_13_D3_faith_ethnocultural_part2.csv",
    "eligibility_screening_batch_14_D4_mdh_community.csv",
]

PRIMARY_DECISIONS = {"eligible", "probably_eligible"}
NONUNIT_DECISIONS = {"duplicate_alias", "duplicate_program_candidate"}


def read_remote_csv(filename: str) -> pd.DataFrame:
    with urllib.request.urlopen(BASE + filename) as response:
        text = response.read().decode("utf-8")
    frame = pd.read_csv(io.StringIO(text), dtype=str).fillna("")
    if "record_id" in frame.columns and "org_id" not in frame.columns:
        frame = frame.rename(columns={"record_id": "org_id"})
    frame["source_screening_file"] = filename
    return frame


def main() -> None:
    frames = [read_remote_csv(f) for f in FILES]
    all_rows = pd.concat(frames, ignore_index=True, sort=False).fillna("")

    expected = {
        "eligible": 91,
        "probably_eligible": 23,
        "exclude": 22,
        "nonunit": 2,
        "raw_rows": 138,
        "primary_units": 114,
    }

    counts = all_rows["screening_decision"].value_counts().to_dict()
    nonunit = int(all_rows["screening_decision"].isin(NONUNIT_DECISIONS).sum())
    primary = int(all_rows["screening_decision"].isin(PRIMARY_DECISIONS).sum())

    observed = {
        "eligible": int(counts.get("eligible", 0)),
        "probably_eligible": int(counts.get("probably_eligible", 0)),
        "exclude": int(counts.get("exclude", 0)),
        "nonunit": nonunit,
        "raw_rows": len(all_rows),
        "primary_units": primary,
    }

    if observed != expected:
        raise RuntimeError(f"Eligibility reconciliation mismatch. Expected {expected}; observed {observed}")

    all_rows["analysis_universe_status"] = all_rows["screening_decision"].map(
        lambda x: "include_primary_universe" if x in PRIMARY_DECISIONS else (
            "exclude" if x == "exclude" else "merge_not_independent_unit"
        )
    )
    all_rows["primary_universe_flag"] = all_rows["screening_decision"].isin(PRIMARY_DECISIONS).astype(int)
    all_rows["evidence_certainty"] = all_rows["screening_decision"].map(
        {"eligible": "verified", "probably_eligible": "provisional", "exclude": "excluded", "duplicate_alias": "merged", "duplicate_program_candidate": "merged"}
    ).fillna("review")

    preferred = [
        "org_id", "organization_name", "screening_decision", "analysis_universe_status",
        "primary_universe_flag", "evidence_certainty", "twin_cities_presence",
        "immigrant_refugee_relevance", "civil_society_form", "study_period_existence",
        "unit_of_analysis_flag", "evidence_summary", "evidence_url_1", "evidence_url_2",
        "communication_audit_note", "screening_notes", "source_screening_file",
    ]
    cols = [c for c in preferred if c in all_rows.columns]
    extra = [c for c in all_rows.columns if c not in cols]
    out = all_rows[cols + extra].copy()
    out.to_csv(OUT, index=False)

    excluded = out.loc[out["screening_decision"].eq("exclude"), ["org_id", "organization_name"]]
    merged = out.loc[out["screening_decision"].isin(NONUNIT_DECISIONS), ["org_id", "organization_name", "screening_decision"]]

    lines = [
        "# Eligibility Universe Reconciliation v2",
        "",
        "Authoritative row-level reconstruction from the 14 eligibility-screening batches in the historical precursor repository.",
        "",
        "## Reconciled counts",
        "",
        f"- Raw screened records: **{observed['raw_rows']}**",
        f"- Eligible: **{observed['eligible']}**",
        f"- Probably eligible / verification needed: **{observed['probably_eligible']}**",
        f"- Excluded: **{observed['exclude']}**",
        f"- Duplicate/alias/program merges: **{observed['nonunit']}**",
        f"- Primary analytical universe (eligible + probably eligible): **{observed['primary_units']}**",
        "",
        "## Analytical rule",
        "",
        "`primary_universe_flag = 1` only for `eligible` and `probably_eligible`. Excluded and merged records remain in the reconciliation file for auditability but must not be treated as independent primary-universe organizations.",
        "",
        "## Excluded records",
        "",
    ]
    lines.extend([f"- `{r.org_id}` — {r.organization_name}" for r in excluded.itertuples(index=False)])
    lines.extend(["", "## Merged / non-independent records", ""])
    lines.extend([f"- `{r.org_id}` — {r.organization_name} (`{r.screening_decision}`)" for r in merged.itertuples(index=False)])
    lines.extend([
        "",
        "## Provenance",
        "",
        "Source: `Endalk-Chala/mn-immigration-nonprofit-communication`, `research_workspace/01_sampling_frame/eligibility_screening_batch_01...14`.",
        "",
        "This file closes a migration gap in the standalone repository: the earlier summary retained the aggregate 114-unit logic, but the row-level screening batches had not yet been migrated into one canonical reconciliation table.",
    ])
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(observed)


if __name__ == "__main__":
    main()
