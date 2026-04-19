"""VLM calls — grounding button candidates in screenshots, visual feature extraction.

Uses Anthropic Opus 4.7 vision as primary. Output is always schema-validated.
"""

from pathlib import Path

from consent_audit.llm.budget import BudgetLedger
from consent_audit.models import ElementRef, Pathway, ScreenshotBBox


async def locate_pathways(
    screenshot: Path,
    *,
    ledger: BudgetLedger,
) -> dict[Pathway, list[ElementRef]]:
    """Return candidate elements for each Pathway, each with bbox.

    Returns multiple candidates per pathway — the agent validates by clicking.
    """
    raise NotImplementedError("implement week 2-3")


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
    raise NotImplementedError("implement week 3 — VLM gate")
