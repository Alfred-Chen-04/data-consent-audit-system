"""Tests for the deterministic Layer 2 MVP."""

from datetime import datetime

from consent_audit.layers import score_layer1, score_layer2
from consent_audit.models import (
    CaptureBundle,
    EffortCategory,
    ElementRef,
    EventLogRef,
    MultimodalFingerprint,
    PathOutcome,
    Pathway,
)


def _element(pathway: Pathway) -> ElementRef:
    return ElementRef(
        dom_selector=f"button.{pathway.value}",
        visible_text=pathway.value.title(),
    )


def _outcome(pathway: Pathway, *, click_depth: int = 1) -> PathOutcome:
    return PathOutcome(
        pathway=pathway,
        attempted=True,
        succeeded=True,
        click_depth=click_depth,
        trigger_element=_element(pathway),
    )


def test_score_layer2_uses_deterministic_subfeatures_for_available_paths() -> None:
    bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30),
        layers=[],
        path_outcomes={
            Pathway.ACCEPT: _outcome(Pathway.ACCEPT, click_depth=1),
            Pathway.REJECT: _outcome(Pathway.REJECT, click_depth=2),
            Pathway.CUSTOMIZE: _outcome(Pathway.CUSTOMIZE, click_depth=2),
            Pathway.DISMISS: _outcome(Pathway.DISMISS, click_depth=1),
        },
        fingerprint=MultimodalFingerprint(dom_hash="dom", perceptual_image_hash="img"),
        event_log=[
            EventLogRef(event_index=0, action="click_accept", target=_element(Pathway.ACCEPT), outcome="success"),
            EventLogRef(event_index=1, action="click_reject", target=_element(Pathway.REJECT), outcome="success"),
            EventLogRef(
                event_index=2,
                action="click_customize",
                target=_element(Pathway.CUSTOMIZE),
                outcome="success",
            ),
            EventLogRef(event_index=3, action="click_dismiss", target=_element(Pathway.DISMISS), outcome="success"),
        ],
    )
    layer1 = score_layer1(bundle)

    result = score_layer2(bundle, layer1)

    assert result.overall_category == EffortCategory.EASY
    assert set(result.per_path_effort) == set(Pathway)
    reject = result.per_path_effort[Pathway.REJECT]
    assert reject.score == 0.1
    assert {feature.name for feature in reject.sub_features} == {"click_depth", "immediate_feedback"}
    assert all(feature.evidence for feature in reject.sub_features)


def test_score_layer2_skips_paths_layer1_marked_unavailable() -> None:
    bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30),
        layers=[],
        path_outcomes={
            Pathway.ACCEPT: _outcome(Pathway.ACCEPT),
            Pathway.CUSTOMIZE: _outcome(Pathway.CUSTOMIZE),
        },
        fingerprint=MultimodalFingerprint(dom_hash="dom", perceptual_image_hash="img"),
        event_log=[
            EventLogRef(event_index=0, action="click_accept", target=_element(Pathway.ACCEPT), outcome="success"),
            EventLogRef(
                event_index=1,
                action="click_customize",
                target=_element(Pathway.CUSTOMIZE),
                outcome="success",
            ),
        ],
    )
    layer1 = score_layer1(bundle)

    result = score_layer2(bundle, layer1)

    assert set(result.per_path_effort) == {Pathway.ACCEPT, Pathway.CUSTOMIZE}
