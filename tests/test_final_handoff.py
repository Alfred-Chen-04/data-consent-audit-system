import csv
import hashlib
import json
from pathlib import Path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_august11_final_handoff_is_complete_and_hash_verified() -> None:
    manifest_path = Path("data/final_handoff_manifest_2026-08-11.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["schema_version"] == 1
    assert manifest["all_files_present"] is True
    assert manifest["research_result"] == {
        "research_questions": 2,
        "local_site_count": 5,
        "local_direction_counts": {"insufficient_evidence": 5},
        "historical_case_count": 6,
        "historical_direction_counts": {"improved": 5, "regressed": 1},
        "source_registry_count": 12,
        "direct_case_source_count": 8,
        "context_source_count": 4,
        "capture_png_count": 365,
    }

    for record in manifest["files"]:
        path = Path(record["path"])
        assert path.is_file(), path
        assert path.stat().st_size == record["bytes"]
        assert _sha256(path) == record["sha256"]


def test_august11_claim_and_source_evidence_boundaries() -> None:
    with Path("data/final_claim_evidence_matrix_2026-08-11.csv").open(
        newline="", encoding="utf-8"
    ) as stream:
        claims = list(csv.DictReader(stream))
    with Path("data/retrospective_source_registry_2026-07-29.csv").open(
        newline="", encoding="utf-8"
    ) as stream:
        sources = list(csv.DictReader(stream))

    assert len(claims) == 14
    assert all(row["verification_status"].startswith("verified") for row in claims)
    assert all(row["claim_boundary"] for row in claims)
    assert len(sources) == 12
    assert all(row["last_verified_at"] == "2026-08-11" for row in sources)

    source_cards = sorted(
        Path("docs/research/final/evidence/source_cards_2026-08-11").glob("*.png")
    )
    source_screenshots = sorted(
        Path("docs/research/final/evidence/source_screenshots_2026-08-11").glob(
            "*.png"
        )
    )
    source_documents = sorted(
        Path("docs/research/final/evidence/source_documents_2026-08-11").glob(
            "*.pdf"
        )
    )
    assert len(source_cards) == 12
    assert len(source_screenshots) == 5
    assert len(source_documents) == 2
    assert all(path.read_bytes().startswith(b"%PDF-") for path in source_documents)


def test_august11_final_paper_uses_the_corrected_vanity_fair_claim() -> None:
    paper = Path(
        "docs/research/final/ssrp_final_paper_2026-08-11.md"
    ).read_text(encoding="utf-8")

    assert "Refusal effectiveness regressed; transparency not assessed" in paper
    assert "Transparency and refusal effectiveness regressed" not in paper
    normalized = " ".join(paper.split()).lower()
    assert "five improve at least one audited component and one" in normalized
    assert "not prevalence estimates" in normalized
