"""Tests for the longitudinal-summary export script."""

import csv
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from consent_audit.models import ChangeEvent, ChangeEventType, LetterGrade, WeeklySummary
from consent_audit.storage import db
from scripts import export_longitudinal_summary


def _summary(url: str, week_of: datetime, description: str) -> WeeklySummary:
    return WeeklySummary(
        url=url,  # type: ignore[arg-type]
        week_of=week_of,
        events=[
            ChangeEvent(
                change_type=ChangeEventType.SCORE_CHANGE,
                from_bundle_id=uuid4(),
                to_bundle_id=uuid4(),
                magnitude=1.0,
                description=description,
            )
        ],
        summary=description,
        severity=LetterGrade.D,
        implications_for_user="Inspect score evidence.",
    )


def test_run_exports_all_saved_weekly_summaries_newest_first(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(db, "WEEKLY_SUMMARY_STORE_PATH", tmp_path / "weekly_summaries.jsonl")
    older = _summary(
        "https://example.com",
        datetime(2026, 6, 6, tzinfo=UTC),
        "old change",
    )
    newer = _summary(
        "https://example.com",
        datetime(2026, 6, 13, tzinfo=UTC),
        "new change",
    )
    db.save_weekly_summary(older)
    db.save_weekly_summary(newer)
    out_csv = tmp_path / "longitudinal_summary.csv"

    export_longitudinal_summary._run(out_csv)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    assert [row["summary"] for row in rows] == ["new change", "old change"]
    assert rows[0]["has_score_change"] == "true"
