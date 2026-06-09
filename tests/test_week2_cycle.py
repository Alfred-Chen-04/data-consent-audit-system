"""Tests for the Week 2 full capture cycle orchestrator."""

from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

import consent_audit.week2_cycle as week2_cycle
from consent_audit.week2_cycle import run_week2_cycle


@pytest.mark.asyncio
async def test_run_week2_cycle_preflights_captures_refreshes_and_reports(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {"calls": []}

    def fake_export_preflight(**kwargs: Any) -> str:
        seen["calls"].append("preflight")
        seen["preflight"] = kwargs
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text(
            "- Overall status: ready_for_capture\n",
            encoding="utf-8",
        )
        return "- Overall status: ready_for_capture\n"

    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None,
        summary_week_of: datetime | None = None,
    ) -> SimpleNamespace:
        seen["calls"].append("weekly")
        seen["weekly"] = {
            "sites_csv": sites_csv,
            "consent_table_path": consent_table_path,
            "cohort": cohort,
            "limit": limit,
            "summary_week_of": summary_week_of,
        }
        return SimpleNamespace(
            target_count=5,
            attempted_count=5,
            succeeded_count=5,
            failed_count=0,
            budget_exceeded=False,
            failures=[],
        )

    def fake_refresh_week2_outputs(**kwargs: Any) -> dict[str, Any]:
        seen["calls"].append("refresh")
        seen["refresh"] = kwargs
        return {
            "audit_report_count": 42,
            "weekly_summary_count": 17,
            "sanity_status": "ready",
            "preflight_status": "ready_for_capture",
        }

    def fake_export_capture_checklist(**kwargs: Any) -> str:
        seen["calls"].append("checklist")
        seen["checklist"] = kwargs
        cycle_text = kwargs["cycle_report"].read_text(encoding="utf-8")
        assert "- Capture status: completed" in cycle_text
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# checklist\n- Last capture status: `completed`\n", encoding="utf-8")
        return "# checklist\n- Last capture status: `completed`\n"

    monkeypatch.setattr(week2_cycle, "export_week2_preflight_check", fake_export_preflight)
    monkeypatch.setattr(week2_cycle, "run_weekly_audit", fake_run_weekly_audit)
    monkeypatch.setattr(week2_cycle, "refresh_week2_outputs", fake_refresh_week2_outputs)
    monkeypatch.setattr(
        week2_cycle,
        "export_week2_capture_checklist",
        fake_export_capture_checklist,
        raising=False,
    )

    cycle_report_md = tmp_path / "docs" / "cycle.md"

    summary = await run_week2_cycle(
        targets_csv=tmp_path / "data" / "targets.csv",
        consent_table_csv=tmp_path / "data" / "consent.csv",
        cmp_confirmation_csv=tmp_path / "data" / "confirmation.csv",
        cmp_packet_html=tmp_path / "data" / "packet" / "index.html",
        runbook_md=tmp_path / "docs" / "runbook.md",
        sample_plan_md=tmp_path / "docs" / "sample.md",
        research_package_dir=tmp_path / "data" / "package",
        advisor_brief_md=tmp_path / "docs" / "advisor.md",
        sanity_check_md=tmp_path / "docs" / "sanity.md",
        checkin_index_md=tmp_path / "docs" / "index.md",
        capture_checklist_md=tmp_path / "docs" / "checklist.md",
        preflight_check_md=tmp_path / "docs" / "preflight.md",
        refresh_report_md=tmp_path / "docs" / "refresh.md",
        cycle_report_md=cycle_report_md,
        cohort="week2-2026-06-06",
        week_of="2026-06-06",
        run_date="2026-06-06",
        expected_target_count=5,
        limit=3,
        force=False,
    )

    assert seen["calls"] == ["preflight", "weekly", "refresh", "checklist"]
    assert seen["weekly"] == {
        "sites_csv": tmp_path / "data" / "targets.csv",
        "consent_table_path": tmp_path / "data" / "consent.csv",
        "cohort": "week2-2026-06-06",
        "limit": 3,
        "summary_week_of": datetime(2026, 6, 6, tzinfo=UTC),
    }
    assert seen["refresh"]["targets_csv"] == tmp_path / "data" / "targets.csv"
    assert seen["checklist"]["cycle_report"] == cycle_report_md
    assert seen["checklist"]["out_md"] == tmp_path / "docs" / "checklist.md"
    assert summary == {
        "preflight_status": "ready_for_capture",
        "capture_status": "completed",
        "capture_target_count": 5,
        "capture_attempted_count": 5,
        "capture_succeeded_count": 5,
        "capture_failed_count": 0,
        "audit_report_count": 42,
        "weekly_summary_count": 17,
        "sanity_status": "ready",
        "post_refresh_preflight_status": "ready_for_capture",
    }
    report_text = cycle_report_md.read_text(encoding="utf-8")
    assert "# Week 2 Cycle Report, 2026-06-06" in report_text
    assert "- Capture status: completed" in report_text
    assert "- Capture successes: 5/5" in report_text
    assert "- Capture failures: 0" in report_text
    assert "- Sanity status after refresh: `ready`" in report_text
    assert "## Inputs" in report_text
    assert f"- Target list: `{tmp_path / 'data' / 'targets.csv'}`" in report_text
    assert f"- Consent table: `{tmp_path / 'data' / 'consent.csv'}`" in report_text
    assert "- Cohort: `week2-2026-06-06`" in report_text
    assert "- Expected targets: 5" in report_text
    assert "- Capture limit: 3" in report_text
    assert "- Force used: false" in report_text
    assert "- Dry run: false" in report_text
    checklist_text = (tmp_path / "docs" / "checklist.md").read_text(encoding="utf-8")
    assert "- Last capture status: `completed`" in checklist_text


@pytest.mark.asyncio
async def test_run_week2_cycle_dry_run_preflights_and_skips_capture_and_refresh(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {"calls": []}

    def fake_export_preflight(**kwargs: Any) -> str:
        seen["calls"].append("preflight")
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text(
            "- Overall status: ready_for_capture\n",
            encoding="utf-8",
        )
        return "- Overall status: ready_for_capture\n"

    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None = None,
        summary_week_of: datetime | None = None,
    ) -> None:
        _ = sites_csv, consent_table_path, cohort, limit, summary_week_of
        seen["calls"].append("weekly")

    def fake_refresh_week2_outputs(**kwargs: Any) -> dict[str, Any]:
        _ = kwargs
        seen["calls"].append("refresh")
        return {}

    def fake_export_capture_checklist(**kwargs: Any) -> str:
        seen["calls"].append("checklist")
        cycle_text = kwargs["cycle_report"].read_text(encoding="utf-8")
        assert "- Capture status: dry_run" in cycle_text
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text("# checklist\n- Last capture status: `dry_run`\n", encoding="utf-8")
        return "# checklist\n- Last capture status: `dry_run`\n"

    monkeypatch.setattr(week2_cycle, "export_week2_preflight_check", fake_export_preflight)
    monkeypatch.setattr(week2_cycle, "run_weekly_audit", fake_run_weekly_audit)
    monkeypatch.setattr(week2_cycle, "refresh_week2_outputs", fake_refresh_week2_outputs)
    monkeypatch.setattr(
        week2_cycle,
        "export_week2_capture_checklist",
        fake_export_capture_checklist,
        raising=False,
    )

    cycle_report_md = tmp_path / "docs" / "cycle.md"

    summary = await run_week2_cycle(
        targets_csv=tmp_path / "data" / "targets.csv",
        consent_table_csv=tmp_path / "data" / "consent.csv",
        cmp_confirmation_csv=tmp_path / "data" / "confirmation.csv",
        cmp_packet_html=tmp_path / "data" / "packet" / "index.html",
        runbook_md=tmp_path / "docs" / "runbook.md",
        sample_plan_md=tmp_path / "docs" / "sample.md",
        research_package_dir=tmp_path / "data" / "package",
        advisor_brief_md=tmp_path / "docs" / "advisor.md",
        sanity_check_md=tmp_path / "docs" / "sanity.md",
        checkin_index_md=tmp_path / "docs" / "index.md",
        capture_checklist_md=tmp_path / "docs" / "checklist.md",
        preflight_check_md=tmp_path / "docs" / "preflight.md",
        refresh_report_md=tmp_path / "docs" / "refresh.md",
        cycle_report_md=cycle_report_md,
        cohort="week2-2026-06-06",
        week_of="2026-06-06",
        run_date="2026-05-30",
        expected_target_count=5,
        limit=500,
        force=False,
        dry_run=True,
    )

    assert seen["calls"] == ["preflight", "checklist"]
    assert summary == {
        "preflight_status": "ready_for_capture",
        "capture_status": "dry_run",
        "capture_target_count": 5,
        "capture_attempted_count": 0,
        "capture_succeeded_count": 0,
        "capture_failed_count": 0,
        "audit_report_count": 0,
        "weekly_summary_count": 0,
        "sanity_status": "not_run",
        "post_refresh_preflight_status": "not_run",
    }
    report_text = cycle_report_md.read_text(encoding="utf-8")
    assert "# Week 2 Cycle Report, 2026-06-06" in report_text
    assert "- Cycle mode: dry_run" in report_text
    assert "- Capture status: dry_run" in report_text
    assert "- Capture attempts: 0/5" in report_text
    assert "- Capture successes: 0/5" in report_text
    assert "- Preflight status before capture: `ready_for_capture`" in report_text
    assert "- Browser capture and refresh were not run." in report_text
    assert "## Inputs" in report_text
    assert f"- Target list: `{tmp_path / 'data' / 'targets.csv'}`" in report_text
    assert f"- Consent table: `{tmp_path / 'data' / 'consent.csv'}`" in report_text
    assert "- Cohort: `week2-2026-06-06`" in report_text
    assert "- Expected targets: 5" in report_text
    assert "- Force used: false" in report_text
    assert "- Dry run: true" in report_text
    checklist_text = (tmp_path / "docs" / "checklist.md").read_text(encoding="utf-8")
    assert "- Last capture status: `dry_run`" in checklist_text


@pytest.mark.asyncio
async def test_run_week2_cycle_dry_run_reports_next_action_when_preflight_not_ready(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {"calls": []}

    def fake_export_preflight(**kwargs: Any) -> str:
        seen["calls"].append("preflight")
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text(
            "- Overall status: needs_attention\n",
            encoding="utf-8",
        )
        return "- Overall status: needs_attention\n"

    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None = None,
        summary_week_of: datetime | None = None,
    ) -> None:
        _ = sites_csv, consent_table_path, cohort, limit, summary_week_of
        seen["calls"].append("weekly")

    def fake_refresh_week2_outputs(**kwargs: Any) -> dict[str, Any]:
        _ = kwargs
        seen["calls"].append("refresh")
        return {}

    monkeypatch.setattr(week2_cycle, "export_week2_preflight_check", fake_export_preflight)
    monkeypatch.setattr(week2_cycle, "run_weekly_audit", fake_run_weekly_audit)
    monkeypatch.setattr(week2_cycle, "refresh_week2_outputs", fake_refresh_week2_outputs)

    cycle_report_md = tmp_path / "docs" / "cycle.md"

    summary = await run_week2_cycle(
        targets_csv=tmp_path / "data" / "targets.csv",
        consent_table_csv=tmp_path / "data" / "consent.csv",
        cmp_confirmation_csv=tmp_path / "data" / "confirmation.csv",
        cmp_packet_html=tmp_path / "data" / "packet" / "index.html",
        runbook_md=tmp_path / "docs" / "runbook.md",
        sample_plan_md=tmp_path / "docs" / "sample.md",
        research_package_dir=tmp_path / "data" / "package",
        advisor_brief_md=tmp_path / "docs" / "advisor.md",
        sanity_check_md=tmp_path / "docs" / "sanity.md",
        checkin_index_md=tmp_path / "docs" / "index.md",
        capture_checklist_md=tmp_path / "docs" / "checklist.md",
        preflight_check_md=tmp_path / "docs" / "preflight.md",
        refresh_report_md=tmp_path / "docs" / "refresh.md",
        cycle_report_md=cycle_report_md,
        cohort="week2-2026-06-06",
        week_of="2026-06-06",
        run_date="2026-05-30",
        expected_target_count=5,
        limit=500,
        force=False,
        dry_run=True,
    )

    assert seen["calls"] == ["preflight"]
    assert summary["capture_status"] == "dry_run_needs_attention"
    report_text = cycle_report_md.read_text(encoding="utf-8")
    assert "- Capture status: dry_run_needs_attention" in report_text
    assert "## Next Action" in report_text
    assert (
        "- Do not start live capture until preflight is `ready_for_capture` "
        "or a force rationale is recorded."
    ) in report_text


@pytest.mark.asyncio
async def test_run_week2_cycle_marks_capture_needs_attention_after_two_failures(
    monkeypatch,
    tmp_path: Path,
) -> None:
    def fake_export_preflight(**kwargs: Any) -> str:
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text(
            "- Overall status: ready_for_capture\n",
            encoding="utf-8",
        )
        return "- Overall status: ready_for_capture\n"

    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None = None,
        summary_week_of: datetime | None = None,
    ) -> SimpleNamespace:
        _ = sites_csv, consent_table_path, cohort, limit, summary_week_of
        return SimpleNamespace(
            target_count=5,
            attempted_count=5,
            succeeded_count=3,
            failed_count=2,
            budget_exceeded=False,
            failures=[
                SimpleNamespace(url="https://broken-one.example", error="timeout"),
                SimpleNamespace(url="https://broken-two.example", error="blocked"),
            ],
        )

    def fake_refresh_week2_outputs(**kwargs: Any) -> dict[str, Any]:
        _ = kwargs
        return {
            "audit_report_count": 45,
            "weekly_summary_count": 18,
            "sanity_status": "needs_attention",
            "preflight_status": "needs_attention",
        }

    monkeypatch.setattr(week2_cycle, "export_week2_preflight_check", fake_export_preflight)
    monkeypatch.setattr(week2_cycle, "run_weekly_audit", fake_run_weekly_audit)
    monkeypatch.setattr(week2_cycle, "refresh_week2_outputs", fake_refresh_week2_outputs)

    cycle_report_md = tmp_path / "docs" / "cycle.md"

    summary = await run_week2_cycle(
        targets_csv=tmp_path / "data" / "targets.csv",
        consent_table_csv=tmp_path / "data" / "consent.csv",
        cmp_confirmation_csv=tmp_path / "data" / "confirmation.csv",
        cmp_packet_html=tmp_path / "data" / "packet" / "index.html",
        runbook_md=tmp_path / "docs" / "runbook.md",
        sample_plan_md=tmp_path / "docs" / "sample.md",
        research_package_dir=tmp_path / "data" / "package",
        advisor_brief_md=tmp_path / "docs" / "advisor.md",
        sanity_check_md=tmp_path / "docs" / "sanity.md",
        checkin_index_md=tmp_path / "docs" / "index.md",
        capture_checklist_md=tmp_path / "docs" / "checklist.md",
        preflight_check_md=tmp_path / "docs" / "preflight.md",
        refresh_report_md=tmp_path / "docs" / "refresh.md",
        cycle_report_md=cycle_report_md,
        cohort="week2-2026-06-06",
        week_of="2026-06-06",
        run_date="2026-06-06",
        expected_target_count=5,
        limit=500,
        force=False,
    )

    assert summary["capture_status"] == "needs_attention"
    assert summary["capture_failed_count"] == 2
    report_text = cycle_report_md.read_text(encoding="utf-8")
    assert "- Capture status: needs_attention" in report_text
    assert "- Capture failures: 2" in report_text
    assert "https://broken-one.example: timeout" in report_text


@pytest.mark.asyncio
async def test_run_week2_cycle_aborts_when_preflight_needs_attention(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {"weekly_called": False}

    def fake_export_preflight(**kwargs: Any) -> str:
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text(
            "- Overall status: needs_attention\n",
            encoding="utf-8",
        )
        return "- Overall status: needs_attention\n"

    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None = None,
        summary_week_of: datetime | None = None,
    ) -> None:
        _ = sites_csv, consent_table_path, cohort, limit, summary_week_of
        seen["weekly_called"] = True

    monkeypatch.setattr(week2_cycle, "export_week2_preflight_check", fake_export_preflight)
    monkeypatch.setattr(week2_cycle, "run_weekly_audit", fake_run_weekly_audit)

    cycle_report_md = tmp_path / "docs" / "cycle.md"
    capture_checklist_md = tmp_path / "docs" / "checklist.md"

    with pytest.raises(RuntimeError, match="preflight status needs_attention"):
        await run_week2_cycle(
            targets_csv=tmp_path / "data" / "targets.csv",
            consent_table_csv=tmp_path / "data" / "consent.csv",
            cmp_confirmation_csv=tmp_path / "data" / "confirmation.csv",
            cmp_packet_html=tmp_path / "data" / "packet" / "index.html",
            runbook_md=tmp_path / "docs" / "runbook.md",
            sample_plan_md=tmp_path / "docs" / "sample.md",
            research_package_dir=tmp_path / "data" / "package",
            advisor_brief_md=tmp_path / "docs" / "advisor.md",
            sanity_check_md=tmp_path / "docs" / "sanity.md",
            checkin_index_md=tmp_path / "docs" / "index.md",
            capture_checklist_md=capture_checklist_md,
            preflight_check_md=tmp_path / "docs" / "preflight.md",
            refresh_report_md=tmp_path / "docs" / "refresh.md",
            cycle_report_md=cycle_report_md,
            cohort="week2-2026-06-06",
            week_of="2026-06-06",
            run_date="2026-06-06",
            expected_target_count=5,
            limit=500,
            force=False,
        )

    assert seen["weekly_called"] is False
    report_text = cycle_report_md.read_text(encoding="utf-8")
    assert "- Cycle mode: preflight_blocked" in report_text
    assert "- Capture status: aborted" in report_text
    assert "- Capture attempts: 0/5" in report_text
    assert "- Capture successes: 0/5" in report_text
    assert (
        "- Resolve preflight warnings before rerunning Week 2 capture."
        in report_text
    )
    checklist_text = capture_checklist_md.read_text(encoding="utf-8")
    assert "- Last capture status: `aborted`" in checklist_text
    assert "- Last capture attempts: 0/5" in checklist_text


@pytest.mark.asyncio
async def test_run_week2_cycle_blocks_live_capture_before_scheduled_date(
    monkeypatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {"weekly_called": False}

    def fake_export_preflight(**kwargs: Any) -> str:
        kwargs["out_md"].parent.mkdir(parents=True, exist_ok=True)
        kwargs["out_md"].write_text(
            "- Overall status: ready_for_capture\n",
            encoding="utf-8",
        )
        return "- Overall status: ready_for_capture\n"

    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None = None,
        summary_week_of: datetime | None = None,
    ) -> None:
        _ = sites_csv, consent_table_path, cohort, limit, summary_week_of
        seen["weekly_called"] = True

    monkeypatch.setattr(week2_cycle, "export_week2_preflight_check", fake_export_preflight)
    monkeypatch.setattr(week2_cycle, "run_weekly_audit", fake_run_weekly_audit)

    cycle_report_md = tmp_path / "docs" / "cycle.md"
    capture_checklist_md = tmp_path / "docs" / "checklist.md"

    with pytest.raises(RuntimeError, match="before scheduled week 2026-06-06"):
        await run_week2_cycle(
            targets_csv=tmp_path / "data" / "targets.csv",
            consent_table_csv=tmp_path / "data" / "consent.csv",
            cmp_confirmation_csv=tmp_path / "data" / "confirmation.csv",
            cmp_packet_html=tmp_path / "data" / "packet" / "index.html",
            runbook_md=tmp_path / "docs" / "runbook.md",
            sample_plan_md=tmp_path / "docs" / "sample.md",
            research_package_dir=tmp_path / "data" / "package",
            advisor_brief_md=tmp_path / "docs" / "advisor.md",
            sanity_check_md=tmp_path / "docs" / "sanity.md",
            checkin_index_md=tmp_path / "docs" / "index.md",
            capture_checklist_md=capture_checklist_md,
            preflight_check_md=tmp_path / "docs" / "preflight.md",
            refresh_report_md=tmp_path / "docs" / "refresh.md",
            cycle_report_md=cycle_report_md,
            cohort="week2-2026-06-06",
            week_of="2026-06-06",
            run_date="2026-05-30",
            expected_target_count=5,
            limit=500,
            force=False,
            allow_early=False,
        )

    assert seen["weekly_called"] is False
    report_text = cycle_report_md.read_text(encoding="utf-8")
    assert "- Cycle mode: scheduled_date_blocked" in report_text
    assert "- Capture status: scheduled_date_not_reached" in report_text
    assert "- Capture attempts: 0/5" in report_text
    assert "- Run date: 2026-05-30" in report_text
    assert "- Allow early: false" in report_text
    assert (
        "- Wait until 2026-06-06 before live capture, or rerun with "
        "`--allow-early` after recording the timing risk."
        in report_text
    )
    checklist_text = capture_checklist_md.read_text(encoding="utf-8")
    assert "- Last capture status: `scheduled_date_not_reached`" in checklist_text
