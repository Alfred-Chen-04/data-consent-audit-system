# SSRP Closeout Control Index, 2026-07-26

## Role

Use this file as the current project entrypoint for the remaining SSRP
closeout window. It separates current working artifacts from dated history and
links the response decision, revision execution, evidence freeze, and final QA
steps in one place.

**Status: `pre_freeze`, reconciled August 10. This is not a final index. The
machine-verifiable evidence and artifacts are current; Summer Intersections has
passed without checked-in participation evidence, and a timed rehearsal plus
actual final-paper submission remain human facts.**

## Current Snapshot

- Summer 2026 Intersections occurred on July 30, 2026, 10:00 a.m.-12:00 p.m.
  The repository does not establish whether the project was registered or
  presented. Do not infer the answer from prepared files; obtain an email or
  CampusGroups record, or request the Fall 2026/Spring 2027 path from URO.
- The official SSRP program period is May 26-July 31, 2026. The official final
  paper deadline is August 31, 2026.
- Current display artifacts are the July 30 ten-slide presentation and the
  July 30 48 x 36 poster in PPTX, PDF, and PNG form.
- Evidence exports: 42 audit-report rows and 20 longitudinal rows; latest
  longitudinal `week_of` is 2026-06-06.
- Local matched-pair evidence: five sites, one May 29-June 5 interval, and five
  `insufficient_evidence` direction labels. It validates the method but does
  not support a local improvement/regression claim.
- Retrospective evidence: six source-complete company trajectories backed by
  12 dated primary or primary-research sources; five improve and one regresses
  under the component rule. All three first-layer cases improve rejection
  parity or effort.
- Result boundary: this is a purposively selected observational case series,
  not an experiment, randomized causal estimate, or prevalence estimate.
- Causal evidence is graded separately from direction. Google has direct
  company attribution; Facebook and Orange have regulator order verification;
  TikTok and SHEIN changed during proceedings; Vanity Fair's later failure has
  unknown cause.
- Audit CSV references: 42/42 screenshot refs are present locally; 42/42 DOM
  refs are missing locally; the CSV has no `report_pdf_ref` column.
- Human-decision sheets: 25 open rows across four dated sheets. This is a
  cross-sheet row count, not 25 unique questions.
- Joint revision matrix: exactly 20 expected rows. The selected value for every
  row is backed by `response_basis=project_owner_decision`; the advisor sheet
  remains pending and blank.
- Decision execution remains valid: 20/20 revision rows are
  `applied_verified`, with 20 project-owner response-basis claims, 0 basis
  errors, and 0 active joint-sheet contract errors.
- Artifact QA: presentation/poster rendering, visual inspection, overflow,
  template fidelity, poster PDF rendering, and 48 x 36 dimensions pass.
- Remaining human facts: actual Intersections/board status, one timed
  rehearsal, and actual final-paper submission. The final index must continue
  to refuse completion until the required QA rows are verified.

File presence is not completion. The July 30 SHA-256 manifest is the current
artifact inventory; the schema-v2 pre-freeze manifest still supplies the
decision-execution gate used by `closeout-final-index`.

Run `uv run consent-audit research-status` for the compact current-state
dashboard. It reads this control index and the schema-v2 pre-freeze manifest;
its closeout counts and next action are derived from those checked-in sources,
not maintained as a separate status claim.

## Current Working Set

| Role | Current file | Current use |
|---|---|---|
| Canonical project goal | [Current project goal](current_project_goal_2026-07-02.md) | Longitudinal objective; RQ1 defines the measure and RQ2 creates the matched timeline |
| Research reframing | [Longitudinal reframing and SOURCE alignment](july29_longitudinal_reframing_and_source_alignment_2026-07-29.md) | Current facts, outcome taxonomy, research gaps, and display plan |
| Retrospective finding | [Evidence-rescue analysis](july29_retrospective_longitudinal_evidence_rescue_2026-07-29.md) | Six dated trajectories, direction/causal-strength audit, external benchmark, limitations, and discussion questions |
| Presentation | [10-slide rehearsal-ready PPTX](presentation/ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04.pptx), [montage](presentation/ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04_montage.png), and [readiness guide](presentation/ssrp_consent_presentation_readiness_2026-08-04.md) | Machine and visual QA pass; speaker notes, short formats, and question bank are ready; one timed human rehearsal remains |
| Poster | [Longitudinal poster PPTX](poster/ssrp_consent_longitudinal_poster_2026-07-30.pptx), [PDF](poster/ssrp_consent_longitudinal_poster_2026-07-30.pdf), and [PNG](poster/ssrp_consent_longitudinal_poster_2026-07-30.png) | Template, overflow, visual, PDF, and 48 x 36 checks pass; actual board/event status remains |
| Evidence tables | [Audit summary](../../data/research_package/audit_report_summary.csv), [longitudinal summary](../../data/research_package/longitudinal_summary.csv), and [research manifest](../../data/research_package/research_manifest.json) | Current checked-in evidence exports |
| Directional review | [Five-site matched-pair CSV](../../data/longitudinal_directional_review_2026-07-29.csv) | All current trajectory labels remain insufficient evidence |
| Historical directional cases | [Six-company case CSV](../../data/retrospective_longitudinal_cases_2026-07-29.csv) and [12-source registry](../../data/retrospective_source_registry_2026-07-29.csv) | Five component improvements and one regression; case-series fractions are not prevalence estimates |
| Longitudinal artifact QA | [July 30 QA record](../../data/longitudinal_revision_qa_2026-07-30.csv) | Machine/render checks pass; rehearsal and actual event/board status remain |
| Longitudinal artifact inventory | [July 30 SHA-256 manifest](../../data/longitudinal_artifact_manifest_2026-07-30.json) | Reproducible current research, evidence, presentation, poster, plan, and QA inventory |
| Artifact delivery | [July 30 delivery note](july30_evidence_complete_artifact_delivery_2026-07-30.md) | Final paths, verification results, backup location, and remaining human gates |
| Today-to-submission plan | [August 3 closeout plan](july30_final_closeout_execution_plan_2026-07-30.md), [source-audited paper candidate](ssrp_final_paper_submission_candidate_2026-08-05.docx), [Markdown source](ssrp_final_paper_submission_candidate_2026-08-05.md), and [paper completion plan](ssrp_final_paper_completion_plan_2026-07-30.md) | Current recovery, paper review, claim audit, and submission path; actual submission remains an owner fact |
| August 3 reconciliation | [Closeout reconciliation](aug03_closeout_reconciliation_2026-08-03.md) | Separates the passed Summer event from remaining evidence-backed obligations |
| Joint review attachment | [Nine-file joint review ZIP](joint_review/ssrp_joint_advisor_review_2026-07-25.zip) | Current single-attachment review packet |
| Review request | [Joint advisor email](advisor_email_joint_presentation_poster_review_2026-07-25.md) | Current send/discussion text |
| Response record | [Joint decision sheet](../../data/joint_advisor_review_decision_sheet_2026-07-25.csv) | Only actual responses with reviewer/date provenance belong here |
| Project-owner decisions | [Decision note](july29_project_owner_closeout_decisions_2026-07-29.md) and [five-row CSV](../../data/closeout/project_owner_decision_sheet_2026-07-29.csv) | Current selected branch; explicitly separate from advisor confirmation and fallback |
| Revision execution | [Decision-to-revision handoff](july26_decision_to_revision_matrix_2026-07-26.md) and [20-row CSV](../../data/closeout/joint_decision_revision_matrix_2026-07-26.csv) | Select, apply, and verify exact affected surfaces |
| Response branch | [Advisor response and fallback protocol](july26_advisor_response_and_fallback_protocol_2026-07-26.md) | Separates actual answers from the post-cutoff project fallback |
| Freeze evidence | [Human-readable pre-freeze manifest](july26_closeout_prefreeze_manifest_2026-07-26.md) and [schema-v2 JSON](../../data/closeout/closeout_prefreeze_manifest_2026-07-26.json) | Reproducible presence, provenance, execution, and readiness gate |
| Current closeout assessment | [July 25 gap review and joint packet](july25_gap_review_and_joint_packet_2026-07-25.md) | On-track assessment and July 25-August 7 work order |
| Final-week sync audit | [August 10 sync and handoff](aug10_final_week_sync_and_handoff_2026-08-10.md) | GitHub parity, external-file disposition, and the three remaining human facts |
| Low-token execution | [August 6 low-token runbook](closeout_low_token_runbook_2026-07-27.md) | Three-line human status intake, final-index path, and short final-paper prompts |
| Final QA and index gate | [Five-row final-QA checklist](../../data/closeout/final_qa_checklist_2026-07-27.csv) | Machine rows verified; rehearsal remains pending; `closeout-final-index` refuses incomplete state |

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
| [July 29 audit/versioning presentation](presentation/ssrp_consent_audit_presentation_closeout_2026-07-29.pptx) and [poster PDF](poster/ssrp_poster_closeout_2026-07-29.pdf) | Superseded display story; preserved as a closeout baseline | Current longitudinal presentation and poster in the working set above |

Do not delete or rewrite the historical files to make old pending states look
resolved. Their role is provenance, not current control.

## Work Order By Date

| Date | Required action | Evidence of completion |
|---|---|---|
| July 30-31 | Machine QA, current hashes, manifest, backup, and documentation | Completed; July 30 delivery note and manifests match the checkout |
| August 3-7 | Obtain evidence of Summer participation or request Fall/Spring path; perform one timed rehearsal | Human confirmation CSV or URO reply contains dated evidence, not assumptions |
| August 3-7 | Apply only rehearsal-exposed corrections, format-check the completed paper candidate, and rerun final QA | All five final-QA rows become verified; submission candidate retains source-linked claims |
| August 8-14 | Use only for mentor corrections or event contingency | No unsupported scope expansion or relabeling |
| August 15-31 | Apply only mentor-format corrections, claim-audit any revision, and submit the final-paper candidate | Submission evidence retained; claim boundary remains observational |

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
- [ ] Presentation wording, overflow, render, montage, and rehearsal checks
  pass. Everything except the live timed rehearsal is complete.
- [x] Poster wording, overflow, 48 x 36 print dimensions, PDF/PNG render, and
  visual inspection pass. Board registration is tracked separately in the new
  QA CSV.
- [x] Evidence direction and causal-strength claims resolve to the six-case,
  12-source registry; local insufficient-evidence labels remain unchanged.
- [x] Current presentation/poster machine checks and visual inspection pass.
- [ ] Actual Intersections/board status is recorded with human provenance.
- [ ] Actual final-paper submission channel, receipt, and timestamp are recorded with human provenance.
- [x] Full repository verification, July 30 manifest, and external backup are
  refreshed for the current checkout.
- [x] The regenerated manifest reports `ready_for_final_freeze=true` and no
  blocker for its existing 18-file inventory.
- [ ] A final index opens the verified presentation, poster, and evidence
  package after every final-QA row is verified.

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
| July 29 | Longitudinal objective correction, retrospective evidence rescue, directional protocol, CWRU SOURCE alignment, and rebuilt presentation/poster | [Evidence rescue](july29_retrospective_longitudinal_evidence_rescue_2026-07-29.md), [longitudinal reframing](july29_longitudinal_reframing_and_source_alignment_2026-07-29.md), [artifact delivery](july29_longitudinal_artifact_delivery_2026-07-29.md) |
| July 30 | Sixth trajectory, explicit causal-strength grading, current artifacts, official deadline audit, and low-token closeout plan | [Execution plan](july30_final_closeout_execution_plan_2026-07-30.md), [paper plan](ssrp_final_paper_completion_plan_2026-07-30.md) |
| August 3 | Post-event status reconciliation, Fall/Spring presentation branch, and source-linked final-paper working draft | [Reconciliation](aug03_closeout_reconciliation_2026-08-03.md), [paper working draft](ssrp_final_paper_working_draft_2026-08-03.md) |

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
- Do not translate raw `C/D` change priority into improvement or regression.
- Do not treat scorer-version changes as website-interface evolution.
