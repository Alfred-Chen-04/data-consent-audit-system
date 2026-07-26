"""Build a fact-only pre-freeze manifest for SSRP closeout artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


@dataclass(frozen=True)
class DecisionSheetSpec:
    """Columns needed to summarize one human-decision gate."""

    name: str
    path: Path
    status_column: str | None
    confirmation_column: str


DEFAULT_AUDIT_CSV = Path("data/research_package/audit_report_summary.csv")
DEFAULT_LONGITUDINAL_CSV = Path(
    "data/research_package/longitudinal_summary.csv"
)
DEFAULT_REVISION_MATRIX_CSV = Path(
    "data/closeout/joint_decision_revision_matrix_2026-07-26.csv"
)
DEFAULT_JOINT_DECISION_CSV = Path(
    "data/joint_advisor_review_decision_sheet_2026-07-25.csv"
)
DEFAULT_REFERENCE_COLUMNS = (
    "first_screenshot_ref",
    "first_dom_snapshot_ref",
    "report_pdf_ref",
)
REVISION_MATRIX_REQUIRED_COLUMNS = (
    "revision_id",
    "decision_id",
    "artifact",
    "execution_status",
    "selected_value",
    "response_basis",
    "applied_by",
    "applied_at",
)
JOINT_DECISION_REQUIRED_COLUMNS = (
    "decision_id",
    "recommended_default",
    "decision_options",
    "review_status",
    "confirmed_decision",
    "reviewer",
    "review_date",
    "notes",
)
ALLOWED_REVISION_STATUSES = frozenset(
    {
        "waiting_for_response_branch",
        "ready_to_apply",
        "applied_verified",
    }
)
ALLOWED_RESPONSE_BASES = frozenset(
    {
        "actual_advisor_response",
        "project_fallback_after_internal_cutoff",
    }
)
PROJECT_FALLBACK_CUTOFF = datetime(
    2026,
    7,
    29,
    23,
    59,
    tzinfo=timezone(timedelta(hours=8)),
)
PROJECT_FALLBACK_VALUES = {
    "shared_scope_framing": "five_site_pilot_method",
    "main_evidence_cards": "guardian_and_coca_cola",
    "contrast_case_treatment": "no_visible_first_screen_banner_contrast",
    "unresolved_review_items": (
        "carry_as_visible_limitations_unless_stronger_claims_requested"
    ),
    "rq2_continuity_gate": (
        "freeze_current_evidence_unless_specific_rq2_question_is_approved"
    ),
}
DEFAULT_REQUIRED_REVISION_IDS = (
    "scope_presentation_cover",
    "scope_presentation_snapshot",
    "scope_presentation_closeout",
    "scope_poster_eyebrow",
    "scope_poster_status",
    "scope_poster_footer",
    "scope_evidence_manifest",
    "cards_presentation_guardian",
    "cards_presentation_coca",
    "cards_poster_guardian",
    "cards_poster_coca",
    "contrast_presentation",
    "contrast_poster",
    "contrast_evidence_tables",
    "unresolved_presentation",
    "unresolved_poster",
    "unresolved_evidence",
    "rq2_presentation",
    "rq2_poster",
    "rq2_evidence",
)
DEFAULT_DECISION_SHEETS = (
    DecisionSheetSpec(
        "joint_advisor_review",
        DEFAULT_JOINT_DECISION_CSV,
        "review_status",
        "confirmed_decision",
    ),
    DecisionSheetSpec(
        "poster_review",
        Path("data/poster_review_decision_sheet_2026-07-16.csv"),
        "review_status",
        "confirmed_decision",
    ),
    DecisionSheetSpec(
        "current_five",
        Path("data/current_five_decision_sheet_2026-06-19.csv"),
        None,
        "confirmed_decision",
    ),
    DecisionSheetSpec(
        "cmp_manual_review",
        Path("data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv"),
        "confirmation_status",
        "confirmed_decision",
    ),
)
DEFAULT_DELIVERABLE_PATHS = (
    DEFAULT_AUDIT_CSV,
    DEFAULT_LONGITUDINAL_CSV,
    Path("data/research_package/research_manifest.json"),
    Path(
        "docs/research/presentation/"
        "ssrp_consent_audit_presentation_draft_2026-07-22.pptx"
    ),
    Path(
        "docs/research/presentation/"
        "ssrp_consent_audit_presentation_draft_2026-07-22_montage.png"
    ),
    Path("docs/research/poster/ssrp_poster_aligned_review_2026-07-25.pptx"),
    Path("docs/research/poster/ssrp_poster_aligned_review_2026-07-25.pdf"),
    Path("docs/research/poster/ssrp_poster_aligned_review_2026-07-25.png"),
    Path(
        "docs/research/joint_review/"
        "ssrp_joint_advisor_review_2026-07-25.zip"
    ),
    DEFAULT_JOINT_DECISION_CSV,
    Path(
        "docs/research/"
        "july26_advisor_response_and_fallback_protocol_2026-07-26.md"
    ),
    DEFAULT_REVISION_MATRIX_CSV,
    Path("docs/research/july26_decision_to_revision_matrix_2026-07-26.md"),
    Path("docs/research/closeout_control_index_2026-07-26.md"),
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _repo_relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root).as_posix()


def _resolve_input(repo_root: Path, path: Path) -> Path:
    return path.resolve() if path.is_absolute() else (repo_root / path).resolve()


def _outside_repo_label(path: Path) -> str:
    return f"<outside_repo>/{path.name or 'path'}"


def _file_record(repo_root: Path, path: Path) -> dict[str, Any]:
    resolved = _resolve_input(repo_root, path)
    try:
        relative = _repo_relative(repo_root, resolved)
    except ValueError:
        return {"path": _outside_repo_label(path), "status": "outside_repo"}
    if not resolved.is_file():
        return {"path": relative, "status": "missing"}
    return {
        "path": relative,
        "status": "present",
        "bytes": resolved.stat().st_size,
        "sha256": _sha256(resolved),
    }


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _table_record(repo_root: Path, path: Path) -> dict[str, Any]:
    record = _file_record(repo_root, path)
    if record["status"] != "present":
        return {**record, "row_count": None, "columns": []}
    fields, rows = _read_csv(_resolve_input(repo_root, path))
    return {**record, "row_count": len(rows), "columns": fields}


def _classify_reference(repo_root: Path, raw_ref: str) -> dict[str, Any]:
    parsed = urlsplit(raw_ref)
    if parsed.scheme or parsed.netloc or raw_ref.startswith("//"):
        return {"ref": raw_ref, "status": "external"}

    candidate = Path(raw_ref)
    resolved = _resolve_input(repo_root, candidate)
    try:
        relative = _repo_relative(repo_root, resolved)
    except ValueError:
        return {"ref": _outside_repo_label(candidate), "status": "outside_repo"}
    if not resolved.is_file():
        return {"ref": relative, "status": "missing"}
    return {
        "ref": relative,
        "status": "present",
        "bytes": resolved.stat().st_size,
        "sha256": _sha256(resolved),
    }


def _reference_record(
    repo_root: Path,
    rows: Sequence[dict[str, str]],
    fields: Sequence[str],
    column: str,
) -> dict[str, Any]:
    if column not in fields:
        return {
            "column_present": False,
            "total_rows": len(rows),
            "nonblank_rows": None,
            "blank_rows": None,
            "status_counts_by_row": None,
            "unique_reference_count": 0,
            "status_counts_unique": {},
            "references": [],
        }

    raw_refs = [(row.get(column) or "").strip() for row in rows]
    nonblank_refs = [ref for ref in raw_refs if ref]
    records_by_raw_ref = {
        ref: _classify_reference(repo_root, ref) for ref in sorted(set(nonblank_refs))
    }
    unique_records = list(records_by_raw_ref.values())
    row_statuses = [records_by_raw_ref[ref]["status"] for ref in nonblank_refs]
    return {
        "column_present": True,
        "total_rows": len(rows),
        "nonblank_rows": len(nonblank_refs),
        "blank_rows": len(raw_refs) - len(nonblank_refs),
        "status_counts_by_row": dict(sorted(Counter(row_statuses).items())),
        "unique_reference_count": len(unique_records),
        "status_counts_unique": dict(
            sorted(Counter(record["status"] for record in unique_records).items())
        ),
        "references": unique_records,
    }


def _decision_gate_record(
    repo_root: Path,
    spec: DecisionSheetSpec,
) -> dict[str, Any]:
    record = _file_record(repo_root, spec.path)
    if record["status"] != "present":
        return {
            **record,
            "row_count": None,
            "status_column": spec.status_column,
            "status_column_present": None,
            "status_counts": None,
            "pending_count": None,
            "confirmation_column": spec.confirmation_column,
            "confirmation_column_present": None,
            "blank_confirmation_count": None,
            "open_row_count": None,
        }

    fields, rows = _read_csv(_resolve_input(repo_root, spec.path))
    status_present = spec.status_column in fields if spec.status_column else None
    status_counts: dict[str, int] | None = None
    pending_count: int | None = None
    if spec.status_column and status_present:
        statuses = [(row.get(spec.status_column) or "").strip() for row in rows]
        status_counts = dict(sorted(Counter(statuses).items()))
        pending_count = sum(status.casefold() == "pending" for status in statuses)

    confirmation_present = spec.confirmation_column in fields
    blank_count: int | None = None
    if confirmation_present:
        blank_count = sum(
            not (row.get(spec.confirmation_column) or "").strip() for row in rows
        )

    open_rows: set[int] = set()
    if spec.status_column and status_present:
        open_rows.update(
            index
            for index, row in enumerate(rows)
            if (row.get(spec.status_column) or "").strip().casefold() == "pending"
        )
    if confirmation_present:
        open_rows.update(
            index
            for index, row in enumerate(rows)
            if not (row.get(spec.confirmation_column) or "").strip()
        )

    return {
        **record,
        "row_count": len(rows),
        "status_column": spec.status_column,
        "status_column_present": status_present,
        "status_counts": status_counts,
        "pending_count": pending_count,
        "confirmation_column": spec.confirmation_column,
        "confirmation_column_present": confirmation_present,
        "blank_confirmation_count": blank_count,
        "open_row_count": len(open_rows),
    }


def _has_timezone(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _joint_decision_contract_errors(
    *,
    source_present: bool,
    fields: Sequence[str],
    rows: Sequence[dict[str, str]],
    required_decision_ids: set[str],
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    def add(decision_id: str, code: str) -> None:
        item = {"decision_id": decision_id, "code": code}
        if item not in errors:
            errors.append(item)

    if not source_present:
        add("<sheet>", "joint_decision_source_missing")
        return errors

    missing_columns = sorted(set(JOINT_DECISION_REQUIRED_COLUMNS) - set(fields))
    for column in missing_columns:
        add("<sheet>", f"joint_decision_missing_column:{column}")
    if missing_columns:
        return errors

    decision_ids = [
        (row.get("decision_id") or "").strip() for row in rows
    ]
    decision_id_counts = Counter(
        decision_id for decision_id in decision_ids if decision_id
    )
    for index, decision_id in enumerate(decision_ids, start=1):
        if not decision_id:
            add(f"<row_{index}>", "decision_id_missing")
    for decision_id, count in sorted(decision_id_counts.items()):
        if count > 1:
            add(decision_id, "decision_id_not_unique")
    for decision_id in sorted(required_decision_ids - set(decision_id_counts)):
        add(decision_id, "required_decision_missing")

    for index, row in enumerate(rows, start=1):
        decision_id = (row.get("decision_id") or "").strip() or f"<row_{index}>"
        options = {
            option.strip()
            for option in (row.get("decision_options") or "").split("|")
            if option.strip()
        }
        recommended_default = (row.get("recommended_default") or "").strip()
        status = (row.get("review_status") or "").strip().casefold()
        confirmed_decision = (row.get("confirmed_decision") or "").strip()
        reviewer = (row.get("reviewer") or "").strip()
        review_date = (row.get("review_date") or "").strip()
        notes = (row.get("notes") or "").strip()

        if not recommended_default:
            add(decision_id, "recommended_default_missing")
        elif recommended_default not in options:
            add(decision_id, "recommended_default_not_in_options")
        if "other" not in options:
            add(decision_id, "other_option_missing")

        if status == "pending":
            if any((confirmed_decision, reviewer, review_date)):
                add(decision_id, "pending_response_fields_not_blank")
        elif status == "confirmed":
            if not all((confirmed_decision, reviewer, review_date)):
                add(decision_id, "confirmed_response_fields_missing")
            if confirmed_decision and confirmed_decision not in options:
                add(decision_id, "confirmed_decision_not_in_options")
            if confirmed_decision == "other" and not notes:
                add(decision_id, "other_response_notes_missing")
        else:
            add(decision_id, "review_status_invalid")

    return errors


def _revision_matrix_record(
    repo_root: Path,
    path: Path,
    *,
    generated_at: datetime,
    joint_decision_csv: Path,
    required_revision_ids: Sequence[str],
) -> dict[str, Any]:
    record = _file_record(repo_root, path)
    response_source = _file_record(repo_root, joint_decision_csv)
    if record["status"] != "present":
        return {
            **record,
            "row_count": None,
            "columns": [],
            "missing_required_columns": list(REVISION_MATRIX_REQUIRED_COLUMNS),
            "status_counts": {},
            "artifact_counts": {},
            "decision_counts": {},
            "blank_selected_value_count": None,
            "blank_response_basis_count": None,
            "blank_applied_by_count": None,
            "blank_applied_at_count": None,
            "not_applied_verified_count": None,
            "duplicate_revision_ids": [],
            "missing_required_revision_ids": sorted(required_revision_ids),
            "unexpected_revision_ids": [],
            "coverage_valid": False,
            "inconsistent_revision_ids": [],
            "schema_valid": False,
            "row_states_valid": False,
            "response_basis_claim_count": None,
            "actual_response_basis_count": None,
            "project_fallback_basis_count": None,
            "response_basis_source": response_source,
            "response_basis_validation_errors": [],
            "response_basis_claims_valid": False,
            "joint_decision_contract_validation_errors": [],
            "joint_decision_contract_valid": False,
        }

    fields, rows = _read_csv(_resolve_input(repo_root, path))
    missing_columns = sorted(set(REVISION_MATRIX_REQUIRED_COLUMNS) - set(fields))

    def value(row: dict[str, str], column: str) -> str:
        return (row.get(column) or "").strip()

    status_counts = Counter(value(row, "execution_status") for row in rows)
    artifact_counts = Counter(value(row, "artifact") for row in rows)
    decision_counts = Counter(value(row, "decision_id") for row in rows)
    revision_id_counts = Counter(
        value(row, "revision_id") for row in rows if value(row, "revision_id")
    )
    duplicate_revision_ids = sorted(
        revision_id for revision_id, count in revision_id_counts.items() if count > 1
    )
    actual_revision_ids = set(revision_id_counts)
    expected_revision_ids = set(required_revision_ids)
    missing_required_revision_ids = sorted(
        expected_revision_ids - actual_revision_ids
    )
    unexpected_revision_ids = sorted(actual_revision_ids - expected_revision_ids)

    joint_fields: list[str] = []
    joint_rows: list[dict[str, str]] = []
    if response_source["status"] == "present":
        joint_fields, joint_rows = _read_csv(
            _resolve_input(repo_root, joint_decision_csv)
        )
    joint_schema_valid = set(JOINT_DECISION_REQUIRED_COLUMNS).issubset(
        joint_fields
    )
    joint_rows_by_id: dict[str, list[dict[str, str]]] = {}
    for row in joint_rows:
        decision_id = (row.get("decision_id") or "").strip()
        if decision_id:
            joint_rows_by_id.setdefault(decision_id, []).append(row)

    joint_contract_errors = _joint_decision_contract_errors(
        source_present=response_source["status"] == "present",
        fields=joint_fields,
        rows=joint_rows,
        required_decision_ids={
            decision_id for decision_id in decision_counts if decision_id
        },
    )

    response_basis_errors: list[dict[str, str]] = []

    def add_basis_error(revision_id: str, code: str) -> None:
        item = {"revision_id": revision_id, "code": code}
        if item not in response_basis_errors:
            response_basis_errors.append(item)

    inconsistent_revision_ids: list[str] = []
    claimed_rows_by_decision: dict[str, list[tuple[str, str, str]]] = {}
    for index, row in enumerate(rows, start=1):
        raw_revision_id = value(row, "revision_id")
        revision_id = raw_revision_id or f"<row_{index}>"
        decision_id = value(row, "decision_id")
        artifact = value(row, "artifact")
        status = value(row, "execution_status")
        selected_value = value(row, "selected_value")
        response_basis = value(row, "response_basis")
        applied_by = value(row, "applied_by")
        applied_at = value(row, "applied_at")

        inconsistent = (
            not all((raw_revision_id, decision_id, artifact))
            or status not in ALLOWED_REVISION_STATUSES
            or (response_basis and response_basis not in ALLOWED_RESPONSE_BASES)
        )
        if status == "waiting_for_response_branch":
            inconsistent = inconsistent or any(
                (selected_value, response_basis, applied_by, applied_at)
            )
        elif status == "ready_to_apply":
            inconsistent = inconsistent or not selected_value or not response_basis
            inconsistent = inconsistent or bool(applied_by or applied_at)
        elif status == "applied_verified":
            inconsistent = inconsistent or not all(
                (selected_value, response_basis, applied_by, applied_at)
            )
            inconsistent = inconsistent or (
                bool(applied_at) and not _has_timezone(applied_at)
            )
        if inconsistent:
            inconsistent_revision_ids.append(revision_id)

        if response_basis in ALLOWED_RESPONSE_BASES:
            claimed_rows_by_decision.setdefault(decision_id, []).append(
                (revision_id, selected_value, response_basis)
            )
            if response_source["status"] != "present":
                add_basis_error(revision_id, "joint_decision_source_missing")
                continue
            if not joint_schema_valid:
                add_basis_error(revision_id, "joint_decision_schema_invalid")
                continue
            source_rows = joint_rows_by_id.get(decision_id, [])
            if len(source_rows) != 1:
                add_basis_error(revision_id, "joint_decision_id_not_unique")
                continue
            source_row = source_rows[0]
            source_status = value(source_row, "review_status").casefold()
            source_value = value(source_row, "confirmed_decision")
            source_reviewer = value(source_row, "reviewer")
            source_date = value(source_row, "review_date")
            if response_basis == "actual_advisor_response":
                if source_status != "confirmed":
                    add_basis_error(revision_id, "actual_response_not_confirmed")
                if not source_value or source_value != selected_value:
                    add_basis_error(revision_id, "actual_response_value_mismatch")
                if not source_reviewer or not source_date:
                    add_basis_error(revision_id, "actual_response_provenance_missing")
            else:
                if generated_at < PROJECT_FALLBACK_CUTOFF:
                    add_basis_error(revision_id, "fallback_before_internal_cutoff")
                if PROJECT_FALLBACK_VALUES.get(decision_id) != selected_value:
                    add_basis_error(revision_id, "fallback_value_mismatch")
                if (
                    source_status != "pending"
                    or source_value
                    or source_reviewer
                    or source_date
                ):
                    add_basis_error(
                        revision_id, "fallback_conflicts_with_recorded_response"
                    )

    for claimed_rows in claimed_rows_by_decision.values():
        selected_branches = {
            (selected_value, response_basis)
            for _, selected_value, response_basis in claimed_rows
        }
        if len(selected_branches) > 1:
            for revision_id, _, _ in claimed_rows:
                add_basis_error(revision_id, "decision_rows_disagree")

    return {
        **record,
        "row_count": len(rows),
        "columns": fields,
        "missing_required_columns": missing_columns,
        "status_counts": dict(sorted(status_counts.items())),
        "artifact_counts": dict(sorted(artifact_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "blank_selected_value_count": sum(
            not value(row, "selected_value") for row in rows
        ),
        "blank_response_basis_count": sum(
            not value(row, "response_basis") for row in rows
        ),
        "blank_applied_by_count": sum(not value(row, "applied_by") for row in rows),
        "blank_applied_at_count": sum(not value(row, "applied_at") for row in rows),
        "not_applied_verified_count": sum(
            value(row, "execution_status") != "applied_verified" for row in rows
        ),
        "duplicate_revision_ids": duplicate_revision_ids,
        "missing_required_revision_ids": missing_required_revision_ids,
        "unexpected_revision_ids": unexpected_revision_ids,
        "coverage_valid": not missing_required_revision_ids
        and not unexpected_revision_ids,
        "inconsistent_revision_ids": inconsistent_revision_ids,
        "schema_valid": not missing_columns,
        "row_states_valid": not duplicate_revision_ids
        and not inconsistent_revision_ids
        and bool(rows),
        "response_basis_claim_count": sum(
            bool(value(row, "response_basis")) for row in rows
        ),
        "actual_response_basis_count": sum(
            value(row, "response_basis") == "actual_advisor_response"
            for row in rows
        ),
        "project_fallback_basis_count": sum(
            value(row, "response_basis")
            == "project_fallback_after_internal_cutoff"
            for row in rows
        ),
        "response_basis_source": {
            **response_source,
            "schema_valid": joint_schema_valid,
        },
        "response_basis_validation_errors": response_basis_errors,
        "response_basis_claims_valid": not response_basis_errors,
        "joint_decision_contract_validation_errors": joint_contract_errors,
        "joint_decision_contract_valid": not joint_contract_errors,
    }


def _freeze_readiness(
    *,
    missing_deliverable_count: int,
    revision_matrix: dict[str, Any],
) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    if missing_deliverable_count:
        blockers.append(
            {
                "code": "missing_key_deliverables",
                "count": missing_deliverable_count,
            }
        )
    if revision_matrix["status"] != "present":
        blockers.append({"code": "revision_matrix_missing", "count": 1})
    else:
        missing_columns = revision_matrix["missing_required_columns"]
        if missing_columns:
            blockers.append(
                {
                    "code": "revision_matrix_missing_required_columns",
                    "count": len(missing_columns),
                }
            )
        duplicate_ids = revision_matrix["duplicate_revision_ids"]
        if duplicate_ids:
            blockers.append(
                {
                    "code": "revision_matrix_duplicate_revision_ids",
                    "count": len(duplicate_ids),
                }
            )
        missing_revision_ids = revision_matrix["missing_required_revision_ids"]
        if missing_revision_ids:
            blockers.append(
                {
                    "code": "revision_matrix_missing_required_rows",
                    "count": len(missing_revision_ids),
                }
            )
        unexpected_revision_ids = revision_matrix["unexpected_revision_ids"]
        if unexpected_revision_ids:
            blockers.append(
                {
                    "code": "revision_matrix_unexpected_rows",
                    "count": len(unexpected_revision_ids),
                }
            )
        inconsistent_ids = revision_matrix["inconsistent_revision_ids"]
        if inconsistent_ids:
            blockers.append(
                {
                    "code": "revision_matrix_inconsistent_rows",
                    "count": len(inconsistent_ids),
                }
            )
        joint_contract_errors = revision_matrix[
            "joint_decision_contract_validation_errors"
        ]
        if joint_contract_errors:
            affected_decision_ids = {
                error["decision_id"] for error in joint_contract_errors
            }
            blockers.append(
                {
                    "code": "joint_decision_contract_invalid",
                    "count": len(affected_decision_ids),
                }
            )
        response_basis_errors = revision_matrix[
            "response_basis_validation_errors"
        ]
        if response_basis_errors:
            affected_revision_ids = {
                error["revision_id"] for error in response_basis_errors
            }
            blockers.append(
                {
                    "code": "revision_response_basis_unverified",
                    "count": len(affected_revision_ids),
                }
            )
        if not revision_matrix["row_count"]:
            blockers.append({"code": "revision_matrix_empty", "count": 1})
        elif revision_matrix["not_applied_verified_count"]:
            blockers.append(
                {
                    "code": "revision_rows_not_applied_verified",
                    "count": revision_matrix["not_applied_verified_count"],
                }
            )
    return {
        "ready_for_final_freeze": not blockers,
        "blocker_count": len(blockers),
        "blockers": blockers,
    }


def build_closeout_prefreeze_manifest(
    repo_root: Path,
    *,
    generated_at: datetime | None = None,
    audit_csv: Path = DEFAULT_AUDIT_CSV,
    longitudinal_csv: Path = DEFAULT_LONGITUDINAL_CSV,
    revision_matrix_csv: Path = DEFAULT_REVISION_MATRIX_CSV,
    joint_decision_csv: Path = DEFAULT_JOINT_DECISION_CSV,
    required_revision_ids: Sequence[str] = DEFAULT_REQUIRED_REVISION_IDS,
    reference_columns: Sequence[str] = DEFAULT_REFERENCE_COLUMNS,
    decision_sheets: Sequence[DecisionSheetSpec] = DEFAULT_DECISION_SHEETS,
    deliverable_paths: Sequence[Path] = DEFAULT_DELIVERABLE_PATHS,
) -> dict[str, Any]:
    """Build the current closeout inventory without claiming a final freeze."""
    root = repo_root.resolve()
    timestamp = generated_at or datetime.now(UTC)
    if timestamp.tzinfo is None:
        raise ValueError("generated_at must include a timezone")

    audit_record = _table_record(root, audit_csv)
    longitudinal_record = _table_record(root, longitudinal_csv)
    audit_rows: list[dict[str, str]] = []
    audit_fields: list[str] = []
    if audit_record["status"] == "present":
        audit_fields, audit_rows = _read_csv(_resolve_input(root, audit_csv))

    reference_audit = {
        column: _reference_record(root, audit_rows, audit_fields, column)
        for column in reference_columns
    }
    decision_gates = {
        spec.name: _decision_gate_record(root, spec) for spec in decision_sheets
    }
    revision_matrix = _revision_matrix_record(
        root,
        revision_matrix_csv,
        generated_at=timestamp,
        joint_decision_csv=joint_decision_csv,
        required_revision_ids=required_revision_ids,
    )
    deliverables = [_file_record(root, path) for path in deliverable_paths]

    present_deliverables = sum(
        record["status"] == "present" for record in deliverables
    )
    open_decision_rows = sum(
        record["open_row_count"] or 0 for record in decision_gates.values()
    )
    missing_deliverables = len(deliverables) - present_deliverables
    freeze_readiness = _freeze_readiness(
        missing_deliverable_count=missing_deliverables,
        revision_matrix=revision_matrix,
    )
    return {
        "schema_version": 2,
        "manifest_status": "pre_freeze",
        "finalized": False,
        "generated_at": timestamp.astimezone(UTC).isoformat(),
        "repository_path": ".",
        "evidence_tables": {
            "audit_report_summary": audit_record,
            "longitudinal_summary": longitudinal_record,
        },
        "reference_audit": reference_audit,
        "decision_gates": decision_gates,
        "revision_execution_gate": revision_matrix,
        "key_deliverables": deliverables,
        "freeze_readiness": freeze_readiness,
        "summary": {
            "key_deliverable_count": len(deliverables),
            "present_key_deliverable_count": present_deliverables,
            "missing_key_deliverable_count": missing_deliverables,
            "decision_gate_count": len(decision_gates),
            "open_decision_row_count_across_sheets": open_decision_rows,
            "revision_matrix_row_count": revision_matrix["row_count"],
            "revision_rows_applied_verified_count": (
                revision_matrix["status_counts"].get("applied_verified", 0)
            ),
            "revision_rows_not_applied_verified_count": revision_matrix[
                "not_applied_verified_count"
            ],
            "revision_response_basis_claim_count": revision_matrix[
                "response_basis_claim_count"
            ],
            "revision_response_basis_error_count": len(
                revision_matrix["response_basis_validation_errors"]
            ),
            "joint_decision_contract_error_count": len(
                revision_matrix[
                    "joint_decision_contract_validation_errors"
                ]
            ),
            "revision_missing_required_row_count": len(
                revision_matrix["missing_required_revision_ids"]
            ),
            "revision_unexpected_row_count": len(
                revision_matrix["unexpected_revision_ids"]
            ),
            "final_freeze_blocker_count": freeze_readiness["blocker_count"],
            "ready_for_final_freeze": freeze_readiness[
                "ready_for_final_freeze"
            ],
        },
        "limitations": [
            "This is a pre-freeze inventory, not a final or frozen manifest.",
            "A missing reference records checkout availability only; it does not prove the artifact never existed.",
            "Recommendations and fallback labels are not counted as confirmed human decisions.",
            "Open decision-sheet rows are reported separately from revision execution because the documented no-response branch preserves blank confirmations.",
            "File hashes establish byte identity, not research validity or legal compliance.",
        ],
    }


def render_closeout_prefreeze_markdown(
    manifest: dict[str, Any],
    *,
    json_path: str,
) -> str:
    """Render a compact human-readable view of a pre-freeze manifest."""
    lines = [
        "# SSRP Closeout Pre-Freeze Manifest",
        "",
        "**Status: `pre_freeze` - this is not a final or frozen manifest.**",
        "",
        f"Generated at: `{manifest['generated_at']}`",
        "",
        f"Machine-readable source: [`{json_path}`]({json_path})",
        "",
        "Regenerate from the repository root with "
        "`uv run consent-audit closeout-prefreeze-manifest`.",
        "",
        "## Evidence Tables",
        "",
        "| Table | Status | Rows | Bytes | SHA-256 |",
        "|---|---:|---:|---:|---|",
    ]
    for record in manifest["evidence_tables"].values():
        lines.append(
            "| `{path}` | {status} | {rows} | {size} | `{digest}` |".format(
                path=record["path"],
                status=record["status"],
                rows=record.get("row_count")
                if record.get("row_count") is not None
                else "n/a",
                size=record.get("bytes", "n/a"),
                digest=record.get("sha256", "n/a"),
            )
        )

    lines.extend(
        [
            "",
            "## Evidence References",
            "",
            "| CSV column | Present | Nonblank | Blank | Present refs | Missing refs | External | Outside repo |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for column, record in manifest["reference_audit"].items():
        counts = record.get("status_counts_by_row") or {}
        lines.append(
            "| `{column}` | {present} | {nonblank} | {blank} | {local} | {missing} | {external} | {outside} |".format(
                column=column,
                present=str(record["column_present"]).lower(),
                nonblank=record["nonblank_rows"]
                if record["nonblank_rows"] is not None
                else "n/a",
                blank=record["blank_rows"]
                if record["blank_rows"] is not None
                else "n/a",
                local=counts.get("present", 0),
                missing=counts.get("missing", 0),
                external=counts.get("external", 0),
                outside=counts.get("outside_repo", 0),
            )
        )

    lines.extend(
        [
            "",
            "## Decision Gates",
            "",
            "| Gate | Rows | Pending | Blank confirmations | Open rows | Status |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for name, record in manifest["decision_gates"].items():
        lines.append(
            "| `{name}` | {rows} | {pending} | {blank} | {open_rows} | {status} |".format(
                name=name,
                rows=record.get("row_count", "n/a"),
                pending=record.get("pending_count")
                if record.get("pending_count") is not None
                else "n/a",
                blank=record.get("blank_confirmation_count")
                if record.get("blank_confirmation_count") is not None
                else "n/a",
                open_rows=record.get("open_row_count", "n/a"),
                status=record["status"],
            )
        )

    revision = manifest["revision_execution_gate"]
    status_counts = revision.get("status_counts") or {}
    lines.extend(
        [
            "",
            "## Revision Execution Gate",
            "",
            "| Matrix | Rows | Waiting | Ready to apply | Applied + verified | Basis claims | Basis errors | Coverage errors | Inconsistent | Status |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
            "| `{path}` | {rows} | {waiting} | {ready} | {applied} | {claims} | {basis_errors} | {coverage_errors} | {inconsistent} | {status} |".format(
                path=revision["path"],
                rows=revision.get("row_count")
                if revision.get("row_count") is not None
                else "n/a",
                waiting=status_counts.get("waiting_for_response_branch", 0),
                ready=status_counts.get("ready_to_apply", 0),
                applied=status_counts.get("applied_verified", 0),
                claims=revision.get("response_basis_claim_count") or 0,
                basis_errors=len(
                    revision.get("response_basis_validation_errors") or []
                ),
                coverage_errors=len(
                    revision.get("missing_required_revision_ids") or []
                )
                + len(revision.get("unexpected_revision_ids") or []),
                inconsistent=len(revision.get("inconsistent_revision_ids") or []),
                status=revision["status"],
            ),
            "",
            "Joint decision contract errors: "
            f"{len(revision.get('joint_decision_contract_validation_errors') or [])}.",
            "",
            "**Ready for final freeze: "
            f"`{str(manifest['freeze_readiness']['ready_for_final_freeze']).lower()}`.**",
            "",
            "| Readiness blocker | Count |",
            "|---|---:|",
        ]
    )
    blockers = manifest["freeze_readiness"]["blockers"]
    if blockers:
        lines.extend(
            f"| `{blocker['code']}` | {blocker['count']} |"
            for blocker in blockers
        )
    else:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Key Deliverables",
            "",
            "| Path | Status | Bytes | SHA-256 |",
            "|---|---:|---:|---|",
        ]
    )
    for record in manifest["key_deliverables"]:
        lines.append(
            "| `{path}` | {status} | {size} | `{digest}` |".format(
                path=record["path"],
                status=record["status"],
                size=record.get("bytes", "n/a"),
                digest=record.get("sha256", "n/a"),
            )
        )

    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in manifest["limitations"])
    lines.append("")
    return "\n".join(lines)


def export_closeout_prefreeze_manifest(
    repo_root: Path,
    out_json: Path,
    out_markdown: Path,
    *,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Write the JSON manifest and its human-readable Markdown view."""
    root = repo_root.resolve()
    manifest = build_closeout_prefreeze_manifest(root, generated_at=generated_at)
    json_output = _resolve_input(root, out_json)
    markdown_output = _resolve_input(root, out_markdown)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    json_link = Path(os.path.relpath(json_output, markdown_output.parent)).as_posix()
    markdown_output.write_text(
        render_closeout_prefreeze_markdown(manifest, json_path=json_link),
        encoding="utf-8",
    )
    return manifest
