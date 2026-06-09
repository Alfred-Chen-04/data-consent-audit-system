"""Tests for deterministic vision wrapper fallbacks."""

from pathlib import Path

import pytest
from PIL import Image

from consent_audit.llm.budget import BudgetExceeded, BudgetLedger
from consent_audit.llm.vision import analyze_visual_features, locate_pathways
from consent_audit.models import ElementRef, Pathway, ScreenshotBBox


def _screenshot(path: Path) -> Path:
    Image.new("RGB", (24, 16), "white").save(path)
    return path


@pytest.mark.asyncio
async def test_locate_pathways_records_budget_and_returns_no_hallucinated_candidates(
    tmp_path: Path,
) -> None:
    ledger = BudgetLedger(cap_usd=1.0)
    screenshot = _screenshot(tmp_path / "banner.png")

    result = await locate_pathways(screenshot, ledger=ledger)

    assert ledger.entries == [("llm.vision.locate_pathways", 0.02)]
    assert result == {pathway: [] for pathway in Pathway}


@pytest.mark.asyncio
async def test_analyze_visual_features_records_budget_and_preserves_bbox_evidence(
    tmp_path: Path,
) -> None:
    ledger = BudgetLedger(cap_usd=1.0)
    screenshot = _screenshot(tmp_path / "banner.png")
    bbox = ScreenshotBBox(
        screenshot_ref=str(screenshot),
        x=1,
        y=2,
        width=8,
        height=4,
    )

    result = await analyze_visual_features(
        screenshot,
        candidates={
            Pathway.ACCEPT: ElementRef(
                dom_selector="button.accept",
                visible_text="Accept",
                bbox=bbox,
            )
        },
        ledger=ledger,
    )

    assert ledger.entries == [("llm.vision.analyze_visual_features", 0.02)]
    assert result[Pathway.ACCEPT]["button_size_ratio"] == (1.0, [bbox])
    assert result[Pathway.ACCEPT]["layout_symmetry"] == (0.0, [bbox])
    assert result[Pathway.ACCEPT]["label_clarity"] == (0.0, [bbox])


@pytest.mark.asyncio
async def test_vision_wrappers_fail_cleanly_when_budget_cap_is_exceeded(tmp_path: Path) -> None:
    ledger = BudgetLedger(cap_usd=0.0)
    screenshot = _screenshot(tmp_path / "banner.png")

    with pytest.raises(BudgetExceeded):
        await locate_pathways(screenshot, ledger=ledger)

    assert ledger.spent_usd == 0.0
    assert ledger.entries == []
