"""Tests for advisor check-in index exports."""

from pathlib import Path

from consent_audit.checkin_index import export_checkin_index


def test_export_checkin_index_links_required_artifacts_and_status(tmp_path: Path) -> None:
    advisor_brief = tmp_path / "docs" / "advisor.md"
    sanity_check = tmp_path / "docs" / "sanity.md"
    capture_checklist = tmp_path / "docs" / "checklist.md"
    cycle_report = tmp_path / "docs" / "cycle.md"
    runbook = tmp_path / "docs" / "runbook.md"
    sample_plan = tmp_path / "docs" / "sample_plan.md"
    confirmation = tmp_path / "data" / "confirmation.csv"
    packet = tmp_path / "data" / "packet" / "index.html"
    research_package = tmp_path / "data" / "research_package"
    manifest = research_package / "research_manifest.json"
    for path in [
        advisor_brief,
        sanity_check,
        capture_checklist,
        cycle_report,
        runbook,
        sample_plan,
        confirmation,
        packet,
        manifest,
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder", encoding="utf-8")
    sanity_check.write_text(
        "# Sanity\n\n- Overall status: pending_capture\n",
        encoding="utf-8",
    )
    out_md = tmp_path / "docs" / "index.md"

    text = export_checkin_index(
        out_md=out_md,
        title="Advisor Check-in Index",
        advisor_brief=advisor_brief,
        sanity_check=sanity_check,
        capture_checklist=capture_checklist,
        cycle_report=cycle_report,
        runbook=runbook,
        sample_plan=sample_plan,
        cmp_confirmation_sheet=confirmation,
        cmp_packet=packet,
        research_package_dir=research_package,
        research_manifest=manifest,
    )

    assert out_md.read_text(encoding="utf-8") == text
    assert "# Advisor Check-in Index" in text
    assert "- Week 2 sanity status: `pending_capture`" in text
    assert "[Advisor update](advisor.md)" in text
    assert "[Sanity check](sanity.md)" in text
    assert "[Capture checklist](checklist.md)" in text
    assert "[Cycle report](cycle.md)" in text
    assert "[Research package](../data/research_package)" in text
    assert "[CMP confirmation sheet](../data/confirmation.csv)" in text
    assert "[CMP evidence packet](../data/packet/index.html)" in text
    assert "Use this index as the first file for advisor check-ins." in text
    assert (
        "`PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-preflight-check`"
    ) in text
    assert (
        "`PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-cycle --dry-run`"
    ) in text
    assert (
        "`AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m "
        "consent_audit.cli week2-cycle`"
    ) in text
    assert (
        "`PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-refresh-outputs`"
    ) in text
    assert (
        "`PYTHONPATH=src .venv/bin/python -m consent_audit.cli "
        "week2-capture-checklist`"
    ) in text
