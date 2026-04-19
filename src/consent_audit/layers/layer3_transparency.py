"""Layer 3 — Transparency and Unbiased Choice. Two analytically distinct scores.

CONCEPTS.md §3 forbids collapsing these into one number.
"""

from consent_audit.models import (
    CaptureBundle,
    Layer1Result,
    Layer2Result,
    Layer3Result,
)


def score_layer3(
    bundle: CaptureBundle,
    layer1: Layer1Result,
    layer2: Layer2Result,
) -> Layer3Result:
    """Produce Transparency (topic coverage + framing) AND Unbiased Choice (visual asymmetry).

    Depends on LLM/VLM outputs that should already be attached to the bundle.
    Layer 2 result is passed so we can apply effort-based weighting on bias severity.
    """
    raise NotImplementedError("implement week 4 — depends on llm.text + llm.vision")
