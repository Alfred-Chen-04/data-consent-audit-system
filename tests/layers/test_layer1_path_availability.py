"""Deterministic tests for Layer 1 Path Availability."""

from datetime import datetime

from consent_audit.layers import score_layer1
from consent_audit.models import (
    CaptureBundle,
    ElementRef,
    MultimodalFingerprint,
    PathOutcome,
    Pathway,
)


def _outcome(pathway: Pathway, *, succeeded: bool = True, click_depth: int = 1) -> PathOutcome:
    return PathOutcome(
        pathway=pathway,
        attempted=True,
        succeeded=succeeded,
        click_depth=click_depth,
        trigger_element=ElementRef(
            dom_selector=f"button[data-path='{pathway.value}']",
            visible_text=pathway.value.title(),
        ),
    )


def _bundle(path_outcomes: dict[Pathway, PathOutcome]) -> CaptureBundle:
    return CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30),
        layers=[],
        path_outcomes=path_outcomes,
        fingerprint=MultimodalFingerprint(dom_hash="dom", perceptual_image_hash="img"),
    )


def test_clean_banner_passes_gate() -> None:
    bundle = _bundle(
        {
            Pathway.ACCEPT: _outcome(Pathway.ACCEPT),
            Pathway.REJECT: _outcome(Pathway.REJECT, click_depth=1),
            Pathway.CUSTOMIZE: _outcome(Pathway.CUSTOMIZE, click_depth=2),
            Pathway.DISMISS: _outcome(Pathway.DISMISS),
        }
    )

    result = score_layer1(bundle)

    assert result.gate_passed
    assert result.accept_available
    assert result.reject_available
    assert result.customize_available
    assert result.dismiss_available
    assert result.missing_paths == []


def test_missing_reject_fails_gate() -> None:
    bundle = _bundle(
        {
            Pathway.ACCEPT: _outcome(Pathway.ACCEPT),
            Pathway.CUSTOMIZE: _outcome(Pathway.CUSTOMIZE),
            Pathway.DISMISS: _outcome(Pathway.DISMISS),
        }
    )

    result = score_layer1(bundle)

    assert not result.gate_passed
    assert not result.reject_available
    assert Pathway.REJECT in result.missing_paths


def test_reject_requires_three_actions_fails_gate() -> None:
    bundle = _bundle(
        {
            Pathway.ACCEPT: _outcome(Pathway.ACCEPT),
            Pathway.REJECT: _outcome(Pathway.REJECT, click_depth=3),
            Pathway.CUSTOMIZE: _outcome(Pathway.CUSTOMIZE),
        }
    )

    result = score_layer1(bundle)

    assert not result.gate_passed
    assert not result.reject_available
    assert Pathway.REJECT in result.missing_paths
