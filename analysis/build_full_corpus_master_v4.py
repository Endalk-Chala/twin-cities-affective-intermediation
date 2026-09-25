"""Validated corpus builder v4.

Extends v3 by reconciling duplicate item_ids before the recurring-series merge.
Source CSVs remain unchanged. When the same verified communication was coded in
more than one batch, the first canonical occurrence is retained and the duplicate
occurrence is reported in CI output. Final validation still requires exactly 337
unique primary items.
"""
import pandas as pd
from build_full_corpus_master_v3 import (
    normalize_pilot, read_aligned, EXPANDED_FILES, TARGET, P, OUT, validate, report
)


def main():
    pilot = normalize_pilot()
    expanded = pd.concat([read_aligned(p) for p in EXPANDED_FILES], ignore_index=True)
    missing = sorted(set(TARGET) - set(expanded.columns))
    if missing:
        raise ValueError(f"Expanded schema missing columns: {missing}")

    master = pd.concat([pilot, expanded[TARGET]], ignore_index=True)
    master["date"] = pd.to_datetime(master["date"], errors="raise").dt.strftime("%Y-%m-%d")

    dup_mask = master.duplicated("item_id", keep=False)
    if dup_mask.any():
        dup = master.loc[dup_mask, ["item_id", "organization", "date", "platform", "coder_id"]].sort_values("item_id")
        print("Duplicate coded occurrences detected before reconciliation:")
        print(dup.to_string(index=False))
        before = len(master)
        master = master.drop_duplicates("item_id", keep="first").copy()
        print(f"Reconciled duplicate occurrences: {before} -> {len(master)} rows")

    series = pd.read_csv(P / "recurring_series_map_v1.csv").rename(
        columns={"analysis_note": "series_analysis_note"}
    )[["item_id", "series_id", "series_label", "series_type", "series_analysis_note"]]
    if series["item_id"].duplicated().any():
        raise ValueError("recurring_series_map_v1.csv contains duplicate item_id values")

    master = master.merge(series, on="item_id", how="left", validate="one_to_one")
    master["is_recurring_series"] = master["series_id"].notna().astype(int)

    validate(master)
    master = master.sort_values(["date", "organization", "platform", "item_id"], kind="stable").reset_index(drop=True)
    master.to_csv(OUT, index=False)
    report(master)

    print(f"PASS rows={len(master)} unique_ids={master.item_id.nunique()} organizations={master.organization.nunique()}")
    print(master.platform.value_counts().to_string())


if __name__ == "__main__":
    main()
