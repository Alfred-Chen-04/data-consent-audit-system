# Sample Strategy

## Default Strategy

Use a focused deep sample first. The August paper can succeed with approximately 20 well-documented websites if each site has traceable captures, scoring evidence, and at least a few weekly observations.

## Phased Sample Plan

| Phase | Size | Purpose | Exit Criteria |
|---|---:|---|---|
| Smoke canaries | 6 | Verify browser access, screenshots, and basic banner detection. | Capture succeeds or failure reason is recorded. |
| Pilot sample | 10-15 | Exercise Layer 1 and consent-table recording across varied sites. | Consent table rows are complete and reviewed. |
| Deep sample | ~20 | Main SSRP analysis sample. | Weekly capture and full scoring are stable enough for paper tables. |
| Broad tracker | 80+ optional | Lightweight longitudinal monitoring if time permits. | Only pursue after deep sample is stable. |

## Current Pilot Candidate Table

The current pilot review table is `data/deep_sample_candidates.csv`. It contains
15 public unauthenticated desktop candidates across news, social, ecommerce,
travel, entertainment, finance, and reference/control categories.

Current supporting artifacts:

- `data/access_probe_pilot_2026-05-30.csv`
- `data/sample_readiness_pilot_2026-05-30.csv`
- `data/cmp_review_queue_pilot_2026-05-30.csv`
- `data/cmp_review_worksheet_pilot_2026-05-30.csv`
- `data/cmp_review_packet_pilot_2026-05-30/`
- `data/cmp_review_suggestions_pilot_2026-05-30.csv`
- `data/cmp_review_decision_draft_pilot_2026-05-30.csv`
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
- `data/cmp_review_rerun_targets_pilot_2026-05-30.csv`
- `data/sample_lock_plan_pilot_2026-05-30.csv`
- `data/sample_action_queues_pilot_2026-05-30/`
- `data/deep_sample_weekly_targets_pilot_2026-05-30.csv`
- `data/replacement_review_batch2_2026-05-30.csv`
- `data/deep_sample_weekly_targets_expanded_2026-05-30.csv`
- `data/week2_deep_sample_targets_2026-06-06.csv`
- `data/audit_report_summary.csv`
- `data/longitudinal_summary.csv`
- `data/research_package/`
- `docs/research/cmp_manual_review_brief_2026-05-30.md`
- `docs/research/replacement_probe_brief_2026-05-30.md`
- `docs/research/replacement_probe_batch2_brief_2026-05-30.md`
- `docs/research/expanded_weekly_capture_brief_2026-05-30.md`
- `docs/research/week2_sample_plan_2026-05-30.md`
- `docs/research/week2_execution_runbook_2026-06-06.md`
- `docs/research/week2_advisor_update_2026-06-06.md`
- `docs/research/week2_sanity_check_2026-06-06.md`
- `docs/research/week2_checkin_index_2026-06-06.md`
- `docs/research/week2_preflight_check_2026-06-06.md`
- `docs/research/week2_refresh_report_2026-06-06.md`

As of the May 30 pilot probe, Booking.com fallback rerun, and CMP
fresh-context rerun, the readiness table shows:

- `pilot_ready=4`
- `needs_weekly_capture=0`
- `needs_cmp_review=8`
- `control_candidate=1`
- `access_blocked=2`

The blocked candidates should be reviewed before locking the deep sample; keep
them only if they are useful access-feasibility canaries.

After the first pilot weekly capture, 7 of 8 weekly target sites wrote consent
table rows. Booking.com initially failed during dynamic page navigation, then
the DOM fallback rerun produced a traceable screenshot, DOM snapshot,
consent-table row, and `AuditReport`.

The CMP/manual review queue contains the 8 `needs_cmp_review` sites with
access-probe screenshot refs, weekly capture screenshot/DOM refs, hashes, and a
recommended manual review action. Use it to decide whether each row is a true
no-banner case, a region/browser-context artifact, or a site to replace before
locking the deep sample.

The CMP/manual review worksheet is the fillable decision layer for those 8 rows.
It keeps the evidence refs and adds blank manual fields for whether a banner was
observed, the CMP/vendor if visible, sample decision, reviewer, review date, and
notes. Valid sample decisions are `keep_consent_sample`,
`keep_no_banner_case`, `rerun_fresh_context`, `replace_candidate`, and
`exclude`.

The CMP/manual review packet is the visual review layer for the same 8 rows. It
writes `index.html` and `index.md` with access-probe screenshots, weekly-capture
screenshots, DOM links, review reasons, recommended actions, and decision
options so the worksheet can be filled without manually joining CSV columns.

The CMP review suggestions table is a non-final triage layer. It reads saved DOM
snapshots for configured CMP indicators and recommends a worksheet decision for
review. Current automatic suggestions are `rerun_fresh_context=7` and
`keep_no_banner_case=1`; every row still requires human confirmation before it
should be copied into the worksheet.

The CMP review decision draft turns the review brief into a human-confirmable
decision table. It currently drafts `keep_no_banner_case=6` for BBC, New York
Times, Amazon, Airbnb, Spotify, and Chase, and `replace_candidate=2` for Reddit
and Walmart. Every row has `requires_human_confirmation=true`; these are advisor
review prompts, not locked sample decisions.

The CMP review confirmation sheet is the gate between draft advice and sample
lock. It currently has 8 `pending` rows and blank `confirmed_decision` fields.
Only rows changed to `confirmation_status=confirmed` should be applied back to a
worksheet copy with `cmp-review-apply-confirmations`, after which
`sample-lock-plan` can regenerate the lock statuses from human-confirmed
decisions.

The CMP review rerun targets file converts only the `rerun_fresh_context`
suggestions into a normal weekly site-list CSV. It currently contains 7 targets
for fresh-context capture: BBC, New York Times, Amazon, Walmart, Airbnb,
Spotify, and Chase. Reddit is excluded because the suggestion artifact currently
classifies it as a possible no-banner case rather than a rerun target.

The fresh-context CMP rerun completed for all 7 target sites. It appended new
consent-table rows and weekly summaries, but still did not observe visible
consent banners in the current browser/location context. These rows should
remain in manual CMP review rather than being automatically promoted into the
deep sample.

The CMP manual review brief summarizes the 8 pending sites for advisor/human
decision-making. It flags Reddit and Walmart as likely replacement/access
friction cases, and frames BBC, New York Times, Amazon, Airbnb, Spotify, and
Chase as no-banner or region/context review candidates rather than
banner-present sample rows.

The first replacement probe tried 12 additional candidates. Weather.com was the
only clear access-probe banner hit, but full weekly capture was not stable enough
to lock it into the deep sample yet. AP News, USA Today, eBay, Best Buy, and
Indeed loaded without banner hits; Forbes and WebMD showed CAPTCHA/block text;
Home Depot, Etsy, Tripadvisor, and Expedia produced hard block/error signals.

The second replacement probe tried 16 additional candidates. Coca-Cola is the
first replacement candidate that reproduced a complete, traceable,
banner-present full audit: Accept, Reject, and Customize paths were detected,
Layer 1 passed, Layer 2 was Easy, Transparency was B, Unbiased Choice was A, and
the final tier was Compliant. IKEA, IBM, and Intuit had access-probe banner hits
but did not stably reproduce visible actionable paths in the weekly pipeline, so
they remain reprobe/context candidates rather than locked sample rows.

The replacement review artifact turns this into a machine-readable promotion
gate. Current status is `verified_replacement=1`, `promising_reprobe=3`,
`no_banner_or_locale_shift=3`, and `blocked_or_error=9`. Only Coca-Cola is
promoted into the expanded weekly target list.

Current paper-facing exports contain 42 audit-report rows and 20 longitudinal
weekly-summary rows. The research package manifest mirrors those counts.

The sample-lock action plan rolls readiness and worksheet decisions into one
table for deciding the deep sample. Current status:

- `provisionally_selected=4`: The Guardian, CNN, Booking.com, NerdWallet
- `pending_manual_review=8`: BBC, New York Times, Reddit, Amazon, Walmart, Airbnb, Spotify, Chase
- `needs_capture_rerun=0`
- `blocked_review_or_replace=2`: Reuters, Netflix
- `optional_control=1`: Wikipedia

The sample action queues split that plan into concrete CSVs:

- `weekly_capture_shortlist.csv`: 4 provisionally selected sites
- `manual_review_queue.csv`: 8 sites needing CMP evidence review
- `rerun_capture_queue.csv`: 0 sites needing another weekly capture attempt
- `replacement_review_queue.csv`: 2 blocked/error sites to review or replace
- `optional_control_queue.csv`: 1 control candidate

The next weekly-capture target list merges `weekly_capture_shortlist.csv` and
`rerun_capture_queue.csv` into a normal site-list CSV. Current targets: The
Guardian, CNN, Booking.com, and NerdWallet.

The expanded weekly-capture target list adds verified replacements after the
replacement review gate. Current expanded targets: The Guardian, CNN,
Booking.com, NerdWallet, and Coca-Cola. This is the recommended next capture
input if advisor confirmation does not reject Coca-Cola on category-balance
grounds.

The first expanded weekly capture completed for all five targets. Later Week 2
evidence changed the latest Coca-Cola interpretation: the latest first-layer
capture has banner/control evidence with Accept observed, but
Reject/Customize/Dismiss were not observed in that first layer. The current
manual review worksheet should be used before treating Coca-Cola as final
sample evidence.

The Week 2 default capture list is frozen at
`data/week2_deep_sample_targets_2026-06-06.csv`. It copies the expanded target
list into a dated Week 2 artifact: The Guardian, CNN, Booking.com, NerdWallet,
and Coca-Cola. It validates cleanly with 5 active sites and category counts
`finance=1`, `food=1`, `news=2`, and `travel=1`.

The Week 2 execution runbook gives the exact capture, export-refresh, count
check, and advisor-review commands for the 2026-06-06 observation cycle. It
keeps the 5 frozen capture targets separate from the 8 CMP decision-draft rows,
so the research can continue collecting longitudinal evidence while sample-lock
decisions remain pending.

The advisor update brief is the compact communication artifact for the next
mentor check-in. It is generated from the current target list, audit-report
summary, longitudinal summary, CMP confirmation sheet, and research-package
manifest; rerun `advisor-update-brief` after each Week 2 capture/export refresh.

The Week 2 sanity check is the post-capture evidence gate. It now records
`ready` for cohort `week2-2026-06-06`: all 5 frozen targets have consent rows,
screenshot/DOM/hash evidence, matching audit-report evidence, and weekly
summaries.

The Week 2 advisor check-in index is the single handoff entrypoint for the
advisor meeting. It links the update brief, sanity check, runbook, research
package CSVs, capture-day checklist, cycle report, CMP confirmation sheet, and
CMP evidence packet, and it records the current sanity status as
`ready`. Its Run Controls section includes the dry-run and live
`week2-cycle` commands so capture-day operators do not have to reconstruct the
sequence from separate notes.

The Week 2 capture-day checklist is generated at
`docs/research/week2_capture_day_checklist_2026-06-06.md`. It is the practical
operator protocol for the first scheduled longitudinal observation: it records
current preflight/sanity/cycle status, links the target list and consent table,
and lists the screenshot/DOM/hash/report evidence gates. The full-cycle command
rewrites the checklist after writing the final cycle report, keeping its
last-cycle fields aligned with the latest dry-run, abort, or live capture
outcome.

The Week 2 preflight check is the machine-readable gate before browser capture.
It currently reports `ready_for_capture`: the frozen target CSV validates with
5 active sites, all required advisor/research artifacts exist, the research
package has 42 audit reports and 20 longitudinal summaries, and the CMP
confirmation sheet still has 8 pending advisor-confirmation rows.

The Week 2 refresh report is generated by `week2-refresh-outputs`, the safe
post-capture refresh command. It refreshes the research package first, then
regenerates the advisor brief, sanity check, check-in index, and preflight check
from the fresh package CSVs.

The full Week 2 cycle command is `week2-cycle`. It is the preferred command on
the scheduled capture day because it runs the preflight gate before browser
capture, stops if the gate is not `ready_for_capture`, captures the frozen
5-site target list, and then runs the refresh orchestrator.

Use `week2-cycle --dry-run` before the live capture. The dry run writes the
cycle report from the current preflight status and skips browser capture and
refresh, so the command path can be checked without changing research counts.
The report keeps the 5-site denominator visible as `0/5` attempts and
successes to distinguish a rehearsal from an empty target list.
Cycle reports also include an `Inputs` section with the target-list path,
consent-table path, cohort, expected target count, force flag, and dry-run flag.
This makes the weekly observation reproducible even if the shell command is not
available later.
The `Next Action` section is the operator-facing checkpoint: dry-run reports can
tell the runner to start live capture, while warning statuses tell the runner to
stop and inspect preflight or capture failures.

The weekly pipeline now returns a structured capture summary. The cycle report
uses it to show target count, attempts, successes, failures, and failed URL/error
pairs. If 2 or more Week 2 targets fail, the cycle status becomes
`needs_attention` rather than quietly treating the run as complete.

## Selection Criteria

- Public unauthenticated desktop websites.
- English-language or English-accessible consent interfaces.
- Varied categories such as news, social, travel, ecommerce, finance, entertainment, and public-interest/reference.
- Likely to present a cookie or privacy consent interface in a fresh browser session.
- Avoid sites where access requires login, payment, or user personal data.

## Core Rule

Do not let the broad 80+ set endanger the paper. If automation is unstable, the project contracts to the deep sample plus a transparent semi-automated protocol.

## SOC 2 Boundary

SOC 2 is not a sample-selection criterion. If mentioned later, it belongs in discussion as possible downstream relevance for privacy evidence readiness, not as the empirical frame.
