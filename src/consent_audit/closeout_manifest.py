"""Build a fact-only pre-freeze manifest for SSRP closeout artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
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
DEFAULT_REFERENCE_COLUMNS = (
    "first_screenshot_ref",
    "first_dom_snapshot_ref",
    "report_pdf_ref",
)
DEFAULT_DECISION_SHEETS = (
    DecisionSheetSpec(
        "joint_advisor_review",
        Path("data/joint_advisor_review_decision_sheet_2026-07-25.csv"),
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
    Path("data/joint_advisor_review_decision_sheet_2026-07-25.csv"),
    Path(
        "docs/research/"
        "july26_advisor_response_and_fallback_protocol_2026-07-26.md"
    ),
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


def build_closeout_prefreeze_manifest(
    repo_root: Path,
    *,
    generated_at: datetime | None = None,
    audit_csv: Path = DEFAULT_AUDIT_CSV,
    longitudinal_csv: Path = DEFAULT_LONGITUDINAL_CSV,
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
    deliverables = [_file_record(root, path) for path in deliverable_paths]

    present_deliverables = sum(
        record["status"] == "present" for record in deliverables
    )
    open_decision_rows = sum(
        record["open_row_count"] or 0 for record in decision_gates.values()
    )
    return {
        "schema_version": 1,
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
        "key_deliverables": deliverables,
        "summary": {
            "key_deliverable_count": len(deliverables),
            "present_key_deliverable_count": present_deliverables,
            "missing_key_deliverable_count": len(deliverables)
            - present_deliverables,
            "decision_gate_count": len(decision_gates),
            "open_decision_row_count_across_sheets": open_decision_rows,
        },
        "limitations": [
            "This is a pre-freeze inventory, not a final or frozen manifest.",
            "A missing reference records checkout availability only; it does not prove the artifact never existed.",
            "Recommendations and fallback labels are not counted as confirmed human decisions.",
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
