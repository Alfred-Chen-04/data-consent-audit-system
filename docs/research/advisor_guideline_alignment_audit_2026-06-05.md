# Advisor Guideline Alignment Audit, 2026-06-05

This audit checks whether the project is still following Dr. Singh's June 5
guidance. It uses the current worktree and `research-status` output as the
authoritative state.

## Bottom Line

The project is moving in the correct direction. The current work follows the
advisor guidance: keep the RQ1/RQ2 paper spine, treat no-banner observations as
contrast cases, prioritize a smaller deep sample, and keep the broader 80-ish
list as a scaling pool rather than the immediate main sample.

The main thing not to do after the June 6 capture is overclaim. The Week 2
evidence gate is complete for 5/5 targets, but this is still the first evidence
gate, not the final roughly 20-site deep sample or final SSRP dataset.

## Guideline Audit

| Advisor guideline | Current alignment | Evidence | Guardrail |
|---|---|---|---|
| Keep the current RQ framing. | Aligned | `SCHEMA.md` freezes RQ1 scoring and RQ2 longitudinal capture/versioning; `docs/research/advisor_response_action_plan_2026-06-05.md` keeps the same spine. | Do not introduce AI, SOC 2, or policy-text auditing as a new RQ. |
| Treat no-banner cases as contrasts. | Aligned | `docs/research/week2_sample_plan_2026-05-30.md` and the advisor response action plan both say clean repeated no-banner rows are contrast cases. | Do not score no-banner rows as failed banner-present flows. |
| Favor deeper analysis of fewer sites. | Aligned | The frozen Week 2 gate uses 5 sites; the plan expands toward about 20 deep sites only after the evidence gate is stable. | Do not jump to the 80-ish list before the 5-site capture/sanity check works. |
| Keep scalability visible. | Aligned | The 80-ish/Qiyao-derived list is described as a lightweight tracker or candidate pool, subject to provenance/release constraints. | Do not claim the 80-ish tracker is operational or approved for publication yet. |
| Communicate concrete evidence next. | Aligned | `advisor_email_post_capture_draft_2026-06-06.md` reports site-level capture results, sample logic, and paper structure from the completed Week 2 gate. | Keep claims tied to sanity/source evidence refs. |

## Current State Checked

Latest dashboard state:

- Week 2 targets: 5
- Preflight status: `ready_for_capture`
- Sanity status: `ready`
- Cycle capture status: `completed`
- Audit reports in package: 42
- Longitudinal summaries in package: 20
- CMP confirmations: pending=8

Current Week 2 targets:

- The Guardian
- CNN
- Booking.com
- NerdWallet
- Coca-Cola

## Direction Risks

These are the places where the project could drift if we are not careful:

1. Treating the 5-site Week 2 evidence gate as the final 20-site SSRP sample.
2. Expanding too early from 5 targets to the 80-ish tracker.
3. Letting SOC 2/GRC become the main research frame.
4. Mixing access-friction cases such as Reddit/Walmart with clean no-banner
   contrast cases.
5. Sending unsupported site-specific claims without screenshot/DOM/report refs.

## Correct Next Step

Do not change the research direction after the successful capture. Current next
step:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

Then use `docs/research/advisor_email_post_capture_draft_2026-06-06.md` as the
evidence-based advisor update.
