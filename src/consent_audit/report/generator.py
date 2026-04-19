"""Human-readable report from structured layer results.

Critical: every claim in the report text must cite an evidence ref from the underlying
schema (ElementRef or ScreenshotBBox). This is the anti-hallucination discipline
from AGENTS.md §2 principle 1.
"""

from datetime import datetime

from consent_audit.models import (
    AuditReport,
    CaptureBundle,
    Layer1Result,
    Layer2Result,
    Layer3Result,
    Tier,
)


def generate_report(
    bundle: CaptureBundle,
    layer1: Layer1Result,
    layer2: Layer2Result | None,
    layer3: Layer3Result | None,
    *,
    api_cost_usd: float,
) -> AuditReport:
    """Assemble the final AuditReport with Markdown body + tier classification."""
    raise NotImplementedError("implement week 5")


def classify_tier(
    layer1: Layer1Result,
    layer2: Layer2Result | None,
    layer3: Layer3Result | None,
) -> Tier:
    """Map layer results to the four-tier categorical summary (CONCEPTS.md §4)."""
    raise NotImplementedError("implement week 5")


# Imported for type re-export convenience
_ = datetime
