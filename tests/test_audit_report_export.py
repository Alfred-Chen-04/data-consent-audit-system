"""Tests for paper-facing AuditReport CSV export."""

import csv
from datetime import UTC, datetime
from pathlib import Path

from consent_audit.audit_export import (
    AUDIT_REPORT_FIELDNAMES,
    audit_report_to_row,
    export_audit_reports_to_csv,
)
from consent_audit.models import (
    AuditReport,
    CaptureBundle,
    EffortCategory,
    Layer1Result,
    Layer2Result,
    Layer3Result,
    LayerSnapshot,
    LetterGrade,
    MultimodalFingerprint,
    PathOutcome,
    Pathway,
    Tier,
    TransparencyResult,
    UnbiasedChoiceResult,
)


def _report() -> AuditReport:
    bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 6, 13, 9, 30, tzinfo=UTC),
        layers=[
            LayerSnapshot(
                layer_index=1,
                screenshot_ref="captures/example/layer1.png",
                dom_snapshot_ref="captures/example/layer1.html",
                visible_text="We use cookies. Accept, reject, or customize choices.",
            )
        ],
        path_outcomes={},
        fingerprint=MultimodalFingerprint(dom_hash="dom123", perceptual_image_hash="img456"),
    )
    layer1 = Layer1Result(
        accept_available=True,
        reject_available=True,
        customize_available=True,
        dismiss_available=False,
        missing_paths=[],
        evidence={},
        gate_passed=True,
    )
    layer2 = Layer2Result(
        per_path_effort={},
        overall_category=EffortCategory.EASY,
        mean_effort=0.25,
    )
    layer3 = Layer3Result(
        transparency=TransparencyResult(
            topic_coverage={},
            framing={},
            letter_grade=LetterGrade.B,
            rationale="fixture",
        ),
        unbiased_choice=UnbiasedChoiceResult(
            asymmetry_score=0.4,
            biased_toward=Pathway.ACCEPT,
            evidence=[],
            letter_grade=LetterGrade.C,
            rationale="fixture",
        ),
    )
    return AuditReport(
        bundle=bundle,
        layer1=layer1,
        layer2=layer2,
        layer3=layer3,
        tier=Tier.COMPLIANT,
        report_markdown="fixture",
        total_api_cost_usd=0.01,
        generated_at=datetime(2026, 6, 13, 9, 31, tzinfo=UTC),
    )


def test_audit_report_to_row_flattens_layer_scores_for_paper_table() -> None:
    row = audit_report_to_row(_report())

    assert row["url"] == "https://example.com/"
    assert row["capture_date"] == "2026-06-13"
    assert row["tier"] == "Compliant"
    assert row["banner_detected"] == "false"
    assert row["layer1_gate_passed"] == "true"
    assert row["accept_available"] == "true"
    assert row["dismiss_available"] == "false"
    assert row["missing_paths"] == ""
    assert row["layer2_mean_effort"] == "0.25"
    assert row["layer2_overall_category"] == "Easy"
    assert row["transparency_grade"] == "B"
    assert row["unbiased_choice_grade"] == "C"
    assert row["biased_toward"] == "accept"
    assert row["first_screenshot_ref"] == "captures/example/layer1.png"
    assert row["dom_hash"] == "dom123"
    assert row["api_cost_usd"] == "0.0100"


def test_export_audit_reports_to_csv_writes_header_and_rows(tmp_path: Path) -> None:
    out_csv = tmp_path / "audit_report_summary.csv"

    export_audit_reports_to_csv(out_csv, [_report()])

    with out_csv.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    assert reader.fieldnames == AUDIT_REPORT_FIELDNAMES
    assert len(rows) == 1
    assert rows[0]["tier"] == "Compliant"


def test_audit_report_to_row_marks_banner_detected_from_attempted_paths() -> None:
    report = _report()
    report.bundle.path_outcomes = {
        Pathway.ACCEPT: PathOutcome(
            pathway=Pathway.ACCEPT,
            attempted=True,
            succeeded=True,
            click_depth=0,
        )
    }

    row = audit_report_to_row(report)

    assert row["banner_detected"] == "true"
