"""Gate and generate the final closeout index from verified evidence."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import tempfile
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

DEFAULT_CLOSEOUT_MANIFEST_JSON = Path(
    "data/closeout/closeout_prefreeze_manifest_2026-07-26.json"
)
DEFAULT_FINAL_QA_CSV = Path("data/closeout/final_qa_checklist_2026-07-27.csv")
DEFAULT_FINAL_INDEX_MARKDOWN = Path("docs/research/final_closeout_index.md")
FINAL_QA_REQUIRED_COLUMNS = (
    "check_id",
    "check_scope",
    "required_verification",
    "status",
    "evidence",
    "verified_by",
    "verified_at",
    "notes",
)
DEFAULT_REQUIRED_QA_IDS = (
    "presentation_final_qa",
    "poster_final_qa",
    "evidence_package_final_qa",
    "repository_final_verification",
    "backup_open_check",
)
DEFAULT_FINAL_ARTIFACTS = (
    (
        "Presentation PPTX",
        Path(
            "docs/research/presentation/"
            "ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04.pptx"
        ),
    ),
    (
        "Presentation montage",
        Path(
            "docs/research/presentation/"
            "ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04_montage.png"
        ),
    ),
    (
        "Poster PPTX",
        Path("docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.pptx"),
    ),
    (
        "Poster PDF",
        Path("docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.pdf"),
    ),
    (
        "Poster PNG",
        Path("docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.png"),
    ),
    (
        "Audit summary",
        Path("data/research_package/audit_report_summary.csv"),
    ),
    (
        "Longitudinal summary",
        Path("data/research_package/longitudinal_summary.csv"),
    ),
    (
        "Local directional review",
        Path("data/longitudinal_directional_review_2026-07-29.csv"),
    ),
    (
        "Retrospective cases",
        Path("data/retrospective_longitudinal_cases_2026-07-29.csv"),
    ),
    (
        "Retrospective source registry",
        Path("data/retrospective_source_registry_2026-07-29.csv"),
    ),
    (
        "Evidence-rescue analysis",
        Path(
            "docs/research/"
            "july29_retrospective_longitudinal_evidence_rescue_2026-07-29.md"
        ),
    ),
    (
        "Research manifest",
        Path("data/research_package/research_manifest.json"),
    ),
    (
        "Longitudinal artifact manifest",
        Path("data/longitudinal_artifact_manifest_2026-07-30.json"),
    ),
    (
        "Closeout reconciliation",
        Path("docs/research/aug03_closeout_reconciliation_2026-08-03.md"),
    ),
    (
        "Final paper working draft",
        Path("docs/research/ssrp_final_paper_working_draft_2026-08-03.md"),
    ),
    (
        "Presentation readiness guide",
        Path(
            "docs/research/presentation/"
            "ssrp_consent_presentation_readiness_2026-08-04.md"
        ),
    ),
    (
        "Project-owner decisions",
        Path("data/closeout/project_owner_decision_sheet_2026-07-29.csv"),
    ),
    (
        "Project-owner decision note",
        Path("docs/research/july29_project_owner_closeout_decisions_2026-07-29.md"),
    ),
)


@dataclass(frozen=True)
class FinalArtifactRecord:
    """One hashed artifact linked by the final index."""

    role: str
    path: str
    bytes: int
    sha256: str


@dataclass(frozen=True)
class FinalQaRecord:
    """One verified final-QA attestation."""

    check_id: str
    check_scope: str
    evidence: str
    verified_by: str
    verified_at: str


@dataclass(frozen=True)
class FinalIndexResult:
    """Dry-run or write result for a fully gated final closeout index."""

    generated_at: datetime
    out_markdown: Path
    write_requested: bool
    write_performed: bool
    revision_row_count: int
    actual_response_basis_count: int
    fallback_response_basis_count: int
    project_owner_basis_count: int
    required_qa_count: int
    artifacts: tuple[FinalArtifactRecord, ...]
    qa_records: tuple[FinalQaRecord, ...]
    markdown: str


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"Closeout manifest is missing: {path}")
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Closeout manifest root must be an object")
    return cast(dict[str, Any], raw)


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"Closeout manifest {label} must be an object")
    return cast(dict[str, Any], value)


def _validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest.get("schema_version") != 2:
        raise ValueError("Closeout manifest must use schema_version=2")
    freeze = _mapping(manifest.get("freeze_readiness"), "freeze_readiness")
    blockers = freeze.get("blockers")
    if freeze.get("ready_for_final_freeze") is not True or blockers != []:
        raise ValueError(
            "Final index blocked: closeout manifest is not ready for final freeze"
        )

    revision = _mapping(
        manifest.get("revision_execution_gate"),
        "revision_execution_gate",
    )
    row_count = revision.get("row_count")
    status_counts = _mapping(revision.get("status_counts"), "status_counts")
    required_truths = (
        ("coverage_valid", revision.get("coverage_valid")),
        ("row_states_valid", revision.get("row_states_valid")),
        ("response_basis_claims_valid", revision.get("response_basis_claims_valid")),
        ("joint_decision_contract_valid", revision.get("joint_decision_contract_valid")),
    )
    failed_truths = [name for name, value in required_truths if value is not True]
    if failed_truths:
        raise ValueError(
            f"Final index blocked: invalid revision gates: {', '.join(failed_truths)}"
        )
    if not isinstance(row_count, int) or row_count <= 0:
        raise ValueError("Final index blocked: revision matrix row_count is invalid")
    if status_counts != {"applied_verified": row_count}:
        raise ValueError("Final index blocked: not every revision row is applied_verified")
    if revision.get("not_applied_verified_count") != 0:
        raise ValueError("Final index blocked: unapplied revision rows remain")
    if revision.get("response_basis_claim_count") != row_count:
        raise ValueError("Final index blocked: not every revision row has a response basis")
    actual_count = revision.get("actual_response_basis_count")
    fallback_count = revision.get("project_fallback_basis_count")
    project_owner_count = revision.get("project_owner_basis_count")
    if (
        not isinstance(actual_count, int)
        or isinstance(actual_count, bool)
        or not isinstance(fallback_count, int)
        or isinstance(fallback_count, bool)
        or not isinstance(project_owner_count, int)
        or isinstance(project_owner_count, bool)
        or actual_count + fallback_count + project_owner_count != row_count
    ):
        raise ValueError("Final index blocked: response-basis counts do not cover all rows")
    if revision.get("response_basis_validation_errors") != []:
        raise ValueError("Final index blocked: response-basis validation errors remain")
    if revision.get("joint_decision_contract_validation_errors") != []:
        raise ValueError("Final index blocked: joint-decision contract errors remain")
    return revision


def _has_timezone(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _read_verified_qa(
    path: Path,
    required_qa_ids: Sequence[str],
) -> tuple[FinalQaRecord, ...]:
    if not path.is_file():
        raise ValueError(f"Final QA checklist is missing: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    missing_columns = sorted(set(FINAL_QA_REQUIRED_COLUMNS) - set(fields))
    if missing_columns:
        raise ValueError(
            f"Final QA checklist is missing columns: {', '.join(missing_columns)}"
        )

    def value(row: dict[str, str], column: str) -> str:
        return (row.get(column) or "").strip()

    ids = [value(row, "check_id") for row in rows]
    counts = Counter(check_id for check_id in ids if check_id)
    duplicate_ids = sorted(
        check_id for check_id, count in counts.items() if count > 1
    )
    expected = set(required_qa_ids)
    actual = set(counts)
    errors: list[str] = []
    if any(not check_id for check_id in ids):
        errors.append("blank check_id")
    if duplicate_ids:
        errors.append(f"duplicate check IDs: {', '.join(duplicate_ids)}")
    missing_ids = sorted(expected - actual)
    unexpected_ids = sorted(actual - expected)
    if missing_ids:
        errors.append(f"missing check IDs: {', '.join(missing_ids)}")
    if unexpected_ids:
        errors.append(f"unexpected check IDs: {', '.join(unexpected_ids)}")

    records: list[FinalQaRecord] = []
    for index, row in enumerate(rows, start=1):
        check_id = value(row, "check_id") or f"<row_{index}>"
        scope = value(row, "check_scope")
        required_verification = value(row, "required_verification")
        status = value(row, "status")
        evidence = value(row, "evidence")
        verified_by = value(row, "verified_by")
        verified_at = value(row, "verified_at")
        if not scope or not required_verification:
            errors.append(f"{check_id}: scope and required_verification are required")
        if status != "verified":
            errors.append(f"{check_id}: status is not verified")
            continue
        if not all((evidence, verified_by, verified_at)):
            errors.append(f"{check_id}: verified provenance is incomplete")
            continue
        if not _has_timezone(verified_at):
            errors.append(f"{check_id}: verified_at must include a timezone")
            continue
        records.append(
            FinalQaRecord(
                check_id=check_id,
                check_scope=scope,
                evidence=evidence,
                verified_by=verified_by,
                verified_at=verified_at,
            )
        )
    if errors:
        raise ValueError(f"Final QA checklist is not ready: {'; '.join(errors)}")
    return tuple(records)


def _resolve_within(repo_root: Path, path: Path) -> Path:
    resolved = path.resolve() if path.is_absolute() else (repo_root / path).resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"Path must stay inside the repository: {path}") from exc
    return resolved


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _artifact_records(
    repo_root: Path,
    artifacts: Sequence[tuple[str, Path]],
) -> tuple[FinalArtifactRecord, ...]:
    records: list[FinalArtifactRecord] = []
    seen: set[str] = set()
    for role, path in artifacts:
        resolved = _resolve_within(repo_root, path)
        relative = resolved.relative_to(repo_root).as_posix()
        if relative in seen:
            raise ValueError(f"Duplicate final artifact path: {relative}")
        seen.add(relative)
        if not resolved.is_file():
            raise ValueError(f"Final artifact is missing: {relative}")
        records.append(
            FinalArtifactRecord(
                role=role,
                path=relative,
                bytes=resolved.stat().st_size,
                sha256=_sha256(resolved),
            )
        )
    return tuple(records)


def _cell(value: str) -> str:
    return " ".join(value.replace("|", "\\|").split())


def _render_markdown(
    *,
    generated_at: datetime,
    manifest_path: str,
    qa_path: str,
    revision: dict[str, Any],
    artifacts: Sequence[FinalArtifactRecord],
    qa_records: Sequence[FinalQaRecord],
    out_parent: Path,
    repo_root: Path,
) -> str:
    manifest_link = Path(
        os.path.relpath(repo_root / manifest_path, out_parent)
    ).as_posix()
    qa_link = Path(os.path.relpath(repo_root / qa_path, out_parent)).as_posix()
    lines = [
        "# SSRP Final Closeout Index",
        "",
        "**Status: `final_closeout_index`. This file was generated only after the",
        "schema-v2 freeze gate and all required final-QA attestations passed.**",
        "",
        f"Generated at: `{generated_at.astimezone(UTC).isoformat()}`",
        "",
        "## Gate Snapshot",
        "",
        f"- Closeout manifest: [`{manifest_path}`]({manifest_link})",
        f"- Final QA checklist: [`{qa_path}`]({qa_link})",
        f"- Revision rows applied and verified: {revision['row_count']}/{revision['row_count']}",
        f"- Actual-response rows: {revision.get('actual_response_basis_count', 0)}",
        f"- Project-owner decision rows: {revision.get('project_owner_basis_count', 0)}",
        f"- Project-fallback rows: {revision.get('project_fallback_basis_count', 0)}",
        f"- Final QA checks verified: {len(qa_records)}/{len(qa_records)}",
        "",
        "## Final Artifacts",
        "",
        "| Role | File | Bytes | SHA-256 |",
        "|---|---|---:|---|",
    ]
    for artifact_record in artifacts:
        link = Path(
            os.path.relpath(repo_root / artifact_record.path, out_parent)
        ).as_posix()
        lines.append(
            f"| {_cell(artifact_record.role)} | "
            f"[`{artifact_record.path}`]({link}) | "
            f"{artifact_record.bytes} | `{artifact_record.sha256}` |"
        )
    lines.extend(
        [
            "",
            "## Final QA Evidence",
            "",
            "| Check | Scope | Evidence | Verified by | Verified at |",
            "|---|---|---|---|---|",
        ]
    )
    for qa_record in qa_records:
        lines.append(
            f"| `{qa_record.check_id}` | {_cell(qa_record.check_scope)} | "
            f"{_cell(qa_record.evidence)} | {_cell(qa_record.verified_by)} | "
            f"`{qa_record.verified_at}` |"
        )
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "- Response-basis counts distinguish recorded responses from project fallbacks; neither is silently relabeled.",
            "- File hashes establish byte identity, not legal compliance or broad research validity.",
            "- The deliverable remains a bounded five-site pilot plus six-case observational series; neither is a population estimate or experiment.",
            "",
        ]
    )
    return "\n".join(lines)


def _write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(text)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def prepare_final_closeout_index(
    *,
    repo_root: Path,
    manifest_json: Path = DEFAULT_CLOSEOUT_MANIFEST_JSON,
    final_qa_csv: Path = DEFAULT_FINAL_QA_CSV,
    out_markdown: Path = DEFAULT_FINAL_INDEX_MARKDOWN,
    generated_at: datetime | None = None,
    write: bool = False,
    required_qa_ids: Sequence[str] = DEFAULT_REQUIRED_QA_IDS,
    final_artifacts: Sequence[tuple[str, Path]] = DEFAULT_FINAL_ARTIFACTS,
) -> FinalIndexResult:
    """Validate all final gates and optionally write one final artifact index."""
    root = repo_root.resolve()
    timestamp = generated_at or datetime.now(UTC)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("generated_at must include a timezone")
    manifest_path = _resolve_within(root, manifest_json)
    qa_path = _resolve_within(root, final_qa_csv)
    output_path = _resolve_within(root, out_markdown)
    manifest = _read_json(manifest_path)
    revision = _validate_manifest(manifest)
    qa_records = _read_verified_qa(qa_path, required_qa_ids)
    artifact_inputs = [*final_artifacts, ("Closeout manifest", manifest_path)]
    artifacts = _artifact_records(root, artifact_inputs)
    manifest_relative = manifest_path.relative_to(root).as_posix()
    qa_relative = qa_path.relative_to(root).as_posix()
    markdown = _render_markdown(
        generated_at=timestamp,
        manifest_path=manifest_relative,
        qa_path=qa_relative,
        revision=revision,
        artifacts=artifacts,
        qa_records=qa_records,
        out_parent=output_path.parent,
        repo_root=root,
    )
    if write:
        _write_atomic(output_path, markdown)
    return FinalIndexResult(
        generated_at=timestamp,
        out_markdown=output_path,
        write_requested=write,
        write_performed=write,
        revision_row_count=int(revision["row_count"]),
        actual_response_basis_count=int(
            revision.get("actual_response_basis_count", 0)
        ),
        fallback_response_basis_count=int(
            revision.get("project_fallback_basis_count", 0)
        ),
        project_owner_basis_count=int(
            revision.get("project_owner_basis_count", 0)
        ),
        required_qa_count=len(required_qa_ids),
        artifacts=artifacts,
        qa_records=qa_records,
        markdown=markdown,
    )


def render_final_index_result(result: FinalIndexResult) -> str:
    """Render a compact final-index dry-run or write report."""
    mode = "write" if result.write_requested else "dry_run"
    lines = [
        "Final closeout index preparation",
        f"- mode={mode}; write_performed={str(result.write_performed).lower()}",
        f"- revision_rows_applied_verified={result.revision_row_count}",
        f"- final_qa_verified={len(result.qa_records)}/{result.required_qa_count}",
        f"- final_artifacts_hashed={len(result.artifacts)}",
        f"- output={result.out_markdown}",
    ]
    if result.write_performed:
        lines.append("- next=open every linked artifact from the final index")
    else:
        lines.append("- next=review this dry run, then rerun with --write")
    return "\n".join(lines)
