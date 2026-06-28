# Recent Task Fact Audit, 2026-06-28

## Purpose

This audit checks the recent project-management and research-status documents
for claims that are stale, unsupported, or too final for the evidence currently
in the repository.

The audit uses current files, GitHub PR metadata, local Git state,
`research-status`, and structured CSV reads. It does not add browser capture or
new consent-interface evidence.

## Evidence Checked

| Evidence | Current fact |
|---|---|
| GitHub PR #7 | `open`, `draft=true`, `merged=false`, `mergeable=true` |
| Local branch | `codex/june26-current-state-note` at `6e5e368` before this audit commit |
| Local `main` | `cd02b72b8beee54f3688ed1c14f0d49d270ab79b`, the PR #6 merge commit |
| `research-status` | 5 Week 2 targets; sanity `ready`; cycle `completed`; 42 audit reports; 20 longitudinal summaries; CMP confirmations `pending=8` |
| Current-five decision sheet | 7 rows; 7 blank `confirmed_decision` cells |
| CMP confirmation sheet | 8 rows; 8 `pending`; 8 blank `confirmed_decision` cells |
| Current-five evidence packet | Still labels The Guardian and Coca-Cola as banner-present evidence-card candidates and CNN/Booking.com/NerdWallet as no-visible-banner contrast candidates |
| Results tables / claim register | Separate banner-present automated tiers from raw automated target tiers and keep CMP confirmations as an open limitation |

## Files Reviewed

- `README.md`
- `docs/research/week2_checkin_index_2026-06-06.md`
- `docs/research/advisor_packet_index_2026-06-05.md`
- `docs/research/today_work_note_2026-06-25.md`
- `docs/research/today_work_note_2026-06-26.md`
- `docs/research/today_work_note_2026-06-27.md`
- `docs/research/current_five_evidence_packet_2026-06-19.md`
- `docs/research/advisor_email_current_five_decision_2026-06-19.md`
- `docs/research/ssrp_results_tables_2026-06-06.md`
- `docs/research/ssrp_claim_register_2026-06-06.md`
- `data/current_five_decision_sheet_2026-06-19.csv`
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
- `task_plan.md`
- `findings.md`
- `progress.md`

## Findings

| Item | Result | Evidence / action |
|---|---|---|
| New capture today | Not supported | PR #7 is still open/draft and the decision sheet is still blank, so new capture would not address the known blocker. |
| Current-five decisions | Unresolved | Structured CSV read shows 7 blank `confirmed_decision` cells: 5 site rows and 2 project rows. |
| CMP/manual-review decisions | Unresolved | Structured CSV read shows 8 rows, all `pending`, with 8 blank `confirmed_decision` cells. |
| No-visible-banner rows | Not final main-table failures | Current evidence packet and results tables explicitly treat CNN, Booking.com, and NerdWallet as no-visible-banner contrast candidates. |
| Generated results tables | Evidence-facing, not final-paper decisions | They are useful for drafting and review, but final table treatment still depends on the decision sheet. |
| Advisor packet index | Stale entrypoint | It still pointed at older June 8 advisor questions as the current email. Updated it to the June 28 decision-gate email. |
| README wording | Too final | Changed "paper-ready RQ1/RQ2 results tables" to "paper-facing current-evidence RQ1/RQ2 results tables." |
| CSV counting method | Needs care | A quick `awk -F,` check can misread CSV files with quoted commas. Current counts in this audit use Python `csv.DictReader`. |

## Corrections Made

- Added `docs/research/today_work_note_2026-06-28.md`.
- Added `docs/research/advisor_email_decision_gate_2026-06-28.md`.
- Updated `README.md` to point to the June 28 daily note, June 28 advisor email,
  and this fact audit.
- Updated `docs/research/week2_checkin_index_2026-06-06.md` to put the June 28
  note and advisor email first.
- Updated `docs/research/advisor_packet_index_2026-06-05.md` so the current
  sendable email and current facts no longer stop at June 8.
- Updated planning records with phase 122 and the CSV parsing caution.

## Current Decision Gate

The next research move should be selected only after recording advisor/user
decisions in:

```text
data/current_five_decision_sheet_2026-06-19.csv
```

The latest sendable email draft is:

```text
docs/research/advisor_email_decision_gate_2026-06-28.md
```
