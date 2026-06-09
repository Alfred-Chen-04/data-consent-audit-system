"""Tests for deterministic longitudinal diff events."""

from datetime import datetime

import pytest

from consent_audit.diff import detect_changes, summarize_week
from consent_audit.llm.budget import BudgetLedger
from consent_audit.models import (
    AuditReport,
    CaptureBundle,
    ChangeEventType,
    Layer1Result,
    LayerSnapshot,
    LetterGrade,
    MultimodalFingerprint,
    Pathway,
    Tier,
)


def _report(
    *,
    dom_hash: str = "dom",
    image_hash: str = "img",
    text: str = "Accept or reject cookies.",
    reject_available: bool = True,
    tier: Tier = Tier.COMPLIANT,
) -> AuditReport:
    bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30),
        layers=[
            LayerSnapshot(
                layer_index=1,
                screenshot_ref="banner.png",
                dom_snapshot_ref="banner.html",
                visible_text=text,
            )
        ],
        path_outcomes={},
        fingerprint=MultimodalFingerprint(dom_hash=dom_hash, perceptual_image_hash=image_hash),
    )
    layer1 = Layer1Result(
        accept_available=True,
        reject_available=reject_available,
        customize_available=True,
        dismiss_available=False,
        missing_paths=[] if reject_available else [Pathway.REJECT],
        evidence={},
        gate_passed=reject_available,
    )
    return AuditReport(
        bundle=bundle,
        layer1=layer1,
        layer2=None,
        layer3=None,
        tier=tier,
        report_markdown="fixture",
        total_api_cost_usd=0.0,
        generated_at=datetime(2026, 5, 30),
    )


def test_detect_changes_emits_pathway_layout_copy_dom_and_score_events() -> None:
    previous = _report()
    current = _report(
        dom_hash="dom2",
        image_hash="img2",
        text="Accept all cookies only.",
        reject_available=False,
        tier=Tier.HIGH_RISK,
    )

    event_types = {event.change_type for event in detect_changes(previous, current)}

    assert ChangeEventType.PATHWAY_CHANGE in event_types
    assert ChangeEventType.LAYOUT_CHANGE in event_types
    assert ChangeEventType.COPY_CHANGE in event_types
    assert ChangeEventType.DOM_RESTRUCTURE in event_types
    assert ChangeEventType.SCORE_CHANGE in event_types


@pytest.mark.asyncio
async def test_summarize_week_returns_deterministic_high_attention_summary_without_budget_spend() -> None:
    previous = _report()
    current = _report(
        dom_hash="dom2",
        image_hash="img2",
        text="Accept all cookies only.",
        reject_available=False,
        tier=Tier.HIGH_RISK,
    )
    events = detect_changes(previous, current)
    ledger = BudgetLedger(cap_usd=1.0)

    summary = await summarize_week("https://example.com", events, ledger=ledger)

    assert summary.url == previous.bundle.url
    assert summary.events == events
    assert summary.severity == LetterGrade.D
    assert "pathway_change" in summary.summary
    assert "score_change" in summary.summary
    assert "inspect evidence" in summary.implications_for_user.lower()
    assert ledger.spent_usd == 0.0
