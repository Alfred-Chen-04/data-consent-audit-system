"""Tests for local append-only AuditReport storage."""

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from consent_audit.models import (
    AuditReport,
    CaptureBundle,
    ChangeEvent,
    ChangeEventType,
    Layer1Result,
    LayerSnapshot,
    LetterGrade,
    MultimodalFingerprint,
    Pathway,
    Tier,
    WeeklySummary,
)
from consent_audit.storage import db


def _report(
    url: str,
    *,
    generated_at: datetime,
    dom_hash: str,
) -> AuditReport:
    bundle = CaptureBundle(
        url=url,  # type: ignore[arg-type]
        captured_at=generated_at,
        layers=[],
        path_outcomes={},
        fingerprint=MultimodalFingerprint(dom_hash=dom_hash, perceptual_image_hash="img"),
    )
    layer1 = Layer1Result(
        accept_available=False,
        reject_available=False,
        customize_available=False,
        dismiss_available=False,
        missing_paths=list(Pathway),
        evidence={},
        gate_passed=False,
    )
    return AuditReport(
        bundle=bundle,
        layer1=layer1,
        layer2=None,
        layer3=None,
        tier=Tier.HIGH_RISK,
        report_markdown="fixture",
        total_api_cost_usd=0.0,
        generated_at=generated_at,
    )


def test_save_and_load_report_round_trips_jsonl(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    store_path = tmp_path / "reports.jsonl"
    monkeypatch.setattr(db, "REPORT_STORE_PATH", store_path)
    report = _report(
        "https://example.com",
        generated_at=datetime(2026, 5, 30, tzinfo=UTC),
        dom_hash="dom-1",
    )

    report_id = db.save_report(report)
    loaded = db.load_report(report_id)

    assert store_path.exists()
    assert loaded.report_id == report.report_id
    assert loaded.bundle.fingerprint.dom_hash == "dom-1"


def test_save_report_escapes_unicode_line_separators_for_jsonl(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    store_path = tmp_path / "reports.jsonl"
    monkeypatch.setattr(db, "REPORT_STORE_PATH", store_path)
    report = _report(
        "https://example.com",
        generated_at=datetime(2026, 5, 30, tzinfo=UTC),
        dom_hash="dom-1",
    )
    report.bundle.layers.append(
        LayerSnapshot(
            layer_index=1,
            screenshot_ref="captures/example/layer1.png",
            dom_snapshot_ref="captures/example/layer1.html",
            visible_text="Reward copy\u2028next visual line",
        )
    )

    db.save_report(report)

    physical_lines = store_path.read_text(encoding="utf-8").splitlines()
    assert len(physical_lines) == 1
    loaded = AuditReport.model_validate_json(physical_lines[0])
    assert loaded.bundle.layers[0].visible_text == "Reward copy\u2028next visual line"


def test_list_reports_for_url_returns_newest_first_with_limit(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(db, "REPORT_STORE_PATH", tmp_path / "reports.jsonl")
    older = _report(
        "https://example.com",
        generated_at=datetime(2026, 5, 30, tzinfo=UTC),
        dom_hash="old",
    )
    newer = _report(
        "https://example.com",
        generated_at=datetime(2026, 6, 6, tzinfo=UTC),
        dom_hash="new",
    )
    other = _report(
        "https://other.example",
        generated_at=datetime(2026, 6, 7, tzinfo=UTC),
        dom_hash="other",
    )

    db.save_report(older)
    db.save_report(other)
    db.save_report(newer)

    reports = db.list_reports_for_url("https://example.com", limit=1)

    assert [report.bundle.fingerprint.dom_hash for report in reports] == ["new"]


def test_list_reports_returns_newest_first_across_urls(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(db, "REPORT_STORE_PATH", tmp_path / "reports.jsonl")
    older = _report(
        "https://example.com",
        generated_at=datetime(2026, 5, 30, tzinfo=UTC),
        dom_hash="old",
    )
    newer = _report(
        "https://other.example",
        generated_at=datetime(2026, 6, 6, tzinfo=UTC),
        dom_hash="new",
    )

    db.save_report(older)
    db.save_report(newer)

    reports = db.list_reports(limit=2)

    assert [report.bundle.fingerprint.dom_hash for report in reports] == ["new", "old"]


def _weekly_summary(
    url: str,
    *,
    week_of: datetime,
    description: str,
) -> WeeklySummary:
    return WeeklySummary(
        url=url,  # type: ignore[arg-type]
        week_of=week_of,
        events=[
            ChangeEvent(
                change_type=ChangeEventType.COPY_CHANGE,
                from_bundle_id=uuid4(),
                to_bundle_id=uuid4(),
                magnitude=0.5,
                description=description,
            )
        ],
        summary=description,
        severity=LetterGrade.B,
        implications_for_user="Review copy before coding.",
    )


def test_save_and_list_weekly_summaries_for_url_returns_newest_first(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(db, "WEEKLY_SUMMARY_STORE_PATH", tmp_path / "weekly_summaries.jsonl")
    older = _weekly_summary(
        "https://example.com",
        week_of=datetime(2026, 6, 6, tzinfo=UTC),
        description="old copy changed",
    )
    newer = _weekly_summary(
        "https://example.com",
        week_of=datetime(2026, 6, 13, tzinfo=UTC),
        description="new copy changed",
    )
    other = _weekly_summary(
        "https://other.example",
        week_of=datetime(2026, 6, 14, tzinfo=UTC),
        description="other copy changed",
    )

    db.save_weekly_summary(older)
    db.save_weekly_summary(other)
    db.save_weekly_summary(newer)

    summaries = db.list_weekly_summaries_for_url("https://example.com", limit=1)

    assert [summary.summary for summary in summaries] == ["new copy changed"]


def test_save_weekly_summary_escapes_unicode_line_separators_for_jsonl(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    store_path = tmp_path / "weekly_summaries.jsonl"
    monkeypatch.setattr(db, "WEEKLY_SUMMARY_STORE_PATH", store_path)
    summary = _weekly_summary(
        "https://example.com",
        week_of=datetime(2026, 6, 6, tzinfo=UTC),
        description="copy changed\u2028next visual line",
    )

    db.save_weekly_summary(summary)

    physical_lines = store_path.read_text(encoding="utf-8").splitlines()
    assert len(physical_lines) == 1
    loaded = WeeklySummary.model_validate_json(physical_lines[0])
    assert loaded.summary == "copy changed\u2028next visual line"
