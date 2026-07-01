# Today Work Note, 2026-07-01

## Bottom Line

Today was a fact-check, midpoint recheck, and evidence-wording cleanup day.

Do not describe the project as halfway complete as a final SSRP deliverable.
As of 2026-07-01, the project is near the calendar midpoint of the May 30-Aug.
7 core cycle, but the paper dataset and final writing are still behind the
calendar.

The useful work today is to keep the current state traceable, fix one remaining
evidence-wording ambiguity, and keep the next action focused on decisions rather
than blind capture.

## Verified Facts

- Current local branch: `codex/project-status-plain-language`.
- Local branch is synced with `origin/codex/project-status-plain-language` at
  `e9542343909282cb230d644ed13a6388ca8b4ab6` before this note.
- `origin/main` is still at
  `28ee83755bc1eb379b08a8941ebad146d9c8fd45`, so PR #8 content is not in
  `main` yet.
- GitHub PR #8:
  <https://github.com/Alfred-Chen-04/data-consent-audit-system/pull/8>
- PR #8 state from GitHub: `open`
- PR #8 draft: `true`
- PR #8 merged: `false`
- PR #8 mergeable: `true`
- `consent-audit research-status` still reports:
  - Week 2 targets: 5
  - cycle: `completed`
  - sanity: `ready`
  - audit reports: 42
  - longitudinal summaries: 20
  - CMP confirmations: pending=8
  - paper artifacts present: claim register, figure plan, paper skeleton,
    poster plan, results tables, writing pack
- `data/current_five_decision_sheet_2026-06-19.csv` has 7 rows and 7 blank
  `confirmed_decision` cells.
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` has 8 rows, all
  `pending`, with 8 blank `confirmed_decision` cells.
- `data/research_package/audit_report_summary.csv` has 42 rows:
  `banner_detected=true` for 9 rows and `banner_detected=false` for 33 rows.
- `data/research_package/longitudinal_summary.csv` has 20 rows.
- `data/captures/sites` currently has 326 `layer1.png` screenshot files and 0
  `layer1.html` raw DOM files in this checkout.

## Calendar Midpoint Check

Using the May 30-Aug. 7, 2026 core build/research cycle:

| Date fact | Value |
|---|---|
| Core cycle start | 2026-05-30 |
| Current date | 2026-07-01 |
| Core cycle end | 2026-08-07 |
| Inclusive elapsed days | 33 of 70 |
| Calendar progress | about 47.1% |
| Calendar midpoint dates | around 2026-07-03 to 2026-07-04 |
| Days left to core end | 37 |
| Days left to Aug. 31 polish end | 61 |

Interpretation: the project is almost at the calendar midpoint, but it has not
quite crossed it yet. By deliverable readiness, the technical pipeline is ahead
of halfway, while the final research sample, advisor-confirmed decisions, paper
prose, and poster/demo are not halfway complete.

## What Was Corrected Today

The Week 2 sanity check previously said `Evidence-complete rows: 5/5`, which
is true for the consent-table fields but could be misread as proving that raw
HTML files are synced locally.

Today I updated the sanity-check generator so regenerated sanity checks now say
that evidence completeness means screenshot ref, DOM snapshot ref, DOM hash,
and image hash are present in the consent table, and that raw DOM file sync
must be verified separately before claiming local HTML availability.

Regenerated file:

- `docs/research/week2_sanity_check_2026-06-06.md`

Code/test files updated:

- `src/consent_audit/week2_sanity.py`
- `tests/test_week2_sanity.py`
- `tests/test_research_artifacts.py`

## What Still Holds From The June 29 Audit

- PR #8 is still the current project-status handoff PR and is not merged into
  `main`.
- The current five-site evidence gate remains valid as a Week 2 evidence gate,
  not as the final SSRP dataset.
- The current five should still be treated as 2 banner/control evidence cases
  and 3 no-visible-banner contrast candidates unless the advisor decides
  otherwise.
- The 20-site deep sample is not locked.
- The current-five decision sheet is still blank.
- The CMP/manual-review confirmation sheet is still pending.
- No new browser capture or new consent-interface evidence was added today.

## Today's Safe Work Boundary

Do not run a blind capture just to create progress. The evidence-supported next
step is still a decision gate:

1. Review or merge PR #8 so the clarified project state reaches `main`.
2. Send or adapt
   `docs/research/advisor_email_decision_gate_2026-06-28.md`.
3. Record the advisor/user answer in
   `data/current_five_decision_sheet_2026-06-19.csv`.
4. Then pick one work mode:
   - manually validate and write up the current five,
   - rerun the current five with the fixed capture agent,
   - expand toward about 20 deep sites with priority on banner-present/control
     evidence,
   - or resolve the 8 CMP/manual-review rows first.

## If We Need To Catch Up

The fastest evidence-safe catch-up path is not to build more infrastructure.
It is:

1. Lock the current-five table rule.
2. Add 10-15 more banner-present/control-evidence candidates only after that
   rule is recorded.
3. Refresh the RQ1/RQ2 exports after successful captures.
4. Turn the existing skeleton/writing pack into actual paper prose during
   Week 8-10.

Do not claim the project has reached final-paper halfway until at least the
current-five rule is recorded and the expansion or fallback writing path is
chosen.
