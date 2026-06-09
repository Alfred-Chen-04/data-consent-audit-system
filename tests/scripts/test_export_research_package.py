"""Tests for one-command research package export."""

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from consent_audit.models import (
    AuditReport,
    CaptureBundle,
    ChangeEvent,
    ChangeEventType,
    Layer1Result,
    LetterGrade,
    MultimodalFingerprint,
    Pathway,
    Tier,
    WeeklySummary,
)
from consent_audit.storage import db
from scripts import export_research_package


def _report() -> AuditReport:
    captured_at = datetime(2026, 6, 13, tzinfo=UTC)
    bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=captured_at,
        layers=[],
        path_outcomes={},
        fingerprint=MultimodalFingerprint(dom_hash="dom", perceptual_image_hash="img"),
    )
    layer1 = Layer1Result(
        accept_available=False,
        reject_available=False,
        customize_available=False,
        dismiss_available=False,
        missing_paths=list(Pathway),
        evidence={},
        gate_passed=False,
    )
    return AuditReport(
        bundle=bundle,
        layer1=layer1,
        layer2=None,
        layer3=None,
        tier=Tier.HIGH_RISK,
        report_markdown="fixture",
        total_api_cost_usd=0.0,
        generated_at=captured_at,
    )


def _weekly_summary() -> WeeklySummary:
    return WeeklySummary(
        url="https://example.com",  # type: ignore[arg-type]
        week_of=datetime(2026, 6, 13, tzinfo=UTC),
        events=[
            ChangeEvent(
                change_type=ChangeEventType.SCORE_CHANGE,
                from_bundle_id=uuid4(),
                to_bundle_id=uuid4(),
                magnitude=1.0,
                description="Score changed.",
            )
        ],
        summary="Score changed.",
        severity=LetterGrade.D,
        implications_for_user="Inspect score evidence.",
    )


def test_run_exports_a_complete_research_package(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(db, "REPORT_STORE_PATH", tmp_path / "reports.jsonl")
    monkeypatch.setattr(db, "WEEKLY_SUMMARY_STORE_PATH", tmp_path / "weekly_summaries.jsonl")
    db.save_report(_report())
    db.save_weekly_summary(_weekly_summary())
    out_dir = tmp_path / "research_package"

    manifest = export_research_package._run(out_dir, limit=50)

    audit_csv = out_dir / "audit_report_summary.csv"
    longitudinal_csv = out_dir / "longitudinal_summary.csv"
    manifest_path = out_dir / "research_manifest.json"

    assert audit_csv.exists()
    assert longitudinal_csv.exists()
    assert manifest_path.exists()
    assert manifest["audit_report_count"] == 1
    assert manifest["weekly_summary_count"] == 1
    assert manifest["files"] == {
        "audit_report_summary": "audit_report_summary.csv",
        "longitudinal_summary": "longitudinal_summary.csv",
    }

    with audit_csv.open(newline="", encoding="utf-8") as fh:
        assert len(list(csv.DictReader(fh))) == 1
    with longitudinal_csv.open(newline="", encoding="utf-8") as fh:
        assert len(list(csv.DictReader(fh))) == 1

    saved_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert saved_manifest == manifest
