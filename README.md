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
| [AGENTS.md](AGENTS.md) | How AI agents (Claude Code, Cursor, etc.) collaborate on this repo |
| [CONCEPTS.md](CONCEPTS.md) | Precise definitions of every audit dimension — the project's ontology |
| [docs/architecture.md](docs/architecture.md) | Technical architecture, data flow, module boundaries |
| [Chen_Qianyi_SSRP 2026_Proposal_Final Version.docx.pdf](./Chen_Qianyi_SSRP%202026_Proposal_Final%20Version.docx.pdf) | Original SSRP research proposal |

## Quick start (WIP)

```bash
# Install deps
uv sync

# Install Playwright browsers (first time only)
uv run playwright install chromium

# Week 0 — access feasibility probe (runs before any LLM/VLM is involved)
uv run python scripts/access_probe.py --sites data/sites.csv --out data/access_probe_v0.csv

# Audit a single URL
uv run python scripts/run_audit.py --url https://example.com

# Run the weekly pipeline against all sites in data/sites.csv
uv run python scripts/run_weekly.py
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
scripts/        — CLI entry points
data/           — site list, capture artifacts (gitignored)
tests/          — unit + integration tests
docs/           — architecture, references, paper drafts
```

## Status

Stage 0 — scaffolding. See the plan at `~/.claude/plans/proposal-proposal-ai-encapsulated-neumann.md`.
