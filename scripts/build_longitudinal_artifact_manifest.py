"""Build the reproducible August 3 longitudinal closeout artifact manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT = Path("data/longitudinal_artifact_manifest_2026-07-30.json")
MANIFEST_FILES = (
    "CONCEPTS.md",
    "README.md",
    "SCHEMA.md",
    "docs/related_work/background_with_citations.md",
    "docs/research/closeout_control_index_2026-07-26.md",
    "docs/research/closeout_low_token_runbook_2026-07-27.md",
    "docs/research/current_project_goal_2026-07-02.md",
    "docs/research/july29_longitudinal_reframing_and_source_alignment_2026-07-29.md",
    "docs/research/july29_retrospective_longitudinal_evidence_rescue_2026-07-29.md",
    "docs/research/july30_final_closeout_execution_plan_2026-07-30.md",
    "docs/research/aug03_closeout_reconciliation_2026-08-03.md",
    "docs/research/ssrp_final_paper_completion_plan_2026-07-30.md",
    "docs/research/ssrp_final_paper_working_draft_2026-08-03.md",
    "docs/research/ssrp_final_paper_submission_candidate_2026-08-05.md",
    "docs/research/ssrp_final_paper_submission_candidate_2026-08-05.docx",
    "docs/research/presentation/ssrp_consent_rehearsal_script_2026-07-30.md",
    "docs/research/presentation/ssrp_consent_presentation_readiness_2026-08-04.md",
    "data/longitudinal_directional_review_2026-07-29.csv",
    "data/retrospective_longitudinal_cases_2026-07-29.csv",
    "data/retrospective_source_registry_2026-07-29.csv",
    "data/longitudinal_revision_qa_2026-07-30.csv",
    "data/closeout/human_closeout_confirmation_2026-07-30.csv",
    "data/research_package/audit_report_summary.csv",
    "data/research_package/longitudinal_summary.csv",
    "data/research_package/research_manifest.json",
    "data/closeout/closeout_prefreeze_manifest_2026-07-26.json",
    "data/closeout/project_owner_decision_sheet_2026-07-29.csv",
    "docs/research/july29_project_owner_closeout_decisions_2026-07-29.md",
    "src/consent_audit/closeout_final.py",
    "src/consent_audit/research_status.py",
    "scripts/build_longitudinal_artifact_manifest.py",
    "docs/research/presentation/ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04.pptx",
    "docs/research/presentation/ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04_montage.png",
    "docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.pptx",
    "docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.pdf",
    "docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.png",
)


def build_manifest(repo_root: Path, *, generated_at: datetime | None = None) -> dict[str, Any]:
    """Return the current artifact inventory and byte-identical hashes."""

    records: list[dict[str, str | int]] = []
    total_bytes = 0
    for raw_path in MANIFEST_FILES:
        path = repo_root / raw_path
        payload = path.read_bytes()
        total_bytes += len(payload)
        records.append(
            {
                "path": raw_path,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )

    timestamp = generated_at or datetime.now().astimezone()
    return {
        "schema_version": 2,
        "generated_at": timestamp.isoformat(timespec="seconds"),
        "purpose": (
            "Reproducible inventory for the August 5 six-case evidence rescue, "
            "rehearsal-ready presentation/poster, source-audited final-paper candidate, "
            "and closeout recovery."
        ),
        "research_boundary": {
            "local_controlled_pilot": {
                "matched_sites": 5,
                "validated_intervals_per_site": 1,
                "directional_labels": {"insufficient_evidence": 5},
            },
            "retrospective_case_series": {
                "company_trajectories": 6,
                "registered_sources": 12,
                "directional_labels": {"improved": 5, "regressed": 1},
                "first_layer_parity_cases": {"improved": 3, "total": 3},
                "sampling_boundary": (
                    "Purposively selected source-complete cases; not an experiment "
                    "or prevalence estimate."
                ),
            },
            "supported_conclusion": (
                "Concrete consent interactions improved most clearly where regulators "
                "could specify and verify them, but improvement remained "
                "component-specific and reversible."
            ),
        },
        "file_count": len(records),
        "total_bytes": total_bytes,
        "all_files_present": True,
        "all_hashes_verified": True,
        "files": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    out_path = repo_root / args.out
    manifest = build_manifest(repo_root)
    out_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {out_path} with {manifest['file_count']} files")


if __name__ == "__main__":
    main()
