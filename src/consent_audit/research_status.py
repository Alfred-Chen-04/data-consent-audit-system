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
    closeout_manifest_json: Path,
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
    current_closeout_md: Path,
    final_qa_csv: Path,
    human_closeout_confirmation_csv: Path,
    final_index_md: Path,
) -> str:
    """Render a concise status view from existing research artifacts."""

    target_rows = _read_rows(targets_csv)
    categories = _count_values(target_rows, "category", default="unknown")
    manifest = _read_manifest(research_manifest_json)
    closeout_manifest = _read_manifest(closeout_manifest_json)
    closeout_summary = _mapping_value(closeout_manifest, "summary")
    revision_gate = _mapping_value(
        closeout_manifest, "revision_execution_gate"
    )
    revision_status_counts = _mapping_value(revision_gate, "status_counts")
    freeze_readiness = _mapping_value(closeout_manifest, "freeze_readiness")
    confirmation_rows = _read_rows(cmp_confirmation_csv)
    confirmation_counts = _count_values(
        confirmation_rows,
        "confirmation_status",
        default="pending",
    )
    final_qa_rows = _read_all_rows(final_qa_csv)
    final_qa_counts = _count_values(
        final_qa_rows,
        "status",
        default="pending",
    )
    human_closeout_rows = _read_all_rows(human_closeout_confirmation_csv)
    human_closeout_counts = _count_values(
        human_closeout_rows,
        "status",
        default="pending",
    )
    pending_human_confirmations = sorted(
        row.get("confirmation_id", "unknown")
        for row in human_closeout_rows
        if row.get("status") != "verified"
    )
    preflight_status = _extract_bullet_value(preflight_md, "Overall status")
    sanity_status = _extract_bullet_value(sanity_md, "Overall status")
    cycle_capture_status = _extract_bullet_value(cycle_report_md, "Capture status")
    next_action = _extract_next_action(cycle_report_md)
    support_artifacts = {
        "figure_plan": _artifact_status(figure_plan_md),
        "paper_skeleton": _artifact_status(paper_skeleton_md),
        "poster_plan": _artifact_status(poster_plan_md),
        "claim_register": _artifact_status(claim_register_md),
        "results_tables": _artifact_status(results_tables_md),
        "writing_pack": _artifact_status(writing_pack_md),
    }
    present_deliverables = _integer_value(
        closeout_summary, "present_key_deliverable_count"
    )
    total_deliverables = _integer_value(
        closeout_summary, "key_deliverable_count"
    )
    response_basis_claims = _integer_value(
        closeout_summary, "revision_response_basis_claim_count"
    )
    response_basis_errors = _integer_value(
        closeout_summary, "revision_response_basis_error_count"
    )
    decision_contract_errors = _integer_value(
        closeout_summary, "joint_decision_contract_error_count"
    )
    freeze_ready = _boolean_label(
        closeout_summary.get("ready_for_final_freeze")
    )
    freeze_blockers = _format_blockers(freeze_readiness.get("blockers"))
    closeout_next_action = _closeout_next_action(
        closeout_manifest,
        closeout_summary,
        freeze_readiness,
        final_qa_rows,
        final_index_md,
    )

    return (
        "# SSRP Research Status\n\n"
        "## Snapshot\n\n"
        "- Current phase: `closeout`\n"
        f"- Closeout control index: `{current_closeout_md}` "
        f"({_artifact_status(current_closeout_md)})\n"
        f"- Closeout manifest: `{closeout_manifest.get('manifest_status', 'missing')}`; "
        f"key deliverables={present_deliverables}/{total_deliverables}\n"
        f"- Revision execution: "
        f"{_format_counts(revision_status_counts) or 'none'}\n"
        f"- Response-basis claims: {response_basis_claims}; "
        f"validation errors: {response_basis_errors + decision_contract_errors}\n"
        f"- Final-freeze readiness: `{freeze_ready}`; "
        f"blockers={freeze_blockers or 'none'}\n"
        f"- Final QA: {_format_counts(final_qa_counts) or 'missing'}; "
        f"final index={_artifact_status(final_index_md)}\n"
        f"- External confirmations: "
        f"{_format_counts(human_closeout_counts) or 'missing'}; "
        f"pending={', '.join(pending_human_confirmations) or 'none'}\n"
        f"- Current next action: {closeout_next_action}\n"
        f"- Week 2 targets: {len(target_rows)}\n"
        f"- Categories: {_format_counts(categories) or 'none'}\n"
        f"- Preflight status: `{preflight_status}`\n"
        f"- Sanity status: `{sanity_status}`\n"
        f"- Cycle capture status: `{cycle_capture_status}`\n"
        f"- Audit reports in package: {manifest.get('audit_report_count', 0)}\n"
        f"- Longitudinal summaries in package: {manifest.get('weekly_summary_count', 0)}\n"
        f"- CMP confirmations: {_format_counts(confirmation_counts) or 'none'}\n"
        f"- Historical/support artifacts: {_format_counts(support_artifacts)}\n"
        f"- Historical cycle-report next action: {next_action}\n\n"
        "## Current Closeout Artifacts\n\n"
        f"- Closeout control index: `{current_closeout_md}`\n"
        f"- Closeout pre-freeze manifest: `{closeout_manifest_json}`\n"
        f"- Final QA checklist: `{final_qa_csv}`\n"
        f"- Human closeout confirmations: `{human_closeout_confirmation_csv}`\n"
        f"- Final closeout index: `{final_index_md}`\n\n"
        "## Historical And Supporting Artifacts\n\n"
        f"- Targets: `{targets_csv}`\n"
        f"- Research manifest: `{research_manifest_json}`\n"
        f"- CMP confirmation sheet: `{cmp_confirmation_csv}`\n"
        f"- Preflight check: `{preflight_md}`\n"
        f"- Sanity check: `{sanity_md}`\n"
        f"- Cycle report: `{cycle_report_md}`\n"
        f"- SSRP results tables: `{results_tables_md}`\n"
        f"- Optional future-paper skeleton: `{paper_skeleton_md}`\n"
        f"- SSRP presentation/poster figure plan: `{figure_plan_md}`\n"
        f"- SSRP writing support pack: `{writing_pack_md}`\n"
        f"- SSRP evidence claim register: `{claim_register_md}`\n"
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


def _read_all_rows(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8") as csv_file:
            return [
                {str(key): (value or "").strip() for key, value in row.items()}
                for row in csv.DictReader(csv_file)
                if any((value or "").strip() for value in row.values())
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


def _mapping_value(data: Mapping[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        return {}
    return {str(item_key): item_value for item_key, item_value in value.items()}


def _integer_value(data: Mapping[str, Any], key: str) -> int:
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        return 0
    return value


def _boolean_label(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return "unknown"


def _format_blockers(value: object) -> str:
    if not isinstance(value, list):
        return ""
    blockers: dict[str, int] = {}
    for item in value:
        if not isinstance(item, dict):
            continue
        code = item.get("code")
        count = item.get("count")
        if isinstance(code, str) and isinstance(count, int) and not isinstance(
            count, bool
        ):
            blockers[code] = count
    return _format_counts(blockers)


def _closeout_next_action(
    closeout_manifest: Mapping[str, Any],
    summary: Mapping[str, Any],
    freeze_readiness: Mapping[str, Any],
    final_qa_rows: list[dict[str, str]],
    final_index_md: Path,
) -> str:
    if not closeout_manifest:
        return "Regenerate the pre-freeze manifest before making closeout claims."
    if summary.get("ready_for_final_freeze") is True:
        pending_ids = [
            row.get("check_id", "unknown")
            for row in final_qa_rows
            if row.get("status") != "verified"
        ]
        if pending_ids:
            return (
                "Complete pending final-QA checks: "
                f"{', '.join(pending_ids)}; then dry-run closeout-final-index."
            )
        if not final_index_md.is_file():
            return (
                "All final-QA checks are verified; dry-run closeout-final-index, "
                "then write and open the final index."
            )
        return (
            "Open the final index and its linked artifacts for the final handoff."
        )
    if _integer_value(summary, "revision_response_basis_claim_count") == 0:
        return (
            "Record actual joint decisions through July 29; if none are "
            "recorded, wait until the internal cutoff before selecting the "
            "documented project fallbacks."
        )
    unapplied = _integer_value(
        summary, "revision_rows_not_applied_verified_count"
    )
    if unapplied:
        return (
            f"Apply and verify the {unapplied} remaining mapped revision rows "
            "using validated response bases."
        )
    blockers = _format_blockers(freeze_readiness.get("blockers"))
    return f"Resolve the remaining closeout blockers: {blockers or 'unknown'}."


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
