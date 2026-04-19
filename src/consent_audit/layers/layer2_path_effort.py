"""Layer 2 — Path Effort. Six sub-features, deterministic weighted aggregation.

Weights are fixed in CONCEPTS.md §2. Do not vary per-site.
"""

from consent_audit.models import CaptureBundle, Layer1Result, Layer2Result


# Weights from CONCEPTS.md §2 — sum to 1.0
SUBFEATURE_WEIGHTS: dict[str, float] = {
    "button_size_ratio": 0.25,
    "color_contrast": 0.15,
    "layout_symmetry": 0.15,
    "click_depth": 0.20,
    "label_clarity": 0.15,
    "immediate_feedback": 0.10,
}


def score_layer2(
    bundle: CaptureBundle,
    layer1: Layer1Result,
) -> Layer2Result:
    """Per-pathway effort + overall category.

    Skips pathways where Layer 1 marked not-available.
    """
    raise NotImplementedError("implement week 3-4 — needs VLM vision output")
