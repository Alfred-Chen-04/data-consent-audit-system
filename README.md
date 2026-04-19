# Dynamic Consent Interface Audit System

**SSRP 2026** · Qianyi (Alfred) Chen · Mentor: Dr. Jagdip Singh

An AI-driven, agent-based, longitudinal audit framework for website consent interfaces (cookie banners, privacy pages). Combines **Vision-Language Models** (for visual analysis of banner screenshots), **Large Language Models** (for content and framing analysis), and **Browser Agents** (for dynamic consent-path traversal).

## Why this project

Current approaches leave a gap:
- **PRISMe** (2025) audits privacy *policy text* with LLMs, but ignores the interface.
- **UMBRA / "Abyss"** (2026) audits banner *interfaces* with rule-based heuristics, but uses no AI and only captures static snapshots.

This project sits in the middle: **multimodal + AI-driven + agent-dynamic + longitudinal**. Built on the Notice-and-Choice framework with a three-layer audit (Path Availability → Path Effort → Transparency & Unbiased Choice).

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
