"""Multimodal fingerprinting for longitudinal diffing.

The fingerprint is NOT an audit signal — it is a cheap identity check used
by the diff engine to decide "has this banner meaningfully changed?"
before triggering expensive LLM re-analysis.
"""

from pathlib import Path

from consent_audit.models import MultimodalFingerprint


def compute_fingerprint(
    *,
    dom_html: str,
    screenshot_path: Path,
    visible_text: str,
) -> MultimodalFingerprint:
    """Produce (dom_hash, perceptual_image_hash, text_embedding)."""
    raise NotImplementedError("implement in week 2 alongside capture.agent")
