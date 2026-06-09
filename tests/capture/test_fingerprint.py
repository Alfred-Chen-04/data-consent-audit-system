"""Tests for deterministic multimodal fingerprinting."""

from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from consent_audit.capture.fingerprint import compute_fingerprint


def _png(path: Path, color: tuple[int, int, int]) -> None:
    Image.new("RGB", (8, 8), color=color).save(path)


def test_compute_fingerprint_is_stable_for_same_inputs() -> None:
    with TemporaryDirectory() as tmp:
        screenshot = Path(tmp) / "banner.png"
        _png(screenshot, (255, 255, 255))

        first = compute_fingerprint(
            dom_html="<div>Accept</div>",
            screenshot_path=screenshot,
            visible_text="Accept cookies",
        )
        second = compute_fingerprint(
            dom_html="<div>Accept</div>",
            screenshot_path=screenshot,
            visible_text="Accept cookies",
        )

    assert first == second
    assert len(first.dom_hash) == 64
    assert first.perceptual_image_hash
    assert first.text_embedding


def test_compute_fingerprint_changes_when_dom_or_image_changes() -> None:
    with TemporaryDirectory() as tmp:
        first_image = Path(tmp) / "first.png"
        second_image = Path(tmp) / "second.png"
        _png(first_image, (255, 255, 255))
        _png(second_image, (0, 0, 0))

        first = compute_fingerprint(
            dom_html="<div>Accept</div>",
            screenshot_path=first_image,
            visible_text="Accept cookies",
        )
        second = compute_fingerprint(
            dom_html="<div>Reject</div>",
            screenshot_path=second_image,
            visible_text="Reject cookies",
        )

    assert first.dom_hash != second.dom_hash
    assert first.perceptual_image_hash != second.perceptual_image_hash
    assert first.text_embedding != second.text_embedding
