# Advisor Packet Index, 2026-06-05

This is the one-file entrypoint for communicating the current SSRP consent
interface audit status to Dr. Singh after his June 5 guidance.

## What Can Be Sent Today

After the successful June 6 live capture and June 8 no-visible-banner review,
use this short next-step draft as the current advisor email:

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
| Research questions | Current RQ framing is on track. | Keep RQ1 scoring and RQ2 longitudinal capture/versioning as the paper spine. |
| No-banner cases | Treat them as contrasts. | Use clean repeated no-banner observations as contrast cases, not failed samples. |
| Sample scale | Deep analysis of fewer sites is appropriate if scalable. | Use about 20 sites as the deep SSRP paper sample and the 80-ish list as a lightweight tracker/candidate pool. |

The project-level implementation is recorded in:

- `docs/research/advisor_response_action_plan_2026-06-05.md`
- `docs/research/week2_sample_plan_2026-05-30.md`
- `docs/research/advisor_guideline_alignment_audit_2026-06-05.md`

## Current Facts To Report

These facts are current as of the latest `research-status` check on 2026-06-08:

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
- Paper artifacts present: claim register, figure plan, paper skeleton, poster plan, results tables, writing pack

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

The current email draft asks these three questions:

1. Should the deep sample include only a small number of clean no-banner contrast
   examples, or should all repeated no-banner observations remain in the main
   sample table with a type label?
2. Should Qiyao's previous 80-ish website list remain an internal candidate
   pool for now, or can it be described in the paper methods as a source for
   scalable coverage?
3. For the next update, is a compact site-level table enough, or should each
   site have an evidence card with screenshot/DOM/report references?

## Current Work Order

After the completed June 6 evidence gate:

1. Review the refreshed sanity check and advisor index:

   ```bash
   PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
   ```

2. Send or discuss the filled advisor update draft:

   - `docs/research/advisor_email_post_capture_draft_2026-06-06.md`

3. Keep the 8 CMP/manual-review rows separate from locked sample decisions.

4. Expand toward the roughly 20-site deep sample only after deciding:

   - how many clean no-banner contrast rows to include;
   - which access-friction rows to replace;
   - whether the next advisor update should use compact tables or evidence cards.
