# SSRP Remaining Work Audit, 2026-05-30

This audit checks the current repository against the SSRP consent-interface audit
plan. It is intentionally conservative: an item is marked complete only when a
current artifact or command output proves it.

## Current State Snapshot

- Week 2 targets: 5
- Categories: finance=1, food=1, news=2, travel=1
- Preflight status: `ready_for_capture`
- Sanity status: `ready`
- Cycle capture status: `completed`
- Audit reports in package: 42
- Longitudinal summaries in package: 20
- CMP confirmations: pending=8
- Paper artifacts present: claim register, figure plan, paper skeleton, poster plan, results tables, writing pack

## Requirement Audit

| Requirement | Current status | Evidence | Next action |
|---|---|---|---|
| Keep RQ1/RQ2 as the core research frame | Complete | `docs/research/ssrp_paper_outline.md`; `docs/research/ssrp_paper_skeleton_2026-06-06.md` | Keep AI framed as method support, not a third RQ. |
| Keep SOC 2 out of the core framing | Complete | `docs/research/ssrp_writing_pack_2026-06-06.md`; `docs/research/ssrp_claim_register_2026-06-06.md` | Keep SOC 2/GRC to a short discussion implication. |
| Lightweight consent-table layer | Complete | `data/consent_table_pilot_2026-05-30.csv`; consent-table tests | Continue appending Week 2 rows after live capture. |
| Core capture -> scoring -> report pipeline | Complete for current Week 2 evidence gate | `data/reports/audit_reports.jsonl`; `data/research_package/audit_report_summary.csv`; 42 exported reports | Continue weekly capture on frozen targets while expanding sample carefully. |
| Layer 1 path availability | Complete for current deterministic scorer | Layer 1 tests and exported path fields in `data/research_package/audit_report_summary.csv` | Re-check edge cases after live capture. |
| Layer 2 effort scoring | Complete for current deterministic scorer | Layer 2 tests and exported effort fields | Re-check effort distribution after live capture. |
| Layer 3 text/framing rubric | Complete as deterministic fallback | Layer 3 tests; `docs/research/ssrp_writing_pack_2026-06-06.md` | Treat model-based extraction as optional method enhancement. |
| Longitudinal diff and weekly summaries | Complete for stored observations | `data/research_package/longitudinal_summary.csv`; 20 exported summaries | Use Week 2 summaries as the first completed evidence gate, not the final dataset. |
| Evidence for every score | Complete for the 5-site Week 2 gate | `docs/research/week2_sanity_check_2026-06-06.md` confirms 5/5 screenshot/DOM/hash/report evidence | Preserve this evidence standard during sample expansion. |
| Deterministic final scoring after model extraction | Complete for current code path | `CONCEPTS.md`; deterministic layer modules; tests | Preserve invariant if adding LLM/VLM extraction later. |
| Week 1 tooling/setup/sample artifacts | Complete | Planning files, access probes, sample readiness outputs, research package | No immediate action. |
| Week 2 single-site/weekly capture cycle | Complete for 5/5 targets | `docs/research/week2_capture_day_checklist_2026-06-06.md`; `docs/research/week2_cycle_report_2026-06-06.md` | Review results before expanding the sample. |
| Focused deep sample around 20 sites | Incomplete | Frozen Week 2 target list has 5 active sites | Expand toward roughly 20 only after Week 2 evidence gate is stable. |
| CMP/manual-review loop | Built but unresolved | `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`; `docs/research/cmp_confirmation_request_2026-05-30.md`; CMP confirmations pending=8 | Advisor/human review must confirm or reject the 8 pending rows. |
| Paper results tables | Ready for Week 2 evidence-gate discussion | `docs/research/ssrp_results_tables_2026-06-06.md`; claim register marks result claims ready | Use with sanity/source evidence refs; refresh after future captures. |
| Paper skeleton/writing pack | Ready as Week 2 drafting scaffold | `docs/research/ssrp_paper_skeleton_2026-06-06.md`; `docs/research/ssrp_writing_pack_2026-06-06.md` | Use as draft scaffold, not final 10-week results. |
| Claim register | Complete as a guardrail | `docs/research/ssrp_claim_register_2026-06-06.md` | Re-run before copying any final results claims. |
| Poster plan | Complete as a storyboard, evidence now refreshed for Week 2 | `docs/research/ssrp_poster_plan_2026-06-06.md` | Render final visuals after sample expansion and paper story are stable. |
| Demo/evidence browser | Missing | No current generated evidence-browser index for all Week 2 targets | Needs a short design approval before implementation. |
| SSRP paper/poster final deliverables | Incomplete by date and evidence gate | Current artifacts are scaffold/provisional; final period is Aug. 8-Aug. 31 | Freeze dataset after Week 10, then revise paper/poster. |

## Test Plan Audit

| Planned check | Current evidence | Status |
|---|---|---|
| Pydantic/model round-trip tests | `tests/test_models.py`; full pytest run | Covered |
| Layer 1 fixture cases | `tests/layers/test_layer1_path_availability.py` | Covered |
| Capture smoke on public canary sites | Stored access/weekly CSV artifacts under `data/` | Covered for pilot evidence, not a substitute for Week 2 live capture |
| LLM evidence quote substring check | Layer 3/text wrapper tests | Covered for deterministic fallback |
| Diff tests with synthetic week-over-week changes | `tests/diff/` | Covered |
| Budget guard failures | `tests/llm/` | Covered |

## Goal Completion Blockers

The overall goal cannot be marked complete yet because:

- CMP/manual-review confirmations remain pending for 8 rows.
- The focused deep sample has only 5 frozen Week 2 targets, below the planned roughly 20-site deep sample.
- Final SSRP paper and poster deliverables are not frozen; current paper/poster artifacts are Week 2 evidence-gate scaffolds.
- A supporting demo/evidence browser has not been designed or implemented.

## Next Viable Work

1. Review the completed Week 2 sanity check, results tables, and claim register.
2. Send or discuss the filled June 6 advisor update draft.
3. Resolve the 8 CMP/manual-review confirmations with human/advisor input.
4. Expand the deep sample toward roughly 20 sites after the Week 2 evidence gate is stable.
5. Design and implement a small static evidence browser that links targets, latest audit reports, screenshots, DOM refs, longitudinal summaries, claim status, and source artifacts.
