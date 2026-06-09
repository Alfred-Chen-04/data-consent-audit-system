"""Tests for CMP/manual review queue exports."""

import csv
from pathlib import Path

from consent_audit.cmp_review import (
    apply_cmp_review_confirmations_to_worksheet,
    build_cmp_review_confirmation_sheet,
    build_cmp_review_decision_draft,
    build_cmp_review_queue,
    build_cmp_review_suggestions,
    build_cmp_review_worksheet,
    export_cmp_review_confirmation_sheet_to_csv,
    export_cmp_review_decision_draft_to_csv,
    export_cmp_review_packet,
    export_cmp_review_queue_to_csv,
    export_cmp_review_rerun_targets,
    export_cmp_review_suggestions_to_csv,
    export_cmp_review_worksheet_to_csv,
    summarize_cmp_review_decision_draft,
    summarize_cmp_review_queue,
    summarize_cmp_review_suggestions,
    summarize_cmp_review_worksheet,
)


def test_build_cmp_review_queue_filters_and_enriches_evidence(tmp_path: Path) -> None:
    readiness = tmp_path / "readiness.csv"
    readiness.write_text(
        "url,name,category,cohort,candidate_status,selection_reason,"
        "access_http_status,access_loaded,access_banner_detected,access_block_signal,"
        "access_screenshot_path,capture_observed,capture_date,consent_banner_detected,"
        "layer1_gate_passed,tier,readiness_status,readiness_notes\n"
        "https://www.bbc.com,BBC,news,smoke,pending_review,Known candidate,"
        "200,true,false,,captures/access/bbc.png,true,2026-05-29,false,"
        "false,High-Risk,needs_cmp_review,"
        "no banner observed; verify whether this site fits the consent sample\n"
        "https://www.theguardian.com,The Guardian,news,smoke,pending_review,"
        "Banner detected,200,true,true,,captures/access/guardian.png,true,"
        "2026-05-29,false,false,High-Risk,pilot_ready,"
        "access and weekly capture available\n",
        encoding="utf-8",
    )
    consent_table = tmp_path / "consent_table.csv"
    consent_table.write_text(
        "url,capture_date,captured_at,cohort,banner_detected,accept_available,"
        "reject_available,customize_available,dismiss_available,layer1_gate_passed,"
        "first_screenshot_ref,first_dom_snapshot_ref,dom_hash,image_hash,"
        "layer2_mean_effort,layer2_overall_category,transparency_grade,"
        "unbiased_choice_grade,tier,notes\n"
        "https://www.bbc.com/,2026-05-29,2026-05-29T00:00:00+00:00,"
        "smoke-2026-05-29,false,false,false,false,false,false,"
        "data/captures/sites/bbc/layer1.png,data/captures/sites/bbc/layer1.html,"
        "domhash,imagehash,,,,High-Risk,\n",
        encoding="utf-8",
    )

    rows = build_cmp_review_queue(readiness, consent_table)

    assert len(rows) == 1
    row = rows[0]
    assert row.url == "https://www.bbc.com"
    assert row.name == "BBC"
    assert row.category == "news"
    assert row.access_screenshot_path == "captures/access/bbc.png"
    assert row.capture_screenshot_ref == "data/captures/sites/bbc/layer1.png"
    assert row.capture_dom_snapshot_ref == "data/captures/sites/bbc/layer1.html"
    assert row.dom_hash == "domhash"
    assert row.image_hash == "imagehash"
    assert row.review_reason == (
        "no banner observed in access probe or weekly capture; inspect saved "
        "screenshots/DOM to verify CMP presence, region behavior, or sample fit"
    )
    assert row.recommended_action == (
        "manual screenshot/DOM review; rerun with fresh browser context if a "
        "CMP is expected"
    )


def test_export_cmp_review_queue_to_csv_and_summary(tmp_path: Path) -> None:
    readiness = tmp_path / "readiness.csv"
    readiness.write_text(
        "url,name,category,cohort,candidate_status,selection_reason,"
        "access_http_status,access_loaded,access_banner_detected,access_block_signal,"
        "access_screenshot_path,capture_observed,capture_date,consent_banner_detected,"
        "layer1_gate_passed,tier,readiness_status,readiness_notes\n"
        "https://www.amazon.com,Amazon,ecommerce,pilot,pending_review,"
        "Large ecommerce site,202,true,false,,captures/access/amazon.png,true,"
        "2026-05-30,false,false,High-Risk,needs_cmp_review,"
        "no banner observed; verify whether this site fits the consent sample\n",
        encoding="utf-8",
    )
    consent_table = tmp_path / "consent_table.csv"
    consent_table.write_text(
        "url,capture_date,first_screenshot_ref,first_dom_snapshot_ref,"
        "dom_hash,image_hash,banner_detected,tier\n"
        "https://www.amazon.com/,2026-05-30,"
        "data/captures/amazon/layer1.png,data/captures/amazon/layer1.html,"
        "dom,image,false,High-Risk\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "cmp_review_queue.csv"

    rows = build_cmp_review_queue(readiness, [consent_table])
    export_cmp_review_queue_to_csv(out_csv, rows)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    assert summarize_cmp_review_queue(rows) == {"needs_cmp_review": 1}
    assert exported[0]["url"] == "https://www.amazon.com"
    assert exported[0]["access_banner_detected"] == "false"
    assert exported[0]["capture_observed"] == "true"
    assert exported[0]["capture_screenshot_ref"] == "data/captures/amazon/layer1.png"


def test_build_cmp_review_worksheet_adds_manual_decision_columns(
    tmp_path: Path,
) -> None:
    queue = tmp_path / "cmp_review_queue.csv"
    queue.write_text(
        "url,name,category,cohort,readiness_status,readiness_notes,"
        "access_banner_detected,consent_banner_detected,capture_observed,"
        "capture_date,tier,access_screenshot_path,capture_screenshot_ref,"
        "capture_dom_snapshot_ref,dom_hash,image_hash,review_reason,"
        "recommended_action\n"
        "https://www.bbc.com,BBC,news,smoke,needs_cmp_review,"
        "no banner observed,false,false,true,2026-05-29,High-Risk,"
        "captures/access/bbc.png,data/captures/bbc/layer1.png,"
        "data/captures/bbc/layer1.html,domhash,imagehash,"
        "inspect saved screenshots,manual screenshot/DOM review\n",
        encoding="utf-8",
    )

    rows = build_cmp_review_worksheet(queue)

    assert len(rows) == 1
    row = rows[0]
    assert row.url == "https://www.bbc.com"
    assert row.name == "BBC"
    assert row.access_screenshot_path == "captures/access/bbc.png"
    assert row.capture_screenshot_ref == "data/captures/bbc/layer1.png"
    assert row.decision_options == (
        "keep_consent_sample|keep_no_banner_case|rerun_fresh_context|"
        "replace_candidate|exclude"
    )
    assert row.manual_banner_observed == ""
    assert row.manual_cmp_vendor == ""
    assert row.sample_decision == ""
    assert row.reviewer_notes == ""
    assert row.review_question == (
        "Inspect the access and capture evidence; decide whether this is a "
        "true no-banner case, a missed CMP, or a candidate to rerun/replace."
    )


def test_export_cmp_review_worksheet_to_csv_and_summary(tmp_path: Path) -> None:
    queue = tmp_path / "cmp_review_queue.csv"
    queue.write_text(
        "url,name,category,cohort,readiness_status,readiness_notes,"
        "access_banner_detected,consent_banner_detected,capture_observed,"
        "capture_date,tier,access_screenshot_path,capture_screenshot_ref,"
        "capture_dom_snapshot_ref,dom_hash,image_hash,review_reason,"
        "recommended_action\n"
        "https://www.amazon.com,Amazon,ecommerce,pilot,needs_cmp_review,"
        "no banner observed,false,false,true,2026-05-30,High-Risk,"
        "captures/access/amazon.png,data/captures/amazon/layer1.png,"
        "data/captures/amazon/layer1.html,dom,image,"
        "inspect saved screenshots,manual screenshot/DOM review\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "cmp_review_worksheet.csv"

    rows = build_cmp_review_worksheet(queue)
    export_cmp_review_worksheet_to_csv(out_csv, rows)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    assert summarize_cmp_review_worksheet(rows) == {"pending_manual_decision": 1}
    assert exported[0]["url"] == "https://www.amazon.com"
    assert exported[0]["manual_banner_observed"] == ""
    assert exported[0]["sample_decision"] == ""
    assert exported[0]["decision_options"] == (
        "keep_consent_sample|keep_no_banner_case|rerun_fresh_context|"
        "replace_candidate|exclude"
    )


def test_export_cmp_review_packet_writes_static_html_and_markdown(tmp_path: Path) -> None:
    queue = tmp_path / "cmp_review_queue.csv"
    queue.write_text(
        "url,name,category,cohort,readiness_status,readiness_notes,"
        "access_banner_detected,consent_banner_detected,capture_observed,"
        "capture_date,tier,access_screenshot_path,capture_screenshot_ref,"
        "capture_dom_snapshot_ref,dom_hash,image_hash,review_reason,"
        "recommended_action\n"
        "https://www.bbc.com,BBC,news,smoke,needs_cmp_review,"
        "no banner observed,false,false,true,2026-05-29,High-Risk,"
        "captures/access_probe/www_bbc_com.png,"
        "data/captures/sites/www_bbc_com/layer1.png,"
        "data/captures/sites/www_bbc_com/layer1.html,domhash,imagehash,"
        "inspect saved screenshots,manual screenshot/DOM review\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "data" / "cmp_review_packet"

    manifest = export_cmp_review_packet(queue, out_dir, project_root=tmp_path)

    html = (out_dir / "index.html").read_text(encoding="utf-8")
    markdown = (out_dir / "index.md").read_text(encoding="utf-8")

    assert manifest == {
        "row_count": 1,
        "index_html": str(out_dir / "index.html"),
        "index_markdown": str(out_dir / "index.md"),
    }
    assert '<article class="review-card" id="bbc">' in html
    assert "BBC" in html
    assert "https://www.bbc.com" in html
    assert "keep_consent_sample" in html
    assert "manual screenshot/DOM review" in html
    assert 'src="../captures/access_probe/www_bbc_com.png"' in html
    assert 'href="../captures/sites/www_bbc_com/layer1.html"' in html
    assert "![Access probe](../captures/access_probe/www_bbc_com.png)" in markdown
    assert "[Capture DOM](../captures/sites/www_bbc_com/layer1.html)" in markdown


def test_build_cmp_review_suggestions_uses_dom_indicators_without_finalizing_decisions(
    tmp_path: Path,
) -> None:
    dom_dir = tmp_path / "data" / "captures" / "sites"
    dom_dir.mkdir(parents=True)
    (dom_dir / "hidden_cmp.html").write_text(
        "<html><script>window.OneTrust = {}</script><body>Cookie consent preferences</body></html>",
        encoding="utf-8",
    )
    (dom_dir / "plain.html").write_text(
        "<html><body>Welcome to the public home page.</body></html>",
        encoding="utf-8",
    )
    queue = tmp_path / "cmp_review_queue.csv"
    queue.write_text(
        "url,name,category,cohort,readiness_status,readiness_notes,"
        "access_banner_detected,consent_banner_detected,capture_observed,"
        "capture_date,tier,access_screenshot_path,capture_screenshot_ref,"
        "capture_dom_snapshot_ref,dom_hash,image_hash,review_reason,"
        "recommended_action\n"
        "https://hidden.example,Hidden CMP,news,pilot,needs_cmp_review,"
        "no banner observed,false,false,true,2026-05-30,High-Risk,"
        "captures/access/hidden.png,data/captures/sites/hidden.png,"
        "data/captures/sites/hidden_cmp.html,dom,image,inspect,manual review\n"
        "https://plain.example,Plain Site,reference,pilot,needs_cmp_review,"
        "no banner observed,false,false,true,2026-05-30,High-Risk,"
        "captures/access/plain.png,data/captures/sites/plain.png,"
        "data/captures/sites/plain.html,dom,image,inspect,manual review\n"
        "https://banner.example,Banner Site,news,pilot,needs_cmp_review,"
        "probe banner,true,false,true,2026-05-30,High-Risk,"
        "captures/access/banner.png,data/captures/sites/banner.png,"
        "data/captures/sites/plain.html,dom,image,inspect,manual review\n",
        encoding="utf-8",
    )

    rows = build_cmp_review_suggestions(queue, project_root=tmp_path)

    assert [row.url for row in rows] == [
        "https://hidden.example",
        "https://plain.example",
        "https://banner.example",
    ]
    assert rows[0].auto_suggested_decision == "rerun_fresh_context"
    assert rows[0].confidence == "medium"
    assert "onetrust" in rows[0].dom_indicator_terms
    assert "DOM contains CMP/consent indicators" in rows[0].evidence_summary
    assert rows[1].auto_suggested_decision == "keep_no_banner_case"
    assert rows[1].confidence == "low"
    assert rows[2].auto_suggested_decision == "keep_consent_sample"
    assert rows[2].confidence == "high"
    assert all(row.requires_human_confirmation for row in rows)


def test_export_cmp_review_suggestions_to_csv_and_summary(tmp_path: Path) -> None:
    dom_path = tmp_path / "page.html"
    dom_path.write_text("<html><body>cookie preference center</body></html>", encoding="utf-8")
    queue = tmp_path / "cmp_review_queue.csv"
    queue.write_text(
        "url,name,category,cohort,readiness_status,readiness_notes,"
        "access_banner_detected,consent_banner_detected,capture_observed,"
        "capture_date,tier,access_screenshot_path,capture_screenshot_ref,"
        "capture_dom_snapshot_ref,dom_hash,image_hash,review_reason,"
        "recommended_action\n"
        "https://www.amazon.com,Amazon,ecommerce,pilot,needs_cmp_review,"
        "no banner observed,false,false,true,2026-05-30,High-Risk,"
        "captures/access/amazon.png,data/captures/amazon/layer1.png,"
        f"{dom_path},dom,image,inspect,manual screenshot/DOM review\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "cmp_review_suggestions.csv"

    rows = build_cmp_review_suggestions(queue, project_root=tmp_path)
    export_cmp_review_suggestions_to_csv(out_csv, rows)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    assert summarize_cmp_review_suggestions(rows) == {"rerun_fresh_context": 1}
    assert exported[0]["url"] == "https://www.amazon.com"
    assert exported[0]["auto_suggested_decision"] == "rerun_fresh_context"
    assert exported[0]["requires_human_confirmation"] == "true"
    assert "cookie" in exported[0]["dom_indicator_terms"]


def test_export_cmp_review_rerun_targets_writes_weekly_site_list(
    tmp_path: Path,
) -> None:
    suggestions = tmp_path / "cmp_review_suggestions.csv"
    suggestions.write_text(
        "url,name,category,cohort,readiness_status,capture_dom_snapshot_ref,"
        "auto_suggested_decision,confidence,evidence_summary,dom_indicator_terms,"
        "requires_human_confirmation\n"
        "https://www.bbc.com,BBC,news,smoke,needs_cmp_review,bbc.html,"
        "rerun_fresh_context,medium,DOM contains indicators,cookie|consent,true\n"
        "https://www.reddit.com,Reddit,social,smoke,needs_cmp_review,reddit.html,"
        "keep_no_banner_case,low,No indicators,,true\n"
        "https://www.airbnb.com,Airbnb,travel,pilot,needs_cmp_review,airbnb.html,"
        "rerun_fresh_context,medium,DOM contains indicators,onetrust|cookie,true\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "cmp_rerun_targets.csv"

    count = export_cmp_review_rerun_targets(suggestions, out_csv)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    assert count == 2
    assert rows == [
        {
            "url": "https://www.bbc.com",
            "name": "BBC",
            "category": "news",
            "inherited_from_phd_mentor": "false",
            "notes": (
                "cmp_review_suggestion: rerun_fresh_context; confidence=medium; "
                "indicators=cookie|consent"
            ),
        },
        {
            "url": "https://www.airbnb.com",
            "name": "Airbnb",
            "category": "travel",
            "inherited_from_phd_mentor": "false",
            "notes": (
                "cmp_review_suggestion: rerun_fresh_context; confidence=medium; "
                "indicators=onetrust|cookie"
            ),
        },
    ]


def test_build_cmp_review_decision_draft_marks_human_confirmation_required(
    tmp_path: Path,
) -> None:
    queue = tmp_path / "cmp_review_queue.csv"
    queue.write_text(
        "url,name,category,cohort,readiness_status,readiness_notes,"
        "access_banner_detected,consent_banner_detected,capture_observed,"
        "capture_date,tier,access_screenshot_path,capture_screenshot_ref,"
        "capture_dom_snapshot_ref,dom_hash,image_hash,review_reason,"
        "recommended_action\n"
        "https://www.bbc.com,BBC,news,smoke,needs_cmp_review,"
        "no banner observed,false,false,true,2026-05-29,High-Risk,"
        "captures/access/bbc.png,data/captures/bbc/layer1.png,"
        "data/captures/bbc/layer1.html,dom,image,inspect,manual review\n"
        "https://www.reddit.com,Reddit,social,smoke,needs_cmp_review,"
        "security block,false,false,true,2026-05-29,High-Risk,"
        "captures/access/reddit.png,data/captures/reddit/layer1.png,"
        "data/captures/reddit/layer1.html,dom,image,inspect,manual review\n"
        "https://www.walmart.com,Walmart,ecommerce,pilot,needs_cmp_review,"
        "robot challenge,false,false,true,2026-05-29,High-Risk,"
        "captures/access/walmart.png,data/captures/walmart/layer1.png,"
        "data/captures/walmart/layer1.html,dom,image,inspect,manual review\n",
        encoding="utf-8",
    )
    suggestions = tmp_path / "cmp_review_suggestions.csv"
    suggestions.write_text(
        "url,name,category,cohort,readiness_status,capture_dom_snapshot_ref,"
        "auto_suggested_decision,confidence,evidence_summary,"
        "dom_indicator_terms,requires_human_confirmation\n"
        "https://www.bbc.com,BBC,news,smoke,needs_cmp_review,"
        "data/captures/bbc/layer1.html,rerun_fresh_context,medium,"
        "DOM contains CMP indicators,cookie|consent,true\n"
        "https://www.reddit.com,Reddit,social,smoke,needs_cmp_review,"
        "data/captures/reddit/layer1.html,keep_no_banner_case,low,"
        "No indicators,,true\n"
        "https://www.walmart.com,Walmart,ecommerce,pilot,needs_cmp_review,"
        "data/captures/walmart/layer1.html,rerun_fresh_context,medium,"
        "DOM contains privacy choices,cookie|ccpa,true\n",
        encoding="utf-8",
    )

    rows = build_cmp_review_decision_draft(queue, suggestions)

    assert [row.draft_decision for row in rows] == [
        "keep_no_banner_case",
        "replace_candidate",
        "replace_candidate",
    ]
    assert all(row.requires_human_confirmation for row in rows)
    assert rows[0].source_auto_suggestion == "rerun_fresh_context"
    assert "possible no-banner contrast" in rows[0].draft_rationale
    assert "access-friction" in rows[1].draft_rationale
    assert "access-friction" in rows[2].draft_rationale


def test_export_cmp_review_decision_draft_to_csv_and_summary(tmp_path: Path) -> None:
    queue = tmp_path / "cmp_review_queue.csv"
    queue.write_text(
        "url,name,category,cohort,readiness_status,readiness_notes,"
        "access_banner_detected,consent_banner_detected,capture_observed,"
        "capture_date,tier,access_screenshot_path,capture_screenshot_ref,"
        "capture_dom_snapshot_ref,dom_hash,image_hash,review_reason,"
        "recommended_action\n"
        "https://www.spotify.com,Spotify,entertainment,pilot,needs_cmp_review,"
        "no banner observed,false,false,true,2026-05-29,High-Risk,"
        "captures/access/spotify.png,data/captures/spotify/layer1.png,"
        "data/captures/spotify/layer1.html,dom,image,inspect,manual review\n",
        encoding="utf-8",
    )
    suggestions = tmp_path / "cmp_review_suggestions.csv"
    suggestions.write_text(
        "url,name,category,cohort,readiness_status,capture_dom_snapshot_ref,"
        "auto_suggested_decision,confidence,evidence_summary,"
        "dom_indicator_terms,requires_human_confirmation\n"
        "https://www.spotify.com,Spotify,entertainment,pilot,needs_cmp_review,"
        "data/captures/spotify/layer1.html,rerun_fresh_context,medium,"
        "DOM contains cookie,cookie,true\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "decision_draft.csv"

    rows = build_cmp_review_decision_draft(queue, suggestions)
    export_cmp_review_decision_draft_to_csv(out_csv, rows)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    assert summarize_cmp_review_decision_draft(rows) == {"keep_no_banner_case": 1}
    assert exported[0]["url"] == "https://www.spotify.com"
    assert exported[0]["draft_decision"] == "keep_no_banner_case"
    assert exported[0]["requires_human_confirmation"] == "true"
    assert exported[0]["source_auto_suggestion"] == "rerun_fresh_context"


def test_build_cmp_review_confirmation_sheet_requires_explicit_confirmation(
    tmp_path: Path,
) -> None:
    draft = tmp_path / "decision_draft.csv"
    draft.write_text(
        "url,name,category,cohort,draft_decision,draft_confidence,"
        "source_auto_suggestion,draft_rationale,recommended_next_step,"
        "requires_human_confirmation\n"
        "https://www.bbc.com,BBC,news,smoke,keep_no_banner_case,low,"
        "rerun_fresh_context,possible no-banner contrast,"
        "human reviewer should confirm,true\n",
        encoding="utf-8",
    )

    rows = build_cmp_review_confirmation_sheet(draft)

    assert len(rows) == 1
    assert rows[0].url == "https://www.bbc.com"
    assert rows[0].draft_decision == "keep_no_banner_case"
    assert rows[0].confirmation_status == "pending"
    assert rows[0].confirmed_decision == ""
    assert rows[0].reviewer == ""
    assert rows[0].reviewer_notes == ""


def test_export_confirmation_sheet_and_apply_confirmed_rows_to_worksheet(
    tmp_path: Path,
) -> None:
    draft = tmp_path / "decision_draft.csv"
    draft.write_text(
        "url,name,category,cohort,draft_decision,draft_confidence,"
        "source_auto_suggestion,draft_rationale,recommended_next_step,"
        "requires_human_confirmation\n"
        "https://www.bbc.com,BBC,news,smoke,keep_no_banner_case,low,"
        "rerun_fresh_context,possible no-banner contrast,"
        "human reviewer should confirm,true\n"
        "https://www.reddit.com,Reddit,social,smoke,replace_candidate,medium,"
        "keep_no_banner_case,access friction,replace unless kept,true\n",
        encoding="utf-8",
    )
    confirmation_csv = tmp_path / "confirmation.csv"

    rows = build_cmp_review_confirmation_sheet(draft)
    export_cmp_review_confirmation_sheet_to_csv(confirmation_csv, rows)

    with confirmation_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    exported[0]["confirmation_status"] = "confirmed"
    exported[0]["confirmed_decision"] = "keep_no_banner_case"
    exported[0]["manual_banner_observed"] = "false"
    exported[0]["manual_cmp_vendor"] = "none observed"
    exported[0]["reviewer"] = "Advisor"
    exported[0]["reviewed_at"] = "2026-06-01"
    exported[0]["reviewer_notes"] = "Keep as a no-banner contrast case."
    with confirmation_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=exported[0].keys())
        writer.writeheader()
        writer.writerows(exported)

    worksheet = tmp_path / "worksheet.csv"
    worksheet.write_text(
        "url,name,category,cohort,readiness_status,access_screenshot_path,"
        "capture_screenshot_ref,capture_dom_snapshot_ref,review_reason,"
        "recommended_action,review_question,decision_options,"
        "manual_banner_observed,manual_cmp_vendor,sample_decision,reviewer,"
        "reviewed_at,reviewer_notes\n"
        "https://www.bbc.com,BBC,news,smoke,needs_cmp_review,"
        "captures/access/bbc.png,data/captures/bbc/layer1.png,"
        "data/captures/bbc/layer1.html,inspect,manual review,"
        "question,options,,,,,,\n"
        "https://www.reddit.com,Reddit,social,smoke,needs_cmp_review,"
        "captures/access/reddit.png,data/captures/reddit/layer1.png,"
        "data/captures/reddit/layer1.html,inspect,manual review,"
        "question,options,,,,,,\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "worksheet_confirmed.csv"

    summary = apply_cmp_review_confirmations_to_worksheet(
        worksheet,
        confirmation_csv,
        out_csv,
    )

    with out_csv.open(newline="", encoding="utf-8") as fh:
        updated = list(csv.DictReader(fh))

    assert summary == {"applied": 1, "pending": 1}
    assert updated[0]["sample_decision"] == "keep_no_banner_case"
    assert updated[0]["manual_banner_observed"] == "false"
    assert updated[0]["manual_cmp_vendor"] == "none observed"
    assert updated[0]["reviewer"] == "Advisor"
    assert updated[0]["reviewed_at"] == "2026-06-01"
    assert updated[0]["reviewer_notes"] == "Keep as a no-banner contrast case."
    assert updated[1]["sample_decision"] == ""


def test_apply_cmp_review_confirmations_counts_invalid_and_unknown_rows(
    tmp_path: Path,
) -> None:
    worksheet = tmp_path / "worksheet.csv"
    worksheet.write_text(
        "url,name,category,cohort,readiness_status,access_screenshot_path,"
        "capture_screenshot_ref,capture_dom_snapshot_ref,review_reason,"
        "recommended_action,review_question,decision_options,"
        "manual_banner_observed,manual_cmp_vendor,sample_decision,reviewer,"
        "reviewed_at,reviewer_notes\n"
        "https://www.bbc.com,BBC,news,smoke,needs_cmp_review,"
        "captures/access/bbc.png,data/captures/bbc/layer1.png,"
        "data/captures/bbc/layer1.html,inspect,manual review,"
        "question,options,,,,,,\n",
        encoding="utf-8",
    )
    confirmation = tmp_path / "confirmation.csv"
    confirmation.write_text(
        "url,name,category,cohort,draft_decision,draft_confidence,"
        "draft_rationale,recommended_next_step,confirmation_status,"
        "confirmed_decision,manual_banner_observed,manual_cmp_vendor,"
        "reviewer,reviewed_at,reviewer_notes\n"
        "https://www.bbc.com,BBC,news,smoke,keep_no_banner_case,low,"
        "rationale,next,confirmed,not_a_valid_decision,false,,Advisor,"
        "2026-06-01,Invalid decision\n"
        "https://unknown.example,Unknown,news,smoke,keep_no_banner_case,low,"
        "rationale,next,confirmed,exclude,false,,Advisor,2026-06-01,"
        "No matching worksheet row\n",
        encoding="utf-8",
    )

    summary = apply_cmp_review_confirmations_to_worksheet(
        worksheet,
        confirmation,
        tmp_path / "out.csv",
    )

    assert summary == {"invalid_decision": 1, "unknown_url": 1}
