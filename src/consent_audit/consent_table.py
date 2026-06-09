"""Lightweight weekly consent-table records.

This module is the paper-first fallback path: even before the full report stack
is mature, each weekly capture can be reduced to a stable, auditable row.
"""

import csv
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from consent_audit.models import (
    CaptureBundle,
    EffortCategory,
    Layer1Result,
    Layer2Result,
    Layer3Result,
    LetterGrade,
    Tier,
)


class ConsentTableRow(BaseModel):
    """One weekly row for paper analysis and manual QA."""

    url: str
    capture_date: str
    captured_at: str
    cohort: str = ""
    banner_detected: bool
    accept_available: bool
    reject_available: bool
    customize_available: bool
    dismiss_available: bool
    layer1_gate_passed: bool
    first_screenshot_ref: str = ""
    first_dom_snapshot_ref: str = ""
    dom_hash: str
    image_hash: str
    layer2_mean_effort: float | None = None
    layer2_overall_category: EffortCategory | None = None
    transparency_grade: LetterGrade | None = None
    unbiased_choice_grade: LetterGrade | None = None
    tier: Tier | None = None
    notes: str = ""


CONSENT_TABLE_FIELDNAMES = list(ConsentTableRow.model_fields)


def row_from_bundle(
    bundle: CaptureBundle,
    layer1: Layer1Result,
    *,
    layer2: Layer2Result | None = None,
    layer3: Layer3Result | None = None,
    tier: Tier | None = None,
    cohort: str = "",
    notes: str = "",
) -> ConsentTableRow:
    """Flatten a capture + layer results into the weekly analysis table."""

    first_layer = bundle.layers[0] if bundle.layers else None
    banner_detected = any(outcome.attempted for outcome in bundle.path_outcomes.values())
    return ConsentTableRow(
        url=str(bundle.url),
        capture_date=bundle.captured_at.date().isoformat(),
        captured_at=bundle.captured_at.isoformat(),
        cohort=cohort,
        banner_detected=banner_detected,
        accept_available=layer1.accept_available,
        reject_available=layer1.reject_available,
        customize_available=layer1.customize_available,
        dismiss_available=layer1.dismiss_available,
        layer1_gate_passed=layer1.gate_passed,
        first_screenshot_ref=first_layer.screenshot_ref if first_layer is not None else "",
        first_dom_snapshot_ref=first_layer.dom_snapshot_ref if first_layer is not None else "",
        dom_hash=bundle.fingerprint.dom_hash,
        image_hash=bundle.fingerprint.perceptual_image_hash,
        layer2_mean_effort=layer2.mean_effort if layer2 is not None else None,
        layer2_overall_category=layer2.overall_category if layer2 is not None else None,
        transparency_grade=(
            layer3.transparency.letter_grade
            if layer3 is not None
            else None
        ),
        unbiased_choice_grade=(
            layer3.unbiased_choice.letter_grade
            if layer3 is not None
            else None
        ),
        tier=tier,
        notes=notes,
    )


def append_row_to_csv(path: Path, row: ConsentTableRow) -> None:
    """Append one row, creating parent directories and the header if needed."""

    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CONSENT_TABLE_FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(_csv_ready(row))


def _csv_ready(row: ConsentTableRow) -> dict[str, str]:
    raw = row.model_dump(mode="json")
    return {field: _csv_cell(raw.get(field)) for field in CONSENT_TABLE_FIELDNAMES}


def _csv_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)
