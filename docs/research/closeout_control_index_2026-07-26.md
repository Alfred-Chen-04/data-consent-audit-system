# SSRP Closeout Control Index, 2026-07-26

## Role

Use this file as the current project entrypoint for the remaining SSRP
closeout window. It separates current working artifacts from dated history and
links the response decision, revision execution, evidence freeze, and final QA
steps in one place.

**Status: `pre_freeze`. This is not a final index. The selected branch is a
project-owner decision, not an advisor response or post-cutoff fallback.**

## Current Snapshot

- Core closeout target: August 7, 2026. Nine calendar days remain from July 29.
- Key deliverables present: 18/18, including the July 29 closeout artifacts and
  project-owner decision provenance in the reproducible manifest.
- Evidence exports: 42 audit-report rows and 20 longitudinal rows; latest
  longitudinal `week_of` is 2026-06-06.
- Audit CSV references: 42/42 screenshot refs are present locally; 42/42 DOM
  refs are missing locally; the CSV has no `report_pdf_ref` column.
- Human-decision sheets: 25 open rows across four dated sheets. This is a
  cross-sheet row count, not 25 unique questions.
- Joint revision matrix: exactly 20 expected rows. The selected value for every
  row is backed by `response_basis=project_owner_decision`; the advisor sheet
  remains pending and blank.
- Final-freeze readiness: `true`; 20/20 revision rows are `applied_verified`,
  with 20 project-owner response-basis claims, 0 basis errors, and
  0 active joint-sheet contract errors.
- Final QA: poster, evidence-package, repository, and repository-external
  backup checks are verified. Only presentation rehearsal timing remains
  `pending`; the final index is absent and its generator refuses this
  incomplete QA state.

File presence is not completion. The machine-readable source for these counts
is the current pre-freeze manifest. Final QA, rehearsal, and backup checks still
control when this page may be replaced by a final index.

Run `uv run consent-audit research-status` for the compact current-state
dashboard. It reads this control index and the schema-v2 pre-freeze manifest;
its closeout counts and next action are derived from those checked-in sources,
not maintained as a separate status claim.

## Current Working Set

| Role | Current file | Current use |
|---|---|---|
| Canonical project goal | [Current project goal](current_project_goal_2026-07-02.md) | Keep RQ1 scoring and RQ2 versioning as the project spine |
| Presentation | [10-slide closeout PPTX](presentation/ssrp_consent_audit_presentation_closeout_2026-07-29.pptx) and [montage](presentation/ssrp_consent_audit_presentation_closeout_2026-07-29_montage.png) | Selected conservative branch applied; final rehearsal remains |
| Poster | [Closeout poster PPTX](poster/ssrp_poster_closeout_2026-07-29.pptx), [PDF](poster/ssrp_poster_closeout_2026-07-29.pdf), and [PNG](poster/ssrp_poster_closeout_2026-07-29.png) | Selected conservative branch, visual/print QA, and repository-external backup/open check complete |
| Evidence tables | [Audit summary](../../data/research_package/audit_report_summary.csv), [longitudinal summary](../../data/research_package/longitudinal_summary.csv), and [research manifest](../../data/research_package/research_manifest.json) | Current checked-in evidence exports |
| Joint review attachment | [Nine-file joint review ZIP](joint_review/ssrp_joint_advisor_review_2026-07-25.zip) | Current single-attachment review packet |
| Review request | [Joint advisor email](advisor_email_joint_presentation_poster_review_2026-07-25.md) | Current send/discussion text |
| Response record | [Joint decision sheet](../../data/joint_advisor_review_decision_sheet_2026-07-25.csv) | Only actual responses with reviewer/date provenance belong here |
| Project-owner decisions | [Decision note](july29_project_owner_closeout_decisions_2026-07-29.md) and [five-row CSV](../../data/closeout/project_owner_decision_sheet_2026-07-29.csv) | Current selected branch; explicitly separate from advisor confirmation and fallback |
| Revision execution | [Decision-to-revision handoff](july26_decision_to_revision_matrix_2026-07-26.md) and [20-row CSV](../../data/closeout/joint_decision_revision_matrix_2026-07-26.csv) | Select, apply, and verify exact affected surfaces |
| Response branch | [Advisor response and fallback protocol](july26_advisor_response_and_fallback_protocol_2026-07-26.md) | Separates actual answers from the post-cutoff project fallback |
| Freeze evidence | [Human-readable pre-freeze manifest](july26_closeout_prefreeze_manifest_2026-07-26.md) and [schema-v2 JSON](../../data/closeout/closeout_prefreeze_manifest_2026-07-26.json) | Reproducible presence, provenance, execution, and readiness gate |
| Current closeout assessment | [July 25 gap review and joint packet](july25_gap_review_and_joint_packet_2026-07-25.md) | On-track assessment and July 25-August 7 work order |
| Low-token execution | [July 27 low-token runbook](closeout_low_token_runbook_2026-07-27.md) | Four-step response, revision, verification, and freeze path with short prompts |
| Final QA and index gate | [Five-row final-QA checklist](../../data/closeout/final_qa_checklist_2026-07-27.csv) | Four checks verified; only rehearsal timing remains; `closeout-final-index` refuses incomplete state |

## Superseded Or Historical Paths

These files remain useful evidence of project history, but they are not the
current closeout response path.

| Dated path | Classification | Use instead for current work |
|---|---|---|
| [July 14 poster mockup](july14_first_poster_mockup_2026-07-14.md) | Historical first visual draft | July 25 aligned poster files |
| [July 21 poster-only review bundle](july21_poster_review_bundle_2026-07-21.md) | Superseded review attachment | July 25 joint review ZIP |
| [July 14 poster-only email](advisor_email_poster_mockup_review_2026-07-14.md) | Superseded email | July 25 joint advisor email |
| [July 16 poster-only decision sheet](july16_poster_review_decision_sheet_2026-07-16.md) | Superseded response path; preserve its pending rows as dated history; two recommended defaults are not listed options, so do not use it for current intake | July 25 joint decision sheet |
| [July 1 scope email](advisor_email_scope_update_2026-07-01.md) and [June 28 decision email](advisor_email_decision_gate_2026-06-28.md) | Historical communication | July 25 joint advisor email |
| [Week 2 check-in index](week2_checkin_index_2026-06-06.md) | Full evidence/history navigation | This closeout control index |
| [Advisor packet index](advisor_packet_index_2026-06-05.md) | Full communication history | This closeout control index |
| [Paper skeleton](ssrp_paper_skeleton_2026-06-06.md) and [writing pack](ssrp_writing_pack_2026-06-06.md) | Supporting research material, not the current summer deliverable | Presentation, poster, and traceable evidence package |

Do not delete or rewrite the historical files to make old pending states look
resolved. Their role is provenance, not current control.

## Work Order By Date

| Date | Required action | Evidence of completion |
|---|---|---|
| July 26-29 | Send or discuss the joint packet and record only actual answers received | Joint sheet preserves only actual advisor-response provenance |
| July 29 | Record the project owner's explicit authorization and conservative selections | Separate five-row project-owner source validates without changing advisor fields |
| July 29-August 2 | Apply the selected values to every mapped presentation, poster, and evidence surface | All 20 matrix rows reach `applied_verified` with executor and timezone-aware timestamp |
| August 3-5 | Rebuild packages and regenerate hashes/readiness | Manifest matches the checkout and reports no blocker |
| August 6-7 | Rerender, inspect, rehearse, back up, and replace this pre-freeze control page with the final index | One final index opens the verified presentation, poster, and evidence package |

## Branch Rules

### Project-owner decision

- Keep the advisor sheet pending unless an actual answer is received.
- Record exact listed values, authorization, rationale, evidence, and a
  timezone-aware timestamp in the separate project-owner sheet.
- Use `response_basis=project_owner_decision`; never describe it as advisor
  approval or as a post-cutoff fallback.

### Actual response

- Record the exact answer in the joint decision sheet with reviewer/date
  provenance.
- Copy the exact confirmed value into matching matrix rows with
  `response_basis=actual_advisor_response`.
- Apply and verify only the mapped surfaces.

### No response after the internal cutoff

- Internal cutoff: July 29, 23:59 Asia/Shanghai.
- Keep joint-sheet confirmation, reviewer, and date fields blank/pending.
- Use only the five fallback values in the July 26 protocol with
  `response_basis=project_fallback_after_internal_cutoff`.
- Describe the basis as a project closeout decision, never as advisor approval.

## Final Acceptance Checklist

- [x] One response basis is valid for every revision row.
- [x] All 20 expected revision IDs are present and `applied_verified`.
- [ ] Presentation wording, overflow, render, montage, and rehearsal checks pass.
- [x] Poster wording, overflow, 48 x 36 print dimensions, PDF/PNG render, and
  visual inspection pass.
- [x] Evidence tables, current/missing refs, limitations, packages, and hashes
  are refreshed from the revised sources.
- [x] Full tests, Ruff, Mypy, compileall, links, JSON, ZIP, and Git-state checks
  pass.
- [x] The regenerated manifest reports `ready_for_final_freeze=true` and no
  blocker.
- [ ] A final index and backup open the verified presentation, poster, and
  evidence package.

Record the five final artifact-level checks in the linked final-QA CSV. Run
`uv run consent-audit closeout-final-index` as a dry-run; only rerun with
`--write` after both the schema-v2 manifest and every QA row pass validation.

## Historical Trail

| Period | What it established | Primary dated navigation |
|---|---|---|
| May 30-June 5 | Scope, sample strategy, RQs, and advisor direction | [Sample strategy](sample_strategy.md), [advisor alignment audit](advisor_guideline_alignment_audit_2026-06-05.md) |
| June 6-15 | Live-cycle evidence, sanity checks, initial results, and capture troubleshooting | [Week 2 index](week2_checkin_index_2026-06-06.md), [June 15 full audit](full_project_audit_2026-06-15.md) |
| June 18-29 | Current-five evidence, unresolved human decisions, publication, and midpoint fact audits | [Current-five packet](current_five_evidence_packet_2026-06-19.md), [midpoint audit](summer_midpoint_progress_audit_2026-06-29.md) |
| July 1-16 | Canonical scope, poster story, layouts, assets, first visual draft, and print QA | [Current goal](current_project_goal_2026-07-02.md), [first poster](july14_first_poster_mockup_2026-07-14.md), [print QA](july15_poster_pdf_and_print_qa_2026-07-15.md) |
| July 20-26 | Joint presentation/poster review, fallback protocol, reproducible inventory, revision map, and freeze gate | [July 25 gap review](july25_gap_review_and_joint_packet_2026-07-25.md), [July 26 pre-freeze manifest](july26_closeout_prefreeze_manifest_2026-07-26.md) |

## Claim Guardrails

- Keep the contribution framed as a bounded pilot/method package unless
  additional reviewed evidence supports a broader claim.
- Keep CNN, Booking.com, and NerdWallet as no-visible-first-screen-banner
  contrasts, not implied banner-path failures.
- Do not present stored screenshots as current live-site observations.
- Do not claim locally synced raw DOM, per-report PDFs, continuous July
  tracking, active external-model scoring, hosted infrastructure, or legal
  compliance verdicts.
- Do not run a continuity capture without a specific approved RQ2 question.
