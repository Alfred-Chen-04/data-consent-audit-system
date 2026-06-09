"""Tests for the audit-report summary export script."""

import csv
from datetime import UTC, datetime
from pathlib import Path

import pytest

from consent_audit.models import (
    AuditReport,
    CaptureBundle,
    Layer1Result,
    MultimodalFingerprint,
    Pathway,
    Tier,
)
from consent_audit.storage import db
from scripts import export_audit_reports


def _report(
    url: str,
    *,
    generated_at: datetime,
    dom_hash: str,
) -> AuditReport:
    bundle = CaptureBundle(
        url=url,  # type: ignore[arg-type]
        captured_at=generated_at,
        layers=[],
        path_outcomes={},
        fingerprint=MultimodalFingerprint(dom_hash=dom_hash, perceptual_image_hash="img"),
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
        generated_at=generated_at,
    )


def test_run_exports_all_saved_reports_newest_first(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(db, "REPORT_STORE_PATH", tmp_path / "reports.jsonl")
    older = _report(
        "https://example.com",
        generated_at=datetime(2026, 6, 6, tzinfo=UTC),
        dom_hash="old",
    )
    newer = _report(
        "https://other.example",
        generated_at=datetime(2026, 6, 13, tzinfo=UTC),
        dom_hash="new",
    )
    db.save_report(older)
    db.save_report(newer)
    out_csv = tmp_path / "audit_report_summary.csv"

    export_audit_reports._run(out_csv)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    assert [row["dom_hash"] for row in rows] == ["new", "old"]
    assert rows[0]["tier"] == "High-Risk"
