"""Tests for SSRP paper skeleton generation."""

import json
from pathlib import Path

from consent_audit.paper_skeleton import export_ssrp_paper_skeleton


def test_export_ssrp_paper_skeleton_turns_research_package_into_draft(
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
        "https://example.com,2026-06-06,B,1,copy_change,0.20,false,false,true,"
        "false,false,Copy changed,Review text\n"
        "https://example.com,2026-06-06,D,2,copy_change|pathway_change,1.00,true,"
        "false,true,false,false,Path changed,Review paths\n"
        "https://stable.example,2026-06-06,A,0,,0.00,false,false,false,false,"
        "false,No detected consent-interface changes,No follow-up required\n",
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
    out_md = tmp_path / "paper_skeleton.md"

    text = export_ssrp_paper_skeleton(
        targets_csv=targets,
        audit_summary_csv=audit_summary,
        longitudinal_summary_csv=longitudinal,
        manifest_json=manifest,
        out_md=out_md,
        title="SSRP Paper Skeleton",
        week_label="Week 2",
    )

    assert out_md.read_text(encoding="utf-8") == text
    assert "# SSRP Paper Skeleton" in text
    assert "How to develop a computational audit and scoring system" in text
    assert "How can we automatically capture and version" in text
    assert "- Target sites: 2" in text
    assert "- Categories: food=1, news=1" in text
    assert "- Audit reports in package: 3" in text
    assert "- Longitudinal summaries in package: 2" in text
    assert "- Banner evidence classes: banner_present=1, no_visible_banner=1" in text
    assert "- Banner-present automated tiers: Compliant=1" in text
    assert "- Raw automated target tiers: Compliant=1, High-Risk=1" in text
    assert "- Latest longitudinal severity: A=1, D=1" in text
    assert (
        "| Example | news | banner/control evidence | banner-present scored case | "
        "Compliant | Accept+Reject+Customize | D / 2 |"
    ) in text
    assert (
        "| Stable | food | no visible first-screen banner | "
        "no-visible-banner contrast; do not treat as banner-path failure | "
        "High-Risk | missing accept\\|reject\\|customize\\|dismiss | A / 0 |"
    ) in text
    assert "## Results Tables To Fill" in text
    assert "ssrp-results-tables" in text
    assert "ssrp-writing-pack" in text
    assert "## Figure Queue" in text
    assert "ssrp-figure-plan" in text
    assert "## Known Gaps Before Draft Freeze" in text
    assert f"- Targets: `{targets}`" in text
    assert f"- RQ1 table: `{audit_summary}`" in text
    assert f"- RQ2 table: `{longitudinal}`" in text
    assert f"- Manifest: `{manifest}`" in text
