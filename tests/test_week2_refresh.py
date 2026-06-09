"""Tests for the Week 2 post-capture refresh orchestrator."""

from pathlib import Path
from typing import Any

import consent_audit.week2_refresh as week2_refresh
from consent_audit.week2_refresh import refresh_week2_outputs


def test_refresh_week2_outputs_uses_fresh_research_package_tables(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {"calls": []}

    def fake_export_research_package(out_dir: Path, *, limit: int = 500) -> dict[str, Any]:
        seen["calls"].append("research_package")
        seen["research_package_out_dir"] = out_dir
        seen["research_package_limit"] = limit
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "audit_report_summary.csv").write_text("url\n", encoding="utf-8")
        (out_dir / "longitudinal_summary.csv").write_text("url\n", encoding="utf-8")
        (out_dir / "research_manifest.json").write_text("{}", encoding="utf-8")
        return {
            "audit_report_count": 42,
            "weekly_summary_count": 17,
            "files": {
                "audit_report_summary": "audit_report_summary.csv",
                "longitudinal_summary": "longitudinal_summary.csv",
            },
        }

    def fake_export_advisor_brief(
        *,
        targets_csv: Path,
        audit_summary_csv: Path,
        longitudinal_summary_csv: Path,
        cmp_confirmation_csv: Path,
        manifest_json: Path,
        out_md: Path,
        title: str,
    ) -> str:
        seen["calls"].append("advisor")
        seen["advisor"] = {
            "targets_csv": targets_csv,
            "audit_summary_csv": audit_summary_csv,
            "longitudinal_summary_csv": longitudinal_summary_csv,
            "cmp_confirmation_csv": cmp_confirmation_csv,
            "manifest_json": manifest_json,
            "out_md": out_md,
            "title": title,
        }
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text("# advisor\n", encoding="utf-8")
        return "# advisor\n"

    def fake_export_sanity_check(
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
        seen["calls"].append("sanity")
        seen["sanity"] = {
            "targets_csv": targets_csv,
            "consent_table_csv": consent_table_csv,
            "audit_summary_csv": audit_summary_csv,
            "longitudinal_summary_csv": longitudinal_summary_csv,
            "out_md": out_md,
            "cohort": cohort,
            "week_of": week_of,
            "title": title,
        }
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text("- Overall status: ready\n", encoding="utf-8")
        return "- Overall status: ready\n"

    def fake_export_results_tables(**kwargs: Any) -> str:
        seen["calls"].append("results_tables")
        seen["results_tables"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# tables\n", encoding="utf-8")
        return "# tables\n"

    def fake_export_paper_skeleton(**kwargs: Any) -> str:
        seen["calls"].append("paper_skeleton")
        seen["paper_skeleton"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# skeleton\n", encoding="utf-8")
        return "# skeleton\n"

    def fake_export_figure_plan(**kwargs: Any) -> str:
        seen["calls"].append("figure_plan")
        seen["figure_plan"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# figures\n", encoding="utf-8")
        return "# figures\n"

    def fake_export_writing_pack(**kwargs: Any) -> str:
        seen["calls"].append("writing_pack")
        seen["writing_pack"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# writing\n", encoding="utf-8")
        return "# writing\n"

    def fake_export_claim_register(**kwargs: Any) -> str:
        seen["calls"].append("claim_register")
        seen["claim_register"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# claims\n", encoding="utf-8")
        return "# claims\n"

    def fake_export_poster_plan(**kwargs: Any) -> str:
        seen["calls"].append("poster_plan")
        seen["poster_plan"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# poster\n", encoding="utf-8")
        return "# poster\n"

    def fake_export_checkin_index(**kwargs: Any) -> str:
        seen["calls"].append("checkin")
        seen["checkin"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# index\n", encoding="utf-8")
        return "# index\n"

    def fake_export_preflight_check(**kwargs: Any) -> str:
        seen["calls"].append("preflight")
        seen["preflight"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("- Overall status: ready_for_capture\n", encoding="utf-8")
        return "- Overall status: ready_for_capture\n"

    def fake_export_capture_checklist(**kwargs: Any) -> str:
        seen["calls"].append("checklist")
        seen["checklist"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# checklist\n", encoding="utf-8")
        return "# checklist\n"

    monkeypatch.setattr(week2_refresh, "export_research_package", fake_export_research_package)
    monkeypatch.setattr(week2_refresh, "export_weekly_advisor_brief", fake_export_advisor_brief)
    monkeypatch.setattr(week2_refresh, "export_week2_sanity_check", fake_export_sanity_check)
    monkeypatch.setattr(week2_refresh, "export_ssrp_results_tables", fake_export_results_tables)
    monkeypatch.setattr(week2_refresh, "export_ssrp_paper_skeleton", fake_export_paper_skeleton)
    monkeypatch.setattr(week2_refresh, "export_ssrp_figure_plan", fake_export_figure_plan)
    monkeypatch.setattr(week2_refresh, "export_ssrp_writing_pack", fake_export_writing_pack)
    monkeypatch.setattr(week2_refresh, "export_ssrp_claim_register", fake_export_claim_register)
    monkeypatch.setattr(week2_refresh, "export_ssrp_poster_plan", fake_export_poster_plan)
    monkeypatch.setattr(week2_refresh, "export_checkin_index", fake_export_checkin_index)
    monkeypatch.setattr(week2_refresh, "export_week2_preflight_check", fake_export_preflight_check)
    monkeypatch.setattr(
        week2_refresh,
        "export_week2_capture_checklist",
        fake_export_capture_checklist,
    )

    research_package_dir = tmp_path / "data" / "research_package"
    report_md = tmp_path / "docs" / "refresh.md"

    summary = refresh_week2_outputs(
        targets_csv=tmp_path / "data" / "targets.csv",
        consent_table_csv=tmp_path / "data" / "consent.csv",
        cmp_confirmation_csv=tmp_path / "data" / "confirmation.csv",
        cmp_packet_html=tmp_path / "data" / "packet" / "index.html",
        runbook_md=tmp_path / "docs" / "runbook.md",
        sample_plan_md=tmp_path / "docs" / "sample_plan.md",
        research_package_dir=research_package_dir,
        advisor_brief_md=tmp_path / "docs" / "advisor.md",
        sanity_check_md=tmp_path / "docs" / "sanity.md",
        checkin_index_md=tmp_path / "docs" / "index.md",
        capture_checklist_md=tmp_path / "docs" / "checklist.md",
        results_tables_md=tmp_path / "docs" / "results_tables.md",
        paper_skeleton_md=tmp_path / "docs" / "paper_skeleton.md",
        figure_plan_md=tmp_path / "docs" / "figure_plan.md",
        writing_pack_md=tmp_path / "docs" / "writing_pack.md",
        claim_register_md=tmp_path / "docs" / "claim_register.md",
        poster_plan_md=tmp_path / "docs" / "poster_plan.md",
        preflight_check_md=tmp_path / "docs" / "preflight.md",
        refresh_report_md=report_md,
        cycle_report_md=tmp_path / "docs" / "cycle.md",
        cohort="week2-2026-06-06",
        week_of="2026-06-06",
        expected_target_count=5,
        limit=123,
    )

    package_audit_csv = research_package_dir / "audit_report_summary.csv"
    package_longitudinal_csv = research_package_dir / "longitudinal_summary.csv"

    assert seen["calls"] == [
        "research_package",
        "advisor",
        "sanity",
        "results_tables",
        "paper_skeleton",
        "figure_plan",
        "writing_pack",
        "claim_register",
        "poster_plan",
        "preflight",
        "checklist",
        "checkin",
    ]
    assert seen["advisor"]["audit_summary_csv"] == package_audit_csv
    assert seen["advisor"]["longitudinal_summary_csv"] == package_longitudinal_csv
    assert seen["sanity"]["audit_summary_csv"] == package_audit_csv
    assert seen["sanity"]["longitudinal_summary_csv"] == package_longitudinal_csv
    assert seen["results_tables"]["audit_summary_csv"] == package_audit_csv
    assert seen["results_tables"]["longitudinal_summary_csv"] == package_longitudinal_csv
    assert seen["paper_skeleton"]["audit_summary_csv"] == package_audit_csv
    assert seen["paper_skeleton"]["longitudinal_summary_csv"] == package_longitudinal_csv
    assert seen["paper_skeleton"]["manifest_json"] == research_package_dir / "research_manifest.json"
    assert seen["figure_plan"]["audit_summary_csv"] == package_audit_csv
    assert seen["figure_plan"]["longitudinal_summary_csv"] == package_longitudinal_csv
    assert seen["figure_plan"]["results_tables_md"] == tmp_path / "docs" / "results_tables.md"
    assert seen["figure_plan"]["paper_skeleton_md"] == tmp_path / "docs" / "paper_skeleton.md"
    assert seen["figure_plan"]["cycle_report_md"] == tmp_path / "docs" / "cycle.md"
    assert seen["writing_pack"]["audit_summary_csv"] == package_audit_csv
    assert seen["writing_pack"]["longitudinal_summary_csv"] == package_longitudinal_csv
    assert seen["writing_pack"]["cmp_confirmation_csv"] == tmp_path / "data" / "confirmation.csv"
    assert seen["writing_pack"]["results_tables_md"] == tmp_path / "docs" / "results_tables.md"
    assert seen["writing_pack"]["paper_skeleton_md"] == tmp_path / "docs" / "paper_skeleton.md"
    assert seen["writing_pack"]["figure_plan_md"] == tmp_path / "docs" / "figure_plan.md"
    assert seen["writing_pack"]["cycle_report_md"] == tmp_path / "docs" / "cycle.md"
    assert seen["claim_register"]["audit_summary_csv"] == package_audit_csv
    assert seen["claim_register"]["longitudinal_summary_csv"] == package_longitudinal_csv
    assert seen["claim_register"]["cmp_confirmation_csv"] == tmp_path / "data" / "confirmation.csv"
    assert seen["claim_register"]["results_tables_md"] == tmp_path / "docs" / "results_tables.md"
    assert seen["claim_register"]["paper_skeleton_md"] == tmp_path / "docs" / "paper_skeleton.md"
    assert seen["claim_register"]["figure_plan_md"] == tmp_path / "docs" / "figure_plan.md"
    assert seen["claim_register"]["writing_pack_md"] == tmp_path / "docs" / "writing_pack.md"
    assert seen["claim_register"]["cycle_report_md"] == tmp_path / "docs" / "cycle.md"
    assert seen["poster_plan"]["audit_summary_csv"] == package_audit_csv
    assert seen["poster_plan"]["longitudinal_summary_csv"] == package_longitudinal_csv
    assert seen["poster_plan"]["cmp_confirmation_csv"] == tmp_path / "data" / "confirmation.csv"
    assert seen["poster_plan"]["results_tables_md"] == tmp_path / "docs" / "results_tables.md"
    assert seen["poster_plan"]["paper_skeleton_md"] == tmp_path / "docs" / "paper_skeleton.md"
    assert seen["poster_plan"]["figure_plan_md"] == tmp_path / "docs" / "figure_plan.md"
    assert seen["poster_plan"]["writing_pack_md"] == tmp_path / "docs" / "writing_pack.md"
    assert seen["poster_plan"]["claim_register_md"] == tmp_path / "docs" / "claim_register.md"
    assert seen["poster_plan"]["cycle_report_md"] == tmp_path / "docs" / "cycle.md"
    assert seen["checkin"]["cycle_report"] == tmp_path / "docs" / "cycle.md"
    assert seen["checkin"]["capture_checklist"] == tmp_path / "docs" / "checklist.md"
    assert seen["checklist"]["preflight_check"] == tmp_path / "docs" / "preflight.md"
    assert seen["checklist"]["cycle_report"] == tmp_path / "docs" / "cycle.md"
    assert seen["research_package_limit"] == 123
    assert summary["audit_report_count"] == 42
    assert summary["weekly_summary_count"] == 17
    assert summary["sanity_status"] == "ready"
    assert summary["preflight_status"] == "ready_for_capture"
    assert summary["results_tables_md"] == str(tmp_path / "docs" / "results_tables.md")
    assert summary["paper_skeleton_md"] == str(tmp_path / "docs" / "paper_skeleton.md")
    assert summary["figure_plan_md"] == str(tmp_path / "docs" / "figure_plan.md")
    assert summary["writing_pack_md"] == str(tmp_path / "docs" / "writing_pack.md")
    assert summary["claim_register_md"] == str(tmp_path / "docs" / "claim_register.md")
    assert summary["poster_plan_md"] == str(tmp_path / "docs" / "poster_plan.md")
    assert "# Week 2 Refresh Report" in report_md.read_text(encoding="utf-8")
    assert "Research package" in report_md.read_text(encoding="utf-8")
    assert "SSRP results tables" in report_md.read_text(encoding="utf-8")
    assert "SSRP paper skeleton" in report_md.read_text(encoding="utf-8")
    assert "SSRP figure plan" in report_md.read_text(encoding="utf-8")
    assert "SSRP writing pack" in report_md.read_text(encoding="utf-8")
    assert "SSRP claim register" in report_md.read_text(encoding="utf-8")
    assert "SSRP poster plan" in report_md.read_text(encoding="utf-8")
    assert "Capture checklist" in report_md.read_text(encoding="utf-8")
