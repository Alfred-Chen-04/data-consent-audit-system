"""Screenshot sanitization — crop to banner region, blur PII zones before storage.

Required by AGENTS.md §8. Applied before any object-store upload.
"""

from pathlib import Path

from consent_audit.models import ScreenshotBBox


def sanitize_screenshot(
    source: Path,
    *,
    crop_to: ScreenshotBBox | None = None,
    blur_regions: list[ScreenshotBBox] | None = None,
) -> Path:
    """Apply crop + blur, write to a new path, return that path."""
    raise NotImplementedError("implement in week 1 — gate for data ethics review")
