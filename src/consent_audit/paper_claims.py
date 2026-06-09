"""Generate an evidence-aware SSRP paper claim register."""

from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def export_ssrp_claim_register(
    *,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    cmp_confirmation_csv: Path,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    figure_plan_md: Path,
    writing_pack_md: Path,
    cycle_report_md: Path,
    out_md: Path,
    title: str,
    week_label: str,
) -> str:
    """Write a Markdown register of supported, provisional, and blocked claims."""

    targets = _read_rows(targets_csv)
    reports = _latest_by_url(_read_rows(audit_summary_csv), date_key="captured_at")
    summaries = _latest_by_url(_read_rows(longitudinal_summary_csv), date_key="week_of")
    confirmation_counts = _count_values(
        _read_rows(cmp_confirmation_csv),
        "confirmation_status",
        default="pending",
    )
    cycle_status = _extract_capture_status(cycle_report_md)
    text = _render_claim_register(
        title=title,
        week_label=week_label,
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        figure_plan_md=figure_plan_md,
        writing_pack_md=writing_pack_md,
        cycle_report_md=cycle_report_md,
        targets=targets,
        reports=reports,
        summaries=summaries,
        confirmation_counts=confirmation_counts,
        cycle_status=cycle_status,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _render_claim_register(
    *,
    title: str,
    week_label: str,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    cmp_confirmation_csv: Path,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    figure_plan_md: Path,
    writing_pack_md: Path,
    cycle_report_md: Path,
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
    summaries: dict[str, dict[str, str]],
    confirmation_counts: dict[str, int],
    cycle_status: str,
) -> str:
    target_count = len(targets)
    report_count = sum(1 for target in targets if _row_for(target, reports))
    summary_count = sum(1 for target in targets if _row_for(target, summaries))
    tier_counts = _count_target_values(targets, reports, "tier", default="missing")
    banner_counts = _count_banner_classes(targets, reports)
    banner_tier_counts = _count_banner_present_values(targets, reports, "tier")
    severity_counts = _count_target_values(targets, summaries, "severity", default="missing")
    cmp_status = _format_counts(confirmation_counts) or "none"
    claim_mode = _claim_mode(cycle_status)
    claims = _claims(
        target_count=target_count,
        report_count=report_count,
        summary_count=summary_count,
        tier_counts=tier_counts,
        banner_counts=banner_counts,
        banner_tier_counts=banner_tier_counts,
        severity_counts=severity_counts,
        cmp_status=cmp_status,
        claim_mode=claim_mode,
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        figure_plan_md=figure_plan_md,
        writing_pack_md=writing_pack_md,
    )

    return (
        f"# {title}\n\n"
        "## Evidence Snapshot\n\n"
        f"- Evidence window: {week_label}\n"
        f"- Target sites: {target_count}\n"
        f"- RQ1 reports available for targets: {report_count}/{target_count}\n"
        f"- RQ2 summaries available for targets: {summary_count}/{target_count}\n"
        f"- Banner evidence classes: {_format_counts(banner_counts) or 'none'}\n"
        f"- Banner-present automated tiers: {_format_counts(banner_tier_counts) or 'none'}\n"
        f"- Raw automated target tiers: {_format_counts(tier_counts) or 'none'}\n"
        f"- Latest longitudinal severity: {_format_counts(severity_counts) or 'none'}\n"
        f"- CMP confirmations: {cmp_status}\n"
        f"- Cycle capture status: `{cycle_status}`\n"
        f"- Claim mode: {claim_mode}\n\n"
        "## Claim Register\n\n"
        "| ID | Section | Claim | Status | Evidence | Next action |\n"
        "|---|---|---|---|---|---|\n"
        f"{_render_claim_rows(claims)}\n\n"
        "## Blocked Claims\n\n"
        f"{_render_blocked_claims(claims)}\n\n"
        "## Source Artifacts\n\n"
        f"- Targets: `{targets_csv}`\n"
        f"- RQ1 audit reports: `{audit_summary_csv}`\n"
        f"- RQ2 longitudinal summaries: `{longitudinal_summary_csv}`\n"
        f"- CMP confirmation sheet: `{cmp_confirmation_csv}`\n"
        f"- Results tables: `{results_tables_md}`\n"
        f"- Paper skeleton: `{paper_skeleton_md}`\n"
        f"- Figure plan: `{figure_plan_md}`\n"
        f"- Writing pack: `{writing_pack_md}`\n"
        f"- Cycle report: `{cycle_report_md}`\n"
    )


def _claims(
    *,
    target_count: int,
    report_count: int,
    summary_count: int,
    tier_counts: dict[str, int],
    banner_counts: dict[str, int],
    banner_tier_counts: dict[str, int],
    severity_counts: dict[str, int],
    cmp_status: str,
    claim_mode: str,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    figure_plan_md: Path,
    writing_pack_md: Path,
) -> list[dict[str, str]]:
    result_status = "Ready" if claim_mode == "ready" else "Provisional"
    result_next = (
        "Use with the current sanity check; refresh again after any new capture."
        if claim_mode == "ready"
        else "Refresh after live capture before finalizing counts."
    )
    c8_claim = (
        "Week 2 live capture and sanity confirmation are complete for the "
        "current evidence gate."
        if claim_mode == "ready"
        else (
            "Final Week 2 result claims are not available until live capture "
            "and sanity confirmation."
        )
    )
    c8_next = (
        "Use with sanity-check and source-evidence references; update after future captures."
        if claim_mode == "ready"
        else "Run scheduled `week2-cycle`, then refresh outputs."
    )
    return [
        {
            "id": "C1",
            "section": "Methods",
            "claim": "The project implements a traceable three-layer consent-interface audit workflow.",
            "status": "Supported",
            "evidence": f"{paper_skeleton_md}; {writing_pack_md}",
            "next": "Use in Methods with the architecture figure.",
        },
        {
            "id": "C2",
            "section": "RQ1",
            "claim": f"Current RQ1 evidence covers {report_count}/{target_count} Week 2 targets.",
            "status": result_status,
            "evidence": str(results_tables_md),
            "next": result_next,
        },
        {
            "id": "C3",
            "section": "RQ2",
            "claim": f"Current RQ2 evidence covers {summary_count}/{target_count} Week 2 targets.",
            "status": result_status,
            "evidence": str(results_tables_md),
            "next": result_next,
        },
        {
            "id": "C4",
            "section": "RQ1",
            "claim": (
                "Banner-present automated tiers are "
                f"{_format_counts(banner_tier_counts) or 'none'}; "
                "no-visible-banner contrast candidates="
                f"{banner_counts.get('no_visible_banner', 0)}; "
                f"raw automated tiers are {_format_counts(tier_counts) or 'none'}."
            ),
            "status": result_status,
            "evidence": str(results_tables_md),
            "next": result_next,
        },
        {
            "id": "C5",
            "section": "RQ2",
            "claim": f"Latest longitudinal severity levels are {_format_counts(severity_counts) or 'none'}.",
            "status": result_status,
            "evidence": f"{results_tables_md}; {figure_plan_md}",
            "next": "Use only after selecting timeline examples.",
        },
        {
            "id": "C6",
            "section": "Discussion",
            "claim": "Consent-interface evidence may inform privacy/GRC readiness, but this is not a SOC 2 audit.",
            "status": "Supported",
            "evidence": str(writing_pack_md),
            "next": "Keep as a short implication, not a main result.",
        },
        {
            "id": "C7",
            "section": "Limitations",
            "claim": f"pending CMP/manual-review confirmations remain unresolved: {cmp_status}.",
            "status": "Open limitation",
            "evidence": str(writing_pack_md),
            "next": "Update after advisor/human confirmation.",
        },
        {
            "id": "C8",
            "section": "Final results",
            "claim": c8_claim,
            "status": "Blocked" if claim_mode == "provisional" else "Ready",
            "evidence": str(writing_pack_md),
            "next": c8_next,
        },
    ]


def _render_claim_rows(claims: list[dict[str, str]]) -> str:
    return "\n".join(
        "| "
        f"{_cell(claim['id'])} | "
        f"{_cell(claim['section'])} | "
        f"{_cell(claim['claim'])} | "
        f"{_cell(claim['status'])} | "
        f"{_cell(claim['evidence'])} | "
        f"{_cell(claim['next'])} |"
        for claim in claims
    )


def _render_blocked_claims(claims: list[dict[str, str]]) -> str:
    blocked = [claim for claim in claims if claim["status"] == "Blocked"]
    if not blocked:
        return "- None."
    return "\n".join(f"- {claim['id']}: {claim['claim']}" for claim in blocked)


def _claim_mode(cycle_status: str) -> str:
    if cycle_status in {"complete", "capture_complete", "completed", "ready", "refreshed"}:
        return "ready"
    return "provisional"


def _row_for(
    target: dict[str, str],
    rows_by_url: dict[str, dict[str, str]],
) -> dict[str, str]:
    return rows_by_url.get(_canonicalize_url(target.get("url", "")), {})


def _latest_by_url(
    rows: list[dict[str, str]],
    *,
    date_key: str,
) -> dict[str, dict[str, str]]:
    latest: dict[str, dict[str, str]] = {}
    for row in rows:
        canonical_url = _canonicalize_url(row.get("url", ""))
        if not canonical_url:
            continue
        current = latest.get(canonical_url)
        if current is None or row.get(date_key, "") >= current.get(date_key, ""):
            latest[canonical_url] = row
    return latest


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]


def _count_target_values(
    targets: list[dict[str, str]],
    rows_by_url: dict[str, dict[str, str]],
    key: str,
    *,
    default: str,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for target in targets:
        row = rows_by_url.get(_canonicalize_url(target.get("url", "")), {})
        value = (row.get(key) or default).strip() or default
        counts[value] = counts.get(value, 0) + 1
    return counts


def _banner_evidence_class(report: dict[str, str]) -> str:
    if not report:
        return "missing"
    if _parse_bool(report.get("banner_detected", "")):
        return "banner_present"
    return "no_visible_banner"


def _count_banner_classes(
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for target in targets:
        report = reports.get(_canonicalize_url(target.get("url", "")), {})
        value = _banner_evidence_class(report)
        counts[value] = counts.get(value, 0) + 1
    return counts


def _count_banner_present_values(
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
    key: str,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for target in targets:
        report = reports.get(_canonicalize_url(target.get("url", "")), {})
        if _banner_evidence_class(report) != "banner_present":
            continue
        value = (report.get(key) or "missing").strip() or "missing"
        counts[value] = counts.get(value, 0) + 1
    return counts


def _count_values(
    rows: list[dict[str, str]],
    key: str,
    *,
    default: str,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = (row.get(key) or default).strip() or default
        counts[value] = counts.get(value, 0) + 1
    return counts


def _extract_capture_status(path: Path) -> str:
    if not path.exists():
        return "missing_cycle_report"
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- Capture status:"):
            return stripped.split(":", 1)[1].strip().strip("`") or "unknown"
    return "unknown"


def _format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}={count}" for key, count in sorted(counts.items()))


def _cell(value: str) -> str:
    return value.replace("|", "\\|")


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))
