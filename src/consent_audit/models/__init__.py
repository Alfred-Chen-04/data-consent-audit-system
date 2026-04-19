"""Pydantic schemas. Shared interface between capture, layers, storage, and report.

All cross-module types live here. Do not re-define the same concept elsewhere.
"""

from consent_audit.models.audit import (
    AuditReport,
    CaptureBundle,
    ChangeEvent,
    ElementRef,
    Layer1Result,
    Layer2Result,
    Layer3Result,
    LayerSnapshot,
    MultimodalFingerprint,
    PathOutcome,
    ScreenshotBBox,
    Tier,
)
from consent_audit.models.dimensions import (
    BiasLevel,
    DisclosureTopic,
    EffortCategory,
    FramingMechanism,
    LetterGrade,
    Pathway,
)

__all__ = [
    "AuditReport",
    "BiasLevel",
    "CaptureBundle",
    "ChangeEvent",
    "DisclosureTopic",
    "EffortCategory",
    "ElementRef",
    "FramingMechanism",
    "Layer1Result",
    "Layer2Result",
    "Layer3Result",
    "LayerSnapshot",
    "LetterGrade",
    "MultimodalFingerprint",
    "Pathway",
    "PathOutcome",
    "ScreenshotBBox",
    "Tier",
]
