"""Screenshot sanitization — crop to banner region, blur PII zones before storage.

Required by AGENTS.md §8. Applied before any object-store upload.
"""

from pathlib import Path

from PIL import Image, ImageFilter

from consent_audit.models import ScreenshotBBox


def sanitize_screenshot(
    source: Path,
    *,
    crop_to: ScreenshotBBox | None = None,
    blur_regions: list[ScreenshotBBox] | None = None,
) -> Path:
    """Apply crop + blur, write to a new path, return that path."""
    output = source.with_name(f"{source.stem}.sanitized{source.suffix}")
    with Image.open(source) as image:
        working = image.convert("RGB")
        crop_origin = (0, 0)

        if crop_to is not None:
            box = _clamped_box(crop_to, working.size)
            working = working.crop(box)
            crop_origin = (box[0], box[1])

        for region in blur_regions or []:
            box = _clamped_box(region, working.size, offset=crop_origin)
            if box[2] <= box[0] or box[3] <= box[1]:
                continue
            patch = working.crop(box).filter(ImageFilter.GaussianBlur(radius=8))
            working.paste(patch, box)

        working.save(output)

    return output


def _clamped_box(
    bbox: ScreenshotBBox,
    image_size: tuple[int, int],
    *,
    offset: tuple[int, int] = (0, 0),
) -> tuple[int, int, int, int]:
    width, height = image_size
    x1 = max(0, bbox.x - offset[0])
    y1 = max(0, bbox.y - offset[1])
    x2 = min(width, x1 + bbox.width)
    y2 = min(height, y1 + bbox.height)
    return (x1, y1, x2, y2)
