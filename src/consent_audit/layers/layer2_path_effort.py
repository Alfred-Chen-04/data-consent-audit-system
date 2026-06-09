"""Layer 2 — Path Effort. Six sub-features, deterministic weighted aggregation.

Weights are fixed in CONCEPTS.md §2. Do not vary per-site.
"""

from consent_audit.models import (
    CaptureBundle,
    EffortCategory,
    EffortScore,
    EffortSubFeature,
    ElementRef,
    EventLogRef,
    Layer1Result,
    Layer2Result,
    Pathway,
    ScreenshotBBox,
)

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
    per_path_effort: dict[Pathway, EffortScore] = {}
    for pathway in Pathway:
        if not _layer1_available(layer1, pathway):
            continue

        outcome = bundle.path_outcomes.get(pathway)
        if outcome is None:
            continue

        event = _event_for_path(bundle, pathway)
        evidence = _evidence(event, outcome.trigger_element)
        click_depth_value = _click_depth_value(outcome.click_depth)
        immediate_feedback_value = _immediate_feedback_value(event)

        sub_features = [
            EffortSubFeature(
                name="click_depth",
                value=click_depth_value,
                weight=SUBFEATURE_WEIGHTS["click_depth"],
                evidence=evidence,
                rationale=f"{pathway.value} path took {outcome.click_depth} click(s).",
            ),
            EffortSubFeature(
                name="immediate_feedback",
                value=immediate_feedback_value,
                weight=SUBFEATURE_WEIGHTS["immediate_feedback"],
                evidence=evidence,
                rationale="Click produced a success event." if immediate_feedback_value == 0 else "No success event was recorded.",
            ),
        ]
        score = round(sum(feature.value * feature.weight for feature in sub_features), 6)
        per_path_effort[pathway] = EffortScore(
            pathway=pathway,
            sub_features=sub_features,
            score=score,
        )

    mean_effort = (
        round(
            sum(effort.score for effort in per_path_effort.values()) / len(per_path_effort),
            6,
        )
        if per_path_effort
        else 0.0
    )
    return Layer2Result(
        per_path_effort=per_path_effort,
        overall_category=_category(mean_effort),
        mean_effort=mean_effort,
    )


def _layer1_available(layer1: Layer1Result, pathway: Pathway) -> bool:
    return {
        Pathway.ACCEPT: layer1.accept_available,
        Pathway.REJECT: layer1.reject_available,
        Pathway.CUSTOMIZE: layer1.customize_available,
        Pathway.DISMISS: layer1.dismiss_available,
    }[pathway]


def _event_for_path(bundle: CaptureBundle, pathway: Pathway) -> EventLogRef | None:
    action = f"click_{pathway.value}"
    return next((event for event in bundle.event_log if event.action == action), None)


def _evidence(
    event: EventLogRef | None,
    element: ElementRef | None,
) -> list[ElementRef | ScreenshotBBox | EventLogRef]:
    if event is not None:
        return [event]
    if element is not None:
        return [element]
    return []


def _click_depth_value(click_depth: int) -> float:
    if click_depth <= 1:
        return 0.0
    if click_depth == 2:
        return 0.5
    return 1.0


def _immediate_feedback_value(event: EventLogRef | None) -> float:
    if event is None:
        return 0.5
    return 0.0 if event.outcome == "success" else 1.0


def _category(mean_effort: float) -> EffortCategory:
    if mean_effort <= 0.30:
        return EffortCategory.EASY
    if mean_effort <= 0.60:
        return EffortCategory.AVERAGE
    return EffortCategory.POOR
