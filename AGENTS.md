# AGENTS.md — AI Collaboration Guide for This Project

This file tells any AI coding agent (Claude Code, Cursor, Codex, Gemini, etc.) **how to work productively in this repo**. Humans also read this file to understand conventions.

**For the project's what-and-why**, read [README.md](README.md).
**For precise audit definitions**, read [CONCEPTS.md](CONCEPTS.md) — that file is the source of truth for every vocabulary term.

---

## 1. Project identity

- **Name**: Dynamic Consent Interface Audit System
- **Purpose**: Audit cookie-banner / privacy-consent interfaces at three layers (Path Availability → Path Effort → Transparency & Unbiased Choice) using LLM + VLM + browser agent, tracked weekly across a fixed site list.
- **Author**: Qianyi (Alfred) Chen · SSRP 2026 · Case Western Reserve University
- **Mentor**: Dr. Jagdip Singh (Design & Innovation)
- **Academic frame**: Notice-and-Choice (N+C) framework; the AI is *how* we implement the framework, not a replacement for it.
- **Career frame**: Author is training to be an AI Product Manager with data-privacy expertise — favor decisions that showcase explainability, traceability, and user trust over edge-case academic completeness.

## 2. Three non-negotiable design principles

These override any short-term convenience. If an agent finds itself about to violate one, it should stop and ask.

1. **Every audit score must be traceable to concrete evidence.** No floating numbers. Every Layer-2/3 score must link back to a specific DOM element, a screenshot bounding box, or a verbatim text span. This is the explicit lesson learned from PRISMe's user-trust problems.
2. **Separate "detection" from "judgment."** LLM/VLM output goes through a structured schema (Pydantic models in `src/consent_audit/models/`). Scoring rules are deterministic functions over that schema. Never let a model freely emit a final score.
3. **The dynamic path matters, not just the first screenshot.** A site's Layer-1 and Layer-2 values depend on *navigating* — agent must actually attempt each of Accept / Reject / Customize / Dismiss paths. Static single-screenshot analysis is insufficient.

## 3. Tech stack (locked for summer 2026 unless explicitly revisited)

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | Mentor's existing work, ML/LLM ecosystem |
| Package manager | `uv` | Fast, modern, lockfile-based |
| Browser automation | Playwright (Python) | Most reliable headless; accessible to non-expert maintainers |
| Agent control | Custom orchestration using VLM vision calls → Playwright actions | Recommended over Claude Computer Use / Browser Use for audit-trail clarity (see plan §7) |
| VLM | Claude Opus 4.7 vision (primary) · GPT-4o vision (comparison) | Best image grounding; dual-model for validation |
| LLM | Claude Haiku 4.5 (first pass) · Opus 4.7 (complex framing analysis & review) | Cost-aware tiering |
| DB | PostgreSQL (Supabase free tier acceptable for summer) | Versioned records, JSON columns for flexible schema |
| Object storage | S3-compatible (Cloudflare R2 or Supabase Storage) | For screenshots, DOM snapshots |
| Scheduling | `APScheduler` (simple) or a cron on a cheap VM | Weekly pipeline |
| Front-end | Next.js (App Router) on Vercel | Demo site, static timeline browser |
| Data models | Pydantic v2 | Schema enforcement between stages |

## 4. Module boundaries

```
src/consent_audit/
├── capture/    — "what the site looks like right now"
│   ├── agent.py         — Playwright + VLM driver that walks consent paths
│   └── fingerprint.py   — DOM hash + perceptual hash + text embedding
├── layers/     — pure functions that consume Capture output and emit scores
│   ├── layer1_path_availability.py
│   ├── layer2_path_effort.py
│   └── layer3_transparency.py
├── llm/        — thin wrappers around Anthropic / OpenAI SDKs
│   ├── vision.py        — "VLM: describe this banner"
│   └── text.py          — "LLM: classify these disclosures"
├── models/     — Pydantic schemas shared across layers
│   └── audit.py         — CaptureBundle, LayerResult, AuditReport, etc.
├── storage/    — DB and object-store IO only; no business logic
│   └── db.py
├── diff/       — longitudinal comparison between versions
│   └── engine.py
└── report/     — human-readable report assembly
    └── generator.py
```

**Rule**: Each module depends *inward* (layers → models, llm → models, storage → models; never reversed). This keeps the audit framework testable without a live network or DB.

## 5. Coding conventions

- **Type everything.** Run `mypy --strict` on `src/` before merging.
- **Lint with `ruff`** (config in `pyproject.toml`). No exceptions.
- **No magic strings.** Audit dimension names come from `consent_audit.models.dimensions` enums, never literals.
- **Comments**: default to none. Only add a comment when the *why* is non-obvious. Never write docstrings that restate what the function signature already says.
- **No premature abstraction.** If we have 1 VLM provider, write 1 call. Don't invent a `VLMProviderInterface` until we have the second.
- **File-level tests.** Every module in `layers/` has a matching `tests/layers/test_<name>.py` with fixture-based tests.
- **One test per audit dimension** exists before we claim that dimension "works." See `tests/fixtures/` for ground-truth snippets.

## 6. Data flow (one-site audit)

```
URL
 │
 ▼
capture.agent.run(url)
 ├─ launches Playwright
 ├─ takes initial screenshot + DOM snapshot
 ├─ VLM: locate Accept/Reject/Customize/Dismiss candidates → (element_id, bbox)
 ├─ for each pathway: attempt click → record outcome → take new screenshot
 └─ emit CaptureBundle { url, timestamp, layers=[L1 screenshot+DOM, L2 screenshot+DOM, ...], path_outcomes={...} }
 │
 ▼
layers.layer1.score(bundle)      → Layer1Result (availability booleans + missing-paths list)
layers.layer2.score(bundle)      → Layer2Result (effort score + feature JSON + evidence refs)
layers.layer3.score(bundle)      → Layer3Result (transparency score + unbiased-choice score + quotes + bbox refs)
 │
 ▼
report.generator(bundle, [L1, L2, L3]) → AuditReport (Markdown + JSON + PDF)
 │
 ▼
storage.db.save(AuditReport)
storage.object_store.save(screenshots, DOM snapshots)
```

## 7. Cost & API discipline

- **Never call an LLM/VLM without logging the token cost.** Wrapper in `src/consent_audit/llm/` appends to a running ledger per audit run.
- **Cache aggressively.** Use Anthropic prompt caching for Layer-3 framing prompts (the system prompt + schema is static across sites).
- **Haiku first, Opus second.** Default to Haiku for Layer-3 first-pass; escalate to Opus only when Haiku returns low-confidence or fails schema validation.
- **Budget alerts.** Weekly cron must check cumulative API spend against `SSRP_BUDGET_CAP` env var; abort run if exceeded.

## 8. Data & ethics guardrails

- **Sites are public** — we audit consent interfaces as a third party, no authentication, no PII submission.
- **Screenshot PII**: geolocation hints, user-state leaks, or embedded user content can appear in captured screenshots. All artifacts go through `capture.sanitize()` before object-store upload (crop to banner region + blur known PII zones).
- **No scraping of sites that explicitly forbid it in `robots.txt`** for paths we visit. Respect 429/503 with backoff.
- **Site list provenance**: the 80-site list inherited from the PhD mentor requires her approval before public release. Default: keep private unless confirmed.
- **Paper-time review**: before any dataset release, IRB / privacy officer review of the release scope. Flag this to Dr. Singh at week 8.

## 9. How an AI agent should approach a task here

1. **Read [CONCEPTS.md](CONCEPTS.md) first.** Most tasks hinge on precise definitions.
2. **Check the plan at** `~/.claude/plans/proposal-proposal-ai-encapsulated-neumann.md` for the week's target.
3. **Work inside one module at a time.** Don't mix capture + scoring in one PR.
4. **Add tests before claiming done.** A layer module without a fixture test = not done.
5. **Commits are English, imperative, concise** — e.g. `capture: add retry-on-cloudflare to playwright driver`.
6. **If unsure whether a change violates §2 (non-negotiable principles), ask** rather than guess.

## 10. Out-of-scope for summer 2026

These are valid future work but **will not be built before August**:
- Chat / conversational audit UI (deferred to fall semester)
- Mobile-specific auditing (desktop only for now)
- Non-English sites (English only; non-English is a post-summer extension)
- Real-time on-demand audit API beyond the demo site
- B2B SaaS features (auth, multi-tenant, billing) — explicitly not the summer goal

If a task claims to need one of these, it's probably scope creep. Push back.
