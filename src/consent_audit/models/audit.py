"""Core data models. All cross-module communication flows through these types.

Every field that represents an audit finding should carry an evidence reference
(ElementRef or ScreenshotBBox) so scores remain traceable — see CONCEPTS.md §2.
"""

from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl

from consent_audit.models.dimensions import (
    BiasLevel,
    ChangeEventType,
    DisclosureTopic,
    EffortCategory,
    FramingMechanism,
    LetterGrade,
    Pathway,
    Tier,
)

# ─── Evidence primitives ──────────────────────────────────────────────────────


class ScreenshotBBox(BaseModel):
    """A rectangular region on a captured screenshot. Pixel coordinates."""

    screenshot_ref: str  # object-store key or local path
    x: int
    y: int
    width: int
    height: int


class ElementRef(BaseModel):
    """A reference to a DOM element + its visual location."""

    dom_selector: str  # CSS selector stable enough for replay
    xpath: str | None = None
    bbox: ScreenshotBBox | None = None
    visible_text: str | None = None


class EventLogRef(BaseModel):
    """A reference to an entry in the agent's per-run event log."""

    event_index: int
    action: str  # "click", "scroll", "wait", ...
    target: ElementRef | None = None
    outcome: str  # "success", "blocked", "no_effect"


# ─── Capture stage output ─────────────────────────────────────────────────────


class LayerSnapshot(BaseModel):
    """One layer of the consent interface (first or second)."""

    layer_index: int  # 1 = banner, 2 = settings panel
    screenshot_ref: str
    dom_snapshot_ref: str
    visible_text: str


class PathOutcome(BaseModel):
    """Result of the agent attempting one pathway."""

    pathway: Pathway
    attempted: bool
    succeeded: bool
    click_depth: int
    trigger_element: ElementRef | None = None
    failure_reason: str | None = None


class MultimodalFingerprint(BaseModel):
    """Cheap identity signature used by the diff engine."""

    dom_hash: str
    perceptual_image_hash: str
    text_embedding: list[float] = Field(default_factory=list)


class CaptureBundle(BaseModel):
    """Immutable snapshot of a site's consent interface at a point in time."""

    bundle_id: UUID = Field(default_factory=uuid4)
    url: HttpUrl
    captured_at: datetime
    layers: list[LayerSnapshot]
    path_outcomes: dict[Pathway, PathOutcome]
    fingerprint: MultimodalFingerprint
    event_log: list[EventLogRef] = Field(default_factory=list)
    capture_warnings: list[str] = Field(default_factory=list)


# ─── Layer 1 ──────────────────────────────────────────────────────────────────


class Layer1Result(BaseModel):
    """Path Availability — CONCEPTS.md §1."""

    accept_available: bool
    reject_available: bool
    customize_available: bool
    dismiss_available: bool
    missing_paths: list[Pathway]
    evidence: dict[Pathway, ElementRef]
    gate_passed: bool  # False if any required path is missing → skip Layer 2/3


# ─── Layer 2 ──────────────────────────────────────────────────────────────────


class EffortSubFeature(BaseModel):
    """One of the six Path-Effort sub-features. Every value carries evidence."""

    name: str
    value: float = Field(ge=0.0, le=1.0)
    weight: float = Field(ge=0.0, le=1.0)
    evidence: list[ElementRef | ScreenshotBBox | EventLogRef]
    rationale: str


class EffortScore(BaseModel):
    """Aggregated effort score for one pathway."""

    pathway: Pathway
    sub_features: list[EffortSubFeature]
    score: float = Field(ge=0.0, le=1.0)


class Layer2Result(BaseModel):
    """Path Effort — CONCEPTS.md §2."""

    per_path_effort: dict[Pathway, EffortScore]
    overall_category: EffortCategory
    mean_effort: float = Field(ge=0.0, le=1.0)


# ─── Layer 3 ──────────────────────────────────────────────────────────────────


class TopicCoverageResult(BaseModel):
    """One row of the Disclosure Topic Coverage table — CONCEPTS.md §3.1a."""

    topic: DisclosureTopic
    present: bool
    clarity_grade: LetterGrade
    evidence_quote: str | None = None
    evidence_ref: ElementRef | None = None
    consistent_with_layer2: bool | None = None


class FramingResult(BaseModel):
    """One framing mechanism's bias reading — CONCEPTS.md §3.1b."""

    mechanism: FramingMechanism
    level: BiasLevel
    rationale: str
    evidence_quotes: list[str]


class TransparencyResult(BaseModel):
    topic_coverage: dict[DisclosureTopic, TopicCoverageResult]
    framing: dict[FramingMechanism, FramingResult]
    letter_grade: LetterGrade
    rationale: str


class UnbiasedChoiceResult(BaseModel):
    """Layer-3 structural/visual asymmetry — CONCEPTS.md §3.2."""

    asymmetry_score: float = Field(ge=0.0, le=1.0)
    biased_toward: Pathway | None = None
    evidence: list[ElementRef]
    letter_grade: LetterGrade
    rationale: str


class Layer3Result(BaseModel):
    """Layer 3 = Transparency AND Unbiased Choice (kept separate — CONCEPTS.md §3.2)."""

    transparency: TransparencyResult
    unbiased_choice: UnbiasedChoiceResult


# ─── Final report ─────────────────────────────────────────────────────────────


class AuditReport(BaseModel):
    """Full audit of one site at one time. The unit of persistence in the DB."""

    report_id: UUID = Field(default_factory=uuid4)
    bundle: CaptureBundle
    layer1: Layer1Result
    layer2: Layer2Result | None  # None if Layer 1 gate failed
    layer3: Layer3Result | None  # None if Layer 1 gate failed
    tier: Tier
    report_markdown: str
    report_pdf_ref: str | None = None
    total_api_cost_usd: float
    generated_at: datetime


# ─── Longitudinal primitives ──────────────────────────────────────────────────


class ChangeEvent(BaseModel):
    """One detected change between two consecutive captures (CONCEPTS.md §5)."""

    change_type: ChangeEventType
    from_bundle_id: UUID
    to_bundle_id: UUID
    magnitude: float  # normalized strength of the change
    description: str  # LLM-authored summary referencing evidence


class WeeklySummary(BaseModel):
    """LLM-authored summary of the week's changes for one site."""

    url: HttpUrl
    week_of: datetime
    events: list[ChangeEvent]
    summary: str
    severity: LetterGrade  # reuses A..F scale
    implications_for_user: str


__all__ = [
    "AuditReport",
    "CaptureBundle",
    "ChangeEvent",
    "EffortScore",
    "EffortSubFeature",
    "ElementRef",
    "EventLogRef",
    "FramingResult",
    "Layer1Result",
    "Layer2Result",
    "Layer3Result",
    "LayerSnapshot",
    "MultimodalFingerprint",
    "PathOutcome",
    "ScreenshotBBox",
    "TopicCoverageResult",
    "TransparencyResult",
    "UnbiasedChoiceResult",
    "WeeklySummary",
]


# Keep Path importable for type-hint callers that want to refer to file paths
_ = Path  # re-export shim; some downstream modules import Path from here
