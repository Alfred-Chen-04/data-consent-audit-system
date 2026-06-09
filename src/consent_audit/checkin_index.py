"""Advisor check-in index generation."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def export_checkin_index(
    *,
    out_md: Path,
    title: str,
    advisor_brief: Path,
    sanity_check: Path,
    capture_checklist: Path,
    cycle_report: Path,
    runbook: Path,
    sample_plan: Path,
    cmp_confirmation_sheet: Path,
    cmp_packet: Path,
    research_package_dir: Path,
    research_manifest: Path,
) -> str:
    """Write a Markdown index for the current advisor check-in packet."""

    manifest = _read_manifest(research_manifest)
    files = manifest.get("files", {})
    package_files = files if isinstance(files, dict) else {}
    audit_summary = research_package_dir / str(
        package_files.get("audit_report_summary", "audit_report_summary.csv")
    )
    longitudinal_summary = research_package_dir / str(
        package_files.get("longitudinal_summary", "longitudinal_summary.csv")
    )
    sanity_status = _extract_sanity_status(sanity_check)

    text = _render_index(
        title=title,
        out_md=out_md,
        advisor_brief=advisor_brief,
        sanity_check=sanity_check,
        capture_checklist=capture_checklist,
        cycle_report=cycle_report,
        runbook=runbook,
        sample_plan=sample_plan,
        cmp_confirmation_sheet=cmp_confirmation_sheet,
        cmp_packet=cmp_packet,
        research_package_dir=research_package_dir,
        research_manifest=research_manifest,
        audit_summary=audit_summary,
        longitudinal_summary=longitudinal_summary,
        sanity_status=sanity_status,
        manifest=manifest,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _render_index(
    *,
    title: str,
    out_md: Path,
    advisor_brief: Path,
    sanity_check: Path,
    capture_checklist: Path,
    cycle_report: Path,
    runbook: Path,
    sample_plan: Path,
    cmp_confirmation_sheet: Path,
    cmp_packet: Path,
    research_package_dir: Path,
    research_manifest: Path,
    audit_summary: Path,
    longitudinal_summary: Path,
    sanity_status: str,
    manifest: dict[str, Any],
) -> str:
    return (
        f"# {title}\n\n"
        "Use this index as the first file for advisor check-ins.\n\n"
        "## Status\n\n"
        f"- Week 2 sanity status: `{sanity_status}`\n"
        f"- Audit reports in package: {manifest.get('audit_report_count', 'unknown')}\n"
        f"- Longitudinal summaries in package: "
        f"{manifest.get('weekly_summary_count', 'unknown')}\n"
        "- CMP review state: pending advisor confirmation\n\n"
        "## Read First\n\n"
        f"- [Advisor update]({_relative_link(out_md, advisor_brief)})\n"
        f"- [Sanity check]({_relative_link(out_md, sanity_check)})\n"
        f"- [Capture checklist]({_relative_link(out_md, capture_checklist)})\n"
        f"- [Cycle report]({_relative_link(out_md, cycle_report)})\n"
        f"- [Execution runbook]({_relative_link(out_md, runbook)})\n"
        f"- [Week 2 sample plan]({_relative_link(out_md, sample_plan)})\n\n"
        "## Data Package\n\n"
        f"- [Research package]({_relative_link(out_md, research_package_dir)})\n"
        f"- [Research manifest]({_relative_link(out_md, research_manifest)})\n"
        f"- [Audit report summary]({_relative_link(out_md, audit_summary)})\n"
        f"- [Longitudinal summary]({_relative_link(out_md, longitudinal_summary)})\n\n"
        "## Manual Review\n\n"
        f"- [CMP confirmation sheet]({_relative_link(out_md, cmp_confirmation_sheet)})\n"
        f"- [CMP evidence packet]({_relative_link(out_md, cmp_packet)})\n\n"
        "## Run Controls\n\n"
        "- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-preflight-check`\n"
        "- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-cycle --dry-run`\n"
        "- `AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m "
        "consent_audit.cli week2-cycle`\n"
        "- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-refresh-outputs`\n"
        "- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-capture-checklist`\n"
        "- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "export-research-package`\n"
        "- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "advisor-update-brief`\n"
        "- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-sanity-check`\n"
        "- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli checkin-index`\n"
    )


def _extract_sanity_status(sanity_check: Path) -> str:
    try:
        text = sanity_check.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "unknown"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- Overall status:"):
            return stripped.split(":", 1)[1].strip().strip("`") or "unknown"
    return "unknown"


def _read_manifest(research_manifest: Path) -> dict[str, Any]:
    try:
        data: object = json.loads(research_manifest.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(key): value for key, value in data.items()}


def _relative_link(out_md: Path, target: Path) -> str:
    relative = os.path.relpath(target, start=out_md.parent)
    return relative.replace(os.sep, "/")
