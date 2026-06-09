"""Generate a current-evidence SSRP paper skeleton."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlparse, urlunparse

RQ1 = (
    "How to develop a computational audit and scoring system to quantify the "
    "layered consent interfaces in terms of unbiased choice across the full "
    "consent pathway?"
)
RQ2 = (
    "How can we automatically capture and version firms' privacy interfaces "
    "to systematically document interface changes over time?"
)


def export_ssrp_paper_skeleton(
    *,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    manifest_json: Path,
    out_md: Path,
    title: str,
    week_label: str,
) -> str:
    """Write a Markdown paper skeleton grounded in the current research package."""

    targets = _read_rows(targets_csv)
    reports = _read_rows(audit_summary_csv)
    summaries = _read_rows(longitudinal_summary_csv)
    manifest = _read_manifest(manifest_json)
    latest_reports = _latest_by_url(reports, date_key="captured_at")
    latest_summaries = _latest_by_url(summaries, date_key="week_of")

    text = _render_skeleton(
        title=title,
        week_label=week_label,
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        manifest_json=manifest_json,
        targets=targets,
        manifest=manifest,
        latest_reports=latest_reports,
        latest_summaries=latest_summaries,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _render_skeleton(
    *,
    title: str,
    week_label: str,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    manifest_json: Path,
    targets: list[dict[str, str]],
    manifest: dict[str, object],
    latest_reports: dict[str, dict[str, str]],
    latest_summaries: dict[str, dict[str, str]],
) -> str:
    target_reports = [
        latest_reports.get(_canonicalize_url(target.get("url", "")), {})
        for target in targets
    ]
    target_summaries = [
        latest_summaries.get(_canonicalize_url(target.get("url", "")), {})
        for target in targets
    ]
    tier_counts = _count_values(target_reports, "tier", default="missing")
    banner_counts = _count_banner_classes(target_reports)
    banner_tier_counts = _count_banner_present_values(target_reports, "tier")
    severity_counts = _count_values(target_summaries, "severity", default="missing")

    return (
        f"# {title}\n\n"
        "## Abstract Draft\n\n"
        "This paper presents a traceable computational audit framework for "
        "layered consent interfaces and a longitudinal capture workflow for "
        "documenting how those interfaces change over time. The current draft "
        "uses the completed Week 2 evidence gate as pilot evidence, not as the "
        "final SSRP dataset.\n\n"
        "## Research Questions\n\n"
        f"1. {RQ1}\n"
        f"2. {RQ2}\n\n"
        "## Current Evidence Snapshot\n\n"
        f"- Evidence window: {week_label}\n"
        f"- Target sites: {len(targets)}\n"
        f"- Categories: {_format_counts(_count_values(targets, 'category', default='unknown')) or 'none'}\n"
        f"- Audit reports in package: {manifest.get('audit_report_count', 0)}\n"
        f"- Longitudinal summaries in package: {manifest.get('weekly_summary_count', 0)}\n"
        f"- Banner evidence classes: {_format_counts(banner_counts) or 'none'}\n"
        f"- Banner-present automated tiers: {_format_counts(banner_tier_counts) or 'none'}\n"
        f"- Raw automated target tiers: {_format_counts(tier_counts) or 'none'}\n"
        f"- Latest longitudinal severity: {_format_counts(severity_counts) or 'none'}\n\n"
        "## Draft Section Map\n\n"
        "Generated drafting artifact: run `consent-audit ssrp-writing-pack` "
        "to refresh `docs/research/ssrp_writing_pack_2026-06-06.md`.\n\n"
        "1. Introduction: consent interfaces as privacy communication and why static audits miss operational change.\n"
        "2. Background: Notice-and-Choice, cookie-banner auditing, longitudinal privacy measurement, and multimodal agents as method.\n"
        "3. Methods: three-layer scoring, evidence requirements, deterministic grades after schema validation, and weekly capture/versioning.\n"
        "4. Pilot Evidence: current RQ1 scoring table and RQ2 longitudinal change summaries.\n"
        "5. Discussion: what longitudinal evidence adds, what is not a legal determination, and small GRC/SOC 2 relevance note.\n"
        "6. Limitations: desktop-only, public unauthenticated pages, English-focused, location/session effects, and manual validation gates.\n\n"
        "## Current Deep-Sample Evidence Table\n\n"
        "| Site | Category | Banner evidence | RQ1 coding | Latest automated tier | Path status | Longitudinal |\n"
        "|---|---|---|---|---|---|---|\n"
        f"{_render_target_rows(targets, latest_reports, latest_summaries)}\n\n"
        "## Results Tables To Fill\n\n"
        "Generated table artifact: run `consent-audit ssrp-results-tables` "
        "to refresh `docs/research/ssrp_results_tables_2026-06-06.md`.\n\n"
        "| Table | Purpose | Current source |\n"
        "|---|---|---|\n"
        "| RQ1 scoring summary | Path availability, tier, Layer 2/3 columns by site | `data/research_package/audit_report_summary.csv` |\n"
        "| RQ2 longitudinal summary | Event counts, event types, severity, implications by site-week | `data/research_package/longitudinal_summary.csv` |\n"
        "| Sample construction log | Why sites were selected, replaced, or held for review | `data/sample_lock_plan_pilot_2026-05-30.csv` |\n\n"
        "## Figure Queue\n\n"
        "Generated figure artifact: run `consent-audit ssrp-figure-plan` "
        "to refresh `docs/research/ssrp_figure_plan_2026-06-06.md`.\n\n"
        "- Architecture diagram: URL to capture bundle to three layers to report/export.\n"
        "- Three-layer rubric table from `CONCEPTS.md`.\n"
        "- Evidence card example with screenshot, DOM/hash refs, pathway outcomes, and quotes.\n"
        "- Longitudinal timeline for 2-3 sites with visible change events.\n\n"
        "## Known Gaps Before Draft Freeze\n\n"
        "- Review the completed Week 2 evidence gate and select the strongest examples.\n"
        "- Resolve or explicitly bracket the 8 pending CMP/manual-review rows.\n"
        "- Decide whether no-banner contrast cases belong in the methods section.\n"
        "- Add final limitations text after the observed capture failures and manual-review outcomes are known.\n\n"
        "## Source Artifacts\n\n"
        f"- Targets: `{targets_csv}`\n"
        f"- RQ1 table: `{audit_summary_csv}`\n"
        f"- RQ2 table: `{longitudinal_summary_csv}`\n"
        f"- Manifest: `{manifest_json}`\n"
    )


def _render_target_rows(
    targets: list[dict[str, str]],
    latest_reports: dict[str, dict[str, str]],
    latest_summaries: dict[str, dict[str, str]],
) -> str:
    rows: list[str] = []
    for target in targets:
        url = target.get("url", "")
        report = latest_reports.get(_canonicalize_url(url), {})
        summary = latest_summaries.get(_canonicalize_url(url), {})
        rows.append(
            "| "
            f"{_escape_table_cell(target.get('name', '') or url)} | "
            f"{_escape_table_cell(target.get('category', ''))} | "
            f"{_escape_table_cell(_banner_evidence_label(report))} | "
            f"{_escape_table_cell(_rq1_coding_note(report))} | "
            f"{_escape_table_cell(report.get('tier', 'missing'))} | "
            f"{_escape_table_cell(_path_status(report))} | "
            f"{_escape_table_cell(_longitudinal_status(summary))} |"
        )
    return "\n".join(rows)


def _path_status(report: dict[str, str]) -> str:
    if not report:
        return "missing report"
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
    if available:
        return "+".join(available)
    missing = report.get("missing_paths", "").strip()
    return f"missing {missing}" if missing else "no paths detected"


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


def _longitudinal_status(summary: dict[str, str]) -> str:
    if not summary:
        return "missing"
    return f"{summary.get('severity', '')} / {summary.get('event_count', '')}"


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


def _read_manifest(path: Path) -> dict[str, object]:
    data: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {}
    return {str(key): value for key, value in data.items()}


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


def _count_banner_classes(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = _banner_evidence_class(row)
        counts[value] = counts.get(value, 0) + 1
    return counts


def _count_banner_present_values(
    rows: list[dict[str, str]],
    key: str,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        if _banner_evidence_class(row) != "banner_present":
            continue
        value = (row.get(key) or "missing").strip() or "missing"
        counts[value] = counts.get(value, 0) + 1
    return counts


def _format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}={count}" for key, count in sorted(counts.items()))


def _escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))
