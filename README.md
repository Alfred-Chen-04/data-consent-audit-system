# Dynamic Consent Interface Audit System

**SSRP 2026** · Qianyi (Alfred) Chen · Mentor: Dr. Jagdip Singh

A browser-assisted, evidence-linked audit and versioning framework for website
consent interfaces (cookie banners and preference panels). The current pilot
runtime uses Playwright capture plus deterministic DOM, text, scoring, and diff
logic. The `llm/` modules are schema-shaped, no-network fallbacks; external
LLM/VLM calls are not wired into production scoring.

## Why this project

Current approaches leave a gap:
- **PRISMe** (Freiberger, Fleig & Buchmann, ACM CHI 2026) audits privacy *policy text* with LLMs, but ignores the interface.
- **UMBRA / "When the Abyss Looks Back"** (Singh, Jin & Kim, 2026) audits banner *interfaces* with rule-based heuristics + multi-step interaction tracing + cookie-state monitoring; 14k sites, 19 dark patterns — but no LLM/VLM, and not longitudinal.
- **ConsentDiff at Scale** (Guo, 2026) is longitudinal (9 months) and pairs DOM signals with screenshot cues — but uses weak-supervision vision rather than VLM-driven action execution.

The research design targets the combination of dynamic multi-step traversal,
evidence-linked scoring, longitudinal comparison, and text/visual framing
analysis. The current pilot proves the browser-capture, deterministic-scoring,
export, and versioning path; it does not yet prove live external-model execution
or a production longitudinal deployment. The audit ontology is built on the
Notice-and-Choice framework (Path Availability -> Path Effort -> Transparency &
Unbiased Choice). See
[`docs/related_work/background_with_citations.md`](docs/related_work/background_with_citations.md)
for the full positioning.

## Documents

| File | Purpose |
|---|---|
| [docs/research/closeout_control_index_2026-07-26.md](docs/research/closeout_control_index_2026-07-26.md) | **Start here for closeout** — current artifacts, response/revision/freeze gates, dated work order, historical map, and final acceptance checklist |
| [docs/research/closeout_low_token_runbook_2026-07-27.md](docs/research/closeout_low_token_runbook_2026-07-27.md) | Short safe path for response intake, cutoff fallback, mapped revisions, verification, and final freeze |
| [SCHEMA.md](SCHEMA.md) | One-page technical master view: research question → ontology → pipeline → modules → status → open decisions |
| [AGENTS.md](AGENTS.md) | How AI agents (Claude Code, Cursor, etc.) collaborate on this repo |
| [CONCEPTS.md](CONCEPTS.md) | Precise definitions of every audit dimension — the project's ontology |
| [docs/research/current_project_goal_2026-07-02.md](docs/research/current_project_goal_2026-07-02.md) | Current canonical plain-language goal: RQ1 scoring + RQ2 versioning, not screenshot-only framing |
| [docs/research/july26_decision_to_revision_matrix_2026-07-26.md](docs/research/july26_decision_to_revision_matrix_2026-07-26.md) | Current non-final execution map from five joint decisions to exact presentation, poster, and evidence-package surfaces |
| [docs/research/july26_closeout_prefreeze_manifest_2026-07-26.md](docs/research/july26_closeout_prefreeze_manifest_2026-07-26.md) | Current reproducible pre-freeze inventory: evidence refs, decision gates, revision execution, deliverable presence, hashes, and final-freeze readiness |
| [docs/research/july26_advisor_response_and_fallback_protocol_2026-07-26.md](docs/research/july26_advisor_response_and_fallback_protocol_2026-07-26.md) | Current response gate: verified send preflight plus actual-response and no-response closeout paths |
| [docs/research/july25_gap_review_and_joint_packet_2026-07-25.md](docs/research/july25_gap_review_and_joint_packet_2026-07-25.md) | Current gap review: on-track assessment, remaining evidence/decision gaps, July 25-August 7 plan, and joint review packet |
| [docs/research/advisor_email_joint_presentation_poster_review_2026-07-25.md](docs/research/advisor_email_joint_presentation_poster_review_2026-07-25.md) | Current sendable advisor email for five shared presentation/poster closeout decisions |
| [docs/research/presentation/ssrp_consent_audit_presentation_draft_2026-07-22.pptx](docs/research/presentation/ssrp_consent_audit_presentation_draft_2026-07-22.pptx) | Current 10-slide presentation draft pending decision-aware final revision |
| [docs/research/poster/ssrp_poster_aligned_review_2026-07-25.pdf](docs/research/poster/ssrp_poster_aligned_review_2026-07-25.pdf) | Current aligned 48 x 36 poster review PDF; not final |
| [docs/research/joint_review/ssrp_joint_advisor_review_2026-07-25.zip](docs/research/joint_review/ssrp_joint_advisor_review_2026-07-25.zip) | Current source-matched single-attachment joint review packet |
| [docs/research/week2_checkin_index_2026-06-06.md](docs/research/week2_checkin_index_2026-06-06.md) | Full dated evidence and work-history navigation; no longer the current closeout entrypoint |
| [docs/research/advisor_packet_index_2026-06-05.md](docs/research/advisor_packet_index_2026-06-05.md) | Full dated advisor-communication history; no longer the current closeout entrypoint |
| [docs/architecture.md](docs/architecture.md) | Technical architecture, data flow, module boundaries |
| [docs/related_work/background_with_citations.md](docs/related_work/background_with_citations.md) | Lit review + regulatory framework + user ecosystem (cited) |
| [docs/related_work/legal_cheatsheet.md](docs/related_work/legal_cheatsheet.md) | 1-page reference: the 8 legal anchors every audit metric maps to |
| [Chen_Qianyi_SSRP 2026_Proposal_Final Version.docx.pdf](./Chen_Qianyi_SSRP%202026_Proposal_Final%20Version.docx.pdf) | Original SSRP research proposal |

## Quick start

```bash
# Install deps
uv sync

# Install Playwright browsers (first time only)
uv run playwright install chromium

# Print the current SSRP research state and next action
uv run consent-audit research-status

# Check that a real capture CSV has no placeholders, duplicates, or malformed URLs.
# data/sites.csv is still a scaffold placeholder until the broader mentor list is approved.
uv run consent-audit validate-sites --sites-csv data/week2_deep_sample_targets_2026-06-06.csv

# Week 0 — access feasibility probe for a real candidate/sample CSV
uv run consent-audit access-probe --sites-csv data/deep_sample_candidates.csv --out-csv data/access_probe_v0.csv

# Summarize the access probe for mentor/advisor triage
uv run consent-audit access-probe-summary --csv-path data/access_probe_v0.csv

# Audit a single URL
uv run consent-audit audit https://example.com

# Run the generic weekly pipeline against an explicit, validated site list.
# The Week 2 cycle command below is preferred for the frozen 2026-06-06 run.
uv run consent-audit weekly --sites-csv data/week2_deep_sample_targets_2026-06-06.csv --consent-table-path data/consent_table_pilot_2026-05-30.csv --cohort week2-2026-06-06

# Summarize candidate readiness for advisor/sample review
uv run consent-audit sample-readiness

# Export sites needing CMP/manual review with evidence refs
uv run consent-audit cmp-review-queue

# Export a fillable decision worksheet for CMP/manual review
uv run consent-audit cmp-review-worksheet

# Export a static HTML/Markdown evidence packet for CMP/manual review
uv run consent-audit cmp-review-packet

# Export non-final suggested worksheet decisions from DOM evidence
uv run consent-audit cmp-review-suggestions

# Export a human-confirmable draft decision table for pending CMP rows
uv run consent-audit cmp-review-decision-draft

# Export the sheet an advisor fills to confirm or override CMP draft decisions
uv run consent-audit cmp-review-confirmation-sheet

# Apply explicitly confirmed CMP decisions to a worksheet copy
uv run consent-audit cmp-review-apply-confirmations

# Export fresh-context rerun site-list rows from CMP suggestions
uv run consent-audit cmp-review-rerun-targets

# Export the current sample-lock action plan
uv run consent-audit sample-lock-plan

# Split the sample-lock plan into concrete next-action queues
uv run consent-audit sample-action-queues

# Export the next weekly-capture target list from shortlist + rerun queues
uv run consent-audit sample-weekly-targets

# Review replacement candidates and promote only verified full-pipeline rows
uv run consent-audit replacement-review

# Add verified replacements to the next weekly-capture target list
uv run consent-audit expanded-weekly-targets

# Freeze the current Week 2 default capture list
uv run consent-audit week2-capture-targets

# Export a compact advisor update from current targets/results/review state
uv run consent-audit advisor-update-brief

# Export optional future-paper support notes from current evidence
uv run consent-audit ssrp-paper-skeleton

# Export paper-facing current-evidence RQ1/RQ2 Markdown results tables
uv run consent-audit ssrp-results-tables

# Export a figure queue for presentation/poster and optional future paper
uv run consent-audit ssrp-figure-plan

# Export draftable notes for presentation/poster and optional future paper
uv run consent-audit ssrp-writing-pack

# Export an evidence/status register for claims
uv run consent-audit ssrp-claim-register

# Export a poster storyboard and asset checklist
uv run consent-audit ssrp-poster-plan

# Check whether the Week 2 capture run produced complete evidence rows
uv run consent-audit week2-sanity-check

# Export the single advisor check-in index linking Week 2 evidence artifacts
uv run consent-audit checkin-index

# Export the Week 2 capture-day operator checklist
uv run consent-audit week2-capture-checklist

# Check whether Week 2 inputs are ready before running browser capture
uv run consent-audit week2-preflight-check

# Refresh the full Week 2 presentation/poster/advisor support package after a capture run
uv run consent-audit week2-refresh-outputs

# Dry-run the full Week 2 cycle without opening browser capture
uv run consent-audit week2-cycle --dry-run

# Run the full Week 2 cycle: preflight, browser capture, then refresh outputs
uv run consent-audit week2-cycle

# Export paper-facing RQ1/RQ2 tables plus a manifest
uv run consent-audit export-research-package

# Inventory closeout evidence, decisions, revision execution, deliverables, and freeze readiness
uv run consent-audit closeout-prefreeze-manifest

# Preview the valid actual-response/fallback branch; add --write only after review
uv run consent-audit closeout-prepare-revisions
```

## Repository layout

```
src/consent_audit/
├── capture/    — browser agent, multimodal fingerprinting
├── layers/     — Layer 1/2/3 audit logic
├── llm/        — deterministic no-network fallbacks; future model adapters
├── models/     — Pydantic data models (audit report schema)
├── storage/    — DB + object storage
├── diff/       — longitudinal diff engine
└── report/     — report rendering
scripts/        — direct-execution wrappers and research utility scripts
data/           — site lists, research exports, and selected evidence artifacts
tests/          — unit + integration tests
docs/           — architecture, research records, and delivery artifacts
```

## Status

Current research cycle: Week 2 evidence gate completed as of 2026-06-06.
The attempted Week 3 continuity capture on 2026-06-14 failed at browser
navigation for all five current targets and did not produce valid new
consent-interface observations. A controlled Coca-Cola smoke capture on
2026-06-15 produced screenshot/DOM evidence again and exposed a OneTrust
control-recognition bug. That bug has a regression fix, and a post-fix
Coca-Cola smoke passes all Layer 1 paths.

- Core capture/scoring/export pipeline is executable for the pilot sample and the frozen Week 2 targets.
- Current evidence-facing exports contain 42 audit reports and 20 longitudinal weekly summaries.
- Current model boundary: capture and scoring do not call an external LLM/VLM;
  `llm/text.py` and `llm/vision.py` are deterministic no-network fallbacks and
  are not wired into the capture/scoring orchestration.
- Current persistence is local append-only JSONL plus a local object-store
  fallback. PostgreSQL, R2/S3, APScheduler, and PDF report generation remain
  target architecture, not active runtime capabilities.
- Current summer deliverables are presentation + large poster + traceable
  evidence package. A formal paper is not required for the current summer
  scope unless Dr. Singh reintroduces it later.
- As of 2026-07-25, the independent presentation draft and a fact-aligned poster
  revision both exist. They remain review drafts while five joint decisions,
  seven current-five decisions, and eight CMP confirmations are unresolved.
- Week 2 default capture list is `data/week2_deep_sample_targets_2026-06-06.csv`.
- The Week 2 live cycle completed 5/5 captures; sanity is `ready`.
- Next operational step is the joint presentation/poster review gate; freeze
  current evidence unless one specific RQ2 continuity question is approved.
- Current closeout entrypoint is [docs/research/closeout_control_index_2026-07-26.md](docs/research/closeout_control_index_2026-07-26.md); it separates the active working set from dated history.
- Current canonical project goal is [docs/research/current_project_goal_2026-07-02.md](docs/research/current_project_goal_2026-07-02.md).
- Current reproducible evidence inventory is [docs/research/july26_closeout_prefreeze_manifest_2026-07-26.md](docs/research/july26_closeout_prefreeze_manifest_2026-07-26.md); 15/15 files are present, but `ready_for_final_freeze=false` because all 20 revision rows still await application and verification.
- Current decision-aware revision map is [docs/research/july26_decision_to_revision_matrix_2026-07-26.md](docs/research/july26_decision_to_revision_matrix_2026-07-26.md).
- Current response/fallback protocol is [docs/research/july26_advisor_response_and_fallback_protocol_2026-07-26.md](docs/research/july26_advisor_response_and_fallback_protocol_2026-07-26.md).
- Current review path is the [joint advisor email](docs/research/advisor_email_joint_presentation_poster_review_2026-07-25.md), [joint review ZIP](docs/research/joint_review/ssrp_joint_advisor_review_2026-07-25.zip), and [joint decision sheet](data/joint_advisor_review_decision_sheet_2026-07-25.csv).
- Full dated evidence/work history remains in the [Week 2 index](docs/research/week2_checkin_index_2026-06-06.md); communication history remains in the [advisor packet index](docs/research/advisor_packet_index_2026-06-05.md).
- Run `uv run consent-audit research-status` for the compact runtime dashboard and `uv run consent-audit closeout-prefreeze-manifest` for the reproducible freeze gate.
- The 8 pending CMP/manual-review rows remain advisor-review material, not locked sample decisions.
