"""Week 2 full capture cycle orchestration."""

from __future__ import annotations

import os
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from consent_audit.pipeline import run_weekly_audit
from consent_audit.week2_checklist import export_week2_capture_checklist
from consent_audit.week2_preflight import export_week2_preflight_check
from consent_audit.week2_refresh import refresh_week2_outputs


async def run_week2_cycle(
    *,
    targets_csv: Path,
    consent_table_csv: Path,
    cmp_confirmation_csv: Path,
    cmp_packet_html: Path,
    runbook_md: Path,
    sample_plan_md: Path,
    research_package_dir: Path,
    advisor_brief_md: Path,
    sanity_check_md: Path,
    checkin_index_md: Path,
    capture_checklist_md: Path,
    preflight_check_md: Path,
    refresh_report_md: Path,
    cycle_report_md: Path,
    cohort: str,
    week_of: str,
    run_date: str | None = None,
    expected_target_count: int,
    limit: int,
    force: bool,
    allow_early: bool = False,
    dry_run: bool = False,
    max_capture_failures: int = 2,
) -> dict[str, Any]:
    """Run preflight, weekly capture, and post-capture refresh for Week 2."""

    effective_run_date = run_date or date.today().isoformat()
    report_inputs = _report_inputs(
        targets_csv=targets_csv,
        consent_table_csv=consent_table_csv,
        cohort=cohort,
        run_date=effective_run_date,
        expected_target_count=expected_target_count,
        limit=limit,
        force=force,
        allow_early=allow_early,
        dry_run=dry_run,
    )
    preflight_text = export_week2_preflight_check(
        targets_csv=targets_csv,
        sanity_check_md=sanity_check_md,
        advisor_brief_md=advisor_brief_md,
        checkin_index_md=checkin_index_md,
        runbook_md=runbook_md,
        research_manifest_json=research_package_dir / "research_manifest.json",
        cmp_confirmation_csv=cmp_confirmation_csv,
        cmp_packet_html=cmp_packet_html,
        out_md=preflight_check_md,
        title=f"Week 2 Preflight Check, {week_of}",
        expected_target_count=expected_target_count,
    )
    preflight_status = _extract_status(preflight_text)
    if dry_run:
        capture_status = "dry_run"
        if preflight_status != "ready_for_capture" and not force:
            capture_status = "dry_run_needs_attention"
        dry_run_summary = {
            "preflight_status": preflight_status,
            "capture_status": capture_status,
            "capture_target_count": expected_target_count,
            "capture_attempted_count": 0,
            "capture_succeeded_count": 0,
            "capture_failed_count": 0,
            "audit_report_count": 0,
            "weekly_summary_count": 0,
            "sanity_status": "not_run",
            "post_refresh_preflight_status": "not_run",
        }
        _write_cycle_report(
            out_md=cycle_report_md,
            week_of=week_of,
            summary=dry_run_summary,
            report_inputs=report_inputs,
            refresh_report_md=refresh_report_md,
        )
        _sync_capture_checklist(
            out_md=capture_checklist_md,
            week_of=week_of,
            cohort=cohort,
            expected_target_count=expected_target_count,
            targets_csv=targets_csv,
            consent_table_csv=consent_table_csv,
            preflight_check_md=preflight_check_md,
            cycle_report_md=cycle_report_md,
            refresh_report_md=refresh_report_md,
            sanity_check_md=sanity_check_md,
            checkin_index_md=checkin_index_md,
            advisor_brief_md=advisor_brief_md,
        )
        return dry_run_summary

    if preflight_status != "ready_for_capture" and not force:
        aborted_summary = {
            "preflight_status": preflight_status,
            "capture_status": "aborted",
            "capture_target_count": expected_target_count,
            "capture_attempted_count": 0,
            "capture_succeeded_count": 0,
            "capture_failed_count": 0,
            "audit_report_count": 0,
            "weekly_summary_count": 0,
            "sanity_status": "not_run",
            "post_refresh_preflight_status": "not_run",
        }
        _write_cycle_report(
            out_md=cycle_report_md,
            week_of=week_of,
            summary=aborted_summary,
            report_inputs=report_inputs,
            refresh_report_md=refresh_report_md,
        )
        _sync_capture_checklist(
            out_md=capture_checklist_md,
            week_of=week_of,
            cohort=cohort,
            expected_target_count=expected_target_count,
            targets_csv=targets_csv,
            consent_table_csv=consent_table_csv,
            preflight_check_md=preflight_check_md,
            cycle_report_md=cycle_report_md,
            refresh_report_md=refresh_report_md,
            sanity_check_md=sanity_check_md,
            checkin_index_md=checkin_index_md,
            advisor_brief_md=advisor_brief_md,
        )
        raise RuntimeError(
            f"Week 2 preflight status {preflight_status}; "
            "rerun with force=True only after recording the risk."
        )

    if not force and not allow_early and effective_run_date < week_of:
        scheduled_summary = {
            "preflight_status": preflight_status,
            "capture_status": "scheduled_date_not_reached",
            "capture_target_count": expected_target_count,
            "capture_attempted_count": 0,
            "capture_succeeded_count": 0,
            "capture_failed_count": 0,
            "audit_report_count": 0,
            "weekly_summary_count": 0,
            "sanity_status": "not_run",
            "post_refresh_preflight_status": "not_run",
            "scheduled_week_of": week_of,
        }
        _write_cycle_report(
            out_md=cycle_report_md,
            week_of=week_of,
            summary=scheduled_summary,
            report_inputs=report_inputs,
            refresh_report_md=refresh_report_md,
        )
        _sync_capture_checklist(
            out_md=capture_checklist_md,
            week_of=week_of,
            cohort=cohort,
            expected_target_count=expected_target_count,
            targets_csv=targets_csv,
            consent_table_csv=consent_table_csv,
            preflight_check_md=preflight_check_md,
            cycle_report_md=cycle_report_md,
            refresh_report_md=refresh_report_md,
            sanity_check_md=sanity_check_md,
            checkin_index_md=checkin_index_md,
            advisor_brief_md=advisor_brief_md,
        )
        raise RuntimeError(
            f"Week 2 run date {effective_run_date} is before scheduled week {week_of}; "
            "rerun with allow_early=True only after recording the timing risk."
        )

    capture_summary = await run_weekly_audit(
        targets_csv,
        consent_table_path=consent_table_csv,
        cohort=cohort,
        limit=limit,
        summary_week_of=_summary_week_datetime(week_of),
    )
    capture_status = _capture_status(
        failed_count=capture_summary.failed_count,
        budget_exceeded=capture_summary.budget_exceeded,
        max_capture_failures=max_capture_failures,
    )
    refresh_summary = refresh_week2_outputs(
        targets_csv=targets_csv,
        consent_table_csv=consent_table_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        cmp_packet_html=cmp_packet_html,
        runbook_md=runbook_md,
        sample_plan_md=sample_plan_md,
        research_package_dir=research_package_dir,
        advisor_brief_md=advisor_brief_md,
        sanity_check_md=sanity_check_md,
        checkin_index_md=checkin_index_md,
        capture_checklist_md=capture_checklist_md,
        preflight_check_md=preflight_check_md,
        refresh_report_md=refresh_report_md,
        cycle_report_md=cycle_report_md,
        cohort=cohort,
        week_of=week_of,
        expected_target_count=expected_target_count,
        limit=limit,
    )
    summary: dict[str, Any] = {
        "preflight_status": preflight_status,
        "capture_status": capture_status,
        "capture_target_count": capture_summary.target_count,
        "capture_attempted_count": capture_summary.attempted_count,
        "capture_succeeded_count": capture_summary.succeeded_count,
        "capture_failed_count": capture_summary.failed_count,
        "audit_report_count": refresh_summary.get("audit_report_count", 0),
        "weekly_summary_count": refresh_summary.get("weekly_summary_count", 0),
        "sanity_status": refresh_summary.get("sanity_status", "unknown"),
        "post_refresh_preflight_status": refresh_summary.get(
            "preflight_status",
            "unknown",
        ),
    }
    if capture_summary.failures:
        summary["capture_failures"] = [
            f"{failure.url}: {failure.error}" for failure in capture_summary.failures
        ]
    _write_cycle_report(
        out_md=cycle_report_md,
        week_of=week_of,
        summary=summary,
        report_inputs=report_inputs,
        refresh_report_md=refresh_report_md,
    )
    _sync_capture_checklist(
        out_md=capture_checklist_md,
        week_of=week_of,
        cohort=cohort,
        expected_target_count=expected_target_count,
        targets_csv=targets_csv,
        consent_table_csv=consent_table_csv,
        preflight_check_md=preflight_check_md,
        cycle_report_md=cycle_report_md,
        refresh_report_md=refresh_report_md,
        sanity_check_md=sanity_check_md,
        checkin_index_md=checkin_index_md,
        advisor_brief_md=advisor_brief_md,
    )
    return summary


def _sync_capture_checklist(
    *,
    out_md: Path,
    week_of: str,
    cohort: str,
    expected_target_count: int,
    targets_csv: Path,
    consent_table_csv: Path,
    preflight_check_md: Path,
    cycle_report_md: Path,
    refresh_report_md: Path,
    sanity_check_md: Path,
    checkin_index_md: Path,
    advisor_brief_md: Path,
) -> None:
    export_week2_capture_checklist(
        out_md=out_md,
        title=f"Week 2 Capture-Day Checklist, {week_of}",
        week_of=week_of,
        cohort=cohort,
        expected_target_count=expected_target_count,
        targets_csv=targets_csv,
        consent_table_csv=consent_table_csv,
        preflight_check=preflight_check_md,
        cycle_report=cycle_report_md,
        refresh_report=refresh_report_md,
        sanity_check=sanity_check_md,
        checkin_index=checkin_index_md,
        advisor_brief=advisor_brief_md,
    )


def _write_cycle_report(
    *,
    out_md: Path,
    week_of: str,
    summary: dict[str, Any],
    report_inputs: dict[str, str],
    refresh_report_md: Path,
) -> None:
    text = (
        f"# Week 2 Cycle Report, {week_of}\n\n"
        "## Summary\n\n"
        f"- Cycle mode: {_cycle_mode(summary)}\n"
        f"- Preflight status before capture: `{summary['preflight_status']}`\n"
        f"- Capture status: {summary['capture_status']}\n"
        f"- Capture attempts: {summary.get('capture_attempted_count', 0)}/"
        f"{summary.get('capture_target_count', 0)}\n"
        f"- Capture successes: {summary.get('capture_succeeded_count', 0)}/"
        f"{summary.get('capture_target_count', 0)}\n"
        f"- Capture failures: {summary.get('capture_failed_count', 0)}\n"
        f"- Audit reports after refresh: {summary['audit_report_count']}\n"
        f"- Longitudinal summaries after refresh: {summary['weekly_summary_count']}\n"
        f"- Sanity status after refresh: `{summary['sanity_status']}`\n"
        "- Preflight status after refresh: "
        f"`{summary['post_refresh_preflight_status']}`\n"
        f"- [Refresh report]({_relative_link(out_md, refresh_report_md)})\n"
        "\n## Inputs\n\n"
        f"- Target list: `{report_inputs['targets_csv']}`\n"
        f"- Consent table: `{report_inputs['consent_table_csv']}`\n"
        f"- Cohort: `{report_inputs['cohort']}`\n"
        f"- Expected targets: {report_inputs['expected_target_count']}\n"
        f"- Capture limit: {report_inputs['limit']}\n"
        f"- Force used: {report_inputs['force']}\n"
        f"- Run date: {report_inputs['run_date']}\n"
        f"- Allow early: {report_inputs['allow_early']}\n"
        f"- Dry run: {report_inputs['dry_run']}\n"
        "\n## Next Action\n\n"
        f"- {_next_action(summary)}\n"
    )
    failures = summary.get("capture_failures", [])
    if failures:
        text += "\n## Capture Failures\n\n"
        for failure in failures:
            text += f"- {failure}\n"
    if str(summary["capture_status"]).startswith("dry_run"):
        text += "\n## Dry Run\n\n- Browser capture and refresh were not run.\n"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")


def _capture_status(
    *,
    failed_count: int,
    budget_exceeded: bool,
    max_capture_failures: int,
) -> str:
    if budget_exceeded:
        return "budget_exceeded"
    if failed_count >= max_capture_failures:
        return "needs_attention"
    if failed_count > 0:
        return "completed_with_warnings"
    return "completed"


def _summary_week_datetime(week_of: str) -> datetime:
    return datetime.fromisoformat(f"{week_of}T00:00:00+00:00").astimezone(UTC)


def _cycle_mode(summary: dict[str, Any]) -> str:
    capture_status = str(summary["capture_status"])
    if capture_status == "aborted":
        return "preflight_blocked"
    if capture_status == "scheduled_date_not_reached":
        return "scheduled_date_blocked"
    if capture_status.startswith("dry_run"):
        return "dry_run"
    return "live_capture"


def _report_inputs(
    *,
    targets_csv: Path,
    consent_table_csv: Path,
    cohort: str,
    run_date: str,
    expected_target_count: int,
    limit: int,
    force: bool,
    allow_early: bool,
    dry_run: bool,
) -> dict[str, str]:
    return {
        "targets_csv": str(targets_csv),
        "consent_table_csv": str(consent_table_csv),
        "cohort": cohort,
        "run_date": run_date,
        "expected_target_count": str(expected_target_count),
        "limit": str(limit),
        "force": _format_bool(force),
        "allow_early": _format_bool(allow_early),
        "dry_run": _format_bool(dry_run),
    }


def _format_bool(value: bool) -> str:
    return "true" if value else "false"


def _next_action(summary: dict[str, Any]) -> str:
    capture_status = str(summary["capture_status"])
    if capture_status == "dry_run":
        return "Start live capture with `week2-cycle` when ready."
    if capture_status == "dry_run_needs_attention":
        return (
            "Do not start live capture until preflight is `ready_for_capture` "
            "or a force rationale is recorded."
        )
    if capture_status == "aborted":
        return "Resolve preflight warnings before rerunning Week 2 capture."
    if capture_status == "scheduled_date_not_reached":
        scheduled_week = str(summary.get("scheduled_week_of", "the scheduled date"))
        return (
            f"Wait until {scheduled_week} before live capture, or rerun with "
            "`--allow-early` after recording the timing risk."
        )
    if capture_status == "needs_attention":
        return "Review capture failures before treating the Week 2 run as complete."
    if capture_status == "budget_exceeded":
        return "Review the budget cap before rerunning or extending capture."
    if capture_status == "completed_with_warnings":
        return "Review the single-site warning, then rerun Week 2 refresh outputs if needed."
    if capture_status == "completed":
        return "Review the refreshed sanity check and advisor index."
    return "Review the cycle report before continuing."


def _extract_status(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- Overall status:"):
            return stripped.split(":", 1)[1].strip().strip("`") or "unknown"
    return "unknown"


def _relative_link(out_md: Path, target: Path) -> str:
    relative = os.path.relpath(target, start=out_md.parent)
    return relative.replace(os.sep, "/")
