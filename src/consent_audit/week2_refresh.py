"""Week 2 post-capture artifact refresh orchestration."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from consent_audit.advisor_brief import export_weekly_advisor_brief
from consent_audit.checkin_index import export_checkin_index
from consent_audit.paper_claims import export_ssrp_claim_register
from consent_audit.paper_figures import export_ssrp_figure_plan
from consent_audit.paper_skeleton import export_ssrp_paper_skeleton
from consent_audit.paper_tables import export_ssrp_results_tables
from consent_audit.paper_writing_pack import export_ssrp_writing_pack
from consent_audit.poster_plan import export_ssrp_poster_plan
from consent_audit.research_package import export_research_package
from consent_audit.week2_checklist import export_week2_capture_checklist
from consent_audit.week2_preflight import export_week2_preflight_check
from consent_audit.week2_sanity import export_week2_sanity_check


def refresh_week2_outputs(
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
    expected_target_count: int,
    limit: int,
    results_tables_md: Path | None = None,
    paper_skeleton_md: Path | None = None,
    figure_plan_md: Path | None = None,
    writing_pack_md: Path | None = None,
    claim_register_md: Path | None = None,
    poster_plan_md: Path | None = None,
) -> dict[str, Any]:
    """Refresh all advisor-facing Week 2 artifacts after capture/export changes."""

    manifest = export_research_package(research_package_dir, limit=limit)
    manifest_json = research_package_dir / "research_manifest.json"
    audit_summary_csv = _package_file(
        research_package_dir,
        manifest,
        key="audit_report_summary",
        default="audit_report_summary.csv",
    )
    longitudinal_summary_csv = _package_file(
        research_package_dir,
        manifest,
        key="longitudinal_summary",
        default="longitudinal_summary.csv",
    )
    effective_results_tables_md = results_tables_md or (
        refresh_report_md.parent / f"ssrp_results_tables_{week_of}.md"
    )
    effective_paper_skeleton_md = paper_skeleton_md or (
        refresh_report_md.parent / f"ssrp_paper_skeleton_{week_of}.md"
    )
    effective_figure_plan_md = figure_plan_md or (
        refresh_report_md.parent / f"ssrp_figure_plan_{week_of}.md"
    )
    effective_writing_pack_md = writing_pack_md or (
        refresh_report_md.parent / f"ssrp_writing_pack_{week_of}.md"
    )
    effective_claim_register_md = claim_register_md or (
        refresh_report_md.parent / f"ssrp_claim_register_{week_of}.md"
    )
    effective_poster_plan_md = poster_plan_md or (
        refresh_report_md.parent / f"ssrp_poster_plan_{week_of}.md"
    )

    export_weekly_advisor_brief(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        manifest_json=manifest_json,
        out_md=advisor_brief_md,
        title=f"Week 2 Advisor Update, {week_of}",
    )
    sanity_text = export_week2_sanity_check(
        targets_csv=targets_csv,
        consent_table_csv=consent_table_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        out_md=sanity_check_md,
        cohort=cohort,
        week_of=week_of,
        title=f"Week 2 Capture Sanity Check, {week_of}",
    )
    export_ssrp_results_tables(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        out_md=effective_results_tables_md,
        title=f"SSRP 2026 Results Tables, {week_of}",
        week_label="Week 2",
    )
    export_ssrp_paper_skeleton(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        manifest_json=manifest_json,
        out_md=effective_paper_skeleton_md,
        title=f"SSRP 2026 Paper Skeleton, {week_of}",
        week_label="Week 2",
    )
    export_ssrp_figure_plan(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        results_tables_md=effective_results_tables_md,
        paper_skeleton_md=effective_paper_skeleton_md,
        cycle_report_md=cycle_report_md,
        out_md=effective_figure_plan_md,
        title=f"SSRP 2026 Figure Plan, {week_of}",
        week_label="Week 2",
    )
    export_ssrp_writing_pack(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        results_tables_md=effective_results_tables_md,
        paper_skeleton_md=effective_paper_skeleton_md,
        figure_plan_md=effective_figure_plan_md,
        cycle_report_md=cycle_report_md,
        out_md=effective_writing_pack_md,
        title=f"SSRP 2026 Writing Pack, {week_of}",
        week_label="Week 2",
    )
    export_ssrp_claim_register(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        results_tables_md=effective_results_tables_md,
        paper_skeleton_md=effective_paper_skeleton_md,
        figure_plan_md=effective_figure_plan_md,
        writing_pack_md=effective_writing_pack_md,
        cycle_report_md=cycle_report_md,
        out_md=effective_claim_register_md,
        title=f"SSRP 2026 Claim Register, {week_of}",
        week_label="Week 2",
    )
    export_ssrp_poster_plan(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        results_tables_md=effective_results_tables_md,
        paper_skeleton_md=effective_paper_skeleton_md,
        figure_plan_md=effective_figure_plan_md,
        writing_pack_md=effective_writing_pack_md,
        claim_register_md=effective_claim_register_md,
        cycle_report_md=cycle_report_md,
        out_md=effective_poster_plan_md,
        title=f"SSRP 2026 Poster Plan, {week_of}",
        week_label="Week 2",
    )
    preflight_text = export_week2_preflight_check(
        targets_csv=targets_csv,
        sanity_check_md=sanity_check_md,
        advisor_brief_md=advisor_brief_md,
        checkin_index_md=checkin_index_md,
        runbook_md=runbook_md,
        research_manifest_json=manifest_json,
        cmp_confirmation_csv=cmp_confirmation_csv,
        cmp_packet_html=cmp_packet_html,
        out_md=preflight_check_md,
        title=f"Week 2 Preflight Check, {week_of}",
        expected_target_count=expected_target_count,
    )
    export_week2_capture_checklist(
        out_md=capture_checklist_md,
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
    export_checkin_index(
        out_md=checkin_index_md,
        title=f"Week 2 Advisor Check-in Index, {week_of}",
        advisor_brief=advisor_brief_md,
        sanity_check=sanity_check_md,
        capture_checklist=capture_checklist_md,
        cycle_report=cycle_report_md,
        runbook=runbook_md,
        sample_plan=sample_plan_md,
        cmp_confirmation_sheet=cmp_confirmation_csv,
        cmp_packet=cmp_packet_html,
        research_package_dir=research_package_dir,
        research_manifest=manifest_json,
    )

    summary: dict[str, Any] = {
        "audit_report_count": manifest.get("audit_report_count", 0),
        "weekly_summary_count": manifest.get("weekly_summary_count", 0),
        "sanity_status": _extract_status(sanity_text),
        "preflight_status": _extract_status(preflight_text),
        "research_package_dir": str(research_package_dir),
        "advisor_brief_md": str(advisor_brief_md),
        "sanity_check_md": str(sanity_check_md),
        "checkin_index_md": str(checkin_index_md),
        "capture_checklist_md": str(capture_checklist_md),
        "results_tables_md": str(effective_results_tables_md),
        "paper_skeleton_md": str(effective_paper_skeleton_md),
        "figure_plan_md": str(effective_figure_plan_md),
        "writing_pack_md": str(effective_writing_pack_md),
        "claim_register_md": str(effective_claim_register_md),
        "poster_plan_md": str(effective_poster_plan_md),
        "preflight_check_md": str(preflight_check_md),
        "cycle_report_md": str(cycle_report_md),
    }
    _write_refresh_report(
        out_md=refresh_report_md,
        week_of=week_of,
        summary=summary,
        research_package_dir=research_package_dir,
        research_manifest_json=manifest_json,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        advisor_brief_md=advisor_brief_md,
        sanity_check_md=sanity_check_md,
        results_tables_md=effective_results_tables_md,
        paper_skeleton_md=effective_paper_skeleton_md,
        figure_plan_md=effective_figure_plan_md,
        writing_pack_md=effective_writing_pack_md,
        claim_register_md=effective_claim_register_md,
        poster_plan_md=effective_poster_plan_md,
        capture_checklist_md=capture_checklist_md,
        checkin_index_md=checkin_index_md,
        preflight_check_md=preflight_check_md,
    )
    return summary


def _write_refresh_report(
    *,
    out_md: Path,
    week_of: str,
    summary: dict[str, Any],
    research_package_dir: Path,
    research_manifest_json: Path,
    audit_summary_csv: Path,
    longitudinal_summary_csv: Path,
    advisor_brief_md: Path,
    sanity_check_md: Path,
    results_tables_md: Path,
    paper_skeleton_md: Path,
    figure_plan_md: Path,
    writing_pack_md: Path,
    claim_register_md: Path,
    poster_plan_md: Path,
    capture_checklist_md: Path,
    checkin_index_md: Path,
    preflight_check_md: Path,
) -> None:
    text = (
        f"# Week 2 Refresh Report, {week_of}\n\n"
        "## Summary\n\n"
        f"- Audit reports in package: {summary['audit_report_count']}\n"
        f"- Longitudinal summaries in package: {summary['weekly_summary_count']}\n"
        f"- Sanity status: `{summary['sanity_status']}`\n"
        f"- Preflight status: `{summary['preflight_status']}`\n"
        "- Advisor and sanity outputs read the freshly exported research-package CSVs.\n\n"
        "## Refreshed Outputs\n\n"
        f"- [Research package]({_relative_link(out_md, research_package_dir)})\n"
        f"- [Research manifest]({_relative_link(out_md, research_manifest_json)})\n"
        f"- [Audit report summary]({_relative_link(out_md, audit_summary_csv)})\n"
        f"- [Longitudinal summary]({_relative_link(out_md, longitudinal_summary_csv)})\n"
        f"- [Advisor update]({_relative_link(out_md, advisor_brief_md)})\n"
        f"- [Week 2 sanity check]({_relative_link(out_md, sanity_check_md)})\n"
        f"- [SSRP results tables]({_relative_link(out_md, results_tables_md)})\n"
        f"- [SSRP paper skeleton]({_relative_link(out_md, paper_skeleton_md)})\n"
        f"- [SSRP figure plan]({_relative_link(out_md, figure_plan_md)})\n"
        f"- [SSRP writing pack]({_relative_link(out_md, writing_pack_md)})\n"
        f"- [SSRP claim register]({_relative_link(out_md, claim_register_md)})\n"
        f"- [SSRP poster plan]({_relative_link(out_md, poster_plan_md)})\n"
        f"- [Capture checklist]({_relative_link(out_md, capture_checklist_md)})\n"
        f"- [Check-in index]({_relative_link(out_md, checkin_index_md)})\n"
        f"- [Week 2 preflight]({_relative_link(out_md, preflight_check_md)})\n"
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")


def _package_file(
    research_package_dir: Path,
    manifest: dict[str, Any],
    *,
    key: str,
    default: str,
) -> Path:
    files = manifest.get("files", {})
    if isinstance(files, dict):
        return research_package_dir / str(files.get(key, default))
    return research_package_dir / default


def _extract_status(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- Overall status:"):
            return stripped.split(":", 1)[1].strip().strip("`") or "unknown"
    return "unknown"


def _relative_link(out_md: Path, target: Path) -> str:
    relative = os.path.relpath(target, start=out_md.parent)
    return relative.replace(os.sep, "/")
