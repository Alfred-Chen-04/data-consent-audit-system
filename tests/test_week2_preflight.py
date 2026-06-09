"""Tests for Week 2 preflight readiness checks."""

import csv
import json
from pathlib import Path

from consent_audit.week2_preflight import export_week2_preflight_check


def test_export_week2_preflight_check_reports_ready_for_capture(tmp_path: Path) -> None:
    targets_csv = tmp_path / "targets.csv"
    targets_csv.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://www.theguardian.com,The Guardian,news,false,\n"
        "https://www.cnn.com,CNN,news,false,\n"
        "https://www.booking.com,Booking.com,travel,false,\n"
        "https://www.nerdwallet.com,NerdWallet,finance,false,\n"
        "https://www.coca-cola.com/us/en,Coca-Cola,food,false,\n",
        encoding="utf-8",
    )
    sanity_check_md = tmp_path / "docs" / "sanity.md"
    advisor_brief_md = tmp_path / "docs" / "advisor.md"
    checkin_index_md = tmp_path / "docs" / "index.md"
    runbook_md = tmp_path / "docs" / "runbook.md"
    cmp_packet_html = tmp_path / "data" / "packet" / "index.html"
    for path in [
        sanity_check_md,
        advisor_brief_md,
        checkin_index_md,
        runbook_md,
        cmp_packet_html,
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder", encoding="utf-8")
    sanity_check_md.write_text(
        "# Sanity\n\n- Overall status: pending_capture\n",
        encoding="utf-8",
    )

    research_manifest_json = tmp_path / "data" / "research_package" / "research_manifest.json"
    research_manifest_json.parent.mkdir(parents=True, exist_ok=True)
    research_manifest_json.write_text(
        json.dumps({"audit_report_count": 37, "weekly_summary_count": 15}),
        encoding="utf-8",
    )
    cmp_confirmation_csv = tmp_path / "data" / "confirmation.csv"
    with cmp_confirmation_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["url", "confirmation_status"])
        writer.writeheader()
        for index in range(8):
            writer.writerow(
                {
                    "url": f"https://example-{index}.com",
                    "confirmation_status": "pending",
                }
            )
    out_md = tmp_path / "docs" / "preflight.md"

    text = export_week2_preflight_check(
        targets_csv=targets_csv,
        sanity_check_md=sanity_check_md,
        advisor_brief_md=advisor_brief_md,
        checkin_index_md=checkin_index_md,
        runbook_md=runbook_md,
        research_manifest_json=research_manifest_json,
        cmp_confirmation_csv=cmp_confirmation_csv,
        cmp_packet_html=cmp_packet_html,
        out_md=out_md,
        title="Week 2 Preflight",
        expected_target_count=5,
    )

    assert out_md.read_text(encoding="utf-8") == text
    assert "# Week 2 Preflight" in text
    assert "- Overall status: ready_for_capture" in text
    assert "- Week 2 targets: 5/5" in text
    assert "- Target validation: passed" in text
    assert "- Sanity status: `pending_capture`" in text
    assert "- Audit reports in package: 37" in text
    assert "- Longitudinal summaries in package: 15" in text
    assert "- CMP confirmations: pending=8" in text
    assert "- Categories: finance=1, food=1, news=2, travel=1" in text
    assert "[Advisor update](advisor.md)" in text
    assert "[Check-in index](index.md)" in text
