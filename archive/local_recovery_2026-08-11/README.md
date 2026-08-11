# Local Recovery Archive

This directory preserves durable project files that were found outside the
active `repo/` Git worktree during the final computer-handoff audit on August
11, 2026. These are recovery copies, not the current research deliverables.

## Contents

- `patches/`: seven historical email-format patches. Their changes already
  exist in Git commits `7ecbb35`, `b4d2a7a`, `1e9bf62`, `aa76e85`, `fae345b`,
  `97394b2`, and `d77ef99`; the patch files are retained as exact local
  recovery artifacts.
- `backup_zips/`: July 29 and July 30 closeout ZIPs plus their SHA-256
  sidecars. Both sidecar checks passed before copying.
- `closeout_backup_2026-07-29/`: the eight-file expanded July 29 closeout
  backup, including presentation, poster, and evidence-package copies.
- `desktop_stale_clone_inventory.csv`: a 508-row byte-level inventory of every
  untracked Finder ` 2` copy in the stale June 15 desktop clone. It records the
  file size, SHA-256, Git blob ID, corresponding unsuffixed path, and whether
  the exact bytes were already reachable from a GitHub remote ref.
- `desktop_stale_clone_unique/`: exact copies of the 24 stale-clone files whose
  Git blobs were not reachable from any GitHub remote ref. The other 484
  untracked files are represented by exact byte-identical blobs already in the
  remote Git history and are therefore not duplicated here.
- `desktop_stale_clone_ignored_captures.zip`: a lossless ZIP of the 326 ignored
  historical `layer1.html` captures found only in the stale desktop clone. The
  archive contains 72,400,099 source bytes and passed `ZipFile.testzip()`.
- `desktop_stale_clone_ignored_capture_inventory.csv`: member path, size,
  SHA-256, and Git blob ID for all 326 files in that ZIP.
- `MANIFEST.sha256`: hashes for every archived file except the manifest itself.

Use `docs/research/final/FINAL_DELIVERABLES_2026-08-11.md` for the current paper,
presentation, poster, evidence package, and submission ZIP. The files here are
intentionally historical and may contain superseded wording or layouts.
