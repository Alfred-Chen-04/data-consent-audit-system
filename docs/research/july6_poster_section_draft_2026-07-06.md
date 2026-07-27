# July 6 Poster Section Draft, 2026-07-06

Purpose: turn the verified project state into poster/presentation sections that
can be used now without overstating the evidence.

This draft adds no new browser capture and no new consent-interface evidence.
It uses the current evidence state checked on 2026-07-06.

## Current Facts Used

- Date: 2026-07-06.
- Core research window: May 30-August 7, 2026.
- Calendar progress: 38 of 70 core-cycle days, or 54.3%.
- Days left before August 7 core deadline: 32.
- Days left before August 31 polish deadline: 56.
- PR #8: open, draft, mergeable, not merged into `main`.
- Local branch and upstream: `dfa1d437aa7413fc4072fe50a4f95fd9ed565284`.
- `research-status`: preflight `ready_for_capture`, sanity `ready`, cycle
  capture `completed`.
- Research package: 42 audit reports and 20 longitudinal summaries.
- Banner-detected counts in `audit_report_summary.csv`: true=9, false=33.
- Screenshot evidence: 326 site `layer1.png` files; 0 synced site
  `layer1.html` raw DOM files.
- Current-five decision sheet: 7 rows, 7 blank decisions.
- CMP/manual-review confirmation sheet: 8 rows, 8 pending confirmations.

## Poster Title Draft

Traceable Consent Interface Audit and Versioning

## One-Sentence Poster Claim

This project develops a computational audit and versioning workflow for website
consent interfaces: RQ1 scores whether layered consent pathways support
unbiased choice, while RQ2 captures and compares interface evidence over time.

## Research Questions Section

RQ1: How can layered consent interfaces be scored for unbiased choice across
the full consent pathway?

RQ2: How can privacy and consent interfaces be captured and versioned over time
to document interface change?

## Method Section

Workflow:

1. Capture website evidence: screenshot, DOM reference/hash, visible text,
   interaction attempts, and event metadata.
2. Score the consent pathway through layered rules:
   - Layer 1: path availability.
   - Layer 2: path effort.
   - Layer 3: transparency and unbiased-choice framing.
3. Export an `AuditReport` with evidence refs.
4. Repeat captures over time.
5. Compare screenshots, DOM hashes, text, and pathway outputs to produce
   longitudinal summaries.

Poster-safe wording:

> The system treats screenshots, DOM refs, hashes, visible text, and interaction
> logs as evidence inputs. Final grades are deterministic after extraction and
> schema validation; model outputs are not accepted as unsupported final scores.

## Current Evidence Snapshot Section

Use this as the current evidence box:

| Item | Current verified count |
|---|---:|
| Week 2 target sites | 5 |
| Audit reports in research package | 42 |
| Longitudinal summaries | 20 |
| Site `layer1.png` screenshots | 326 |
| Synced site `layer1.html` raw DOM files | 0 |
| Current-five blank decisions | 7 |
| CMP/manual-review pending confirmations | 8 |

## Evidence Card Section

Use two banner-present evidence cards:

1. The Guardian
   - Evidence class: `banner_present`.
   - Poster role: example of a visible choice interface.
   - Safe claim: screenshot evidence shows a visible Guardian consent-choice
     screen.

2. Coca-Cola
   - Evidence class: `banner_present`.
   - Poster role: example of a visible preference-center interface.
   - Safe claim: screenshot evidence shows a visible Privacy Preference Center
     with consent controls.

Use three contrast cases:

1. CNN
   - Evidence class: `no_visible_banner`.
   - Safe claim: stored screenshot shows the CNN homepage with no visible
     first-screen cookie banner.

2. Booking.com
   - Evidence class: `no_visible_banner`.
   - Safe claim: stored screenshot shows the Booking.com homepage/search UI
     with no visible first-screen cookie banner.

3. NerdWallet
   - Evidence class: `no_visible_banner`.
   - Safe claim: stored screenshot shows the NerdWallet homepage/product UI
     with no visible first-screen cookie banner.

Important label:

> No-visible-banner contrast cases are not banner-path failures. They require a
> separate table label or advisor decision before final scoring claims.

## Findings So Far Section

Use this wording:

> The pilot evidence shows that a single pipeline can support both proposal
> questions: RQ1 scoring outputs and RQ2 longitudinal summaries can be generated
> from the same evidence bundle. Current results are pilot evidence, not a final
> 20-site dataset.

Current pilot observations:

- The project has evidence-linked audit-report exports.
- The project has longitudinal-summary exports.
- Screenshot evidence is synced to the PR branch.
- Screenshot review is necessary because no-visible-banner cases should not be
  counted as banner-path failures without a separate coding rule.

## Limitations Section

Use this wording:

> The current poster should be read as a pilot and methods demonstration. Raw
> `layer1.html` files are not synced in this checkout; current-five decisions
> remain blank; CMP/manual-review confirmations are pending; and PR #8 is not
> merged into `main`. The current evidence supports method and traceability
> claims, not final compliance conclusions.

Do not claim:

- The final dataset is complete.
- The 20-site sample is locked.
- Raw HTML files are synced.
- CNN, Booking.com, or NerdWallet are banner-path failures.
- Any site is legally compliant or non-compliant.
- PR #8 is merged into `main`.

## Next-Step Section

Recommended next steps:

1. Review or merge PR #8 so the current scope and evidence-audit docs are on
   `main`.
2. Resolve the 7 current-five decision rows.
3. Resolve or label the 8 CMP/manual-review rows.
4. Decide whether the final poster stays as a careful five-site pilot/method
   poster or expands toward more banner-present examples.
5. Run more live capture only after the current-five and no-visible-banner
   treatment decisions are recorded.

## What Can Be Built Today

The poster can now safely include:

- a research-question panel;
- a pipeline/method panel;
- a current evidence snapshot table;
- two banner-present evidence cards;
- a no-visible-banner contrast panel;
- a limitations panel;
- a next-step panel.

The poster should not yet include:

- final sample-wide findings;
- final 20-site result tables;
- final legal/compliance claims;
- raw-HTML evidence claims;
- unqualified no-visible-banner failure claims.
