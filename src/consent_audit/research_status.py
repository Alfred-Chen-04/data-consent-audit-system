"""Compact current-state dashboard for the SSRP research workflow."""

from __future__ import annotations

import csv
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any


def render_research_status(
    *,
    targets_csv: Path,
    research_manifest_json: Path,
    cmp_confirmation_csv: Path,
    preflight_md: Path,
    sanity_md: Path,
    cycle_report_md: Path,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    figure_plan_md: Path,
    writing_pack_md: Path,
    claim_register_md: Path,
    poster_plan_md: Path,
) -> str:
    """Render a concise status view from existing research artifacts."""

    target_rows = _read_rows(targets_csv)
    categories = _count_values(target_rows, "category", default="unknown")
    manifest = _read_manifest(research_manifest_json)
    confirmation_rows = _read_rows(cmp_confirmation_csv)
    confirmation_counts = _count_values(
        confirmation_rows,
        "confirmation_status",
        default="pending",
    )
    preflight_status = _extract_bullet_value(preflight_md, "Overall status")
    sanity_status = _extract_bullet_value(sanity_md, "Overall status")
    cycle_capture_status = _extract_bullet_value(cycle_report_md, "Capture status")
    next_action = _extract_next_action(cycle_report_md)
    paper_artifacts = {
        "figure_plan": _artifact_status(figure_plan_md),
        "paper_skeleton": _artifact_status(paper_skeleton_md),
        "poster_plan": _artifact_status(poster_plan_md),
        "claim_register": _artifact_status(claim_register_md),
        "results_tables": _artifact_status(results_tables_md),
        "writing_pack": _artifact_status(writing_pack_md),
    }

    return (
        "# SSRP Research Status\n\n"
        "## Snapshot\n\n"
        f"- Week 2 targets: {len(target_rows)}\n"
        f"- Categories: {_format_counts(categories) or 'none'}\n"
        f"- Preflight status: `{preflight_status}`\n"
        f"- Sanity status: `{sanity_status}`\n"
        f"- Cycle capture status: `{cycle_capture_status}`\n"
        f"- Audit reports in package: {manifest.get('audit_report_count', 0)}\n"
        f"- Longitudinal summaries in package: {manifest.get('weekly_summary_count', 0)}\n"
        f"- CMP confirmations: {_format_counts(confirmation_counts) or 'none'}\n"
        f"- Paper artifacts: {_format_counts(paper_artifacts)}\n"
        f"- Next action: {next_action}\n\n"
        "## Key Artifacts\n\n"
        f"- Targets: `{targets_csv}`\n"
        f"- Research manifest: `{research_manifest_json}`\n"
        f"- CMP confirmation sheet: `{cmp_confirmation_csv}`\n"
        f"- Preflight check: `{preflight_md}`\n"
        f"- Sanity check: `{sanity_md}`\n"
        f"- Cycle report: `{cycle_report_md}`\n"
        f"- SSRP results tables: `{results_tables_md}`\n"
        f"- SSRP paper skeleton: `{paper_skeleton_md}`\n"
        f"- SSRP figure plan: `{figure_plan_md}`\n"
        f"- SSRP writing pack: `{writing_pack_md}`\n"
        f"- SSRP claim register: `{claim_register_md}`\n"
        f"- SSRP poster plan: `{poster_plan_md}`\n"
    )


def _read_rows(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8") as csv_file:
            return [
                {str(key): (value or "").strip() for key, value in row.items()}
                for row in csv.DictReader(csv_file)
                if (row.get("url") or "").strip()
            ]
    except FileNotFoundError:
        return []


def _read_manifest(path: Path) -> dict[str, Any]:
    try:
        data: object = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
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


def _extract_bullet_value(path: Path, label: str) -> str:
    prefix = f"- {label}:"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return "missing"
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped.split(":", 1)[1].strip().strip("`") or "unknown"
    return "unknown"


def _extract_next_action(path: Path) -> str:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return "Open the Week 2 runbook and regenerate preflight/check-in artifacts."

    in_next_action = False
    for line in lines:
        stripped = line.strip()
        if stripped == "## Next Action":
            in_next_action = True
            continue
        if in_next_action and stripped.startswith("## "):
            break
        if in_next_action and stripped.startswith("- "):
            return stripped[2:].strip()
    return "Open the Week 2 check-in index and follow the Run Controls sequence."


def _artifact_status(path: Path) -> str:
    return "present" if path.exists() else "missing"


def _format_counts(counts: Mapping[str, object]) -> str:
    return ", ".join(f"{key}={count}" for key, count in sorted(counts.items()))
