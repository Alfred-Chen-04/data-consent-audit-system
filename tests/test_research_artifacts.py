"""Tests for paper-facing research scaffolding files."""

import csv
from pathlib import Path


def test_smoke_site_list_has_week1_probe_size() -> None:
    sites_path = Path("data/sites_smoke.csv")
    with sites_path.open(encoding="utf-8") as fh:
        rows = [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
            and not (row.get("url") or "").strip().startswith("#")
        ]

    assert len(rows) >= 6


def test_deep_sample_candidates_cover_pilot_size_and_categories() -> None:
    candidates_path = Path("data/deep_sample_candidates.csv")
    with candidates_path.open(encoding="utf-8") as fh:
        rows = [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
            and not (row.get("url") or "").strip().startswith("#")
        ]

    urls = [(row.get("url") or "").strip() for row in rows]
    categories = {(row.get("category") or "").strip() for row in rows}
    cohorts = {(row.get("cohort") or "").strip() for row in rows}

    assert 10 <= len(rows) <= 15
    assert len(set(urls)) == len(urls)
    assert "https://example.com" not in urls
    assert "placeholder" not in categories
    assert len(categories) >= 6
    assert "pilot" in cohorts
    assert all((row.get("selection_reason") or "").strip() for row in rows)


def test_pilot_weekly_targets_cover_unblocked_pilot_candidates() -> None:
    readiness_path = Path("data/sample_readiness_pilot_2026-05-30.csv")
    targets_path = Path("data/pilot_weekly_targets_2026-05-30.csv")

    with readiness_path.open(encoding="utf-8") as fh:
        readiness_urls = {
            (row.get("url") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("cohort") or "").strip() == "pilot"
            and (row.get("readiness_status") or "").strip() != "access_blocked"
        }

    with targets_path.open(encoding="utf-8") as fh:
        target_rows = [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
            and not (row.get("url") or "").strip().startswith("#")
        ]

    target_urls = {(row.get("url") or "").strip() for row in target_rows}
    target_notes = " ".join((row.get("notes") or "") for row in target_rows).lower()

    assert target_urls == readiness_urls
    assert len(target_rows) == 8
    assert "blocked" not in target_notes
    assert all((row.get("category") or "").strip() for row in target_rows)


def test_cmp_review_queue_covers_current_manual_review_rows() -> None:
    readiness_path = Path("data/sample_readiness_pilot_2026-05-30.csv")
    queue_path = Path("data/cmp_review_queue_pilot_2026-05-30.csv")

    with readiness_path.open(encoding="utf-8") as fh:
        cmp_review_urls = {
            (row.get("url") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("readiness_status") or "").strip() == "needs_cmp_review"
        }

    with queue_path.open(encoding="utf-8") as fh:
        queue_rows = [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
            and not (row.get("url") or "").strip().startswith("#")
        ]

    queue_urls = {(row.get("url") or "").strip() for row in queue_rows}

    assert queue_urls == cmp_review_urls
    assert len(queue_rows) == 8
    assert all((row.get("access_screenshot_path") or "").strip() for row in queue_rows)
    assert all((row.get("capture_screenshot_ref") or "").strip() for row in queue_rows)
    assert all((row.get("capture_dom_snapshot_ref") or "").strip() for row in queue_rows)
    assert all((row.get("review_reason") or "").strip() for row in queue_rows)
    assert all((row.get("recommended_action") or "").strip() for row in queue_rows)


def test_cmp_review_worksheet_covers_current_queue_rows() -> None:
    queue_path = Path("data/cmp_review_queue_pilot_2026-05-30.csv")
    worksheet_path = Path("data/cmp_review_worksheet_pilot_2026-05-30.csv")

    with queue_path.open(encoding="utf-8") as fh:
        queue_urls = {
            (row.get("url") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        }

    with worksheet_path.open(encoding="utf-8") as fh:
        worksheet_rows = [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]

    worksheet_urls = {(row.get("url") or "").strip() for row in worksheet_rows}

    assert worksheet_urls == queue_urls
    assert len(worksheet_rows) == 8
    assert all((row.get("review_question") or "").strip() for row in worksheet_rows)
    assert all((row.get("decision_options") or "").strip() for row in worksheet_rows)
    assert all((row.get("manual_banner_observed") or "") == "" for row in worksheet_rows)
    assert all((row.get("sample_decision") or "") == "" for row in worksheet_rows)


def test_cmp_review_packet_covers_current_queue_rows() -> None:
    queue_path = Path("data/cmp_review_queue_pilot_2026-05-30.csv")
    packet_dir = Path("data/cmp_review_packet_pilot_2026-05-30")

    with queue_path.open(encoding="utf-8") as fh:
        queue_rows = [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]

    html = (packet_dir / "index.html").read_text(encoding="utf-8")
    markdown = (packet_dir / "index.md").read_text(encoding="utf-8")

    assert html.count('class="review-card"') == len(queue_rows) == 8
    assert "# CMP Manual Review Packet" in markdown
    for row in queue_rows:
        assert (row.get("url") or "").strip() in html
        assert (row.get("name") or "").strip() in html
        assert (row.get("access_screenshot_path") or "").strip().removeprefix("data/") in html
        assert (row.get("capture_dom_snapshot_ref") or "").strip().removeprefix("data/") in html


def test_cmp_review_suggestions_cover_current_queue_rows() -> None:
    queue_path = Path("data/cmp_review_queue_pilot_2026-05-30.csv")
    suggestions_path = Path("data/cmp_review_suggestions_pilot_2026-05-30.csv")

    with queue_path.open(encoding="utf-8") as fh:
        queue_urls = {
            (row.get("url") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        }

    with suggestions_path.open(encoding="utf-8") as fh:
        suggestion_rows = [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]

    suggestion_urls = {(row.get("url") or "").strip() for row in suggestion_rows}
    allowed_decisions = {
        "keep_consent_sample",
        "keep_no_banner_case",
        "rerun_fresh_context",
        "replace_candidate",
        "exclude",
    }

    assert suggestion_urls == queue_urls
    assert len(suggestion_rows) == 8
    assert all(
        (row.get("auto_suggested_decision") or "").strip() in allowed_decisions
        for row in suggestion_rows
    )
    assert all((row.get("confidence") or "").strip() for row in suggestion_rows)
    assert all((row.get("evidence_summary") or "").strip() for row in suggestion_rows)
    assert all((row.get("requires_human_confirmation") or "") == "true" for row in suggestion_rows)


def test_cmp_review_rerun_targets_cover_rerun_suggestions() -> None:
    suggestions_path = Path("data/cmp_review_suggestions_pilot_2026-05-30.csv")
    targets_path = Path("data/cmp_review_rerun_targets_pilot_2026-05-30.csv")

    with suggestions_path.open(encoding="utf-8") as fh:
        rerun_urls = {
            (row.get("url") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("auto_suggested_decision") or "").strip()
            == "rerun_fresh_context"
        }

    with targets_path.open(encoding="utf-8") as fh:
        target_rows = [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]

    target_urls = {(row.get("url") or "").strip() for row in target_rows}

    assert target_urls == rerun_urls
    assert len(target_rows) == 7
    assert all((row.get("inherited_from_phd_mentor") or "") == "false" for row in target_rows)
    assert all("cmp_review_suggestion: rerun_fresh_context" in (row.get("notes") or "") for row in target_rows)
    assert "https://www.reddit.com" not in target_urls


def test_sample_lock_plan_covers_current_readiness_rows() -> None:
    readiness_path = Path("data/sample_readiness_pilot_2026-05-30.csv")
    lock_plan_path = Path("data/sample_lock_plan_pilot_2026-05-30.csv")

    with readiness_path.open(encoding="utf-8") as fh:
        readiness_urls = {
            (row.get("url") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        }

    with lock_plan_path.open(encoding="utf-8") as fh:
        lock_rows = [
            row
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        ]

    lock_urls = {(row.get("url") or "").strip() for row in lock_rows}
    status_counts: dict[str, int] = {}
    for row in lock_rows:
        status = (row.get("lock_status") or "").strip()
        status_counts[status] = status_counts.get(status, 0) + 1

    assert lock_urls == readiness_urls
    assert len(lock_rows) == 15
    assert status_counts == {
        "provisionally_selected": 4,
        "pending_manual_review": 8,
        "optional_control": 1,
        "blocked_review_or_replace": 2,
    }
    assert all((row.get("next_action") or "").strip() for row in lock_rows)
    assert all((row.get("priority") or "").strip() for row in lock_rows)


def test_sample_action_queues_match_current_lock_plan() -> None:
    queues_dir = Path("data/sample_action_queues_pilot_2026-05-30")
    expected_counts = {
        "weekly_capture_shortlist": 4,
        "manual_review_queue": 8,
        "rerun_capture_queue": 0,
        "replacement_review_queue": 2,
        "optional_control_queue": 1,
    }

    with (queues_dir / "queue_manifest.csv").open(encoding="utf-8") as fh:
        manifest_counts = {
            row["queue_name"]: int(row["row_count"])
            for row in csv.DictReader(fh)
        }

    assert manifest_counts == expected_counts

    for queue_name, expected_count in expected_counts.items():
        with (queues_dir / f"{queue_name}.csv").open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert len(rows) == expected_count
        assert all((row.get("queue_name") or "") == queue_name for row in rows)
        assert all((row.get("url") or "").strip() for row in rows)
        assert all((row.get("next_action") or "").strip() for row in rows)


def test_deep_sample_weekly_targets_cover_shortlist_and_rerun_queue() -> None:
    target_path = Path("data/deep_sample_weekly_targets_pilot_2026-05-30.csv")
    queues_dir = Path("data/sample_action_queues_pilot_2026-05-30")

    expected_urls: set[str] = set()
    for queue_name in ["weekly_capture_shortlist", "rerun_capture_queue"]:
        with (queues_dir / f"{queue_name}.csv").open(encoding="utf-8") as fh:
            expected_urls.update(
                (row.get("url") or "").strip()
                for row in csv.DictReader(fh)
                if (row.get("url") or "").strip()
            )

    with target_path.open(encoding="utf-8") as fh:
        target_rows = list(csv.DictReader(fh))

    target_urls = {(row.get("url") or "").strip() for row in target_rows}

    assert target_urls == expected_urls
    assert len(target_rows) == 4
    assert all((row.get("name") or "").strip() for row in target_rows)
    assert all((row.get("category") or "").strip() for row in target_rows)
    assert all((row.get("inherited_from_phd_mentor") or "") == "false" for row in target_rows)
    assert all((row.get("notes") or "").strip() for row in target_rows)


def test_replacement_review_batch2_promotes_only_verified_rows() -> None:
    review_path = Path("data/replacement_review_batch2_2026-05-30.csv")

    with review_path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    status_counts: dict[str, int] = {}
    for row in rows:
        status = (row.get("replacement_status") or "").strip()
        status_counts[status] = status_counts.get(status, 0) + 1

    verified_urls = {
        (row.get("url") or "").strip()
        for row in rows
        if (row.get("replacement_status") or "").strip() == "verified_replacement"
    }

    assert len(rows) == 16
    assert status_counts == {
        "verified_replacement": 1,
        "promising_reprobe": 3,
        "no_banner_or_locale_shift": 3,
        "blocked_or_error": 9,
    }
    assert verified_urls == {"https://www.coca-cola.com/us/en"}


def test_expanded_weekly_targets_add_verified_replacements_to_current_shortlist() -> None:
    base_target_path = Path("data/deep_sample_weekly_targets_pilot_2026-05-30.csv")
    expanded_target_path = Path("data/deep_sample_weekly_targets_expanded_2026-05-30.csv")

    with base_target_path.open(encoding="utf-8") as fh:
        base_urls = {
            (row.get("url") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        }
    with expanded_target_path.open(encoding="utf-8") as fh:
        expanded_rows = list(csv.DictReader(fh))

    expanded_urls = {
        (row.get("url") or "").strip()
        for row in expanded_rows
        if (row.get("url") or "").strip()
    }

    assert expanded_urls == base_urls | {"https://www.coca-cola.com/us/en"}
    assert len(expanded_rows) == 5
    assert all((row.get("name") or "").strip() for row in expanded_rows)
    assert all((row.get("category") or "").strip() for row in expanded_rows)
    assert all((row.get("inherited_from_phd_mentor") or "") == "false" for row in expanded_rows)
    assert any(
        (row.get("url") or "").strip() == "https://www.coca-cola.com/us/en"
        and "verified_replacement" in (row.get("notes") or "")
        for row in expanded_rows
    )


def test_longitudinal_summary_includes_coca_cola_stable_observation() -> None:
    summary_path = Path("data/longitudinal_summary.csv")

    with summary_path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    coca_rows = [
        row
        for row in rows
        if (row.get("url") or "").strip() == "https://www.coca-cola.com/us/en"
    ]

    assert len(coca_rows) == 1
    assert coca_rows[0]["severity"] == "A"
    assert coca_rows[0]["event_count"] == "0"
    assert coca_rows[0]["event_types"] == ""
    assert "No detected consent-interface changes" in coca_rows[0]["summary"]


def test_week2_targets_freeze_expanded_capture_list() -> None:
    expanded_path = Path("data/deep_sample_weekly_targets_expanded_2026-05-30.csv")
    week2_path = Path("data/week2_deep_sample_targets_2026-06-06.csv")

    with expanded_path.open(encoding="utf-8") as fh:
        expanded_rows = list(csv.DictReader(fh))
    with week2_path.open(encoding="utf-8") as fh:
        week2_rows = list(csv.DictReader(fh))

    assert [row["url"] for row in week2_rows] == [row["url"] for row in expanded_rows]
    assert len(week2_rows) == 5
    assert all((row.get("notes") or "").startswith("week2_default_capture:") for row in week2_rows)
    assert "https://www.coca-cola.com/us/en" in {row["url"] for row in week2_rows}


def test_cmp_review_decision_draft_covers_pending_manual_review_rows() -> None:
    queue_path = Path("data/cmp_review_queue_pilot_2026-05-30.csv")
    draft_path = Path("data/cmp_review_decision_draft_pilot_2026-05-30.csv")

    with queue_path.open(encoding="utf-8") as fh:
        queue_urls = {
            (row.get("url") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        }
    with draft_path.open(encoding="utf-8") as fh:
        draft_rows = list(csv.DictReader(fh))

    draft_urls = {
        (row.get("url") or "").strip()
        for row in draft_rows
        if (row.get("url") or "").strip()
    }
    decision_counts: dict[str, int] = {}
    for row in draft_rows:
        decision = (row.get("draft_decision") or "").strip()
        decision_counts[decision] = decision_counts.get(decision, 0) + 1

    assert draft_urls == queue_urls
    assert len(draft_rows) == 8
    assert decision_counts == {"keep_no_banner_case": 6, "replace_candidate": 2}
    assert all((row.get("requires_human_confirmation") or "") == "true" for row in draft_rows)
    assert {
        row["url"]
        for row in draft_rows
        if row["draft_decision"] == "replace_candidate"
    } == {"https://www.reddit.com", "https://www.walmart.com"}


def test_cmp_review_confirmation_sheet_covers_pending_manual_review_rows() -> None:
    draft_path = Path("data/cmp_review_decision_draft_pilot_2026-05-30.csv")
    confirmation_path = Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv")

    with draft_path.open(encoding="utf-8") as fh:
        draft_urls = {
            (row.get("url") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("url") or "").strip()
        }
    with confirmation_path.open(encoding="utf-8") as fh:
        confirmation_rows = list(csv.DictReader(fh))

    confirmation_urls = {
        (row.get("url") or "").strip()
        for row in confirmation_rows
        if (row.get("url") or "").strip()
    }

    assert confirmation_urls == draft_urls
    assert len(confirmation_rows) == 8
    assert all((row.get("confirmation_status") or "") == "pending" for row in confirmation_rows)
    assert all((row.get("confirmed_decision") or "") == "" for row in confirmation_rows)


def test_week2_advisor_update_brief_exists_and_mentions_current_counts() -> None:
    brief_path = Path("docs/research/week2_advisor_update_2026-06-06.md")

    text = brief_path.read_text(encoding="utf-8")

    assert "# Week 2 Advisor Update, 2026-06-06" in text
    assert "- Target sites: 5" in text
    assert "- Audit reports in package: 42" in text
    assert "- Longitudinal summaries in package: 20" in text
    assert "- CMP confirmations: pending=8" in text
    assert "Coca-Cola" in text
    assert "Confirm pending CMP rows before changing sample-lock status." in text


def test_week2_sanity_check_exists_and_reports_completed_capture_gate() -> None:
    sanity_path = Path("docs/research/week2_sanity_check_2026-06-06.md")

    text = sanity_path.read_text(encoding="utf-8")

    assert "# Week 2 Capture Sanity Check, 2026-06-06" in text
    assert "- Cohort: `week2-2026-06-06`" in text
    assert "- Target sites: 5" in text
    assert "- Consent rows captured: 5/5" in text
    assert "- Evidence-complete rows: 5/5" in text
    assert "verify raw DOM file sync separately" in text
    assert "- Matching audit reports: 5/5" in text
    assert "- Weekly summaries present: 5/5" in text
    assert "- Overall status: ready" in text
    assert "Ready for advisor review." in text


def test_week2_checkin_index_exists_and_links_core_artifacts() -> None:
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")

    text = index_path.read_text(encoding="utf-8")

    assert "# Week 2 Advisor Check-in Index, 2026-06-06" in text
    assert "- Week 2 sanity status: `ready`" in text
    assert "[Advisor update](week2_advisor_update_2026-06-06.md)" in text
    assert "[Sanity check](week2_sanity_check_2026-06-06.md)" in text
    assert "[Capture checklist](week2_capture_day_checklist_2026-06-06.md)" in text
    assert "[Cycle report](week2_cycle_report_2026-06-06.md)" in text
    assert "[Research package](../../data/research_package)" in text
    assert "[CMP confirmation sheet](../../data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv)" in text
    assert "[CMP evidence packet](../../data/cmp_review_packet_pilot_2026-05-30/index.html)" in text
    assert "week2-cycle --dry-run" in text
    assert (
        "AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m "
        "consent_audit.cli week2-cycle"
    ) in text
    assert "week2-capture-checklist" in text


def test_week2_capture_day_checklist_exists_and_tracks_operator_gates() -> None:
    checklist_path = Path("docs/research/week2_capture_day_checklist_2026-06-06.md")

    text = checklist_path.read_text(encoding="utf-8")

    assert "# Week 2 Capture-Day Checklist, 2026-06-06" in text
    assert "- Cohort: `week2-2026-06-06`" in text
    assert "- Expected targets: 5" in text
    assert "- Preflight status: `ready_for_capture`" in text
    assert "- Sanity status: `ready`" in text
    assert "- Last cycle mode: `live_capture`" in text
    assert "- Last capture status: `completed`" in text
    assert "- Last capture attempts: 5/5" in text
    assert "[Preflight check](week2_preflight_check_2026-06-06.md)" in text
    assert "[Cycle report](week2_cycle_report_2026-06-06.md)" in text
    assert "week2-cycle --dry-run" in text
    assert "AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-cycle" in text
    assert "- [ ] Confirm every target has screenshot, DOM, hash, and report evidence." in text


def test_week2_preflight_check_exists_and_reports_ready_for_capture() -> None:
    preflight_path = Path("docs/research/week2_preflight_check_2026-06-06.md")

    text = preflight_path.read_text(encoding="utf-8")

    assert "# Week 2 Preflight Check, 2026-06-06" in text
    assert "- Overall status: ready_for_capture" in text
    assert "- Week 2 targets: 5/5" in text
    assert "- Target validation: passed" in text
    assert "- Sanity status: `ready`" in text
    assert "- Audit reports in package: 42" in text
    assert "- Longitudinal summaries in package: 20" in text
    assert "- CMP confirmations: pending=8" in text
    assert "[Check-in index](week2_checkin_index_2026-06-06.md)" in text
    assert "[CMP evidence packet](../../data/cmp_review_packet_pilot_2026-05-30/index.html)" in text


def test_week2_refresh_report_exists_and_records_refreshed_outputs() -> None:
    refresh_path = Path("docs/research/week2_refresh_report_2026-06-06.md")

    text = refresh_path.read_text(encoding="utf-8")

    assert "# Week 2 Refresh Report, 2026-06-06" in text
    assert "- Audit reports in package: 42" in text
    assert "- Longitudinal summaries in package: 20" in text
    assert "- Sanity status: `ready`" in text
    assert "- Preflight status: `ready_for_capture`" in text
    assert "[Research package](../../data/research_package)" in text
    assert "[Advisor update](week2_advisor_update_2026-06-06.md)" in text
    assert "[Week 2 preflight](week2_preflight_check_2026-06-06.md)" in text


def test_schema_status_matches_current_week2_workflow() -> None:
    schema_path = Path("SCHEMA.md")

    text = schema_path.read_text(encoding="utf-8")

    assert "### 9.1 Current executable workflow" in text
    assert "`consent-audit research-status`" in text
    assert "`week2-cycle --dry-run`" in text
    assert "42 audit reports" in text
    assert "20 longitudinal summaries" in text
    assert "### 9.2 Remaining research gates" in text
    assert "Scaffolded but not yet functional" not in text
    assert "implementations stubbed" not in text


def test_ssrp_paper_skeleton_exists_and_uses_current_research_package() -> None:
    skeleton_path = Path("docs/research/ssrp_paper_skeleton_2026-06-06.md")

    text = skeleton_path.read_text(encoding="utf-8")

    assert "# SSRP 2026 Paper Skeleton, 2026-06-06" in text
    assert "## Research Questions" in text
    assert "How to develop a computational audit and scoring system" in text
    assert "- Target sites: 5" in text
    assert "- Categories: finance=1, food=1, news=2, travel=1" in text
    assert "- Audit reports in package: 42" in text
    assert "- Longitudinal summaries in package: 20" in text
    assert "## Current Deep-Sample Evidence Table" in text
    assert "Coca-Cola" in text
    assert "ssrp_results_tables_2026-06-06.md" in text
    assert "## Known Gaps Before Draft Freeze" in text
    assert "Review the completed Week 2 evidence gate" in text


def test_ssrp_results_tables_exist_and_use_current_research_package() -> None:
    tables_path = Path("docs/research/ssrp_results_tables_2026-06-06.md")

    text = tables_path.read_text(encoding="utf-8")

    assert "# SSRP 2026 Results Tables, 2026-06-06" in text
    assert "- Target sites: 5" in text
    assert "- RQ1 reports available for targets: 5/5" in text
    assert "- RQ2 summaries available for targets: 5/5" in text
    assert "- Banner evidence classes: banner_present=2, no_visible_banner=3" in text
    assert "- Banner-present automated tiers: High-Risk=2" in text
    assert "- Raw automated target tiers: High-Risk=5" in text
    assert "## Table 1. RQ1 Consent-Interface Scoring Summary" in text
    assert "## Table 2. RQ2 Longitudinal Change Summary" in text
    assert "no-visible-banner contrast; do not treat as banner-path failure" in text
    assert (
        "| Coca-Cola | food | banner/control evidence | banner-present scored case | "
        "High-Risk | fail | Accept | reject\\|customize\\|dismiss | not scored | missing | missing |"
    ) in text
    assert "| The Guardian | news |" in text
    assert "## Source Tables" in text


def test_ssrp_figure_plan_exists_and_tracks_ready_vs_blocked_figures() -> None:
    figure_path = Path("docs/research/ssrp_figure_plan_2026-06-06.md")

    text = figure_path.read_text(encoding="utf-8")

    assert "# SSRP 2026 Figure Plan, 2026-06-06" in text
    assert "- Target sites: 5" in text
    assert "- RQ1 figure data available: 5/5" in text
    assert "- RQ2 timeline data available: 5/5" in text
    assert "- Cycle capture status: `completed`" in text
    assert "## Figure Readiness" in text
    assert "| System architecture | Methods | Ready now |" in text
    assert "| Evidence card example | Methods/Findings | Ready after sanity review |" in text
    assert "| Longitudinal change timeline | RQ2 findings | Ready after sanity review |" in text
    assert "## Architecture Diagram Draft" in text
    assert "flowchart LR" in text
    assert "## Timeline Candidates" in text
    assert "## Source Artifacts" in text


def test_ssrp_writing_pack_exists_and_marks_ready_claims() -> None:
    writing_path = Path("docs/research/ssrp_writing_pack_2026-06-06.md")

    text = writing_path.read_text(encoding="utf-8")

    assert "# SSRP 2026 Writing Pack, 2026-06-06" in text
    assert "- Target sites: 5" in text
    assert "- RQ1 reports available for targets: 5/5" in text
    assert "- RQ2 summaries available for targets: 5/5" in text
    assert "- Cycle capture status: `completed`" in text
    assert "- Claim status: ready for post-sanity drafting." in text
    assert "## Methods Draft Blocks" in text
    assert "deterministic scoring after schema validation" in text
    assert "## Preliminary Results Notes" in text
    assert "banner-present automated tiers are High-Risk=2" in text
    assert "no-visible-banner contrast candidates=3" in text
    assert "## Discussion And Implication Notes" in text
    assert "small GRC/SOC 2 implication" in text
    assert "## Limitations To Carry Forward" in text
    assert "result claims should cite the sanity check and source evidence references" in text
    assert "pending CMP/manual-review confirmations remain unresolved" in text
    assert "## Source Artifacts" in text


def test_ssrp_claim_register_exists_and_labels_claim_statuses() -> None:
    claim_path = Path("docs/research/ssrp_claim_register_2026-06-06.md")

    text = claim_path.read_text(encoding="utf-8")

    assert "# SSRP 2026 Claim Register, 2026-06-06" in text
    assert "- Target sites: 5" in text
    assert "- RQ1 reports available for targets: 5/5" in text
    assert "- RQ2 summaries available for targets: 5/5" in text
    assert "- Cycle capture status: `completed`" in text
    assert "- Claim mode: ready" in text
    assert "## Claim Register" in text
    assert "| C1 | Methods |" in text
    assert "| C2 | RQ1 | Current RQ1 evidence covers 5/5 Week 2 targets. | Ready |" in text
    assert (
        "| C4 | RQ1 | Banner-present automated tiers are High-Risk=2; "
        "no-visible-banner contrast candidates=3; raw automated tiers are High-Risk=5. | Ready |"
    ) in text
    assert "| C8 | Final results | Week 2 live capture and sanity confirmation are complete for the current evidence gate. | Ready |" in text
    assert "## Blocked Claims" in text
    assert "## Source Artifacts" in text


def test_ssrp_poster_plan_exists_and_marks_week2_gate_ready() -> None:
    poster_path = Path("docs/research/ssrp_poster_plan_2026-06-06.md")

    text = poster_path.read_text(encoding="utf-8")

    assert "# SSRP 2026 Poster Plan, 2026-06-06" in text
    assert "- Target sites: 5" in text
    assert "- RQ1 poster data available: 5/5" in text
    assert "- RQ2 poster data available: 5/5" in text
    assert "- Cycle capture status: `completed`" in text
    assert "- Poster claim status: ready after sanity review." in text
    assert "## Poster Storyboard" in text
    assert "| Pipeline | Center column | Browser capture -> Layer scoring -> AuditReport -> WeeklySummary. |" in text
    assert (
        "| RQ1 evidence | Results band | Banner-present automated tiers: High-Risk=2; "
        "no-visible-banner contrast candidates: 3. |"
    ) in text
    assert "## Figure Assets" in text
    assert "Ready after sanity review" in text
    assert "## Poster Copy Blocks" in text
    assert "## Before Final Poster" in text
    assert "Use the completed Week 2 gate as first evidence, not the final dataset." in text
    assert "## Source Artifacts" in text


def test_current_scope_and_advisor_email_reflect_presentation_poster_deliverable() -> None:
    scope_path = Path("docs/research/current_scope_2026-07-01.md")
    email_path = Path("docs/research/advisor_email_scope_update_2026-07-01.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")

    scope_text = scope_path.read_text(encoding="utf-8")
    email_text = email_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")

    assert "presentation;" in scope_text
    assert "large poster;" in scope_text
    assert "A formal SSRP paper is not required as a summer deliverable" in scope_text
    assert "original RQ1/RQ2 spine" in scope_text
    assert "not as a replacement research question" in scope_text
    assert "Subject: Current project scope and next consent-audit decisions" in email_text
    assert "presentation + large poster + traceable" in readme_text
    assert "advisor_email_scope_update_2026-07-01.md" in readme_text
    assert "[Current scope note, 2026-07-01](current_scope_2026-07-01.md)" in index_text


def test_july2_work_note_and_poster_work_order_are_current_entrypoints() -> None:
    today_path = Path("docs/research/today_work_note_2026-07-02.md")
    work_order_path = Path("docs/research/presentation_poster_work_order_2026-07-02.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")

    today_text = today_path.read_text(encoding="utf-8")
    work_order_text = work_order_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")

    assert "Calendar progress | about 48.6%" in today_text
    assert "0 tracked or filesystem `layer1.html` raw DOM files" in today_text
    assert "There is still no evidence-based reason to run a blind live capture." in today_text
    assert "## Presentation/Poster Story" in work_order_text
    assert "RQ1 computational" in work_order_text
    assert "RQ2 automatic" in work_order_text
    assert "Guardian and Coca-Cola are the current banner-present evidence-card" in work_order_text
    assert "today_work_note_2026-07-02.md" in readme_text
    assert "presentation_poster_work_order_2026-07-02.md" in readme_text
    assert "[Today work note, 2026-07-02](today_work_note_2026-07-02.md)" in index_text


def test_project_inventory_and_poster_story_is_current_entrypoint() -> None:
    inventory_path = Path("docs/research/project_inventory_and_poster_story_2026-07-02.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")

    inventory_text = inventory_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")

    assert 'The project is not "a screenshot project."' in inventory_text
    assert "RQ1: develop a computational audit and scoring system" in inventory_text
    assert "RQ2: automatically capture and version firms' privacy interfaces" in inventory_text
    assert "Screenshots are evidence inputs." in inventory_text
    assert "326 tracked site `layer1.png` screenshots" in inventory_text
    assert "42 audit reports and 20 longitudinal summaries" in inventory_text
    assert "All 42 referenced screenshot paths exist locally." in inventory_text
    assert "Do not say:" in inventory_text
    assert "project_inventory_and_poster_story_2026-07-02.md" in readme_text
    assert (
        "[Project inventory and poster story, 2026-07-02]"
        "(project_inventory_and_poster_story_2026-07-02.md)"
    ) in index_text


def test_current_project_goal_is_canonical_entrypoint() -> None:
    goal_path = Path("docs/research/current_project_goal_2026-07-02.md")
    schema_path = Path("SCHEMA.md")
    readme_path = Path("README.md")
    scope_path = Path("docs/research/current_scope_2026-07-01.md")
    work_order_path = Path("docs/research/presentation_poster_work_order_2026-07-02.md")
    inventory_path = Path("docs/research/project_inventory_and_poster_story_2026-07-02.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")

    goal_text = goal_path.read_text(encoding="utf-8")
    schema_text = schema_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    scope_text = scope_path.read_text(encoding="utf-8")
    work_order_text = work_order_path.read_text(encoding="utf-8")
    inventory_text = inventory_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")

    assert "One-Sentence Goal" in goal_text
    assert "RQ1 scores" in goal_text
    assert "layered consent interfaces for unbiased choice" in goal_text
    assert "RQ2 captures and versions" in goal_text
    assert "Not a screenshot collection project." in goal_text
    assert "Evidence traceability is a design requirement" in goal_text
    assert "Presentation." in goal_text
    assert "Large poster." in goal_text
    assert "Traceable evidence package" in goal_text
    assert "current_project_goal_2026-07-02.md" in schema_text
    assert "current_project_goal_2026-07-02.md" in readme_text
    assert "original RQ1/RQ2 spine" in scope_text
    assert "current_project_goal_2026-07-02.md" in work_order_text
    assert "current_project_goal_2026-07-02.md" in inventory_text
    assert "[Current project goal, 2026-07-02](current_project_goal_2026-07-02.md)" in index_text


def test_july3_scope_fact_review_and_poster_plan_is_current_entrypoint() -> None:
    review_path = Path("docs/research/july3_scope_fact_review_and_poster_plan_2026-07-03.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")
    goal_path = Path("docs/research/current_project_goal_2026-07-02.md")

    review_text = review_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")
    goal_text = goal_path.read_text(encoding="utf-8")

    assert "# July 3 Scope/Fact Review and Poster Plan, 2026-07-03" in review_text
    assert "35 of 70" in review_text
    assert "50.0%" in review_text
    assert "RQ1 scoring" in review_text
    assert "RQ2 versioning" in review_text
    assert "326 tracked site `layer1.png`" in review_text
    assert "0 synced `layer1.html`" in review_text
    assert "42 audit reports and 20 longitudinal summaries" in review_text
    assert "7 blank current-five decisions" in review_text
    assert "8 pending CMP/manual-review" in review_text
    assert "Poster can be drafted now as a pilot/evidence poster" in review_text
    assert "not a completed 20-site final dataset" in advisor_index_text
    assert "july3_scope_fact_review_and_poster_plan_2026-07-03.md" in readme_text
    assert (
        "[July 3 scope/fact review and poster plan, 2026-07-03]"
        "(july3_scope_fact_review_and_poster_plan_2026-07-03.md)"
    ) in index_text
    assert "july3_scope_fact_review_and_poster_plan_2026-07-03.md" in advisor_index_text
    assert "july3_scope_fact_review_and_poster_plan_2026-07-03.md" in goal_text


def test_july5_evidence_sync_audit_is_current_entrypoint() -> None:
    audit_path = Path("docs/research/july5_evidence_sync_audit_2026-07-05.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    audit_text = audit_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")

    assert "# July 5 Evidence Sync Audit, 2026-07-05" in audit_text
    assert "Local HEAD: `3c202181ca6510e5fd395989b2b62511aa155641`" in audit_text
    assert "PR #8: open, draft, mergeable, not merged." in audit_text
    assert "`data/captures` contains 365 PNG files." in audit_text
    assert "Git tracks 365 capture PNG files." in audit_text
    assert (
        "`origin/codex/project-status-plain-language` contains 365 capture PNG files."
        in audit_text
    )
    assert "Missing screenshot refs: 0." in audit_text
    assert "Missing raw DOM HTML files: 42." in audit_text
    assert "Missing raw DOM HTML files: 5." in audit_text
    assert "Missing raw DOM HTML files: 8." in audit_text
    assert "Blank confirmed decisions: 7." in audit_text
    assert "Pending confirmations: 8." in audit_text
    assert "Screenshot evidence is tracked by Git and present on the GitHub PR branch." in audit_text
    assert "2026-07-05 evidence sync confirmation" in advisor_index_text
    assert "july5_evidence_sync_audit_2026-07-05.md" in readme_text
    assert (
        "[July 5 evidence sync audit, 2026-07-05]"
        "(july5_evidence_sync_audit_2026-07-05.md)"
    ) in index_text
    assert "july5_evidence_sync_audit_2026-07-05.md" in advisor_index_text


def test_july6_poster_section_draft_is_current_entrypoint() -> None:
    draft_path = Path("docs/research/july6_poster_section_draft_2026-07-06.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    draft_text = draft_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")

    assert "# July 6 Poster Section Draft, 2026-07-06" in draft_text
    assert "38 of 70 core-cycle days" in draft_text
    assert "54.3%" in draft_text
    assert "PR #8: open, draft, mergeable, not merged into `main`." in draft_text
    assert "42 audit reports and 20 longitudinal summaries" in draft_text
    assert "Banner-detected counts" in draft_text
    assert "true=9, false=33" in draft_text
    assert "326 site `layer1.png` files" in draft_text
    assert "0 synced site" in draft_text
    assert "Current-five decision sheet: 7 rows, 7 blank decisions." in draft_text
    assert "CMP/manual-review confirmation sheet: 8 rows, 8 pending confirmations." in draft_text
    assert "Traceable Consent Interface Audit and Versioning" in draft_text
    assert "No-visible-banner contrast cases are not banner-path failures." in draft_text
    assert "The poster can now safely include:" in draft_text
    assert "july6_poster_section_draft_2026-07-06.md" in readme_text
    assert (
        "[July 6 poster section draft, 2026-07-06]"
        "(july6_poster_section_draft_2026-07-06.md)"
    ) in index_text
    assert "july6_poster_section_draft_2026-07-06.md" in advisor_index_text


def test_july6_recent_work_validation_and_gap_audit_is_current_entrypoint() -> None:
    audit_path = Path("docs/research/july6_recent_work_validation_and_gap_audit_2026-07-06.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    audit_text = audit_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")

    assert "# July 6 Recent Work Validation and Gap Audit, 2026-07-06" in audit_text
    assert "38 of 70 days" in audit_text
    assert "54.3%" in audit_text
    assert "PR #8 is open, draft, mergeable, and not merged into `main`." in audit_text
    assert "Audit reports in package: 42." in audit_text
    assert "Longitudinal summaries in package: 20." in audit_text
    assert "Current-five decision sheet: 7 rows, 7 blank decisions." in audit_text
    assert "CMP/manual-review confirmation sheet: 8 rows, 8 pending confirmations" in audit_text
    assert "Site screenshot evidence: 326 `layer1.png` files." in audit_text
    assert "Synced site raw HTML evidence: 0 `layer1.html` files." in audit_text
    assert "No code/data correction was required by this scan." in audit_text
    assert "Yes, for the current safe scope:" in audit_text
    assert "No, if \"OK\" means final experiment complete:" in audit_text
    assert "Remaining Gaps Before Experiment Endpoint" in audit_text
    assert "july6_recent_work_validation_and_gap_audit_2026-07-06.md" in readme_text
    assert (
        "[July 6 validation and gap audit, 2026-07-06]"
        "(july6_recent_work_validation_and_gap_audit_2026-07-06.md)"
    ) in index_text
    assert "july6_recent_work_validation_and_gap_audit_2026-07-06.md" in advisor_index_text


def test_july7_poster_build_work_order_is_current_entrypoint() -> None:
    work_order_path = Path("docs/research/july7_poster_build_work_order_2026-07-07.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    work_order_text = work_order_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")

    assert "# July 7 Poster Build Work Order, 2026-07-07" in work_order_text
    assert "39 of 70 core-cycle days" in work_order_text
    assert "55.7%" in work_order_text
    assert "Days left before August 7 core deadline: 31." in work_order_text
    assert "PR #8: open, draft, mergeable, not merged into `main`." in work_order_text
    assert "Research package: 42 audit reports and 20 longitudinal summaries." in work_order_text
    assert "Banner-detected counts" in work_order_text
    assert "true=9, false=33" in work_order_text
    assert "326 site `layer1.png` files" in work_order_text
    assert "0 synced site" in work_order_text
    assert "Current-five decision sheet: 7 rows, 7 blank decisions." in work_order_text
    assert "CMP/manual-review confirmation sheet: 8 rows, 8 pending confirmations." in work_order_text
    assert "Build the poster as a pilot/method poster with seven panels:" in work_order_text
    assert "Guardian" in work_order_text
    assert "Coca-Cola" in work_order_text
    assert "CNN" in work_order_text
    assert "Booking.com" in work_order_text
    assert "NerdWallet" in work_order_text
    assert "No-visible-banner contrast cases are not banner-path failures." in work_order_text
    assert "The final dataset is complete." in work_order_text
    assert "july7_poster_build_work_order_2026-07-07.md" in readme_text
    assert (
        "[July 7 poster build work order, 2026-07-07]"
        "(july7_poster_build_work_order_2026-07-07.md)"
    ) in index_text
    assert "july7_poster_build_work_order_2026-07-07.md" in advisor_index_text


def test_july7_poster_layout_draft_is_current_entrypoint() -> None:
    layout_path = Path("docs/research/july7_poster_layout_draft_2026-07-07.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    layout_text = layout_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")

    assert "# July 7 Poster Layout Draft, 2026-07-07" in layout_text
    assert "first poster layout" in layout_text
    assert "This draft adds no new browser capture" in layout_text
    assert "Build the poster as a pilot/method poster" in layout_text
    assert "Top band" in layout_text
    assert "Left column" in layout_text
    assert "Middle column" in layout_text
    assert "Right column" in layout_text
    assert "Traceable Consent Interface Audit and Versioning" in layout_text
    assert "Week 2 target sites | 5" in layout_text
    assert "Audit reports | 42" in layout_text
    assert "Longitudinal summaries | 20" in layout_text
    assert "Synced raw `layer1.html` files | 0" in layout_text
    assert "data/captures/sites/www_theguardian_com_20260605_160209/layer1.png" in layout_text
    assert "data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png" in layout_text
    assert "data/captures/sites/www_cnn_com_20260605_160221/layer1.png" in layout_text
    assert "data/captures/sites/www_booking_com_20260605_160226/layer1.png" in layout_text
    assert "data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png" in layout_text
    assert "No-visible-banner contrast cases are not banner-path failures." in layout_text
    assert "final dataset complete" in layout_text
    assert "ready for a first visual mockup" in layout_text
    assert "july7_poster_layout_draft_2026-07-07.md" in readme_text
    assert (
        "[July 7 poster layout draft, 2026-07-07]"
        "(july7_poster_layout_draft_2026-07-07.md)"
    ) in index_text
    assert "july7_poster_layout_draft_2026-07-07.md" in advisor_index_text


def test_july9_poster_asset_manifest_is_current_entrypoint() -> None:
    manifest_path = Path("docs/research/july9_poster_asset_manifest_2026-07-09.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    manifest_text = manifest_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")

    assert "# July 9 Poster Asset Manifest, 2026-07-09" in manifest_text
    assert "41 of 70 core-cycle days" in manifest_text
    assert "58.6%" in manifest_text
    assert "Days left before August 7 core deadline: 29." in manifest_text
    assert "Research package: 42 audit reports and 20 longitudinal summaries." in manifest_text
    assert "Banner-detected counts" in manifest_text
    assert "true=9, false=33" in manifest_text
    assert "326 site `layer1.png` files" in manifest_text
    assert "0 synced site" in manifest_text
    assert "Current-five decision sheet: 7 rows, 7 blank decisions." in manifest_text
    assert "CMP/manual-review confirmation sheet: 8 rows, 8 pending confirmations." in manifest_text
    assert "The July 8 draft task was carried forward on July 9" in manifest_text
    assert "data/captures/sites/www_theguardian_com_20260605_160209/layer1.png" in manifest_text
    assert "data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png" in manifest_text
    assert "data/captures/sites/www_cnn_com_20260605_160221/layer1.png" in manifest_text
    assert "data/captures/sites/www_booking_com_20260605_160226/layer1.png" in manifest_text
    assert "data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png" in manifest_text
    assert manifest_text.count("1440x900") == 5
    assert "144914" in manifest_text
    assert "338126" in manifest_text
    assert "439361" in manifest_text
    assert "97083" in manifest_text
    assert "608556" in manifest_text
    assert "Do not treat as a banner-path failure without the separate table rule." in manifest_text
    assert "This screenshot proves the site still looks the same today." in manifest_text
    assert "july9_poster_asset_manifest_2026-07-09.md" in readme_text
    assert (
        "[July 9 poster asset manifest, 2026-07-09]"
        "(july9_poster_asset_manifest_2026-07-09.md)"
    ) in index_text
    assert "july9_poster_asset_manifest_2026-07-09.md" in advisor_index_text


def test_july12_poster_assembly_packet_is_current_entrypoint() -> None:
    packet_path = Path("docs/research/july12_poster_assembly_packet_2026-07-12.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    packet_text = packet_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")

    assert "# July 12 Poster Assembly Packet, 2026-07-12" in packet_text
    assert "44 of 70 core-cycle days" in packet_text
    assert "62.9%" in packet_text
    assert "Days left before August 7 core deadline: 26." in packet_text
    assert "Days left before August 31 polish deadline: 50." in packet_text
    assert "62e98b7f332c8ff958fe85f0dde6904eda41914e" in packet_text
    assert "GitHub PR #8: open, draft, mergeable, not merged into `main`." in packet_text
    assert "Research package: 42 audit reports and 20 longitudinal summaries." in packet_text
    assert "true=9, false=33" in packet_text
    assert "326 site `layer1.png` files" in packet_text
    assert "0 synced site" in packet_text
    assert "Current-five decision sheet: 7 rows, 7 blank decisions." in packet_text
    assert "CMP/manual-review confirmation sheet: 8 rows, 8 pending confirmations." in packet_text
    assert "Build a first visual poster mockup from existing verified evidence." in packet_text
    assert "Traceable Consent Interface Audit and Versioning" in packet_text
    assert "Week 2 target sites | 5" in packet_text
    assert "Audit reports | 42" in packet_text
    assert "Longitudinal summaries | 20" in packet_text
    assert "data/captures/sites/www_theguardian_com_20260605_160209/layer1.png" in packet_text
    assert "data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png" in packet_text
    assert "data/captures/sites/www_cnn_com_20260605_160221/layer1.png" in packet_text
    assert "data/captures/sites/www_booking_com_20260605_160226/layer1.png" in packet_text
    assert "data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png" in packet_text
    assert "No-visible-banner contrast cases are not banner-path failures." in packet_text
    assert "Final dataset complete." in packet_text
    assert "The live website still looks the same today." in packet_text
    assert "july12_poster_assembly_packet_2026-07-12.md" in readme_text
    assert (
        "[July 12 poster assembly packet, 2026-07-12]"
        "(july12_poster_assembly_packet_2026-07-12.md)"
    ) in index_text
    assert "july12_poster_assembly_packet_2026-07-12.md" in advisor_index_text


def test_july14_first_poster_mockup_is_traceable_and_rendered() -> None:
    mockup_path = Path("docs/research/july14_first_poster_mockup_2026-07-14.md")
    pptx_path = Path("docs/research/poster/ssrp_poster_mockup_2026-07-14.pptx")
    preview_path = Path("docs/research/poster/ssrp_poster_mockup_2026-07-14.png")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    mockup_text = mockup_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")

    assert pptx_path.is_file()
    assert pptx_path.stat().st_size > 1_000_000
    assert preview_path.is_file()
    assert preview_path.stat().st_size > 1_000_000
    assert "# July 14 First Poster Mockup, 2026-07-14" in mockup_text
    assert "48 x 36 inch landscape poster canvas" in mockup_text
    assert "46 of 70 core-cycle days" in mockup_text
    assert "65.7%" in mockup_text
    assert "Research package: 42 audit reports and 20 longitudinal summaries." in mockup_text
    assert "326 site `layer1.png` files" in mockup_text
    assert "0 synced site" in mockup_text
    assert "7 rows, 7 blank decisions" in mockup_text
    assert "8 rows, 8 pending confirmations" in mockup_text
    assert "data/captures/sites/www_theguardian_com_20260605_160209/layer1.png" in mockup_text
    assert "data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png" in mockup_text
    assert "data/captures/sites/www_cnn_com_20260605_160221/layer1.png" in mockup_text
    assert "data/captures/sites/www_booking_com_20260605_160226/layer1.png" in mockup_text
    assert "data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png" in mockup_text
    assert "no-visible-banner contrast case" in mockup_text
    assert "does not claim legal compliance" in mockup_text
    assert "Test passed. No overflow detected." in mockup_text
    assert "july14_first_poster_mockup_2026-07-14.md" in readme_text
    assert (
        "[July 14 first poster mockup, 2026-07-14]"
        "(july14_first_poster_mockup_2026-07-14.md)"
    ) in index_text
    assert "july14_first_poster_mockup_2026-07-14.md" in advisor_index_text


def test_july14_poster_mockup_review_email_is_current_advisor_entrypoint() -> None:
    email_path = Path("docs/research/advisor_email_poster_mockup_review_2026-07-14.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    email_text = email_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    advisor_index_text = advisor_index_path.read_text(encoding="utf-8")

    assert "# Advisor Email Poster Mockup Review, 2026-07-14" in email_text
    assert "First poster mockup for review" in email_text
    assert "docs/research/poster/ssrp_poster_mockup_2026-07-14.pptx" in email_text
    assert "docs/research/poster/ssrp_poster_mockup_2026-07-14.png" in email_text
    assert "docs/research/july14_first_poster_mockup_2026-07-14.md" in email_text
    assert "42 audit reports" in email_text
    assert "20 longitudinal summaries" in email_text
    assert "326 synced site screenshot PNGs" in email_text
    assert "0 synced raw HTML" in email_text
    assert "7 blank current-five decisions" in email_text
    assert "8 pending CMP/manual-review confirmations" in email_text
    assert "five-site pilot/method poster" in email_text
    assert "The Guardian and Coca-Cola" in email_text
    assert "no-visible-first-screen-banner contrast cases" in email_text
    assert "Do not claim the final dataset is complete." in email_text
    assert "Do not make legal compliance or non-compliance verdicts." in email_text
    assert "advisor_email_poster_mockup_review_2026-07-14.md" in readme_text
    assert (
        "[Current advisor email: poster mockup review, 2026-07-14]"
        "(advisor_email_poster_mockup_review_2026-07-14.md)"
    ) in index_text
    assert "advisor_email_poster_mockup_review_2026-07-14.md" in advisor_index_text


def test_july15_poster_pdf_is_verified_and_linked() -> None:
    qa_path = Path("docs/research/july15_poster_pdf_and_print_qa_2026-07-15.md")
    pdf_path = Path("docs/research/poster/ssrp_poster_mockup_2026-07-14.pdf")
    mockup_path = Path("docs/research/july14_first_poster_mockup_2026-07-14.md")
    email_path = Path("docs/research/advisor_email_poster_mockup_review_2026-07-14.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    qa_text = qa_path.read_text(encoding="utf-8")
    linked_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            mockup_path,
            email_path,
            readme_path,
            index_path,
            advisor_index_path,
        )
    )

    assert pdf_path.is_file()
    assert pdf_path.stat().st_size > 500_000
    assert pdf_path.read_bytes().startswith(b"%PDF-")
    assert "# July 15 Poster PDF and Print QA, 2026-07-15" in qa_text
    assert "PDF pages: 1" in qa_text
    assert "3456 x 2592 points, exactly 48 x 36 inches" in qa_text
    assert "Test passed. No overflow detected." in qa_text
    assert "No clipping, overlap, black boxes, or broken glyphs" in qa_text
    assert "47 of 70 core-cycle days" in qa_text
    assert "67.1%" in qa_text
    assert "23" in qa_text
    assert "47" in qa_text
    assert "42 audit reports" in qa_text
    assert "20 longitudinal summaries" in qa_text
    assert "326 site `layer1.png`" in qa_text
    assert "0 synced site `layer1.html`" in qa_text
    assert "7 blank current-five decisions" in qa_text
    assert "8 pending CMP/manual" in qa_text
    assert "ssrp_poster_mockup_2026-07-14.pdf" in linked_text
    assert "july15_poster_pdf_and_print_qa_2026-07-15.md" in linked_text


def test_july16_poster_review_decision_sheet_preserves_pending_decisions() -> None:
    sheet_path = Path("data/poster_review_decision_sheet_2026-07-16.csv")
    note_path = Path("docs/research/july16_poster_review_decision_sheet_2026-07-16.md")
    email_path = Path("docs/research/advisor_email_poster_mockup_review_2026-07-14.md")
    readme_path = Path("README.md")
    index_path = Path("docs/research/week2_checkin_index_2026-06-06.md")
    advisor_index_path = Path("docs/research/advisor_packet_index_2026-06-05.md")

    with sheet_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    note_text = note_path.read_text(encoding="utf-8")
    linked_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (email_path, readme_path, index_path, advisor_index_path)
    )

    assert len(rows) == 5
    assert {row["decision_id"] for row in rows} == {
        "poster_framing",
        "main_evidence_cards",
        "contrast_case_treatment",
        "unresolved_review_items",
        "final_print_revision",
    }
    assert all(row["review_status"] == "pending" for row in rows)
    assert all(not row["confirmed_decision"] for row in rows)
    assert all(not row["reviewer"] for row in rows)
    assert all(not row["review_date"] for row in rows)
    assert all(row["source_evidence"] for row in rows)
    assert all(row["decision_options"] for row in rows)
    assert rows[0]["recommended_default"] == "five_site_pilot_method"
    assert rows[1]["recommended_default"] == "guardian_and_coca_cola"
    assert (
        rows[2]["recommended_default"]
        == "no_visible_first_screen_banner_contrast"
    )
    assert "# July 16 Poster Review Decision Sheet, 2026-07-16" in note_text
    assert "48 of 70 core-cycle days" in note_text
    assert "68.6%" in note_text
    assert "7 blank rows" in note_text
    assert "8 pending rows" in note_text
    assert "Do not copy `recommended_default`" in note_text
    assert "poster_review_decision_sheet_2026-07-16.csv" in linked_text
    assert "july16_poster_review_decision_sheet_2026-07-16.md" in linked_text
