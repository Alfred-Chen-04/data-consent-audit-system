"""Tests for SSRP figure-planning artifact generation."""

from pathlib import Path

from consent_audit.paper_figures import export_ssrp_figure_plan


def test_export_ssrp_figure_plan_turns_current_evidence_into_figure_queue(
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
        "layer1_gate_passed,accept_available,reject_available,customize_available,"
        "dismiss_available,missing_paths,layer2_mean_effort,layer2_overall_category,"
        "transparency_grade,unbiased_choice_grade,biased_toward,"
        "first_screenshot_ref,first_dom_snapshot_ref,dom_hash,image_hash,api_cost_usd\n"
        "old,bundle,https://example.com/,2026-05-29,2026-05-29T10:00:00+00:00,"
        "2026-05-29T10:01:00+00:00,High-Risk,false,false,false,false,false,"
        "accept|reject|customize|dismiss,,,,,,old.png,old.html,dom,img,0.0000\n"
        "new,bundle,https://example.com,2026-06-06,2026-06-06T10:00:00+00:00,"
        "2026-06-06T10:01:00+00:00,Compliant,true,true,true,true,false,"
        "dismiss,0.00,Easy,B,A,,new.png,new.html,dom2,img2,0.0000\n"
        "stable,bundle,https://stable.example,2026-06-06,2026-06-06T10:02:00+00:00,"
        "2026-06-06T10:03:00+00:00,High-Risk,false,false,false,false,false,"
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
    cycle_report = tmp_path / "cycle.md"
    cycle_report.write_text(
        "# Week 2 Cycle Report\n\n"
        "- Capture status: `scheduled_date_not_reached`\n"
        "- Cycle mode: `scheduled_date_blocked`\n",
        encoding="utf-8",
    )
    out_md = tmp_path / "figure_plan.md"

    text = export_ssrp_figure_plan(
        targets_csv=targets,
        audit_summary_csv=audit_summary,
        longitudinal_summary_csv=longitudinal,
        results_tables_md=tmp_path / "results_tables.md",
        paper_skeleton_md=tmp_path / "paper_skeleton.md",
        cycle_report_md=cycle_report,
        out_md=out_md,
        title="SSRP Figure Plan",
        week_label="Week 2",
    )

    assert out_md.read_text(encoding="utf-8") == text
    assert "# SSRP Figure Plan" in text
    assert "- Target sites: 2" in text
    assert "- RQ1 figure data available: 2/2" in text
    assert "- RQ2 timeline data available: 2/2" in text
    assert "- Cycle capture status: `scheduled_date_not_reached`" in text
    assert "## Figure Readiness" in text
    assert "| System architecture | Methods | Ready now |" in text
    assert "| Evidence card example | Methods/Findings | Ready as provisional evidence | Example; new.png; new.html |" in text
    assert (
        "| Longitudinal change timeline | RQ2 findings | "
        "Blocked for final paper by live Week 2 capture |"
    ) in text
    assert "## Architecture Diagram Draft" in text
    assert "flowchart LR" in text
    assert "## Timeline Candidates" in text
    assert "| Example | news | D | 2 | copy_change+pathway_change | Review paths |" in text
    assert "| Stable | food | A | 0 | none | No follow-up required |" in text
    assert f"- Results tables: `{tmp_path / 'results_tables.md'}`" in text
    assert f"- Paper skeleton: `{tmp_path / 'paper_skeleton.md'}`" in text
    assert f"- Cycle report: `{cycle_report}`" in text
