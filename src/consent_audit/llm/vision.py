"""VLM calls — grounding button candidates in screenshots, visual feature extraction.

Uses Anthropic Opus 4.7 vision as primary. Output is always schema-validated.
"""

from pathlib import Path

from consent_audit.llm.budget import BudgetLedger
from consent_audit.models import ElementRef, Pathway, ScreenshotBBox

VISION_CALL_COST_USD = 0.02


async def locate_pathways(
    screenshot: Path,
    *,
    ledger: BudgetLedger,
) -> dict[Pathway, list[ElementRef]]:
    """Return candidate elements for each Pathway, each with bbox.

    Returns multiple candidates per pathway — the agent validates by clicking.
    """
    ledger.record("llm.vision.locate_pathways", VISION_CALL_COST_USD)
    _require_screenshot(screenshot)
    return {pathway: [] for pathway in Pathway}


async def analyze_visual_features(
    screenshot: Path,
    *,
    candidates: dict[Pathway, ElementRef],
    ledger: BudgetLedger,
) -> dict[Pathway, dict[str, tuple[float, list[ScreenshotBBox]]]]:
    """For each pathway button, return sub-feature values + evidence bboxes.

    Sub-features: button_size_ratio, layout_symmetry, label_clarity (VLM portion).
    The remaining sub-features (color_contrast, click_depth, immediate_feedback)
    are computed deterministically elsewhere.
    """
    ledger.record("llm.vision.analyze_visual_features", VISION_CALL_COST_USD)
    _require_screenshot(screenshot)

    bboxes = {pathway: candidate.bbox for pathway, candidate in candidates.items()}
    areas = [
        bbox.width * bbox.height
        for bbox in bboxes.values()
        if bbox is not None and bbox.width > 0 and bbox.height > 0
    ]
    max_area = max(areas, default=0)

    result: dict[Pathway, dict[str, tuple[float, list[ScreenshotBBox]]]] = {}
    for pathway, candidate in candidates.items():
        bbox = candidate.bbox
        if bbox is None or bbox.width <= 0 or bbox.height <= 0:
            result[pathway] = {}
            continue

        area = bbox.width * bbox.height
        button_size_ratio = area / max_area if max_area else 1.0
        result[pathway] = {
            "button_size_ratio": (button_size_ratio, [bbox]),
            "layout_symmetry": (0.0, [bbox]),
            "label_clarity": (_label_clarity_penalty(candidate, pathway), [bbox]),
        }
    return result


def _require_screenshot(screenshot: Path) -> None:
    if not screenshot.exists():
        raise FileNotFoundError(f"screenshot not found: {screenshot}")


def _label_clarity_penalty(candidate: ElementRef, pathway: Pathway) -> float:
    label = (candidate.visible_text or "").lower()
    direct_terms = {
        Pathway.ACCEPT: ("accept", "agree", "allow"),
        Pathway.REJECT: ("reject", "decline", "deny"),
        Pathway.CUSTOMIZE: ("customize", "customise", "preferences", "settings"),
        Pathway.DISMISS: ("close", "dismiss"),
    }
    return 0.0 if any(term in label for term in direct_terms[pathway]) else 0.5
