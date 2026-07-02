"""Tests for the compact research-status dashboard."""

import csv
import json
from pathlib import Path

from consent_audit.research_status import render_research_status


def test_render_research_status_summarizes_week2_state(tmp_path: Path) -> None:
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
    manifest_json = tmp_path / "research_manifest.json"
    manifest_json.write_text(
        json.dumps({"audit_report_count": 37, "weekly_summary_count": 15}),
        encoding="utf-8",
    )
    cmp_confirmation_csv = tmp_path / "cmp_confirmation.csv"
    with cmp_confirmation_csv.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["url", "confirmation_status"])
        writer.writeheader()
        for index in range(8):
            writer.writerow(
                {
                    "url": f"https://example-{index}.com",
                    "confirmation_status": "pending",
                }
            )
    preflight_md = tmp_path / "preflight.md"
    preflight_md.write_text(
        "# Preflight\n\n- Overall status: ready_for_capture\n",
        encoding="utf-8",
    )
    sanity_md = tmp_path / "sanity.md"
    sanity_md.write_text(
        "# Sanity\n\n- Overall status: pending_capture\n",
        encoding="utf-8",
    )
    cycle_report_md = tmp_path / "cycle.md"
    cycle_report_md.write_text(
        "# Cycle\n\n"
        "## Summary\n\n"
        "- Capture status: dry_run\n\n"
        "## Next Action\n\n"
        "- Start live capture with `week2-cycle` when ready.\n",
        encoding="utf-8",
    )
    results_tables_md = tmp_path / "ssrp_results_tables.md"
    results_tables_md.write_text("# Tables\n", encoding="utf-8")
    paper_skeleton_md = tmp_path / "ssrp_paper_skeleton.md"
    paper_skeleton_md.write_text("# Skeleton\n", encoding="utf-8")
    figure_plan_md = tmp_path / "ssrp_figure_plan.md"
    figure_plan_md.write_text("# Figures\n", encoding="utf-8")
    writing_pack_md = tmp_path / "ssrp_writing_pack.md"
    writing_pack_md.write_text("# Writing\n", encoding="utf-8")
    claim_register_md = tmp_path / "ssrp_claim_register.md"
    claim_register_md.write_text("# Claims\n", encoding="utf-8")
    poster_plan_md = tmp_path / "ssrp_poster_plan.md"
    poster_plan_md.write_text("# Poster\n", encoding="utf-8")

    text = render_research_status(
        targets_csv=targets_csv,
        research_manifest_json=manifest_json,
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

    assert "# SSRP Research Status" in text
    assert "- Week 2 targets: 5" in text
    assert "- Categories: finance=1, food=1, news=2, travel=1" in text
    assert "- Preflight status: `ready_for_capture`" in text
    assert "- Sanity status: `pending_capture`" in text
    assert "- Cycle capture status: `dry_run`" in text
    assert "- Audit reports in package: 37" in text
    assert "- Longitudinal summaries in package: 15" in text
    assert "- CMP confirmations: pending=8" in text
    assert (
        "- Support artifacts: claim_register=present, figure_plan=present, "
        "paper_skeleton=present, poster_plan=present, results_tables=present, "
        "writing_pack=present"
    ) in text
    assert "- Next action: Start live capture with `week2-cycle` when ready." in text
    assert f"- SSRP results tables: `{results_tables_md}`" in text
    assert f"- Optional future-paper skeleton: `{paper_skeleton_md}`" in text
    assert f"- SSRP presentation/poster figure plan: `{figure_plan_md}`" in text
    assert f"- SSRP writing support pack: `{writing_pack_md}`" in text
    assert f"- SSRP evidence claim register: `{claim_register_md}`" in text
    assert f"- SSRP poster plan: `{poster_plan_md}`" in text
