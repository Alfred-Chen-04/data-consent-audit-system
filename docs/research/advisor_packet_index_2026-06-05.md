# Advisor Packet Index, 2026-06-05

This is the one-file entrypoint for communicating the current SSRP consent
interface audit status to Dr. Singh after his June 5 guidance.

## What Can Be Sent Today

After the successful June 6 live capture, June 8 no-visible-banner review, June
28 fact audit, and July 1 scope update, use this draft as the current advisor
email:

- `docs/research/advisor_email_scope_update_2026-07-01.md`

The current scope note is:

- `docs/research/current_scope_2026-07-01.md`

The June 28 decision-gate email is now historical because it still treated a
formal SSRP paper as a current summer deliverable:

- `docs/research/advisor_email_decision_gate_2026-06-28.md`

The older June 8 next-step draft remains useful background, but it is no longer
the current sendable email:

- `docs/research/advisor_email_next_step_draft_2026-06-08.md`

The fuller post-capture evidence draft remains available if a longer update is
needed:

- `docs/research/advisor_email_post_capture_draft_2026-06-06.md`

The earlier June 5 draft remains useful only as a pre-capture process update:

- `docs/research/advisor_email_draft_2026-06-05.md`

The June 6 draft is intentionally evidence-based. It reports the 5/5 completed
capture, `ready` sanity gate, RQ1/RQ2 result snapshot, pending CMP confirmations,
and follow-up questions for sample expansion.

## What Was Waiting Until After Capture

This template has now been superseded by the filled June 6 draft above:

- `docs/research/post_capture_advisor_update_template_2026-06-06.md`

## Decisions Confirmed By Advisor

| Area | Confirmed direction | Implementation in project materials |
|---|---|---|
| Research questions | Current RQ framing is on track. | Keep RQ1 scoring and RQ2 longitudinal capture/versioning as the presentation/poster research spine. |
| No-banner cases | Treat them as contrasts. | Use clean repeated no-banner observations as contrast cases, not failed samples. |
| Sample scale | Deep analysis of fewer sites is appropriate if scalable. | For the current presentation/poster, decide whether to stay with the five-site evidence gate or expand toward more banner-present examples; keep the 80-ish list as a lightweight tracker/candidate pool. |

The project-level implementation is recorded in:

- `docs/research/advisor_response_action_plan_2026-06-05.md`
- `docs/research/week2_sample_plan_2026-05-30.md`
- `docs/research/advisor_guideline_alignment_audit_2026-06-05.md`

## Current Facts To Report

These facts are current as of the latest 2026-07-01 scope update and
`research-status` check:

- Week 2 targets: 5
- Categories: finance=1, food=1, news=2, travel=1
- Preflight status: `ready_for_capture`
- Sanity status: `ready`
- Cycle capture status: `completed`
- Audit reports in package: 42
- Longitudinal summaries in package: 20
- Week 2 banner evidence classes: banner_present=2, no_visible_banner=3
- Banner-present automated tiers: High-Risk=2
- Raw automated target tiers: High-Risk=5, but no-visible-banner rows should not be claimed as banner-path failures without a coding decision
- CMP confirmations: pending=8
- Current-five decision sheet: 7 blank `confirmed_decision` cells
- PR #8 status: open draft PR, not merged, mergeable
- Current summer deliverables: presentation + large poster + traceable
  evidence package; a formal paper is not required for the current summer
  scope unless Dr. Singh reintroduces it later
- Presentation/poster support artifacts present: claim register, figure plan,
  optional future-paper skeleton, poster plan, results tables, writing pack

The current Week 2 target list is:

- The Guardian
- CNN
- Booking.com
- NerdWallet
- Coca-Cola

## What Not To Claim Yet

Do not claim these yet:

- The Week 2 five-site gate is the final SSRP dataset.
- CNN, Booking.com, or NerdWallet are banner-path failures; they are currently no-visible-banner contrast candidates.
- The 20-site deep sample is locked.
- The 80-ish tracker is operational.
- No-banner contrast rows have final table treatment.
- Qiyao-derived rows are approved for public release or publication.

## Open Questions For Dr. Singh

The current July 1 email draft asks these decision questions:

1. Confirm, rerun, or replace The Guardian and Coca-Cola as banner-present
   evidence-card rows.
2. Keep CNN, Booking.com, and NerdWallet as separate no-visible-banner contrast
   rows, move them into the main RQ1 table with a clear label, rerun them, or
   replace them.
3. Choose the next work block: current-five rerun, manual validation then
   expansion, banner-present expansion first, or CMP/manual-review resolution
   first.
4. Confirm whether the presentation/poster should stay centered on the
   five-site evidence gate or expand toward more banner-present examples.
5. Confirm that a formal paper is not part of the current summer deliverable.

## Current Work Order

After the completed June 6 evidence gate:

1. Review the refreshed sanity check and advisor index:

   ```bash
   PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
   ```

2. Send or discuss the current decision-gate email:

   - `docs/research/advisor_email_scope_update_2026-07-01.md`

3. Keep the 8 CMP/manual-review rows separate from locked sample decisions.

4. Expand beyond the current five-site evidence gate only after deciding:

   - how many clean no-banner contrast rows to include;
   - which access-friction rows to replace;
   - whether the next advisor update should use compact tables or evidence cards.
