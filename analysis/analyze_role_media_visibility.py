from __future__ import annotations

from itertools import combinations
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
ANALYSIS = ROOT / "analysis"

INPUT = PROCESSED / "organization_role_media_visibility_v1.csv"
ROLE_OUT = ANALYSIS / "role_visibility_summary_v1.csv"
PAIR_OUT = ANALYSIS / "role_pair_visibility_summary_v1.csv"
STATUS_OUT = ANALYSIS / "screening_status_visibility_summary_v1.csv"
REPORT_OUT = ANALYSIS / "role_media_descriptive_findings_v1.md"


def as_num(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce").fillna(0)


def pct(num: int | float, den: int | float) -> float:
    return round((num / den * 100.0), 1) if den else 0.0


def main() -> None:
    df = pd.read_csv(INPUT, dtype=str).fillna("")
    if len(df) != 114:
        raise RuntimeError(f"Expected 114 organizations, found {len(df)}")

    numeric_cols = [
        "typology_label_count", "verified_news_edge_count", "unique_news_story_count",
        "unique_outlet_count", "media_layer_count", "community_ethnic_edge_count",
        "local_regional_edge_count", "national_amplification_edge_count",
        "national_amplification_observed", "cross_layer_observed", "three_layer_observed",
        "direct_quote_edge_count", "substantive_interpretation_edge_count",
        "resource_routing_edge_count", "mobilization_uptake_edge_count",
        "legal_information_uptake_edge_count", "service_uptake_edge_count",
    ]
    for col in numeric_cols:
        df[col] = as_num(df, col)

    df["observed_media"] = (df["verified_news_edge_count"] > 0).astype(int)
    df["direct_quote_observed"] = (df["direct_quote_edge_count"] > 0).astype(int)
    df["substantive_interpretation_observed"] = (df["substantive_interpretation_edge_count"] > 0).astype(int)
    df["resource_routing_observed"] = (df["resource_routing_edge_count"] > 0).astype(int)
    df["mobilization_uptake_observed"] = (df["mobilization_uptake_edge_count"] > 0).astype(int)

    # Long organization-role membership table. Each verified role is equal-weight.
    role_rows: list[dict[str, object]] = []
    org_roles: dict[str, list[str]] = {}
    for r in df.itertuples(index=False):
        roles = sorted({x.strip() for x in str(r.verified_typology_labels).split(";") if x.strip()})
        org_roles[r.org_id] = roles
        for role in roles:
            role_rows.append({"org_id": r.org_id, "role_label": role})
    long = pd.DataFrame(role_rows)

    role_summary: list[dict[str, object]] = []
    for role, members in long.groupby("role_label"):
        ids = set(members["org_id"])
        g = df[df["org_id"].isin(ids)].copy()
        n = len(g)
        obs = int(g["observed_media"].sum())
        cross = int(g["cross_layer_observed"].sum())
        national = int(g["national_amplification_observed"].sum())
        quote = int(g["direct_quote_observed"].sum())
        substantive = int(g["substantive_interpretation_observed"].sum())
        resource = int(g["resource_routing_observed"].sum())
        mobilization = int(g["mobilization_uptake_observed"].sum())
        role_summary.append({
            "role_label": role,
            "organization_count": n,
            "organizations_with_verified_media_edge": obs,
            "observed_media_share_pct": pct(obs, n),
            "organizations_with_cross_layer_visibility": cross,
            "cross_layer_share_pct": pct(cross, n),
            "organizations_with_national_amplification": national,
            "national_amplification_share_pct": pct(national, n),
            "organizations_with_direct_quote": quote,
            "direct_quote_share_pct": pct(quote, n),
            "organizations_with_substantive_interpretation": substantive,
            "substantive_interpretation_share_pct": pct(substantive, n),
            "organizations_with_resource_routing": resource,
            "resource_routing_share_pct": pct(resource, n),
            "organizations_with_mobilization_uptake": mobilization,
            "mobilization_uptake_share_pct": pct(mobilization, n),
            "verified_news_edges_total_for_role_members": int(g["verified_news_edge_count"].sum()),
            "median_verified_edges_all_role_members": round(float(g["verified_news_edge_count"].median()), 2),
            "median_verified_edges_observed_members": round(float(g.loc[g["observed_media"].eq(1), "verified_news_edge_count"].median()), 2) if obs else 0.0,
        })

    role_df = pd.DataFrame(role_summary).sort_values(
        ["observed_media_share_pct", "organization_count", "role_label"],
        ascending=[False, False, True],
    )
    role_df.to_csv(ROLE_OUT, index=False)

    # Pair-level co-membership summary. Preserve all pairs; include a small-n flag rather
    # than silently dropping sparse combinations.
    pair_members: dict[tuple[str, str], set[str]] = {}
    for org_id, roles in org_roles.items():
        for a, b in combinations(roles, 2):
            pair_members.setdefault((a, b), set()).add(org_id)

    pair_rows: list[dict[str, object]] = []
    for (a, b), ids in pair_members.items():
        g = df[df["org_id"].isin(ids)].copy()
        n = len(g)
        obs = int(g["observed_media"].sum())
        cross = int(g["cross_layer_observed"].sum())
        national = int(g["national_amplification_observed"].sum())
        pair_rows.append({
            "role_a": a,
            "role_b": b,
            "organization_count": n,
            "organizations_with_verified_media_edge": obs,
            "observed_media_share_pct": pct(obs, n),
            "organizations_with_cross_layer_visibility": cross,
            "cross_layer_share_pct": pct(cross, n),
            "organizations_with_national_amplification": national,
            "national_amplification_share_pct": pct(national, n),
            "verified_news_edges_total_for_pair_members": int(g["verified_news_edge_count"].sum()),
            "small_n_flag": 1 if n < 5 else 0,
        })
    pair_df = pd.DataFrame(pair_rows).sort_values(
        ["small_n_flag", "observed_media_share_pct", "organization_count", "role_a", "role_b"],
        ascending=[True, False, False, True, True],
    )
    pair_df.to_csv(PAIR_OUT, index=False)

    status_rows = []
    for status, g in df.groupby("screening_decision"):
        n = len(g)
        obs = int(g["observed_media"].sum())
        status_rows.append({
            "screening_decision": status,
            "organization_count": n,
            "organizations_with_verified_media_edge": obs,
            "observed_media_share_pct": pct(obs, n),
            "verified_news_edges_total": int(g["verified_news_edge_count"].sum()),
            "organizations_with_cross_layer_visibility": int(g["cross_layer_observed"].sum()),
            "organizations_with_national_amplification": int(g["national_amplification_observed"].sum()),
        })
    pd.DataFrame(status_rows).sort_values("screening_decision").to_csv(STATUS_OUT, index=False)

    total_observed = int(df["observed_media"].sum())
    no_edge = len(df) - total_observed
    cross_total = int(df["cross_layer_observed"].sum())
    national_total = int(df["national_amplification_observed"].sum())

    # Report robust descriptive patterns only. Require at least five organizations for
    # automated role/pair callouts to avoid highlighting tiny cells as substantive.
    robust_roles = role_df[role_df["organization_count"].ge(5)].copy()
    robust_pairs = pair_df[(pair_df["organization_count"].ge(5))].copy()

    top_role_lines = []
    for r in robust_roles.head(8).itertuples(index=False):
        top_role_lines.append(
            f"- `{r.role_label}`: {r.organizations_with_verified_media_edge}/{r.organization_count} organizations "
            f"({r.observed_media_share_pct:.1f}%) have at least one verified media edge; "
            f"{r.organizations_with_cross_layer_visibility} cross media layers; "
            f"{r.organizations_with_national_amplification} reach the national-amplification layer."
        )

    top_pair_lines = []
    for r in robust_pairs.head(8).itertuples(index=False):
        top_pair_lines.append(
            f"- `{r.role_a}` + `{r.role_b}`: {r.organizations_with_verified_media_edge}/{r.organization_count} organizations "
            f"({r.observed_media_share_pct:.1f}%) have a verified media edge; "
            f"{r.organizations_with_cross_layer_visibility} are cross-layer and "
            f"{r.organizations_with_national_amplification} reach national amplification."
        )

    report = [
        "# Role–Media Visibility Descriptive Analysis v1",
        "",
        "**Unit:** organization in the 114-unit primary analytical universe  ",
        "**Media outcome:** at least one verified organization–news relation in the currently collected corpus  ",
        "**Important:** absence of a verified edge is an observability result, not proof that an organization received no media coverage.",
        "",
        "## Universe-level descriptive picture",
        "",
        f"- Primary analytical organizations: **{len(df)}**",
        f"- Organizations with at least one verified media edge: **{total_observed}** ({pct(total_observed, len(df)):.1f}%)",
        f"- Organizations with no verified edge in the current corpus: **{no_edge}** ({pct(no_edge, len(df)):.1f}%)",
        f"- Organizations observed across more than one media layer: **{cross_total}**",
        f"- Organizations observed in the national-amplification layer: **{national_total}**",
        "",
        "## Role-level patterns",
        "",
        "The following rows are descriptive and restricted to role categories represented by at least five organizations. They should not be read as causal effects or as rankings of organizational effectiveness.",
        "",
        *top_role_lines,
        "",
        "## Role-pair patterns",
        "",
        "Role combinations are multi-label co-memberships. The automated callout below requires at least five organizations in the pair; the CSV retains smaller pairs with `small_n_flag = 1` for audit rather than interpretation.",
        "",
        *top_pair_lines,
        "",
        "## Interpretation guardrails",
        "",
        "1. A verified media edge measures observed visibility in the collected corpus, not the full universe of actual coverage.",
        "2. Search misses, inaccessible archives, and uneven historical platform observability can suppress observed visibility.",
        "3. Multi-label roles are equal-weight memberships. An organization contributes to every verified role it carries, so role-level edge totals are intentionally non-additive.",
        "4. National amplification signals broader circulation, not greater organizational quality, legitimacy, influence, or effectiveness.",
        "5. These tables are descriptive infrastructure. Statistical modeling should wait until outlet/organization audit completeness is coded sufficiently to distinguish an audited zero from an unaudited absence.",
        "",
        "## Generated files",
        "",
        "- `analysis/role_visibility_summary_v1.csv`",
        "- `analysis/role_pair_visibility_summary_v1.csv`",
        "- `analysis/screening_status_visibility_summary_v1.csv`",
        "- `data/processed/organization_role_media_visibility_v1.csv`",
    ]
    REPORT_OUT.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Organizations with verified media edge: {total_observed}/{len(df)}")
    print(f"Role categories analyzed: {len(role_df)}")
    print(f"Role pairs analyzed: {len(pair_df)}")


if __name__ == "__main__":
    main()
