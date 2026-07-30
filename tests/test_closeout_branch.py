"""Tests for safe closeout response-branch preparation."""

import csv
from datetime import datetime
from pathlib import Path

import pytest

from consent_audit.closeout_branch import (
    parse_as_of,
    prepare_closeout_revision_branch,
    render_closeout_branch_result,
)

MATRIX_FIELDS = [
    "revision_id",
    "decision_id",
    "artifact",
    "execution_status",
    "selected_value",
    "response_basis",
    "applied_by",
    "applied_at",
]
JOINT_FIELDS = [
    "decision_id",
    "recommended_default",
    "decision_options",
    "review_status",
    "confirmed_decision",
    "reviewer",
    "review_date",
    "notes",
]
PROJECT_FIELDS = [
    "decision_id",
    "selected_value",
    "decision_maker",
    "decided_at",
    "authorization_source",
    "rationale",
    "source_evidence",
]


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _matrix_row(revision_id: str, decision_id: str) -> dict[str, str]:
    return {
        "revision_id": revision_id,
        "decision_id": decision_id,
        "artifact": "presentation",
        "execution_status": "waiting_for_response_branch",
        "selected_value": "",
        "response_basis": "",
        "applied_by": "",
        "applied_at": "",
    }


def _joint_row(
    decision_id: str,
    default: str,
    *,
    status: str = "pending",
    confirmed: str = "",
) -> dict[str, str]:
    return {
        "decision_id": decision_id,
        "recommended_default": default,
        "decision_options": f"{default}|alternate|other",
        "review_status": status,
        "confirmed_decision": confirmed,
        "reviewer": "advisor" if status == "confirmed" else "",
        "review_date": "2026-07-27" if status == "confirmed" else "",
        "notes": "",
    }


def test_before_cutoff_pending_branch_is_a_noop(tmp_path: Path) -> None:
    matrix = tmp_path / "matrix.csv"
    joint = tmp_path / "joint.csv"
    _write_csv(matrix, MATRIX_FIELDS, [_matrix_row("rev_1", "shared_scope_framing")])
    _write_csv(
        joint,
        JOINT_FIELDS,
        [_joint_row("shared_scope_framing", "five_site_pilot_method")],
    )
    original = matrix.read_bytes()

    result = prepare_closeout_revision_branch(
        joint_decision_csv=joint,
        revision_matrix_csv=matrix,
        as_of=datetime.fromisoformat("2026-07-27T12:00:00+08:00"),
        write=True,
        required_revision_ids=("rev_1",),
    )

    assert result.write_requested is True
    assert result.write_performed is False
    assert result.waiting_decision_ids == ("shared_scope_framing",)
    assert result.rows_waiting_count == 1
    assert matrix.read_bytes() == original
    assert "record actual responses or wait" in render_closeout_branch_result(result)


def test_actual_response_prepares_only_its_rows(tmp_path: Path) -> None:
    matrix = tmp_path / "matrix.csv"
    joint = tmp_path / "joint.csv"
    _write_csv(
        matrix,
        MATRIX_FIELDS,
        [
            _matrix_row("rev_scope", "shared_scope_framing"),
            _matrix_row("rev_cards", "main_evidence_cards"),
        ],
    )
    _write_csv(
        joint,
        JOINT_FIELDS,
        [
            _joint_row(
                "shared_scope_framing",
                "five_site_pilot_method",
                status="confirmed",
                confirmed="alternate",
            ),
            _joint_row("main_evidence_cards", "guardian_and_coca_cola"),
        ],
    )

    result = prepare_closeout_revision_branch(
        joint_decision_csv=joint,
        revision_matrix_csv=matrix,
        as_of=datetime.fromisoformat("2026-07-27T12:00:00+08:00"),
        write=True,
        required_revision_ids=("rev_scope", "rev_cards"),
    )

    rows = _read_rows(matrix)
    assert result.actual_decision_count == 1
    assert result.fallback_decision_count == 0
    assert result.rows_prepared_count == 1
    assert result.rows_waiting_count == 1
    assert rows[0]["execution_status"] == "ready_to_apply"
    assert rows[0]["selected_value"] == "alternate"
    assert rows[0]["response_basis"] == "actual_advisor_response"
    assert rows[1]["execution_status"] == "waiting_for_response_branch"
    assert rows[1]["selected_value"] == ""


def test_project_owner_decision_prepares_rows_before_cutoff(tmp_path: Path) -> None:
    matrix = tmp_path / "matrix.csv"
    joint = tmp_path / "joint.csv"
    project = tmp_path / "project.csv"
    _write_csv(matrix, MATRIX_FIELDS, [_matrix_row("rev_1", "shared_scope_framing")])
    _write_csv(
        joint,
        JOINT_FIELDS,
        [_joint_row("shared_scope_framing", "five_site_pilot_method")],
    )
    _write_csv(
        project,
        PROJECT_FIELDS,
        [
            {
                "decision_id": "shared_scope_framing",
                "selected_value": "five_site_pilot_method",
                "decision_maker": "project_owner",
                "decided_at": "2026-07-29T10:41:49+08:00",
                "authorization_source": "project owner instruction",
                "rationale": "bounded evidence",
                "source_evidence": "audit.md",
            }
        ],
    )

    dry_run = prepare_closeout_revision_branch(
        joint_decision_csv=joint,
        project_decision_csv=project,
        revision_matrix_csv=matrix,
        as_of=datetime.fromisoformat("2026-07-29T11:00:00+08:00"),
        required_revision_ids=("rev_1",),
    )
    assert dry_run.project_owner_decision_count == 1
    assert dry_run.fallback_decision_count == 0
    assert dry_run.rows_prepared_count == 1

    written = prepare_closeout_revision_branch(
        joint_decision_csv=joint,
        project_decision_csv=project,
        revision_matrix_csv=matrix,
        as_of=datetime.fromisoformat("2026-07-29T11:00:00+08:00"),
        write=True,
        required_revision_ids=("rev_1",),
    )
    row = _read_rows(matrix)[0]
    assert written.write_performed is True
    assert row["execution_status"] == "ready_to_apply"
    assert row["selected_value"] == "five_site_pilot_method"
    assert row["response_basis"] == "project_owner_decision"


def test_after_cutoff_uses_actual_and_fallback_branches_together(
    tmp_path: Path,
) -> None:
    matrix = tmp_path / "matrix.csv"
    joint = tmp_path / "joint.csv"
    _write_csv(
        matrix,
        MATRIX_FIELDS,
        [
            _matrix_row("rev_scope", "shared_scope_framing"),
            _matrix_row("rev_cards", "main_evidence_cards"),
        ],
    )
    _write_csv(
        joint,
        JOINT_FIELDS,
        [
            _joint_row(
                "shared_scope_framing",
                "five_site_pilot_method",
                status="confirmed",
                confirmed="alternate",
            ),
            _joint_row("main_evidence_cards", "guardian_and_coca_cola"),
        ],
    )

    original = matrix.read_bytes()
    dry_run = prepare_closeout_revision_branch(
        joint_decision_csv=joint,
        revision_matrix_csv=matrix,
        as_of=datetime.fromisoformat("2026-07-30T00:01:00+08:00"),
        write=False,
        required_revision_ids=("rev_scope", "rev_cards"),
    )
    assert dry_run.rows_prepared_count == 2
    assert dry_run.write_performed is False
    assert matrix.read_bytes() == original

    result = prepare_closeout_revision_branch(
        joint_decision_csv=joint,
        revision_matrix_csv=matrix,
        as_of=datetime.fromisoformat("2026-07-30T00:01:00+08:00"),
        write=True,
        required_revision_ids=("rev_scope", "rev_cards"),
    )

    rows = _read_rows(matrix)
    assert result.actual_decision_count == 1
    assert result.fallback_decision_count == 1
    assert result.rows_prepared_count == 2
    assert result.rows_waiting_count == 0
    assert rows[0]["selected_value"] == "alternate"
    assert rows[0]["response_basis"] == "actual_advisor_response"
    assert rows[1]["selected_value"] == "guardian_and_coca_cola"
    assert (
        rows[1]["response_basis"]
        == "project_fallback_after_internal_cutoff"
    )


def test_invalid_contract_and_existing_conflict_do_not_modify_matrix(
    tmp_path: Path,
) -> None:
    matrix = tmp_path / "matrix.csv"
    joint = tmp_path / "joint.csv"
    row = _matrix_row("rev_1", "shared_scope_framing")
    _write_csv(matrix, MATRIX_FIELDS, [row])
    invalid_joint = _joint_row(
        "shared_scope_framing",
        "five_site_pilot_method",
        status="confirmed",
        confirmed="not_an_option",
    )
    _write_csv(joint, JOINT_FIELDS, [invalid_joint])
    original = matrix.read_bytes()

    with pytest.raises(ValueError, match="confirmed_decision_not_in_options"):
        prepare_closeout_revision_branch(
            joint_decision_csv=joint,
            revision_matrix_csv=matrix,
            as_of=datetime.fromisoformat("2026-07-27T12:00:00+08:00"),
            write=True,
            required_revision_ids=("rev_1",),
        )
    assert matrix.read_bytes() == original

    valid_joint = _joint_row(
        "shared_scope_framing",
        "five_site_pilot_method",
        status="confirmed",
        confirmed="alternate",
    )
    row.update(
        execution_status="ready_to_apply",
        selected_value="five_site_pilot_method",
        response_basis="actual_advisor_response",
    )
    _write_csv(matrix, MATRIX_FIELDS, [row])
    _write_csv(joint, JOINT_FIELDS, [valid_joint])
    conflicting = matrix.read_bytes()

    with pytest.raises(ValueError, match="existing selected branch conflicts"):
        prepare_closeout_revision_branch(
            joint_decision_csv=joint,
            revision_matrix_csv=matrix,
            as_of=datetime.fromisoformat("2026-07-27T12:00:00+08:00"),
            write=True,
            required_revision_ids=("rev_1",),
        )
    assert matrix.read_bytes() == conflicting


def test_parse_as_of_requires_timezone() -> None:
    assert parse_as_of("2026-07-27T12:00:00Z").utcoffset() is not None
    with pytest.raises(ValueError, match="include a timezone"):
        parse_as_of("2026-07-27T12:00:00")
