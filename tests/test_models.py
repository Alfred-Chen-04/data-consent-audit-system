"""Schema round-trip sanity checks. Ensures every model serializes and validates."""

from datetime import datetime
from uuid import uuid4

from consent_audit.models import (
    CaptureBundle,
    Layer1Result,
    MultimodalFingerprint,
    Pathway,
)
from consent_audit.models.audit import ElementRef, PathOutcome


def test_capture_bundle_roundtrip() -> None:
    bundle = CaptureBundle(
        bundle_id=uuid4(),
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime.utcnow(),
        layers=[],
        path_outcomes={
            Pathway.ACCEPT: PathOutcome(
                pathway=Pathway.ACCEPT,
                attempted=True,
                succeeded=True,
                click_depth=1,
            ),
        },
        fingerprint=MultimodalFingerprint(
            dom_hash="abc",
            perceptual_image_hash="def",
            text_embedding=[0.1, 0.2, 0.3],
        ),
    )
    dumped = bundle.model_dump_json()
    restored = CaptureBundle.model_validate_json(dumped)
    assert restored.bundle_id == bundle.bundle_id
    assert restored.path_outcomes[Pathway.ACCEPT].click_depth == 1


def test_layer1_result_gate_flag() -> None:
    result = Layer1Result(
        accept_available=True,
        reject_available=False,
        customize_available=True,
        dismiss_available=True,
        missing_paths=[Pathway.REJECT],
        evidence={Pathway.ACCEPT: ElementRef(dom_selector="button.accept")},
        gate_passed=False,
    )
    assert not result.gate_passed
    assert Pathway.REJECT in result.missing_paths
