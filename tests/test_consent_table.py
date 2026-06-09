"""Tests for the lightweight weekly consent-table layer."""

import csv
from datetime import datetime
from pathlib import Path

from consent_audit.consent_table import ConsentTableRow, append_row_to_csv, row_from_bundle
from consent_audit.layers import score_layer1
from consent_audit.models import (
    CaptureBundle,
    EffortCategory,
    ElementRef,
    LayerSnapshot,
    MultimodalFingerprint,
    PathOutcome,
    Pathway,
)


def test_row_from_bundle_records_path_availability_and_hashes() -> None:
    bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30, 9, 0, 0),
        layers=[
            LayerSnapshot(
                layer_index=1,
                screenshot_ref="captures/example/banner.png",
                dom_snapshot_ref="captures/example/banner.html",
                visible_text="We use cookies. Accept All or Reject All.",
            )
        ],
        path_outcomes={
            Pathway.ACCEPT: PathOutcome(
                pathway=Pathway.ACCEPT,
                attempted=True,
                succeeded=True,
                click_depth=1,
                trigger_element=ElementRef(dom_selector="button.accept", visible_text="Accept All"),
            ),
            Pathway.REJECT: PathOutcome(
                pathway=Pathway.REJECT,
                attempted=True,
                succeeded=True,
                click_depth=1,
                trigger_element=ElementRef(dom_selector="button.reject", visible_text="Reject All"),
            ),
            Pathway.CUSTOMIZE: PathOutcome(
                pathway=Pathway.CUSTOMIZE,
                attempted=True,
                succeeded=False,
                click_depth=0,
            ),
        },
        fingerprint=MultimodalFingerprint(
            dom_hash="dom123",
            perceptual_image_hash="img456",
            text_embedding=[0.1, 0.2],
        ),
    )
    layer1 = score_layer1(bundle)

    row = row_from_bundle(bundle, layer1, cohort="deep_sample", notes="pilot")

    assert isinstance(row, ConsentTableRow)
    assert row.url == "https://example.com/"
    assert row.capture_date == "2026-05-30"
    assert row.banner_detected
    assert row.accept_available
    assert row.reject_available
    assert not row.customize_available
    assert row.layer1_gate_passed is False
    assert row.first_screenshot_ref == "captures/example/banner.png"
    assert row.dom_hash == "dom123"
    assert row.image_hash == "img456"
    assert row.cohort == "deep_sample"
    assert row.notes == "pilot"


def test_row_from_bundle_does_not_treat_plain_page_snapshot_as_banner() -> None:
    bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30, 9, 0, 0),
        layers=[
            LayerSnapshot(
                layer_index=1,
                screenshot_ref="captures/example/page.png",
                dom_snapshot_ref="captures/example/page.html",
                visible_text="Example Domain",
            )
        ],
        path_outcomes={
            pathway: PathOutcome(
                pathway=pathway,
                attempted=False,
                succeeded=False,
                click_depth=0,
                failure_reason="no_candidate_detected",
            )
            for pathway in Pathway
        },
        fingerprint=MultimodalFingerprint(
            dom_hash="dom123",
            perceptual_image_hash="img456",
        ),
    )
    layer1 = score_layer1(bundle)

    row = row_from_bundle(bundle, layer1)

    assert row.banner_detected is False
    assert row.first_screenshot_ref == "captures/example/page.png"


def test_append_row_to_csv_writes_header_and_serialized_values(tmp_path: Path) -> None:
    out_csv = tmp_path / "consent_table.csv"
    row = ConsentTableRow(
        url="https://example.com/",
        capture_date="2026-05-30",
        captured_at="2026-05-30T09:00:00",
        cohort="smoke",
        banner_detected=True,
        accept_available=True,
        reject_available=True,
        customize_available=True,
        dismiss_available=False,
        layer1_gate_passed=True,
        first_screenshot_ref="captures/example/banner.png",
        first_dom_snapshot_ref="captures/example/banner.html",
        dom_hash="dom123",
        image_hash="img456",
        layer2_mean_effort=0.1,
        layer2_overall_category=EffortCategory.EASY,
        notes="partial",
    )

    append_row_to_csv(out_csv, row)
    append_row_to_csv(out_csv, row)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    assert len(rows) == 2
    assert rows[0]["url"] == "https://example.com/"
    assert rows[0]["banner_detected"] == "true"
    assert rows[0]["layer2_overall_category"] == "Easy"
    assert rows[0]["transparency_grade"] == ""
