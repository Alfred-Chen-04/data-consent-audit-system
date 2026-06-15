# Today Work Note, 2026-06-11

## Bottom Line

Today is a review-and-organization day, not a new browser-capture day.

The current evidence package is already healthy:

- Week 2 cycle status: `completed`
- Week 2 sanity status: `ready`
- Research package: 42 audit reports and 20 longitudinal summaries
- Week 2 manual review: 5/5 rows have screenshot-grounded draft coding
- CMP/manual-review queue: 8 rows still pending advisor or human confirmation

The next live capture should wait until the target-list decision is clearer.
The current plan is to run the next weekly capture around 2026-06-13 only after
deciding whether to rerun the current five sites or switch to an adjusted /
expanded target list.

## What Was Checked Today

Commands run:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-preflight-check
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-sanity-check
```

Current status after the check:

- `research-status` reports preflight `ready_for_capture`, sanity `ready`,
  cycle capture `completed`, 42 audit reports, 20 longitudinal summaries, and
  8 CMP confirmations pending.
- `week2-preflight-check` regenerated successfully.
- `week2-sanity-check` regenerated successfully.

Note: use `PYTHONPATH=src` when running module commands from the local checkout.
Without it, Python may not find `consent_audit.cli` unless the package is
installed editable in the current environment.

## What To Do Today

1. Use the latest advisor email draft if contacting Dr. Singh:
   `docs/research/advisor_email_latest_update_2026-06-10.md`.
2. Use the manual evidence notes as the current evidence interpretation:
   `docs/research/week2_manual_evidence_review_notes_2026-06-10.md`.
3. Treat The Guardian and Coca-Cola as the two strongest banner-present evidence
   cases.
4. Treat CNN, Booking.com, and NerdWallet as no-visible-banner contrast
   candidates, not as banner-path failures.
5. Do not run a new live weekly capture today unless the target-list decision
   changes.

## Daily Routine

On normal days, do not rerun the full browser capture automatically.

Recommended daily check:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

Run the heavier checks only when preparing to capture, email the advisor, or
freeze a paper/poster artifact:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-preflight-check
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-sanity-check
```

Run live browser capture only on a planned capture day:

```bash
AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-cycle
```

Before the next live capture, decide:

- rerun the current five sites for continuity; or
- adjust/expand the target list toward the roughly 20-site deep sample.

## Waiting On Advisor Or Human Decision

The project does not need more blind automation today. It needs decisions on:

1. how no-visible-banner contrast cases should appear in the final RQ1 table;
2. whether to write five evidence cards first or expand immediately;
3. whether the expansion should prioritize banner-present sites with visible
   controls;
4. whether the next weekly capture around 2026-06-13 should rerun the current
   five sites or use an adjusted target list.
