# Summer Midpoint Progress Audit, 2026-06-29

2026-07-01 scope update: the current summer deliverables are presentation +
large poster + traceable evidence package. A formal SSRP paper is no longer a
required summer deliverable unless Dr. Singh reintroduces it later. Interpret
the paper-related notes below as historical/future-paper support, not the
current July/August priority.

## Bottom Line

By calendar, the project is close to the middle of the 10-week core SSRP cycle:
2026-06-29 is Week 5, about 44% of the May 30-August 7 core window.

By deliverable readiness, the project is uneven:

- The research infrastructure and evidence pipeline are more than halfway for
  an SSRP demo/research-method artifact.
- The final research dataset is not halfway if the target remains about 20 deep
  sites, because only 5 current sites are in the Week 2 evidence gate.
- The presentation/poster are scaffolded but not final deliverables.

So the honest answer is: the project is not "nothing happened," but it is also
not safe to say the whole summer project is halfway complete as a final
presentation/poster package. It is around the middle by time, ahead on tooling,
behind on sample-lock and presentation/poster finalization.

## Evidence Checked

This audit is based on current repository and GitHub state:

- GitHub PR #8 is `open`, `draft=true`, `merged=false`, and `mergeable=true`.
- Current local branch is `codex/project-status-plain-language`.
- `research-status` reports:
  - Week 2 targets: 5
  - sanity: `ready`
  - cycle: `completed`
  - audit reports: 42
  - longitudinal summaries: 20
  - CMP confirmations: pending=8
  - paper artifacts present: claim register, figure plan, paper skeleton,
    poster plan, results tables, writing pack
- `data/current_five_decision_sheet_2026-06-19.csv` has 7 blank
  `confirmed_decision` cells.
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` has 8 rows, all
  `pending`, with 8 blank `confirmed_decision` cells.
- `data/captures/sites` has 326 tracked `layer1.png` screenshot files and 0
  synced `layer1.html` files in the current checkout.
- Targeted research artifact/status tests pass: 32 tests.

## Calendar Position

Using the May 30-August 7 core build/research cycle:

| Date fact | Value |
|---|---|
| Core cycle start | 2026-05-30 |
| Current date | 2026-06-29 |
| Core cycle end | 2026-08-07 |
| Inclusive elapsed days | 31 of 70 |
| Calendar progress | about 44% |
| Current roadmap week | Week 5 of 10 |
| Days left to core end | 39 |
| Days left to Aug. 31 polish end | 63 |

The Week 5 roadmap item in
`docs/research/ssrp_project_clarity_plan_2026-05-30.md` is Layer 3 /
transparency-framing organization. The code and generated artifacts already
have a deterministic Layer 3 fallback and paper-facing writing support, but the
manual sample decisions needed before broader capture are still unresolved.

## What Is Solidly Done

| Area | Status | Evidence |
|---|---|---|
| Research framing | Solid | RQ1/RQ2 remain the core; SOC 2 is not the core frame. |
| Code pipeline | Solid for SSRP MVP | Capture/scoring/report/export/weekly-summary CLI paths exist and are tested. |
| Week 2 evidence gate | Solid | 5/5 targets captured; sanity `ready`; 42 reports and 20 summaries in package. |
| Screenshot evidence | Solid for current synced repo | 326 tracked `layer1.png` screenshots; current-five screenshots verified. |
| Current-five interpretation | Solid as draft, pending advisor confirmation | Guardian/Coca-Cola are banner/control evidence; CNN/Booking/NerdWallet are no-visible-banner contrast candidates. |
| Presentation/poster scaffolding | Solid as scaffold | Results tables, writing support notes, claim register, figure plan, and poster plan exist. |
| Fact-correction discipline | Improved | PR #8 corrects raw HTML sync claims and adds plain-language handoff. |

## What Is Incomplete

| Area | Current gap | Why it matters |
|---|---|---|
| Deep sample | Only 5 current Week 2 targets, not about 20 | The planned SSRP paper sample is not locked. |
| Decision sheet | 7 current-five decisions blank | We cannot fairly choose rerun/manual-validation/expansion mode yet. |
| CMP/manual-review | 8 pending confirmations | These rows should not be treated as final sample decisions. |
| Raw DOM files | 0 synced `layer1.html` files in current checkout | Current synced evidence should be described as screenshots, DOM hashes/report refs, CSVs, and JSONL reports. |
| Week 3 continuity | 2026-06-14 attempt failed at browser navigation | It did not create valid new consent-interface observations. |
| Final presentation | Not built | Existing files are scaffold/current-evidence support, not a final slide deck. |
| Final poster/demo | Not final | Poster plan exists; demo/evidence browser is not final. |

## Corrections Made Today

I found and corrected current-material wording that could be read too strongly:

- Updated `docs/research/advisor_email_decision_gate_2026-06-28.md` so it says
  the five current sites have synced screenshots, DOM hashes/report refs, and a
  manual review packet, rather than implying raw DOM HTML files are synced.
- Updated `src/consent_audit/paper_tables.py` so regenerated results tables
  warn that evidence refs may include generated DOM paths and raw HTML file
  availability must be verified separately.
- Regenerated `docs/research/ssrp_results_tables_2026-06-06.md` with that
  caveat.
- Added a 2026-06-29 correction note to
  `docs/research/full_project_fact_audit_2026-06-10.md`, because its screenshot
  count and DOM-file availability statements are historical, not current.

## Halfway Assessment

| Dimension | Approximate state | Reason |
|---|---|---|
| Calendar | Near halfway | Week 5 of 10; about 44% of core time elapsed. |
| Technical pipeline | More than halfway | Core CLI, exports, reports, summaries, tests, and paper artifact generators exist. |
| Evidence quality for current-five | More than halfway | Current-five screenshots and summary tables exist; interpretation is documented. |
| Sample size / dataset | Less than halfway | 5 current targets versus planned about 20 deep sites. |
| Presentation writing | Less than halfway | Evidence summaries and writing support exist, but the final slide story is not built. |
| Poster/demo | Less than halfway | Poster plan exists, but final poster/demo are not built. |

Overall: this is a midpoint project with a strong infrastructure base and a
clear evidence gate, but the current presentation/poster deliverable is now
bottlenecked by human decisions, sample framing, and final visual/story
assembly, not by writing more scaffolding.

## Critical Path For The Remaining Month

The next month should not be spent making more disconnected docs. It should
follow this order:

1. Merge or review PR #8 so the project state handoff is in `main`.
2. Send or adapt `docs/research/advisor_email_decision_gate_2026-06-28.md`.
3. Record the answers in
   `data/current_five_decision_sheet_2026-06-19.csv`.
4. Decide the next work mode:
   - manual validation/reporting of the current five,
   - post-fix current-five rerun,
   - expansion toward about 20 deep sites,
   - or CMP/manual-review resolution first.
5. If expanding, prioritize banner-present/control evidence sites and keep
   no-visible-banner cases explicitly labeled as contrast cases.
6. Refresh RQ1/RQ2 tables after any successful new capture.
7. Turn the existing poster plan, figure plan, and writing support notes into a
   final presentation/poster story by Week 9-10.

## Safe Claims Right Now

- The Week 2 five-site evidence gate completed and sanity is `ready`.
- The project has 42 audit reports and 20 longitudinal summaries in the current
  research package.
- The current five should be interpreted as 2 banner/control evidence cases and
  3 no-visible-banner contrast candidates unless the advisor decides otherwise.
- The current repo syncs screenshot PNG evidence, but raw `layer1.html` files
  are not synced in this checkout.
- The project is in Week 5 of the 10-week core cycle and is not final
  presentation/poster complete.

## Claims Not To Make

- Do not say the final SSRP dataset is complete.
- Do not say the 20-site deep sample is locked.
- Do not say all five current sites are banner-path failures.
- Do not say raw DOM HTML snapshots are synced in the repo.
- Do not say the presentation/poster are final.
