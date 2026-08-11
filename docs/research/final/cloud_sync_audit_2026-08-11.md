# Final Cloud Synchronization Audit

## Decision

All durable, non-secret material attributable to this research project and
found during the computer-wide closeout scan has been placed under the active
Git repository for synchronization to GitHub. The remaining local-only files
are unrelated personal or company material, reproducible environments, caches,
Git bookkeeping, or temporary renders; they are not unique research inputs or
deliverables.

## Audited Locations

- Active worktree: `/Users/alfred/Documents/data consent audit system/repo`
- Parent project directory: `/Users/alfred/Documents/data consent audit system`
- Stale desktop clone: `/Users/alfred/Desktop/data-consent-audit-system`
- Desktop, Downloads, Documents, and Trash paths found through filename,
  full-text, and Spotlight searches for the project title, SSRP, CWRU
  Intersections, advisor, consent-interface, cookie-banner, and related terms
- Top-level Desktop screenshots: 104 readable images checked with local OCR;
  the other two images were only `4 x 2` and `2 x 4` pixels
- Ignored paths reported by the active repository's `.gitignore`

## Recovered Into Git

| Local-only material found | Cloud location | Disposition |
|---|---|---|
| Summer 2026 Intersections compendium PDF, extracted text, and public registration snapshot | `docs/research/final/evidence/program_records_2026-08-11/` | Preserved as offline CWRU program evidence |
| Seven historical patch files | `archive/local_recovery_2026-08-11/patches/` | Preserved; corresponding commits already exist in Git history |
| Two closeout ZIPs and two SHA-256 sidecars | `archive/local_recovery_2026-08-11/backup_zips/` | Preserved; both sidecars verified before copying |
| Eight-file July 29 closeout backup directory | `archive/local_recovery_2026-08-11/closeout_backup_2026-07-29/` | Preserved as a superseded recovery snapshot |
| 508 untracked Finder ` 2` files in the stale desktop clone | `archive/local_recovery_2026-08-11/desktop_stale_clone_inventory.csv` | Every file inventoried by size, SHA-256, and Git blob ID; 484 exact blobs already reachable from GitHub refs |
| 24 stale-clone files not represented by a GitHub-reachable blob | `archive/local_recovery_2026-08-11/desktop_stale_clone_unique/` | Preserved byte-for-byte with original relative paths |
| 326 ignored historical `layer1.html` captures found only in the stale clone | `archive/local_recovery_2026-08-11/desktop_stale_clone_ignored_captures.zip` | All 72,400,099 source bytes preserved; ZIP test passed and every member has a SHA-256 row in the adjacent inventory CSV |

## Deliberate Exclusions

| Local path class | Reason not uploaded |
|---|---|
| `.venv/` (approximately 926 MB) | Reproducible dependency environment, platform-specific, and already defined by `pyproject.toml` plus `uv.lock` |
| Stale-clone `.venv/`, Python caches, and compiled bytecode among 5,744 ignored paths | Reproducible environment material; the 326 non-cache ignored captures were separately recovered |
| `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `__pycache__/`, and `*.pyc` | Generated caches or compiled bytecode |
| Remaining `.tmp/` paper, slide, poster, and source-card renders | Reproducible QA output from tracked DOCX, PDF, PPTX, and source-card files |
| `.tmp/` copies of S09, S12, and the final submission ZIP | Byte-identical to tracked final files |
| Parent-directory `.git/` | Empty repository metadata with no commits and no remote; the active project history is in `repo/.git/` |
| `/Users/alfred/Desktop/CWRU`, `/Users/alfred/Documents/CWRU`, and `/Users/alfred/Desktop/CWRU暑期研究` | Searches found coursework, planning, invoices, due-diligence, IP, and resume material, but no additional consent-audit research artifact |
| VeloDB privacy, cookie, DPA, audit, and compliance files under Desktop, Downloads, and Terminal workspaces | Separate company project, often confidential; keyword overlap alone does not make it part of this research archive |
| 106 top-level Desktop screenshots | OCR found VeloDB work, personal pages, credentials, or only views of folder names; no unique research evidence was identified, and private screenshots were deliberately not uploaded |

No untracked non-ignored file and no ignored `.env`, private key, database, or
credential file was found in the active repository.

The stale clone's `38da2ac` head is an ancestor of the current GitHub `main`.
All local branch tips have matching remote refs, and `git log --all --not
--remotes` reports no commit reachable only from a local ref.

## Verification

The final acceptance check is:

1. all files intended for preservation are tracked;
2. the full test and artifact-verification suite passes;
3. archive and final manifests reproduce;
4. the worktree is clean; and
5. local `HEAD` exactly matches `refs/heads/main` on GitHub after push.
