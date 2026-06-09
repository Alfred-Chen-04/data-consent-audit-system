"""Tests for paper-facing longitudinal summary CSV export."""

import csv
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from consent_audit.longitudinal_export import (
    LONGITUDINAL_SUMMARY_FIELDNAMES,
    export_weekly_summaries_to_csv,
    weekly_summary_to_row,
)
from consent_audit.models import ChangeEvent, ChangeEventType, LetterGrade, WeeklySummary


def _event(change_type: ChangeEventType, magnitude: float) -> ChangeEvent:
    return ChangeEvent(
        change_type=change_type,
        from_bundle_id=uuid4(),
        to_bundle_id=uuid4(),
        magnitude=magnitude,
        description=f"{change_type.value} detected.",
    )


def _summary() -> WeeklySummary:
    return WeeklySummary(
        url="https://example.com",  # type: ignore[arg-type]
        week_of=datetime(2026, 6, 13, 9, 30, tzinfo=UTC),
        events=[
            _event(ChangeEventType.PATHWAY_CHANGE, 1.0),
            _event(ChangeEventType.COPY_CHANGE, 0.42),
        ],
        summary="Detected pathway and copy changes.",
        severity=LetterGrade.D,
        implications_for_user="Inspect evidence before coding.",
    )


def test_weekly_summary_to_row_flattens_events_for_paper_table() -> None:
    row = weekly_summary_to_row(_summary())

    assert row["url"] == "https://example.com/"
    assert row["week_of"] == "2026-06-13"
    assert row["severity"] == "D"
    assert row["event_count"] == "2"
    assert row["event_types"] == "copy_change|pathway_change"
    assert row["max_magnitude"] == "1.00"
    assert row["has_pathway_change"] == "true"
    assert row["has_score_change"] == "false"
    assert row["summary"] == "Detected pathway and copy changes."
    assert row["implications_for_user"] == "Inspect evidence before coding."


def test_export_weekly_summaries_to_csv_writes_header_and_rows(tmp_path: Path) -> None:
    out_csv = tmp_path / "longitudinal_summary.csv"

    export_weekly_summaries_to_csv(out_csv, [_summary()])

    with out_csv.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    assert reader.fieldnames == LONGITUDINAL_SUMMARY_FIELDNAMES
    assert len(rows) == 1
    assert rows[0]["url"] == "https://example.com/"
    assert rows[0]["event_types"] == "copy_change|pathway_change"
