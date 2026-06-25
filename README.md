# Dynamic Consent Interface Audit System

**SSRP 2026** · Qianyi (Alfred) Chen · Mentor: Dr. Jagdip Singh

An AI-driven, agent-based, longitudinal audit framework for website consent interfaces (cookie banners, privacy pages). Combines **Vision-Language Models** (for visual analysis of banner screenshots), **Large Language Models** (for content and framing analysis), and **Browser Agents** (for dynamic consent-path traversal).

## Why this project

Current approaches leave a gap:
- **PRISMe** (Freiberger, Fleig & Buchmann, ACM CHI 2026) audits privacy *policy text* with LLMs, but ignores the interface.
- **UMBRA / "When the Abyss Looks Back"** (Singh, Jin & Kim, 2026) audits banner *interfaces* with rule-based heuristics + multi-step interaction tracing + cookie-state monitoring; 14k sites, 19 dark patterns — but no LLM/VLM, and not longitudinal.
- **ConsentDiff at Scale** (Guo, 2026) is longitudinal (9 months) and pairs DOM signals with screenshot cues — but uses weak-supervision vision rather than VLM-driven action execution.

This project sits in the gap none of them close: **multimodal AI grounding (VLM + LLM) × agent-dynamic multi-step traversal × longitudinal time series × text-framing analysis × volatility/trajectory as first-class outputs**. Built on the Notice-and-Choice framework with a three-layer audit (Path Availability → Path Effort → Transparency & Unbiased Choice). See [`docs/related_work/background_with_citations.md`](docs/related_work/background_with_citations.md) for the full positioning.

## Documents

| File | Purpose |
|---|---|
| [SCHEMA.md](SCHEMA.md) | **Start here** — one-page master view: research question → ontology → pipeline → modules → status → open decisions |
| [AGENTS.md](AGENTS.md) | How AI agents (Claude Code, Cursor, etc.) collaborate on this repo |
| [CONCEPTS.md](CONCEPTS.md) | Precise definitions of every audit dimension — the project's ontology |
| [docs/architecture.md](docs/architecture.md) | Technical architecture, data flow, module boundaries |
| [docs/related_work/background_with_citations.md](docs/related_work/background_with_citations.md) | Lit review + regulatory framework + user ecosystem (cited) |
| [docs/related_work/legal_cheatsheet.md](docs/related_work/legal_cheatsheet.md) | 1-page reference: the 8 legal anchors every audit metric maps to |
| [docs/research/week2_execution_runbook_2026-06-06.md](docs/research/week2_execution_runbook_2026-06-06.md) | Current Week 2 capture + advisor-review runbook |
| [Chen_Qianyi_SSRP 2026_Proposal_Final Version.docx.pdf](./Chen_Qianyi_SSRP%202026_Proposal_Final%20Version.docx.pdf) | Original SSRP research proposal |

## Quick start (WIP)

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

# Export a current evidence-grounded SSRP paper skeleton
uv run consent-audit ssrp-paper-skeleton

# Export paper-ready RQ1/RQ2 Markdown results tables
uv run consent-audit ssrp-results-tables

# Export a figure queue for the paper/poster
uv run consent-audit ssrp-figure-plan

# Export draftable paper notes for methods/results/discussion/limitations
uv run consent-audit ssrp-writing-pack

# Export an evidence/status register for paper claims
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

# Refresh the full Week 2 paper/advisor package after a capture run
uv run consent-audit week2-refresh-outputs

# Dry-run the full Week 2 cycle without opening browser capture
uv run consent-audit week2-cycle --dry-run

# Run the full Week 2 cycle: preflight, browser capture, then refresh outputs
uv run consent-audit week2-cycle

# Export paper-facing RQ1/RQ2 tables plus a manifest
uv run consent-audit export-research-package
```

## Repository layout

```
src/consent_audit/
├── capture/    — browser agent, multimodal fingerprinting
├── layers/     — Layer 1/2/3 audit logic
├── llm/        — LLM and VLM client wrappers
├── models/     — Pydantic data models (audit report schema)
├── storage/    — DB + object storage
├── diff/       — longitudinal diff engine
└── report/     — report rendering
scripts/        — direct-execution wrappers and research utility scripts
data/           — site lists, research exports, and selected evidence artifacts
tests/          — unit + integration tests
docs/           — architecture, references, paper drafts
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
- Current paper-facing exports contain 42 audit reports and 20 longitudinal weekly summaries.
- Week 2 default capture list is `data/week2_deep_sample_targets_2026-06-06.csv`.
- The Week 2 live cycle completed 5/5 captures; sanity is `ready`.
- Next operational step is advisor/sample review plus a decision on whether to
  rerun the current five with the fixed capture agent, or switch this week to a
  semi-automated screenshot/DOM/manual-validation protocol.
- Current advisor email draft is [docs/research/advisor_email_latest_2026-06-15.md](docs/research/advisor_email_latest_2026-06-15.md).
- Current short advisor decision email is [docs/research/advisor_email_current_five_decision_2026-06-19.md](docs/research/advisor_email_current_five_decision_2026-06-19.md).
- The Week 2 capture runbook remains [docs/research/week2_execution_runbook_2026-06-06.md](docs/research/week2_execution_runbook_2026-06-06.md).
- Current advisor-facing update brief is [docs/research/week2_advisor_update_2026-06-06.md](docs/research/week2_advisor_update_2026-06-06.md).
- Current evidence-grounded paper skeleton is [docs/research/ssrp_paper_skeleton_2026-06-06.md](docs/research/ssrp_paper_skeleton_2026-06-06.md).
- Current paper-ready RQ1/RQ2 results tables are [docs/research/ssrp_results_tables_2026-06-06.md](docs/research/ssrp_results_tables_2026-06-06.md).
- Current paper/poster figure plan is [docs/research/ssrp_figure_plan_2026-06-06.md](docs/research/ssrp_figure_plan_2026-06-06.md).
- Current paper writing pack is [docs/research/ssrp_writing_pack_2026-06-06.md](docs/research/ssrp_writing_pack_2026-06-06.md).
- Current paper claim register is [docs/research/ssrp_claim_register_2026-06-06.md](docs/research/ssrp_claim_register_2026-06-06.md).
- Current SSRP poster plan is [docs/research/ssrp_poster_plan_2026-06-06.md](docs/research/ssrp_poster_plan_2026-06-06.md).
- Current remaining-work audit is [docs/research/ssrp_remaining_work_audit_2026-05-30.md](docs/research/ssrp_remaining_work_audit_2026-05-30.md).
- Current CMP confirmation request is [docs/research/cmp_confirmation_request_2026-05-30.md](docs/research/cmp_confirmation_request_2026-05-30.md).
- Current Week 2 sanity check is [docs/research/week2_sanity_check_2026-06-06.md](docs/research/week2_sanity_check_2026-06-06.md).
- Current Week 2 advisor check-in index is [docs/research/week2_checkin_index_2026-06-06.md](docs/research/week2_checkin_index_2026-06-06.md).
- Current Week 2 capture-day checklist is [docs/research/week2_capture_day_checklist_2026-06-06.md](docs/research/week2_capture_day_checklist_2026-06-06.md).
- Current Week 2 cycle report is [docs/research/week2_cycle_report_2026-06-06.md](docs/research/week2_cycle_report_2026-06-06.md).
- Current Week 2 preflight check is [docs/research/week2_preflight_check_2026-06-06.md](docs/research/week2_preflight_check_2026-06-06.md).
- Current Week 2 refresh report is [docs/research/week2_refresh_report_2026-06-06.md](docs/research/week2_refresh_report_2026-06-06.md).
- Current Week 2 manual evidence review worksheet is [data/week2_manual_evidence_review_2026-06-10.csv](data/week2_manual_evidence_review_2026-06-10.csv).
- Current Week 3 continuity target list is [data/week3_continuity_targets_2026-06-13.csv](data/week3_continuity_targets_2026-06-13.csv).
- Current June 14 capture attempt audit is [docs/research/june14_capture_attempt_audit_2026-06-14.md](docs/research/june14_capture_attempt_audit_2026-06-14.md).
- Current June 15 Coca-Cola smoke capture audit is [docs/research/june15_coca_cola_smoke_audit_2026-06-15.md](docs/research/june15_coca_cola_smoke_audit_2026-06-15.md).
- Current daily work note is [docs/research/today_work_note_2026-06-25.md](docs/research/today_work_note_2026-06-25.md).
- Current current-five evidence packet is [docs/research/current_five_evidence_packet_2026-06-19.md](docs/research/current_five_evidence_packet_2026-06-19.md).
- Current current-five decision sheet is [data/current_five_decision_sheet_2026-06-19.csv](data/current_five_decision_sheet_2026-06-19.csv).
- Current full project audit is [docs/research/full_project_audit_2026-06-15.md](docs/research/full_project_audit_2026-06-15.md).
- Current full fact audit is [docs/research/full_project_fact_audit_2026-06-10.md](docs/research/full_project_fact_audit_2026-06-10.md).
- Run `uv run consent-audit research-status` for a compact current-state dashboard and next action.
- The 8 pending CMP/manual-review rows remain advisor-review material, not locked sample decisions.
