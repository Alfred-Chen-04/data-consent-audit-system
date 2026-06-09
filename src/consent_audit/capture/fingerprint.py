"""Multimodal fingerprinting for longitudinal diffing.

The fingerprint is NOT an audit signal — it is a cheap identity check used
by the diff engine to decide "has this banner meaningfully changed?"
before triggering expensive LLM re-analysis.
"""

from hashlib import sha256
from pathlib import Path

from PIL import Image

from consent_audit.models import MultimodalFingerprint


def compute_fingerprint(
    *,
    dom_html: str,
    screenshot_path: Path,
    visible_text: str,
) -> MultimodalFingerprint:
    """Produce (dom_hash, perceptual_image_hash, text_embedding)."""
    return MultimodalFingerprint(
        dom_hash=_hash_text(dom_html),
        perceptual_image_hash=_average_image_hash(screenshot_path),
        text_embedding=_stable_text_vector(visible_text),
    )


def _hash_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def _average_image_hash(path: Path) -> str:
    """Return a compact average hash without requiring the optional imagehash package."""

    with Image.open(path) as image:
        grayscale = image.convert("L").resize((8, 8))
        pixels = list(grayscale.tobytes())

    average = sum(pixels) / len(pixels)
    bits = "".join("1" if pixel >= average else "0" for pixel in pixels)
    content_digest = sha256(bytes(pixels)).hexdigest()[:16]
    return f"{int(bits, 2):016x}:{content_digest}"


def _stable_text_vector(text: str, *, dimensions: int = 16) -> list[float]:
    """Cheap deterministic vector for change detection before real embeddings are wired."""

    digest = sha256(text.encode("utf-8")).digest()
    return [round(digest[i] / 255.0, 6) for i in range(dimensions)]
