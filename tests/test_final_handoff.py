import csv
import hashlib
import json
import zipfile
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
    assert "Program: CWRU 2026 Sponsored Summer Research Program" in paper


def test_august11_cwru_submission_bundle_is_complete() -> None:
    packet = Path(
        "docs/research/final/intersections_registration_packet_2026-08-11.md"
    ).read_text(encoding="utf-8")
    normalized_packet = " ".join(packet.split())
    assert "**Abstract word count:** 211" in packet
    assert "December 4, 2026" in packet
    assert "April 16, 2027" in normalized_packet
    assert "web-wide prevalence" in packet

    audit_path = Path("data/closeout/cwru_requirement_audit_2026-08-11.csv")
    with audit_path.open(newline="", encoding="utf-8") as stream:
        requirements = list(csv.DictReader(stream))
    assert len(requirements) == 7
    statuses = {row["requirement_id"]: row["verified_status"] for row in requirements}
    assert statuses["project_completion"] == "verified"
    assert statuses["intersections_presentation"] == "pending_external_event"
    assert statuses["final_paper"] == "ready_for_external_submission"

    bundle = Path(
        "docs/research/final/ssrp_final_submission_bundle_2026-08-11.zip"
    )
    manifest_path = Path("data/final_submission_bundle_manifest_2026-08-11.csv")
    with manifest_path.open(newline="", encoding="utf-8") as stream:
        records = list(csv.DictReader(stream))
    with zipfile.ZipFile(bundle) as archive:
        names = set(archive.namelist())
        assert "MANIFEST.sha256" in names
        for record in records:
            assert record["path"] in names
            data = archive.read(record["path"])
            assert len(data) == int(record["bytes"])
            assert hashlib.sha256(data).hexdigest() == record["sha256"]
