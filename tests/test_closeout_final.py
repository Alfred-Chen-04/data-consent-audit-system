"""Tests for the fully gated final closeout index."""

import csv
import json
from datetime import datetime
from pathlib import Path

import pytest

from consent_audit.closeout_final import (
    DEFAULT_FINAL_ARTIFACTS,
    FINAL_QA_REQUIRED_COLUMNS,
    prepare_final_closeout_index,
    render_final_index_result,
)


def test_default_final_artifacts_point_to_current_longitudinal_outputs() -> None:
    paths = {role: path.as_posix() for role, path in DEFAULT_FINAL_ARTIFACTS}

    assert paths["Presentation PPTX"].endswith(
        "ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04.pptx"
    )
    assert paths["Poster PDF"].endswith(
        "ssrp_consent_longitudinal_poster_2026-07-30.pdf"
    )
    assert paths["Retrospective cases"] == (
        "data/retrospective_longitudinal_cases_2026-07-29.csv"
    )
    assert paths["Longitudinal artifact manifest"] == (
        "data/longitudinal_artifact_manifest_2026-07-30.json"
    )
    assert paths["Closeout reconciliation"] == (
        "docs/research/aug03_closeout_reconciliation_2026-08-03.md"
    )
    assert paths["Final paper working draft"] == (
        "docs/research/ssrp_final_paper_working_draft_2026-08-03.md"
    )
    assert paths["Final paper submission candidate"] == (
        "docs/research/ssrp_final_paper_submission_candidate_2026-08-05.docx"
    )
    assert paths["Presentation readiness guide"] == (
        "docs/research/presentation/"
        "ssrp_consent_presentation_readiness_2026-08-04.md"
    )


def _write_manifest(path: Path, *, ready: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    blockers = [] if ready else [
        {"code": "revision_rows_not_applied_verified", "count": 1}
    ]
    path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "freeze_readiness": {
                    "ready_for_final_freeze": ready,
                    "blockers": blockers,
                },
                "revision_execution_gate": {
                    "row_count": 1,
                    "status_counts": {"applied_verified": 1 if ready else 0},
                    "coverage_valid": True,
                    "row_states_valid": True,
                    "response_basis_claims_valid": True,
                    "joint_decision_contract_valid": True,
                    "not_applied_verified_count": 0 if ready else 1,
                    "response_basis_claim_count": 1 if ready else 0,
                    "response_basis_validation_errors": [],
                    "joint_decision_contract_validation_errors": [],
                    "actual_response_basis_count": 1,
                    "project_fallback_basis_count": 0,
                    "project_owner_basis_count": 0,
                },
            }
        ),
        encoding="utf-8",
    )


def _write_qa(path: Path, *, status: str, verified_at: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FINAL_QA_REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerow(
            {
                "check_id": "qa_1",
                "check_scope": "all artifacts",
                "required_verification": "render and inspect",
                "status": status,
                "evidence": "final render report" if status == "verified" else "",
                "verified_by": "researcher" if status == "verified" else "",
                "verified_at": verified_at if status == "verified" else "",
                "notes": "",
            }
        )


def test_final_index_refuses_unready_manifest_before_writing(tmp_path: Path) -> None:
    manifest = tmp_path / "data/manifest.json"
    qa = tmp_path / "data/qa.csv"
    output = tmp_path / "docs/final.md"
    artifact = tmp_path / "artifact.txt"
    _write_manifest(manifest, ready=False)
    _write_qa(qa, status="pending")
    artifact.write_text("artifact", encoding="utf-8")

    with pytest.raises(ValueError, match="not ready for final freeze"):
        prepare_final_closeout_index(
            repo_root=tmp_path,
            manifest_json=manifest,
            final_qa_csv=qa,
            out_markdown=output,
            required_qa_ids=("qa_1",),
            final_artifacts=(("Artifact", artifact),),
            write=True,
        )
    assert not output.exists()


def test_final_index_refuses_pending_or_invalid_qa(tmp_path: Path) -> None:
    manifest = tmp_path / "data/manifest.json"
    qa = tmp_path / "data/qa.csv"
    artifact = tmp_path / "artifact.txt"
    _write_manifest(manifest, ready=True)
    _write_qa(qa, status="pending")
    artifact.write_text("artifact", encoding="utf-8")

    with pytest.raises(ValueError, match="status is not verified"):
        prepare_final_closeout_index(
            repo_root=tmp_path,
            manifest_json=manifest,
            final_qa_csv=qa,
            required_qa_ids=("qa_1",),
            final_artifacts=(("Artifact", artifact),),
        )

    _write_qa(qa, status="verified", verified_at="2026-08-06T12:00:00")
    with pytest.raises(ValueError, match="must include a timezone"):
        prepare_final_closeout_index(
            repo_root=tmp_path,
            manifest_json=manifest,
            final_qa_csv=qa,
            required_qa_ids=("qa_1",),
            final_artifacts=(("Artifact", artifact),),
        )


def test_final_index_dry_run_then_atomic_write(tmp_path: Path) -> None:
    manifest = tmp_path / "data/manifest.json"
    qa = tmp_path / "data/qa.csv"
    artifact = tmp_path / "artifact.txt"
    output = Path("docs/final.md")
    _write_manifest(manifest, ready=True)
    _write_qa(
        qa,
        status="verified",
        verified_at="2026-08-06T12:00:00+08:00",
    )
    artifact.write_text("artifact", encoding="utf-8")
    generated_at = datetime.fromisoformat("2026-08-06T13:00:00+08:00")

    dry_run = prepare_final_closeout_index(
        repo_root=tmp_path,
        manifest_json=manifest,
        final_qa_csv=qa,
        out_markdown=output,
        generated_at=generated_at,
        required_qa_ids=("qa_1",),
        final_artifacts=(("Artifact", artifact),),
    )

    assert dry_run.write_performed is False
    assert dry_run.required_qa_count == 1
    assert len(dry_run.qa_records) == 1
    assert len(dry_run.artifacts) == 2
    assert "Revision rows applied and verified: 1/1" in dry_run.markdown
    assert "Actual-response rows: 1" in dry_run.markdown
    assert "final render report" in dry_run.markdown
    assert "artifact.txt" in dry_run.markdown
    assert not (tmp_path / output).exists()
    assert "final_qa_verified=1/1" in render_final_index_result(dry_run)

    written = prepare_final_closeout_index(
        repo_root=tmp_path,
        manifest_json=manifest,
        final_qa_csv=qa,
        out_markdown=output,
        generated_at=generated_at,
        required_qa_ids=("qa_1",),
        final_artifacts=(("Artifact", artifact),),
        write=True,
    )
    saved = (tmp_path / output).read_text(encoding="utf-8")
    assert written.write_performed is True
    assert saved == written.markdown
    assert "Status: `final_closeout_index`" in saved


def test_final_index_rejects_paths_outside_repository(tmp_path: Path) -> None:
    manifest = tmp_path / "data/manifest.json"
    qa = tmp_path / "data/qa.csv"
    _write_manifest(manifest, ready=True)
    _write_qa(
        qa,
        status="verified",
        verified_at="2026-08-06T12:00:00+08:00",
    )

    with pytest.raises(ValueError, match="inside the repository"):
        prepare_final_closeout_index(
            repo_root=tmp_path,
            manifest_json=manifest,
            final_qa_csv=qa,
            out_markdown=tmp_path.parent / "outside.md",
            required_qa_ids=("qa_1",),
            final_artifacts=(),
            write=True,
        )
