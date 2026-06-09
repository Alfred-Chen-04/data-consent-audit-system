"""Tests for the installed package CLI."""

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from typer.testing import CliRunner

from consent_audit import cli

runner = CliRunner()


def test_cli_help_lists_research_export_commands() -> None:
    result = runner.invoke(cli.app, ["--help"])

    assert result.exit_code == 0
    assert "audit" in result.output
    assert "access-probe" in result.output
    assert "access-probe-summary" in result.output
    assert "research-status" in result.output
    assert "ssrp-paper-skeleton" in result.output
    assert "ssrp-results-tables" in result.output
    assert "ssrp-figure-plan" in result.output
    assert "ssrp-writing-pack" in result.output
    assert "ssrp-claim-register" in result.output
    assert "ssrp-poster-plan" in result.output
    assert "weekly" in result.output
    assert "export-audit-reports" in result.output
    assert "export-longitudinal-summary" in result.output
    assert "export-research-package" in result.output
    assert "cmp-review-queue" in result.output
    assert "cmp-review-worksheet" in result.output
    assert "cmp-review-packet" in result.output
    assert "cmp-review-suggestions" in result.output
    assert "cmp-review-rerun-targets" in result.output
    assert "cmp-review-decision-draft" in result.output
    assert "cmp-review-confirmation-sheet" in result.output
    assert "cmp-review-apply-confirmations" in result.output
    assert "sample-lock-plan" in result.output
    assert "sample-action-queues" in result.output
    assert "sample-weekly-targets" in result.output
    assert "replacement-review" in result.output
    assert "expanded-weekly-targets" in result.output
    assert "week2-capture-targets" in result.output
    assert "advisor-update-brief" in result.output
    assert "week2-sanity-check" in result.output
    assert "checkin-index" in result.output
    assert "week2-preflight-check" in result.output
    assert "week2-capture-checklist" in result.output
    assert "week2-refresh-outputs" in result.output
    assert "week2-cycle" in result.output


def test_cli_audit_invokes_single_site_pipeline(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    async def fake_run_single_site_audit(
        url: str,
        *,
        save: bool,
        consent_table_path: Path | None = None,
        cohort: str = "",
    ) -> SimpleNamespace:
        seen["url"] = url
        seen["save"] = save
        seen["consent_table_path"] = consent_table_path
        seen["cohort"] = cohort
        return SimpleNamespace(report_markdown="report")

    monkeypatch.setattr(cli, "run_single_site_audit", fake_run_single_site_audit)
    out_csv = tmp_path / "consent_table.csv"

    result = runner.invoke(
        cli.app,
        [
            "audit",
            "https://example.com",
            "--no-save",
            "--consent-table-path",
            str(out_csv),
            "--cohort",
            "smoke",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "url": "https://example.com",
        "save": False,
        "consent_table_path": out_csv,
        "cohort": "smoke",
    }


def test_cli_weekly_invokes_weekly_pipeline(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None = None,
    ) -> SimpleNamespace:
        seen["sites_csv"] = sites_csv
        seen["consent_table_path"] = consent_table_path
        seen["cohort"] = cohort
        seen["limit"] = limit
        return SimpleNamespace(
            target_count=2,
            attempted_count=2,
            succeeded_count=1,
            failed_count=1,
            failures=[],
            budget_exceeded=False,
        )

    monkeypatch.setattr(cli, "run_weekly_audit", fake_run_weekly_audit)
    sites_csv = tmp_path / "sites.csv"
    out_csv = tmp_path / "weekly_consent_table.csv"

    result = runner.invoke(
        cli.app,
        [
            "weekly",
            "--sites-csv",
            str(sites_csv),
            "--consent-table-path",
            str(out_csv),
            "--cohort",
            "weekly_smoke",
            "--limit",
            "2",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "sites_csv": sites_csv,
        "consent_table_path": out_csv,
        "cohort": "weekly_smoke",
        "limit": 2,
    }
    assert "attempted=2/2" in result.output
    assert "succeeded=1" in result.output
    assert "failed=1" in result.output
    assert "budget_exceeded=false" in result.output


def test_cli_weekly_reports_site_list_validation_errors(
    monkeypatch,
    tmp_path: Path,
) -> None:
    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None = None,
    ) -> SimpleNamespace:
        _ = (sites_csv, consent_table_path, cohort, limit)
        raise ValueError("site list validation failed before weekly capture: placeholder_url")

    monkeypatch.setattr(cli, "run_weekly_audit", fake_run_weekly_audit)
    sites_csv = tmp_path / "sites.csv"

    result = runner.invoke(cli.app, ["weekly", "--sites-csv", str(sites_csv)])

    assert result.exit_code == 1
    assert "site list validation failed before weekly capture: placeholder_url" in result.output


def test_cli_access_probe_invokes_probe_runner(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    async def fake_run_access_probe_from_csv(
        sites_csv: Path,
        out_csv: Path,
        *,
        concurrency: int,
        timeout_ms: int,
    ) -> SimpleNamespace:
        seen["sites_csv"] = sites_csv
        seen["out_csv"] = out_csv
        seen["concurrency"] = concurrency
        seen["timeout_ms"] = timeout_ms
        return SimpleNamespace(
            total=2,
            loaded=1,
            banner_detected=1,
            blocked_or_error=0,
            out_csv=out_csv,
            screenshot_dir=tmp_path / "captures" / "access_probe",
        )

    monkeypatch.setattr(
        cli,
        "run_access_probe_from_csv",
        fake_run_access_probe_from_csv,
        raising=False,
    )
    sites_csv = tmp_path / "sites.csv"
    out_csv = tmp_path / "access_probe.csv"

    result = runner.invoke(
        cli.app,
        [
            "access-probe",
            "--sites-csv",
            str(sites_csv),
            "--out-csv",
            str(out_csv),
            "--concurrency",
            "2",
            "--timeout-ms",
            "1234",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "sites_csv": sites_csv,
        "out_csv": out_csv,
        "concurrency": 2,
        "timeout_ms": 1234,
    }
    assert "total=2" in result.output
    assert "loaded=1" in result.output
    assert "banner_detected=1" in result.output
    assert "blocked_or_error=0" in result.output


def test_cli_access_probe_summary_invokes_renderer(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_render_access_probe_summary(csv_path: Path) -> str:
        seen["csv_path"] = csv_path
        return "probe summary"

    monkeypatch.setattr(
        cli,
        "render_access_probe_summary",
        fake_render_access_probe_summary,
        raising=False,
    )
    csv_path = tmp_path / "access_probe.csv"

    result = runner.invoke(
        cli.app,
        [
            "access-probe-summary",
            "--csv-path",
            str(csv_path),
        ],
    )

    assert result.exit_code == 0
    assert seen == {"csv_path": csv_path}
    assert "probe summary" in result.output


def test_cli_research_status_invokes_renderer(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_render_research_status(
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
        seen["targets_csv"] = targets_csv
        seen["research_manifest_json"] = research_manifest_json
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["preflight_md"] = preflight_md
        seen["sanity_md"] = sanity_md
        seen["cycle_report_md"] = cycle_report_md
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["figure_plan_md"] = figure_plan_md
        seen["writing_pack_md"] = writing_pack_md
        seen["claim_register_md"] = claim_register_md
        seen["poster_plan_md"] = poster_plan_md
        return "research status"

    monkeypatch.setattr(
        cli,
        "render_research_status",
        fake_render_research_status,
        raising=False,
    )
    targets_csv = tmp_path / "targets.csv"
    manifest_json = tmp_path / "manifest.json"
    cmp_csv = tmp_path / "cmp.csv"
    preflight_md = tmp_path / "preflight.md"
    sanity_md = tmp_path / "sanity.md"
    cycle_md = tmp_path / "cycle.md"
    results_tables_md = tmp_path / "results_tables.md"
    paper_skeleton_md = tmp_path / "paper_skeleton.md"
    figure_plan_md = tmp_path / "figure_plan.md"
    writing_pack_md = tmp_path / "writing_pack.md"
    claim_register_md = tmp_path / "claim_register.md"
    poster_plan_md = tmp_path / "poster_plan.md"

    result = runner.invoke(
        cli.app,
        [
            "research-status",
            "--targets-csv",
            str(targets_csv),
            "--research-manifest-json",
            str(manifest_json),
            "--cmp-confirmation-csv",
            str(cmp_csv),
            "--preflight-md",
            str(preflight_md),
            "--sanity-md",
            str(sanity_md),
            "--cycle-report-md",
            str(cycle_md),
            "--results-tables-md",
            str(results_tables_md),
            "--paper-skeleton-md",
            str(paper_skeleton_md),
            "--figure-plan-md",
            str(figure_plan_md),
            "--writing-pack-md",
            str(writing_pack_md),
            "--claim-register-md",
            str(claim_register_md),
            "--poster-plan-md",
            str(poster_plan_md),
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": targets_csv,
        "research_manifest_json": manifest_json,
        "cmp_confirmation_csv": cmp_csv,
        "preflight_md": preflight_md,
        "sanity_md": sanity_md,
        "cycle_report_md": cycle_md,
        "results_tables_md": results_tables_md,
        "paper_skeleton_md": paper_skeleton_md,
        "figure_plan_md": figure_plan_md,
        "writing_pack_md": writing_pack_md,
        "claim_register_md": claim_register_md,
        "poster_plan_md": poster_plan_md,
    }
    assert "research status" in result.output


def test_cli_ssrp_paper_skeleton_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_paper_skeleton(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        manifest_json: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["manifest_json"] = manifest_json
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Paper skeleton\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_paper_skeleton",
        fake_export_ssrp_paper_skeleton,
        raising=False,
    )

    result = runner.invoke(
        cli.app,
        [
            "ssrp-paper-skeleton",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--audit-summary-csv",
            str(tmp_path / "audit.csv"),
            "--longitudinal-summary-csv",
            str(tmp_path / "longitudinal.csv"),
            "--manifest-json",
            str(tmp_path / "manifest.json"),
            "--out-md",
            str(tmp_path / "paper.md"),
            "--title",
            "Custom Paper Skeleton",
            "--week-label",
            "Week X",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "audit_summary_csv": tmp_path / "audit.csv",
        "longitudinal_summary_csv": tmp_path / "longitudinal.csv",
        "manifest_json": tmp_path / "manifest.json",
        "out_md": tmp_path / "paper.md",
        "title": "Custom Paper Skeleton",
        "week_label": "Week X",
    }
    assert "Wrote SSRP paper skeleton" in result.output


def test_cli_ssrp_paper_skeleton_defaults_to_week2_artifacts(
    monkeypatch,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_paper_skeleton(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        manifest_json: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["manifest_json"] = manifest_json
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Paper skeleton\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_paper_skeleton",
        fake_export_ssrp_paper_skeleton,
        raising=False,
    )

    result = runner.invoke(cli.app, ["ssrp-paper-skeleton"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "audit_summary_csv": Path("data/research_package/audit_report_summary.csv"),
        "longitudinal_summary_csv": Path("data/research_package/longitudinal_summary.csv"),
        "manifest_json": Path("data/research_package/research_manifest.json"),
        "out_md": Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
        "title": "SSRP 2026 Paper Skeleton, 2026-06-06",
        "week_label": "Week 2",
    }


def test_cli_ssrp_results_tables_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_results_tables(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Results tables\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_results_tables",
        fake_export_ssrp_results_tables,
        raising=False,
    )

    result = runner.invoke(
        cli.app,
        [
            "ssrp-results-tables",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--audit-summary-csv",
            str(tmp_path / "audit.csv"),
            "--longitudinal-summary-csv",
            str(tmp_path / "longitudinal.csv"),
            "--out-md",
            str(tmp_path / "tables.md"),
            "--title",
            "Custom Results Tables",
            "--week-label",
            "Week X",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "audit_summary_csv": tmp_path / "audit.csv",
        "longitudinal_summary_csv": tmp_path / "longitudinal.csv",
        "out_md": tmp_path / "tables.md",
        "title": "Custom Results Tables",
        "week_label": "Week X",
    }
    assert "Wrote SSRP results tables" in result.output


def test_cli_ssrp_results_tables_defaults_to_week2_artifacts(
    monkeypatch,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_results_tables(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Results tables\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_results_tables",
        fake_export_ssrp_results_tables,
        raising=False,
    )

    result = runner.invoke(cli.app, ["ssrp-results-tables"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "audit_summary_csv": Path("data/research_package/audit_report_summary.csv"),
        "longitudinal_summary_csv": Path("data/research_package/longitudinal_summary.csv"),
        "out_md": Path("docs/research/ssrp_results_tables_2026-06-06.md"),
        "title": "SSRP 2026 Results Tables, 2026-06-06",
        "week_label": "Week 2",
    }


def test_cli_ssrp_figure_plan_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_figure_plan(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        results_tables_md: Path,
        paper_skeleton_md: Path,
        cycle_report_md: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["cycle_report_md"] = cycle_report_md
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Figure plan\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_figure_plan",
        fake_export_ssrp_figure_plan,
        raising=False,
    )

    result = runner.invoke(
        cli.app,
        [
            "ssrp-figure-plan",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--audit-summary-csv",
            str(tmp_path / "audit.csv"),
            "--longitudinal-summary-csv",
            str(tmp_path / "longitudinal.csv"),
            "--results-tables-md",
            str(tmp_path / "tables.md"),
            "--paper-skeleton-md",
            str(tmp_path / "paper.md"),
            "--cycle-report-md",
            str(tmp_path / "cycle.md"),
            "--out-md",
            str(tmp_path / "figures.md"),
            "--title",
            "Custom Figure Plan",
            "--week-label",
            "Week X",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "audit_summary_csv": tmp_path / "audit.csv",
        "longitudinal_summary_csv": tmp_path / "longitudinal.csv",
        "results_tables_md": tmp_path / "tables.md",
        "paper_skeleton_md": tmp_path / "paper.md",
        "cycle_report_md": tmp_path / "cycle.md",
        "out_md": tmp_path / "figures.md",
        "title": "Custom Figure Plan",
        "week_label": "Week X",
    }
    assert "Wrote SSRP figure plan" in result.output


def test_cli_ssrp_figure_plan_defaults_to_week2_artifacts(
    monkeypatch,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_figure_plan(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        results_tables_md: Path,
        paper_skeleton_md: Path,
        cycle_report_md: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["cycle_report_md"] = cycle_report_md
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Figure plan\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_figure_plan",
        fake_export_ssrp_figure_plan,
        raising=False,
    )

    result = runner.invoke(cli.app, ["ssrp-figure-plan"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "audit_summary_csv": Path("data/research_package/audit_report_summary.csv"),
        "longitudinal_summary_csv": Path("data/research_package/longitudinal_summary.csv"),
        "results_tables_md": Path("docs/research/ssrp_results_tables_2026-06-06.md"),
        "paper_skeleton_md": Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
        "cycle_report_md": Path("docs/research/week2_cycle_report_2026-06-06.md"),
        "out_md": Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
        "title": "SSRP 2026 Figure Plan, 2026-06-06",
        "week_label": "Week 2",
    }


def test_cli_ssrp_writing_pack_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_writing_pack(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        cmp_confirmation_csv: Path,
        results_tables_md: Path,
        paper_skeleton_md: Path,
        figure_plan_md: Path,
        cycle_report_md: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["figure_plan_md"] = figure_plan_md
        seen["cycle_report_md"] = cycle_report_md
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Writing pack\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_writing_pack",
        fake_export_ssrp_writing_pack,
        raising=False,
    )

    result = runner.invoke(
        cli.app,
        [
            "ssrp-writing-pack",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--audit-summary-csv",
            str(tmp_path / "audit.csv"),
            "--longitudinal-summary-csv",
            str(tmp_path / "longitudinal.csv"),
            "--cmp-confirmation-csv",
            str(tmp_path / "cmp.csv"),
            "--results-tables-md",
            str(tmp_path / "tables.md"),
            "--paper-skeleton-md",
            str(tmp_path / "paper.md"),
            "--figure-plan-md",
            str(tmp_path / "figures.md"),
            "--cycle-report-md",
            str(tmp_path / "cycle.md"),
            "--out-md",
            str(tmp_path / "writing.md"),
            "--title",
            "Custom Writing Pack",
            "--week-label",
            "Week X",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "audit_summary_csv": tmp_path / "audit.csv",
        "longitudinal_summary_csv": tmp_path / "longitudinal.csv",
        "cmp_confirmation_csv": tmp_path / "cmp.csv",
        "results_tables_md": tmp_path / "tables.md",
        "paper_skeleton_md": tmp_path / "paper.md",
        "figure_plan_md": tmp_path / "figures.md",
        "cycle_report_md": tmp_path / "cycle.md",
        "out_md": tmp_path / "writing.md",
        "title": "Custom Writing Pack",
        "week_label": "Week X",
    }
    assert "Wrote SSRP writing pack" in result.output


def test_cli_ssrp_writing_pack_defaults_to_week2_artifacts(
    monkeypatch,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_writing_pack(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        cmp_confirmation_csv: Path,
        results_tables_md: Path,
        paper_skeleton_md: Path,
        figure_plan_md: Path,
        cycle_report_md: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["figure_plan_md"] = figure_plan_md
        seen["cycle_report_md"] = cycle_report_md
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Writing pack\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_writing_pack",
        fake_export_ssrp_writing_pack,
        raising=False,
    )

    result = runner.invoke(cli.app, ["ssrp-writing-pack"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "audit_summary_csv": Path("data/research_package/audit_report_summary.csv"),
        "longitudinal_summary_csv": Path("data/research_package/longitudinal_summary.csv"),
        "cmp_confirmation_csv": Path(
            "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
        ),
        "results_tables_md": Path("docs/research/ssrp_results_tables_2026-06-06.md"),
        "paper_skeleton_md": Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
        "figure_plan_md": Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
        "cycle_report_md": Path("docs/research/week2_cycle_report_2026-06-06.md"),
        "out_md": Path("docs/research/ssrp_writing_pack_2026-06-06.md"),
        "title": "SSRP 2026 Writing Pack, 2026-06-06",
        "week_label": "Week 2",
    }


def test_cli_ssrp_claim_register_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_claim_register(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        cmp_confirmation_csv: Path,
        results_tables_md: Path,
        paper_skeleton_md: Path,
        figure_plan_md: Path,
        writing_pack_md: Path,
        cycle_report_md: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["figure_plan_md"] = figure_plan_md
        seen["writing_pack_md"] = writing_pack_md
        seen["cycle_report_md"] = cycle_report_md
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Claim register\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_claim_register",
        fake_export_ssrp_claim_register,
        raising=False,
    )

    result = runner.invoke(
        cli.app,
        [
            "ssrp-claim-register",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--audit-summary-csv",
            str(tmp_path / "audit.csv"),
            "--longitudinal-summary-csv",
            str(tmp_path / "longitudinal.csv"),
            "--cmp-confirmation-csv",
            str(tmp_path / "cmp.csv"),
            "--results-tables-md",
            str(tmp_path / "tables.md"),
            "--paper-skeleton-md",
            str(tmp_path / "paper.md"),
            "--figure-plan-md",
            str(tmp_path / "figures.md"),
            "--writing-pack-md",
            str(tmp_path / "writing.md"),
            "--cycle-report-md",
            str(tmp_path / "cycle.md"),
            "--out-md",
            str(tmp_path / "claims.md"),
            "--title",
            "Custom Claim Register",
            "--week-label",
            "Week X",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "audit_summary_csv": tmp_path / "audit.csv",
        "longitudinal_summary_csv": tmp_path / "longitudinal.csv",
        "cmp_confirmation_csv": tmp_path / "cmp.csv",
        "results_tables_md": tmp_path / "tables.md",
        "paper_skeleton_md": tmp_path / "paper.md",
        "figure_plan_md": tmp_path / "figures.md",
        "writing_pack_md": tmp_path / "writing.md",
        "cycle_report_md": tmp_path / "cycle.md",
        "out_md": tmp_path / "claims.md",
        "title": "Custom Claim Register",
        "week_label": "Week X",
    }
    assert "Wrote SSRP claim register" in result.output


def test_cli_ssrp_claim_register_defaults_to_week2_artifacts(
    monkeypatch,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_claim_register(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        cmp_confirmation_csv: Path,
        results_tables_md: Path,
        paper_skeleton_md: Path,
        figure_plan_md: Path,
        writing_pack_md: Path,
        cycle_report_md: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["figure_plan_md"] = figure_plan_md
        seen["writing_pack_md"] = writing_pack_md
        seen["cycle_report_md"] = cycle_report_md
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Claim register\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_claim_register",
        fake_export_ssrp_claim_register,
        raising=False,
    )

    result = runner.invoke(cli.app, ["ssrp-claim-register"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "audit_summary_csv": Path("data/research_package/audit_report_summary.csv"),
        "longitudinal_summary_csv": Path("data/research_package/longitudinal_summary.csv"),
        "cmp_confirmation_csv": Path(
            "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
        ),
        "results_tables_md": Path("docs/research/ssrp_results_tables_2026-06-06.md"),
        "paper_skeleton_md": Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
        "figure_plan_md": Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
        "writing_pack_md": Path("docs/research/ssrp_writing_pack_2026-06-06.md"),
        "cycle_report_md": Path("docs/research/week2_cycle_report_2026-06-06.md"),
        "out_md": Path("docs/research/ssrp_claim_register_2026-06-06.md"),
        "title": "SSRP 2026 Claim Register, 2026-06-06",
        "week_label": "Week 2",
    }


def test_cli_ssrp_poster_plan_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_poster_plan(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        cmp_confirmation_csv: Path,
        results_tables_md: Path,
        paper_skeleton_md: Path,
        figure_plan_md: Path,
        writing_pack_md: Path,
        claim_register_md: Path,
        cycle_report_md: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["figure_plan_md"] = figure_plan_md
        seen["writing_pack_md"] = writing_pack_md
        seen["claim_register_md"] = claim_register_md
        seen["cycle_report_md"] = cycle_report_md
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Poster plan\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_poster_plan",
        fake_export_ssrp_poster_plan,
        raising=False,
    )

    result = runner.invoke(
        cli.app,
        [
            "ssrp-poster-plan",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--audit-summary-csv",
            str(tmp_path / "audit.csv"),
            "--longitudinal-summary-csv",
            str(tmp_path / "longitudinal.csv"),
            "--cmp-confirmation-csv",
            str(tmp_path / "cmp.csv"),
            "--results-tables-md",
            str(tmp_path / "tables.md"),
            "--paper-skeleton-md",
            str(tmp_path / "paper.md"),
            "--figure-plan-md",
            str(tmp_path / "figures.md"),
            "--writing-pack-md",
            str(tmp_path / "writing.md"),
            "--claim-register-md",
            str(tmp_path / "claims.md"),
            "--cycle-report-md",
            str(tmp_path / "cycle.md"),
            "--out-md",
            str(tmp_path / "poster.md"),
            "--title",
            "Custom Poster Plan",
            "--week-label",
            "Week X",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "audit_summary_csv": tmp_path / "audit.csv",
        "longitudinal_summary_csv": tmp_path / "longitudinal.csv",
        "cmp_confirmation_csv": tmp_path / "cmp.csv",
        "results_tables_md": tmp_path / "tables.md",
        "paper_skeleton_md": tmp_path / "paper.md",
        "figure_plan_md": tmp_path / "figures.md",
        "writing_pack_md": tmp_path / "writing.md",
        "claim_register_md": tmp_path / "claims.md",
        "cycle_report_md": tmp_path / "cycle.md",
        "out_md": tmp_path / "poster.md",
        "title": "Custom Poster Plan",
        "week_label": "Week X",
    }
    assert "Wrote SSRP poster plan" in result.output


def test_cli_ssrp_poster_plan_defaults_to_week2_artifacts(
    monkeypatch,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_ssrp_poster_plan(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        cmp_confirmation_csv: Path,
        results_tables_md: Path,
        paper_skeleton_md: Path,
        figure_plan_md: Path,
        writing_pack_md: Path,
        claim_register_md: Path,
        cycle_report_md: Path,
        out_md: Path,
        title: str,
        week_label: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["figure_plan_md"] = figure_plan_md
        seen["writing_pack_md"] = writing_pack_md
        seen["claim_register_md"] = claim_register_md
        seen["cycle_report_md"] = cycle_report_md
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_label"] = week_label
        return "# Poster plan\n"

    monkeypatch.setattr(
        cli,
        "export_ssrp_poster_plan",
        fake_export_ssrp_poster_plan,
        raising=False,
    )

    result = runner.invoke(cli.app, ["ssrp-poster-plan"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "audit_summary_csv": Path("data/research_package/audit_report_summary.csv"),
        "longitudinal_summary_csv": Path("data/research_package/longitudinal_summary.csv"),
        "cmp_confirmation_csv": Path(
            "data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"
        ),
        "results_tables_md": Path("docs/research/ssrp_results_tables_2026-06-06.md"),
        "paper_skeleton_md": Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
        "figure_plan_md": Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
        "writing_pack_md": Path("docs/research/ssrp_writing_pack_2026-06-06.md"),
        "claim_register_md": Path("docs/research/ssrp_claim_register_2026-06-06.md"),
        "cycle_report_md": Path("docs/research/week2_cycle_report_2026-06-06.md"),
        "out_md": Path("docs/research/ssrp_poster_plan_2026-06-06.md"),
        "title": "SSRP 2026 Poster Plan, 2026-06-06",
        "week_label": "Week 2",
    }


def test_cli_validate_sites_reports_summary(tmp_path: Path) -> None:
    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://www.bbc.com,BBC,news,false,\n"
        "https://www.reddit.com,Reddit,social,true,\n",
        encoding="utf-8",
    )

    result = runner.invoke(cli.app, ["validate-sites", "--sites-csv", str(sites_csv)])

    assert result.exit_code == 0
    assert "2 active sites" in result.output
    assert "news=1" in result.output
    assert "social=1" in result.output
    assert "mentor_inherited=1" in result.output


def test_cli_validate_sites_fails_for_placeholder(tmp_path: Path) -> None:
    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://example.com,Example,placeholder,false,delete before real run\n",
        encoding="utf-8",
    )

    result = runner.invoke(cli.app, ["validate-sites", "--sites-csv", str(sites_csv)])

    assert result.exit_code == 1
    assert "placeholder_url" in result.output
    assert "placeholder_category" in result.output


def test_cli_sample_readiness_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_build_sample_readiness(
        candidates_csv: Path,
        access_probe_csv: Path,
        consent_table_csv: Path,
    ) -> list[SimpleNamespace]:
        seen["candidates_csv"] = candidates_csv
        seen["access_probe_csv"] = access_probe_csv
        seen["consent_table_csv"] = consent_table_csv
        return [
            SimpleNamespace(readiness_status="pilot_ready"),
            SimpleNamespace(readiness_status="access_blocked"),
        ]

    def fake_export_sample_readiness_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        seen["out_csv"] = out_csv
        seen["rows"] = rows

    monkeypatch.setattr(cli, "build_sample_readiness", fake_build_sample_readiness)
    monkeypatch.setattr(cli, "export_sample_readiness_to_csv", fake_export_sample_readiness_to_csv)

    candidates_csv = tmp_path / "candidates.csv"
    access_probe_csv = tmp_path / "probe.csv"
    consent_table_csv = tmp_path / "consent.csv"
    out_csv = tmp_path / "readiness.csv"

    result = runner.invoke(
        cli.app,
        [
            "sample-readiness",
            "--candidates-csv",
            str(candidates_csv),
            "--access-probe-csv",
            str(access_probe_csv),
            "--consent-table-csv",
            str(consent_table_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen["candidates_csv"] == candidates_csv
    assert seen["access_probe_csv"] == access_probe_csv
    assert seen["consent_table_csv"] == [consent_table_csv]
    assert seen["out_csv"] == out_csv
    assert "2 sample readiness rows" in result.output
    assert "pilot_ready=1" in result.output
    assert "access_blocked=1" in result.output


def test_cli_sample_readiness_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_build_sample_readiness(
        candidates_csv: Path,
        access_probe_csv: Path,
        consent_table_csv: Path,
    ) -> list[SimpleNamespace]:
        seen["candidates_csv"] = candidates_csv
        seen["access_probe_csv"] = access_probe_csv
        seen["consent_table_csv"] = consent_table_csv
        return []

    def fake_export_sample_readiness_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        _ = rows
        seen["out_csv"] = out_csv

    monkeypatch.setattr(cli, "build_sample_readiness", fake_build_sample_readiness)
    monkeypatch.setattr(cli, "export_sample_readiness_to_csv", fake_export_sample_readiness_to_csv)

    result = runner.invoke(cli.app, ["sample-readiness"])

    assert result.exit_code == 0
    assert seen == {
        "candidates_csv": Path("data/deep_sample_candidates.csv"),
        "access_probe_csv": Path("data/access_probe_pilot_2026-05-30.csv"),
        "consent_table_csv": [
            Path("data/consent_table_smoke_2026-05-29.csv"),
            Path("data/consent_table_pilot_2026-05-30.csv"),
        ],
        "out_csv": Path("data/sample_readiness_pilot_2026-05-30.csv"),
    }


def test_cli_cmp_review_queue_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_queue(
        readiness_csv: Path,
        consent_table_csv: list[Path],
    ) -> list[SimpleNamespace]:
        seen["readiness_csv"] = readiness_csv
        seen["consent_table_csv"] = consent_table_csv
        return [
            SimpleNamespace(readiness_status="needs_cmp_review"),
            SimpleNamespace(readiness_status="needs_cmp_review"),
        ]

    def fake_export_cmp_review_queue_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        seen["out_csv"] = out_csv
        seen["rows"] = rows

    monkeypatch.setattr(cli, "build_cmp_review_queue", fake_build_cmp_review_queue)
    monkeypatch.setattr(cli, "export_cmp_review_queue_to_csv", fake_export_cmp_review_queue_to_csv)

    readiness_csv = tmp_path / "readiness.csv"
    consent_table_csv = tmp_path / "consent.csv"
    out_csv = tmp_path / "cmp_review_queue.csv"

    result = runner.invoke(
        cli.app,
        [
            "cmp-review-queue",
            "--readiness-csv",
            str(readiness_csv),
            "--consent-table-csv",
            str(consent_table_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen["readiness_csv"] == readiness_csv
    assert seen["consent_table_csv"] == [consent_table_csv]
    assert seen["out_csv"] == out_csv
    assert "2 CMP review rows" in result.output
    assert "needs_cmp_review=2" in result.output


def test_cli_cmp_review_queue_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_queue(
        readiness_csv: Path,
        consent_table_csv: list[Path],
    ) -> list[SimpleNamespace]:
        seen["readiness_csv"] = readiness_csv
        seen["consent_table_csv"] = consent_table_csv
        return []

    def fake_export_cmp_review_queue_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        _ = rows
        seen["out_csv"] = out_csv

    monkeypatch.setattr(cli, "build_cmp_review_queue", fake_build_cmp_review_queue)
    monkeypatch.setattr(cli, "export_cmp_review_queue_to_csv", fake_export_cmp_review_queue_to_csv)

    result = runner.invoke(cli.app, ["cmp-review-queue"])

    assert result.exit_code == 0
    assert seen == {
        "readiness_csv": Path("data/sample_readiness_pilot_2026-05-30.csv"),
        "consent_table_csv": [
            Path("data/consent_table_smoke_2026-05-29.csv"),
            Path("data/consent_table_pilot_2026-05-30.csv"),
        ],
        "out_csv": Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
    }


def test_cli_cmp_review_worksheet_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_worksheet(queue_csv: Path) -> list[SimpleNamespace]:
        seen["queue_csv"] = queue_csv
        return [
            SimpleNamespace(sample_decision=""),
            SimpleNamespace(sample_decision="keep_consent_sample"),
        ]

    def fake_export_cmp_review_worksheet_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        seen["out_csv"] = out_csv
        seen["rows"] = rows

    monkeypatch.setattr(cli, "build_cmp_review_worksheet", fake_build_cmp_review_worksheet)
    monkeypatch.setattr(
        cli,
        "export_cmp_review_worksheet_to_csv",
        fake_export_cmp_review_worksheet_to_csv,
    )

    queue_csv = tmp_path / "cmp_review_queue.csv"
    out_csv = tmp_path / "cmp_review_worksheet.csv"

    result = runner.invoke(
        cli.app,
        [
            "cmp-review-worksheet",
            "--queue-csv",
            str(queue_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen["queue_csv"] == queue_csv
    assert seen["out_csv"] == out_csv
    assert "2 CMP review worksheet rows" in result.output
    assert "pending_manual_decision=1" in result.output
    assert "keep_consent_sample=1" in result.output


def test_cli_cmp_review_worksheet_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_worksheet(queue_csv: Path) -> list[SimpleNamespace]:
        seen["queue_csv"] = queue_csv
        return []

    def fake_export_cmp_review_worksheet_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        _ = rows
        seen["out_csv"] = out_csv

    monkeypatch.setattr(cli, "build_cmp_review_worksheet", fake_build_cmp_review_worksheet)
    monkeypatch.setattr(
        cli,
        "export_cmp_review_worksheet_to_csv",
        fake_export_cmp_review_worksheet_to_csv,
    )

    result = runner.invoke(cli.app, ["cmp-review-worksheet"])

    assert result.exit_code == 0
    assert seen == {
        "queue_csv": Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
        "out_csv": Path("data/cmp_review_worksheet_pilot_2026-05-30.csv"),
    }


def test_cli_cmp_review_packet_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_cmp_review_packet(
        queue_csv: Path,
        out_dir: Path,
        *,
        project_root: Path = Path("."),
    ) -> dict[str, str | int]:
        seen["queue_csv"] = queue_csv
        seen["out_dir"] = out_dir
        seen["project_root"] = project_root
        return {
            "row_count": 2,
            "index_html": str(out_dir / "index.html"),
            "index_markdown": str(out_dir / "index.md"),
        }

    monkeypatch.setattr(cli, "export_cmp_review_packet", fake_export_cmp_review_packet)
    queue_csv = tmp_path / "cmp_review_queue.csv"
    out_dir = tmp_path / "packet"

    result = runner.invoke(
        cli.app,
        [
            "cmp-review-packet",
            "--queue-csv",
            str(queue_csv),
            "--out-dir",
            str(out_dir),
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "queue_csv": queue_csv,
        "out_dir": out_dir,
        "project_root": Path("."),
    }
    assert "Wrote 2 CMP review packet cards" in result.output
    assert str(out_dir / "index.html") in result.output


def test_cli_cmp_review_packet_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_cmp_review_packet(
        queue_csv: Path,
        out_dir: Path,
        *,
        project_root: Path = Path("."),
    ) -> dict[str, str | int]:
        seen["queue_csv"] = queue_csv
        seen["out_dir"] = out_dir
        seen["project_root"] = project_root
        return {
            "row_count": 0,
            "index_html": str(out_dir / "index.html"),
            "index_markdown": str(out_dir / "index.md"),
        }

    monkeypatch.setattr(cli, "export_cmp_review_packet", fake_export_cmp_review_packet)

    result = runner.invoke(cli.app, ["cmp-review-packet"])

    assert result.exit_code == 0
    assert seen == {
        "queue_csv": Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
        "out_dir": Path("data/cmp_review_packet_pilot_2026-05-30"),
        "project_root": Path("."),
    }


def test_cli_cmp_review_suggestions_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_suggestions(
        queue_csv: Path,
        *,
        project_root: Path = Path("."),
    ) -> list[SimpleNamespace]:
        seen["queue_csv"] = queue_csv
        seen["project_root"] = project_root
        return [
            SimpleNamespace(auto_suggested_decision="rerun_fresh_context"),
            SimpleNamespace(auto_suggested_decision="keep_no_banner_case"),
        ]

    def fake_export_cmp_review_suggestions_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        seen["out_csv"] = out_csv
        seen["rows"] = rows

    monkeypatch.setattr(cli, "build_cmp_review_suggestions", fake_build_cmp_review_suggestions)
    monkeypatch.setattr(
        cli,
        "export_cmp_review_suggestions_to_csv",
        fake_export_cmp_review_suggestions_to_csv,
    )
    queue_csv = tmp_path / "cmp_review_queue.csv"
    out_csv = tmp_path / "cmp_review_suggestions.csv"

    result = runner.invoke(
        cli.app,
        [
            "cmp-review-suggestions",
            "--queue-csv",
            str(queue_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen["queue_csv"] == queue_csv
    assert seen["project_root"] == Path(".")
    assert seen["out_csv"] == out_csv
    assert "2 CMP review suggestion rows" in result.output
    assert "rerun_fresh_context=1" in result.output
    assert "keep_no_banner_case=1" in result.output


def test_cli_cmp_review_suggestions_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_suggestions(
        queue_csv: Path,
        *,
        project_root: Path = Path("."),
    ) -> list[SimpleNamespace]:
        seen["queue_csv"] = queue_csv
        seen["project_root"] = project_root
        return []

    def fake_export_cmp_review_suggestions_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        _ = rows
        seen["out_csv"] = out_csv

    monkeypatch.setattr(cli, "build_cmp_review_suggestions", fake_build_cmp_review_suggestions)
    monkeypatch.setattr(
        cli,
        "export_cmp_review_suggestions_to_csv",
        fake_export_cmp_review_suggestions_to_csv,
    )

    result = runner.invoke(cli.app, ["cmp-review-suggestions"])

    assert result.exit_code == 0
    assert seen == {
        "queue_csv": Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
        "project_root": Path("."),
        "out_csv": Path("data/cmp_review_suggestions_pilot_2026-05-30.csv"),
    }


def test_cli_cmp_review_rerun_targets_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_cmp_review_rerun_targets(
        suggestions_csv: Path,
        out_csv: Path,
    ) -> int:
        seen["suggestions_csv"] = suggestions_csv
        seen["out_csv"] = out_csv
        return 7

    monkeypatch.setattr(cli, "export_cmp_review_rerun_targets", fake_export_cmp_review_rerun_targets)
    suggestions_csv = tmp_path / "suggestions.csv"
    out_csv = tmp_path / "targets.csv"

    result = runner.invoke(
        cli.app,
        [
            "cmp-review-rerun-targets",
            "--suggestions-csv",
            str(suggestions_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen == {"suggestions_csv": suggestions_csv, "out_csv": out_csv}
    assert "Wrote 7 CMP review rerun target rows" in result.output


def test_cli_cmp_review_rerun_targets_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_cmp_review_rerun_targets(
        suggestions_csv: Path,
        out_csv: Path,
    ) -> int:
        seen["suggestions_csv"] = suggestions_csv
        seen["out_csv"] = out_csv
        return 0

    monkeypatch.setattr(cli, "export_cmp_review_rerun_targets", fake_export_cmp_review_rerun_targets)

    result = runner.invoke(cli.app, ["cmp-review-rerun-targets"])

    assert result.exit_code == 0
    assert seen == {
        "suggestions_csv": Path("data/cmp_review_suggestions_pilot_2026-05-30.csv"),
        "out_csv": Path("data/cmp_review_rerun_targets_pilot_2026-05-30.csv"),
    }


def test_cli_cmp_review_decision_draft_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_decision_draft(
        queue_csv: Path,
        suggestions_csv: Path,
    ) -> list[SimpleNamespace]:
        seen["queue_csv"] = queue_csv
        seen["suggestions_csv"] = suggestions_csv
        return [
            SimpleNamespace(draft_decision="keep_no_banner_case"),
            SimpleNamespace(draft_decision="replace_candidate"),
        ]

    def fake_export_cmp_review_decision_draft_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        seen["out_csv"] = out_csv
        seen["rows"] = rows

    monkeypatch.setattr(
        cli,
        "build_cmp_review_decision_draft",
        fake_build_cmp_review_decision_draft,
    )
    monkeypatch.setattr(
        cli,
        "export_cmp_review_decision_draft_to_csv",
        fake_export_cmp_review_decision_draft_to_csv,
    )
    queue_csv = tmp_path / "queue.csv"
    suggestions_csv = tmp_path / "suggestions.csv"
    out_csv = tmp_path / "decision_draft.csv"

    result = runner.invoke(
        cli.app,
        [
            "cmp-review-decision-draft",
            "--queue-csv",
            str(queue_csv),
            "--suggestions-csv",
            str(suggestions_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen["queue_csv"] == queue_csv
    assert seen["suggestions_csv"] == suggestions_csv
    assert seen["out_csv"] == out_csv
    assert "2 CMP review decision draft rows" in result.output
    assert "keep_no_banner_case=1" in result.output
    assert "replace_candidate=1" in result.output


def test_cli_cmp_review_decision_draft_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_decision_draft(
        queue_csv: Path,
        suggestions_csv: Path,
    ) -> list[SimpleNamespace]:
        seen["queue_csv"] = queue_csv
        seen["suggestions_csv"] = suggestions_csv
        return []

    def fake_export_cmp_review_decision_draft_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        _ = rows
        seen["out_csv"] = out_csv

    monkeypatch.setattr(
        cli,
        "build_cmp_review_decision_draft",
        fake_build_cmp_review_decision_draft,
    )
    monkeypatch.setattr(
        cli,
        "export_cmp_review_decision_draft_to_csv",
        fake_export_cmp_review_decision_draft_to_csv,
    )

    result = runner.invoke(cli.app, ["cmp-review-decision-draft"])

    assert result.exit_code == 0
    assert seen == {
        "queue_csv": Path("data/cmp_review_queue_pilot_2026-05-30.csv"),
        "suggestions_csv": Path("data/cmp_review_suggestions_pilot_2026-05-30.csv"),
        "out_csv": Path("data/cmp_review_decision_draft_pilot_2026-05-30.csv"),
    }


def test_cli_cmp_review_confirmation_sheet_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_confirmation_sheet(draft_csv: Path) -> list[SimpleNamespace]:
        seen["draft_csv"] = draft_csv
        return [SimpleNamespace(confirmation_status="pending")]

    def fake_export_cmp_review_confirmation_sheet_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        seen["out_csv"] = out_csv
        seen["rows"] = rows

    monkeypatch.setattr(
        cli,
        "build_cmp_review_confirmation_sheet",
        fake_build_cmp_review_confirmation_sheet,
    )
    monkeypatch.setattr(
        cli,
        "export_cmp_review_confirmation_sheet_to_csv",
        fake_export_cmp_review_confirmation_sheet_to_csv,
    )

    draft_csv = tmp_path / "draft.csv"
    out_csv = tmp_path / "confirmation.csv"
    result = runner.invoke(
        cli.app,
        [
            "cmp-review-confirmation-sheet",
            "--draft-csv",
            str(draft_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen["draft_csv"] == draft_csv
    assert seen["out_csv"] == out_csv
    assert "1 CMP review confirmation rows" in result.output


def test_cli_cmp_review_apply_confirmations_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_apply_cmp_review_confirmations_to_worksheet(
        worksheet_csv: Path,
        confirmation_csv: Path,
        out_csv: Path,
    ) -> dict[str, int]:
        seen["worksheet_csv"] = worksheet_csv
        seen["confirmation_csv"] = confirmation_csv
        seen["out_csv"] = out_csv
        return {"applied": 2, "pending": 6}

    monkeypatch.setattr(
        cli,
        "apply_cmp_review_confirmations_to_worksheet",
        fake_apply_cmp_review_confirmations_to_worksheet,
    )

    worksheet_csv = tmp_path / "worksheet.csv"
    confirmation_csv = tmp_path / "confirmation.csv"
    out_csv = tmp_path / "worksheet_confirmed.csv"
    result = runner.invoke(
        cli.app,
        [
            "cmp-review-apply-confirmations",
            "--worksheet-csv",
            str(worksheet_csv),
            "--confirmation-csv",
            str(confirmation_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "worksheet_csv": worksheet_csv,
        "confirmation_csv": confirmation_csv,
        "out_csv": out_csv,
    }
    assert "applied=2" in result.output
    assert "pending=6" in result.output


def test_cli_cmp_review_confirmation_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_build_cmp_review_confirmation_sheet(draft_csv: Path) -> list[SimpleNamespace]:
        seen["draft_csv"] = draft_csv
        return []

    def fake_export_cmp_review_confirmation_sheet_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        _ = rows
        seen["confirmation_out_csv"] = out_csv

    def fake_apply_cmp_review_confirmations_to_worksheet(
        worksheet_csv: Path,
        confirmation_csv: Path,
        out_csv: Path,
    ) -> dict[str, int]:
        seen["worksheet_csv"] = worksheet_csv
        seen["confirmation_csv"] = confirmation_csv
        seen["worksheet_out_csv"] = out_csv
        return {}

    monkeypatch.setattr(
        cli,
        "build_cmp_review_confirmation_sheet",
        fake_build_cmp_review_confirmation_sheet,
    )
    monkeypatch.setattr(
        cli,
        "export_cmp_review_confirmation_sheet_to_csv",
        fake_export_cmp_review_confirmation_sheet_to_csv,
    )
    monkeypatch.setattr(
        cli,
        "apply_cmp_review_confirmations_to_worksheet",
        fake_apply_cmp_review_confirmations_to_worksheet,
    )

    sheet_result = runner.invoke(cli.app, ["cmp-review-confirmation-sheet"])
    apply_result = runner.invoke(cli.app, ["cmp-review-apply-confirmations"])

    assert sheet_result.exit_code == 0
    assert apply_result.exit_code == 0
    assert seen == {
        "draft_csv": Path("data/cmp_review_decision_draft_pilot_2026-05-30.csv"),
        "confirmation_out_csv": Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
        "worksheet_csv": Path("data/cmp_review_worksheet_pilot_2026-05-30.csv"),
        "confirmation_csv": Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
        "worksheet_out_csv": Path("data/cmp_review_worksheet_confirmed_pilot_2026-05-30.csv"),
    }


def test_cli_sample_lock_plan_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_build_sample_lock_plan(
        readiness_csv: Path,
        worksheet_csv: Path,
    ) -> list[SimpleNamespace]:
        seen["readiness_csv"] = readiness_csv
        seen["worksheet_csv"] = worksheet_csv
        return [
            SimpleNamespace(lock_status="provisionally_selected"),
            SimpleNamespace(lock_status="pending_manual_review"),
        ]

    def fake_export_sample_lock_plan_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        seen["out_csv"] = out_csv
        seen["rows"] = rows

    monkeypatch.setattr(cli, "build_sample_lock_plan", fake_build_sample_lock_plan)
    monkeypatch.setattr(cli, "export_sample_lock_plan_to_csv", fake_export_sample_lock_plan_to_csv)

    readiness_csv = tmp_path / "readiness.csv"
    worksheet_csv = tmp_path / "worksheet.csv"
    out_csv = tmp_path / "sample_lock_plan.csv"

    result = runner.invoke(
        cli.app,
        [
            "sample-lock-plan",
            "--readiness-csv",
            str(readiness_csv),
            "--worksheet-csv",
            str(worksheet_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen["readiness_csv"] == readiness_csv
    assert seen["worksheet_csv"] == worksheet_csv
    assert seen["out_csv"] == out_csv
    assert "2 sample lock rows" in result.output
    assert "provisionally_selected=1" in result.output
    assert "pending_manual_review=1" in result.output


def test_cli_sample_lock_plan_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_build_sample_lock_plan(
        readiness_csv: Path,
        worksheet_csv: Path,
    ) -> list[SimpleNamespace]:
        seen["readiness_csv"] = readiness_csv
        seen["worksheet_csv"] = worksheet_csv
        return []

    def fake_export_sample_lock_plan_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        _ = rows
        seen["out_csv"] = out_csv

    monkeypatch.setattr(cli, "build_sample_lock_plan", fake_build_sample_lock_plan)
    monkeypatch.setattr(cli, "export_sample_lock_plan_to_csv", fake_export_sample_lock_plan_to_csv)

    result = runner.invoke(cli.app, ["sample-lock-plan"])

    assert result.exit_code == 0
    assert seen == {
        "readiness_csv": Path("data/sample_readiness_pilot_2026-05-30.csv"),
        "worksheet_csv": Path("data/cmp_review_worksheet_pilot_2026-05-30.csv"),
        "out_csv": Path("data/sample_lock_plan_pilot_2026-05-30.csv"),
    }


def test_cli_sample_action_queues_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_sample_lock_queues(
        lock_plan_csv: Path,
        out_dir: Path,
    ) -> dict[str, int]:
        seen["lock_plan_csv"] = lock_plan_csv
        seen["out_dir"] = out_dir
        return {
            "weekly_capture_shortlist": 2,
            "manual_review_queue": 1,
        }

    monkeypatch.setattr(cli, "export_sample_lock_queues", fake_export_sample_lock_queues)

    lock_plan_csv = tmp_path / "sample_lock_plan.csv"
    out_dir = tmp_path / "queues"

    result = runner.invoke(
        cli.app,
        [
            "sample-action-queues",
            "--lock-plan-csv",
            str(lock_plan_csv),
            "--out-dir",
            str(out_dir),
        ],
    )

    assert result.exit_code == 0
    assert seen == {"lock_plan_csv": lock_plan_csv, "out_dir": out_dir}
    assert "weekly_capture_shortlist=2" in result.output
    assert "manual_review_queue=1" in result.output


def test_cli_sample_action_queues_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_sample_lock_queues(
        lock_plan_csv: Path,
        out_dir: Path,
    ) -> dict[str, int]:
        seen["lock_plan_csv"] = lock_plan_csv
        seen["out_dir"] = out_dir
        return {}

    monkeypatch.setattr(cli, "export_sample_lock_queues", fake_export_sample_lock_queues)

    result = runner.invoke(cli.app, ["sample-action-queues"])

    assert result.exit_code == 0
    assert seen == {
        "lock_plan_csv": Path("data/sample_lock_plan_pilot_2026-05-30.csv"),
        "out_dir": Path("data/sample_action_queues_pilot_2026-05-30"),
    }


def test_cli_sample_weekly_targets_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_weekly_targets_from_queues(
        queues_dir: Path,
        out_csv: Path,
    ) -> int:
        seen["queues_dir"] = queues_dir
        seen["out_csv"] = out_csv
        return 4

    monkeypatch.setattr(
        cli,
        "export_weekly_targets_from_queues",
        fake_export_weekly_targets_from_queues,
    )

    queues_dir = tmp_path / "queues"
    out_csv = tmp_path / "weekly_targets.csv"

    result = runner.invoke(
        cli.app,
        [
            "sample-weekly-targets",
            "--queues-dir",
            str(queues_dir),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen == {"queues_dir": queues_dir, "out_csv": out_csv}
    assert "Wrote 4 weekly target rows" in result.output


def test_cli_sample_weekly_targets_defaults_to_pilot_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_weekly_targets_from_queues(
        queues_dir: Path,
        out_csv: Path,
    ) -> int:
        seen["queues_dir"] = queues_dir
        seen["out_csv"] = out_csv
        return 0

    monkeypatch.setattr(
        cli,
        "export_weekly_targets_from_queues",
        fake_export_weekly_targets_from_queues,
    )

    result = runner.invoke(cli.app, ["sample-weekly-targets"])

    assert result.exit_code == 0
    assert seen == {
        "queues_dir": Path("data/sample_action_queues_pilot_2026-05-30"),
        "out_csv": Path("data/deep_sample_weekly_targets_pilot_2026-05-30.csv"),
    }


def test_cli_replacement_review_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_build_replacement_review(
        candidates_csv: Path,
        access_probe_csv: Path,
        consent_table_csv: Path,
    ) -> list[SimpleNamespace]:
        seen["candidates_csv"] = candidates_csv
        seen["access_probe_csv"] = access_probe_csv
        seen["consent_table_csv"] = consent_table_csv
        return [
            SimpleNamespace(replacement_status="verified_replacement"),
            SimpleNamespace(replacement_status="promising_reprobe"),
        ]

    def fake_export_replacement_review_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        seen["out_csv"] = out_csv
        seen["rows"] = rows

    monkeypatch.setattr(cli, "build_replacement_review", fake_build_replacement_review)
    monkeypatch.setattr(
        cli,
        "export_replacement_review_to_csv",
        fake_export_replacement_review_to_csv,
    )

    candidates_csv = tmp_path / "candidates.csv"
    access_probe_csv = tmp_path / "access_probe.csv"
    consent_table_csv = tmp_path / "consent_table.csv"
    out_csv = tmp_path / "replacement_review.csv"

    result = runner.invoke(
        cli.app,
        [
            "replacement-review",
            "--candidates-csv",
            str(candidates_csv),
            "--access-probe-csv",
            str(access_probe_csv),
            "--consent-table-csv",
            str(consent_table_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen["candidates_csv"] == candidates_csv
    assert seen["access_probe_csv"] == access_probe_csv
    assert seen["consent_table_csv"] == consent_table_csv
    assert seen["out_csv"] == out_csv
    assert "2 replacement review rows" in result.output
    assert "verified_replacement=1" in result.output
    assert "promising_reprobe=1" in result.output


def test_cli_replacement_review_defaults_to_batch2_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_build_replacement_review(
        candidates_csv: Path,
        access_probe_csv: Path,
        consent_table_csv: Path,
    ) -> list[SimpleNamespace]:
        seen["candidates_csv"] = candidates_csv
        seen["access_probe_csv"] = access_probe_csv
        seen["consent_table_csv"] = consent_table_csv
        return []

    def fake_export_replacement_review_to_csv(
        out_csv: Path,
        rows: list[SimpleNamespace],
    ) -> None:
        _ = rows
        seen["out_csv"] = out_csv

    monkeypatch.setattr(cli, "build_replacement_review", fake_build_replacement_review)
    monkeypatch.setattr(
        cli,
        "export_replacement_review_to_csv",
        fake_export_replacement_review_to_csv,
    )

    result = runner.invoke(cli.app, ["replacement-review"])

    assert result.exit_code == 0
    assert seen == {
        "candidates_csv": Path("data/replacement_candidates_batch2_2026-05-30.csv"),
        "access_probe_csv": Path("data/access_probe_replacements_batch2_2026-05-30.csv"),
        "consent_table_csv": Path("data/consent_table_replacements_batch2_2026-05-30.csv"),
        "out_csv": Path("data/replacement_review_batch2_2026-05-30.csv"),
    }


def test_cli_expanded_weekly_targets_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_expanded_weekly_targets(
        base_targets_csv: Path,
        replacement_review_csv: Path,
        out_csv: Path,
    ) -> int:
        seen["base_targets_csv"] = base_targets_csv
        seen["replacement_review_csv"] = replacement_review_csv
        seen["out_csv"] = out_csv
        return 5

    monkeypatch.setattr(
        cli,
        "export_expanded_weekly_targets",
        fake_export_expanded_weekly_targets,
    )

    base_targets_csv = tmp_path / "base_targets.csv"
    replacement_review_csv = tmp_path / "replacement_review.csv"
    out_csv = tmp_path / "expanded_targets.csv"

    result = runner.invoke(
        cli.app,
        [
            "expanded-weekly-targets",
            "--base-targets-csv",
            str(base_targets_csv),
            "--replacement-review-csv",
            str(replacement_review_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "base_targets_csv": base_targets_csv,
        "replacement_review_csv": replacement_review_csv,
        "out_csv": out_csv,
    }
    assert "Wrote 5 expanded weekly target rows" in result.output


def test_cli_expanded_weekly_targets_defaults_to_current_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_expanded_weekly_targets(
        base_targets_csv: Path,
        replacement_review_csv: Path,
        out_csv: Path,
    ) -> int:
        seen["base_targets_csv"] = base_targets_csv
        seen["replacement_review_csv"] = replacement_review_csv
        seen["out_csv"] = out_csv
        return 0

    monkeypatch.setattr(
        cli,
        "export_expanded_weekly_targets",
        fake_export_expanded_weekly_targets,
    )

    result = runner.invoke(cli.app, ["expanded-weekly-targets"])

    assert result.exit_code == 0
    assert seen == {
        "base_targets_csv": Path("data/deep_sample_weekly_targets_pilot_2026-05-30.csv"),
        "replacement_review_csv": Path("data/replacement_review_batch2_2026-05-30.csv"),
        "out_csv": Path("data/deep_sample_weekly_targets_expanded_2026-05-30.csv"),
    }


def test_cli_week2_capture_targets_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_week2_capture_targets(
        expanded_targets_csv: Path,
        out_csv: Path,
    ) -> int:
        seen["expanded_targets_csv"] = expanded_targets_csv
        seen["out_csv"] = out_csv
        return 5

    monkeypatch.setattr(cli, "export_week2_capture_targets", fake_export_week2_capture_targets)
    expanded_targets_csv = tmp_path / "expanded.csv"
    out_csv = tmp_path / "week2.csv"

    result = runner.invoke(
        cli.app,
        [
            "week2-capture-targets",
            "--expanded-targets-csv",
            str(expanded_targets_csv),
            "--out-csv",
            str(out_csv),
        ],
    )

    assert result.exit_code == 0
    assert seen == {"expanded_targets_csv": expanded_targets_csv, "out_csv": out_csv}
    assert "Wrote 5 Week 2 capture target rows" in result.output


def test_cli_week2_capture_targets_defaults_to_current_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_week2_capture_targets(
        expanded_targets_csv: Path,
        out_csv: Path,
    ) -> int:
        seen["expanded_targets_csv"] = expanded_targets_csv
        seen["out_csv"] = out_csv
        return 0

    monkeypatch.setattr(cli, "export_week2_capture_targets", fake_export_week2_capture_targets)

    result = runner.invoke(cli.app, ["week2-capture-targets"])

    assert result.exit_code == 0
    assert seen == {
        "expanded_targets_csv": Path("data/deep_sample_weekly_targets_expanded_2026-05-30.csv"),
        "out_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
    }


def test_cli_advisor_update_brief_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_weekly_advisor_brief(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        cmp_confirmation_csv: Path,
        manifest_json: Path,
        out_md: Path,
        title: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["manifest_json"] = manifest_json
        seen["out_md"] = out_md
        seen["title"] = title
        return "# Advisor update\n"

    monkeypatch.setattr(cli, "export_weekly_advisor_brief", fake_export_weekly_advisor_brief)

    result = runner.invoke(
        cli.app,
        [
            "advisor-update-brief",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--audit-summary-csv",
            str(tmp_path / "audit.csv"),
            "--longitudinal-summary-csv",
            str(tmp_path / "longitudinal.csv"),
            "--cmp-confirmation-csv",
            str(tmp_path / "confirmation.csv"),
            "--manifest-json",
            str(tmp_path / "manifest.json"),
            "--out-md",
            str(tmp_path / "brief.md"),
            "--title",
            "Custom Advisor Update",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "audit_summary_csv": tmp_path / "audit.csv",
        "longitudinal_summary_csv": tmp_path / "longitudinal.csv",
        "cmp_confirmation_csv": tmp_path / "confirmation.csv",
        "manifest_json": tmp_path / "manifest.json",
        "out_md": tmp_path / "brief.md",
        "title": "Custom Advisor Update",
    }
    assert "Wrote advisor update brief" in result.output


def test_cli_advisor_update_brief_defaults_to_week2_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_weekly_advisor_brief(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        cmp_confirmation_csv: Path,
        manifest_json: Path,
        out_md: Path,
        title: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["manifest_json"] = manifest_json
        seen["out_md"] = out_md
        seen["title"] = title
        return "# Advisor update\n"

    monkeypatch.setattr(cli, "export_weekly_advisor_brief", fake_export_weekly_advisor_brief)

    result = runner.invoke(cli.app, ["advisor-update-brief"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "audit_summary_csv": Path("data/research_package/audit_report_summary.csv"),
        "longitudinal_summary_csv": Path("data/research_package/longitudinal_summary.csv"),
        "cmp_confirmation_csv": Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
        "manifest_json": Path("data/research_package/research_manifest.json"),
        "out_md": Path("docs/research/week2_advisor_update_2026-06-06.md"),
        "title": "Week 2 Advisor Update, 2026-06-06",
    }


def test_cli_week2_sanity_check_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_week2_sanity_check(
        *,
        targets_csv: Path,
        consent_table_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        out_md: Path,
        cohort: str,
        week_of: str,
        title: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["consent_table_csv"] = consent_table_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["out_md"] = out_md
        seen["cohort"] = cohort
        seen["week_of"] = week_of
        seen["title"] = title
        return "# sanity\n"

    monkeypatch.setattr(cli, "export_week2_sanity_check", fake_export_week2_sanity_check)

    result = runner.invoke(
        cli.app,
        [
            "week2-sanity-check",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--consent-table-csv",
            str(tmp_path / "consent.csv"),
            "--audit-summary-csv",
            str(tmp_path / "audit.csv"),
            "--longitudinal-summary-csv",
            str(tmp_path / "longitudinal.csv"),
            "--out-md",
            str(tmp_path / "sanity.md"),
            "--cohort",
            "week2-test",
            "--week-of",
            "2026-06-06",
            "--title",
            "Custom Sanity",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "consent_table_csv": tmp_path / "consent.csv",
        "audit_summary_csv": tmp_path / "audit.csv",
        "longitudinal_summary_csv": tmp_path / "longitudinal.csv",
        "out_md": tmp_path / "sanity.md",
        "cohort": "week2-test",
        "week_of": "2026-06-06",
        "title": "Custom Sanity",
    }
    assert "Wrote Week 2 sanity check" in result.output


def test_cli_week2_sanity_check_defaults_to_week2_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_week2_sanity_check(
        *,
        targets_csv: Path,
        consent_table_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        out_md: Path,
        cohort: str,
        week_of: str,
        title: str,
    ) -> str:
        seen["targets_csv"] = targets_csv
        seen["consent_table_csv"] = consent_table_csv
        seen["audit_summary_csv"] = audit_summary_csv
        seen["longitudinal_summary_csv"] = longitudinal_summary_csv
        seen["out_md"] = out_md
        seen["cohort"] = cohort
        seen["week_of"] = week_of
        seen["title"] = title
        return "# sanity\n"

    monkeypatch.setattr(cli, "export_week2_sanity_check", fake_export_week2_sanity_check)

    result = runner.invoke(cli.app, ["week2-sanity-check"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "consent_table_csv": Path("data/consent_table_pilot_2026-05-30.csv"),
        "audit_summary_csv": Path("data/research_package/audit_report_summary.csv"),
        "longitudinal_summary_csv": Path("data/research_package/longitudinal_summary.csv"),
        "out_md": Path("docs/research/week2_sanity_check_2026-06-06.md"),
        "cohort": "week2-2026-06-06",
        "week_of": "2026-06-06",
        "title": "Week 2 Capture Sanity Check, 2026-06-06",
    }


def test_cli_checkin_index_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_checkin_index(
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
        seen["out_md"] = out_md
        seen["title"] = title
        seen["advisor_brief"] = advisor_brief
        seen["sanity_check"] = sanity_check
        seen["capture_checklist"] = capture_checklist
        seen["cycle_report"] = cycle_report
        seen["runbook"] = runbook
        seen["sample_plan"] = sample_plan
        seen["cmp_confirmation_sheet"] = cmp_confirmation_sheet
        seen["cmp_packet"] = cmp_packet
        seen["research_package_dir"] = research_package_dir
        seen["research_manifest"] = research_manifest
        return "# index\n"

    monkeypatch.setattr(cli, "export_checkin_index", fake_export_checkin_index)

    result = runner.invoke(
        cli.app,
        [
            "checkin-index",
            "--out-md",
            str(tmp_path / "index.md"),
            "--title",
            "Custom Index",
            "--advisor-brief",
            str(tmp_path / "advisor.md"),
            "--sanity-check",
            str(tmp_path / "sanity.md"),
            "--capture-checklist",
            str(tmp_path / "checklist.md"),
            "--cycle-report",
            str(tmp_path / "cycle.md"),
            "--runbook",
            str(tmp_path / "runbook.md"),
            "--sample-plan",
            str(tmp_path / "sample.md"),
            "--cmp-confirmation-sheet",
            str(tmp_path / "confirm.csv"),
            "--cmp-packet",
            str(tmp_path / "packet.html"),
            "--research-package-dir",
            str(tmp_path / "package"),
            "--research-manifest",
            str(tmp_path / "manifest.json"),
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "out_md": tmp_path / "index.md",
        "title": "Custom Index",
        "advisor_brief": tmp_path / "advisor.md",
        "sanity_check": tmp_path / "sanity.md",
        "capture_checklist": tmp_path / "checklist.md",
        "cycle_report": tmp_path / "cycle.md",
        "runbook": tmp_path / "runbook.md",
        "sample_plan": tmp_path / "sample.md",
        "cmp_confirmation_sheet": tmp_path / "confirm.csv",
        "cmp_packet": tmp_path / "packet.html",
        "research_package_dir": tmp_path / "package",
        "research_manifest": tmp_path / "manifest.json",
    }
    assert "Wrote check-in index" in result.output


def test_cli_checkin_index_defaults_to_week2_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_checkin_index(
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
        seen["out_md"] = out_md
        seen["title"] = title
        seen["advisor_brief"] = advisor_brief
        seen["sanity_check"] = sanity_check
        seen["capture_checklist"] = capture_checklist
        seen["cycle_report"] = cycle_report
        seen["runbook"] = runbook
        seen["sample_plan"] = sample_plan
        seen["cmp_confirmation_sheet"] = cmp_confirmation_sheet
        seen["cmp_packet"] = cmp_packet
        seen["research_package_dir"] = research_package_dir
        seen["research_manifest"] = research_manifest
        return "# index\n"

    monkeypatch.setattr(cli, "export_checkin_index", fake_export_checkin_index)

    result = runner.invoke(cli.app, ["checkin-index"])

    assert result.exit_code == 0
    assert seen == {
        "out_md": Path("docs/research/week2_checkin_index_2026-06-06.md"),
        "title": "Week 2 Advisor Check-in Index, 2026-06-06",
        "advisor_brief": Path("docs/research/week2_advisor_update_2026-06-06.md"),
        "sanity_check": Path("docs/research/week2_sanity_check_2026-06-06.md"),
        "capture_checklist": Path(
            "docs/research/week2_capture_day_checklist_2026-06-06.md"
        ),
        "cycle_report": Path("docs/research/week2_cycle_report_2026-06-06.md"),
        "runbook": Path("docs/research/week2_execution_runbook_2026-06-06.md"),
        "sample_plan": Path("docs/research/week2_sample_plan_2026-05-30.md"),
        "cmp_confirmation_sheet": Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
        "cmp_packet": Path("data/cmp_review_packet_pilot_2026-05-30/index.html"),
        "research_package_dir": Path("data/research_package"),
        "research_manifest": Path("data/research_package/research_manifest.json"),
    }


def test_cli_week2_capture_checklist_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_week2_capture_checklist(
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
        seen["out_md"] = out_md
        seen["title"] = title
        seen["week_of"] = week_of
        seen["cohort"] = cohort
        seen["expected_target_count"] = expected_target_count
        seen["targets_csv"] = targets_csv
        seen["consent_table_csv"] = consent_table_csv
        seen["preflight_check"] = preflight_check
        seen["cycle_report"] = cycle_report
        seen["refresh_report"] = refresh_report
        seen["sanity_check"] = sanity_check
        seen["checkin_index"] = checkin_index
        seen["advisor_brief"] = advisor_brief
        return "# checklist\n"

    monkeypatch.setattr(
        cli,
        "export_week2_capture_checklist",
        fake_export_week2_capture_checklist,
    )

    result = runner.invoke(
        cli.app,
        [
            "week2-capture-checklist",
            "--out-md",
            str(tmp_path / "checklist.md"),
            "--title",
            "Custom Checklist",
            "--week-of",
            "2026-06-13",
            "--cohort",
            "week3",
            "--expected-target-count",
            "6",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--consent-table-csv",
            str(tmp_path / "consent.csv"),
            "--preflight-check",
            str(tmp_path / "preflight.md"),
            "--cycle-report",
            str(tmp_path / "cycle.md"),
            "--refresh-report",
            str(tmp_path / "refresh.md"),
            "--sanity-check",
            str(tmp_path / "sanity.md"),
            "--checkin-index",
            str(tmp_path / "index.md"),
            "--advisor-brief",
            str(tmp_path / "advisor.md"),
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "out_md": tmp_path / "checklist.md",
        "title": "Custom Checklist",
        "week_of": "2026-06-13",
        "cohort": "week3",
        "expected_target_count": 6,
        "targets_csv": tmp_path / "targets.csv",
        "consent_table_csv": tmp_path / "consent.csv",
        "preflight_check": tmp_path / "preflight.md",
        "cycle_report": tmp_path / "cycle.md",
        "refresh_report": tmp_path / "refresh.md",
        "sanity_check": tmp_path / "sanity.md",
        "checkin_index": tmp_path / "index.md",
        "advisor_brief": tmp_path / "advisor.md",
    }
    assert "Wrote Week 2 capture checklist" in result.output


def test_cli_week2_capture_checklist_defaults_to_week2_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_week2_capture_checklist(**kwargs: Any) -> str:
        seen.update(kwargs)
        return "# checklist\n"

    monkeypatch.setattr(
        cli,
        "export_week2_capture_checklist",
        fake_export_week2_capture_checklist,
    )

    result = runner.invoke(cli.app, ["week2-capture-checklist"])

    assert result.exit_code == 0
    assert seen == {
        "out_md": Path("docs/research/week2_capture_day_checklist_2026-06-06.md"),
        "title": "Week 2 Capture-Day Checklist, 2026-06-06",
        "week_of": "2026-06-06",
        "cohort": "week2-2026-06-06",
        "expected_target_count": 5,
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "consent_table_csv": Path("data/consent_table_pilot_2026-05-30.csv"),
        "preflight_check": Path("docs/research/week2_preflight_check_2026-06-06.md"),
        "cycle_report": Path("docs/research/week2_cycle_report_2026-06-06.md"),
        "refresh_report": Path("docs/research/week2_refresh_report_2026-06-06.md"),
        "sanity_check": Path("docs/research/week2_sanity_check_2026-06-06.md"),
        "checkin_index": Path("docs/research/week2_checkin_index_2026-06-06.md"),
        "advisor_brief": Path("docs/research/week2_advisor_update_2026-06-06.md"),
    }


def test_cli_week2_preflight_check_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_week2_preflight_check(
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
        seen["targets_csv"] = targets_csv
        seen["sanity_check_md"] = sanity_check_md
        seen["advisor_brief_md"] = advisor_brief_md
        seen["checkin_index_md"] = checkin_index_md
        seen["runbook_md"] = runbook_md
        seen["research_manifest_json"] = research_manifest_json
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["cmp_packet_html"] = cmp_packet_html
        seen["out_md"] = out_md
        seen["title"] = title
        seen["expected_target_count"] = expected_target_count
        return "# preflight\n"

    monkeypatch.setattr(
        cli,
        "export_week2_preflight_check",
        fake_export_week2_preflight_check,
    )

    result = runner.invoke(
        cli.app,
        [
            "week2-preflight-check",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--sanity-check-md",
            str(tmp_path / "sanity.md"),
            "--advisor-brief-md",
            str(tmp_path / "advisor.md"),
            "--checkin-index-md",
            str(tmp_path / "index.md"),
            "--runbook-md",
            str(tmp_path / "runbook.md"),
            "--research-manifest-json",
            str(tmp_path / "manifest.json"),
            "--cmp-confirmation-csv",
            str(tmp_path / "confirmation.csv"),
            "--cmp-packet-html",
            str(tmp_path / "packet.html"),
            "--out-md",
            str(tmp_path / "preflight.md"),
            "--title",
            "Custom Preflight",
            "--expected-target-count",
            "7",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "sanity_check_md": tmp_path / "sanity.md",
        "advisor_brief_md": tmp_path / "advisor.md",
        "checkin_index_md": tmp_path / "index.md",
        "runbook_md": tmp_path / "runbook.md",
        "research_manifest_json": tmp_path / "manifest.json",
        "cmp_confirmation_csv": tmp_path / "confirmation.csv",
        "cmp_packet_html": tmp_path / "packet.html",
        "out_md": tmp_path / "preflight.md",
        "title": "Custom Preflight",
        "expected_target_count": 7,
    }
    assert "Wrote Week 2 preflight check" in result.output


def test_cli_week2_preflight_check_defaults_to_week2_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_export_week2_preflight_check(
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
        seen["targets_csv"] = targets_csv
        seen["sanity_check_md"] = sanity_check_md
        seen["advisor_brief_md"] = advisor_brief_md
        seen["checkin_index_md"] = checkin_index_md
        seen["runbook_md"] = runbook_md
        seen["research_manifest_json"] = research_manifest_json
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["cmp_packet_html"] = cmp_packet_html
        seen["out_md"] = out_md
        seen["title"] = title
        seen["expected_target_count"] = expected_target_count
        return "# preflight\n"

    monkeypatch.setattr(
        cli,
        "export_week2_preflight_check",
        fake_export_week2_preflight_check,
    )

    result = runner.invoke(cli.app, ["week2-preflight-check"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "sanity_check_md": Path("docs/research/week2_sanity_check_2026-06-06.md"),
        "advisor_brief_md": Path("docs/research/week2_advisor_update_2026-06-06.md"),
        "checkin_index_md": Path("docs/research/week2_checkin_index_2026-06-06.md"),
        "runbook_md": Path("docs/research/week2_execution_runbook_2026-06-06.md"),
        "research_manifest_json": Path("data/research_package/research_manifest.json"),
        "cmp_confirmation_csv": Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
        "cmp_packet_html": Path("data/cmp_review_packet_pilot_2026-05-30/index.html"),
        "out_md": Path("docs/research/week2_preflight_check_2026-06-06.md"),
        "title": "Week 2 Preflight Check, 2026-06-06",
        "expected_target_count": 5,
    }


def test_cli_week2_refresh_outputs_invokes_orchestrator(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_refresh_week2_outputs(
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
        results_tables_md: Path,
        paper_skeleton_md: Path,
        figure_plan_md: Path,
        writing_pack_md: Path,
        claim_register_md: Path,
        poster_plan_md: Path,
        preflight_check_md: Path,
        refresh_report_md: Path,
        cycle_report_md: Path,
        cohort: str,
        week_of: str,
        expected_target_count: int,
        limit: int,
    ) -> dict[str, Any]:
        seen["targets_csv"] = targets_csv
        seen["consent_table_csv"] = consent_table_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["cmp_packet_html"] = cmp_packet_html
        seen["runbook_md"] = runbook_md
        seen["sample_plan_md"] = sample_plan_md
        seen["research_package_dir"] = research_package_dir
        seen["advisor_brief_md"] = advisor_brief_md
        seen["sanity_check_md"] = sanity_check_md
        seen["checkin_index_md"] = checkin_index_md
        seen["capture_checklist_md"] = capture_checklist_md
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["figure_plan_md"] = figure_plan_md
        seen["writing_pack_md"] = writing_pack_md
        seen["claim_register_md"] = claim_register_md
        seen["poster_plan_md"] = poster_plan_md
        seen["preflight_check_md"] = preflight_check_md
        seen["refresh_report_md"] = refresh_report_md
        seen["cycle_report_md"] = cycle_report_md
        seen["cohort"] = cohort
        seen["week_of"] = week_of
        seen["expected_target_count"] = expected_target_count
        seen["limit"] = limit
        return {
            "audit_report_count": 42,
            "weekly_summary_count": 17,
            "sanity_status": "ready",
            "preflight_status": "ready_for_capture",
        }

    monkeypatch.setattr(cli, "refresh_week2_outputs", fake_refresh_week2_outputs)

    result = runner.invoke(
        cli.app,
        [
            "week2-refresh-outputs",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--consent-table-csv",
            str(tmp_path / "consent.csv"),
            "--cmp-confirmation-csv",
            str(tmp_path / "confirmation.csv"),
            "--cmp-packet-html",
            str(tmp_path / "packet.html"),
            "--runbook-md",
            str(tmp_path / "runbook.md"),
            "--sample-plan-md",
            str(tmp_path / "sample.md"),
            "--research-package-dir",
            str(tmp_path / "package"),
            "--advisor-brief-md",
            str(tmp_path / "advisor.md"),
            "--sanity-check-md",
            str(tmp_path / "sanity.md"),
            "--checkin-index-md",
            str(tmp_path / "index.md"),
            "--capture-checklist-md",
            str(tmp_path / "checklist.md"),
            "--results-tables-md",
            str(tmp_path / "results_tables.md"),
            "--paper-skeleton-md",
            str(tmp_path / "paper_skeleton.md"),
            "--figure-plan-md",
            str(tmp_path / "figure_plan.md"),
            "--writing-pack-md",
            str(tmp_path / "writing_pack.md"),
            "--claim-register-md",
            str(tmp_path / "claim_register.md"),
            "--poster-plan-md",
            str(tmp_path / "poster_plan.md"),
            "--preflight-check-md",
            str(tmp_path / "preflight.md"),
            "--refresh-report-md",
            str(tmp_path / "refresh.md"),
            "--cycle-report-md",
            str(tmp_path / "cycle.md"),
            "--cohort",
            "custom-cohort",
            "--week-of",
            "2026-06-13",
            "--expected-target-count",
            "7",
            "--limit",
            "321",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "consent_table_csv": tmp_path / "consent.csv",
        "cmp_confirmation_csv": tmp_path / "confirmation.csv",
        "cmp_packet_html": tmp_path / "packet.html",
        "runbook_md": tmp_path / "runbook.md",
        "sample_plan_md": tmp_path / "sample.md",
        "research_package_dir": tmp_path / "package",
        "advisor_brief_md": tmp_path / "advisor.md",
        "sanity_check_md": tmp_path / "sanity.md",
        "checkin_index_md": tmp_path / "index.md",
        "capture_checklist_md": tmp_path / "checklist.md",
        "results_tables_md": tmp_path / "results_tables.md",
        "paper_skeleton_md": tmp_path / "paper_skeleton.md",
        "figure_plan_md": tmp_path / "figure_plan.md",
        "writing_pack_md": tmp_path / "writing_pack.md",
        "claim_register_md": tmp_path / "claim_register.md",
        "poster_plan_md": tmp_path / "poster_plan.md",
        "preflight_check_md": tmp_path / "preflight.md",
        "refresh_report_md": tmp_path / "refresh.md",
        "cycle_report_md": tmp_path / "cycle.md",
        "cohort": "custom-cohort",
        "week_of": "2026-06-13",
        "expected_target_count": 7,
        "limit": 321,
    }
    assert "Refreshed Week 2 outputs" in result.output
    assert "42 reports" in result.output
    assert "17 weekly summaries" in result.output


def test_cli_week2_refresh_outputs_defaults_to_week2_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def fake_refresh_week2_outputs(
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
        results_tables_md: Path,
        paper_skeleton_md: Path,
        figure_plan_md: Path,
        writing_pack_md: Path,
        claim_register_md: Path,
        poster_plan_md: Path,
        preflight_check_md: Path,
        refresh_report_md: Path,
        cycle_report_md: Path,
        cohort: str,
        week_of: str,
        expected_target_count: int,
        limit: int,
    ) -> dict[str, Any]:
        seen["targets_csv"] = targets_csv
        seen["consent_table_csv"] = consent_table_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["cmp_packet_html"] = cmp_packet_html
        seen["runbook_md"] = runbook_md
        seen["sample_plan_md"] = sample_plan_md
        seen["research_package_dir"] = research_package_dir
        seen["advisor_brief_md"] = advisor_brief_md
        seen["sanity_check_md"] = sanity_check_md
        seen["checkin_index_md"] = checkin_index_md
        seen["capture_checklist_md"] = capture_checklist_md
        seen["results_tables_md"] = results_tables_md
        seen["paper_skeleton_md"] = paper_skeleton_md
        seen["figure_plan_md"] = figure_plan_md
        seen["writing_pack_md"] = writing_pack_md
        seen["claim_register_md"] = claim_register_md
        seen["poster_plan_md"] = poster_plan_md
        seen["preflight_check_md"] = preflight_check_md
        seen["refresh_report_md"] = refresh_report_md
        seen["cycle_report_md"] = cycle_report_md
        seen["cohort"] = cohort
        seen["week_of"] = week_of
        seen["expected_target_count"] = expected_target_count
        seen["limit"] = limit
        return {
            "audit_report_count": 0,
            "weekly_summary_count": 0,
            "sanity_status": "pending_capture",
            "preflight_status": "ready_for_capture",
        }

    monkeypatch.setattr(cli, "refresh_week2_outputs", fake_refresh_week2_outputs)

    result = runner.invoke(cli.app, ["week2-refresh-outputs"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "consent_table_csv": Path("data/consent_table_pilot_2026-05-30.csv"),
        "cmp_confirmation_csv": Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
        "cmp_packet_html": Path("data/cmp_review_packet_pilot_2026-05-30/index.html"),
        "runbook_md": Path("docs/research/week2_execution_runbook_2026-06-06.md"),
        "sample_plan_md": Path("docs/research/week2_sample_plan_2026-05-30.md"),
        "research_package_dir": Path("data/research_package"),
        "advisor_brief_md": Path("docs/research/week2_advisor_update_2026-06-06.md"),
        "sanity_check_md": Path("docs/research/week2_sanity_check_2026-06-06.md"),
        "checkin_index_md": Path("docs/research/week2_checkin_index_2026-06-06.md"),
        "capture_checklist_md": Path(
            "docs/research/week2_capture_day_checklist_2026-06-06.md"
        ),
        "results_tables_md": Path("docs/research/ssrp_results_tables_2026-06-06.md"),
        "paper_skeleton_md": Path("docs/research/ssrp_paper_skeleton_2026-06-06.md"),
        "figure_plan_md": Path("docs/research/ssrp_figure_plan_2026-06-06.md"),
        "writing_pack_md": Path("docs/research/ssrp_writing_pack_2026-06-06.md"),
        "claim_register_md": Path("docs/research/ssrp_claim_register_2026-06-06.md"),
        "poster_plan_md": Path("docs/research/ssrp_poster_plan_2026-06-06.md"),
        "preflight_check_md": Path("docs/research/week2_preflight_check_2026-06-06.md"),
        "refresh_report_md": Path("docs/research/week2_refresh_report_2026-06-06.md"),
        "cycle_report_md": Path("docs/research/week2_cycle_report_2026-06-06.md"),
        "cohort": "week2-2026-06-06",
        "week_of": "2026-06-06",
        "expected_target_count": 5,
        "limit": 500,
    }


def test_cli_week2_cycle_invokes_orchestrator(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    async def fake_run_week2_cycle(
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
        run_date: str | None,
        expected_target_count: int,
        limit: int,
        force: bool,
        allow_early: bool,
        dry_run: bool,
    ) -> dict[str, Any]:
        seen["targets_csv"] = targets_csv
        seen["consent_table_csv"] = consent_table_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["cmp_packet_html"] = cmp_packet_html
        seen["runbook_md"] = runbook_md
        seen["sample_plan_md"] = sample_plan_md
        seen["research_package_dir"] = research_package_dir
        seen["advisor_brief_md"] = advisor_brief_md
        seen["sanity_check_md"] = sanity_check_md
        seen["checkin_index_md"] = checkin_index_md
        seen["capture_checklist_md"] = capture_checklist_md
        seen["preflight_check_md"] = preflight_check_md
        seen["refresh_report_md"] = refresh_report_md
        seen["cycle_report_md"] = cycle_report_md
        seen["cohort"] = cohort
        seen["week_of"] = week_of
        seen["run_date"] = run_date
        seen["expected_target_count"] = expected_target_count
        seen["limit"] = limit
        seen["force"] = force
        seen["allow_early"] = allow_early
        seen["dry_run"] = dry_run
        return {
            "preflight_status": "ready_for_capture",
            "capture_status": "dry_run",
            "audit_report_count": 42,
            "weekly_summary_count": 17,
            "sanity_status": "ready",
            "post_refresh_preflight_status": "not_run",
        }

    monkeypatch.setattr(cli, "run_week2_cycle", fake_run_week2_cycle)

    result = runner.invoke(
        cli.app,
        [
            "week2-cycle",
            "--targets-csv",
            str(tmp_path / "targets.csv"),
            "--consent-table-csv",
            str(tmp_path / "consent.csv"),
            "--cmp-confirmation-csv",
            str(tmp_path / "confirmation.csv"),
            "--cmp-packet-html",
            str(tmp_path / "packet.html"),
            "--runbook-md",
            str(tmp_path / "runbook.md"),
            "--sample-plan-md",
            str(tmp_path / "sample.md"),
            "--research-package-dir",
            str(tmp_path / "package"),
            "--advisor-brief-md",
            str(tmp_path / "advisor.md"),
            "--sanity-check-md",
            str(tmp_path / "sanity.md"),
            "--checkin-index-md",
            str(tmp_path / "index.md"),
            "--capture-checklist-md",
            str(tmp_path / "checklist.md"),
            "--preflight-check-md",
            str(tmp_path / "preflight.md"),
            "--refresh-report-md",
            str(tmp_path / "refresh.md"),
            "--cycle-report-md",
            str(tmp_path / "cycle.md"),
            "--cohort",
            "custom-cohort",
            "--week-of",
            "2026-06-13",
            "--run-date",
            "2026-06-13",
            "--expected-target-count",
            "7",
            "--limit",
            "321",
            "--force",
            "--allow-early",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": tmp_path / "targets.csv",
        "consent_table_csv": tmp_path / "consent.csv",
        "cmp_confirmation_csv": tmp_path / "confirmation.csv",
        "cmp_packet_html": tmp_path / "packet.html",
        "runbook_md": tmp_path / "runbook.md",
        "sample_plan_md": tmp_path / "sample.md",
        "research_package_dir": tmp_path / "package",
        "advisor_brief_md": tmp_path / "advisor.md",
        "sanity_check_md": tmp_path / "sanity.md",
        "checkin_index_md": tmp_path / "index.md",
        "capture_checklist_md": tmp_path / "checklist.md",
        "preflight_check_md": tmp_path / "preflight.md",
        "refresh_report_md": tmp_path / "refresh.md",
        "cycle_report_md": tmp_path / "cycle.md",
        "cohort": "custom-cohort",
        "week_of": "2026-06-13",
        "run_date": "2026-06-13",
        "expected_target_count": 7,
        "limit": 321,
        "force": True,
        "allow_early": True,
        "dry_run": True,
    }
    assert "Dry-ran Week 2 cycle" in result.output
    assert "42 reports" in result.output
    assert "preflight=ready_for_capture" in result.output


def test_cli_week2_cycle_defaults_to_week2_artifacts(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    async def fake_run_week2_cycle(
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
        run_date: str | None,
        expected_target_count: int,
        limit: int,
        force: bool,
        allow_early: bool,
        dry_run: bool,
    ) -> dict[str, Any]:
        seen["targets_csv"] = targets_csv
        seen["consent_table_csv"] = consent_table_csv
        seen["cmp_confirmation_csv"] = cmp_confirmation_csv
        seen["cmp_packet_html"] = cmp_packet_html
        seen["runbook_md"] = runbook_md
        seen["sample_plan_md"] = sample_plan_md
        seen["research_package_dir"] = research_package_dir
        seen["advisor_brief_md"] = advisor_brief_md
        seen["sanity_check_md"] = sanity_check_md
        seen["checkin_index_md"] = checkin_index_md
        seen["capture_checklist_md"] = capture_checklist_md
        seen["preflight_check_md"] = preflight_check_md
        seen["refresh_report_md"] = refresh_report_md
        seen["cycle_report_md"] = cycle_report_md
        seen["cohort"] = cohort
        seen["week_of"] = week_of
        seen["run_date"] = run_date
        seen["expected_target_count"] = expected_target_count
        seen["limit"] = limit
        seen["force"] = force
        seen["allow_early"] = allow_early
        seen["dry_run"] = dry_run
        return {
            "capture_status": "completed",
            "audit_report_count": 0,
            "weekly_summary_count": 0,
            "sanity_status": "pending_capture",
            "post_refresh_preflight_status": "ready_for_capture",
        }

    monkeypatch.setattr(cli, "run_week2_cycle", fake_run_week2_cycle)

    result = runner.invoke(cli.app, ["week2-cycle"])

    assert result.exit_code == 0
    assert seen == {
        "targets_csv": Path("data/week2_deep_sample_targets_2026-06-06.csv"),
        "consent_table_csv": Path("data/consent_table_pilot_2026-05-30.csv"),
        "cmp_confirmation_csv": Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
        "cmp_packet_html": Path("data/cmp_review_packet_pilot_2026-05-30/index.html"),
        "runbook_md": Path("docs/research/week2_execution_runbook_2026-06-06.md"),
        "sample_plan_md": Path("docs/research/week2_sample_plan_2026-05-30.md"),
        "research_package_dir": Path("data/research_package"),
        "advisor_brief_md": Path("docs/research/week2_advisor_update_2026-06-06.md"),
        "sanity_check_md": Path("docs/research/week2_sanity_check_2026-06-06.md"),
        "checkin_index_md": Path("docs/research/week2_checkin_index_2026-06-06.md"),
        "capture_checklist_md": Path(
            "docs/research/week2_capture_day_checklist_2026-06-06.md"
        ),
        "preflight_check_md": Path("docs/research/week2_preflight_check_2026-06-06.md"),
        "refresh_report_md": Path("docs/research/week2_refresh_report_2026-06-06.md"),
        "cycle_report_md": Path("docs/research/week2_cycle_report_2026-06-06.md"),
        "cohort": "week2-2026-06-06",
        "week_of": "2026-06-06",
        "run_date": None,
        "expected_target_count": 5,
        "limit": 500,
        "force": False,
        "allow_early": False,
        "dry_run": False,
    }


def test_cli_week2_cycle_reports_schedule_guard(monkeypatch) -> None:
    async def fake_run_week2_cycle(**kwargs: Any) -> dict[str, Any]:
        assert kwargs["run_date"] is None
        assert kwargs["allow_early"] is False
        raise RuntimeError(
            "Week 2 run date 2026-05-30 is before scheduled week 2026-06-06"
        )

    monkeypatch.setattr(cli, "run_week2_cycle", fake_run_week2_cycle)

    result = runner.invoke(cli.app, ["week2-cycle"])

    assert result.exit_code == 1
    assert "before scheduled week 2026-06-06" in result.output


def test_cli_export_research_package_invokes_exporter(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    def fake_export_research_package(out_dir: Path, *, limit: int) -> dict[str, Any]:
        seen["out_dir"] = out_dir
        seen["limit"] = limit
        return {
            "audit_report_count": 3,
            "weekly_summary_count": 2,
            "files": {
                "audit_report_summary": "audit_report_summary.csv",
                "longitudinal_summary": "longitudinal_summary.csv",
            },
        }

    monkeypatch.setattr(cli, "export_research_package_data", fake_export_research_package)

    result = runner.invoke(
        cli.app,
        [
            "export-research-package",
            "--out-dir",
            str(tmp_path),
            "--limit",
            "7",
        ],
    )

    assert result.exit_code == 0
    assert seen == {"out_dir": tmp_path, "limit": 7}
    assert "3 reports" in result.output
    assert "2 weekly summaries" in result.output
