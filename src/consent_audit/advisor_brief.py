"""Advisor-facing weekly research update briefs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def export_weekly_advisor_brief(
    *,
    targets_csv: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    cmp_confirmation_csv: Path,
    manifest_json: Path,
    out_md: Path,
    title: str,
) -> str:
    """Write a compact Markdown update from the current research tables."""

    targets = _read_rows(targets_csv)
    latest_reports = _latest_by_url(_read_rows(audit_summary_csv), date_key="captured_at")
    latest_summaries = _latest_by_url(
        _read_rows(longitudinal_summary_csv),
        date_key="week_of",
    )
    confirmation_rows = _read_rows(cmp_confirmation_csv)
    manifest = _read_manifest(manifest_json)

    text = _render_brief(
        title=title,
        targets=targets,
        latest_reports=latest_reports,
        latest_summaries=latest_summaries,
        confirmation_rows=confirmation_rows,
        manifest=manifest,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _render_brief(
    *,
    title: str,
    targets: list[dict[str, str]],
    latest_reports: dict[str, dict[str, str]],
    latest_summaries: dict[str, dict[str, str]],
    confirmation_rows: list[dict[str, str]],
    manifest: dict[str, object],
) -> str:
    status_counts = _count_values(confirmation_rows, "confirmation_status", default="pending")
    draft_counts = _count_values(confirmation_rows, "draft_decision", default="unknown")
    target_rows = _render_target_rows(targets, latest_reports, latest_summaries)
    cmp_status = _format_counts(status_counts)
    draft_status = _format_counts(draft_counts)

    return (
        f"# {title}\n\n"
        "## Snapshot\n\n"
        f"- Target sites: {len(targets)}\n"
        f"- Audit reports in package: {manifest.get('audit_report_count', 0)}\n"
        f"- Longitudinal summaries in package: {manifest.get('weekly_summary_count', 0)}\n"
        f"- CMP confirmations: {cmp_status or 'none'}\n"
        f"- Draft CMP decisions: {draft_status or 'none'}\n\n"
        "## Week 2 Target Status\n\n"
        "| Site | Category | Latest tier | Path status | Longitudinal |\n"
        "|---|---|---|---|---|\n"
        f"{target_rows}\n\n"
        "## Advisor Review Queue\n\n"
        "- Confirm pending CMP rows before changing sample-lock status.\n"
        "- Decide whether no-banner contrast cases belong in the methods section.\n"
        "- Replace Reddit and Walmart unless advisor wants them as access-friction cases.\n"
        "- Continue weekly capture on the frozen 5-site list while manual review is pending.\n"
    )


def _render_target_rows(
    targets: list[dict[str, str]],
    latest_reports: dict[str, dict[str, str]],
    latest_summaries: dict[str, dict[str, str]],
) -> str:
    rows: list[str] = []
    for target in targets:
        url = target.get("url", "")
        canonical_url = _canonicalize_url(url)
        report = latest_reports.get(canonical_url, {})
        summary = latest_summaries.get(canonical_url, {})
        rows.append(
            "| "
            f"{_escape_table_cell(target.get('name', '') or url)} | "
            f"{_escape_table_cell(target.get('category', ''))} | "
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
        if current is None or row.get(date_key, "") > current.get(date_key, ""):
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
