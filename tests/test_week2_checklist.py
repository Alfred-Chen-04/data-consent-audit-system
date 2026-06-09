"""Tests for Week 2 capture-day checklist exports."""

from pathlib import Path

from consent_audit.week2_checklist import export_week2_capture_checklist


def test_export_week2_capture_checklist_links_controls_and_gates(tmp_path: Path) -> None:
    preflight = tmp_path / "docs" / "preflight.md"
    sanity = tmp_path / "docs" / "sanity.md"
    cycle = tmp_path / "docs" / "cycle.md"
    refresh = tmp_path / "docs" / "refresh.md"
    index = tmp_path / "docs" / "index.md"
    advisor = tmp_path / "docs" / "advisor.md"
    targets = tmp_path / "data" / "targets.csv"
    consent_table = tmp_path / "data" / "consent.csv"
    for path in [preflight, sanity, cycle, refresh, index, advisor, targets, consent_table]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder", encoding="utf-8")
    preflight.write_text("- Overall status: ready_for_capture\n", encoding="utf-8")
    sanity.write_text("- Overall status: pending_capture\n", encoding="utf-8")
    cycle.write_text(
        "- Cycle mode: dry_run\n"
        "- Capture status: `dry_run`\n"
        "- Capture attempts: 0/5\n",
        encoding="utf-8",
    )
    out_md = tmp_path / "docs" / "checklist.md"

    text = export_week2_capture_checklist(
        out_md=out_md,
        title="Week 2 Capture-Day Checklist",
        week_of="2026-06-06",
        cohort="week2-2026-06-06",
        expected_target_count=5,
        targets_csv=targets,
        consent_table_csv=consent_table,
        preflight_check=preflight,
        cycle_report=cycle,
        refresh_report=refresh,
        sanity_check=sanity,
        checkin_index=index,
        advisor_brief=advisor,
    )

    assert out_md.read_text(encoding="utf-8") == text
    assert "# Week 2 Capture-Day Checklist" in text
    assert "- Cohort: `week2-2026-06-06`" in text
    assert "- Expected targets: 5" in text
    assert "- Preflight status: `ready_for_capture`" in text
    assert "- Sanity status: `pending_capture`" in text
    assert "- Last cycle mode: `dry_run`" in text
    assert "- Last capture status: `dry_run`" in text
    assert "[Week 2 targets](../data/targets.csv)" in text
    assert "[Consent table](../data/consent.csv)" in text
    assert "[Preflight check](preflight.md)" in text
    assert "[Cycle report](cycle.md)" in text
    assert "[Refresh report](refresh.md)" in text
    assert "[Sanity check](sanity.md)" in text
    assert (
        "- [ ] Run `PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-cycle --dry-run`"
    ) in text
    assert (
        "- [ ] Run `AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m "
        "consent_audit.cli week2-cycle`"
    ) in text
    assert "- [ ] Confirm every target has screenshot, DOM, hash, and report evidence." in text
