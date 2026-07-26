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
    revision_matrix = tmp_path / "data/revision_matrix.csv"
    _write_csv(
        revision_matrix,
        [
            "revision_id",
            "decision_id",
            "artifact",
            "execution_status",
            "selected_value",
            "response_basis",
            "applied_by",
            "applied_at",
        ],
        [
            {
                "revision_id": "rev_waiting",
                "decision_id": "scope",
                "artifact": "presentation",
                "execution_status": "waiting_for_response_branch",
                "selected_value": "",
                "response_basis": "",
                "applied_by": "",
                "applied_at": "",
            },
            {
                "revision_id": "rev_applied",
                "decision_id": "scope",
                "artifact": "poster",
                "execution_status": "applied_verified",
                "selected_value": "pilot",
                "response_basis": "actual_advisor_response",
                "applied_by": "researcher",
                "applied_at": "2026-07-26T20:00:00+08:00",
            },
        ],
    )
    joint_decisions = tmp_path / "data/joint_decisions.csv"
    _write_csv(
        joint_decisions,
        [
            "decision_id",
            "recommended_default",
            "decision_options",
            "review_status",
            "confirmed_decision",
            "reviewer",
            "review_date",
            "notes",
        ],
        [
            {
                "decision_id": "scope",
                "recommended_default": "pilot",
                "decision_options": "pilot|other",
                "review_status": "confirmed",
                "confirmed_decision": "pilot",
                "reviewer": "advisor",
                "review_date": "2026-07-26",
                "notes": "",
            }
        ],
    )

    manifest = build_closeout_prefreeze_manifest(
        tmp_path,
        generated_at=datetime(2026, 7, 26, 12, tzinfo=UTC),
        audit_csv=audit_csv,
        longitudinal_csv=longitudinal_csv,
        revision_matrix_csv=revision_matrix,
        joint_decision_csv=joint_decisions,
        required_revision_ids=("rev_waiting", "rev_applied"),
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
    assert manifest["schema_version"] == 2
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
    revision_gate = manifest["revision_execution_gate"]
    assert revision_gate["row_count"] == 2
    assert revision_gate["status_counts"] == {
        "applied_verified": 1,
        "waiting_for_response_branch": 1,
    }
    assert revision_gate["not_applied_verified_count"] == 1
    assert revision_gate["row_states_valid"] is True
    assert revision_gate["coverage_valid"] is True
    assert manifest["freeze_readiness"]["ready_for_final_freeze"] is False
    assert {
        blocker["code"] for blocker in manifest["freeze_readiness"]["blockers"]
    } == {"missing_key_deliverables", "revision_rows_not_applied_verified"}
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
    assert saved["freeze_readiness"]["ready_for_final_freeze"] is False
    assert saved["freeze_readiness"]["blockers"] == [
        {"code": "missing_key_deliverables", "count": 12},
        {"code": "revision_matrix_missing", "count": 1},
    ]
    assert "not a final or frozen manifest" in markdown
    assert "## Revision Execution Gate" in markdown
    assert "Ready for final freeze: `false`" in markdown
    assert "../../data/closeout/manifest.json" in markdown
    assert "uv run consent-audit closeout-prefreeze-manifest" in markdown


def test_manifest_readiness_requires_verified_rows_with_provenance(
    tmp_path: Path,
) -> None:
    audit_csv = tmp_path / "audit.csv"
    longitudinal_csv = tmp_path / "longitudinal.csv"
    deliverable = tmp_path / "deliverable.txt"
    matrix = tmp_path / "revision_matrix.csv"
    joint_decisions = tmp_path / "joint_decisions.csv"
    _write_csv(audit_csv, ["report_id"], [{"report_id": "1"}])
    _write_csv(longitudinal_csv, ["week_of"], [{"week_of": "2026-06-06"}])
    deliverable.write_text("ready", encoding="utf-8")
    fields = [
        "revision_id",
        "decision_id",
        "artifact",
        "execution_status",
        "selected_value",
        "response_basis",
        "applied_by",
        "applied_at",
    ]
    applied_row = {
        "revision_id": "rev_1",
        "decision_id": "shared_scope_framing",
        "artifact": "presentation",
        "execution_status": "applied_verified",
        "selected_value": "five_site_pilot_method",
        "response_basis": "project_fallback_after_internal_cutoff",
        "applied_by": "researcher",
        "applied_at": "2026-07-30T09:00:00+08:00",
    }
    _write_csv(matrix, fields, [applied_row])
    _write_csv(
        joint_decisions,
        [
            "decision_id",
            "recommended_default",
            "decision_options",
            "review_status",
            "confirmed_decision",
            "reviewer",
            "review_date",
            "notes",
        ],
        [
            {
                "decision_id": "shared_scope_framing",
                "recommended_default": "five_site_pilot_method",
                "decision_options": "five_site_pilot_method|other",
                "review_status": "pending",
                "confirmed_decision": "",
                "reviewer": "",
                "review_date": "",
                "notes": "",
            }
        ],
    )

    ready = build_closeout_prefreeze_manifest(
        tmp_path,
        generated_at=datetime(2026, 7, 30, 1, tzinfo=UTC),
        audit_csv=audit_csv,
        longitudinal_csv=longitudinal_csv,
        revision_matrix_csv=matrix,
        joint_decision_csv=joint_decisions,
        required_revision_ids=("rev_1",),
        decision_sheets=(),
        deliverable_paths=(deliverable,),
    )

    assert ready["freeze_readiness"] == {
        "ready_for_final_freeze": True,
        "blocker_count": 0,
        "blockers": [],
    }

    incomplete = build_closeout_prefreeze_manifest(
        tmp_path,
        generated_at=datetime(2026, 7, 30, 1, tzinfo=UTC),
        audit_csv=audit_csv,
        longitudinal_csv=longitudinal_csv,
        revision_matrix_csv=matrix,
        joint_decision_csv=joint_decisions,
        required_revision_ids=("rev_1", "rev_2"),
        decision_sheets=(),
        deliverable_paths=(deliverable,),
    )
    assert incomplete["revision_execution_gate"][
        "missing_required_revision_ids"
    ] == ["rev_2"]
    assert incomplete["freeze_readiness"]["blockers"] == [
        {"code": "revision_matrix_missing_required_rows", "count": 1}
    ]

    applied_row["applied_at"] = "2026-07-30T09:00:00"
    _write_csv(matrix, fields, [applied_row])
    invalid = build_closeout_prefreeze_manifest(
        tmp_path,
        generated_at=datetime(2026, 7, 30, 1, tzinfo=UTC),
        audit_csv=audit_csv,
        longitudinal_csv=longitudinal_csv,
        revision_matrix_csv=matrix,
        joint_decision_csv=joint_decisions,
        required_revision_ids=("rev_1",),
        decision_sheets=(),
        deliverable_paths=(deliverable,),
    )

    assert invalid["revision_execution_gate"]["inconsistent_revision_ids"] == [
        "rev_1"
    ]
    assert invalid["freeze_readiness"]["ready_for_final_freeze"] is False
    assert invalid["freeze_readiness"]["blockers"] == [
        {"code": "revision_matrix_inconsistent_rows", "count": 1}
    ]

    applied_row["applied_at"] = "2026-07-29T23:58:00+08:00"
    _write_csv(matrix, fields, [applied_row])
    too_early = build_closeout_prefreeze_manifest(
        tmp_path,
        generated_at=datetime(2026, 7, 29, 15, 58, tzinfo=UTC),
        audit_csv=audit_csv,
        longitudinal_csv=longitudinal_csv,
        revision_matrix_csv=matrix,
        joint_decision_csv=joint_decisions,
        required_revision_ids=("rev_1",),
        decision_sheets=(),
        deliverable_paths=(deliverable,),
    )

    assert too_early["revision_execution_gate"][
        "response_basis_validation_errors"
    ] == [
        {"revision_id": "rev_1", "code": "fallback_before_internal_cutoff"}
    ]
    assert too_early["freeze_readiness"]["blockers"] == [
        {"code": "revision_response_basis_unverified", "count": 1}
    ]


def test_manifest_blocks_invalid_joint_decision_contract(tmp_path: Path) -> None:
    audit_csv = tmp_path / "audit.csv"
    longitudinal_csv = tmp_path / "longitudinal.csv"
    deliverable = tmp_path / "deliverable.txt"
    matrix = tmp_path / "revision_matrix.csv"
    joint_decisions = tmp_path / "joint_decisions.csv"
    _write_csv(audit_csv, ["report_id"], [{"report_id": "1"}])
    _write_csv(longitudinal_csv, ["week_of"], [{"week_of": "2026-06-06"}])
    deliverable.write_text("ready", encoding="utf-8")
    _write_csv(
        matrix,
        [
            "revision_id",
            "decision_id",
            "artifact",
            "execution_status",
            "selected_value",
            "response_basis",
            "applied_by",
            "applied_at",
        ],
        [
            {
                "revision_id": "rev_1",
                "decision_id": "scope",
                "artifact": "presentation",
                "execution_status": "applied_verified",
                "selected_value": "mistyped_value",
                "response_basis": "actual_advisor_response",
                "applied_by": "researcher",
                "applied_at": "2026-07-27T10:00:00+08:00",
            }
        ],
    )
    _write_csv(
        joint_decisions,
        [
            "decision_id",
            "recommended_default",
            "decision_options",
            "review_status",
            "confirmed_decision",
            "reviewer",
            "review_date",
            "notes",
        ],
        [
            {
                "decision_id": "scope",
                "recommended_default": "unlisted_default",
                "decision_options": "pilot|other",
                "review_status": "confirmed",
                "confirmed_decision": "mistyped_value",
                "reviewer": "advisor",
                "review_date": "2026-07-27",
                "notes": "",
            }
        ],
    )

    manifest = build_closeout_prefreeze_manifest(
        tmp_path,
        generated_at=datetime(2026, 7, 27, 2, tzinfo=UTC),
        audit_csv=audit_csv,
        longitudinal_csv=longitudinal_csv,
        revision_matrix_csv=matrix,
        joint_decision_csv=joint_decisions,
        required_revision_ids=("rev_1",),
        decision_sheets=(),
        deliverable_paths=(deliverable,),
    )

    revision_gate = manifest["revision_execution_gate"]
    assert revision_gate["joint_decision_contract_validation_errors"] == [
        {"decision_id": "scope", "code": "recommended_default_not_in_options"},
        {"decision_id": "scope", "code": "confirmed_decision_not_in_options"},
    ]
    assert revision_gate["joint_decision_contract_valid"] is False
    assert manifest["summary"]["joint_decision_contract_error_count"] == 2
    assert manifest["freeze_readiness"]["blockers"] == [
        {"code": "joint_decision_contract_invalid", "count": 1}
    ]
