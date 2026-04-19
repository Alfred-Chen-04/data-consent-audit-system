# Architecture

High-level overview of how the audit system is wired. For audit *definitions*, see [CONCEPTS.md](../CONCEPTS.md). For AI-agent conventions, see [AGENTS.md](../AGENTS.md).

## System diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATION                           │
│   scripts/run_audit.py (single URL) · scripts/run_weekly.py     │
│                  (cron — full site list)                        │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌──────────────────────────┐      ┌──────────────────────────────┐
│      capture.agent       │◄────▶│     llm.vision  (VLM)        │
│  Playwright + Agent loop │      │   locate buttons, bbox        │
│  · launches Chromium     │      │   describe visual features   │
│  · per pathway: find →   │      └──────────────────────────────┘
│    click → screenshot →  │
│    record event          │
│  · outputs CaptureBundle │      ┌──────────────────────────────┐
└────────────┬─────────────┘      │     llm.text  (LLM)          │
             │                    │  disclosure topic coverage,   │
             │                    │  framing analysis, quotes     │
             │                    └──────────────────────────────┘
             │                              ▲       ▲
             ▼                              │       │
┌──────────────────────────┐                │       │
│     capture.fingerprint  │                │       │
│  DOM hash + pHash + embed│                │       │
└────────────┬─────────────┘                │       │
             │                              │       │
             ▼                              │       │
      CaptureBundle ─────┬──────────┬──────┘       │
                         │          │               │
                         ▼          ▼               │
           ┌──────────────────────────────┐         │
           │   layers.layer1 → result     │         │
           │   layers.layer2 → result ◄───┘         │
           │   layers.layer3 → result ◄─────────────┘
           └──────────────┬───────────────┘
                          │
                          ▼
           ┌──────────────────────────────┐
           │    report.generator          │
           │  (Markdown + JSON + PDF)     │
           └──────────────┬───────────────┘
                          │
                          ▼
           ┌──────────────────────────────┐      ┌──────────────┐
           │      storage.db              │◄────▶│   diff.engine│
           │  (PostgreSQL — versioned)    │      │ week-over-wk │
           └──────────────┬───────────────┘      └──────────────┘
                          │
                          ▼
              storage.object_store
              (R2 / S3 — screenshots, DOM snapshots)
```

## Key runtime contracts

1. **`CaptureBundle` is immutable.** Layer scorers never mutate captures; they only emit new result objects. This makes all scoring deterministic given a bundle, which is essential for reproducibility and testing.

2. **One bundle → three layer results → one report.** These four objects are all Pydantic models defined in `src/consent_audit/models/audit.py`. The schemas are the interface between stages.

3. **LLM/VLM output always goes through schema validation.** If a model returns something that fails validation, we retry once with an explicit schema-correction prompt, then fall back to a conservative default with a flag `confidence_low = True`. We never pass un-validated model output downstream.

4. **No LLM call has side effects on DB or storage.** Storage writes happen only in the orchestration layer (`scripts/`) after all scoring is complete.

## Deployment topology (summer MVP)

```
Vercel (Next.js demo) ──┐
                        │ HTTP
                        ▼
                   Cloud VM (1 vCPU / 2 GB, ~$10/mo)
                   ├─ pipeline runtime (APScheduler)
                   ├─ Playwright + Chromium
                   └─ calls out to Anthropic/OpenAI APIs
                        │
                        ├──▶ Supabase Postgres (audit records)
                        └──▶ Cloudflare R2 (screenshots / DOM)
```

This stays within the $4000 SSRP budget comfortably: ~$120/yr VM + ~$0 DB/storage on free tiers + API spend is the main variable.

## Testing strategy

| Level | Scope | When |
|---|---|---|
| **Unit** | Each `layers/*.py` function against fixture `CaptureBundle` JSONs | Every commit |
| **Schema** | Pydantic round-trip on all models | Every commit |
| **Integration** | `capture.agent` against a local static HTML fixture site (`tests/fixtures/sites/`) | Every PR |
| **End-to-end** | Full pipeline on 3 canary real sites | Weekly (same cron as production) |
| **Drift** | LLM/VLM outputs on frozen fixtures — flag if week-over-week JSON diffs beyond threshold | Weekly |

## Failure modes to watch for

- **Cloudflare / CAPTCHA walls** — Playwright gets blocked. Mitigation: detect via HTTP status + DOM pattern, mark site `capture_failed`, skip (don't retry hard — accidental DoS risk).
- **Consent banner hidden by cookie acceptance from prior run** — Playwright must launch with a fresh user-data-dir per site.
- **VLM hallucinated bbox outside image bounds** — validate bbox is inside screenshot dimensions; reject if not.
- **Runaway LLM cost** — budget cap check before each API call (not just at run start).

## Open technical decisions

Tracked in [AGENTS.md §3](../AGENTS.md) and plan §7. Deferred decisions:
1. Which VLM gives best button-bbox grounding — to be benchmarked week 3
2. Whether to use `sentence-transformers` locally or the Anthropic/OpenAI embedding APIs for text fingerprinting
3. Exact Postgres schema — designed in week 1 after Pydantic models stabilize
