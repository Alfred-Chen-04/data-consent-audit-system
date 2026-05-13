# Project Schema — End-to-End

**Purpose**: a single-page master view connecting research question → audit ontology → pipeline → data structures → modules → outputs → users → current status → open decisions.

**Companion docs** (this doc references but does not duplicate):
- [README.md](README.md) — elevator pitch + repo orientation
- [CONCEPTS.md](CONCEPTS.md) — authoritative audit ontology (definitions of every dimension)
- [docs/architecture.md](docs/architecture.md) — technical wiring (how modules connect at runtime)
- [docs/related_work/legal_cheatsheet.md](docs/related_work/legal_cheatsheet.md) — the 8 legal anchors
- [docs/related_work/background_with_citations.md](docs/related_work/background_with_citations.md) — full lit + regulatory + user-ecosystem with citations

If any conflict between this doc and a companion: the companion wins for its domain (CONCEPTS for ontology, architecture for runtime, etc.). This doc is a navigator, not an authority.

---

## 1. Research Question (what we are answering)

### 1.1 Primary academic question
> **"At a population level, how much of the gap between what websites promise about consent (in policy + banner text) and what users actually experience (in the multi-step consent UI + post-consent cookie behavior) can be machine-detected with multimodal AI, longitudinally?"**

### 1.2 Three sub-questions the project decomposes into
1. **Path Availability** — are the four user pathways (Accept / Reject / Customize / Dismiss) present and reachable on the banner?
2. **Path Effort** — does the cost of choosing one path systematically differ from choosing another (size / depth / friction / clarity)?
3. **Transparency & Unbiased Choice** — does the banner truthfully disclose what users are consenting to, and is its presentation symmetric across options?

### 1.3 What we are NOT trying to answer (out of scope)
- Audit of long-form privacy policy text (covered by PRISMe; see §10 open decision 1 on whether to extend).
- Mobile-app permissions (different threat model — PurPliance / A New Hope cover it).
- Server-side data flows / cookie ecosystem graph (Sánchez-Rola line).
- Per-user behavioral effect of banner design (Utz 2019 already did this with N=80k).
- Geopolitical / ownership questions (CFIUS / national-security blocks — cert / audit cannot solve these).

---

## 2. Audit Ontology (3 layers, kept invariant)

> Defined verbatim in [CONCEPTS.md](CONCEPTS.md). Below is the navigator-level summary.

### 2.1 The four consent pathways
```
Accept    — agree to all / optional data processing
Reject    — refuse all / optional data processing
Customize — open settings panel for per-category choice
Dismiss   — close the banner without explicit choice
```

### 2.2 The three audit layers

| Layer | What it measures | Gate? | Output type |
|---|---|---|---|
| **Layer 1 — Path Availability** | Each pathway: present? reachable in ≤2 actions? | **Yes** — if Reject or Customize missing, site flagged High Risk and Layers 2/3 are skipped | 4 booleans + evidence refs |
| **Layer 2 — Path Effort** | Per pathway: 6 sub-features × deterministic weighted sum → [0,1] effort score | No | per-path EffortScore + overall category {Easy / Average / Poor} |
| **Layer 3 — Transparency & Unbiased Choice** | 3.1 Transparency = Disclosure Topic Coverage + Communicative Framing. 3.2 Unbiased Choice = visual/structural asymmetry. **Kept analytically separate.** | No | per-topic letter grade + per-mechanism bias level + 2 letter grades (transparency, unbiased-choice) |

### 2.3 Six Layer-2 sub-features (deterministic weighted sum)

| Sub-feature | Weight | Source |
|---|---|---|
| `button_size_ratio` | 0.25 | VLM |
| `color_contrast` | 0.15 | Pixel arithmetic (WCAG) |
| `layout_symmetry` | 0.15 | VLM |
| `click_depth` | 0.20 | Browser-agent event log |
| `label_clarity` | 0.15 | VLM + LLM joint |
| `immediate_feedback` | 0.10 | Browser-agent event log |

### 2.4 Layer-3 invariants (paper reviewers will check these)
- Transparency vs Unbiased Choice are **separate** scores (don't collapse).
- First-layer disclosures weighted **2×** second-layer (dominant-anchor effect).
- Any **strong_bias** in a single framing mechanism drops one letter grade.
- Every finding carries a **verbatim evidence quote** + element reference.

### 2.5 Longitudinal primitives
- Multimodal fingerprint = `(dom_hash, perceptual_image_hash, text_embedding)` → cheap weekly change detection.
- `ChangeEvent` → atomized week-over-week shifts with magnitude + LLM-authored description.
- `WeeklySummary` → per-site narrative of the week's changes + severity grade.
- **Volatility & Trajectory** are first-class outputs alongside the static Compliance Score — this is the project's signature differentiator (see §6.4).

---

## 3. Pipeline (input → output, conceptual)

```
                           ┌─────────────────────────────────────────┐
data/sites.csv ─────► run_audit / run_weekly ────► CaptureBundle (immutable)
   (URL list,         (orchestrator)                ├── LayerSnapshot ×N
    cohort tags)                                    ├── PathOutcome ×4 paths
                                                    ├── MultimodalFingerprint
                                                    └── event_log
                                                            │
                                                            ▼
                                          ┌──────────────────────────────┐
                                          │   Layer 1 scorer (gate)      │
                                          │   ↳ Layer1Result + gate_pass │
                                          └──────────────┬───────────────┘
                                                         │ if gate_passed
                                                         ▼
                                          ┌──────────────────────────────┐
                                          │   Layer 2 scorer             │
                                          │   ↳ Layer2Result             │
                                          └──────────────┬───────────────┘
                                                         │
                                                         ▼
                                          ┌──────────────────────────────┐
                                          │   Layer 3 scorer             │
                                          │   ↳ Layer3Result             │
                                          └──────────────┬───────────────┘
                                                         │
                                                         ▼
                                          ┌──────────────────────────────┐
                                          │   report.generator           │
                                          │   ↳ AuditReport (md+json+pdf)│
                                          └──────────────┬───────────────┘
                                                         │
                                          ┌──────────────┴───────────────┐
                                          ▼                              ▼
                                  storage.db (Postgres)        storage.object_store (R2)
                                  ↳ AuditReport rows           ↳ screenshots + DOM
                                          │
                                          ▼
                                  diff.engine (week-over-week)
                                  ↳ ChangeEvent ×N
                                  ↳ WeeklySummary per site
```

### 3.1 LLM/VLM contracts (every call obeys these)
1. Output validates through Pydantic schema, retry once on failure, then conservative default + `confidence_low = True`.
2. No LLM/VLM call has DB or storage side effects — writes happen only in orchestration.
3. Budget cap is checked **before each call** (not just at run start).
4. Outputs cite specific evidence (element ref or screenshot bbox); a value without evidence is a schema violation.

---

## 4. Data Structures (Pydantic schemas in `src/consent_audit/models/audit.py`)

> Authoritative source: [src/consent_audit/models/audit.py](src/consent_audit/models/audit.py). Below is the inheritance / containment map.

### 4.1 Evidence primitives (every finding needs one of these)
```
ScreenshotBBox   — pixel region on a screenshot
ElementRef       — DOM selector + xpath + optional bbox + visible_text
EventLogRef      — entry in the agent's action log
```

### 4.2 Capture stage
```
LayerSnapshot           — one layer (1 = banner, 2 = settings panel)
PathOutcome             — agent's attempt on one pathway (success? click_depth? failure_reason?)
MultimodalFingerprint   — (dom_hash, phash, text_embedding)
CaptureBundle           — immutable container of all the above for one site at one time
```

### 4.3 Layer outputs
```
Layer1Result   — 4 booleans + evidence + gate_passed
EffortSubFeature → EffortScore → Layer2Result
TopicCoverageResult ×4
FramingResult ×4
TransparencyResult  ──┐
UnbiasedChoiceResult ─┴── Layer3Result
```

### 4.4 Final unit of persistence
```
AuditReport
  ├── bundle: CaptureBundle           (the inputs)
  ├── layer1: Layer1Result
  ├── layer2: Layer2Result | None     (None if gate failed)
  ├── layer3: Layer3Result | None     (None if gate failed)
  ├── tier: Tier
  ├── report_markdown: str
  ├── report_pdf_ref: str | None
  ├── total_api_cost_usd: float
  └── generated_at: datetime
```

### 4.5 Longitudinal layer
```
ChangeEvent       — one atomized change between two consecutive captures
WeeklySummary     — LLM-authored summary of the week, with severity grade
```

> Every cross-module boundary uses one of these models. If a function takes/returns anything else, it is internal to one module. This is enforced by import discipline.

---

## 5. Module Layout (`src/consent_audit/`)

| Module | What it does | Maps to pipeline step |
|---|---|---|
| `capture/agent.py` | Playwright + browser agent loop — find/click/screenshot/record per pathway | Capture |
| `capture/fingerprint.py` | DOM hash + pHash + text embedding | Capture |
| `capture/sanitize.py` | Strip PII from captured artifacts before storage | Capture |
| `llm/vision.py` | VLM client (bounding-box-grounded prompts) | Layer 2 (visual features) + Layer 3 (unbiased-choice asymmetry) |
| `llm/text.py` | LLM client (text framing + topic-coverage prompts) | Layer 3 (transparency) |
| `llm/budget.py` | Per-run + per-call $ cap enforcement | All LLM/VLM calls |
| `layers/layer1_path_availability.py` | Boolean availability + 2-action gate test | Layer 1 |
| `layers/layer2_path_effort.py` | 6-sub-feature weighted sum | Layer 2 |
| `layers/layer3_transparency.py` | Transparency + Unbiased Choice (kept separate) | Layer 3 |
| `models/audit.py` | All Pydantic models | Cross-cutting |
| `models/dimensions.py` | Enums (Pathway, LetterGrade, BiasLevel, etc.) | Cross-cutting |
| `diff/engine.py` | Week-over-week change detection | Longitudinal |
| `report/generator.py` | AuditReport → markdown + json + pdf | Output |
| `storage/db.py` | Postgres persistence for AuditReports | Output |
| `storage/object_store.py` | R2/S3 for screenshots + DOM snapshots | Output |
| `cli.py` | Entry-point CLI (wraps scripts/) | Operator interface |
| `config.py` | Env / settings / API keys | Cross-cutting |

Scripts (`scripts/`) are operator entry points:
- `access_probe.py` + `access_probe_summarize.py` — Week-0 feasibility (already run).
- `run_audit.py` — single URL.
- `run_weekly.py` — full site list (cron entry).

---

## 6. Inputs, Outputs, and the User-Facing Artifacts

### 6.1 Inputs
- [`data/sites.csv`](data/sites.csv) — URL list, with cohort tags (e.g., `china_overseas_cohort` is an open decision in §10).
- API keys: Anthropic, OpenAI (set via `.env`, never committed; template in `.env.example`).
- LLM/VLM model selection: pinned in `config.py` (currently parameterized for benchmarking; see §10 open decision 5).

### 6.2 Outputs (per audit run)
1. **AuditReport markdown** — human-readable, embedded screenshots.
2. **AuditReport JSON** — machine-readable, full schema, every evidence ref.
3. **AuditReport PDF** — for sharing / archival.
4. **Postgres row** — queryable, indexed by URL + week.
5. **R2 objects** — screenshots, DOM snapshots, event logs.

### 6.3 Aggregate outputs (per longitudinal run, e.g., weekly)
6. **`ChangeEvent` rows** — one per detected meaningful change.
7. **`WeeklySummary` per site** — LLM-authored narrative of the week.
8. **Compliance Trajectory** — improving / stable / degrading.
9. **Compliance Volatility** — low / mid / high.

### 6.4 The three meta-scores reported per site
> These are the project's signature outputs — what differentiates this work from UMBRA (no trajectory) and ConsentDiff (no volatility):

```
Compliance Score        — traditional, comparable with Nouwens/ConsentDiff/UMBRA
Compliance Trajectory   — improving / stable / degrading over the audit window
Compliance Volatility   — magnitude × frequency of week-over-week changes
```

> The headline claim in the paper's abstract: **"A site with stable C-grade compliance may carry less regulatory risk than a site oscillating between A and D."**

### 6.5 Deliverables (Aug 2026 SSRP target)
- Paper draft (methodology + case study of comparable subset, including the static-vs-dynamic comparison if Qiyao agrees)
- SSRP poster
- Public demo website
- Open-source repo
- Public dataset (subject to Qiyao's decision on the 80-site list)

### 6.6 Possible additional deliverable (open — see §10 decision 3)
- **NGO-targeted Evidence Cards** — per finding, a structured evidence package mapping to specific GDPR / ePrivacy article violation + EDPB dark-pattern category + verbatim screenshot/quote/cookie trace. Designed for noyb / The Markup / plaintiffs' lawyers to consume directly.

---

## 7. Users (for whom we are designing the outputs)

Ranked by feasibility of being a first user, per [background_with_citations.md §4.7](docs/related_work/background_with_citations.md):

1. **An academic measurement-privacy lab as host/co-author** (CMU CyLab CUPS, Inria Bielova group, Cambridge / King's). Provides institutional credibility. Best first move.
2. **noyb's technical team** (Vienna). Running 422 → 500+ cookie complaints aiming for 10k/yr. Workflow already wants our output.
3. **CNIL LINC** (France) or equivalent DPA tech team. Built CookieViz themselves — best regulatory existence proof.
4. **The Markup's data team** or comparable nonprofit newsroom. Open-sourced Blacklight Query Oct 2024 — explicitly inviting collaboration.
5. **US plaintiffs' bar** in CIPA / pixel litigation (Cohen Milstein, Edelson PC, Lyon Firm). Strongest dollar incentive but hardest to reach cold.

> [Heuristic from lit] No successful predecessor tool (WebXray, Blacklight, OpenWPM, CookieViz, EXODUS) launched cold from a student GitHub. All had institutional sponsorship + bundled distribution event + visible maintainer. So **adoption strategy = paper publication + one chosen sponsor relationship by 2026-09**.

---

## 8. External Dependencies

- **APIs**: Anthropic Claude (LLM + VLM), OpenAI (fallback / benchmarking).
- **Browser**: Playwright + Chromium (one fresh user-data-dir per site to avoid prior consent contamination).
- **DB**: Postgres / Supabase (free tier sufficient for SSRP scope).
- **Object store**: Cloudflare R2 (S3-compatible, zero egress cost).
- **Schedule**: APScheduler (in-process cron for the weekly run).
- **Budget envelope**: $4,000 SSRP total — ~$120/year for VM, ~$0 for DB+storage on free tiers, **API spend is the main variable** (budget cap enforced per-call in `llm/budget.py`).

---

## 9. Status — What Is Done vs Pending

### 9.1 Done (committed to main)
- [x] SSRP proposal accepted
- [x] Initial codebase scaffold (all module directories + Pydantic models + module skeletons)
- [x] CONCEPTS.md — full audit ontology
- [x] docs/architecture.md — runtime wiring + 4 invariants
- [x] Week-0 access feasibility probe — 6 canary sites validated (BBC, NYT, Reddit, Guardian, Wikipedia, example.com)
- [x] Qiyao's static audit dataset imported (~90 sites with privacy_notice_data.xlsx + screenshots) — available as a baseline for static-vs-dynamic comparison
- [x] Outreach drafts: Dr. Singh network, Haoze Guo (ConsentDiff), LinkedIn playbook, alumni search
- [x] Alignment memo to Dr. Singh + Qiyao (drafted; user decides timing)
- [x] Strategy docs: positioning + future-extension + SSRP scope advisory
- [x] Lit landscape: rubric landscape (7 papers) + comprehensive background (30+ papers, full regulatory map, user ecosystem)
- [x] Legal cheatsheet (8 anchors)

### 9.2 Scaffolded but not yet functional
- [ ] `capture/agent.py` — Playwright skeleton exists; full pathway-traversal logic not written
- [ ] `capture/fingerprint.py` — function signatures exist; implementations stubbed
- [ ] `llm/vision.py`, `llm/text.py` — client wrappers exist; prompts and validation loops not finalized
- [ ] `layers/layer2_path_effort.py` — sub-feature extractors stubbed
- [ ] `layers/layer3_transparency.py` — stubbed
- [ ] `diff/engine.py` — stubbed
- [ ] `report/generator.py` — stubbed
- [ ] `storage/db.py`, `storage/object_store.py` — stubbed
- [ ] `scripts/run_audit.py` and `scripts/run_weekly.py` — entry points exist; integration not wired

### 9.3 Tests
- [x] `tests/layers/test_layer1_path_availability.py` — first layer tests exist
- [x] `tests/test_models.py` — Pydantic model round-trip tests
- [ ] No tests yet for capture, llm, layer2, layer3, diff, report, storage

### 9.4 Documents that are drafted but not yet sent / published
- `docs/alignment_memo.md` — drafted, not yet sent to Dr. Singh + Qiyao (Alfred's decision)
- `docs/outreach/01-04` — drafted, not yet sent

---

## 10. Open Decisions (Alfred makes these; none are blocked on more research)

| # | Decision | Deadline | What I need to know |
|---|---|---|---|
| 1 | Extend scope to include policy-text auditing? Pick from 5 angles: A (VLM execute claim), B (multilingual drift), C (banner-vs-policy text consistency), D (NGO evidence cards), E (temporal claim stability) — or none | Before paper-draft scaffolding (~ end May) | "C" / "D" / "C+D" / "none" / "tell me more about X" |
| 2 | Add `china_overseas_cohort` tag to `data/sites.csv` (~20 sites: Shein/Temu/AliExpress/RedNote-international/Anker-global/etc.) | **2026-05-31** (after this, site selection is frozen) | "yes do B.1" / "no, skip B.1" |
| 3 | Add `EvidenceCard` export schema to `AuditReport` (the Angle D extension — independent of #1) | Any time before report.generator implementation | "add it" / "defer" / "no" |
| 4 | Whether to send alignment_memo and which actions to take on Dr. Singh / Qiyao feedback | Anytime — but earlier unblocks data-set decisions (Qiyao 80-site list) | "send as is" / "edit then send" / "wait" |
| 5 | Which VLM + LLM combination to standardize on (Anthropic Sonnet 4 vs Opus 4.6 vs OpenAI GPT-4o vs Gemini for VLM bbox grounding) | Before any large run (~ end May / early June) | I can run a benchmark of 5-10 sites with each — say "run benchmark" |
| 6 | Whether to make `regulatory_mapping` field on each finding (B.2 advisory — optional GDPR/ePrivacy/EDPB tagging on every output) | Anytime — a few hours of work | "add it" / "defer" / "no" |
| 7 | First-user target post-SSRP (academic lab co-author vs noyb vs CNIL LINC vs The Markup vs plaintiffs' bar) | After SSRP — but the choice shapes design decisions now | "design output for X" / "defer to August" |
| 8 | Whether to keep the Track-2 commercial extension (`docs/strategy/positioning_and_future_extension.md`) or delete it | Any time | "keep" / "delete" |

> Decisions 1-3 plus 6 are the ones that actually shape what code gets written first. Decisions 4-5 are operational. Decision 7-8 are positioning.

---

## 11. Suggested Execution Order (post-decision)

Assuming Alfred makes decisions on #1-#3 + #5 above, here is the natural critical path:

1. **Lock the LLM/VLM choice** (decision 5) → unblocks all `llm/*` implementation
2. **Implement `capture/agent.py`** end-to-end on 5 canary sites → can produce real `CaptureBundle`s
3. **Implement Layer 1** end-to-end → producing real `Layer1Result`s + the gate test
4. **Implement Layer 2 sub-features** one at a time (deterministic ones first: color_contrast, click_depth, immediate_feedback; then VLM-dependent: button_size_ratio, layout_symmetry, label_clarity)
5. **Implement Layer 3 Transparency** (topic coverage + framing analysis with LLM)
6. **Implement Layer 3 Unbiased Choice** (VLM)
7. **Implement `report.generator`** → first real AuditReport
8. **Implement `storage.*`** → first persistence
9. **Implement `diff.engine`** + run on 2 consecutive weeks → first ChangeEvents
10. **Scale to full sites.csv** for one weekly run → first real dataset
11. **Begin paper draft** with the first real dataset as evidence

If Alfred chooses Angle C or D (decision 1) or adds an `EvidenceCard` schema (decision 3), those are inserted between steps 7 and 8 — they extend output, not the audit core.

---

## 12. Boundary Statement

This SCHEMA is a navigator. It compresses what is fully written elsewhere:
- For **definitions** of any audit dimension → CONCEPTS.md is authoritative.
- For **runtime details** of how modules connect → docs/architecture.md is authoritative.
- For **lit / regulatory / user evidence** behind any positioning claim → docs/related_work/background_with_citations.md.
- For **Pydantic field-level specs** → src/consent_audit/models/audit.py.

If reading this doc raises a question, the answer is in one of the above. If reading this doc leaves a decision unmade, it is listed in §10.
