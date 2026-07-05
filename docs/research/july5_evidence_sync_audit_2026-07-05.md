# July 5 Evidence Sync Audit, 2026-07-05

Purpose: verify whether the evidence files exist, whether the screenshot
evidence is valid, whether the important refs point to real local files, and
whether the latest work is committed to GitHub.

This audit adds no new browser capture and no new consent-interface evidence.

## Commands And Sources Checked

- `git fetch origin`
- `git status -sb`
- `git rev-parse HEAD`
- `git rev-parse @{u}`
- `git ls-files`
- `git ls-tree -r origin/codex/project-status-plain-language`
- GitHub connector read of PR #8
- `PYTHONPATH=src /Users/alfred/Desktop/data-consent-audit-system/.venv/bin/consent-audit research-status`
- structured Python reads of:
  - `data/research_package/audit_report_summary.csv`
  - `data/research_package/longitudinal_summary.csv`
  - `data/week2_manual_evidence_review_2026-06-10.csv`
  - `data/current_five_decision_sheet_2026-06-19.csv`
  - `data/cmp_review_queue_pilot_2026-05-30.csv`
  - `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`

## GitHub Sync State

- Current branch: `codex/project-status-plain-language`.
- Local HEAD: `3c202181ca6510e5fd395989b2b62511aa155641`.
- Upstream HEAD: `3c202181ca6510e5fd395989b2b62511aa155641`.
- Latest commit: `3c20218 Add July 3 scope review and poster plan`.
- PR #8: open, draft, mergeable, not merged.
- PR #8 head SHA: `3c202181ca6510e5fd395989b2b62511aa155641`.

Conclusion: the latest local work is committed and pushed to the GitHub PR
branch. It is not merged into `main` yet.

## Screenshot Evidence Sync

Local filesystem:

- `data/captures` contains 365 PNG files.
- `data/captures/sites` contains 326 `layer1.png` files.
- `data/captures/sites` contains 0 `layer1.html` raw DOM files.
- All 365 PNG files parse as valid PNG files.
- All 365 PNG files are `1440x900`.
- PNG file sizes range from 14,031 bytes to 1,294,565 bytes.

Git tracking:

- Git tracks 365 capture PNG files.
- Git tracks 326 site `layer1.png` files.
- Git tracks 0 site `layer1.html` raw DOM files.

Remote PR branch:

- `origin/codex/project-status-plain-language` contains 365 capture PNG files.
- `origin/codex/project-status-plain-language` contains 326 site `layer1.png`
  files.
- `origin/codex/project-status-plain-language` contains 0 site `layer1.html`
  raw DOM files.

Conclusion: screenshot evidence is present locally, tracked by Git, and present
on the GitHub PR branch. Raw HTML files are not synced.

## Research Package Evidence

`data/research_package/audit_report_summary.csv`:

- Rows: 42.
- Screenshot refs: 42.
- Missing screenshot refs: 0.
- DOM refs: 42.
- Missing raw DOM HTML files: 42.
- `banner_detected` counts: true=9, false=33.

`data/research_package/longitudinal_summary.csv`:

- Rows: 20.

Conclusion: the research package has valid screenshot refs and current
longitudinal rows. It also contains DOM refs and DOM hashes, but the raw DOM
HTML files behind those refs are not synced in this checkout.

## Current-Five Evidence

`data/week2_manual_evidence_review_2026-06-10.csv`:

- Rows: 5.
- Sites: The Guardian, CNN, Booking.com, NerdWallet, Coca-Cola.
- Missing screenshots: 0.
- Bad screenshots: 0.
- Missing raw DOM HTML files: 5.
- Evidence classes:
  - The Guardian: `banner_present`
  - Coca-Cola: `banner_present`
  - CNN: `no_visible_banner`
  - Booking.com: `no_visible_banner`
  - NerdWallet: `no_visible_banner`

`data/current_five_decision_sheet_2026-06-19.csv`:

- Rows: 7.
- Blank confirmed decisions: 7.

Conclusion: current-five screenshot evidence is present and valid. Current-five
raw HTML files and human/advisor decisions are not complete.

## CMP Manual-Review Evidence

`data/cmp_review_queue_pilot_2026-05-30.csv`:

- Rows: 8.
- Missing access screenshots: 0.
- Missing capture screenshots: 0.
- Bad capture screenshots: 0.
- Missing raw DOM HTML files: 8.

`data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`:

- Rows: 8.
- Pending confirmations: 8.
- Blank confirmed decisions: 8.

Conclusion: CMP/manual-review screenshot evidence is present and valid, but the
raw DOM HTML files and human confirmations are not complete.

## Final Evidence Judgment

Safe to say:

- Screenshot evidence is present locally.
- Screenshot evidence is valid PNG evidence.
- Screenshot evidence is tracked by Git and present on the GitHub PR branch.
- The research package contains 42 audit reports and 20 longitudinal summaries.
- The current five have valid screenshot evidence.
- CMP/manual-review rows have valid access and capture screenshots.
- The latest documentation/status work is committed and pushed to PR #8.

Do not say:

- Raw `layer1.html` files are synced.
- DOM HTML evidence files are complete.
- Current-five decisions are complete.
- CMP/manual-review confirmations are complete.
- PR #8 is merged into `main`.
- The final 20-site dataset is complete.

Recommended next action:

- Merge or review PR #8 so `main` has the current project-state and evidence
  audit docs.
- Then resolve the 7 current-five decisions and 8 CMP/manual-review
  confirmations before adding more live capture.
