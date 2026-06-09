"""Command-line interface. `uv run consent-audit --help` once installed."""

import asyncio
from pathlib import Path
from typing import Annotated

import typer

from consent_audit.access_probe import format_access_probe_summary, run_access_probe_from_csv
from consent_audit.access_probe_summary import render_access_probe_summary
from consent_audit.advisor_brief import export_weekly_advisor_brief
from consent_audit.audit_export import export_audit_reports_to_csv
from consent_audit.checkin_index import export_checkin_index
from consent_audit.cmp_review import (
    apply_cmp_review_confirmations_to_worksheet,
    build_cmp_review_confirmation_sheet,
    build_cmp_review_decision_draft,
    build_cmp_review_queue,
    build_cmp_review_suggestions,
    build_cmp_review_worksheet,
    export_cmp_review_confirmation_sheet_to_csv,
    export_cmp_review_decision_draft_to_csv,
    export_cmp_review_packet,
    export_cmp_review_queue_to_csv,
    export_cmp_review_rerun_targets,
    export_cmp_review_suggestions_to_csv,
    export_cmp_review_worksheet_to_csv,
    summarize_cmp_review_confirmation_sheet,
    summarize_cmp_review_decision_draft,
    summarize_cmp_review_queue,
    summarize_cmp_review_suggestions,
    summarize_cmp_review_worksheet,
)
from consent_audit.longitudinal_export import export_weekly_summaries_to_csv
from consent_audit.paper_claims import export_ssrp_claim_register
from consent_audit.paper_figures import export_ssrp_figure_plan
from consent_audit.paper_skeleton import export_ssrp_paper_skeleton
from consent_audit.paper_tables import export_ssrp_results_tables
from consent_audit.paper_writing_pack import export_ssrp_writing_pack
from consent_audit.pipeline import (
    format_weekly_run_summary,
    run_single_site_audit,
    run_weekly_audit,
)
from consent_audit.poster_plan import export_ssrp_poster_plan
from consent_audit.replacement_review import (
    build_replacement_review,
    export_expanded_weekly_targets,
    export_replacement_review_to_csv,
    summarize_replacement_review,
)
from consent_audit.research_package import export_research_package as export_research_package_data
from consent_audit.research_status import render_research_status
from consent_audit.sample_lock import (
    build_sample_lock_plan,
    export_sample_lock_plan_to_csv,
    export_sample_lock_queues,
    export_weekly_targets_from_queues,
    summarize_sample_lock_plan,
)
from consent_audit.sample_readiness import (
    build_sample_readiness,
    export_sample_readiness_to_csv,
    summarize_readiness,
)
from consent_audit.site_list import validate_site_list
from consent_audit.storage import list_reports, list_weekly_summaries
from consent_audit.week2_checklist import export_week2_capture_checklist
from consent_audit.week2_cycle import run_week2_cycle
from consent_audit.week2_plan import export_week2_capture_targets
from consent_audit.week2_preflight import export_week2_preflight_check
from consent_audit.week2_refresh import refresh_week2_outputs
from consent_audit.week2_sanity import export_week2_sanity_check

app = typer.Typer(help="Dynamic consent interface audit system.")


@app.command()
def audit(
    url: str,
    save: bool = True,
    consent_table_path: Path | None = Path("data/consent_table.csv"),
    cohort: str = "",
) -> None:
    """Audit a single URL and write a Markdown report."""
    report = asyncio.run(
        run_single_site_audit(
            url,
            save=save,
            consent_table_path=consent_table_path,
            cohort=cohort,
        )
    )
    typer.echo(report.report_markdown)


@app.command("access-probe")
def access_probe(
    sites_csv: Path = Path("data/sites.csv"),
    out_csv: Path = Path("data/access_probe_v0.csv"),
    concurrency: int = 4,
    timeout_ms: int = 30_000,
) -> None:
    """Run the Week 0 access feasibility probe against a validated site CSV."""
    try:
        summary = asyncio.run(
            run_access_probe_from_csv(
                sites_csv,
                out_csv,
                concurrency=concurrency,
                timeout_ms=timeout_ms,
            )
        )
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc

    typer.echo(format_access_probe_summary(summary))


@app.command("access-probe-summary")
def access_probe_summary(
    csv_path: Path = Path("data/access_probe_v0.csv"),
) -> None:
    """Summarize access-probe CSV output for mentor/advisor review."""
    try:
        summary = render_access_probe_summary(csv_path)
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    typer.echo(summary)


@app.command("research-status")
def research_status(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    research_manifest_json: Path = Path("data/research_package/research_manifest.json"),
    cmp_confirmation_csv: Path = Path(
        "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
    ),
    preflight_md: Path = Path("docs/research/week2_preflight_check_2026-06-06.md"),
    sanity_md: Path = Path("docs/research/week2_sanity_check_2026-06-06.md"),
    cycle_report_md: Path = Path("docs/research/week2_cycle_report_2026-06-06.md"),
    results_tables_md: Path = Path("docs/research/ssrp_results_tables_2026-06-06.md"),
    paper_skeleton_md: Path = Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
    figure_plan_md: Path = Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
    writing_pack_md: Path = Path("docs/research/ssrp_writing_pack_2026-06-06.md"),
    claim_register_md: Path = Path("docs/research/ssrp_claim_register_2026-06-06.md"),
    poster_plan_md: Path = Path("docs/research/ssrp_poster_plan_2026-06-06.md"),
) -> None:
    """Print a compact current-state dashboard for the SSRP workflow."""
    typer.echo(
        render_research_status(
            targets_csv=targets_csv,
            research_manifest_json=research_manifest_json,
            cmp_confirmation_csv=cmp_confirmation_csv,
            preflight_md=preflight_md,
            sanity_md=sanity_md,
            cycle_report_md=cycle_report_md,
            results_tables_md=results_tables_md,
            paper_skeleton_md=paper_skeleton_md,
            figure_plan_md=figure_plan_md,
            writing_pack_md=writing_pack_md,
            claim_register_md=claim_register_md,
            poster_plan_md=poster_plan_md,
        )
    )


@app.command("ssrp-paper-skeleton")
def ssrp_paper_skeleton(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    audit_summary_csv: Path = Path("data/research_package/audit_report_summary.csv"),
    longitudinal_summary_csv: Path = Path("data/research_package/longitudinal_summary.csv"),
    manifest_json: Path = Path("data/research_package/research_manifest.json"),
    out_md: Path = Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
    title: str = "SSRP 2026 Paper Skeleton, 2026-06-06",
    week_label: str = "Week 2",
) -> None:
    """Export a paper-draft skeleton grounded in the current research package."""
    export_ssrp_paper_skeleton(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        manifest_json=manifest_json,
        out_md=out_md,
        title=title,
        week_label=week_label,
    )
    typer.echo(f"Wrote SSRP paper skeleton to {out_md}")


@app.command("ssrp-results-tables")
def ssrp_results_tables(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    audit_summary_csv: Path = Path("data/research_package/audit_report_summary.csv"),
    longitudinal_summary_csv: Path = Path("data/research_package/longitudinal_summary.csv"),
    out_md: Path = Path("docs/research/ssrp_results_tables_2026-06-06.md"),
    title: str = "SSRP 2026 Results Tables, 2026-06-06",
    week_label: str = "Week 2",
) -> None:
    """Export paper-ready RQ1/RQ2 Markdown results tables."""
    export_ssrp_results_tables(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        out_md=out_md,
        title=title,
        week_label=week_label,
    )
    typer.echo(f"Wrote SSRP results tables to {out_md}")


@app.command("ssrp-figure-plan")
def ssrp_figure_plan(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    audit_summary_csv: Path = Path("data/research_package/audit_report_summary.csv"),
    longitudinal_summary_csv: Path = Path("data/research_package/longitudinal_summary.csv"),
    results_tables_md: Path = Path("docs/research/ssrp_results_tables_2026-06-06.md"),
    paper_skeleton_md: Path = Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
    cycle_report_md: Path = Path("docs/research/week2_cycle_report_2026-06-06.md"),
    out_md: Path = Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
    title: str = "SSRP 2026 Figure Plan, 2026-06-06",
    week_label: str = "Week 2",
) -> None:
    """Export a paper/poster figure queue from current evidence."""
    export_ssrp_figure_plan(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        cycle_report_md=cycle_report_md,
        out_md=out_md,
        title=title,
        week_label=week_label,
    )
    typer.echo(f"Wrote SSRP figure plan to {out_md}")


@app.command("ssrp-writing-pack")
def ssrp_writing_pack(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    audit_summary_csv: Path = Path("data/research_package/audit_report_summary.csv"),
    longitudinal_summary_csv: Path = Path("data/research_package/longitudinal_summary.csv"),
    cmp_confirmation_csv: Path = Path(
        "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
    ),
    results_tables_md: Path = Path("docs/research/ssrp_results_tables_2026-06-06.md"),
    paper_skeleton_md: Path = Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
    figure_plan_md: Path = Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
    cycle_report_md: Path = Path("docs/research/week2_cycle_report_2026-06-06.md"),
    out_md: Path = Path("docs/research/ssrp_writing_pack_2026-06-06.md"),
    title: str = "SSRP 2026 Writing Pack, 2026-06-06",
    week_label: str = "Week 2",
) -> None:
    """Export methods/results/discussion drafting notes from current evidence."""
    export_ssrp_writing_pack(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        figure_plan_md=figure_plan_md,
        cycle_report_md=cycle_report_md,
        out_md=out_md,
        title=title,
        week_label=week_label,
    )
    typer.echo(f"Wrote SSRP writing pack to {out_md}")


@app.command("ssrp-claim-register")
def ssrp_claim_register(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    audit_summary_csv: Path = Path("data/research_package/audit_report_summary.csv"),
    longitudinal_summary_csv: Path = Path("data/research_package/longitudinal_summary.csv"),
    cmp_confirmation_csv: Path = Path(
        "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
    ),
    results_tables_md: Path = Path("docs/research/ssrp_results_tables_2026-06-06.md"),
    paper_skeleton_md: Path = Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
    figure_plan_md: Path = Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
    writing_pack_md: Path = Path("docs/research/ssrp_writing_pack_2026-06-06.md"),
    cycle_report_md: Path = Path("docs/research/week2_cycle_report_2026-06-06.md"),
    out_md: Path = Path("docs/research/ssrp_claim_register_2026-06-06.md"),
    title: str = "SSRP 2026 Claim Register, 2026-06-06",
    week_label: str = "Week 2",
) -> None:
    """Export an evidence/status register for paper claims."""
    export_ssrp_claim_register(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        figure_plan_md=figure_plan_md,
        writing_pack_md=writing_pack_md,
        cycle_report_md=cycle_report_md,
        out_md=out_md,
        title=title,
        week_label=week_label,
    )
    typer.echo(f"Wrote SSRP claim register to {out_md}")


@app.command("ssrp-poster-plan")
def ssrp_poster_plan(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    audit_summary_csv: Path = Path("data/research_package/audit_report_summary.csv"),
    longitudinal_summary_csv: Path = Path("data/research_package/longitudinal_summary.csv"),
    cmp_confirmation_csv: Path = Path(
        "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
    ),
    results_tables_md: Path = Path("docs/research/ssrp_results_tables_2026-06-06.md"),
    paper_skeleton_md: Path = Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
    figure_plan_md: Path = Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
    writing_pack_md: Path = Path("docs/research/ssrp_writing_pack_2026-06-06.md"),
    claim_register_md: Path = Path("docs/research/ssrp_claim_register_2026-06-06.md"),
    cycle_report_md: Path = Path("docs/research/week2_cycle_report_2026-06-06.md"),
    out_md: Path = Path("docs/research/ssrp_poster_plan_2026-06-06.md"),
    title: str = "SSRP 2026 Poster Plan, 2026-06-06",
    week_label: str = "Week 2",
) -> None:
    """Export a poster storyboard, asset list, and finalization checklist."""
    export_ssrp_poster_plan(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        figure_plan_md=figure_plan_md,
        writing_pack_md=writing_pack_md,
        claim_register_md=claim_register_md,
        cycle_report_md=cycle_report_md,
        out_md=out_md,
        title=title,
        week_label=week_label,
    )
    typer.echo(f"Wrote SSRP poster plan to {out_md}")


@app.command()
def weekly(
    sites_csv: Path = Path("data/sites.csv"),
    consent_table_path: Path | None = Path("data/consent_table.csv"),
    cohort: str = "weekly",
    limit: int | None = None,
) -> None:
    """Run the full weekly pipeline against a CSV of URLs."""
    try:
        summary = asyncio.run(
            run_weekly_audit(
                sites_csv,
                consent_table_path=consent_table_path,
                cohort=cohort,
                limit=limit,
            )
        )
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    typer.echo(format_weekly_run_summary(summary))


@app.command("validate-sites")
def validate_sites(sites_csv: Path = Path("data/sites.csv")) -> None:
    """Validate a research sample site CSV before running browser capture."""
    result = validate_site_list(sites_csv)
    category_summary = ", ".join(
        f"{category}={count}" for category, count in sorted(result.categories.items())
    )
    typer.echo(
        f"{result.active_count} active sites; "
        f"mentor_inherited={result.inherited_from_phd_mentor_count}; "
        f"categories: {category_summary or 'none'}"
    )
    for issue in result.issues:
        location = f"row {issue.row_number}" if issue.row_number is not None else "file"
        typer.echo(f"{issue.level.value}: {issue.code}: {location}: {issue.message}")
    if result.errors:
        raise typer.Exit(1)


@app.command("sample-readiness")
def sample_readiness(
    candidates_csv: Path = Path("data/deep_sample_candidates.csv"),
    access_probe_csv: Path = Path("data/access_probe_pilot_2026-05-30.csv"),
    consent_table_csv: Annotated[
        list[Path] | None,
        typer.Option("--consent-table-csv"),
    ] = None,
    out_csv: Path = Path("data/sample_readiness_pilot_2026-05-30.csv"),
) -> None:
    """Export an advisor-facing table for deep-sample readiness review."""
    consent_tables = consent_table_csv or [
        Path("data/consent_table_smoke_2026-05-29.csv"),
        Path("data/consent_table_pilot_2026-05-30.csv"),
    ]
    rows = build_sample_readiness(candidates_csv, access_probe_csv, consent_tables)
    export_sample_readiness_to_csv(out_csv, rows)
    summary = summarize_readiness(rows)
    status_summary = ", ".join(
        f"{status}={count}" for status, count in sorted(summary.items())
    )
    typer.echo(
        f"Wrote {len(rows)} sample readiness rows to {out_csv}"
        f" ({status_summary or 'no statuses'})"
    )


@app.command("cmp-review-queue")
def cmp_review_queue(
    readiness_csv: Path = Path("data/sample_readiness_pilot_2026-05-30.csv"),
    consent_table_csv: Annotated[
        list[Path] | None,
        typer.Option("--consent-table-csv"),
    ] = None,
    out_csv: Path = Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
) -> None:
    """Export sites needing manual CMP review with screenshot/DOM evidence refs."""
    consent_tables = consent_table_csv or [
        Path("data/consent_table_smoke_2026-05-29.csv"),
        Path("data/consent_table_pilot_2026-05-30.csv"),
    ]
    rows = build_cmp_review_queue(readiness_csv, consent_tables)
    export_cmp_review_queue_to_csv(out_csv, rows)
    summary = summarize_cmp_review_queue(rows)
    status_summary = ", ".join(
        f"{status}={count}" for status, count in sorted(summary.items())
    )
    typer.echo(
        f"Wrote {len(rows)} CMP review rows to {out_csv}"
        f" ({status_summary or 'no statuses'})"
    )


@app.command("cmp-review-worksheet")
def cmp_review_worksheet(
    queue_csv: Path = Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
    out_csv: Path = Path("data/cmp_review_worksheet_pilot_2026-05-30.csv"),
) -> None:
    """Export a fillable manual decision worksheet for CMP review rows."""
    rows = build_cmp_review_worksheet(queue_csv)
    export_cmp_review_worksheet_to_csv(out_csv, rows)
    summary = summarize_cmp_review_worksheet(rows)
    status_summary = ", ".join(
        f"{status}={count}" for status, count in sorted(summary.items())
    )
    typer.echo(
        f"Wrote {len(rows)} CMP review worksheet rows to {out_csv}"
        f" ({status_summary or 'no statuses'})"
    )


@app.command("cmp-review-packet")
def cmp_review_packet(
    queue_csv: Path = Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
    out_dir: Path = Path("data/cmp_review_packet_pilot_2026-05-30"),
) -> None:
    """Export a static HTML/Markdown evidence packet for CMP review rows."""
    manifest = export_cmp_review_packet(queue_csv, out_dir)
    typer.echo(
        f"Wrote {manifest['row_count']} CMP review packet cards to "
        f"{manifest['index_html']} and {manifest['index_markdown']}"
    )


@app.command("cmp-review-suggestions")
def cmp_review_suggestions(
    queue_csv: Path = Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
    out_csv: Path = Path("data/cmp_review_suggestions_pilot_2026-05-30.csv"),
) -> None:
    """Export non-final suggested decisions for CMP review rows."""
    rows = build_cmp_review_suggestions(queue_csv)
    export_cmp_review_suggestions_to_csv(out_csv, rows)
    summary = summarize_cmp_review_suggestions(rows)
    status_summary = ", ".join(
        f"{decision}={count}" for decision, count in sorted(summary.items())
    )
    typer.echo(
        f"Wrote {len(rows)} CMP review suggestion rows to {out_csv}"
        f" ({status_summary or 'no suggestions'})"
    )


@app.command("cmp-review-rerun-targets")
def cmp_review_rerun_targets(
    suggestions_csv: Path = Path("data/cmp_review_suggestions_pilot_2026-05-30.csv"),
    out_csv: Path = Path("data/cmp_review_rerun_targets_pilot_2026-05-30.csv"),
) -> None:
    """Export weekly target rows for fresh-context CMP review reruns."""
    count = export_cmp_review_rerun_targets(suggestions_csv, out_csv)
    typer.echo(f"Wrote {count} CMP review rerun target rows to {out_csv}")


@app.command("cmp-review-decision-draft")
def cmp_review_decision_draft(
    queue_csv: Path = Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
    suggestions_csv: Path = Path("data/cmp_review_suggestions_pilot_2026-05-30.csv"),
    out_csv: Path = Path("data/cmp_review_decision_draft_pilot_2026-05-30.csv"),
) -> None:
    """Export non-final CMP worksheet decision drafts for advisor review."""
    rows = build_cmp_review_decision_draft(queue_csv, suggestions_csv)
    export_cmp_review_decision_draft_to_csv(out_csv, rows)
    summary = summarize_cmp_review_decision_draft(rows)
    status_summary = ", ".join(
        f"{decision}={count}" for decision, count in sorted(summary.items())
    )
    typer.echo(
        f"Wrote {len(rows)} CMP review decision draft rows to {out_csv}"
        f" ({status_summary or 'no draft decisions'})"
    )


@app.command("cmp-review-confirmation-sheet")
def cmp_review_confirmation_sheet(
    draft_csv: Path = Path("data/cmp_review_decision_draft_pilot_2026-05-30.csv"),
    out_csv: Path = Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
) -> None:
    """Export a human-fillable confirmation sheet for CMP review decisions."""
    rows = build_cmp_review_confirmation_sheet(draft_csv)
    export_cmp_review_confirmation_sheet_to_csv(out_csv, rows)
    summary = summarize_cmp_review_confirmation_sheet(rows)
    status_summary = ", ".join(
        f"{status}={count}" for status, count in sorted(summary.items())
    )
    typer.echo(
        f"Wrote {len(rows)} CMP review confirmation rows to {out_csv}"
        f" ({status_summary or 'no confirmation rows'})"
    )


@app.command("cmp-review-apply-confirmations")
def cmp_review_apply_confirmations(
    worksheet_csv: Path = Path("data/cmp_review_worksheet_pilot_2026-05-30.csv"),
    confirmation_csv: Path = Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
    out_csv: Path = Path("data/cmp_review_worksheet_confirmed_pilot_2026-05-30.csv"),
) -> None:
    """Apply explicitly confirmed CMP decisions to a worksheet copy."""
    summary = apply_cmp_review_confirmations_to_worksheet(
        worksheet_csv,
        confirmation_csv,
        out_csv,
    )
    status_summary = ", ".join(
        f"{status}={count}" for status, count in sorted(summary.items())
    )
    typer.echo(
        f"Wrote CMP review confirmed worksheet to {out_csv}"
        f" ({status_summary or 'no confirmations applied'})"
    )


@app.command("sample-lock-plan")
def sample_lock_plan(
    readiness_csv: Path = Path("data/sample_readiness_pilot_2026-05-30.csv"),
    worksheet_csv: Path = Path("data/cmp_review_worksheet_pilot_2026-05-30.csv"),
    out_csv: Path = Path("data/sample_lock_plan_pilot_2026-05-30.csv"),
) -> None:
    """Export a sample-lock action plan from readiness and review decisions."""
    rows = build_sample_lock_plan(readiness_csv, worksheet_csv)
    export_sample_lock_plan_to_csv(out_csv, rows)
    summary = summarize_sample_lock_plan(rows)
    status_summary = ", ".join(
        f"{status}={count}" for status, count in sorted(summary.items())
    )
    typer.echo(
        f"Wrote {len(rows)} sample lock rows to {out_csv}"
        f" ({status_summary or 'no statuses'})"
    )


@app.command("sample-action-queues")
def sample_action_queues(
    lock_plan_csv: Path = Path("data/sample_lock_plan_pilot_2026-05-30.csv"),
    out_dir: Path = Path("data/sample_action_queues_pilot_2026-05-30"),
) -> None:
    """Split the sample-lock plan into concrete next-action queues."""
    manifest = export_sample_lock_queues(lock_plan_csv, out_dir)
    status_summary = ", ".join(
        f"{queue_name}={count}" for queue_name, count in manifest.items()
    )
    typer.echo(
        f"Wrote sample action queues to {out_dir}"
        f" ({status_summary or 'no queues'})"
    )


@app.command("sample-weekly-targets")
def sample_weekly_targets(
    queues_dir: Path = Path("data/sample_action_queues_pilot_2026-05-30"),
    out_csv: Path = Path("data/deep_sample_weekly_targets_pilot_2026-05-30.csv"),
) -> None:
    """Export a weekly capture site-list CSV from sample action queues."""
    count = export_weekly_targets_from_queues(queues_dir, out_csv)
    typer.echo(f"Wrote {count} weekly target rows to {out_csv}")


@app.command("replacement-review")
def replacement_review(
    candidates_csv: Path = Path("data/replacement_candidates_batch2_2026-05-30.csv"),
    access_probe_csv: Path = Path("data/access_probe_replacements_batch2_2026-05-30.csv"),
    consent_table_csv: Path = Path("data/consent_table_replacements_batch2_2026-05-30.csv"),
    out_csv: Path = Path("data/replacement_review_batch2_2026-05-30.csv"),
) -> None:
    """Export replacement-candidate promotion decisions from observed evidence."""
    rows = build_replacement_review(candidates_csv, access_probe_csv, consent_table_csv)
    export_replacement_review_to_csv(out_csv, rows)
    summary = summarize_replacement_review(rows)
    status_summary = ", ".join(
        f"{status}={count}" for status, count in sorted(summary.items())
    )
    typer.echo(
        f"Wrote {len(rows)} replacement review rows to {out_csv}"
        f" ({status_summary or 'no statuses'})"
    )


@app.command("expanded-weekly-targets")
def expanded_weekly_targets(
    base_targets_csv: Path = Path("data/deep_sample_weekly_targets_pilot_2026-05-30.csv"),
    replacement_review_csv: Path = Path("data/replacement_review_batch2_2026-05-30.csv"),
    out_csv: Path = Path("data/deep_sample_weekly_targets_expanded_2026-05-30.csv"),
) -> None:
    """Add verified replacement candidates to the current weekly target list."""
    count = export_expanded_weekly_targets(
        base_targets_csv,
        replacement_review_csv,
        out_csv,
    )
    typer.echo(f"Wrote {count} expanded weekly target rows to {out_csv}")


@app.command("week2-capture-targets")
def week2_capture_targets(
    expanded_targets_csv: Path = Path("data/deep_sample_weekly_targets_expanded_2026-05-30.csv"),
    out_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
) -> None:
    """Freeze expanded targets as the Week 2 default capture list."""
    count = export_week2_capture_targets(expanded_targets_csv, out_csv)
    typer.echo(f"Wrote {count} Week 2 capture target rows to {out_csv}")


@app.command("advisor-update-brief")
def advisor_update_brief(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    audit_summary_csv: Path = Path("data/research_package/audit_report_summary.csv"),
    longitudinal_summary_csv: Path = Path("data/research_package/longitudinal_summary.csv"),
    cmp_confirmation_csv: Path = Path(
        "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
    ),
    manifest_json: Path = Path("data/research_package/research_manifest.json"),
    out_md: Path = Path("docs/research/week2_advisor_update_2026-06-06.md"),
    title: str = "Week 2 Advisor Update, 2026-06-06",
) -> None:
    """Export a compact advisor-facing Markdown update from current tables."""
    export_weekly_advisor_brief(
        targets_csv=targets_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        cmp_confirmation_csv=cmp_confirmation_csv,
        manifest_json=manifest_json,
        out_md=out_md,
        title=title,
    )
    typer.echo(f"Wrote advisor update brief to {out_md}")


@app.command("week2-sanity-check")
def week2_sanity_check(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    consent_table_csv: Path = Path("data/consent_table_pilot_2026-05-30.csv"),
    audit_summary_csv: Path = Path("data/research_package/audit_report_summary.csv"),
    longitudinal_summary_csv: Path = Path("data/research_package/longitudinal_summary.csv"),
    out_md: Path = Path("docs/research/week2_sanity_check_2026-06-06.md"),
    cohort: str = "week2-2026-06-06",
    week_of: str = "2026-06-06",
    title: str = "Week 2 Capture Sanity Check, 2026-06-06",
) -> None:
    """Export a post-capture sanity check for the Week 2 target list."""
    export_week2_sanity_check(
        targets_csv=targets_csv,
        consent_table_csv=consent_table_csv,
        audit_summary_csv=audit_summary_csv,
        longitudinal_summary_csv=longitudinal_summary_csv,
        out_md=out_md,
        cohort=cohort,
        week_of=week_of,
        title=title,
    )
    typer.echo(f"Wrote Week 2 sanity check to {out_md}")


@app.command("checkin-index")
def checkin_index(
    out_md: Path = Path("docs/research/week2_checkin_index_2026-06-06.md"),
    title: str = "Week 2 Advisor Check-in Index, 2026-06-06",
    advisor_brief: Path = Path("docs/research/week2_advisor_update_2026-06-06.md"),
    sanity_check: Path = Path("docs/research/week2_sanity_check_2026-06-06.md"),
    capture_checklist: Path = Path(
        "docs/research/week2_capture_day_checklist_2026-06-06.md"
    ),
    cycle_report: Path = Path("docs/research/week2_cycle_report_2026-06-06.md"),
    runbook: Path = Path("docs/research/week2_execution_runbook_2026-06-06.md"),
    sample_plan: Path = Path("docs/research/week2_sample_plan_2026-05-30.md"),
    cmp_confirmation_sheet: Path = Path(
        "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
    ),
    cmp_packet: Path = Path("data/cmp_review_packet_pilot_2026-05-30/index.html"),
    research_package_dir: Path = Path("data/research_package"),
    research_manifest: Path = Path("data/research_package/research_manifest.json"),
) -> None:
    """Export a linked advisor check-in index for Week 2 artifacts."""
    export_checkin_index(
        out_md=out_md,
        title=title,
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
    )
    typer.echo(f"Wrote check-in index to {out_md}")


@app.command("week2-capture-checklist")
def week2_capture_checklist(
    out_md: Path = Path("docs/research/week2_capture_day_checklist_2026-06-06.md"),
    title: str = "Week 2 Capture-Day Checklist, 2026-06-06",
    week_of: str = "2026-06-06",
    cohort: str = "week2-2026-06-06",
    expected_target_count: int = 5,
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    consent_table_csv: Path = Path("data/consent_table_pilot_2026-05-30.csv"),
    preflight_check: Path = Path("docs/research/week2_preflight_check_2026-06-06.md"),
    cycle_report: Path = Path("docs/research/week2_cycle_report_2026-06-06.md"),
    refresh_report: Path = Path("docs/research/week2_refresh_report_2026-06-06.md"),
    sanity_check: Path = Path("docs/research/week2_sanity_check_2026-06-06.md"),
    checkin_index: Path = Path("docs/research/week2_checkin_index_2026-06-06.md"),
    advisor_brief: Path = Path("docs/research/week2_advisor_update_2026-06-06.md"),
) -> None:
    """Export the Week 2 capture-day operator checklist."""
    export_week2_capture_checklist(
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
    )
    typer.echo(f"Wrote Week 2 capture checklist to {out_md}")


@app.command("week2-preflight-check")
def week2_preflight_check(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    sanity_check_md: Path = Path("docs/research/week2_sanity_check_2026-06-06.md"),
    advisor_brief_md: Path = Path("docs/research/week2_advisor_update_2026-06-06.md"),
    checkin_index_md: Path = Path("docs/research/week2_checkin_index_2026-06-06.md"),
    runbook_md: Path = Path("docs/research/week2_execution_runbook_2026-06-06.md"),
    research_manifest_json: Path = Path("data/research_package/research_manifest.json"),
    cmp_confirmation_csv: Path = Path(
        "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
    ),
    cmp_packet_html: Path = Path("data/cmp_review_packet_pilot_2026-05-30/index.html"),
    out_md: Path = Path("docs/research/week2_preflight_check_2026-06-06.md"),
    title: str = "Week 2 Preflight Check, 2026-06-06",
    expected_target_count: int = 5,
) -> None:
    """Export a preflight gate before the scheduled Week 2 capture."""
    export_week2_preflight_check(
        targets_csv=targets_csv,
        sanity_check_md=sanity_check_md,
        advisor_brief_md=advisor_brief_md,
        checkin_index_md=checkin_index_md,
        runbook_md=runbook_md,
        research_manifest_json=research_manifest_json,
        cmp_confirmation_csv=cmp_confirmation_csv,
        cmp_packet_html=cmp_packet_html,
        out_md=out_md,
        title=title,
        expected_target_count=expected_target_count,
    )
    typer.echo(f"Wrote Week 2 preflight check to {out_md}")


@app.command("week2-refresh-outputs")
def week2_refresh_outputs(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    consent_table_csv: Path = Path("data/consent_table_pilot_2026-05-30.csv"),
    cmp_confirmation_csv: Path = Path(
        "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
    ),
    cmp_packet_html: Path = Path("data/cmp_review_packet_pilot_2026-05-30/index.html"),
    runbook_md: Path = Path("docs/research/week2_execution_runbook_2026-06-06.md"),
    sample_plan_md: Path = Path("docs/research/week2_sample_plan_2026-05-30.md"),
    research_package_dir: Path = Path("data/research_package"),
    advisor_brief_md: Path = Path("docs/research/week2_advisor_update_2026-06-06.md"),
    sanity_check_md: Path = Path("docs/research/week2_sanity_check_2026-06-06.md"),
    checkin_index_md: Path = Path("docs/research/week2_checkin_index_2026-06-06.md"),
    capture_checklist_md: Path = Path(
        "docs/research/week2_capture_day_checklist_2026-06-06.md"
    ),
    results_tables_md: Path = Path("docs/research/ssrp_results_tables_2026-06-06.md"),
    paper_skeleton_md: Path = Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
    figure_plan_md: Path = Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
    writing_pack_md: Path = Path("docs/research/ssrp_writing_pack_2026-06-06.md"),
    claim_register_md: Path = Path("docs/research/ssrp_claim_register_2026-06-06.md"),
    poster_plan_md: Path = Path("docs/research/ssrp_poster_plan_2026-06-06.md"),
    preflight_check_md: Path = Path("docs/research/week2_preflight_check_2026-06-06.md"),
    refresh_report_md: Path = Path("docs/research/week2_refresh_report_2026-06-06.md"),
    cycle_report_md: Path = Path("docs/research/week2_cycle_report_2026-06-06.md"),
    cohort: str = "week2-2026-06-06",
    week_of: str = "2026-06-06",
    expected_target_count: int = 5,
    limit: int = 500,
) -> None:
    """Refresh all Week 2 paper/advisor outputs after a capture run."""
    summary = refresh_week2_outputs(
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
        results_tables_md=results_tables_md,
        paper_skeleton_md=paper_skeleton_md,
        figure_plan_md=figure_plan_md,
        writing_pack_md=writing_pack_md,
        claim_register_md=claim_register_md,
        poster_plan_md=poster_plan_md,
        preflight_check_md=preflight_check_md,
        refresh_report_md=refresh_report_md,
        cycle_report_md=cycle_report_md,
        cohort=cohort,
        week_of=week_of,
        expected_target_count=expected_target_count,
        limit=limit,
    )
    typer.echo(
        "Refreshed Week 2 outputs "
        f"({summary['audit_report_count']} reports, "
        f"{summary['weekly_summary_count']} weekly summaries; "
        f"sanity={summary['sanity_status']}; "
        f"preflight={summary['preflight_status']})"
    )


@app.command("week2-cycle")
def week2_cycle(
    targets_csv: Path = Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    consent_table_csv: Path = Path("data/consent_table_pilot_2026-05-30.csv"),
    cmp_confirmation_csv: Path = Path(
        "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
    ),
    cmp_packet_html: Path = Path("data/cmp_review_packet_pilot_2026-05-30/index.html"),
    runbook_md: Path = Path("docs/research/week2_execution_runbook_2026-06-06.md"),
    sample_plan_md: Path = Path("docs/research/week2_sample_plan_2026-05-30.md"),
    research_package_dir: Path = Path("data/research_package"),
    advisor_brief_md: Path = Path("docs/research/week2_advisor_update_2026-06-06.md"),
    sanity_check_md: Path = Path("docs/research/week2_sanity_check_2026-06-06.md"),
    checkin_index_md: Path = Path("docs/research/week2_checkin_index_2026-06-06.md"),
    capture_checklist_md: Path = Path(
        "docs/research/week2_capture_day_checklist_2026-06-06.md"
    ),
    preflight_check_md: Path = Path("docs/research/week2_preflight_check_2026-06-06.md"),
    refresh_report_md: Path = Path("docs/research/week2_refresh_report_2026-06-06.md"),
    cycle_report_md: Path = Path("docs/research/week2_cycle_report_2026-06-06.md"),
    cohort: str = "week2-2026-06-06",
    week_of: str = "2026-06-06",
    run_date: str | None = None,
    expected_target_count: int = 5,
    limit: int = 500,
    force: bool = False,
    allow_early: bool = False,
    dry_run: bool = False,
) -> None:
    """Run or dry-run the full Week 2 preflight, capture, and refresh cycle."""
    try:
        summary = asyncio.run(
            run_week2_cycle(
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
                run_date=run_date,
                expected_target_count=expected_target_count,
                limit=limit,
                force=force,
                allow_early=allow_early,
                dry_run=dry_run,
            )
        )
    except RuntimeError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    action = "Dry-ran" if dry_run else "Completed"
    preflight_status = summary["post_refresh_preflight_status"]
    if dry_run:
        preflight_status = summary["preflight_status"]
    typer.echo(
        f"{action} Week 2 cycle "
        f"({summary['audit_report_count']} reports, "
        f"{summary['weekly_summary_count']} weekly summaries; "
        f"sanity={summary['sanity_status']}; "
        f"preflight={preflight_status})"
    )


@app.command("export-audit-reports")
def export_audit_reports(
    out_csv: Path = Path("data/audit_report_summary.csv"),
    limit: int = 500,
) -> None:
    """Export saved AuditReport rows to a CSV table."""
    reports = list_reports(limit=limit)
    export_audit_reports_to_csv(out_csv, reports)
    typer.echo(f"Wrote {len(reports)} audit reports to {out_csv}")


@app.command("export-longitudinal-summary")
def export_longitudinal_summary(
    out_csv: Path = Path("data/longitudinal_summary.csv"),
    limit: int = 500,
) -> None:
    """Export saved WeeklySummary rows to a CSV table."""
    summaries = list_weekly_summaries(limit=limit)
    export_weekly_summaries_to_csv(out_csv, summaries)
    typer.echo(f"Wrote {len(summaries)} weekly summaries to {out_csv}")


@app.command("export-research-package")
def export_research_package(
    out_dir: Path = Path("data/research_package"),
    limit: int = 500,
) -> None:
    """Export all paper-facing research tables plus a manifest."""
    manifest = export_research_package_data(out_dir, limit=limit)
    typer.echo(
        "Wrote research package "
        f"({manifest['audit_report_count']} reports, "
        f"{manifest['weekly_summary_count']} weekly summaries) to {out_dir}"
    )


if __name__ == "__main__":
    app()
