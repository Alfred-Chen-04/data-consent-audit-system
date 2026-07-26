"""Tests for the fact-only closeout pre-freeze manifest."""

import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from consent_audit.closeout_manifest import (
    DecisionSheetSpec,
    build_closeout_prefreeze_manifest,
    export_closeout_prefreeze_manifest,
)


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_manifest_classifies_actual_reference_and_decision_states(
    tmp_path: Path,
) -> None:
    screenshot = tmp_path / "data/captures/site/layer1.png"
    screenshot.parent.mkdir(parents=True)
    screenshot.write_bytes(b"png evidence")
    audit_csv = tmp_path / "data/research_package/audit.csv"
    _write_csv(
        audit_csv,
        ["report_id", "first_screenshot_ref", "first_dom_snapshot_ref"],
        [
            {
                "report_id": "1",
                "first_screenshot_ref": "data/captures/site/layer1.png",
                "first_dom_snapshot_ref": "data/captures/site/layer1.html",
            },
            {
                "report_id": "2",
                "first_screenshot_ref": "https://example.com/evidence.png",
                "first_dom_snapshot_ref": "",
            },
            {
                "report_id": "3",
                "first_screenshot_ref": "../outside.png",
                "first_dom_snapshot_ref": "data/captures/site/layer1.html",
            },
        ],
    )
    longitudinal_csv = tmp_path / "data/research_package/longitudinal.csv"
    _write_csv(longitudinal_csv, ["week_of"], [{"week_of": "2026-06-06"}])
    decisions = tmp_path / "data/decisions.csv"
    _write_csv(
        decisions,
        ["review_status", "confirmed_decision"],
        [
            {"review_status": "pending", "confirmed_decision": ""},
            {"review_status": "complete", "confirmed_decision": "keep"},
        ],
    )
    deliverable = tmp_path / "docs/deliverable.txt"
    deliverable.parent.mkdir(parents=True)
    deliverable.write_text("deliverable", encoding="utf-8")

    manifest = build_closeout_prefreeze_manifest(
        tmp_path,
        generated_at=datetime(2026, 7, 26, 12, tzinfo=UTC),
        audit_csv=audit_csv,
        longitudinal_csv=longitudinal_csv,
        decision_sheets=(
            DecisionSheetSpec(
                "review",
                decisions,
                "review_status",
                "confirmed_decision",
            ),
        ),
        deliverable_paths=(deliverable, tmp_path / "docs/missing.txt"),
    )

    assert manifest["manifest_status"] == "pre_freeze"
    assert manifest["finalized"] is False
    assert manifest["repository_path"] == "."
    screenshot_refs = manifest["reference_audit"]["first_screenshot_ref"]
    assert screenshot_refs["status_counts_by_row"] == {
        "external": 1,
        "outside_repo": 1,
        "present": 1,
    }
    assert "<outside_repo>/outside.png" in {
        record["ref"] for record in screenshot_refs["references"]
    }
    present_ref = next(
        record
        for record in screenshot_refs["references"]
        if record["status"] == "present"
    )
    assert present_ref["sha256"] == hashlib.sha256(b"png evidence").hexdigest()
    dom_refs = manifest["reference_audit"]["first_dom_snapshot_ref"]
    assert dom_refs["blank_rows"] == 1
    assert dom_refs["status_counts_by_row"] == {"missing": 2}
    pdf_refs = manifest["reference_audit"]["report_pdf_ref"]
    assert pdf_refs["column_present"] is False
    assert pdf_refs["blank_rows"] is None
    assert manifest["decision_gates"]["review"]["pending_count"] == 1
    assert manifest["decision_gates"]["review"]["blank_confirmation_count"] == 1
    assert manifest["decision_gates"]["review"]["open_row_count"] == 1
    assert [item["status"] for item in manifest["key_deliverables"]] == [
        "present",
        "missing",
    ]
    assert str(tmp_path) not in json.dumps(manifest)


def test_export_writes_json_and_explicit_nonfinal_markdown(tmp_path: Path) -> None:
    audit_csv = tmp_path / "data/research_package/audit_report_summary.csv"
    longitudinal_csv = tmp_path / "data/research_package/longitudinal_summary.csv"
    _write_csv(audit_csv, ["report_id"], [{"report_id": "1"}])
    _write_csv(longitudinal_csv, ["week_of"], [{"week_of": "2026-06-06"}])
    out_json = Path("data/closeout/manifest.json")
    out_markdown = Path("docs/research/manifest.md")

    export_closeout_prefreeze_manifest(
        tmp_path,
        out_json,
        out_markdown,
        generated_at=datetime(2026, 7, 26, 12, tzinfo=UTC),
    )

    saved = json.loads((tmp_path / out_json).read_text(encoding="utf-8"))
    markdown = (tmp_path / out_markdown).read_text(encoding="utf-8")
    assert saved["manifest_status"] == "pre_freeze"
    assert saved["finalized"] is False
    assert "not a final or frozen manifest" in markdown
    assert "../../data/closeout/manifest.json" in markdown
    assert "uv run consent-audit closeout-prefreeze-manifest" in markdown
