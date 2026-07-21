# July 22 Closeout Audit And Plan, 2026-07-22

## Bottom Line

The remembered "about two weeks" is correct for the project's internal core
closeout date, not for every date mentioned in the repository.

- Original proposal work period: May 18-August 14, 2026.
- Current core execution window: May 30-August 7, 2026.
- Today is day 54 of the 70-day core window: 77.1% of the calendar window.
- 16 calendar days remain before August 7.
- 23 calendar days remain before the original proposal end date, August 14.
- 40 calendar days remain before the August 31 polish date used in current
  planning notes.

This is calendar progress, not a fabricated percentage of research completion.
The project should be managed by deliverable state and open gates instead.

## Current Deliverable State

| Deliverable | Verified state | What prevents "final" |
|---|---|---|
| Presentation | No independent presentation PPTX existed at the start of this audit | A first draft, render review, evidence check, and revision are still required |
| Large poster | Editable 48 x 36 PPTX, one-page PDF, PNG preview, QA note, and verified review ZIP exist | Five poster-review decisions are pending; it remains a review mockup |
| Traceable evidence package | 42 audit-report rows, 20 longitudinal-summary rows, screenshots, review notes, and manifests exist | Raw DOM refs are not present in this checkout; final limitations/manifest freeze remains |
| Formal paper | Internal paper-oriented notes exist | Not a current summer deliverable unless the advisor reintroduces it |

## Evidence Audit

The following counts were read from the current checkout, not inferred from
project prose:

- Frozen Week 2 target list: 5 active sites across finance, food, news, and
  travel.
- Research package: 42 audit-report rows and 20 longitudinal-summary rows.
- Audit-report observation dates: May 29-June 5, 2026.
- Latest `week_of` value in the longitudinal export: June 6, 2026.
- Tracked site screenshots: 326 `layer1.png` files; all parse as 1440 x 900 PNG.
- Synced site raw DOM files: 0 `layer1.html` files.
- Screenshot refs in report export: 42 of 42 resolve to files.
- DOM refs in report export: 0 of 42 resolve to files.
- `report_pdf_ref`: blank in all 42 audit-report rows.
- Poster-review sheet: 5 pending rows and 5 blank confirmed decisions.
- Current-five sheet: 7 rows and 7 blank confirmed decisions.
- CMP/manual-review confirmation sheet: 8 pending rows and 8 blank confirmed
  decisions.

The 42 automated report rows contain 40 `High-Risk` and 2 `Compliant` tier
labels, but these are not safe final findings: 33 rows have
`banner_detected=false`, and the no-visible-banner coding rule remains
unconfirmed. The presentation and poster must not turn those raw labels into a
sample-wide compliance claim.

## Implementation Audit

| Capability | Current fact | Closeout implication |
|---|---|---|
| Browser capture | Playwright capture, screenshots, DOM-derived evidence, deterministic candidate classification/click replay | Can support a pilot methods demonstration |
| Layer scoring | Layer 1/2/3 are executable with deterministic rules | Describe as deterministic pilot scoring |
| LLM/VLM | `llm/text.py` and `llm/vision.py` are no-network fallbacks and are not wired into capture/scoring orchestration | Do not claim active model-powered scoring |
| Persistence | Append-only local JSONL and local sanitized file copies | Do not claim active PostgreSQL/R2 storage |
| Scheduling | CLI/scripts only; no APScheduler implementation found | Do not claim automated weekly production operation |
| Reports | Structured report objects, Markdown, JSON serialization, CSV exports | Do not claim per-report PDF generation |
| Longitudinal operation | Pilot summaries exist through June 6 | Do not claim continuous weekly tracking through July |
| Default site list | `data/sites.csv` is a one-row placeholder and fails validation; Week 2 runs require the explicit frozen target CSV | Keep explicit target-path commands in all run instructions |

The repository has broad automated coverage for the pilot workflow, but test
quantity is not evidence that deferred infrastructure exists. Current entrypoint
documentation has been corrected to separate active runtime from target
architecture.

## Major Omissions Found

### P0: Required Before Core Closeout

1. Build and review the independent presentation deck.
2. Resolve the five poster-review decisions, or visibly carry them as unresolved
   limitations if no advisor response arrives by the review cutoff.
3. Resolve or explicitly label the seven current-five decisions and eight
   CMP/manual-review rows; recommendations must not be copied into confirmed
   fields.
4. Freeze claims around the actual pilot: no final 20-site dataset, no legal
   verdict, no current-July observation, no raw-DOM sync claim, and no active
   external-model claim.

### P1: Required For A Defensible Evidence Package

1. Add a final manifest that distinguishes files present from references only.
2. Decide whether one controlled continuity run is still worth doing. It is
   optional and must answer an approved RQ2 question; it must not delay the
   presentation/poster.
3. Re-render and visually inspect every presentation slide and the final poster.
4. Record the exact final test and Git state in the closeout handoff.

### Deferred Beyond The Current Summer Scope

- External LLM/VLM API integration and benchmarking.
- PostgreSQL/Supabase, R2/S3, in-process scheduling, and hosted demo.
- Final public dataset and broad sample expansion.
- Formal paper prose unless the advisor reintroduces it.

## July 22-August 7 Closeout Plan

| Dates | Work | Exit condition |
|---|---|---|
| July 22-23 | Correct implementation claims; finish audit; build first presentation draft from verified evidence | Current docs distinguish active vs target; deck renders without unsupported claims |
| July 24-26 | Review deck flow and poster together; prepare a single advisor decision packet | Presentation and poster ask the same bounded questions |
| July 27-29 | Record advisor decisions or invoke documented fallback labels | No recommendation is silently treated as confirmation |
| July 30-August 2 | Revise presentation and poster; add only approved evidence/copy | Both artifacts pass content and visual QA |
| August 3-5 | Freeze evidence package, manifest, hashes, limitations, and final status note | Every displayed claim has a present source file or explicit limitation |
| August 6-7 | Rehearse, verify links/tests, make final backup, and freeze core deliverables | Presentation, poster, and evidence ZIP are reviewable from one index |

August 8-14 is contingency and presentation/rehearsal time inside the original
proposal window. August 15-31 is polish only; it should not be used to hide an
unfinished core deliverable.

## Work Completed On July 22

- Audited the original proposal dates, current scope, current goal, roadmap,
  evidence exports, decision sheets, poster files, source modules, tests, and
  Git state.
- Corrected README, SCHEMA, architecture, and source docstrings that could be
  read as claims of active LLM/VLM, PostgreSQL/R2, scheduler, or PDF-report
  behavior.
- Corrected `research-status` so the historical Week 2 cycle action is labeled
  as such and the current July 22 closeout plan is shown separately.
- Created this closeout audit and a source-by-source presentation content plan.
- Built the first independent presentation draft from the five verified stored
  screenshots and current pilot evidence; no new site observation or decision
  was introduced.
- Final verification: 245 tests passed; Ruff passed; Mypy reported no issues in
  61 source files; 161 current-entrypoint local links resolved; presentation
  overflow and final-PPTX visual checks passed.

## Source Trail

- Original schedule and deliverables: `Chen_Qianyi_SSRP 2026_Proposal_Final Version.docx.pdf`, pp. 5-6.
- Current deliverable scope: `docs/research/current_scope_2026-07-01.md`.
- Canonical goal and RQs: `docs/research/current_project_goal_2026-07-02.md`.
- Evidence rows: `data/research_package/audit_report_summary.csv` and
  `data/research_package/longitudinal_summary.csv`.
- Current review gates: `data/poster_review_decision_sheet_2026-07-16.csv`,
  `data/current_five_decision_sheet_2026-06-19.csv`, and
  `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`.
- Poster assets: `docs/research/poster/`.
- Implementation source: `src/consent_audit/` and `scripts/`.
