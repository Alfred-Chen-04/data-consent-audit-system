from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

PRIMARY_FILES = (
    Path("docs/research/final/FINAL_DELIVERABLES_2026-08-11.md"),
    Path("docs/research/final/ssrp_final_paper_2026-08-11.md"),
    Path("docs/research/final/ssrp_final_paper_2026-08-11.docx"),
    Path("docs/research/final/ssrp_final_paper_2026-08-11.pdf"),
    Path("docs/research/final/final_results_brief_2026-08-11.md"),
    Path("docs/research/final/项目最终结论与展示提纲_2026-08-11.md"),
    Path("docs/research/final/evidence_chain_audit_2026-08-11.md"),
    Path(
        "docs/research/presentation/"
        "ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04.pptx"
    ),
    Path(
        "docs/research/presentation/"
        "ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04_montage.png"
    ),
    Path("docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.pptx"),
    Path("docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.pdf"),
    Path("docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.png"),
    Path("data/final_claim_evidence_matrix_2026-08-11.csv"),
    Path("data/final_source_card_manifest_2026-08-11.csv"),
    Path("data/retrospective_longitudinal_cases_2026-07-29.csv"),
    Path("data/retrospective_source_registry_2026-07-29.csv"),
    Path("data/longitudinal_directional_review_2026-07-29.csv"),
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _record(path: Path) -> dict[str, object]:
    return {
        "path": path.as_posix(),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    evidence_assets = sorted(
        Path("docs/research/final/evidence").glob("**/*")
    )
    evidence_assets = [path for path in evidence_assets if path.is_file()]
    files = list(PRIMARY_FILES) + evidence_assets
    missing = [path.as_posix() for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing final files: {missing}")

    cases = _read_csv(Path("data/retrospective_longitudinal_cases_2026-07-29.csv"))
    sources = _read_csv(Path("data/retrospective_source_registry_2026-07-29.csv"))
    local = _read_csv(Path("data/longitudinal_directional_review_2026-07-29.csv"))
    direct_source_ids = {
        source_id
        for row in cases
        for source_id in row["source_ids"].split("|")
        if source_id
    }
    capture_pngs = list(Path("data/captures").glob("**/*.png"))

    payload = {
        "schema_version": 1,
        "generated_at": "2026-08-11T00:00:00+08:00",
        "all_files_present": True,
        "research_result": {
            "research_questions": 2,
            "local_site_count": len(local),
            "local_direction_counts": dict(
                Counter(row["directional_label"] for row in local)
            ),
            "historical_case_count": len(cases),
            "historical_direction_counts": dict(
                Counter(row["directional_label"] for row in cases)
            ),
            "source_registry_count": len(sources),
            "direct_case_source_count": len(direct_source_ids),
            "context_source_count": len(sources) - len(direct_source_ids),
            "capture_png_count": len(capture_pngs),
        },
        "files": [_record(path) for path in files],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
