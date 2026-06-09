"""Tests for SSRP paper claim-register generation."""

from pathlib import Path

from consent_audit.paper_claims import export_ssrp_claim_register


def test_export_ssrp_claim_register_tracks_supported_provisional_and_blocked_claims(
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
        "- Capture status: `scheduled_date_not_reached`\n",
        encoding="utf-8",
    )
    out_md = tmp_path / "claim_register.md"

    text = export_ssrp_claim_register(
        targets_csv=targets,
        audit_summary_csv=audit_summary,
        longitudinal_summary_csv=longitudinal,
        cmp_confirmation_csv=confirmations,
        results_tables_md=tmp_path / "results_tables.md",
        paper_skeleton_md=tmp_path / "paper_skeleton.md",
        figure_plan_md=tmp_path / "figure_plan.md",
        writing_pack_md=tmp_path / "writing_pack.md",
        cycle_report_md=cycle_report,
        out_md=out_md,
        title="SSRP Claim Register",
        week_label="Week 2",
    )

    assert out_md.read_text(encoding="utf-8") == text
    assert "# SSRP Claim Register" in text
    assert "- Target sites: 2" in text
    assert "- RQ1 reports available for targets: 2/2" in text
    assert "- RQ2 summaries available for targets: 2/2" in text
    assert "- Claim mode: provisional" in text
    assert "## Claim Register" in text
    assert (
        "| C1 | Methods | The project implements a traceable three-layer consent-interface audit workflow. | "
        "Supported |"
    ) in text
    assert (
        "| C2 | RQ1 | Current RQ1 evidence covers 2/2 Week 2 targets. | "
        "Provisional |"
    ) in text
    assert (
        "| C4 | RQ1 | Banner-present automated tiers are Compliant=1; "
        "no-visible-banner contrast candidates=1; raw automated tiers are "
        "Compliant=1, High-Risk=1. | Provisional |"
    ) in text
    assert "| C5 | RQ2 | Latest longitudinal severity levels are A=1, D=1. | Provisional |" in text
    assert (
        "| C7 | Limitations | pending CMP/manual-review confirmations remain unresolved: "
        "confirmed=1, pending=1. | Open limitation |"
    ) in text
    assert (
        "| C8 | Final results | Final Week 2 result claims are not available until live capture "
        "and sanity confirmation. | Blocked |"
    ) in text
    assert "## Blocked Claims" in text
    assert "Final Week 2 result claims" in text
    assert f"- Writing pack: `{tmp_path / 'writing_pack.md'}`" in text
    assert f"- Cycle report: `{cycle_report}`" in text

    cycle_report.write_text(
        "# Week 2 Cycle Report\n\n"
        "- Capture status: completed\n",
        encoding="utf-8",
    )
    completed_text = export_ssrp_claim_register(
        targets_csv=targets,
        audit_summary_csv=audit_summary,
        longitudinal_summary_csv=longitudinal,
        cmp_confirmation_csv=confirmations,
        results_tables_md=tmp_path / "results_tables.md",
        paper_skeleton_md=tmp_path / "paper_skeleton.md",
        figure_plan_md=tmp_path / "figure_plan.md",
        writing_pack_md=tmp_path / "writing_pack.md",
        cycle_report_md=cycle_report,
        out_md=out_md,
        title="SSRP Claim Register",
        week_label="Week 2",
    )

    assert (
        "| C8 | Final results | Week 2 live capture and sanity confirmation are complete "
        "for the current evidence gate. | Ready |"
    ) in completed_text
    assert "Final Week 2 result claims are not available" not in completed_text
    assert "Run scheduled `week2-cycle`" not in completed_text
