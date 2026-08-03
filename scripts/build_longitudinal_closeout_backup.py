"""Create and hash the repository-external longitudinal closeout ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

DEFAULT_MANIFEST = Path("data/longitudinal_artifact_manifest_2026-07-30.json")
DEFAULT_BACKUP = Path(
    "/Users/alfred/Documents/data consent audit system/backup/"
    "ssrp_consent_longitudinal_closeout_2026-07-30.zip"
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out", type=Path, default=DEFAULT_BACKUP)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    manifest_path = repo_root / args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifact_paths = [Path(record["path"]) for record in manifest["files"]]
    archive_paths = [*artifact_paths, args.manifest]

    out_path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative_path in archive_paths:
            archive.write(repo_root / relative_path, arcname=relative_path.as_posix())

    digest = hashlib.sha256(out_path.read_bytes()).hexdigest()
    out_path.with_suffix(".zip.sha256").write_text(
        f"{digest}  {out_path.name}\n",
        encoding="ascii",
    )
    print(f"Wrote {out_path} with {len(archive_paths)} entries")


if __name__ == "__main__":
    main()
