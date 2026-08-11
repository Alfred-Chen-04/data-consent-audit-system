# Final Cloud Synchronization Audit

## Decision

All durable, non-secret project material found on the computer has been placed
under the active Git repository for synchronization to GitHub. The remaining
local-only files are reproducible environments, caches, Git bookkeeping, or
temporary renders; they are not unique research inputs or deliverables.

## Audited Locations

- Active worktree: `/Users/alfred/Documents/data consent audit system/repo`
- Parent project directory: `/Users/alfred/Documents/data consent audit system`
- Ignored paths reported by the active repository's `.gitignore`

## Recovered Into Git

| Local-only material found | Cloud location | Disposition |
|---|---|---|
| Summer 2026 Intersections compendium PDF, extracted text, and public registration snapshot | `docs/research/final/evidence/program_records_2026-08-11/` | Preserved as offline CWRU program evidence |
| Seven historical patch files | `archive/local_recovery_2026-08-11/patches/` | Preserved; corresponding commits already exist in Git history |
| Two closeout ZIPs and two SHA-256 sidecars | `archive/local_recovery_2026-08-11/backup_zips/` | Preserved; both sidecars verified before copying |
| Eight-file July 29 closeout backup directory | `archive/local_recovery_2026-08-11/closeout_backup_2026-07-29/` | Preserved as a superseded recovery snapshot |

## Deliberate Exclusions

| Local path class | Reason not uploaded |
|---|---|
| `.venv/` (approximately 926 MB) | Reproducible dependency environment, platform-specific, and already defined by `pyproject.toml` plus `uv.lock` |
| `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `__pycache__/`, and `*.pyc` | Generated caches or compiled bytecode |
| Remaining `.tmp/` paper, slide, poster, and source-card renders | Reproducible QA output from tracked DOCX, PDF, PPTX, and source-card files |
| `.tmp/` copies of S09, S12, and the final submission ZIP | Byte-identical to tracked final files |
| Parent-directory `.git/` | Empty repository metadata with no commits and no remote; the active project history is in `repo/.git/` |

No untracked non-ignored file and no ignored `.env`, private key, database, or
credential file was found in the active repository.

## Verification

The final acceptance check is:

1. all files intended for preservation are tracked;
2. the full test and artifact-verification suite passes;
3. archive and final manifests reproduce;
4. the worktree is clean; and
5. local `HEAD` exactly matches `refs/heads/main` on GitHub after push.
