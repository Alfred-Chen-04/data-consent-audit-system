"""Paper-facing exports for longitudinal consent-interface changes."""

import csv
from pathlib import Path

from consent_audit.models import ChangeEventType, WeeklySummary

LONGITUDINAL_SUMMARY_FIELDNAMES = [
    "url",
    "week_of",
    "severity",
    "event_count",
    "event_types",
    "max_magnitude",
    "has_pathway_change",
    "has_score_change",
    "has_copy_change",
    "has_layout_change",
    "has_dom_restructure",
    "summary",
    "implications_for_user",
]


def weekly_summary_to_row(summary: WeeklySummary) -> dict[str, str]:
    """Flatten a WeeklySummary into one stable CSV row."""
    event_types = {event.change_type for event in summary.events}
    return {
        "url": str(summary.url),
        "week_of": summary.week_of.date().isoformat(),
        "severity": summary.severity.value,
        "event_count": str(len(summary.events)),
        "event_types": "|".join(sorted(event_type.value for event_type in event_types)),
        "max_magnitude": _max_magnitude(summary),
        "has_pathway_change": _bool_cell(ChangeEventType.PATHWAY_CHANGE in event_types),
        "has_score_change": _bool_cell(ChangeEventType.SCORE_CHANGE in event_types),
        "has_copy_change": _bool_cell(ChangeEventType.COPY_CHANGE in event_types),
        "has_layout_change": _bool_cell(ChangeEventType.LAYOUT_CHANGE in event_types),
        "has_dom_restructure": _bool_cell(ChangeEventType.DOM_RESTRUCTURE in event_types),
        "summary": summary.summary,
        "implications_for_user": summary.implications_for_user,
    }


def export_weekly_summaries_to_csv(path: Path, summaries: list[WeeklySummary]) -> None:
    """Write WeeklySummary rows as a research-ready CSV table."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=LONGITUDINAL_SUMMARY_FIELDNAMES)
        writer.writeheader()
        for summary in summaries:
            writer.writerow(weekly_summary_to_row(summary))


def _max_magnitude(summary: WeeklySummary) -> str:
    if not summary.events:
        return "0.00"
    return f"{max(event.magnitude for event in summary.events):.2f}"


def _bool_cell(value: bool) -> str:
    return "true" if value else "false"
