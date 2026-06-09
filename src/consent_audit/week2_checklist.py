"""Week 2 capture-day operator checklist."""

from __future__ import annotations

import os
from pathlib import Path


def export_week2_capture_checklist(
    *,
    out_md: Path,
    title: str,
    week_of: str,
    cohort: str,
    expected_target_count: int,
    targets_csv: Path,
    consent_table_csv: Path,
    preflight_check: Path,
    cycle_report: Path,
    refresh_report: Path,
    sanity_check: Path,
    checkin_index: Path,
    advisor_brief: Path,
) -> str:
    """Write the capture-day checklist for the weekly research cycle."""

    preflight_status = _extract_status(preflight_check)
    sanity_status = _extract_status(sanity_check)
    cycle_mode = _extract_value(cycle_report, "- Cycle mode:", default="not_run")
    capture_status = _extract_value(cycle_report, "- Capture status:", default="not_run")
    capture_attempts = _extract_value(cycle_report, "- Capture attempts:", default="not_run")

    text = _render_checklist(
        out_md=out_md,
        title=title,
        week_of=week_of,
        cohort=cohort,
        expected_target_count=expected_target_count,
        targets_csv=targets_csv,
        consent_table_csv=consent_table_csv,
        preflight_check=preflight_check,
        cycle_report=cycle_report,
        refresh_report=refresh_report,
        sanity_check=sanity_check,
        checkin_index=checkin_index,
        advisor_brief=advisor_brief,
        preflight_status=preflight_status,
        sanity_status=sanity_status,
        cycle_mode=cycle_mode,
        capture_status=capture_status,
        capture_attempts=capture_attempts,
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    return text


def _render_checklist(
    *,
    out_md: Path,
    title: str,
    week_of: str,
    cohort: str,
    expected_target_count: int,
    targets_csv: Path,
    consent_table_csv: Path,
    preflight_check: Path,
    cycle_report: Path,
    refresh_report: Path,
    sanity_check: Path,
    checkin_index: Path,
    advisor_brief: Path,
    preflight_status: str,
    sanity_status: str,
    cycle_mode: str,
    capture_status: str,
    capture_attempts: str,
) -> str:
    return (
        f"# {title}\n\n"
        "Use this checklist when running the weekly capture cycle.\n\n"
        "## Current State\n\n"
        f"- Week of: {week_of}\n"
        f"- Cohort: `{cohort}`\n"
        f"- Expected targets: {expected_target_count}\n"
        f"- Preflight status: `{preflight_status}`\n"
        f"- Sanity status: `{sanity_status}`\n"
        f"- Last cycle mode: `{cycle_mode}`\n"
        f"- Last capture status: `{capture_status}`\n"
        f"- Last capture attempts: {capture_attempts}\n\n"
        "## Evidence Links\n\n"
        f"- [Week 2 targets]({_relative_link(out_md, targets_csv)})\n"
        f"- [Consent table]({_relative_link(out_md, consent_table_csv)})\n"
        f"- [Preflight check]({_relative_link(out_md, preflight_check)})\n"
        f"- [Cycle report]({_relative_link(out_md, cycle_report)})\n"
        f"- [Refresh report]({_relative_link(out_md, refresh_report)})\n"
        f"- [Sanity check]({_relative_link(out_md, sanity_check)})\n"
        f"- [Check-in index]({_relative_link(out_md, checkin_index)})\n"
        f"- [Advisor update]({_relative_link(out_md, advisor_brief)})\n\n"
        "## Run Checklist\n\n"
        "- [ ] Open the check-in index and confirm the target list and cohort.\n"
        "- [ ] Run `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-preflight-check`.\n"
        "- [ ] Confirm preflight status is `ready_for_capture` or record a force rationale.\n"
        "- [ ] Run `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-cycle --dry-run`.\n"
        "- [ ] Read the cycle report `Next Action` before live capture.\n"
        "- [ ] Run `AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m "
        "consent_audit.cli week2-cycle`.\n"
        "- [ ] Run `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-refresh-outputs` if the live cycle did not reach refresh.\n"
        "- [ ] Confirm every target has screenshot, DOM, hash, and report evidence.\n"
        "- [ ] Confirm Week 2 sanity status is `ready` before treating capture complete.\n"
    )


def _extract_status(path: Path) -> str:
    return _extract_value(path, "- Overall status:", default="unknown")


def _extract_value(path: Path, prefix: str, *, default: str) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            value = stripped.split(":", 1)[1].strip().strip("`")
            return value or default
    return default


def _relative_link(out_md: Path, target: Path) -> str:
    relative = os.path.relpath(target, start=out_md.parent)
    return relative.replace(os.sep, "/")
