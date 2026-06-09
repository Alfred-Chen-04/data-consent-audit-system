"""Tests for SSRP paper writing-pack generation."""

from pathlib import Path

from consent_audit.paper_writing_pack import export_ssrp_writing_pack


def test_export_ssrp_writing_pack_turns_current_evidence_into_draft_notes(
    tmp_path: Path,
) -> None:
    targets = tmp_path / "targets.csv"
    targets.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://example.com,Example,news,false,week2 target\n"
        "https://stable.example,Stable,food,false,week2 target\n",
        encoding="utf-8",
    )
    audit_summary = tmp_path / "audit_summary.csv"
    audit_summary.write_text(
        "report_id,bundle_id,url,capture_date,captured_at,generated_at,tier,"
        "banner_detected,layer1_gate_passed,accept_available,reject_available,"
        "customize_available,dismiss_available,missing_paths,layer2_mean_effort,"
        "layer2_overall_category,"
        "transparency_grade,unbiased_choice_grade,biased_toward,"
        "first_screenshot_ref,first_dom_snapshot_ref,dom_hash,image_hash,api_cost_usd\n"
        "old,bundle,https://example.com/,2026-05-29,2026-05-29T10:00:00+00:00,"
        "2026-05-29T10:01:00+00:00,High-Risk,false,false,false,false,false,false,"
        "accept|reject|customize|dismiss,,,,,,old.png,old.html,dom,img,0.0000\n"
        "new,bundle,https://example.com,2026-06-06,2026-06-06T10:00:00+00:00,"
        "2026-06-06T10:01:00+00:00,Compliant,true,true,true,true,true,false,"
        "dismiss,0.00,Easy,B,A,,new.png,new.html,dom2,img2,0.0000\n"
        "stable,bundle,https://stable.example,2026-06-06,2026-06-06T10:02:00+00:00,"
        "2026-06-06T10:03:00+00:00,High-Risk,false,false,false,false,false,false,"
        "accept|reject|customize|dismiss,,,,,,stable.png,stable.html,dom3,img3,0.0000\n",
        encoding="utf-8",
    )
    longitudinal = tmp_path / "longitudinal.csv"
    longitudinal.write_text(
        "url,week_of,severity,event_count,event_types,max_magnitude,"
        "has_pathway_change,has_score_change,has_copy_change,has_layout_change,"
        "has_dom_restructure,summary,implications_for_user\n"
        "https://example.com,2026-06-06,D,2,copy_change|pathway_change,1.00,true,"
        "false,true,false,false,Path changed,Review paths\n"
        "https://stable.example,2026-06-06,A,0,,0.00,false,false,false,false,"
        "false,No detected consent-interface changes,No follow-up required\n",
        encoding="utf-8",
    )
    confirmations = tmp_path / "cmp_confirmation.csv"
    confirmations.write_text(
        "url,confirmation_status\n"
        "https://manual.example,pending\n"
        "https://done.example,confirmed\n",
        encoding="utf-8",
    )
    cycle_report = tmp_path / "cycle.md"
    cycle_report.write_text(
        "# Week 2 Cycle Report\n\n"
        "- Capture status: `scheduled_date_not_reached`\n"
        "- Cycle mode: `scheduled_date_blocked`\n",
        encoding="utf-8",
    )
    out_md = tmp_path / "writing_pack.md"

    text = export_ssrp_writing_pack(
        targets_csv=targets,
        audit_summary_csv=audit_summary,
        longitudinal_summary_csv=longitudinal,
        cmp_confirmation_csv=confirmations,
        results_tables_md=tmp_path / "results_tables.md",
        paper_skeleton_md=tmp_path / "paper_skeleton.md",
        figure_plan_md=tmp_path / "figure_plan.md",
        cycle_report_md=cycle_report,
        out_md=out_md,
        title="SSRP Writing Pack",
        week_label="Week 2",
    )

    assert out_md.read_text(encoding="utf-8") == text
    assert "# SSRP Writing Pack" in text
    assert "- Target sites: 2" in text
    assert "- RQ1 reports available for targets: 2/2" in text
    assert "- RQ2 summaries available for targets: 2/2" in text
    assert "- Banner evidence classes: banner_present=1, no_visible_banner=1" in text
    assert "- Banner-present automated tiers: Compliant=1" in text
    assert "- Raw automated target tiers: Compliant=1, High-Risk=1" in text
    assert "- Latest longitudinal severity: A=1, D=1" in text
    assert "- CMP confirmations: confirmed=1, pending=1" in text
    assert "- Claim status: provisional until scheduled Week 2 capture is complete." in text
    assert "## Methods Draft Blocks" in text
    assert "focused deep sample of 2 public websites" in text
    assert "deterministic scoring after schema validation" in text
    assert "## Preliminary Results Notes" in text
    assert "- RQ1: banner-present automated tiers are Compliant=1." in text
    assert (
        "- RQ1 contrast context: no-visible-banner contrast candidates=1; "
        "raw automated tiers are Compliant=1, High-Risk=1."
    ) in text
    assert "- RQ2: latest target longitudinal severity levels are A=1, D=1." in text
    assert "## Discussion And Implication Notes" in text
    assert "small GRC/SOC 2 implication" in text
    assert "## Limitations To Carry Forward" in text
    assert "pending CMP/manual-review confirmations remain unresolved: confirmed=1, pending=1" in text
    assert "## Drafting Checklist" in text
    assert "Do not turn provisional results into final claims until `week2-cycle` completes." in text
    assert f"- Results tables: `{tmp_path / 'results_tables.md'}`" in text
    assert f"- Paper skeleton: `{tmp_path / 'paper_skeleton.md'}`" in text
    assert f"- Figure plan: `{tmp_path / 'figure_plan.md'}`" in text
    assert "ssrp-claim-register" in text
    assert f"- Cycle report: `{cycle_report}`" in text

    cycle_report.write_text(
        "# Week 2 Cycle Report\n\n"
        "- Capture status: completed\n",
        encoding="utf-8",
    )
    completed_text = export_ssrp_writing_pack(
        targets_csv=targets,
        audit_summary_csv=audit_summary,
        longitudinal_summary_csv=longitudinal,
        cmp_confirmation_csv=confirmations,
        results_tables_md=tmp_path / "results_tables.md",
        paper_skeleton_md=tmp_path / "paper_skeleton.md",
        figure_plan_md=tmp_path / "figure_plan.md",
        cycle_report_md=cycle_report,
        out_md=out_md,
        title="SSRP Writing Pack",
        week_label="Week 2",
    )

    assert "- Claim status: ready for post-sanity drafting." in completed_text
    assert "final results should wait for fresh capture and sanity confirmation" not in completed_text
    assert "Do not turn provisional results into final claims" not in completed_text
    assert "Use ready Week 2 result claims only with the sanity check and source evidence refs." in completed_text
