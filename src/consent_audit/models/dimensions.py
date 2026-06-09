"""Controlled vocabulary for audit dimensions.

Every string that names an audit concept MUST come from one of these enums.
Anchored in CONCEPTS.md — do not add values here without updating CONCEPTS.md first.
"""

from enum import StrEnum


class Pathway(StrEnum):
    """The four consent outcomes (CONCEPTS.md §0)."""

    ACCEPT = "accept"
    REJECT = "reject"
    CUSTOMIZE = "customize"
    DISMISS = "dismiss"


class LetterGrade(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class EffortCategory(StrEnum):
    """Layer 2 summary bucket (CONCEPTS.md §2)."""

    EASY = "Easy"
    AVERAGE = "Average"
    POOR = "Poor"


class DisclosureTopic(StrEnum):
    """Four mandatory topics for Layer-3 Transparency coverage (CONCEPTS.md §3.1a)."""

    DATA_TYPES = "data_types"
    PURPOSES = "purposes"
    THIRD_PARTY_SHARING = "third_party_sharing"
    CONSEQUENCES = "consequences"


class FramingMechanism(StrEnum):
    """Layer-3 framing-effect channels (CONCEPTS.md §3.1b)."""

    EMPHASIS = "emphasis"
    LINGUISTIC_COMPLEXITY = "linguistic_complexity"
    SEQUENCING = "sequencing"
    SELECTIVE_PROMINENCE = "selective_prominence"


class BiasLevel(StrEnum):
    NEUTRAL = "neutral"
    MILD_BIAS = "mild_bias"
    STRONG_BIAS = "strong_bias"


class Tier(StrEnum):
    """Overall audit tier (CONCEPTS.md §4). Categorical by design."""

    EXEMPLARY = "Exemplary"
    COMPLIANT = "Compliant"
    MARGINAL = "Marginal"
    HIGH_RISK = "High-Risk"


class ChangeEventType(StrEnum):
    """Diff engine outputs (CONCEPTS.md §5)."""

    LAYOUT_CHANGE = "layout_change"
    COPY_CHANGE = "copy_change"
    DOM_RESTRUCTURE = "dom_restructure"
    PATHWAY_CHANGE = "pathway_change"
    SCORE_CHANGE = "score_change"
