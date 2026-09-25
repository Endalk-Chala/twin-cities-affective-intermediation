"""Validated corpus builder v6.

Adds organization-name normalization to the collision-aware v5 build so the
master uses one canonical organization label per entity. Source files remain
unchanged; canonicalization occurs only in the generated master.
"""
from pathlib import Path
import pandas as pd
from build_full_corpus_master_v5 import (
    normalize_pilot, read_aligned, EXPANDED_FILES, TARGET, P, OUT,
    canonicalize_ids, KNOWN_ID_REMAP
)

REPORT = Path(__file__).resolve().parent / "reproducibility_report_v1.md"

ORG_NAME_MAP = {
    "CLUES": "Comunidades Latinas Unidas En Servicio (CLUES)",
}

EXPECTED_ROWS = 337
EXPECTED_ORGS = 44
EXPECTED_PLATFORMS = {"website": 311, "LinkedIn": 26}


def normalize_org_names(df):
    df = df.copy()
    df["source_organization"] = df["organization"]
    df["organization"] = df["organization"].replace(ORG_NAME_MAP)
    return df


def validate(master):
    dates = pd.to_datetime(master["date"], errors="raise")
    platform_counts = master["platform"].value_counts().to_dict()
    checks = {
        "rows": len(master) == EXPECTED_ROWS,
        "unique_ids": master["item_id"].nunique() == EXPECTED_ROWS,
        "no_duplicate_ids": not master["item_id"].duplicated().any(),
        "dates_in_window": ((dates >= pd.Timestamp("2025-11-01")) & (dates <= pd.Timestamp("2026-03-31"))).all(),
        "organizations": master["organization"].nunique() == EXPECTED_ORGS,
        "platform_counts": platform_counts == EXPECTED_PLATFORMS,
    }
    bad = [k for k, v in checks.items() if not v]
    if bad:
        raise ValueError(
            f"Validation failed {bad}; rows={len(master)}, ids={master.item_id.nunique()}, "
            f"orgs={master.organization.nunique()}, platforms={platform_counts}"
        )


def write_report(master):
    month_counts = master.assign(month=master["date"].str[:7])["month"].value_counts().sort_index()
    org_counts = master.groupby("organization").size().sort_values(ascending=False)
    missing = master.isna().sum().sort_values(ascending=False)
    missing = missing[missing > 0]
    import hashlib
    sha256 = hashlib.sha256(OUT.read_bytes()).hexdigest()

    lines = [
        "# Reproducibility Report — Full Coded Corpus v1", "",
        "## Build result", "",
        f"- Primary verified rows: **{len(master)}**",
        f"- Unique item IDs: **{master['item_id'].nunique()}**",
        f"- Organizations: **{master['organization'].nunique()}**",
        f"- Study window: **{master['date'].min()} to {master['date'].max()}**",
        f"- Website items: **{int((master['platform']=='website').sum())}**",
        f"- LinkedIn items: **{int((master['platform']=='LinkedIn').sum())}**",
        f"- Recurring-series rows: **{int(master['series_id'].notna().sum())}**",
        "- Candidate-tier records excluded and retained separately.",
        f"- SHA-256: `{sha256}`", "",
        "## Validation checks", "",
        "- PASS: 337 rows",
        "- PASS: 337 unique item IDs",
        "- PASS: no duplicate item IDs",
        "- PASS: all dates in study window",
        "- PASS: 44 canonical organizations",
        "- PASS: 311 website + 26 LinkedIn items",
        "- PASS: organization labels normalized (including CLUES)", "",
        "## Monthly coverage", "",
        "| Month | Items |", "|---|---:|",
    ]
    lines += [f"| {m} | {int(n)} |" for m, n in month_counts.items()]
    lines += ["", "## Organization coverage", "", "| Organization | Items |", "|---|---:|"]
    lines += [f"| {org.replace('|','/')} | {int(n)} |" for org, n in org_counts.items()]
    lines += ["", "## Missingness", "", "Missing values remain NA; they are not silently converted to zero.", "", "| Field | Missing rows |", "|---|---:|"]
    lines += [f"| `{field}` | {int(n)} |" for field, n in missing.items()] if len(missing) else ["| None | 0 |"]
    lines += [
        "", "## Rebuild", "",
        "```bash",
        "python -m pip install pandas",
        "python analysis/build_full_corpus_master_v6.py",
        "```", "",
        "All source coding CSVs are preserved unchanged. Structural CSV drift is repaired deterministically at build time using schema constraints and hard anchors. Known legacy item-ID reuse is canonicalized while preserving `source_item_id`. Organization labels are canonicalized while preserving `source_organization`. Candidate-tier records remain outside the primary quantitative corpus."
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    pilot = normalize_pilot()
    expanded = pd.concat([read_aligned(p) for p in EXPANDED_FILES], ignore_index=True)
    missing = sorted(set(TARGET) - set(expanded.columns))
    if missing:
        raise ValueError(f"Expanded schema missing columns: {missing}")

    master = pd.concat([pilot, expanded[TARGET]], ignore_index=True)
    master["date"] = pd.to_datetime(master["date"], errors="raise").dt.strftime("%Y-%m-%d")
    master = canonicalize_ids(master)
    master = normalize_org_names(master)

    if master["item_id"].duplicated().any():
        dup = master.loc[master["item_id"].duplicated(keep=False), ["item_id","organization","date","platform"]]
        raise ValueError("Unresolved item_id collisions remain:\n" + dup.to_string(index=False))

    series = pd.read_csv(P / "recurring_series_map_v1.csv").rename(
        columns={"analysis_note": "series_analysis_note"}
    )[["item_id", "series_id", "series_label", "series_type", "series_analysis_note"]]
    if series["item_id"].duplicated().any():
        raise ValueError("recurring_series_map_v1.csv contains duplicate item_id values")

    master = master.merge(series, on="item_id", how="left", validate="one_to_one")
    master["is_recurring_series"] = master["series_id"].notna().astype(int)

    validate(master)
    master = master.sort_values(["date","organization","platform","item_id"], kind="stable").reset_index(drop=True)
    master.to_csv(OUT, index=False)
    write_report(master)

    print(f"PASS rows={len(master)} unique_ids={master.item_id.nunique()} organizations={master.organization.nunique()}")
    print(master.platform.value_counts().to_string())


if __name__ == "__main__":
    main()
