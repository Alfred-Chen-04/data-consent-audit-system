"""Tests for advisor-facing weekly update briefs."""

import json
from pathlib import Path

from consent_audit.advisor_brief import export_weekly_advisor_brief


def test_export_weekly_advisor_brief_summarizes_targets_and_review_status(
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
        "https://example.com,2026-06-06,B,1,copy_change,0.20,false,false,true,"
        "false,false,Copy changed,Review text\n"
        "https://stable.example,2026-06-06,A,0,,0.00,false,false,false,false,"
        "false,No detected consent-interface changes,No follow-up required\n",
        encoding="utf-8",
    )
    confirmation = tmp_path / "confirmation.csv"
    confirmation.write_text(
        "url,name,category,cohort,draft_decision,draft_confidence,"
        "source_auto_suggestion,draft_rationale,recommended_next_step,"
        "confirmation_status,confirmed_decision,manual_banner_observed,"
        "manual_cmp_vendor,reviewer,reviewed_at,reviewer_notes\n"
        "https://pending.example,Pending,news,pilot,keep_no_banner_case,low,"
        "rerun,rationale,next,pending,,,,,,\n"
        "https://confirmed.example,Confirmed,finance,pilot,replace_candidate,medium,"
        "keep_no_banner_case,rationale,next,confirmed,replace_candidate,false,,"
        "Advisor,2026-06-01,Replace it\n",
        encoding="utf-8",
    )
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "audit_report_count": 3,
                "weekly_summary_count": 2,
                "generated_at": "2026-06-06T12:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )
    out_md = tmp_path / "advisor_update.md"

    text = export_weekly_advisor_brief(
        targets_csv=targets,
        audit_summary_csv=audit_summary,
        longitudinal_summary_csv=longitudinal,
        cmp_confirmation_csv=confirmation,
        manifest_json=manifest,
        out_md=out_md,
        title="Week 2 Advisor Update",
    )

    assert out_md.read_text(encoding="utf-8") == text
    assert "# Week 2 Advisor Update" in text
    assert "- Target sites: 2" in text
    assert "- Audit reports in package: 3" in text
    assert "- Longitudinal summaries in package: 2" in text
    assert "- CMP confirmations: confirmed=1, pending=1" in text
    assert "- Draft CMP decisions: keep_no_banner_case=1, replace_candidate=1" in text
    assert "| Example | news | Compliant | Accept+Reject+Customize | B / 1 |" in text
    assert "| Stable | food | High-Risk | missing accept\\|reject\\|customize\\|dismiss | A / 0 |" in text
    assert "Confirm pending CMP rows before changing sample-lock status." in text
