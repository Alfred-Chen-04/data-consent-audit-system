"""Prepare the evidence-backed closeout revision branch without applying edits."""

from __future__ import annotations

import csv
import os
import tempfile
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from consent_audit.closeout_manifest import (
    ALLOWED_RESPONSE_BASES,
    ALLOWED_REVISION_STATUSES,
    DEFAULT_JOINT_DECISION_CSV,
    DEFAULT_REQUIRED_REVISION_IDS,
    DEFAULT_REVISION_MATRIX_CSV,
    JOINT_DECISION_REQUIRED_COLUMNS,
    PROJECT_FALLBACK_CUTOFF,
    PROJECT_FALLBACK_VALUES,
    REVISION_MATRIX_REQUIRED_COLUMNS,
    validate_joint_decision_contract,
    validate_project_decision_contract,
)


@dataclass(frozen=True)
class BranchSelection:
    """One validated response branch selected for a joint decision."""

    selected_value: str
    response_basis: str


@dataclass(frozen=True)
class CloseoutBranchResult:
    """Dry-run or write result for revision-matrix branch preparation."""

    as_of: datetime
    revision_matrix_csv: Path
    write_requested: bool
    write_performed: bool
    actual_decision_count: int
    fallback_decision_count: int
    project_owner_decision_count: int
    waiting_decision_ids: tuple[str, ...]
    rows_prepared_count: int
    rows_already_ready_count: int
    rows_applied_verified_count: int
    rows_waiting_count: int
    total_row_count: int


def parse_as_of(value: str | None) -> datetime:
    """Parse an optional timezone-aware CLI timestamp."""
    if value is None:
        return datetime.now(UTC)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("--as-of must be a valid ISO 8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("--as-of must include a timezone")
    return parsed


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise ValueError(f"CSV is missing: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _value(row: dict[str, str], column: str) -> str:
    return (row.get(column) or "").strip()


def _has_timezone(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _format_contract_errors(errors: Sequence[dict[str, str]]) -> str:
    details = ", ".join(
        f"{error['decision_id']}:{error['code']}" for error in errors
    )
    return f"Joint decision sheet contract is invalid: {details}"


def _format_project_contract_errors(errors: Sequence[dict[str, str]]) -> str:
    details = ", ".join(
        f"{error['decision_id']}:{error['code']}" for error in errors
    )
    return f"Project decision sheet contract is invalid: {details}"


def _matrix_errors(
    fields: Sequence[str],
    rows: Sequence[dict[str, str]],
    required_revision_ids: Sequence[str],
) -> list[str]:
    errors: list[str] = []
    missing_columns = sorted(set(REVISION_MATRIX_REQUIRED_COLUMNS) - set(fields))
    if missing_columns:
        errors.append(f"missing columns: {', '.join(missing_columns)}")
        return errors

    revision_ids = [_value(row, "revision_id") for row in rows]
    counts = Counter(revision_id for revision_id in revision_ids if revision_id)
    if any(not revision_id for revision_id in revision_ids):
        errors.append("one or more revision_id values are blank")
    duplicates = sorted(
        revision_id for revision_id, count in counts.items() if count > 1
    )
    if duplicates:
        errors.append(f"duplicate revision IDs: {', '.join(duplicates)}")
    actual_ids = set(counts)
    required_ids = set(required_revision_ids)
    missing_ids = sorted(required_ids - actual_ids)
    unexpected_ids = sorted(actual_ids - required_ids)
    if missing_ids:
        errors.append(f"missing revision IDs: {', '.join(missing_ids)}")
    if unexpected_ids:
        errors.append(f"unexpected revision IDs: {', '.join(unexpected_ids)}")

    for index, row in enumerate(rows, start=1):
        revision_id = _value(row, "revision_id") or f"<row_{index}>"
        decision_id = _value(row, "decision_id")
        artifact = _value(row, "artifact")
        status = _value(row, "execution_status")
        selected_value = _value(row, "selected_value")
        response_basis = _value(row, "response_basis")
        applied_by = _value(row, "applied_by")
        applied_at = _value(row, "applied_at")
        if not decision_id or not artifact:
            errors.append(f"{revision_id}: decision_id and artifact are required")
        if status not in ALLOWED_REVISION_STATUSES:
            errors.append(f"{revision_id}: invalid execution_status {status!r}")
        if response_basis and response_basis not in ALLOWED_RESPONSE_BASES:
            errors.append(f"{revision_id}: invalid response_basis {response_basis!r}")
        if status == "waiting_for_response_branch" and any(
            (selected_value, response_basis, applied_by, applied_at)
        ):
            errors.append(f"{revision_id}: waiting row contains execution fields")
        if status == "ready_to_apply" and (
            not selected_value
            or not response_basis
            or bool(applied_by or applied_at)
        ):
            errors.append(f"{revision_id}: ready row has inconsistent execution fields")
        if status == "applied_verified" and not all(
            (selected_value, response_basis, applied_by, applied_at)
        ):
            errors.append(f"{revision_id}: applied row is missing execution provenance")
        elif status == "applied_verified" and not _has_timezone(applied_at):
            errors.append(
                f"{revision_id}: applied_at must be a timezone-aware ISO 8601 timestamp"
            )
    return errors


def _select_decision_branches(
    rows: Sequence[dict[str, str]],
    required_decision_ids: set[str],
    as_of: datetime,
    project_rows: Sequence[dict[str, str]],
) -> tuple[dict[str, BranchSelection], tuple[str, ...]]:
    rows_by_id = {_value(row, "decision_id"): row for row in rows}
    project_rows_by_id = {
        _value(row, "decision_id"): row for row in project_rows
    }
    selections: dict[str, BranchSelection] = {}
    waiting: list[str] = []
    for decision_id in sorted(required_decision_ids):
        row = rows_by_id[decision_id]
        if _value(row, "review_status").casefold() == "confirmed":
            selections[decision_id] = BranchSelection(
                selected_value=_value(row, "confirmed_decision"),
                response_basis="actual_advisor_response",
            )
        elif decision_id in project_rows_by_id:
            selections[decision_id] = BranchSelection(
                selected_value=_value(
                    project_rows_by_id[decision_id], "selected_value"
                ),
                response_basis="project_owner_decision",
            )
        elif as_of >= PROJECT_FALLBACK_CUTOFF:
            fallback = PROJECT_FALLBACK_VALUES.get(decision_id)
            if fallback is None:
                raise ValueError(
                    f"No project fallback is defined for decision {decision_id}"
                )
            selections[decision_id] = BranchSelection(
                selected_value=fallback,
                response_basis="project_fallback_after_internal_cutoff",
            )
        else:
            waiting.append(decision_id)
    return selections, tuple(waiting)


def _write_csv_atomic(
    path: Path,
    fields: Sequence[str],
    rows: Sequence[dict[str, str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def prepare_closeout_revision_branch(
    *,
    joint_decision_csv: Path = DEFAULT_JOINT_DECISION_CSV,
    project_decision_csv: Path | None = None,
    revision_matrix_csv: Path = DEFAULT_REVISION_MATRIX_CSV,
    as_of: datetime | None = None,
    write: bool = False,
    required_revision_ids: Sequence[str] = DEFAULT_REQUIRED_REVISION_IDS,
) -> CloseoutBranchResult:
    """Prepare only response-backed or post-cutoff revision rows."""
    timestamp = as_of or datetime.now(UTC)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("as_of must include a timezone")

    matrix_fields, matrix_rows = _read_csv(revision_matrix_csv)
    errors = _matrix_errors(matrix_fields, matrix_rows, required_revision_ids)
    if errors:
        raise ValueError(f"Revision matrix is invalid: {'; '.join(errors)}")

    required_decision_ids = {
        _value(row, "decision_id") for row in matrix_rows if _value(row, "decision_id")
    }
    joint_fields, joint_rows = _read_csv(joint_decision_csv)
    contract_errors = validate_joint_decision_contract(
        source_present=True,
        fields=joint_fields,
        rows=joint_rows,
        required_decision_ids=required_decision_ids,
    )
    if contract_errors:
        raise ValueError(_format_contract_errors(contract_errors))
    if not set(JOINT_DECISION_REQUIRED_COLUMNS).issubset(joint_fields):
        raise ValueError("Joint decision sheet schema is invalid")

    project_fields: list[str] = []
    project_rows: list[dict[str, str]] = []
    if project_decision_csv is not None and project_decision_csv.is_file():
        project_fields, project_rows = _read_csv(project_decision_csv)
        project_errors = validate_project_decision_contract(
            source_present=True,
            fields=project_fields,
            rows=project_rows,
            required_decision_ids=required_decision_ids,
            joint_rows=joint_rows,
        )
        if project_errors:
            raise ValueError(_format_project_contract_errors(project_errors))

    selections, waiting_decision_ids = _select_decision_branches(
        joint_rows,
        required_decision_ids,
        timestamp,
        project_rows,
    )
    rows_prepared = 0
    rows_already_ready = 0
    rows_applied = 0
    rows_waiting = 0
    updated_rows: list[dict[str, str]] = []
    conflicts: list[str] = []

    for row in matrix_rows:
        updated = dict(row)
        revision_id = _value(row, "revision_id")
        decision_id = _value(row, "decision_id")
        status = _value(row, "execution_status")
        selection = selections.get(decision_id)
        if selection is None:
            if status != "waiting_for_response_branch":
                conflicts.append(
                    f"{revision_id}: decision is waiting but row status is {status}"
                )
            rows_waiting += 1
            updated_rows.append(updated)
            continue

        selected_value = _value(row, "selected_value")
        response_basis = _value(row, "response_basis")
        if status == "waiting_for_response_branch":
            updated["execution_status"] = "ready_to_apply"
            updated["selected_value"] = selection.selected_value
            updated["response_basis"] = selection.response_basis
            rows_prepared += 1
        elif (
            selected_value != selection.selected_value
            or response_basis != selection.response_basis
        ):
            conflicts.append(
                f"{revision_id}: existing selected branch conflicts with decision source"
            )
        elif status == "ready_to_apply":
            rows_already_ready += 1
        elif status == "applied_verified":
            rows_applied += 1
        updated_rows.append(updated)

    if conflicts:
        raise ValueError(f"Revision matrix branch conflict: {'; '.join(conflicts)}")

    write_performed = write and rows_prepared > 0
    if write_performed:
        _write_csv_atomic(revision_matrix_csv, matrix_fields, updated_rows)

    return CloseoutBranchResult(
        as_of=timestamp,
        revision_matrix_csv=revision_matrix_csv,
        write_requested=write,
        write_performed=write_performed,
        actual_decision_count=sum(
            selection.response_basis == "actual_advisor_response"
            for selection in selections.values()
        ),
        fallback_decision_count=sum(
            selection.response_basis
            == "project_fallback_after_internal_cutoff"
            for selection in selections.values()
        ),
        project_owner_decision_count=sum(
            selection.response_basis == "project_owner_decision"
            for selection in selections.values()
        ),
        waiting_decision_ids=waiting_decision_ids,
        rows_prepared_count=rows_prepared,
        rows_already_ready_count=rows_already_ready,
        rows_applied_verified_count=rows_applied,
        rows_waiting_count=rows_waiting,
        total_row_count=len(matrix_rows),
    )


def render_closeout_branch_result(result: CloseoutBranchResult) -> str:
    """Render a compact, low-token branch-preparation report."""
    mode = "write" if result.write_requested else "dry_run"
    lines = [
        "Closeout revision branch preparation",
        f"- as_of={result.as_of.isoformat()}",
        f"- mode={mode}; write_performed={str(result.write_performed).lower()}",
        (
            "- decisions: "
            f"actual={result.actual_decision_count}; "
            f"project_owner={result.project_owner_decision_count}; "
            f"fallback={result.fallback_decision_count}; "
            f"waiting={len(result.waiting_decision_ids)}"
        ),
        (
            "- revision rows: "
            f"prepared={result.rows_prepared_count}; "
            f"already_ready={result.rows_already_ready_count}; "
            f"applied_verified={result.rows_applied_verified_count}; "
            f"waiting={result.rows_waiting_count}; "
            f"total={result.total_row_count}"
        ),
    ]
    if result.waiting_decision_ids:
        lines.append(f"- waiting_decision_ids={','.join(result.waiting_decision_ids)}")
    if result.rows_prepared_count and not result.write_requested:
        lines.append("- next=review this dry run, then rerun with --write")
    elif result.write_performed:
        lines.append("- next=apply only mapped artifact changes, verify, then record provenance")
    elif result.waiting_decision_ids:
        lines.append("- next=record actual responses or wait for the internal cutoff")
    else:
        lines.append("- next=no matrix preparation change is needed")
    return "\n".join(lines)
