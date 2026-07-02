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
    assert "Guardian and Coca-Cola are the current banner-present evidence-card" in work_order_text
    assert "today_work_note_2026-07-02.md" in readme_text
    assert "presentation_poster_work_order_2026-07-02.md" in readme_text
    assert "[Today work note, 2026-07-02](today_work_note_2026-07-02.md)" in index_text
