"""Generate paper-facing SSRP results tables from current research CSVs."""

from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def export_ssrp_results_tables(
    *,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    out_md: Path,
    title: str,
    week_label: str,
) -> str:
    """Write Markdown RQ1/RQ2 tables grounded in current research exports."""

    targets = _read_rows(targets_csv)
    reports = _latest_by_url(_read_rows(audit_summary_csv), date_key="captured_at")
    summaries = _latest_by_url(_read_rows(longitudinal_summary_csv), date_key="week_of")
    text = _render_tables(
        title=title,
        week_label=week_label,
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        targets=targets,
        reports=reports,
        summaries=summaries,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _render_tables(
    *,
    title: str,
    week_label: str,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
    summaries: dict[str, dict[str, str]],
) -> str:
    target_count = len(targets)
    report_count = sum(1 for target in targets if _report_for(target, reports))
    summary_count = sum(1 for target in targets if _summary_for(target, summaries))
    return (
        f"# {title}\n\n"
        "## Evidence Snapshot\n\n"
        f"- Evidence window: {week_label}\n"
        f"- Target sites: {target_count}\n"
        f"- RQ1 reports available for targets: {report_count}/{target_count}\n"
        f"- RQ2 summaries available for targets: {summary_count}/{target_count}\n"
        f"- Banner evidence classes: {_format_counts(_count_banner_classes(targets, reports)) or 'none'}\n"
        f"- Banner-present automated tiers: {_format_counts(_count_banner_present_values(targets, reports, 'tier')) or 'none'}\n"
        f"- Raw automated target tiers: {_format_counts(_count_target_values(targets, reports, 'tier', default='missing')) or 'none'}\n"
        f"- Latest longitudinal severity: {_format_counts(_count_target_values(targets, summaries, 'severity', default='missing')) or 'none'}\n"
        "- Evidence refs may include generated DOM paths from CSV/report exports; verify raw HTML file availability separately before claiming synced DOM snapshots.\n\n"
        "## Table 1. RQ1 Consent-Interface Scoring Summary\n\n"
        "| Site | Category | Banner evidence | RQ1 coding | Automated tier | L1 gate | Available paths | Missing paths | L2 effort | Transparency | Unbiased | Evidence refs |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        f"{_render_rq1_rows(targets, reports)}\n\n"
        "## Table 2. RQ2 Longitudinal Change Summary\n\n"
        "| Site | Category | Severity | Event count | Event types | User implication | Follow-up |\n"
        "|---|---|---|---|---|---|---|\n"
        f"{_render_rq2_rows(targets, summaries)}\n\n"
        "## Source Tables\n\n"
        f"- Targets: `{targets_csv}`\n"
        f"- RQ1 audit reports: `{audit_summary_csv}`\n"
        f"- RQ2 longitudinal summaries: `{longitudinal_summary_csv}`\n"
    )


def _render_rq1_rows(
    targets: list[dict[str, str]],
    reports: dict[str, dict[str, str]],
) -> str:
    rows: list[str] = []
    for target in targets:
        report = _report_for(target, reports)
        rows.append(
            "| "
            f"{_cell(target.get('name', '') or target.get('url', ''))} | "
            f"{_cell(target.get('category', ''))} | "
            f"{_cell(_banner_evidence_label(report))} | "
            f"{_cell(_rq1_coding_note(report))} | "
            f"{_cell(report.get('tier', 'missing'))} | "
            f"{_cell(_gate_status(report))} | "
            f"{_cell(_available_paths(report))} | "
            f"{_cell(_missing_paths(report))} | "
            f"{_cell(_layer2_effort(report))} | "
            f"{_cell(report.get('transparency_grade') or 'missing')} | "
            f"{_cell(report.get('unbiased_choice_grade') or 'missing')} | "
            f"{_cell(_evidence_refs(report))} |"
        )
    return "\n".join(rows)


def _render_rq2_rows(
    targets: list[dict[str, str]],
    summaries: dict[str, dict[str, str]],
) -> str:
    rows: list[str] = []
    for target in targets:
        summary = _summary_for(target, summaries)
        rows.append(
            "| "
            f"{_cell(target.get('name', '') or target.get('url', ''))} | "
            f"{_cell(target.get('category', ''))} | "
            f"{_cell(summary.get('severity', 'missing'))} | "
            f"{_cell(summary.get('event_count', 'missing'))} | "
            f"{_cell(_event_types(summary))} | "
            f"{_cell(summary.get('implications_for_user') or 'missing')} | "
            f"{_cell(_follow_up(summary))} |"
        )
    return "\n".join(rows)


def _report_for(
    target: dict[str, str],
    reports: dict[str, dict[str, str]],
) -> dict[str, str]:
    return reports.get(_canonicalize_url(target.get("url", "")), {})


def _summary_for(
    target: dict[str, str],
    summaries: dict[str, dict[str, str]],
) -> dict[str, str]:
    return summaries.get(_canonicalize_url(target.get("url", "")), {})


def _gate_status(report: dict[str, str]) -> str:
    if not report:
        return "missing"
    return "pass" if _parse_bool(report.get("layer1_gate_passed", "")) else "fail"


def _available_paths(report: dict[str, str]) -> str:
    if not report:
        return "missing"
    available = [
        label
        for label, field in [
            ("Accept", "accept_available"),
            ("Reject", "reject_available"),
            ("Customize", "customize_available"),
            ("Dismiss", "dismiss_available"),
        ]
        if _parse_bool(report.get(field, ""))
    ]
    return "+".join(available) if available else "none"


def _missing_paths(report: dict[str, str]) -> str:
    if not report:
        return "missing"
    return report.get("missing_paths") or "none"


def _layer2_effort(report: dict[str, str]) -> str:
    if not report:
        return "missing"
    effort = report.get("layer2_mean_effort", "")
    category = report.get("layer2_overall_category", "")
    if effort and category:
        return f"{effort} / {category}"
    return "not scored"


def _evidence_refs(report: dict[str, str]) -> str:
    if not report:
        return "missing"
    refs = [
        ref
        for ref in [
            report.get("first_screenshot_ref", ""),
            report.get("first_dom_snapshot_ref", ""),
        ]
        if ref
    ]
    return "; ".join(refs) if refs else "missing"


def _event_types(summary: dict[str, str]) -> str:
    if not summary:
        return "missing"
    event_types = summary.get("event_types", "")
    return event_types.replace("|", "+") if event_types else "none"


def _follow_up(summary: dict[str, str]) -> str:
    if not summary:
        return "Capture another observation or mark the gap in limitations."
    severity = summary.get("severity", "")
    event_count = summary.get("event_count", "")
    if severity == "A" and event_count == "0":
        return "No immediate follow-up."
    if _parse_bool(summary.get("has_pathway_change", "")) or _parse_bool(
        summary.get("has_score_change", "")
    ):
        return "Review before paper coding."
    return "Use as longitudinal context."


def _banner_evidence_class(report: dict[str, str]) -> str:
    if not report:
        return "missing"
    if _parse_bool(report.get("banner_detected", "")):
        return "banner_present"
    return "no_visible_banner"


def _banner_evidence_label(report: dict[str, str]) -> str:
    banner_class = _banner_evidence_class(report)
    if banner_class == "banner_present":
        return "banner/control evidence"
    if banner_class == "no_visible_banner":
        return "no visible first-screen banner"
    return "missing"


def _rq1_coding_note(report: dict[str, str]) -> str:
    banner_class = _banner_evidence_class(report)
    if banner_class == "banner_present":
        return "banner-present scored case"
    if banner_class == "no_visible_banner":
        return "no-visible-banner contrast; do not treat as banner-path failure"
    return "missing evidence"


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
