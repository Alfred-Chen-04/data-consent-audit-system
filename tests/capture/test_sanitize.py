"""Tests for screenshot sanitization."""

from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from consent_audit.capture.sanitize import sanitize_screenshot
from consent_audit.models import ScreenshotBBox


def test_sanitize_screenshot_crops_and_writes_new_file() -> None:
    with TemporaryDirectory() as tmp:
        source = Path(tmp) / "source.png"
        Image.new("RGB", (20, 20), color=(255, 0, 0)).save(source)

        sanitized = sanitize_screenshot(
            source,
            crop_to=ScreenshotBBox(
                screenshot_ref=str(source),
                x=5,
                y=5,
                width=10,
                height=8,
            ),
        )

        with Image.open(sanitized) as img:
            size = img.size

    assert sanitized != source
    assert sanitized.name == "source.sanitized.png"
    assert size == (10, 8)


def test_sanitize_screenshot_blurs_regions_without_changing_dimensions() -> None:
    with TemporaryDirectory() as tmp:
        source = Path(tmp) / "source.png"
        Image.new("RGB", (20, 20), color=(255, 0, 0)).save(source)

        sanitized = sanitize_screenshot(
            source,
            blur_regions=[
                ScreenshotBBox(
                    screenshot_ref=str(source),
                    x=2,
                    y=2,
                    width=6,
                    height=6,
                )
            ],
        )

        with Image.open(sanitized) as img:
            size = img.size

    assert size == (20, 20)
