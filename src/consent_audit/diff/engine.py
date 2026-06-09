"""Week-over-week change detection + deterministic summarization.

Runs AFTER two successive AuditReports exist for the same URL.
Principle: summaries describe detected events; judgments come from Layer scores.
"""

from datetime import UTC, datetime
from difflib import SequenceMatcher

from pydantic import HttpUrl, TypeAdapter

from consent_audit.llm.budget import BudgetLedger
from consent_audit.models import (
    AuditReport,
    ChangeEvent,
    ChangeEventType,
    LetterGrade,
    WeeklySummary,
)

_HTTP_URL_ADAPTER = TypeAdapter(HttpUrl)


def detect_changes(previous: AuditReport, current: AuditReport) -> list[ChangeEvent]:
    """Compare two reports on five channels (CONCEPTS.md §5).

    Deterministic — no LLM involved.
    """
    events: list[ChangeEvent] = []

    if _layer1_signature(previous) != _layer1_signature(current):
        events.append(
            _event(
                ChangeEventType.PATHWAY_CHANGE,
                previous,
                current,
                1.0,
                "Layer-1 pathway availability changed.",
            )
        )

    if (
        previous.bundle.fingerprint.perceptual_image_hash
        != current.bundle.fingerprint.perceptual_image_hash
    ):
        events.append(
            _event(
                ChangeEventType.LAYOUT_CHANGE,
                previous,
                current,
                1.0,
                "Perceptual screenshot fingerprint changed.",
            )
        )

    if _visible_text(previous) != _visible_text(current):
        events.append(
            _event(
                ChangeEventType.COPY_CHANGE,
                previous,
                current,
                _text_magnitude(_visible_text(previous), _visible_text(current)),
                "Visible consent-interface text changed.",
            )
        )

    if (
        previous.bundle.fingerprint.dom_hash != current.bundle.fingerprint.dom_hash
        and previous.bundle.fingerprint.perceptual_image_hash
        != current.bundle.fingerprint.perceptual_image_hash
    ):
        events.append(
            _event(
                ChangeEventType.DOM_RESTRUCTURE,
                previous,
                current,
                1.0,
                "DOM fingerprint changed together with layout.",
            )
        )

    if _score_signature(previous) != _score_signature(current):
        events.append(
            _event(
                ChangeEventType.SCORE_CHANGE,
                previous,
                current,
                1.0,
                "Audit tier or layer score category changed.",
            )
        )

    return events


def _event(
    change_type: ChangeEventType,
    previous: AuditReport,
    current: AuditReport,
    magnitude: float,
    description: str,
) -> ChangeEvent:
    return ChangeEvent(
        change_type=change_type,
        from_bundle_id=previous.bundle.bundle_id,
        to_bundle_id=current.bundle.bundle_id,
        magnitude=magnitude,
        description=description,
    )


def _layer1_signature(report: AuditReport) -> tuple[bool, bool, bool, bool]:
    return (
        report.layer1.accept_available,
        report.layer1.reject_available,
        report.layer1.customize_available,
        report.layer1.dismiss_available,
    )


def _score_signature(report: AuditReport) -> tuple[str, str | None, str | None, str | None]:
    return (
        report.tier.value,
        report.layer2.overall_category.value if report.layer2 is not None else None,
        report.layer3.transparency.letter_grade.value if report.layer3 is not None else None,
        report.layer3.unbiased_choice.letter_grade.value if report.layer3 is not None else None,
    )


def _visible_text(report: AuditReport) -> str:
    return "\n".join(layer.visible_text for layer in report.bundle.layers).strip()


def _text_magnitude(previous: str, current: str) -> float:
    if not previous and not current:
        return 0.0
    return 1.0 - SequenceMatcher(a=previous, b=current).ratio()


async def summarize_week(
    url: HttpUrl | str,
    events: list[ChangeEvent],
    *,
    ledger: BudgetLedger,
    week_of: datetime | None = None,
) -> WeeklySummary:
    """Return a deterministic weekly summary without spending model budget."""
    _ = ledger
    normalized_url = _HTTP_URL_ADAPTER.validate_python(str(url))
    severity = _severity_for_events(events)
    return WeeklySummary(
        url=normalized_url,
        week_of=week_of or datetime.now(UTC),
        events=events,
        summary=_summary_text(events),
        severity=severity,
        implications_for_user=_implications_for_user(events),
    )


def _severity_for_events(events: list[ChangeEvent]) -> LetterGrade:
    event_types = {event.change_type for event in events}
    if not events:
        return LetterGrade.A
    if ChangeEventType.PATHWAY_CHANGE in event_types or ChangeEventType.SCORE_CHANGE in event_types:
        return LetterGrade.D
    if ChangeEventType.DOM_RESTRUCTURE in event_types or ChangeEventType.LAYOUT_CHANGE in event_types:
        return LetterGrade.C
    return LetterGrade.B


def _summary_text(events: list[ChangeEvent]) -> str:
    if not events:
        return "No detected consent-interface changes for this observation window."

    event_summaries = "; ".join(
        f"{event.change_type.value} (magnitude {event.magnitude:.2f}): {event.description}"
        for event in events
    )
    return f"Detected {len(events)} consent-interface change(s): {event_summaries}"


def _implications_for_user(events: list[ChangeEvent]) -> str:
    event_types = {event.change_type for event in events}
    if not events:
        return "No follow-up is required beyond the next scheduled capture."
    if ChangeEventType.PATHWAY_CHANGE in event_types or ChangeEventType.SCORE_CHANGE in event_types:
        return (
            "User-visible consent choices or audit tier changed; inspect evidence "
            "before paper coding."
        )
    if ChangeEventType.DOM_RESTRUCTURE in event_types or ChangeEventType.LAYOUT_CHANGE in event_types:
        return "Interface structure or layout changed; review screenshots before comparing scores."
    return "Consent copy changed; review visible text before coding longitudinal patterns."
