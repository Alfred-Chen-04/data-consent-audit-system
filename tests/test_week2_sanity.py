"""Tests for Week 2 post-capture sanity checks."""

from pathlib import Path

from consent_audit.week2_sanity import export_week2_sanity_check


def test_export_week2_sanity_check_reports_missing_and_complete_targets(
    tmp_path: Path,
) -> None:
    targets = tmp_path / "targets.csv"
    targets.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://complete.example,Complete,news,false,target\n"
        "https://missing.example,Missing,finance,false,target\n",
        encoding="utf-8",
    )
    consent_table = tmp_path / "consent.csv"
    consent_table.write_text(
        "url,capture_date,captured_at,cohort,banner_detected,accept_available,"
        "reject_available,customize_available,dismiss_available,layer1_gate_passed,"
        "first_screenshot_ref,first_dom_snapshot_ref,dom_hash,image_hash,"
        "layer2_mean_effort,layer2_overall_category,transparency_grade,"
        "unbiased_choice_grade,tier,notes\n"
        "https://complete.example/,2026-06-06,2026-06-06T10:00:00+00:00,"
        "week2-2026-06-06,true,true,true,true,false,true,"
        "captures/complete.png,captures/complete.html,dom-complete,img-complete,"
        "0.00,Easy,B,A,Compliant,\n",
        encoding="utf-8",
    )
    audit_summary = tmp_path / "audit.csv"
    audit_summary.write_text(
        "report_id,bundle_id,url,capture_date,captured_at,generated_at,tier,"
        "layer1_gate_passed,accept_available,reject_available,customize_available,"
        "dismiss_available,missing_paths,layer2_mean_effort,layer2_overall_category,"
        "transparency_grade,unbiased_choice_grade,biased_toward,"
        "first_screenshot_ref,first_dom_snapshot_ref,dom_hash,image_hash,api_cost_usd\n"
        "r1,b1,https://complete.example,2026-06-06,2026-06-06T10:00:00+00:00,"
        "2026-06-06T10:01:00+00:00,Compliant,true,true,true,true,false,"
        "dismiss,0.00,Easy,B,A,,captures/complete.png,captures/complete.html,"
        "dom-complete,img-complete,0.0000\n",
        encoding="utf-8",
    )
    longitudinal = tmp_path / "longitudinal.csv"
    longitudinal.write_text(
        "url,week_of,severity,event_count,event_types,max_magnitude,"
        "has_pathway_change,has_score_change,has_copy_change,has_layout_change,"
        "has_dom_restructure,summary,implications_for_user\n"
        "https://complete.example,2026-06-06,A,0,,0.00,false,false,false,"
        "false,false,No change,No follow-up\n",
        encoding="utf-8",
    )
    out_md = tmp_path / "sanity.md"

    text = export_week2_sanity_check(
        targets_csv=targets,
        consent_table_csv=consent_table,
        audit_summary_csv=audit_summary,
        longitudinal_summary_csv=longitudinal,
        out_md=out_md,
        cohort="week2-2026-06-06",
        week_of="2026-06-06",
        title="Week 2 Sanity",
    )

    assert out_md.read_text(encoding="utf-8") == text
    assert "# Week 2 Sanity" in text
    assert "- Target sites: 2" in text
    assert "- Consent rows captured: 1/2" in text
    assert "- Evidence-complete rows: 1/2" in text
    assert "verify raw DOM file sync separately" in text
    assert "- Matching audit reports: 1/2" in text
    assert "- Weekly summaries present: 1/2" in text
    assert "- Overall status: needs_attention" in text
    assert "| Complete | captured | complete | matched | present |" in text
    assert "| Missing | missing | not checked | missing | missing |" in text
    assert "No consent-table row for cohort week2-2026-06-06" in text
