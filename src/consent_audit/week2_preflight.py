"""Week 2 preflight readiness checks."""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any

from consent_audit.site_list import SiteListValidation, validate_site_list


def export_week2_preflight_check(
    *,
    targets_csv: Path,
    sanity_check_md: Path,
    advisor_brief_md: Path,
    checkin_index_md: Path,
    runbook_md: Path,
    research_manifest_json: Path,
    cmp_confirmation_csv: Path,
    cmp_packet_html: Path,
    out_md: Path,
    title: str,
    expected_target_count: int,
) -> str:
    """Write a Markdown preflight check for the scheduled Week 2 capture."""

    target_validation = validate_site_list(targets_csv)
    sanity_status = _extract_sanity_status(sanity_check_md)
    manifest = _read_manifest(research_manifest_json)
    confirmation_counts = _count_confirmation_statuses(cmp_confirmation_csv)
    required_files = [
        ("Advisor update", advisor_brief_md),
        ("Sanity check", sanity_check_md),
        ("Check-in index", checkin_index_md),
        ("Execution runbook", runbook_md),
        ("Research manifest", research_manifest_json),
        ("CMP confirmation sheet", cmp_confirmation_csv),
        ("CMP evidence packet", cmp_packet_html),
    ]

    text = _render_preflight(
        title=title,
        out_md=out_md,
        targets_csv=targets_csv,
        target_validation=target_validation,
        expected_target_count=expected_target_count,
        sanity_status=sanity_status,
        manifest=manifest,
        confirmation_counts=confirmation_counts,
        required_files=required_files,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _render_preflight(
    *,
    title: str,
    out_md: Path,
    targets_csv: Path,
    target_validation: SiteListValidation,
    expected_target_count: int,
    sanity_status: str,
    manifest: dict[str, Any],
    confirmation_counts: dict[str, int],
    required_files: list[tuple[str, Path]],
) -> str:
    overall_status = _overall_status(
        target_validation=target_validation,
        expected_target_count=expected_target_count,
        sanity_status=sanity_status,
        manifest=manifest,
        required_files=required_files,
    )
    target_status = (
        "passed"
        if not target_validation.errors
        and target_validation.active_count == expected_target_count
        else "needs_attention"
    )
    required_file_rows = "\n".join(
        _render_required_file_row(out_md, label, path) for label, path in required_files
    )
    issue_rows = "\n".join(_render_issue_row(issue) for issue in target_validation.issues)
    if not issue_rows:
        issue_rows = "| none | - | - | - |"

    return (
        f"# {title}\n\n"
        "## Summary\n\n"
        f"- Overall status: {overall_status}\n"
        f"- Week 2 targets: {target_validation.active_count}/{expected_target_count}\n"
        f"- Target validation: {target_status}\n"
        f"- Sanity status: `{sanity_status}`\n"
        f"- Audit reports in package: {manifest.get('audit_report_count', 0)}\n"
        f"- Longitudinal summaries in package: "
        f"{manifest.get('weekly_summary_count', 0)}\n"
        f"- CMP confirmations: {_format_counts(confirmation_counts) or 'none'}\n"
        f"- Categories: {_format_counts(target_validation.categories) or 'none'}\n"
        f"- Mentor-inherited rows: "
        f"{target_validation.inherited_from_phd_mentor_count}\n\n"
        "## Required Files\n\n"
        "| Artifact | Status | Link |\n"
        "|---|---|---|\n"
        f"{required_file_rows}\n\n"
        "## Target CSV\n\n"
        f"- [Week 2 targets]({_relative_link(out_md, targets_csv)})\n\n"
        "## Target Issues\n\n"
        "| Level | Code | Row | Message |\n"
        "|---|---|---|---|\n"
        f"{issue_rows}\n"
    )


def _overall_status(
    *,
    target_validation: SiteListValidation,
    expected_target_count: int,
    sanity_status: str,
    manifest: dict[str, Any],
    required_files: list[tuple[str, Path]],
) -> str:
    if target_validation.errors:
        return "needs_attention"
    if target_validation.active_count != expected_target_count:
        return "needs_attention"
    if any(not path.exists() for _, path in required_files):
        return "needs_attention"
    if int(manifest.get("audit_report_count", 0) or 0) <= 0:
        return "needs_attention"
    if int(manifest.get("weekly_summary_count", 0) or 0) <= 0:
        return "needs_attention"
    if sanity_status not in {"pending_capture", "ready"}:
        return "needs_attention"
    return "ready_for_capture"


def _render_required_file_row(out_md: Path, label: str, path: Path) -> str:
    status = "present" if path.exists() else "missing"
    return (
        "| "
        f"{_escape_table_cell(label)} | "
        f"{status} | "
        f"[{_escape_table_cell(label)}]({_relative_link(out_md, path)}) |"
    )


def _render_issue_row(issue: object) -> str:
    level = str(getattr(issue, "level", ""))
    code = str(getattr(issue, "code", ""))
    row_number = getattr(issue, "row_number", None)
    message = str(getattr(issue, "message", ""))
    return (
        "| "
        f"{_escape_table_cell(level)} | "
        f"{_escape_table_cell(code)} | "
        f"{row_number or '-'} | "
        f"{_escape_table_cell(message)} |"
    )


def _count_confirmation_statuses(path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    try:
        with path.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if not (row.get("url") or "").strip():
                    continue
                status = (row.get("confirmation_status") or "pending").strip() or "pending"
                counts[status] = counts.get(status, 0) + 1
    except FileNotFoundError:
        return {}
    return counts


def _extract_sanity_status(sanity_check_md: Path) -> str:
    try:
        text = sanity_check_md.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "unknown"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- Overall status:"):
            return stripped.split(":", 1)[1].strip().strip("`") or "unknown"
    return "unknown"


def _read_manifest(path: Path) -> dict[str, Any]:
    try:
        data: object = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(key): value for key, value in data.items()}


def _format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}={count}" for key, count in sorted(counts.items()))


def _relative_link(out_md: Path, target: Path) -> str:
    relative = os.path.relpath(target, start=out_md.parent)
    return relative.replace(os.sep, "/")


def _escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|")
