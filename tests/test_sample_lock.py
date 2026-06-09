"""Tests for sample-lock planning exports."""

import csv
from pathlib import Path

from consent_audit.sample_lock import (
    build_sample_lock_plan,
    export_sample_lock_plan_to_csv,
    export_sample_lock_queues,
    export_weekly_targets_from_queues,
    summarize_sample_lock_plan,
)


def test_build_sample_lock_plan_merges_readiness_and_manual_decisions(
    tmp_path: Path,
) -> None:
    readiness = tmp_path / "readiness.csv"
    readiness.write_text(
        "url,name,category,cohort,candidate_status,selection_reason,"
        "access_http_status,access_loaded,access_banner_detected,access_block_signal,"
        "access_screenshot_path,capture_observed,capture_date,consent_banner_detected,"
        "layer1_gate_passed,tier,readiness_status,readiness_notes\n"
        "https://www.theguardian.com,The Guardian,news,smoke,pending_review,"
        "Banner detected,200,true,true,,captures/access/guardian.png,true,"
        "2026-05-29,false,false,High-Risk,pilot_ready,"
        "access and weekly capture available\n"
        "https://www.bbc.com,BBC,news,smoke,pending_review,No banner,200,true,"
        "false,,captures/access/bbc.png,true,2026-05-29,false,false,"
        "High-Risk,needs_cmp_review,no banner observed\n"
        "https://www.nytimes.com,New York Times,news,smoke,pending_review,"
        "No banner comparison,200,true,false,,captures/access/nyt.png,true,"
        "2026-05-29,false,false,High-Risk,needs_cmp_review,"
        "no banner observed\n"
        "https://www.booking.com,Booking.com,travel,pilot,pending_review,"
        "Capture failed,202,true,true,,captures/access/booking.png,false,,"
        "false,false,,needs_weekly_capture,"
        "access probe exists but no weekly capture row found\n"
        "https://www.wikipedia.org,Wikipedia,reference,smoke,pending_review,"
        "Control,200,true,false,,captures/access/wiki.png,true,2026-05-29,"
        "false,false,High-Risk,control_candidate,"
        "no banner observed; keep only as control if intentional\n"
        "https://www.reuters.com,Reuters,news,smoke,pending_review,"
        "Blocked canary,401,false,false,http_401,captures/access/reuters.png,"
        "true,2026-05-29,false,false,High-Risk,access_blocked,"
        "access blocked: http_401\n",
        encoding="utf-8",
    )
    worksheet = tmp_path / "worksheet.csv"
    worksheet.write_text(
        "url,name,category,cohort,readiness_status,access_screenshot_path,"
        "capture_screenshot_ref,capture_dom_snapshot_ref,review_reason,"
        "recommended_action,review_question,decision_options,"
        "manual_banner_observed,manual_cmp_vendor,sample_decision,reviewer,"
        "reviewed_at,reviewer_notes\n"
        "https://www.bbc.com,BBC,news,smoke,needs_cmp_review,"
        "captures/access/bbc.png,data/captures/bbc/layer1.png,"
        "data/captures/bbc/layer1.html,inspect evidence,manual review,"
        "question,options,,,,,,\n"
        "https://www.nytimes.com,New York Times,news,smoke,needs_cmp_review,"
        "captures/access/nyt.png,data/captures/nyt/layer1.png,"
        "data/captures/nyt/layer1.html,inspect evidence,manual review,"
        "question,options,true,OneTrust,keep_no_banner_case,Alfred,"
        "2026-05-30,Clear no-banner comparison case\n",
        encoding="utf-8",
    )

    rows = build_sample_lock_plan(readiness, worksheet)

    assert [row.lock_status for row in rows] == [
        "provisionally_selected",
        "pending_manual_review",
        "selected_no_banner_case",
        "needs_capture_rerun",
        "optional_control",
        "blocked_review_or_replace",
    ]
    assert rows[0].next_action == "include in shortlist and continue weekly capture"
    assert rows[1].next_action == "fill CMP review worksheet before sample lock"
    assert rows[1].capture_screenshot_ref == "data/captures/bbc/layer1.png"
    assert rows[2].worksheet_decision == "keep_no_banner_case"
    assert rows[2].lock_notes == "Clear no-banner comparison case"
    assert rows[3].next_action == "rerun weekly capture with fresh context or longer timeout"
    assert rows[4].priority == 4
    assert rows[5].next_action == "review access feasibility; replace unless kept as blocked canary"


def test_export_sample_lock_plan_to_csv_and_summary(tmp_path: Path) -> None:
    readiness = tmp_path / "readiness.csv"
    readiness.write_text(
        "url,name,category,cohort,candidate_status,selection_reason,"
        "access_http_status,access_loaded,access_banner_detected,access_block_signal,"
        "access_screenshot_path,capture_observed,capture_date,consent_banner_detected,"
        "layer1_gate_passed,tier,readiness_status,readiness_notes\n"
        "https://www.cnn.com,CNN,news,pilot,pending_review,Banner,200,true,"
        "true,,captures/access/cnn.png,true,2026-05-30,false,false,"
        "High-Risk,pilot_ready,access and weekly capture available\n",
        encoding="utf-8",
    )
    worksheet = tmp_path / "worksheet.csv"
    worksheet.write_text(
        "url,name,category,cohort,readiness_status,access_screenshot_path,"
        "capture_screenshot_ref,capture_dom_snapshot_ref,review_reason,"
        "recommended_action,review_question,decision_options,"
        "manual_banner_observed,manual_cmp_vendor,sample_decision,reviewer,"
        "reviewed_at,reviewer_notes\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "sample_lock_plan.csv"

    rows = build_sample_lock_plan(readiness, worksheet)
    export_sample_lock_plan_to_csv(out_csv, rows)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    assert summarize_sample_lock_plan(rows) == {"provisionally_selected": 1}
    assert exported == [
        {
            "url": "https://www.cnn.com",
            "name": "CNN",
            "category": "news",
            "cohort": "pilot",
            "readiness_status": "pilot_ready",
            "worksheet_decision": "",
            "lock_status": "provisionally_selected",
            "priority": "1",
            "next_action": "include in shortlist and continue weekly capture",
            "access_screenshot_path": "captures/access/cnn.png",
            "capture_screenshot_ref": "",
            "capture_dom_snapshot_ref": "",
            "lock_notes": "access and weekly capture available",
        }
    ]


def test_export_sample_lock_queues_splits_action_files(tmp_path: Path) -> None:
    lock_plan = tmp_path / "sample_lock_plan.csv"
    lock_plan.write_text(
        "url,name,category,cohort,readiness_status,worksheet_decision,"
        "lock_status,priority,next_action,access_screenshot_path,"
        "capture_screenshot_ref,capture_dom_snapshot_ref,lock_notes\n"
        "https://www.theguardian.com,The Guardian,news,smoke,pilot_ready,,"
        "provisionally_selected,1,include in shortlist,captures/guardian.png,,,"
        "ready\n"
        "https://www.nytimes.com,New York Times,news,smoke,needs_cmp_review,,"
        "pending_manual_review,2,fill worksheet,captures/nyt.png,"
        "captures/nyt/layer1.png,captures/nyt/layer1.html,pending\n"
        "https://www.booking.com,Booking.com,travel,pilot,needs_weekly_capture,,"
        "needs_capture_rerun,2,rerun capture,captures/booking.png,,,"
        "capture failed\n"
        "https://www.reuters.com,Reuters,news,smoke,access_blocked,,"
        "blocked_review_or_replace,3,review access,captures/reuters.png,,,"
        "http_401\n"
        "https://www.wikipedia.org,Wikipedia,reference,smoke,control_candidate,,"
        "optional_control,4,optional control,captures/wiki.png,,,control\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "queues"

    manifest = export_sample_lock_queues(lock_plan, out_dir)

    assert manifest == {
        "weekly_capture_shortlist": 1,
        "manual_review_queue": 1,
        "rerun_capture_queue": 1,
        "replacement_review_queue": 1,
        "optional_control_queue": 1,
    }

    with (out_dir / "weekly_capture_shortlist.csv").open(
        newline="",
        encoding="utf-8",
    ) as fh:
        weekly_rows = list(csv.DictReader(fh))
    with (out_dir / "manual_review_queue.csv").open(
        newline="",
        encoding="utf-8",
    ) as fh:
        manual_rows = list(csv.DictReader(fh))
    with (out_dir / "queue_manifest.csv").open(newline="", encoding="utf-8") as fh:
        manifest_rows = list(csv.DictReader(fh))

    assert weekly_rows[0]["url"] == "https://www.theguardian.com"
    assert weekly_rows[0]["queue_name"] == "weekly_capture_shortlist"
    assert manual_rows[0]["capture_dom_snapshot_ref"] == "captures/nyt/layer1.html"
    assert manifest_rows == [
        {"queue_name": "weekly_capture_shortlist", "row_count": "1"},
        {"queue_name": "manual_review_queue", "row_count": "1"},
        {"queue_name": "rerun_capture_queue", "row_count": "1"},
        {"queue_name": "replacement_review_queue", "row_count": "1"},
        {"queue_name": "optional_control_queue", "row_count": "1"},
    ]


def test_export_weekly_targets_from_queues_writes_site_list_csv(
    tmp_path: Path,
) -> None:
    queues_dir = tmp_path / "queues"
    queues_dir.mkdir()
    header = (
        "queue_name,url,name,category,cohort,readiness_status,"
        "worksheet_decision,lock_status,priority,next_action,"
        "access_screenshot_path,capture_screenshot_ref,"
        "capture_dom_snapshot_ref,lock_notes\n"
    )
    (queues_dir / "weekly_capture_shortlist.csv").write_text(
        header
        + "weekly_capture_shortlist,https://www.cnn.com,CNN,news,pilot,"
        "pilot_ready,,provisionally_selected,1,continue weekly capture,"
        "captures/cnn.png,,,ready\n",
        encoding="utf-8",
    )
    (queues_dir / "rerun_capture_queue.csv").write_text(
        header
        + "rerun_capture_queue,https://www.booking.com,Booking.com,travel,"
        "pilot,needs_weekly_capture,,needs_capture_rerun,2,rerun capture,"
        "captures/booking.png,,,capture failed\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "weekly_targets.csv"

    count = export_weekly_targets_from_queues(queues_dir, out_csv)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    assert count == 2
    assert exported == [
        {
            "url": "https://www.cnn.com",
            "name": "CNN",
            "category": "news",
            "inherited_from_phd_mentor": "false",
            "notes": "weekly_capture_shortlist: continue weekly capture",
        },
        {
            "url": "https://www.booking.com",
            "name": "Booking.com",
            "category": "travel",
            "inherited_from_phd_mentor": "false",
            "notes": "rerun_capture_queue: rerun capture",
        },
    ]
