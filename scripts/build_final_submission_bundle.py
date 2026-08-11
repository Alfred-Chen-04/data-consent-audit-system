from __future__ import annotations

import argparse
import csv
import hashlib
import zipfile
from pathlib import Path

BUNDLE_FILES = (
    Path("docs/research/final/FINAL_DELIVERABLES_2026-08-11.md"),
    Path("docs/research/final/cwru_ssrp_closeout_and_submission_2026-08-11.md"),
    Path("docs/research/final/intersections_registration_packet_2026-08-11.md"),
    Path("docs/research/final/ssrp_final_paper_2026-08-11.docx"),
    Path("docs/research/final/ssrp_final_paper_2026-08-11.pdf"),
    Path("docs/research/final/final_results_brief_2026-08-11.md"),
    Path("docs/research/final/项目最终结论与展示提纲_2026-08-11.md"),
    Path("docs/research/final/evidence_chain_audit_2026-08-11.md"),
    Path(
        "docs/research/presentation/"
        "ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04.pptx"
    ),
    Path("docs/research/presentation/ssrp_consent_presentation_readiness_2026-08-04.md"),
    Path("docs/research/poster/ssrp_consent_longitudinal_poster_2026-07-30.pptx"),
    Path("docs/research/poster/Chen.Qianyi.40x32.print.pdf"),
    Path("docs/research/poster/Chen.Qianyi.60x40.print.pdf"),
    Path("data/closeout/cwru_requirement_audit_2026-08-11.csv"),
    Path("data/final_claim_evidence_matrix_2026-08-11.csv"),
    Path("data/retrospective_longitudinal_cases_2026-07-29.csv"),
    Path("data/retrospective_source_registry_2026-07-29.csv"),
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_zip", type=Path)
    parser.add_argument("output_manifest", type=Path)
    args = parser.parse_args()

    missing = [path.as_posix() for path in BUNDLE_FILES if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing bundle files: {missing}")

    records: list[dict[str, str | int]] = []
    args.output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in BUNDLE_FILES:
            data = path.read_bytes()
            records.append(
                {
                    "path": path.as_posix(),
                    "bytes": len(data),
                    "sha256": _sha256(data),
                }
            )
            info = zipfile.ZipInfo(path.as_posix(), date_time=(2026, 8, 11, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)

        lines = ["sha256  bytes  path"]
        lines.extend(
            f"{record['sha256']}  {record['bytes']}  {record['path']}"
            for record in records
        )
        manifest_info = zipfile.ZipInfo(
            "MANIFEST.sha256",
            date_time=(2026, 8, 11, 0, 0, 0),
        )
        manifest_info.compress_type = zipfile.ZIP_DEFLATED
        manifest_info.external_attr = 0o100644 << 16
        archive.writestr(manifest_info, "\n".join(lines) + "\n")

    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.output_manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=("path", "bytes", "sha256"),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    main()
