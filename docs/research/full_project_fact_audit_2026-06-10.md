# Full Project Fact Audit, 2026-06-10

2026-06-29 correction note: this is a historical audit. Current checkout
evidence counts differ: `data/captures/sites` has 326 tracked `layer1.png`
screenshots and 0 synced `layer1.html` files. Use
`docs/research/project_status_plain_language_2026-06-28.md` and
`docs/research/summer_midpoint_progress_audit_2026-06-29.md` for current
evidence-location claims.

## Purpose

This document audits the consent-interface audit project from the beginning of
the current SSRP work through the latest 2026-06-10 state. Every conclusion
below is tied to a current repo artifact or command output. Historical drafts
are treated as historical records, not current truth.

## Authoritative Evidence Checked

| Evidence source | What it proves |
|---|---|
| `git status --short --branch` | Branch is `codex/ssrp-plan-mvp` and was clean before this audit edit. |
| `git log --oneline --decorate -12` | Recent committed work includes screenshot evidence, advisor email, and June 10 manual review worksheet. |
| `consent-audit research-status` | Current dashboard: 5 Week 2 targets, sanity `ready`, cycle `completed`, 42 audit reports, 20 longitudinal summaries, 8 CMP confirmations pending. |
| `data/research_package/research_manifest.json` | Research package counts: 42 audit reports and 20 weekly summaries. |
| `data/research_package/audit_report_summary.csv` | Current RQ1/export rows and evidence refs. |
| `data/research_package/longitudinal_summary.csv` | Current RQ2/export rows and severity/event fields. |
| `data/week2_deep_sample_targets_2026-06-06.csv` | Current frozen Week 2 target list: 5 active sites. |
| `data/week2_manual_evidence_review_2026-06-10.csv` | Current human review worksheet for the five Week 2 evidence bundles. |
| `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` | 8 CMP/manual-review rows remain pending. |
| `docs/research/week2_cycle_report_2026-06-06.md` | Week 2 live cycle completed 5/5 captures. |
| `docs/research/week2_sanity_check_2026-06-06.md` | All five Week 2 targets have complete evidence rows and matching reports/summaries. |
| `docs/research/ssrp_results_tables_2026-06-06.md` | Current RQ1/RQ2 paper-facing tables, including banner-present vs no-visible-banner split. |
| `docs/research/ssrp_claim_register_2026-06-06.md` | Which claims are ready, supported, or still open limitations. |
| `docs/research/advisor_response_action_plan_2026-06-05.md` | Dr. Singh's recorded guidance: keep RQ1/RQ2, treat no-banner cases as contrasts, use about 20 deep sites with an 80-ish tracker as candidate/scaling pool. |
| `git ls-files data/captures` and local file checks | 363 PNG screenshots are tracked; referenced Week 2 screenshots/DOM files exist locally. |

## Current Truth Snapshot

- The project is a traceable consent-interface audit for SSRP, not a SOC 2
  audit system.
- RQ1 remains consent-interface scoring across consent pathways.
- RQ2 remains longitudinal capture/versioning of privacy/consent interfaces.
- AI/VLM/LLM pieces are methods, not new research questions.
- Week 2 live capture is complete for the frozen five-site evidence gate.
- Current package counts are 42 audit reports and 20 longitudinal summaries.
- Week 2 sanity is `ready`.
- Current Week 2 sites are The Guardian, CNN, Booking.com, NerdWallet, and
  Coca-Cola.
- Current Week 2 evidence classes are:
  - banner/control evidence: The Guardian, Coca-Cola;
  - no visible first-screen banner: CNN, Booking.com, NerdWallet.
- The no-visible-banner rows should not be described as banner-path failures.
- The current five-site evidence gate is not the final SSRP dataset.
- The deep sample still needs expansion toward about 20 well-documented sites.
- 8 CMP/manual-review rows remain pending.
- Paper/poster artifacts exist, but they are Week 2 drafting scaffolds, not
  final August deliverables.

## Timeline Audit

| Period | Supported work | Current status |
|---|---|---|
| Initial orientation | Repo contains proposal, README, SCHEMA, CONCEPTS, related work, Qiyao reference data, and planning files. | Complete as project grounding. |
| Planning pass | Project was narrowed to RQ1 scoring + RQ2 longitudinal capture/versioning; SOC 2 kept out of core frame; about-20 deep sample prioritized over 80+ breadth. | Still aligned with `advisor_response_action_plan_2026-06-05.md`. |
| Pipeline build | Code supports capture, Layer 1/2/3 scoring fallbacks, reports, weekly summaries, exports, site validation, paper/poster artifact generation, and CLI entrypoints. | Supported by source tree, tests, and generated artifacts. |
| Candidate/sample work | Pilot/replacement/CMP review CSVs exist; Week 2 frozen list has five active targets. | Week 2 gate complete; sample expansion still incomplete. |
| Week 2 capture | Live cycle completed 5/5; sanity ready; research package refreshed. | Complete for evidence gate, not final dataset. |
| Post-capture interpretation | Results split banner-present cases from no-visible-banner contrast candidates. | Current guardrail: do not claim all five are banner-present failures. |
| Communication/advisor prep | Evidence-based email draft and recent work audit exist; June 10 manual evidence worksheet exists. | Ready for advisor/human review. |

## Data Audit

| Artifact | Current checked fact | Status |
|---|---|---|
| `data/research_package/audit_report_summary.csv` | 42 rows, 24 columns. | Consistent with manifest. |
| `data/research_package/longitudinal_summary.csv` | 20 rows, 13 columns. | Consistent with manifest. |
| `data/week2_deep_sample_targets_2026-06-06.csv` | 5 target rows. | Current frozen Week 2 input. |
| `data/week2_manual_evidence_review_2026-06-10.csv` | 5 rows, all screenshot/DOM refs exist. | Good current manual-review input. |
| `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` | 8 rows, pending confirmation state. | Open issue. |
| `data/captures/**/*.png` | 363 PNG screenshots tracked by Git. | Evidence synced; HTML snapshots remain local/untracked. |

## Site-Level Current Facts

| Site | Current evidence class | Current coding | RQ2 status | Evidence source |
|---|---|---|---|---|
| The Guardian | Banner/control evidence | Banner-present scored case; automated tier High-Risk; no first-layer paths detected. | Severity D; pathway, copy, layout, DOM changes. | `data/week2_manual_evidence_review_2026-06-10.csv` |
| CNN | No visible first-screen banner | Contrast candidate, not banner-path failure. | Severity C; copy, layout, DOM changes. | `data/week2_manual_evidence_review_2026-06-10.csv` |
| Booking.com | No visible first-screen banner | Contrast candidate, not banner-path failure. | Severity C; copy, layout, DOM changes. | `data/week2_manual_evidence_review_2026-06-10.csv` |
| NerdWallet | No visible first-screen banner | Contrast candidate, not banner-path failure. | Severity C; copy, layout, DOM changes. | `data/week2_manual_evidence_review_2026-06-10.csv` |
| Coca-Cola | Banner/control evidence | Banner-present scored case; Accept observed, Reject/Customize/Dismiss not observed in latest first layer. | Severity D; score, pathway, copy, layout, DOM changes. | `data/week2_manual_evidence_review_2026-06-10.csv` |

## Problems Found And Fixed In This Audit

| Problem | Evidence | Fix |
|---|---|---|
| README implied all capture artifacts are gitignored, but PNG screenshots are now tracked. | `git ls-files data/captures` shows 363 PNG files. | Updated README layout wording to "selected evidence artifacts." |
| SCHEMA status date stopped at 2026-06-06 and did not mention the June 10 manual evidence review worksheet. | `research-status`; `data/week2_manual_evidence_review_2026-06-10.csv`. | Updated SCHEMA status date and added the worksheet. |
| `ssrp_project_clarity_plan_2026-05-30.md` still described pre-capture state: 37/15 counts, `pending_capture`, and waiting for June 6. | Current manifest is 42/20; sanity is `ready`; cycle is `completed`. | Updated the current-state section and next-step instructions. |
| `sample_strategy.md` still described 37/15 counts and a pre-run sanity baseline. | Current manifest and sanity report contradict those values. | Updated counts and Week 2 sanity wording. |
| `sample_strategy.md` still described Coca-Cola as latest Compliant evidence. | Latest Week 2 row has `tier=High-Risk`, Accept only, severity D. | Updated Coca-Cola wording to point to the manual review worksheet. |
| `folder_structure_guide_2026-05-31.md` still described 37/15 counts and `pending_capture`. | Current manifest and `research-status` show 42/20 and `ready`. | Updated the current status sections. |

## Problems Found But Not Edited

These files contain historically correct but now-stale statements. They are
kept as dated historical drafts, not current truth sources:

- `docs/research/advisor_email_draft_2026-06-05.md`
- `docs/research/advisor_meeting_pm_brief_2026-05-31.md`
- `docs/research/replacement_probe_batch2_brief_2026-05-30.md`
- `docs/research/expanded_weekly_capture_brief_2026-05-30.md`
- `docs/research/week2_sample_plan_2026-05-30.md`

When writing current emails, papers, or poster text, use these current sources
instead:

- `docs/research/week2_checkin_index_2026-06-06.md`
- `docs/research/recent_work_evidence_audit_2026-06-09.md`
- `docs/research/advisor_email_evidence_based_next_steps_2026-06-09.md`
- `docs/research/today_work_note_2026-06-10.md`
- `data/week2_manual_evidence_review_2026-06-10.csv`

## Safe Claims

- "The Week 2 five-site evidence gate completed successfully."
- "The current package contains 42 audit reports and 20 longitudinal summaries."
- "The five Week 2 targets have traceable screenshot/DOM/hash/report evidence."
- "The current evidence split is 2 banner-present cases and 3 no-visible-banner contrast candidates."
- "The project should not treat CNN, Booking.com, or NerdWallet as banner-path failure claims."
- "The next research bottleneck is human/advisor coding decisions, not another blind capture run."

## Unsafe Claims

- "The final SSRP dataset is complete."
- "All five Week 2 sites showed visible consent banners."
- "CNN, Booking.com, and NerdWallet failed consent-path availability as banner-present interfaces."
- "Coca-Cola is currently Compliant based on the latest Week 2 capture."
- "The 80-ish broader tracker is the main sample."
- "This project is a SOC 2 audit system."

## Next Evidence-Based Work

1. Fill `data/week2_manual_evidence_review_2026-06-10.csv` by manually opening
   each screenshot/DOM evidence bundle.
2. Send or discuss the evidence-based advisor email draft:
   `docs/research/advisor_email_evidence_based_next_steps_2026-06-09.md`.
3. Resolve the no-visible-banner table rule and CMP/manual-review pending rows.
4. Expand toward about 20 deep-sample sites only after the current five rows
   have human coding decisions.
5. Run the next weekly capture around 2026-06-13 only after deciding whether to
   rerun the current five or use an adjusted/expanded target list.
