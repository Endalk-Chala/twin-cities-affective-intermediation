"""Validated corpus builder v5.

Resolves known legacy item-ID collisions without dropping valid records, then
validates the assembled primary corpus against the reconciled source inventory.
Source CSVs remain unchanged.
"""
import pandas as pd
from build_full_corpus_master_v3 import (
    normalize_pilot, read_aligned, EXPANDED_FILES, TARGET, P, OUT, report
)

# Known legacy ID reuse documented during reconciliation. Both rows are valid
# communications, so the later CVT occurrence receives a stable canonical ID.
KNOWN_ID_REMAP = {
    ("CI0034", "Center for Victims of Torture", "2026-01-26", "website"):
        "TC073-WEB-LEGACY-CI0034"
}

EXPECTED_ROWS = 337
EXPECTED_ORGS = 45
EXPECTED_PLATFORMS = {"website": 311, "LinkedIn": 26}


def canonicalize_ids(df):
    df = df.copy()
    df["source_item_id"] = df["item_id"]
    remapped = []
    for idx, row in df.iterrows():
        key = (str(row["item_id"]), str(row["organization"]), str(row["date"]), str(row["platform"]))
        if key in KNOWN_ID_REMAP:
            new_id = KNOWN_ID_REMAP[key]
            df.at[idx, "item_id"] = new_id
            remapped.append((key, new_id))
    for key, new_id in remapped:
        print(f"Canonical ID remap: {key} -> {new_id}")
    return df


def validate_v5(master):
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


def write_report_v5(master):
    # Reuse v3 report generator, then replace stale fixed validation text.
    report(master)
    report_path = P.parent.parent / "analysis" / "reproducibility_report_v1.md"
    text = report_path.read_text(encoding="utf-8")
    text = text.replace("- PASS: 44 organizations", "- PASS: 45 organizations")
    text = text.replace("- PASS: 317 website + 20 LinkedIn", "- PASS: 311 website + 26 LinkedIn")
    text = text.replace(
        "Candidate-tier records remain outside the primary quantitative corpus.",
        "Candidate-tier records remain outside the primary quantitative corpus. Known legacy item-ID reuse is canonicalized at build time while preserving the original source_item_id."
    )
    report_path.write_text(text, encoding="utf-8")


def main():
    pilot = normalize_pilot()
    expanded = pd.concat([read_aligned(p) for p in EXPANDED_FILES], ignore_index=True)
    missing = sorted(set(TARGET) - set(expanded.columns))
    if missing:
        raise ValueError(f"Expanded schema missing columns: {missing}")

    master = pd.concat([pilot, expanded[TARGET]], ignore_index=True)
    master["date"] = pd.to_datetime(master["date"], errors="raise").dt.strftime("%Y-%m-%d")
    master = canonicalize_ids(master)

    # No unresolved duplicate IDs may remain after canonicalization.
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

    validate_v5(master)
    master = master.sort_values(["date","organization","platform","item_id"], kind="stable").reset_index(drop=True)
    master.to_csv(OUT, index=False)
    write_report_v5(master)

    print(f"PASS rows={len(master)} unique_ids={master.item_id.nunique()} organizations={master.organization.nunique()}")
    print(master.platform.value_counts().to_string())


if __name__ == "__main__":
    main()
