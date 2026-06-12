# June 13 Capture Decision Packet

## Purpose

This packet records what can safely be done on 2026-06-13 before the next live
browser capture. It avoids a blind capture run while still keeping the project
ready to collect the next longitudinal observation.

## Current State

- Current date: 2026-06-13
- Current Week 2 evidence gate: complete
- Sanity status: `ready`
- Cycle status: `completed`
- Research package: 42 audit reports and 20 longitudinal summaries
- Current Week 2 targets: The Guardian, CNN, Booking.com, NerdWallet, Coca-Cola
- Current screenshot-grounded split:
  - banner-present manual-review cases: The Guardian, Coca-Cola
  - no-visible-banner contrast candidates: CNN, Booking.com, NerdWallet
- CMP/manual-review rows still pending: 8

## Decision

Do not run a live browser capture blindly today unless the target-list rule is
accepted.

The safest default is:

1. keep the current five-site list as the continuity target list;
2. wait for the advisor's answer on no-visible-banner representation and sample
   expansion before changing the list;
3. if a capture must run today for weekly continuity, run the current five
   sites and label the cohort as `week3-2026-06-13`;
4. do not add IKEA, IBM, or Intuit to the live weekly list yet; they are
   promising reprobe candidates, not locked deep-sample targets.

## Prepared Target List

Prepared continuity target CSV:

`data/week3_continuity_targets_2026-06-13.csv`

This file intentionally repeats the current five Week 2 sites. It is meant for
continuity, not final sample expansion.

## If Running The Capture

Use this only after deciding to prioritize longitudinal continuity over waiting
for target-list changes:

```bash
AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m consent_audit.cli weekly \
  --sites-csv data/week3_continuity_targets_2026-06-13.csv \
  --consent-table-path data/consent_table_pilot_2026-05-30.csv \
  --cohort week3-2026-06-13
```

After a live capture, refresh paper/advisor artifacts:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-refresh-outputs
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

## If Waiting

If waiting for advisor response, today's useful work is complete once these
items exist:

- the sendable advisor question email:
  `docs/research/advisor_email_review_questions_2026-06-11.md`
- the continuity target list:
  `data/week3_continuity_targets_2026-06-13.csv`
- this decision packet:
  `docs/research/june13_capture_decision_packet_2026-06-13.md`

## Open Questions For Advisor

The next capture list depends on these answers:

1. Should no-visible-banner cases stay in the main RQ1 table, be capped as a
   small contrast group, or move to a separate limitations/contrast table?
2. Should the project first finish evidence cards for the current five sites or
   immediately expand toward the roughly 20-site deep sample?
3. Should expansion prioritize visible banner/control evidence, even if that
   means replacing no-visible-banner or access-friction candidates?
4. Should the next weekly capture rerun the current five for continuity, or wait
   for an adjusted list?
5. Should the 8 pending CMP/manual-review rows be resolved now or treated as
   secondary candidates?

## Recommendation

Send the advisor email first. If no response arrives and a weekly observation is
needed for continuity, run the prepared current-five target list rather than
mixing in unconfirmed candidates.
