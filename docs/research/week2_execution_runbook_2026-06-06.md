# Week 2 Execution Runbook, 2026-06-06

This runbook is the operational checklist for the first scheduled Week 2
capture cycle. It assumes the sample-freeze note in
`docs/research/week2_sample_plan_2026-05-30.md` is still the working default.

## Goal

Capture the 5 frozen Week 2 sites, refresh the paper-facing exports, and keep
the 8 pending CMP/manual-review rows separate from locked sample decisions until
human confirmation.

## Inputs

- Week 2 target list: `data/week2_deep_sample_targets_2026-06-06.csv`
- Running consent table: `data/consent_table_pilot_2026-05-30.csv`
- Audit report store: `data/reports/audit_reports.jsonl`
- Weekly summary store: `data/reports/weekly_summaries.jsonl`
- CMP decision draft: `data/cmp_review_decision_draft_pilot_2026-05-30.csv`
- CMP confirmation sheet: `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
- CMP evidence packet: `data/cmp_review_packet_pilot_2026-05-30/index.html`

## Preflight

Run from the repository root.

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-capture-targets
PYTHONPATH=src .venv/bin/python -m consent_audit.cli validate-sites \
  --sites-csv data/week2_deep_sample_targets_2026-06-06.csv
PYTHONPATH=src .venv/bin/python -m consent_audit.cli cmp-review-decision-draft
PYTHONPATH=src .venv/bin/python -m consent_audit.cli cmp-review-confirmation-sheet
PYTHONPATH=src .venv/bin/python -m consent_audit.cli advisor-update-brief
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-sanity-check
PYTHONPATH=src .venv/bin/python -m consent_audit.cli checkin-index
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-preflight-check
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-refresh-outputs
```

Expected validation summary:

```text
5 active sites; mentor_inherited=0; categories: finance=1, food=1, news=2, travel=1
```

The preflight check is written to
`docs/research/week2_preflight_check_2026-06-06.md`. Before the scheduled
capture, its overall status should be `ready_for_capture`. If it says
`needs_attention`, fix the missing file, target-list issue, manifest count, or
sanity state before opening the browser pipeline.

## Weekly Capture

Run on or after 2026-06-06.

Dry-run the full cycle first:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-cycle --dry-run
```

The dry run reruns the preflight gate and writes
`docs/research/week2_cycle_report_2026-06-06.md`, but it does not open browser
capture or refresh the research package. Use it to confirm paths and status
before starting the live capture. In dry-run mode, the report should show
`Cycle mode: dry_run`, `Capture attempts: 0/5`, and
`Capture successes: 0/5`.

Preferred one-command cycle:

```bash
AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-cycle
```

This command reruns the preflight gate, stops before browser capture if the
preflight status is not `ready_for_capture`, runs the 5-site weekly capture, and
then refreshes the research package, advisor brief, sanity check, check-in
index, preflight check, and refresh report. Only use `--force` after recording
why the preflight warning is acceptable.

The command records capture attempts, successes, and failures in
`docs/research/week2_cycle_report_2026-06-06.md`. If 2 or more of the 5 target
sites fail, the cycle report marks capture status as `needs_attention`. The
report also records the target-list path, consent-table path, cohort, expected
target count, force flag, and dry-run flag so the run can be reconstructed
without rereading the shell history. Read the report's `Next Action` section
before starting a live capture or declaring the cycle complete.

Manual equivalent:

```bash
AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m consent_audit.cli weekly \
  --sites-csv data/week2_deep_sample_targets_2026-06-06.csv \
  --consent-table-path data/consent_table_pilot_2026-05-30.csv \
  --cohort week2-2026-06-06
```

Use the existing pilot consent table until the advisor locks a final sample
name. The row timestamp and cohort identify the Week 2 observation, while the
JSONL report store remains the authoritative longitudinal history.

## Export Refresh

After capture, refresh the paper-facing tables.

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-refresh-outputs
```

The refresh command runs the export sequence in the safe order:
`export-research-package`, `advisor-update-brief`, `week2-sanity-check`,
`checkin-index`, and `week2-preflight-check`. The advisor brief and sanity check
read from the freshly written `data/research_package/` CSVs, which avoids stale
root-level summary files.

Check the new counts:

```bash
wc -l data/consent_table_pilot_2026-05-30.csv
wc -l data/reports/audit_reports.jsonl
wc -l data/reports/weekly_summaries.jsonl
```

If all 5 sites capture successfully, expect 5 new consent-table rows, 5 new
`AuditReport` rows, and up to 5 new `WeeklySummary` rows. A no-change weekly
summary is still valid and should be kept as stability evidence.

The advisor update brief is written to
`docs/research/week2_advisor_update_2026-06-06.md`. It summarizes target count,
research-package counts, latest target outcomes, longitudinal severity/event
counts, and CMP confirmation status.

The Week 2 sanity check is written to
`docs/research/week2_sanity_check_2026-06-06.md`. It verifies whether each of
the 5 frozen targets has a consent-table row for cohort `week2-2026-06-06`,
complete screenshot/DOM/hash evidence, a matching audit-report row, and a
weekly summary for the expected week.

The advisor check-in index is written to
`docs/research/week2_checkin_index_2026-06-06.md`. Use it as the first file for
advisor review because it links the brief, sanity check, runbook, research
package, capture-day checklist, cycle report, CMP confirmation sheet, and CMP
evidence packet. Its Run Controls section now lists the capture-day command
order: preflight, dry run, live `week2-cycle`, refresh, checklist refresh, and
advisor-facing exports.

The capture-day checklist is written to
`docs/research/week2_capture_day_checklist_2026-06-06.md`. It is the
operator-facing checklist for the weekly run and records current preflight,
sanity, and last-cycle status next to the exact commands and evidence gates.
`week2-cycle` rewrites it after writing the final cycle report, so the checklist
reflects the latest dry-run, abort, or live capture status rather than the
pre-cycle report state.

The refresh report is written to
`docs/research/week2_refresh_report_2026-06-06.md`. It records the refreshed
research-package counts and the resulting sanity/preflight statuses.

The full-cycle report is written to
`docs/research/week2_cycle_report_2026-06-06.md` when `week2-cycle` is used. It
records the pre-capture preflight status, capture status, refreshed counts, and
post-refresh sanity/preflight statuses. It also lists failed URLs and error
messages when a site-level capture fails. In `--dry-run` mode, the report
records that browser capture and refresh were skipped. The `Inputs` section is
the authoritative record of which target list, consent table, cohort, expected
target count, force flag, and dry-run flag were used. The `Next Action` section
is the operational handoff for what to do after the report is written.

## Advisor Review

Use the CMP packet and decision draft as review material only:

- Open `data/cmp_review_packet_pilot_2026-05-30/index.html`.
- Review `data/cmp_review_decision_draft_pilot_2026-05-30.csv`.
- Fill `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` by changing
  `confirmation_status` to `confirmed` only after advisor review and putting
  the final decision in `confirmed_decision`.
- Confirm whether no-banner contrast cases belong in the methods section.
- Decide whether Reddit and Walmart should be replaced immediately.

Do not promote CMP decision-draft rows into the locked deep sample until the
worksheet has human-confirmed decisions.

When at least one row is confirmed, apply the confirmations to a worksheet copy:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli cmp-review-apply-confirmations
PYTHONPATH=src .venv/bin/python -m consent_audit.cli sample-lock-plan \
  --worksheet-csv data/cmp_review_worksheet_confirmed_pilot_2026-05-30.csv
PYTHONPATH=src .venv/bin/python -m consent_audit.cli sample-action-queues
```

Expected behavior before advisor review: the confirmation sheet has 8 pending
rows, so applying it should not select or replace any CMP row.

## Stop Conditions

- Stop and record the failure if 2 or more of the 5 Week 2 sites fail capture.
  `week2-cycle` reports this as `Capture status: needs_attention`.
- Stop sample expansion if the capture output cannot preserve screenshot, DOM,
  visible-text hash, and path-outcome evidence for each score.
- If the Week 2 run succeeds but advisor review is still pending, continue
  weekly capture on the frozen 5-site list and keep the 8 CMP rows out of locked
  sample counts.
