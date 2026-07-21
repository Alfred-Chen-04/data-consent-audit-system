# Architecture

High-level overview of the audited local runtime. For audit definitions, see
[CONCEPTS.md](../CONCEPTS.md). For the current project goal and scope, see
[current_project_goal_2026-07-02.md](research/current_project_goal_2026-07-02.md)
and [current_scope_2026-07-01.md](research/current_scope_2026-07-01.md).

## Current Local Runtime (verified 2026-07-22)

```text
CLI / scripts
     |
     v
Playwright capture.agent
  - fresh browser context
  - screenshot + DOM-derived evidence
  - deterministic candidate classification and click replay
     |
     v
CaptureBundle + fingerprint
     |
     +--> Layer 1: deterministic path availability gate
     +--> Layer 2: deterministic path-effort scoring
     +--> Layer 3: deterministic topic/framing/unbiased-choice rules
     |
     v
AuditReport (structured object + Markdown; JSON serialization available)
     |
     +--> local append-only JSONL records
     +--> local sanitized evidence-file copies
     +--> deterministic week-over-week diff + WeeklySummary
```

The `llm/text.py` and `llm/vision.py` modules are no-network fallbacks that
preserve future adapter shapes. They are not imported by the capture or layer
orchestration, and no external model provider is called by the current pilot.

## Current Runtime Contracts

1. **`CaptureBundle` is immutable.** Scorers emit new result objects and do not
   mutate captured evidence.
2. **One bundle -> three layer results -> one report.** Pydantic models in
   `src/consent_audit/models/audit.py` define the stage boundaries.
3. **Final scoring is deterministic in the current runtime.** DOM candidates,
   visible text, stored evidence refs, and fixed rules drive results.
4. **Persistence is local.** `storage/db.py` appends JSONL; the object-store
   module copies sanitized files beneath `data/object_store/`.
5. **Scheduling is external to the repository.** Operators run CLI/scripts;
   an OS scheduler may invoke them, but APScheduler is not implemented here.

## Target Architecture (not implemented)

The following items describe possible continuation work, not current
capabilities:

- schema-validated external LLM/VLM adapters and model benchmarking;
- PostgreSQL/Supabase persistence;
- Cloudflare R2 or another S3-compatible object store;
- an in-process scheduler and hosted browser worker;
- a deployed web demo;
- per-report PDF generation.

Any future model adapter must validate outputs, attach an evidence ref or
screenshot bbox, enforce a per-call budget cap, and have no direct storage side
effects.

## Testing Strategy

| Level | Current coverage |
|---|---|
| Unit | Models, deterministic layer functions, diffing, storage, exports, and helpers |
| Schema | Pydantic validation and round trips |
| Integration | Capture helpers and local fixture-site browser behavior |
| Workflow | CLI/script wrappers, Week 2 controls, evidence exports, and research artifacts |
| Live checks | Explicit operator-run smoke captures; no active weekly scheduler |

## Failure Modes To Watch

- **Cloudflare/CAPTCHA walls**: record `capture_failed` and avoid aggressive retries.
- **Prior consent state**: use a fresh browser context per site.
- **Dynamic navigation churn**: use the DOM snapshot fallback and record warnings.
- **No-visible-banner rows**: do not treat them as banner-path failures without a confirmed coding rule.
- **Missing evidence files**: distinguish a stored reference from a file actually present in the checkout.
- **Future model output**: reject unsupported values or out-of-bounds bboxes before scoring.
