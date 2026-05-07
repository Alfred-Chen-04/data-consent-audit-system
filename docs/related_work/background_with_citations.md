# Background Research with Citations

**Author**: Qianyi (Alfred) Chen, with research assistance from Claude
**Created**: 2026-04-26 (Phase A) | Expanded: 2026-04-26 (Phase B)
**Status**: Complete first pass. Open items flagged inline.
**Companion to**: [`consent_audit_rubrics_landscape.md`](./consent_audit_rubrics_landscape.md) — that doc compares scoring rubrics specifically; this doc is broader background (papers, regulations, enforcement, user ecosystem).

---

## Section 0 — How to Read This Document

This document exists because Alfred asked for a **fully traceable, no-fabrication** background brief. Every factual claim has a citation; every interpretation is labelled.

### Labelling convention

| Tag | Meaning |
|---|---|
| `[FACT]` | A claim with a primary-source URL. Reader should be able to click through and confirm. |
| `[SUMMARY]` | A paraphrase or synthesis of multiple `[FACT]`s in this document. No new claims, just compression. |
| `[INFERENCE]` | The assistant's reasoning beyond the cited facts. **Decision power is 100% Alfred's.** Treat these as discussion starters, not recommendations. |
| `[UNVERIFIED]` | A claim that was searched for but where no primary source could be confirmed. Listed explicitly so Alfred can decide whether to chase it down or drop it. |
| `[CORRECTED]` | A claim the assistant made earlier in conversation that turned out to be wrong on verification. Listed in §6. |

### Boundary statement

This document **does not** make decisions for Alfred. It separates fact from inference, lists what's verified and what's not, and stops short of recommending. If Alfred wants to take any of the inferences as decisions, that is his call. If he wants to challenge any `[FACT]`, he can click the citation.

---

## Section 1 — Academic Literature Map

### Section 1.1 — The Three Papers Alfred Already Knows About

#### 1.1.1 PRISMe (CHI 2026) — VERIFIED ✅

> [CORRECTED] The assistant previously described PRISMe as "PRISMe (2025)". The arxiv submission is from January 2025 [1], but the **actual venue is ACM CHI 2026** [1]. The latest revision is January 2026 [1]. So citing it as "PRISMe (CHI 2026)" is accurate.

`[FACT]` Full title: **"Helping Johnny Make Sense of Privacy Policies with LLMs"** [1].
`[FACT]` Authors: **Vincent Freiberger, Arthur Fleig, Erik Buchmann** [1].
`[FACT]` First arxiv submission 2025-01-27; latest revision 2026-01-28. Venue: **ACM CHI 2026** [1].
`[FACT]` What it does: an interactive browser extension combining LLM-based policy assessment with a dashboard and customizable chat interface; user study N=22; investigates RAG to mitigate hallucinations [1].
`[FACT]` Input: **privacy policy text only** — not cookie banners or consent UI [1].

> [SUMMARY] PRISMe is a CHI-flavored, user-study-driven, LLM-based privacy policy explainer for end users. The artefact is a browser extension + dashboard + chat, not a large-scale audit pipeline. See §1.4 for non-overlapping angles.

#### 1.1.2 UMBRA / "When the Abyss Looks Back" — VERIFIED ✅, EARLIER CHARACTERIZATION PARTIALLY WRONG ⚠️

> [CORRECTED] The repo's `README.md` and the assistant's earlier summary said UMBRA "audits banner interfaces with rule-based heuristics, but uses no AI and only captures **static snapshots**". Verification:
> - "Rule-based heuristics, no AI/LLM" — **confirmed** [3]
> - "Only static snapshots" — **wrong**. UMBRA explicitly does **interaction tracing + cookie-state monitoring** to "capture multi-step consent flows missed by prior tools" [3]. Whether it is **longitudinal** (same site at multiple time points) was not extractable from the abstract; treat as `[UNVERIFIED]` until full PDF read.

`[FACT]` Full title: **"When the Abyss Looks Back: Unveiling Evolving Dark Patterns in Cookie Consent Banners"** [3]. UMBRA is the system name within that paper.
`[FACT]` Authors: **Nivedita Singh, Seyoung Jin, Hyoungshick Kim** [3]. Affiliations not on arxiv landing page (`[UNVERIFIED]`). Hyoungshick Kim is publicly affiliated with Sungkyunkwan University (Korea), but verify before citing.
`[FACT]` arxiv 2026-03-23, ID **2603.21515**, category cs.CR [3].
`[FACT]` Method: text analysis + visual heuristics + interaction tracing + cookie-state monitoring; rule-based, no LLM/VLM [3].
`[FACT]` Sample 14,000 websites; 99% accuracy on hand-annotated ground truth; on sites with revocation barriers, cookies increase by 25% on average [3].

> [SUMMARY] UMBRA is more capable than the README suggested. It does multi-step interactive flows + cookie-state monitoring, just without LLM/VLM. The defensible differentiators for Alfred are now: (1) AI-grounding, (2) longitudinal depth, (3) Layer 3 framing, (4) volatility/trajectory as primary metric. See §1.3 cube and §5 inferences.

#### 1.1.3 ConsentDiff at Scale — VERIFIED ✅

`[FACT]` Full title: **"ConsentDiff at Scale: Longitudinal Audits of Web Privacy Policy Changes and UI Frictions"** [2].
`[FACT]` Single author: **Haoze Guo** [2]. arxiv ID **2512.04316**. First submission 2025-12-03. Latest revision v7 2026-04-13.
`[FACT]` Method: monthly snapshots + DOM signals + screenshot cues + semantic alignment of policy clauses; weighted claim-UI alignment score [2]. Sample (per existing rubric landscape doc [4]): 2,400 domains × 9 months = 21,600 snapshots; geo: EU 900, US-CA 1000, Other 500.

### Section 1.2 — Additional Verified Papers (22 papers, with cube positioning)

These are papers BEYOND the 7 already in [`consent_audit_rubrics_landscape.md`](./consent_audit_rubrics_landscape.md) (Nouwens 2020, Matte 2020, Utz 2019, Bielova 2024, Qu 2025) and the 3 above. Per-paper format: authors / venue / URL / 2-sentence method / "what it does NOT do".

#### Banner-UI auditing (DOM / heuristic / classical-ML lineage)

**P1. Bouhoula et al., USENIX Security 2024 — Automated Large-Scale Analysis of Cookie Notice Compliance** [5].
- CMP-agnostic crawler, 97k EU sites, LLM classifier (95.1%) on accept/reject/save/settings buttons. 48,843 with detectable banners; 16,231 with reject. Detects implicit consent, dark patterns, post-rejection AA-cookie violations.
- Single-snapshot (Mar 2023 CrUX). DOM + LLM-button-classifier.
- Does not: traverse nested settings; longitudinal re-crawl; analyze the linked policy text.

**P2. Bollinger et al., USENIX Security 2022 — CookieBlock** [6].
- XGBoost on cookie attributes (name/domain/expiry/content) → predict purpose without site cooperation. ~30k sites; mean validation 84.4%. Detects 6 GDPR violation types at the cookie-object level.
- Single-snapshot. Classical ML on cookie metadata.
- Does not: analyze banner UI / dark patterns / policy text.

**P3. Khandelwal et al., USENIX Security 2023 — CookieEnforcer** [7].
- Browser extension that locates the cookie notice, predicts the click sequence to disable non-essential cookies (T5 fine-tuned on rendered text), executes the clicks. 500 top sites, 91% effective.
- Single-snapshot. Text-ML + DOM action prediction.
- Does not: audit whether rejection actually stops trackers post-click; longitudinal; policy-text alignment.

**P4. Hils, Woods & Böhme, IMC 2020 — Measuring the Emergence of Consent Management on the Web** [8].
- 161M browser crawls measure CMP adoption growth June 2018 → June 2020; 12% of sites send the consent signal *before* user choice; controlled lab experiments on time-cost.
- Longitudinal 24 months. DOM/network heuristic.
- Does not: enter banner interactively beyond first screen; per-site dark-pattern taxonomy; policy text.

**P5. Kretschmer, Pennekamp & Wehrle, ACM TWEB 2021 — Cookie Banners and Privacy Policies: Measuring the Impact of the GDPR on the Web** [9].
- 42-page systematic measurement linking GDPR introduction to changes in banner prevalence, CMP adoption, privacy-policy length/readability.
- Longitudinal pre/post-GDPR. Heuristic + statistics.
- Does not: deep banner interaction; LLM/VLM; pre-LLM era.

**P6. Tang, Bui & Shin, USENIX Security 2025 — ConsentChk: Navigating Cookie Consent Violations Across the Globe** [10].
- End-to-end measurement system with formal model of cookie-consent violations. 1,793 popular sites × 8 English-speaking regions. Region-dependent violation rates.
- Single-snapshot, geographically distributed. DOM + formal model.
- Does not: VLMs/LLMs; visual dark patterns; policy text.

**P7. Rasaii et al., IMC 2023 — Thou Shalt Not Reject: Analyzing Accept-Or-Pay Cookie Banners** [11].
- First automated analysis of "cookie walls" / pay-or-tracking. Quantifies subscription-vendor adoption across EU news.
- Single-snapshot. DOM heuristic crawler ("BannerClick").
- Does not: banner internals beyond the wall; policy text; AI-based classification.

**P8. Rasaii et al., 2025 (arxiv preprint, MPI-INF) — Intractable Cookie Crumbs** [12].
- Stateful crawls on 20k+ domains; identifies cookies set on banner-accepted sites that persist and leak to trackers on later sites where the user has not consented. Shows GPC reduces these by ~30%.
- Stateful sequential. No ML; no LLM.

**P9. Hausner & Gertz, CHI Workshop / arxiv 2021 — Dark Patterns in the Interaction with Cookie Banners** [13].
- 4,695 most-visited German sites; enumerates dark-pattern strategies (Privacy Zuckering, asymmetric framing).
- Single-snapshot. Heuristic + manual annotation.

**P10. Soe, Santos & Slavkovik, MADWeb 2022 — Automated Detection of Dark Patterns in Cookie Banners: How to Do It Poorly...** [14].
- Classical ML on 300 annotated news-site banners (NordiCHI dataset). **Negative-result paper** — explicitly reports the approach fails and explains why.
- Single-snapshot. Classical ML.

**P11. Soe, Nordberg, Guribye & Slavkovik, NordiCHI 2020 — Circumvention by Design** [15].
- Manual analysis of 300 cookie consents from Scandinavian/UK/US news outlets across 42 countries. Develops the dark-pattern taxonomy (nagging, obstruction, sneaking, etc.) for the consent setting.

**P12. Santos, Rossi, Sanchez Chamorro, Bongard-Blanchy & Biczók, WPES 2021 — Cookie Banners, What's the Purpose? Analyzing Cookie Banner Text Through a Legal Lens** [16].
- Legal-NLP analysis of ~400 banner texts across popular EU-visited sites; 61% use vague language. Releases labeled "purposes" dataset later reused by Bouhoula 2024.
- Single-snapshot. Manual annotation + light NLP, legal lens.
- Does not: analyze banner UI/visuals; check whether stated purposes match actual cookie behavior.

**P13. Mathur et al., CSCW 2019 — Dark Patterns at Scale: Findings from a Crawl of 11K Shopping Websites** [17].
- First large-scale dark-pattern crawl. 1,818 dark patterns across 1,254 of 11k shopping sites; 15-type taxonomy.
- Shopping context, NOT consent — but the taxonomy is the parent of all later consent dark-pattern work.

**P14. Mathur, Mayer & Kshirsagar, CHI 2021 — What Makes a Dark Pattern... Dark? Design Attributes, Normative Considerations, and Measurement Methods** [18].
- Conceptual paper articulating *what makes* something a dark pattern. Design-attribute / normative-perspective / measurement-method axes.
- No empirical detection — but is the conceptual scaffolding any audit must align to.

**P15. Habib et al., CHI 2022 — "Okay, whatever": An Evaluation of Cookie Consent Interfaces** [19].
- Two-stage usability assessment: (1) 191 banners against 5 dark-pattern heuristics; (2) 1,109-participant between-subjects experiment varying 7 design parameters.
- Single-snapshot. Heuristic + RCT.

**P16. Gunawan, Pradeep, Choffnes, Hartzog & Wilson, CSCW 2021 — A Comparative Study of Dark Patterns Across Mobile and Web Modalities** [20].
- Manual cross-modality test of 105 services across mobile-app / mobile-browser / web-browser. Documents how dark patterns differ across modalities.

**P17. Sánchez-Rola et al., AsiaCCS 2019 — Can I Opt Out Yet? GDPR and the Global Illusion of Cookie Control** [21].
- 2,000-site empirical study. **92% track before consent; only 2.5% delete cookies post-rejection; >75% of tracking happens before any user choice.**

**P18. Sánchez-Rola et al., IEEE S&P 2021 — Journey to the Center of the Cookie Ecosystem** [22].
- Cookie-creation chains and inter-organizational cookie-sharing across 6M webpages (~138M cookies). Ecosystem-level not banner-UI-level.

#### Privacy-policy NLP / LLM lineage

**P19. Andow et al., USENIX Security 2019 — PolicyLint: Investigating Internal Privacy Policy Contradictions on Google Play** [23].
- Symbolic-NLP system; auto-builds ontologies from policy corpus; finds 14.2% of 11,430 app policies contain contradictions.

**P20. Cui et al., USENIX Security 2023 — PoliGraph: Automated Privacy Policy Analysis using Knowledge Graphs** [24].
- Builds KGs from policy text; PoliGrapher-LM uses LLM prompting instead of NLP pipelines. Identifies 40% more collection statements than prior SOTA at 97% precision.

**P21. Harkous, Fawaz, Lebret, Schaub, Shin & Aberer, USENIX Security 2018 — Polisis / PriBot** [25].
- Pre-LLM hierarchy of 22 neural classifiers on a 130k-policy embedding model + chatbot answering free-form questions about a policy.

#### VLM/agent stack (CRITICAL — closest to Alfred's stack)

**P22. Grossman, Smith, Borcea & Chen, 2025 (arxiv) — Using Salient Object Detection to Identify Manipulative Cookie Banners** [26].
- **First paper to apply a vision salient-object-detection model on banner screenshots** to quantify aesthetic manipulation (how attention-drawing each button is). Finds aesthetic manipulation on 38% of "compliant" banners. 2,579 sites.
- Vision-only. No LLM reasoning, no policy text, no multi-step interaction, no longitudinal.

**P23. Pohle, Hagedorn & Federrath, ARES 2023 — Cookiescanner** [27].
- Open-source tool; extracts banner candidate elements; evaluates whether they offer a decline option / use color diversion. Tranco top-1k.

**P24. Zharmagambetov et al., NeurIPS D&B 2025 — AgentDAM: Privacy Leakage Evaluation for Autonomous Web Agents** [28].
- Benchmark for whether AI web-navigation agents (GPT-4 / Claude / Llama-3) leak unnecessary sensitive info while completing web tasks. Inverted use case — agents *as* the privacy threat.
- **Relevant**: provides agent-harness scaffolding Alfred could reuse.

**P25. Hu et al., 2026 (arxiv) — WebSP-Eval: Evaluating Web Agents on Website Security and Privacy Tasks** [29].
- Benchmark of 200 task instances over 138 tasks across 28 sites — agents asked to manage cookie preferences, configure privacy settings, revoke sessions. WebVoyager + Chrome extension. **Toggles/checkboxes cause ≥45% failure** in current VLM agents.
- Relevant: closest existing public infrastructure for VLM browser-agent privacy work; the 45% failure rate is a measurable baseline Alfred can build against.

**P26. Aonghusa et al., 2025 (arxiv) — Privacy Practices of Browser Agents** [30].
- Systematic eval of 8 popular browser agents across 15 privacy measurements. Finds 30 vulnerabilities (e.g., autocompleting sensitive form fields, disabled browser privacy).

**P27. Zheng et al., PETS 2026 — AudAgent: Automated Auditing of Privacy Policy Compliance in AI Agents** [31].
- Runtime monitor that parses an AI agent's stated privacy policy with an ensemble LLM, runs Presidio-based detection, auto-checks ontology alignment.
- Audits *agents*, not websites. But the LLM policy-parsing ensemble is a methodological building block.

**P28. Pan et al., USENIX Security 2024 — A New Hope: Contextual Privacy Policies for Mobile Applications** [32].
- Generates contextual, in-situ privacy notices for mobile apps using LLMs. Aligns app screen context with policy clauses.

**P29. Bui et al., CCS 2021 — PurPliance** [33].
- Detect mismatches between stated data-usage purposes in mobile-app policies vs what the app does over the network. 23.1k Android apps; 18.14% policy contradictions; 69.66% flow-policy inconsistencies.

**P30. Kampanos & Shahandashti, IFIP SEC 2021 — Accept All: The Landscape of Cookie Banners in Greece and the UK** [34].
- Two-country focused study; DOM heuristic + manual coding.

> [INFERENCE] **The single most important finding from this lit review for Alfred** is the existence of **WebSP-Eval (P25)** + **AgentDAM (P24)** + **CookieEnforcer (P3)**. Combined, they prove (a) VLM browser agents on privacy tasks are now an active subfield, (b) reusable open infrastructure exists, (c) interactive multi-step on banners has been done with classical ML, but no paper has combined VLM-agent-action-execution × multi-step × banner × longitudinal end-to-end. UMBRA covers 3/4 (rule-based + interactive + 14k-cross-section); ConsentDiff covers 3/4 (DOM+screenshot longitudinal); WebSP-Eval covers 3/4 (VLM-agent + interactive + privacy-task — but no longitudinal audit). The four-way intersection is open, but Alfred should be careful to position against UMBRA + ConsentDiff explicitly in the paper's Related Work.

### Section 1.3 — 3D Positioning Cube

Three axes:
- **Time (A1)**: S = static / I = multi-step interactive / L = longitudinal multi-month
- **Method (A2)**: R = rule/heuristic / M = classical ML or weak supervision / A = LLM/VLM (AI)
- **Modality (A3)**: B = banner UI / P = policy text / X = multimodal (UI + policy + cookies + interaction)

| Paper | Time | Method | Modality | Cell |
|---|---|---|---|---|
| **PRISMe** [1] | S | A | P | S-A-P |
| **UMBRA** [3] | I | R | X | I-R-X |
| **ConsentDiff** [2] | L | A* (weak-sup vision) | X | L-M-X |
| Bouhoula 2024 [5] | S | A (LLM-classifier) | B | S-A-B |
| CookieBlock [6] | S | M | cookies-only | S-M-other |
| CookieEnforcer [7] | I | M | B | I-M-B |
| Hils 2020 [8] | L | R | B | L-R-B |
| Kretschmer 2021 [9] | L | R | B+P | L-R-X(weak) |
| ConsentChk [10] | S | R | B | S-R-B |
| Rasaii 2023 [11] | S | R | B | S-R-B |
| Rasaii 2025 [12] | I | R | cookies-state | I-R-other |
| Hausner 2021 [13] | S | R | B | S-R-B |
| Soe 2022 [14] | S | M | B | S-M-B (negative result) |
| Soe 2020 [15] | S | R | B | S-R-B |
| Santos 2021 [16] | S | R + light NLP | banner-text | S-R-P(banner) |
| Mathur 2019 [17] | S | R | B(shopping) | S-R-B |
| Habib 2022 [19] | S | R + RCT | B | S-R-B |
| Gunawan 2021 [20] | S | R | B(cross-modal) | S-R-B |
| Sánchez-Rola 2019 [21] | S | R | cookies | S-R-other |
| Sánchez-Rola 2021 [22] | S | R | ecosystem | S-R-other |
| PolicyLint 2019 [23] | S | M (symbolic) | P | S-M-P |
| PoliGraph 2023 [24] | S | M→A | P | S-A-P |
| Polisis 2018 [25] | S | M (DL) | P | S-M-P |
| Grossman 2025 [26] | S | A (vision-only) | B | S-A-B |
| Cookiescanner 2023 [27] | S | R | B | S-R-B |
| AgentDAM 2025 [28] | S | A | agent-eval | S-A-meta |
| WebSP-Eval 2026 [29] | I | A | privacy-task agent eval | I-A-meta |
| AudAgent 2026 [31] | I | A | P (for agents) | I-A-P-meta |
| PurPliance 2021 [33] | S | M | mobile P+net | S-M-other |

**Crowded cells** (avoid): S-R-B (≥8 papers); S-A-P (PRISMe + PoliGraph + Polisis variants); the "agent-eval meta" cell suddenly hot (AgentDAM, WebSP-Eval, Browser-Agent-Privacy 2025, AudAgent 2026).

**Empty / sparse cells** (real estate):
- **L-A-B** — longitudinal × VLM/LLM × banner-only. Hils is L but rule-based; Grossman is A but single-snapshot. Empty.
- **I-A-B** — multi-step interactive × VLM × banner. UMBRA is I but rule-based; CookieEnforcer is I but classical ML. Empty (closest = WebSP-Eval but it audits agents, not banners).
- **L-A-X with VLM-agent-driven action execution** — partly covered by ConsentDiff with screenshots+DOM, but no VLM-agent execution. Open.
- **L-A-multilingual** — almost no longitudinal AI work outside Anglosphere. Open.

### Section 1.4 — Five Angles for Auditing Policy Text Without Overlapping PRISMe

> [INFERENCE — ALFRED DECIDES]
>
> PRISMe = LLM explainer of privacy-policy text *to end users*, single-snapshot, no UI grounding. Below are five angles that all cite PRISMe in Related Work without competing with it. Each is scored on overlap-with-PRISMe / novelty-vs-ConsentDiff / 10wk-feasibility.

**Angle A — Claim-Action Alignment via VLM Agent Execution**
- One-sentence: Extract specific factual claims from policy text ("you can withdraw consent at any time", "we do not sell data to advertisers") and use a VLM browser agent to *attempt* the action and verify whether the deployed UI/cookies actually execute that claim.
- Overlap with PRISMe: **low** (PRISMe explains; this audits).
- Novelty vs ConsentDiff: **medium** (ConsentDiff already does claim-UI alignment via screenshots+DOM — differentiator is *VLM agent attempting the action* rather than checking element presence).
- Feasibility 10wk: **medium-high**. Reuse WebSP-Eval [29] scaffolding; pick 5–10 high-frequency claim types; 200–500 sites.

**Angle B — Multilingual / Jurisdictional Drift Audit**
- One-sentence: Audit the same privacy policy across language versions (EN / ZH / DE / etc.) and across jurisdictional pages to find clauses that exist in one and not another.
- Overlap with PRISMe: **low**.
- Novelty vs ConsentDiff: **high** (ConsentDiff is anglophone).
- Feasibility 10wk: **medium** (translation/embedding alignment non-trivial; pick 50 multinational vendors).

**Angle C — Banner-Text vs Policy-Text Internal Consistency**
- One-sentence: Compare claims in the privacy policy against banner copy ("Reject All" button shown on banner — does the policy still treat tracking as opt-out?).
- Overlap with PRISMe: **low**.
- Novelty vs ConsentDiff: **medium-high** (ConsentDiff aligns policy with UI elements; this aligns *policy text* with *banner text* — a semantic micro-corpus problem).
- Feasibility 10wk: **high** (narrowly scoped; no agent infra needed beyond rendering + text alignment).

**Angle D — NGO-Targeted Evidence Cards**
- One-sentence: For each audited site, generate a structured evidence card (claim verbatim → UI test result → screenshot → cookie trace) optimized for NGO/regulator complaints rather than academic readers.
- Overlap with PRISMe: **low**.
- Novelty vs ConsentDiff: **medium** (ConsentDiff produces metrics; this produces actionable evidence packages).
- Feasibility 10wk: **high** (aligns with Alfred's NGO-evidence positioning track per `project_positioning_strategy.md` track 1).

**Angle E — Temporal Claim Stability**
- One-sentence: Track which specific factual claims in policies survive/disappear across CMP migrations and template refreshes; flag silent removals of user-favorable clauses.
- Overlap with PRISMe: **low**.
- Novelty vs ConsentDiff: **medium** (ConsentDiff measures clause-level churn at scale; angle E is narrower — which *user-favorable* clauses silently die — and pairs each disappearance with the UI change accompanying it).
- Feasibility 10wk: **medium** (needs longitudinal corpus; the Princeton-Leuven Privacy Policy Corpus [35] is a starter dataset).

> [INFERENCE — synthesis] Angle C is the cheapest and least crowded; Angle A has the highest novelty-vs-ConsentDiff. Angle D is the right framing for an NGO-evidence positioning. Multiple angles can be combined in a single paper if scoped carefully. **Final selection is Alfred's decision.**

---

## Section 2 — Regulatory & Legal Framework

### 2.1 GDPR core articles

The full consolidated GDPR text is on EUR-Lex [36]. Article-by-article mirror at gdpr-info.eu where convenient.

**Art. 3 — Territorial scope (extraterritorial reach)**
- 3(1): controllers established in the Union, regardless of where processing occurs.
- 3(2): non-EU controllers when offering goods/services to EU data subjects OR monitoring their behaviour.
- EDPB authoritative interpretation: Guidelines 3/2018 [37].
- Real cases applied to non-EU companies:
  - **Clearview AI (US)**: Dutch DPA fined €30.5M on 2024-05-16 for scraping EU faces; Italian, French, and Greek DPAs each separately imposed €20M fines in 2022 [38][39].
  - **OpenAI (US)**: Italian Garante fined €15M on 2024-12-20 — Art. 3(2)(a) jurisdiction over a US controller offering services to Italians [40][41]. **NOTE**: Court of Rome **annulled** this fine on 2026-03-18 after suspending it on 2025-03-21.

**Art. 6 — Lawfulness of processing (six grounds)** [42]
1. **Consent** — Italian Garante v. OpenAI 2024 found no valid consent for training data [40].
2. **Contractual necessity** — Irish DPC v. Meta 2023 (€390M) rejected Meta's reliance on contractual necessity for behavioural advertising.
3. **Legal obligation** — used routinely for tax/AML; few standalone enforcement cases.
4. **Vital interests** — narrow; rarely litigated.
5. **Public task / official authority** — Polish Poczta Polska 2025 (€6.4M, electoral data without legislative basis) [43].
6. **Legitimate interest** — CJEU C-621/22 (Oct 2024) and EDPB Guidelines 1/2024 [44] confirmed commercial marketing can qualify, but only after a strict three-part test.

**Art. 7 — Conditions for consent**
The four conditions ("freely given, specific, informed, unambiguous") are stated in the **definition** at Art. 4(11). Art. 7 itself contains the **conditions**: demonstrability; clearly distinguishable presentation; right to withdraw at any time as easily as it was given; assessment of "freely given" when contract performance is conditioned on consent [45][36].

**Arts. 12–14 — Transparency**
Art. 12 (clear/intelligible/accessible form), Art. 13 (direct collection), Art. 14 (indirect collection). Garante v. OpenAI cited transparency failures explicitly [40].

**Art. 22 — Automated decision-making and profiling**
Restricts solely-automated decisions producing legal/similarly significant effects. Landmark case: **CJEU C-634/21 SCHUFA Holding (Scoring), 7 December 2023** — credit-score generation by a credit bureau is itself an Art. 22 "decision" when lenders rely heavily on it [46][47].

**Art. 32 — Security of processing**
Irish DPC v. Meta, 2024-09-27, fined Meta €91M for storing user passwords in plaintext (Art. 32 violation) [48]. The 2024-12-17 €251M Meta fine was framed under Arts. 25(1)/25(2)/33(3)/33(5) [49].

**Arts. 42–43 — Certification mechanisms**
- Art. 42(5) provides for an EDPB-endorsed "European Data Protection Seal."
- **Europrivacy** approved by EDPB Opinion 28/2022 (10 Oct 2022) [50] as the first such seal.
- EDPB Opinion 14/2026 [51] approved updated criteria, expanding scope to (i) Art. 3(2) third-country controllers and (ii) use as an Art. 46 transfer tool.
- Operationally distinct from **EuroPriSe Cert GmbH** (wound down 2025-05-30) which was a separate, older industry seal — *not* the Art. 42(5) endorsed scheme.

**Art. 79 — Judicial remedy by data subjects**
Direct right of any data subject to bring proceedings against a controller/processor in EU courts of habitual residence or defendant's establishment.

**Art. 80 — NGO representation**
- 80(1): non-profit body active in data-protection rights may, on a data subject's mandate, lodge complaints (Art. 77), seek judicial remedy (Arts. 78, 79), claim compensation (Art. 82).
- 80(2): Member States *may* allow such bodies to act independently of any mandate. Germany, France, Italy, Belgium have implemented liberally; others have not [52].
- Example: **CNIL fine against Google €50M (Jan 2019)** triggered by joint Art. 80 complaints from **noyb + La Quadrature du Net** [53][54].

### 2.2 ePrivacy Directive vs GDPR — why cookies aren't a GDPR question

- Cookie consent is governed by Art. 5(3) of Directive 2002/58/EC, transposed into each Member State's national law.
- **CNIL has explicitly held that the GDPR's "one-stop-shop" cooperation mechanism does NOT apply to ePrivacy enforcement** — each national DPA can act independently for cookie violations affecting its territory [55][56].
- Practical implication: a multinational cannot route all cookie-related actions through Ireland (GDPR lead-supervisor) — **27 DPAs can act in parallel**.
- DPA decision applying ePrivacy: CNIL v. Google + Amazon, 2020-12-07 — €60M against Google LLC + €40M against Google Ireland + €35M against Amazon Europe Core under **Art. 82 of the French Loi Informatique et Libertés** (transposing Art. 5(3) of Directive 2002/58/EC) [57][58].
- More recent: CNIL v. Google **€325M** on 2025-09-03 (advertising in Gmail inbox, again under Art. 82 LIL / ePrivacy) [59][60].

**ePrivacy Regulation status (2025–2026)**
- The European Commission **withdrew** the proposal. Announced in 2025 Work Programme on 2025-02-11; formally approved at the Commission's 2533rd meeting on 2025-07-16; published in the Official Journal on 2025-10-06. Stated reason: "no agreement is expected from the co-legislators" and "outdated in view of recent legislation" [61][62][63].
- This is **separate** from EuroPriSe Cert GmbH wind-down (2025-05-30) — three different "ePrivacy" things to keep separate: (i) ePrivacy Directive (still in force), (ii) ePrivacy Regulation proposal (now dead), (iii) EuroPriSe Seal (wound down).

### 2.3 Other privacy regimes

**CCPA / CPRA (California)** — California Civil Code §§1798.100 et seq. Rights to know / delete / opt-out of sale-share / non-discrimination / correction / opt-out of sensitive PI use. Enforcers: California AG + CPPA (post-CPRA). The 30-day cure period was effectively eliminated by CPRA on 2023-01-01 for AG actions.
- **Sephora settlement (2022-08-24)**: First public CCPA enforcement; $1.2M penalty for failing to disclose sale of PI and to honor Global Privacy Control [64][65].

**CPPA recent actions (2025)**
- **Tractor Supply — $1.35M, 2025-09-30** (largest CPPA admin fine to date; opt-out signal failures, contracting failures) [66][67].
- **American Honda — $632,500** [68].
- **Todd Snyder — $345,178** [69].
- **Background Alert (data broker)** — settlement requiring shutdown or fine, plus a sweep of unregistered data brokers under the Delete Act.

**Section 5 FTC Act** — "Unfair or deceptive acts or practices."
- 2024 was the most aggressive privacy year on record, including 19 AI-related actions [70].
- **X-Mode Social / Outlogic, 2024-01-09** — first FTC ban on use/sale/disclosure of sensitive location data [71].
- **InMarket Media** — second location-data action 9 days later.
- **Avast, 2024-02-22** — settled for selling browsing data despite anti-tracking promises.
- **Blackbaud** — first standalone Section 5 unfairness for unreasonable retention plus inaccurate breach notice [72].
- **Historical anchor**: FTC v. TRUSTe 2014 (already verified §6).

**CIPA (California Invasion of Privacy Act)** — pen-register / chat-tracking class actions
- $5,000 per-violation statutory damages → estimated **50,000–100,000+ filings since 2022** [73][74].
- Representative cases:
  - **Greenley v. Kochava** (S.D. Cal. 2023) — early pen-register claim against an SDK provider.
  - **Licea v. Hickory Farms** — chat-widget session-replay claim (representative of hundreds of similar 2023-2024 filings).
  - **Torres v. Prudential Financial** (N.D. Cal., April 2025) — court required evidence of an actual *read*, not mere capture, for §631(a) liability [75].
  - **Thomas v. Papa John's** — pen-register claim against website chat tools (federal courts split with state) [76].
  - **Smith v. Yeti / similar** — IP-address-only claims, dismissed in 2024–2025 California state court rulings finding IP alone is not an "outgoing communication" for §638.51 [77].
- **`[INFERENCE]`**: specific case captions for some are paraphrased from cited surveys; verify exact docket numbers via PACER for academic citation.
- Legislative effort: **SB 690** passed CA Senate unanimously but stalled in Assembly — delayed to ≥2026 session [78].

**BIPA (Illinois Biometric Information Privacy Act)** — 740 ILCS 14/. Written consent required; private right of action with $1,000 / $5,000 per-violation damages.
- **2024-08-02 Amendment (SB 2979)** reduces "per-scan" liability — repeated collection of same biometric from same person is now a single violation; clarifies electronic signatures suffice [79][80].
- Settlements: Facebook $650M, TikTok/ByteDance $92M, Google $100M, Clearview AI $51.75M (2025), Speedway $12.1M [81][82].

**VPPA (Video Privacy Protection Act, 18 U.S.C. §2710)** — ~200 cases/year recently; 28 filed in first two months of 2025 alone [83]. **Circuit split**: 2nd Circuit (broad consumer) vs 6th Circuit (narrow). Second Circuit also held Meta-Pixel-transmitted strings are not "PII" for VPPA [84]. **Supreme Court cert granted Jan 2026** in *Salazar v. Paramount Global* on definition of "consumer" [85].

**PIPL / CSL / DSL (China)**
- PIPL effective 2021-11-01.
- **Didi Global, July 2022 — RMB 8.026B (~USD 1.2B)** for combined CSL/DSL/PIPL violations [86][87].
- **2025-02-14 CAC Measures for Personal Information Protection Compliance Audits** (effective 2025-05-01): mandatory biennial audit if processing >10M individuals' data [88].
- May 2025: Shanghai authorities penalized a European luxury brand's Shanghai subsidiary for unlawful cross-border PI transfer to French HQ — **first publicly disclosed cross-border-transfer PIPL action** [88].

**LGPD (Brazil) — ANPD** — ~BRL 98M (~USD 20M) total fines 2023-2025 [89]. Meta/Facebook 2024-07-01: ANPD halted Meta from training AI on Brazilian users' data; potential 50,000 reais/day per breach [90].

**Saudi PDPL — SDAIA** — VERIFIED: **48 enforcement decisions confirmed PDPL violations across 2025-2026** [91][92]. (Earlier "48 enforcement actions" claim was correct.) 2025 amendments raise penalty ceiling to SAR 5M (~USD 1.3M); doubled for repeat offences.

**PIPA (South Korea) — PIPC**
- **August 2025**: telecommunications carrier fined ~**KRW 134.7B** + KRW 9.6M after a 23M-user breach — largest ever for a Korean PI leak [93].
- May 2024: KRW 7.5B + KRW 5.4M for a 2.21M-user leak.

**DPDP Act (India, 2023)** — Concept: Data Principals/Data Fiduciaries; consent + Significant Data Fiduciary obligations. `[INFERENCE]` Enforcement infrastructure (Data Protection Board) was still ramping in 2024-2025; few public actions yet — verify with the Board's website before citing specific cases.

**PDPA (Singapore) — PDPC** — Mandatory breach notification + higher fines under 2020 amendments. Decisions published at pdpc.gov.sg.

### 2.4 Who can sue / fine — taxonomy

| Track | Actor | Legal hook | Example |
|---|---|---|---|
| Administrative (EU national) | National DPA | GDPR Arts. 58, 83 + ePrivacy national transposition | CNIL v. Google €325M 2025 (ePrivacy) |
| Administrative (EU one-stop-shop) | Lead DPA + EDPB Art. 65 binding decision in disputes | GDPR Arts. 56, 60–65 | DPC v. Meta €251M (2024) |
| Administrative (EU Commission) | DG CNECT | DSA, DMA — **not GDPR**, not DPA-led | DSA proceedings vs X 2023–2025 |
| Individual private right (EU) | Data subject | Art. 79 (judicial), Art. 82 (compensation) | German consumer-court Art. 82 awards |
| NGO collective (EU) | Qualified non-profit | Art. 80(1) with mandate; Art. 80(2) where Member State allows | noyb / LQDN; CNIL €50M Google 2019 |
| Administrative (US federal) | FTC | FTC Act §5; COPPA, GLBA, FCRA | FTC v. X-Mode 2024 |
| Administrative (US state) | State AG / CPPA | CCPA/CPRA; state UDAP statutes | CA AG v. Sephora 2022 |
| Private right of action (US, narrow) | Consumer | CCPA §1798.150 (breach only); BIPA; VPPA; CIPA | Meta Pixel healthcare class actions |
| Class action | Class counsel | Fed. R. Civ. P. 23 / state | *In re Meta Pixel Healthcare* |
| Sectoral (US) | HHS OCR (HIPAA), FCC, CFPB | Sectoral statutes | HHS OCR HIPAA settlements |

> **Don't confuse**: DSA enforcement (EU Commission, with national Digital Services Coordinators) is *separate from* GDPR enforcement (national DPAs coordinated through EDPB). A platform can be hit by both regimes for the same surface conduct under different theories.

---

## Section 3 — Specific Enforcement Cases

### 3.1 FTC v. TRUSTe (already in §6 self-check)
2014-11-17 announce, 2015-03-18 final order, $200K + 10-year reporting; failed annual recertifications + non-profit misrepresentation [97][98].

### 3.2 Edelman 2006 study (already in §6 self-check)
TRUSTe sites 2× more "bad" (5.4% vs 2.5% baseline); paper at [99][100].

### 3.3 Shein €150M (already in §6 self-check)
CNIL 2025-09-01, INFINITE STYLES SERVICES CO. LIMITED, four cookie-violation grounds [101][102].

### 3.4 CNIL 2025 totals (already in §6 self-check)
83 sanctions, **€486,839,500 total ALL CATEGORIES** (cookies, employee monitoring, security). 21 sanctions specifically for cookies; Google €325M + Shein €150M dominate [103].

### 3.5 Other 2024–2026 DPA enforcement

**CNIL (France)**
- 2024: 87 sanctions, €55.2M total [104].
- 2025: 83 sanctions, €486.8M [103].
- Top 2025: Google €325M (Sep 3), Shein €150M (Sep 1), Free Mobile €27M (Jan 2026), Free €15M (Jan 2026), France Travail €5M (Jan 2026).

**Italian Garante**
- OpenAI €15M (2024-12-20) — annulled by Court of Rome 2026-03-18 [40][41].
- Replika — Feb 2023 ban + 2025 fine [105].

**Irish DPC**
- TikTok €530M (2025-05-02) — unlawful EEA→China transfers + transparency [106][107].
- Meta €251M (2024-12-17) — token breach, Arts. 25/33 [49].
- Meta €91M (2024-09-27) — plaintext password storage, Art. 32 [48].
- TikTok €345M (Sept 2023) — children's privacy [108].
- X / xAI Grok inquiry opened April 2025 [109].

**Austrian DSB (NOYB-driven)**
- 2022-01-12: First "101" decision — Google Analytics use is unlawful US transfer post-Schrems II [110].
- DSB had legal option to fine Google up to €6 billion [111] but did not impose monetary fine.

**UK ICO**
- 2024: 18 fines, total £2.7M, mostly under PECR (UK ePrivacy transposition); largest = MOD £750K [112].
- 2025: 15 fines, ~£21.7M total — fewer actions, much higher amounts [113].
- 23andMe — £2.31M, June 2025 (credential stuffing breach affecting 155,000 UK users; ~50% reduction after representations).
- ICO direction: shift away from one-off breaches toward systemic governance failures.

**Dutch AP**
- Uber €290M (Aug 2024) — unlawful US transfers of driver data [114].
- Clearview AI €30.5M (2024-05-16) [38].

**German DPAs (BfDI federal + 16 state)** — H&M €35.3M (Hamburg, 2020); Deutsche Wohnen action (CJEU Art. 83 attribution decided 2023) [115].

**Spanish AEPD** — FY2024 ~€35.6M total (19.4% YoY), 10 fines >€1M [116][117]. AEPD remains the **highest-volume** DPA in Europe (~1,000 fines since 2018).

**Portuguese CNPD** — 2023: 90 fines totalling ~€559,950 [118]. 2025 annual plan signals stronger sanctioning. CNPD stopped publishing individual decisions, so trend visibility is poor — `[INFERENCE]` itself a research finding.

**Polish UODO** — Poczta Polska €6.44M (2025) for electoral data; mBank PLN 4.05M (~€969K, 2024-09); Toyota Bank Polska €60K + €72K [43].

### 3.6 NGO-driven enforcement (the noyb model)

**noyb (Vienna, founded 2017 by Max Schrems)**
- Built around Art. 80(2) representation + Art. 77/79 strategic complaints/litigation [119][120].
- **Funding model**: Initial €250K/year crowdfunded → now **>4,400 supporting members**. Goal = 2/3 of budget from supporting members to avoid donor capture. Member-fee inflation indexing applied April 2025 (+2.6%) [119].
- Cookie campaign: **422 GDPR complaints filed Aug 2022**, scaled to 500+ and aiming for 10,000/year [121][122]. 81% of pages complained-about lacked "reject" on first layer; 73% used deceptive colors; 90% had no easy withdrawal.
- **History**:
  - *Schrems I* (CJEU C-362/14, 2015) → Safe Harbor invalidated.
  - *Schrems II* (CJEU C-311/18, 2020) → Privacy Shield invalidated.
  - **Day-1 GDPR complaints (2018-05-25)** vs Google/Instagram/WhatsApp/Facebook → **CNIL €50M Google fine, January 2019** (Art. 80, with LQDN partner) [53].
  - **101 Complaints, summer 2020** — every EU/EEA country, Google Analytics + Facebook Connect transfers. First win: Austrian DSB Jan 2022.
- Recent 2024-2025: Meta "pay-or-consent" complaints; multi-country OpenAI complaints; Yahoo/Microsoft cookie-banner sweeps.
- `[INFERENCE]` "Success rate" hard to define — noyb counts both authority decisions (often years later) and policy changes by targets. Verifiable wins include CNIL Google 2019, Austrian DSB 2022, CNIL/Garante Google Analytics 2022, Irish DPC Meta 2023.

**Other key NGOs**
- **EFF (US, 1990)** — strategic litigation under §1983, Wiretap Act, ECPA; amicus filings in CIPA cases.
- **Access Now** — Digital Security Helpline; surveillance/spyware accountability.
- **La Quadrature du Net (LQDN)** — French. Co-complainant in CNIL v. Google 2019; named party in CJEU **C-511/18 La Quadrature du Net & Others** (data-retention judgment, 6 Oct 2020) [123][124].
- **EDRi** — coalition of 50+ NGOs; led public position against AI Act loopholes; vocal on ePrivacy Reg withdrawal [62].
- **Privacy International (UK)** — claimant in CJEU **C-623/17 Privacy International v UK** (2020) on bulk-data; aligned with LQDN cases.

### 3.7 US class-action machine — pixel litigation firms

- **Cohen Milstein** — co-lead in **In re Meta Pixel Healthcare Litigation** (N.D. Cal.) [125].
- **Milberg** — Advocate Aurora $12.25M settlement [126].
- **The Lyon Firm** — Christ Hospital $7M; Advocate Aurora co-lead; substantial Meta-pixel docket [127].
- *In re Meta Pixel Healthcare* — Judge Orrick (N.D. Cal.) refused dismissal Jan 2024; ordered Zuckerberg deposition April 2025.
- Healthcare settlements 2024-2025: Aurora Health $12.25M, Aspen Dental ~$18.5M, Reid Health, Jefferson Healthcare [128].
- Volume: Website-tracking and digital-wiretapping cases grew from 228 in 2022-23 to 2,163 in the most recent year per Coalition's 2025 State of Web Privacy [129].
- How firms identify defendants (`[INFERENCE]` based on standard CIPA pleading patterns): third-party scans (browser extensions, Wayback Machine, Blacklight-style snapshots) → aggrieved-plaintiff intake → technical-expert affidavit [130].

### 3.8 China-export-specific cases (privacy-fixable vs geopolitical-unfixable)

| Company | Action | Type | Cert helps? |
|---|---|---|---|
| **Shein** (CN→FR) | CNIL €150M cookie fine 2025-09-01 | Privacy violation | ✅ Yes |
| **Temu** (CN→EU) | EU Commission DSA proceedings ongoing | DSA platform conduct | Partially |
| **TikTok** (CN→IE) | DPC €530M (2025-05-02) data transfer; DPC €345M (Sept 2023) children's | Privacy + transfers | ✅ for privacy; ❌ for CFIUS |
| **TikTok** (CN→US) | CFIUS ban litigation, House Bill | National-security ownership | ❌ Cert cannot solve |
| **Hikvision** (CN→US/UK) | NDAA / UK gov ban | National-security ownership | ❌ Cert cannot solve |

> [INFERENCE] The clean separation: cookie / data-handling violations are *privacy-fixable* (CERT or audit can cure); ownership / national-security blocks are *geopolitical-unfixable* (no privacy artifact remediates). Alfred's tool serves the first column, not the second.

---

## Section 4 — User Ecosystem

### 4.1 Existing privacy-audit tools — real adoption

**WebXray (Tim Libert)** — Built 2012 [131]. Note: Libert is **NOT at Princeton** (common misattribution); actually U Penn (PhD 2017), CMU CyLab postdoc, Oxford, then Google internal cookie-policy team, now webXray LLC (commercialized 2024) [132]. **Princeton-affiliated framework is OpenWPM**, separate.
- Vendor-claimed citations: "over 900 peer-reviewed studies" [131] — `[INFERENCE]` treat as ballpark; independent Scholar lookup shows Libert 2015 alone has hundreds.
- 2026 status: relaunched as commercial entity webXray LLC with "California Privacy Audit" product at globalprivacyaudit.org [133].

**The Markup's Blacklight** — Launched September 2020 [134][135]. Real-time, free public scanner running 7 privacy tests on a single URL.
- Concrete Markup investigations using Blacklight as data source:
  1. "Facebook Is Receiving Sensitive Medical Information from Hospital Websites" (16 Jun 2022) — found Meta Pixel on 33 of Newsweek's top-100 US hospitals [136].
  2. Senate inquiry follow-up Sep 2022; 28 of 33 hospitals removed the pixel [137].
  3. "10 Million Blacklight Scans Later" (3 May 2023) [138].
  4. CalMatters re-ran Blacklight to track TikTok/X (Feb 2026) [139].
  5. **Open-sourced Blacklight Query CLI** Oct 2024 [140].
- **Funding (load-bearing)**: $20M from Craig Newmark, $2M from Knight, plus Ford and MacArthur [141][142]. Newmark announced Jan 2026 he is pulling back on journalism funding [143] — **a real risk vector**.

**Exodus Privacy** — French volunteer non-profit. **Maintains εxodus tracker analysis platform for Android apps (not websites)** [144]. Active in 2025; consumed by Privacy Guides + Penn State digital-literacy programme.

**PrivacyScore** — Built by University of Hamburg/Bamberg/Siegen as part of DFG Research Training Group 2090 [145]. **The funding research training group concluded at end of 2024**. Site still resolves; project effectively in maintenance/dormant mode. **Cautionary tale: academic-grant-funded tools die when grants end.**

**Privacy Badger** — Electronic Frontier Foundation. GitHub [146]. EFF page [147].

**Disconnect tracker lists** — maintained by Disconnect.me. **Firefox's Enhanced Tracking Protection ships these lists** via mozilla-services/shavar-prod-lists. Microsoft Edge also uses them [148][149]. **Existence proof of how a private-company tracker list moves the needle for hundreds of millions of users.**

**EasyList / EasyPrivacy** — community filter lists, originally Rick Petnel 2005 [150]. Consumed by uBlock Origin, Adblock Plus, Brave, Pi-hole; ground-truth data in academic measurement.

**OpenWPM (Princeton CITP)** — Englehardt & Narayanan, 2015–2016. Built on Firefox + Selenium; community-maintained on GitHub [151][152]. **The 1-million-site study (CCS 2016)** is one of the most-cited web privacy papers, surfaced fingerprinting at scale [153]. Documentation: used "by at least 6 other research groups, as well as journalists, regulators, and students for class projects" [154].

**CookieViz (CNIL LINC)** — French DPA-built, GPLv3, GitHub [155][156]. Used by CNIL itself for cookie-sweep observations. **Strongest existence proof that a regulator will both build and consume tooling like Alfred's.** GPA award entry 2021 [157].

### 4.2 User type catalog with named examples

**Investigative journalists**
- **The Markup (US)** — Pixel Hunt series; Blacklight as public service; hospital-pixel triggered ~5 class actions and Senate inquiry [136].
- **Bloomberg / The CyberSignal** — 2024 reporting on 20 US state health exchanges leaking citizenship/race to TikTok/Meta [158].
- **CalMatters (CA)** — Feb 2026 used Blacklight on TikTok/X [139].
- **Le Monde (FR)** — investigation revealing how commercial ad-tech location data exposed French intelligence officers [159].
- **Süddeutsche Zeitung** — `[INFERENCE]` strong investigative tradition (Panama/Paradise Papers); no specific cookie-banner investigation surfaced; would be a target outlet but does not appear to have an established privacy-measurement franchise.
- **Follow The Money (NL)** — investigative journalism platform, **no dedicated tracker investigation surfaced** [160].

**Privacy NGOs** — see §3.6.

**DPAs (regulators)** — honest answer: **most DPAs act primarily on individual/NGO complaints, but a growing minority run their own scanning programs**:
- **CNIL** — built CookieViz in-house; ran cookie sweeps in Sept/Oct of multiple years; combined fines >€139M Dec 2022–Dec 2024 under Article 82 LIL [161][162][163]. The realistic user is the **CNIL LINC team**.
- **ICO** — endorsed IAB Tech Lab DDRF in 2025; publishes Tech Horizons reports [164][165]. Operates PETs sandbox-style work but no publicly named "Tech Lab" comparable to LINC.
- **Italian Garante** — investigation-driven, not scan-driven [40].
- **Brazilian ANPD** — has acted against Meta/X/ByteDance but **no enforcement on cookies yet**, despite Oct 2022 cookie guidelines [89].
- **Korea PIPC** — Google ~$53M and Meta ~$24M in Sept 2022 for behavioural pixel/SDK tracking without consent [166]. **Most aggressive APAC regulator on tracking specifically.**

> [INFERENCE] The realistic DPA "user" for Alfred's tool is **a techie inside a DPA** (CNIL LINC team, Norwegian Datatilsynet's tech team, ICO Tech Lab equivalent) rather than the agency as institutional buyer.

**Academics — leading privacy-measurement researchers**
- **Princeton CITP** — Arvind Narayanan, Steven Englehardt (now at Mozilla), Jonathan Mayer; OpenWPM lineage [154].
- **CMU CyLab CUPS** — Lorrie Cranor; "Beyond the fine print" Nov 2025 work on consent UI design effects [167][168].
- **MIT/Cambridge** — Nouwens, Liccardi (CHI 2020 dark-patterns).
- **Inria (France)** — Nataliia Bielova (Gray et al. CHI 2021) [169].

**Class-action plaintiffs' lawyers (US)**
- **Edelson PC (Chicago)** — established consumer-class-action firm with privacy track record [170]. `[INFERENCE]` could not directly confirm Edelson lead-counsel role in CIPA chat-tracking specifically; treat as "firm of the type."
- **Bursor & Fisher, Almeida, Lowey Dannenberg** — visible in Meta-Pixel-on-hospitals wave [126][127][171].

**Compliance vendors**
- **OneTrust** — privacy management leader; minimum ACV ~$10K/yr as of Mar 2026; owns Cookiepedia [172][173].
- **Cookiebot (Usercentrics)** — consent-management focused; runs automated scanner [174].
- **Osano** — mid-market positioning; "Data Privacy Benchmark" [175].
- **Securiti** — publishes ANPD/LGPD/PDPL guidance content [176].

> [INFERENCE] For Alfred, vendors are simultaneously potential consumers (they need ground-truth threat intel) AND competitive moats (will not adopt outsider data lightly). Treat them as a content distribution channel via thought-leadership, not as a primary user.

**Big-4 + boutique audit firms** — Deloitte/KPMG/PwC/EY all do SOC 2 Type II + privacy attestation; generally **build their own tools internally** but read public threat intel [177][178]. Boutique (Schellman, A-LIGN, Coalfire) — same shape, smaller scale. `[INFERENCE]` more likely to license a third-party audit dataset than Big-4, but still niche.

**Enterprise procurement teams**
- **SIG Lite (126 questions)** and **CSA CAIQ** are the dominant pre-procurement questionnaires [179][180]. Mature buyers use them sequentially.

> [INFERENCE] An audit dataset that helps buyers verify SIG Lite Privacy answers is high-leverage because procurement cycles already exist.

**Cyber-insurance underwriters**
- **2025-2026 inflection point**: carriers now require proof of CMP usage and tracker inventory. Coalition's 2025 State of Web Privacy: **59% of all web-privacy claims were against companies with <$100M revenue** [129][181].
- **Strong, dollar-motivated user type** that has emerged exactly during Alfred's project window.

### 4.3 Country-by-country usage

**EU heavy enforcement**
- **France**: CNIL most operationally aggressive — runs sweeps, fined Google €60M + Google Ireland €40M in Dec 2020, part of >€139M Article 82 fines through 2024. Realistic users: CNIL LINC; noyb (covers all EU); Bielova @ Inria; vzbv (German consumer-protection).
- **Germany**: 16 state-level DPAs + BfDI; coordinated less than CNIL.
- **Ireland**: DPC is lead supervisor for Meta/Google EU/Apple/TikTok — historically slower; €1.3B Meta fine 2023 [182].
- **Italy (Garante)**: active on AI/ChatGPT (€15M OpenAI Dec 2024); investigation-led.

**UK** — ICO; post-Brexit kept "adequacy" with EU until June 2025 review window [183]. Likely consumer: Privacy International (London); ORG (Open Rights Group).

**US**
- **California**: CPPA + CIPA; **the litigation engine**. CIPA pleadings up ~10× from 2022-23 to 2024-25 [129].
- **Illinois**: BIPA (canvas-fingerprinting overlap).
- **Texas**: state wiretap statute; emerging analog of CIPA [184].
- Likely consumers: Edelson PC and the plaintiffs' bar; The Markup; FTC's Office of Technology (cited a "Lurking Beneath the Surface" pixel-tracking blogpost in 2023) [185].

**Brazil (LGPD)** — ANPD; Oct 2022 cookie guidance; no cookie enforcement yet but engine warming up [89].

**Saudi Arabia / UAE** — Saudi PDPL effective Sep 14 2024; SDAIA authority; **PDPL is silent on cookies but DGA has issued non-binding cookie guidelines** [186][187]. Honest take: civil society / journalism use is **negligible** in these jurisdictions. Realistic users: foreign multinationals' KSA-facing compliance teams.

**APAC**
- Korea PIPC most aggressive on tracking [166].
- Japan PPC: APPI requires opt-in for personal-data third-party transfers; less aggressive enforcement.
- Singapore PDPC: PDPA, fines up to S$1M.
- India: DPDPA 2023; rules being finalized — large compliance market emerging.
- **China outbound**: Chinese SaaS exporters need to demonstrate GDPR/CCPA compliance to win EU/US deals — Alfred's "vendor trust bridge" thesis from `positioning_and_future_extension.md`.

### 4.4 GDPR extraterritoriality — why non-EU people care

Article 3(1) covers establishment in EU regardless of processing location; Art. 3(2) covers non-EU controllers offering services to OR monitoring EU subjects [36][37].

**Real fines on US companies**:
- Meta — €1.2B (May 2023), Irish DPC, EU-US transfers post-Schrems II [182].
- Amazon — €746M (July 2021), Luxembourg CNPD, ad-cookie consent [188].
- Google — €50M (Jan 2019) CNIL transparency + invalid consent; €60M + €40M (Dec 2020) cookies; €325M (2025) Gmail.
- OpenAI — €15M (Dec 2024) Italian Garante (annulled Mar 2026).
- **Eight of the ten largest GDPR fines have been against US-based companies** (~€3.9B, ~63% of total fine pool) [189].

**Brussels Effect** — coined by Anu Bradford (Columbia Law) 2012, expanded in 2020 book *The Brussels Effect: How the European Union Rules the World* [190][191]. GDPR-specific manifestation: California CCPA, Brazil LGPD, Korea PIPA explicitly draw on GDPR; Facebook (Apr 2018) and Microsoft announced global GDPR compliance.

**Adequacy decisions** (EU Commission as of 2024): Andorra, Argentina, Canada (PIPEDA-regulated), Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, Republic of Korea, Switzerland, United Kingdom, Uruguay, **United States (DPF)** [192][193].

### 4.5 Honest motivation map

| User type | Primary motive | Mixed motive (be honest) |
|---|---|---|
| The Markup | (d) Journalism + (a) Public interest | Funded substantially by Newmark + Knight + Ford + MacArthur; **Newmark Jan 2026 announced pulling back from journalism funding** — funding is structural fragility [143] |
| noyb | (a) Public interest | Funded ~⅔ via supporting members; receives a share of GDPR settlements indirectly through legal-fee awards [119] |
| EFF / EDRi / LQDN | (a) Public interest | Endowment + foundation grants; advocacy budgets shaped by donor priorities |
| Privacy International | (a) Public interest | Foundation-funded |
| DPAs (CNIL/ICO/Garante/etc.) | (c) Regulatory | Career, political, budgetary incentives — DPAs need visible wins to justify budget |
| Academics (Princeton/CMU/Inria/MIT) | (e) Publications | Grant cycles (NSF, ERC, DFG); industry funding visible at CMU/CITP creates legitimate "industry-collaboration" pressure |
| Class-action plaintiffs' bar | (b) Commercial — fee awards | They genuinely enforce consumer rights, but the engine is contingency fees on settlements |
| Compliance vendors (OneTrust et al.) | (b) Commercial — vendor sales | Their "research" arms exist to generate sales leads and thought-leadership |
| Big-4 / boutique auditors | (b) Commercial — audit fees | They serve clients' liability needs first; objectivity constrained by who pays |
| Procurement teams | (f) Defensive — cover own ass | Real risk-reduction work, but driven by liability transfer |
| Cyber insurers | (b) Commercial — loss-ratio | Insurers do enforce real privacy hygiene by pricing it, but motive is portfolio profitability |

> [INFERENCE — design principle] **Mixed motives are normal**. Alfred should design the tool so that the same artifact can serve a noyb complaint, a Markup article, a CIPA pleading, AND a vendor-procurement check. That dual-use is feature, not bug.

### 4.6 Realistic adoption path — how predecessors got their first 100 users

- **webXray**: built academically (2012) → press citations → industry job → company. ~12 years.
- **Blacklight**: launched Sep 2020 with WaPo tour + Markup investigation hook [194]. Distribution guaranteed by Newmark/Knight money + press-release machine + Pixel Hunt brand. **Path: institutional sponsorship + bundled-with-investigation distribution.**
- **Exodus Privacy**: French volunteer collective, distributed via F-Droid + privacy-community + Privacy Guides. **Path: open-source community trust + niche app store.**
- **OpenWPM**: Princeton CITP brand + 1-million-site CCS 2016 paper [153]. **Path: one landmark paper → framework adoption.**
- **CookieViz**: built in-house at CNIL LINC, open-sourced GPLv3, marketed via CNIL outreach + Global Privacy Assembly award [157]. **Path: regulator sponsorship.**

> [INFERENCE — pattern] **None of the successful tools went out cold from a student GitHub repo.** Every one had (a) institutional sponsorship, (b) a bundled distribution event (paper, investigation, regulator launch), and (c) a visible maintainer with reputational skin in the game. **The first 100 users do not appear because the tool exists — they appear because someone at a credentialing institution used it visibly.**

### 4.7 Five most realistic first users for Alfred (2026-09 onward)

> [INFERENCE — agent-3 reasoning] Pick users who (i) already use third-party scan data, (ii) have a workflow gap, (iii) are reachable to a student researcher, (iv) provide reputational lift to subsequent users.

1. **An academic measurement-privacy lab as host/co-author** — concretely, **CMU CyLab CUPS (Cranor)**, **Inria (Bielova)**, or a UK group at Cambridge/King's. Provides institutional credibility that PrivacyScore lost. Reachable: cold email with a concrete dataset offer. Lift: a co-authored PETs/CHI paper unlocks all other users on this list.
2. **noyb's technical/engineering team in Vienna** — small NGO running a 10,000-website cookie-banner campaign. Their workflow exactly matches what Alfred's tool would feed. Reachable: noyb takes volunteers and corresponds with researchers. Lift: a tool used in any of their published complaints gets cited by EDRi and trade press.
3. **CNIL LINC / Datatilsynet equivalents** — in-house tech teams that already build/use measurement tools. CNIL LINC is gold candidate (built CookieViz). Reachable: through academic host (#1) or French-language outreach. Lift: one DPA citation creates permanent legitimacy floor.
4. **The Markup's data/tools team OR comparable nonprofit newsroom (CalMatters, ProPublica)** — continually need fresh datasets. Markup just open-sourced Blacklight Query (Oct 2024) so they explicitly invite tool collaboration. Reachable: Markup engineers public on GitHub/Mastodon. Lift: an investigation IS the marketing channel.
5. **A US plaintiffs'-bar boutique active in CIPA/Pixel-Hunt litigation** — Edelson PC, Bursor & Fisher, Almeida, or similar. **Most direct dollar incentive** — every defendant identified is a contingency-fee opportunity. Reachable: harder than others; likely needs warm intro from #1 or #4. Lift: citation in a class-action complaint creates court-record evidentiary footprint that compliance buyers and insurers follow with budgets.

> [INFERENCE — anti-pattern] **What Alfred should NOT chase first**: OneTrust/Cookiebot/Osano (will not adopt outside data); Big-4 (build internally); Saudi/UAE regulators (no civil-society ecosystem yet); cyber insurers (will adopt only after #1-#4 have legitimised the tool). These become reachable in years 2-3, not month 1.

---

## Section 5 — Implications for Alfred's SSRP Scope

> ⚠️ ALL [INFERENCE] — DECISION 100% ALFRED'S.

### 5.1 The "can I audit policy text" question (resolved)

YES, plausibly, via Angles A, C, D, or E in §1.4 — none of which overlap PRISMe. Angle C (banner-vs-policy text consistency) is methodologically cheapest; Angle A (VLM-agent claim execution) has the highest novelty against ConsentDiff; Angle D (NGO-evidence cards) aligns with Alfred's positioning Track 1.

### 5.2 The "what's my real differentiator from UMBRA + ConsentDiff" question (refined)

UMBRA = rule-based interactive 14k-cross-section. ConsentDiff = DOM+screenshot longitudinal 9-month. The **four-way intersection** still empty: longitudinal × VLM-agent × multi-step interactive × banner+policy multimodal. **But Alfred should not claim "first dynamic audit" — UMBRA already did interactive.** The honest claim is "first **AI-grounded × multi-step × longitudinal × framing-aware** audit."

### 5.3 The "how do I get adopted" question (newly informed)

§4.6 pattern is clear: **institutional sponsorship + bundled distribution event + visible maintainer**. For Alfred this means:
- Phase 1 (during SSRP): produce a paper-quality dataset + a CHI/PETs/USENIX submission as the bundled event.
- Phase 2 (post-SSRP): pick ONE of the 5 first-user types (§4.7) and design tool output for THEIR workflow. Most likely candidate per `project_positioning_strategy.md` Track 1 = either #1 (academic co-author) or #2 (noyb).

### 5.4 The "should I add the China sub-cohort to data/sites.csv" question (B.1 advisory)

The user's strategy doc `ssrp_scope_tweak_advisory.md` flagged this with a 2026-05-31 deadline. After Phase B research:
- Shein €150M is a real demo case (§3.3). Adding Shein, Temu, AliExpress, miHoYo international, RedNote international, Anker global etc. is **methodologically defensible** as a sub-cohort for "cross-border B2C" — even without committing to the commercial track.
- The academic value is independent: the same sub-cohort is interesting for "do non-EU vendors comply with GDPR Art. 3(2) extraterritorial reach?" — a genuine research question.

> [INFERENCE — leaning] If Alfred decides to take B.1, frame it inside the academic sub-cohort question, not the commercial track. Decision still his by 2026-05-31.

### 5.5 The "should I update the README's UMBRA description" question (newly raised)

`README.md` says UMBRA "uses no AI and only captures static snapshots". The "static snapshots" framing is wrong (§1.1.2). Recommended fix: update to "uses rule-based heuristics with multi-step interaction tracing — no LLM/VLM" so the project's framing of its differentiation doesn't rely on a falsifiable claim.

> [INFERENCE — leaning] Low-cost edit to README.md if Alfred wants the public framing to match verified facts. Decision his.

### 5.6 The "Italian OpenAI fine annulled" footnote

§3.5 verified that the Italian Garante OpenAI €15M was annulled by Court of Rome 2026-03-18. If Alfred cites this case in his paper, he should cite both the Garante decision AND the annulment.

### 5.7 The "user-ecosystem-driven Layer 3 design" question (newly raised)

§4.7 implies that NGO/journalism/plaintiffs'-bar users want **structured evidence cards** (claim-verbatim → UI test result → screenshot → cookie trace). Alfred's Layer 3 (Transparency / Framing) currently scores text on neutrality but does not necessarily produce evidence-card output.

> [INFERENCE — possible scope tweak] Adding an evidence-card export format (per finding) is a low-cost extension that maps directly onto downstream user workflows. Decision Alfred's.

---

## Section 6 — Self-Check of Assistant's Earlier Assertions (UPDATED)

| # | Earlier claim | Status | Notes / Citation |
|---|---|---|---|
| 1 | PRISMe (2025) audits privacy policy text with LLMs | ⚠️ Corrected | Title = "Helping Johnny Make Sense of Privacy Policies with LLMs"; venue **CHI 2026**; arxiv submission 2025-01-27 but final revision 2026-01-28. Mechanism description correct. [1] |
| 2 | UMBRA / "Abyss" (2026) audits banners with rule-based heuristics, no AI, **only static snapshots** | ⚠️ Corrected | "Rule-based, no AI" confirmed. **"Static snapshots" wrong** — UMBRA does interaction tracing + cookie-state monitoring + multi-step flows. Authors: Singh/Jin/Kim, arxiv 2026-03. [3] |
| 3 | ConsentDiff at Scale (Haoze Guo) | ✅ Verified | arxiv 2512.04316. v7 latest 2026-04-13. [2] |
| 4 | FTC settled against TRUSTe in 2014 for "造假" | ✅ Verified | 2014-11-17 (final 2015-03-18). Specific allegations: failed annual recertifications 1,000+ times 2006-2013; misrepresented non-profit status post-2008. $200K + 10-year reporting. [97][98] |
| 5 | Edelman 2006: TRUSTe sites had ~50% higher violation rate | ✅ Verified, slightly stronger | January 2006, Benjamin Edelman, Harvard. **TRUSTe sites 50% more likely to violate**, OR more precisely **5.4% "bad" vs 2.5% baseline = >2× more likely**. Original framing was directionally right but understated. [99][100] |
| 6 | Shein €150M cookie fine | ✅ Verified | 2025-09-01, CNIL fined INFINITE STYLES SERVICES CO. LIMITED. Reasons: cookies before consent, incomplete banner, failure to honor refusals, missing third-party info. Shein appealing. [101][102] |
| 7 | CNIL 2025 cookie enforcement total €486.8M | ⚠️ Clarified | Actually total CNIL sanctions across **all categories** in 2025 = €486,839,500 across 83 sanctions. **21 sanctions specifically for cookies**, dominated by Google €325M + Shein €150M. So €486.8M is all-category total, not cookie-only — but cookies dominated. [103] |
| 8 | ePrivacy Seal 2025-05 liquidation | ✅ Verified | EuroPriSe Cert GmbH ceased operations 2025-05-30. ⚠️ **NOT** the same as the EU's ePrivacy Regulation (proposal), which was separately withdrawn 2025-07-16 published 2025-10-06. Three different "ePrivacy" things to keep separate. [61][62][63] |
| 9 | 2026-02-20 Claude Code Security launch + cyber stock drops | ⚠️ Not re-verified in Phase B | Cited in v1 strategic doc with sources (CNBC, Bloomberg, SiliconAngle). Defer until strategic doc gets revised. |
| 10 | ETS 2024 revenue $1.16B; 30% from College Board | ⚠️ Not re-verified | Cited in `positioning_and_future_extension.md` §1.2. Defer. |
| 11 | TOEFL founded 1964 by Ford Foundation + College Board + universities | ⚠️ Not re-verified | Defer. |
| 12 | UL founded 1894 by insurance companies | ⚠️ Not re-verified | Defer. |
| 13 | APEC Global CBPR 2025-06; Chinese mainland not participating | ⚠️ Not re-verified | Defer. |
| 14 | China PIP cross-border certification effective 2026-01-01 | ⚠️ Not re-verified | Defer. |
| 15 | Saudi PDPL 48 enforcement actions | ✅ Verified | 48 enforcement decisions confirmed PDPL violations across 2025-2026 per IAPP and CMS. [91][92] |
| 16 | BYD outsold Tesla in Europe May 2025 | ⚠️ Not re-verified | Defer. |
| 17 | ISC2 2025 survey: 77% list ISO 27001/NIST/SOC 2 as top vendor requirement | ⚠️ Not re-verified | Defer. |
| 18 | EuroPriSe was EDPB-endorsed under GDPR Art. 42 | ⚠️ Corrected | **EuroPriSe** (wound down 2025-05-30) was **NOT** the Art. 42(5) endorsed seal. **Europrivacy** is the EDPB-endorsed seal (Opinion 28/2022, updated Opinion 14/2026). Three different things easy to confuse. [50][51] |
| 19 | The Markup Blacklight investigations cite | ✅ Newly verified | Multiple specific investigations confirmed; Blacklight Query CLI open-sourced Oct 2024. [134][140] |
| 20 | noyb Aug 2022 = 422 cookie complaints | ✅ Verified | [121][122] |
| 21 | OpenAI Italian €15M 2024-12-20 (originally I cited it as a strong example) | ⚠️ Updated | **Annulled by Court of Rome 2026-03-18** — citing requires both decisions. [40] |
| 22 | "Tim Libert at Princeton" (a phrasing assistant might have used) | ⚠️ Common misattribution | Libert is **NOT at Princeton**. He's U Penn / CMU CyLab / Oxford / Google / now webXray LLC. **Princeton-affiliated framework is OpenWPM (Englehardt, Narayanan).** [131][132] |

> [SUMMARY] Of items verified in Phase A+B: **3 had material errors** (PRISMe venue, UMBRA "static", EuroPriSe-vs-Europrivacy confusion), **2 had phrasing imprecisions** (Edelman 50% vs 2×; CNIL €486.8M total vs cookie-only). The remaining items 9-17 are deferred to a future verification pass.

---

## Section 7 — Bibliography

URL access dates: 2026-04-26.

### Academic papers — primary

1. Freiberger V., Fleig A., Buchmann E. **"Helping Johnny Make Sense of Privacy Policies with LLMs"**. arXiv:2501.16033. ACM CHI 2026. <https://arxiv.org/abs/2501.16033>
2. Guo H. **"ConsentDiff at Scale: Longitudinal Audits of Web Privacy Policy Changes and UI Frictions"**. arXiv:2512.04316. <https://arxiv.org/abs/2512.04316>
3. Singh N., Jin S., Kim H. **"When the Abyss Looks Back: Unveiling Evolving Dark Patterns in Cookie Consent Banners"** (UMBRA). arXiv:2603.21515. <https://arxiv.org/abs/2603.21515>
4. Chen Q. **`consent_audit_rubrics_landscape.md`**, repo `数据隐私审计系统研究`. 2026-04-19.
5. Bouhoula et al. USENIX Security 2024. <https://www.usenix.org/conference/usenixsecurity24/presentation/bouhoula>
6. Bollinger et al. USENIX Security 2022 (CookieBlock). <https://www.usenix.org/conference/usenixsecurity22/presentation/bollinger>
7. Khandelwal et al. USENIX Security 2023 (CookieEnforcer). <https://www.usenix.org/system/files/sec23fall-prepub-389-khandelwal.pdf>
8. Hils, Woods & Böhme. IMC 2020. <https://dl.acm.org/doi/10.1145/3419394.3423647>
9. Kretschmer, Pennekamp & Wehrle. ACM TWEB 2021. <https://www.comsys.rwth-aachen.de/publication/2021/2021_kretschmer_cookie-banners-and-privacy/2021_kretschmer_cookie-banners-and-privacy.pdf>
10. Tang, Bui & Shin. USENIX Security 2025 (ConsentChk). <https://www.usenix.org/conference/usenixsecurity25/presentation/tang> | arxiv: <https://arxiv.org/abs/2506.08996>
11. Rasaii et al. IMC 2023. <https://bannerclick.github.io/rasaii2023cookiewall.pdf>
12. Rasaii et al. 2025 (Intractable Cookie Crumbs). <https://arxiv.org/abs/2506.11947>
13. Hausner & Gertz. CHI Workshop 2021. <https://arxiv.org/abs/2103.14956>
14. Soe, Santos & Slavkovik. MADWeb 2022. <https://arxiv.org/abs/2204.11836>
15. Soe et al. NordiCHI 2020. <https://dl.acm.org/doi/10.1145/3419249.3420132>
16. Santos et al. WPES 2021. <https://dl.acm.org/doi/10.1145/3463676.3485611>
17. Mathur et al. CSCW 2019. <https://arxiv.org/abs/1907.07032>
18. Mathur, Mayer & Kshirsagar. CHI 2021. <https://arxiv.org/abs/2101.04843>
19. Habib et al. CHI 2022. <https://www.ftc.gov/system/files/ftc_gov/pdf/PrivacyCon-2022-Habib-Li-Young-Cranor-Okay-whatever-An-Evaluation-of-Cookie-Consent-Interfaces.pdf>
20. Gunawan et al. CSCW 2021. <https://dl.acm.org/doi/10.1145/3479521>
21. Sánchez-Rola et al. AsiaCCS 2019. <https://dl.acm.org/doi/10.1145/3321705.3329806>
22. Sánchez-Rola et al. IEEE S&P 2021. <https://www.computer.org/csdl/proceedings-article/sp/2021/09796062/1Eez73rRgIM>
23. Andow et al. USENIX Security 2019 (PolicyLint). <https://www.usenix.org/conference/usenixsecurity19/presentation/andow>
24. Cui et al. USENIX Security 2023 (PoliGraph). <https://arxiv.org/abs/2210.06746>
25. Harkous et al. USENIX Security 2018 (Polisis/PriBot). <https://www.usenix.org/conference/usenixsecurity18/presentation/harkous>
26. Grossman et al. 2025 (Salient Object Detection on banners). <https://arxiv.org/abs/2510.26967>
27. Cookiescanner. ARES 2023. <https://arxiv.org/abs/2309.06196>
28. Zharmagambetov et al. NeurIPS D&B 2025 (AgentDAM). <https://arxiv.org/abs/2503.09780>
29. Hu et al. 2026 (WebSP-Eval). <https://arxiv.org/abs/2604.06367>
30. Aonghusa et al. 2025 (Privacy Practices of Browser Agents). <https://arxiv.org/abs/2512.07725>
31. Zheng et al. PETS 2026 (AudAgent). <https://arxiv.org/abs/2511.07441>
32. Pan et al. USENIX Security 2024 (A New Hope). <https://www.usenix.org/system/files/sec24fall-prepub-303-pan-shidong-hope.pdf>
33. Bui et al. CCS 2021 (PurPliance). <https://dl.acm.org/doi/10.1145/3460120.3484536>
34. Kampanos & Shahandashti. IFIP SEC 2021. <https://www-users.york.ac.uk/~sfs521/papers/KS21-Cookie-Banner-UK-Greece-IFIP-SEC-2021.pdf>
35. Princeton-Leuven Longitudinal Privacy Policy Corpus. <https://privacypolicies.cs.princeton.edu/>

### Regulatory primary sources

36. EUR-Lex — consolidated GDPR (Regulation 2016/679). <https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02016R0679-20160504>
37. EDPB Guidelines 3/2018 — territorial scope (Article 3). <https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-32018-territorial-scope-gdpr-article-3-version_en>
38. Privacy Company — Clearview AI Dutch fine analysis. <https://www.privacycompany.eu/blog/extraterritorial-enforcement-of-the-gdpr-in-light-of-clearview-ais-recent-fine->
39. Eversheds Sutherland — Dutch DDPA Clearview. <https://www.eversheds-sutherland.com/en/finland/insights/eu-dutch-ddpa-clearview-ai-fine>
40. Lewis Silkin — OpenAI Garante €15M. <https://www.lewissilkin.com/en/insights/2025/01/14/openai-faces-15-million-fine-as-the-italian-garante-strikes-again-102jtqc>
41. Euronews — Italy fines OpenAI €15M. <https://www.euronews.com/next/2024/12/20/italys-privacy-watchdog-fines-openai-15-million-after-probe-into-chatgpt-data-collection>
42. GDPR Article 6 — gdpr-info.eu. <https://gdpr-info.eu/art-6-gdpr/>
43. EDPB news — Polish SA Poczta Polska. <https://www.edpb.europa.eu/news/national-news/2025/polish-sa-administrative-fines-gdpr-infringements-organisation-election_en>
44. EDPB Guidelines 1/2024 — legitimate interest. <https://www.edpb.europa.eu/system/files/2024-10/edpb_guidelines_202401_legitimateinterest_en.pdf>
45. GDPR Article 7 — gdpr-info.eu. <https://gdpr-info.eu/art-7-gdpr/>
46. IAPP — CJEU SCHUFA ADM rulings. <https://iapp.org/news/a/key-takeaways-from-the-cjeus-recent-automated-decision-making-rulings>
47. Matheson — CJEU SCHUFA decision. <https://www.matheson.com/insights/cjeu-delivers-important-decision-on-automated-decision-making-under-the-gdpr/>
48. Irish DPC — Meta €91M plaintext password. <https://www.dataprotection.ie/en/news-media/press-releases/DPC-announces-91-million-fine-of-Meta>
49. Irish DPC — Meta €251M token breach. <https://www.dataprotection.ie/en/news-media/press-releases/irish-data-protection-commission-fines-meta-eu251-million>
50. Europrivacy official site. <https://europrivacy.org/>
51. EDPB Opinion 14/2026 on Europrivacy. <https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-142026-europrivacy-certification-criteria_en>
52. Faegre Drinker — Collective Redress + GDPR Art. 80. <https://www.faegredrinker.com/en/insights/publications/2021/11/the-eus-collective-redress-directive-an-analysis-of-the-interplay-with-eu-general-data-protection>
53. Hunton — CNIL €50M Google 2019. <https://www.hunton.com/privacy-and-information-security-law/cnil-fines-google-e50-million-for-alleged-gdpr-violations>
54. Deceptive Design — LQDN/noyb v. Google case file. <https://www.deceptive.design/cases/ngo-la-quadrature-du-net-lqdn-and-noyb-complainant-v-google-llc>
55. NYU Compliance & Enforcement — landmark ePrivacy fines. <https://wp.nyu.edu/compliance_enforcement/2021/01/04/cnil-issues-fines-totaling-e135-million-in-landmark-eprivacy-directive-cases/>
56. IAPP — CNIL ePrivacy enforcement trend. <https://iapp.org/news/a/cnils-eprivacy-fines-reveal-potential-enforcement-trend>
57. Hunton — CNIL €135M Google + Amazon 2020. <https://www.hunton.com/privacy-and-information-security-law/cnil-fines-google-and-amazon-135-million-euros-for-alleged-cookie-violations>
58. Debevoise data blog — Google/Amazon CNIL. <https://www.debevoisedatablog.com/2020/12/22/french-cnil-hits-google-amazon-with-e135-million-fines/>
59. CNIL — Google €325M 2025 (Gmail). <https://www.cnil.fr/en/cookies-and-advertisements-inserted-between-emails-google-fined-325-million-euros-cnil>
60. Goodwin — CNIL €325M analysis. <https://www.goodwinlaw.com/en/insights/publications/2025/09/insights-practices-dpc-cnil-imposes-record-325-million-fine>
61. Hunton — ePrivacy + AI Liability withdrawal. <https://www.hunton.com/privacy-and-information-security-law/european-commission-withdraws-eprivacy-regulation-and-ai-liability-directive-proposals>
62. EDRi — ePrivacy Regulation withdrawal commentary. <https://edri.org/our-work/the-eprivacy-regulation-proposal-has-been-withdrawn-but-the-fight-for-your-privacy-is-far-from-over/>
63. TechCrunch — EU drops ePrivacy reform. <https://techcrunch.com/2025/02/12/eu-abandons-eprivacy-reform-as-bloc-shifts-focus-to-competitiveness-and-fostering-data-access-for-ai/>
64. CA AG — Sephora settlement. <https://oag.ca.gov/news/press-releases/attorney-general-bonta-announces-settlement-sephora-part-ongoing-enforcement>
65. Crowell — Sephora $1.2M analysis. <https://www.crowell.com/en/insights/client-alerts/1-2-million-ccpa-settlement-with-sephora-focuses-on-sale-of-personal-information-and-global-privacy-controls>
66. CPPA — 2025 announcement (Tractor Supply). <https://cppa.ca.gov/announcements/2025/20250909.html>
67. White & Case — CPPA Tractor Supply $1.35M. <https://www.whitecase.com/insight-alert/california-privacy-protection-agency-issues-record-135-million-fine-against-tractor>
68. Byte Back — CPPA Honda first action. <https://www.bytebacklaw.com/2025/03/cppa-announces-its-first-ccpa-enforcement-action/>
69. Byte Back — CPPA Todd Snyder. <https://www.bytebacklaw.com/2025/05/cppa-announces-new-ccpa-enforcement-action/>
70. Koley Jessen — FTC 2024 privacy. <https://www.koleyjessen.com/insights/publications/federal-trade-commission-demonstrates-focus-on-privacy-and-data-security-in-2024>
71. WilmerHale — FTC location data 2024. <https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20240209-recent-enforcement-actions-signal-ftc-focus-on-protecting-location-data>
72. Perkins Coie — Blackbaud Section 5 unfairness. <https://perkinscoie.com/insights/update/ftc-brings-first-standalone-section-5-unfairness-claims-unreasonable-data-retention>
73. Jackson Walker — CIPA surge. <https://www.jw.com/news/insights-california-invasion-privacy-act-claims-surge/>
74. ABA Business Law Today — CIPA primer 2024. <https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-august/californias-invasion-privacy-act/>
75. Coblentz — CIPA, VPPA, SB 690 2024-2025. <https://www.coblentzlaw.com/news/developments-in-digital-privacy-litigation-in-2024-2025-cipa-vppa-and-californias-sb-690/>
76. Holland & Knight — CIPA §638.51 2026 update. <https://www.hklaw.com/en/insights/publications/2026/02/uncertainty-continues-in-california-on-cipa-section-63851-claims>
77. Fisher Phillips — CIPA divided rulings. <https://www.fisherphillips.com/en/insights/insights/courts-still-divided-on-whether-california-privacy-law-applies-to-website-tracking>
78. Hunton — SB 690 abusive lawsuits. <https://www.hunton.com/privacy-and-information-security-law/california-bill-may-curb-the-flood-of-abusive-lawsuits-targeting-standard-online-business-activities>
79. Greenberg Traurig — BIPA SB 2979 amendment. <https://www.gtlaw.com/en/insights/2024/8/bipa-update-illinois-limits-liability-and-clarifies-electronic-consent-for-biometric-data-collection>
80. DWT — BIPA amendment retroactivity. <https://www.dwt.com/blogs/privacy--security-law-blog/2024/08/illinois-bipa-biometrics-law-amended-for-damages>
81. WilmerHale — 2024 BIPA review. <https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20250219-year-in-review-2024-bipa-litigation-takeaways>
82. Privacy World — 2025 BIPA Year in Review. <https://www.privacyworld.blog/2025/12/2025-year-in-review-biometric-privacy-litigation/>
83. ABA Business Law Today — VPPA pixel wave. <https://www.americanbar.org/groups/business_law/resources/business-law-today/2025-april/pixel-tools-vppa-class-action/>
84. Morgan Lewis — Second Circuit Meta Pixel VPPA. <https://www.morganlewis.com/pubs/2025/07/second-circuit-shuts-the-door-on-meta-pixel-vppa-claims>
85. Foley Hoag — SCOTUS Salazar v. Paramount cert grant. <https://foleyhoag.com/news-and-insights/blogs/security-privacy-and-the-law/2026/february/the-supreme-court-enters-the-discussion-about-meta-pixel-and-google-analytics-how-to-define-what-i/>
86. NatLawReview — Didi PIPL/CSL/DSL fine. <https://natlawreview.com/article/chinese-data-security-data-protection-and-cybersecurity-law-recent-enforcement>
87. Moulis Legal — Didi $1.2B. <https://moulislegal.com/knowledge-centre/didi-fined-1-2b-for-breaching-china-s-data-security-laws/>
88. Chambers — China 2025 data privacy. <https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2025/china/trends-and-developments>
89. IAPP — Brazilian DPA sanctions. <https://iapp.org/news/a/lessons-from-brazilian-dpa-sanctions-to-date>
90. Manage Engine — Brazil ANPD vs Meta. <https://insights.manageengine.com/privacy-compliance/brazil-data-privacy/>
91. IAPP — Saudi PDPL first anniversary. <https://iapp.org/news/a/saudi-pdpl-s-first-anniversary-amendments-enforcement-and-ongoing-developments>
92. CMS LawNow — Saudi PDPL one year. <https://cms-lawnow.com/en/ealerts/2025/09/one-year-anniversary-saudi-personal-data-protection-law>
93. Chambers — South Korea 2026. <https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/south-korea/trends-and-developments>

### TRUSTe / Edelman / Shein / EuroPriSe

97. FTC press release: TRUSTe 2014. <https://www.ftc.gov/news-events/news/press-releases/2014/11/truste-settles-ftc-charges-it-deceived-consumers-through-its-privacy-seal-program>
98. FTC press release: TRUSTe Final Order 2015. <https://www.ftc.gov/news-events/news/press-releases/2015/03/ftc-approves-final-order-truste-privacy-case>
99. Edelman B. "Adverse Selection in Online 'Trust' Certifications." January 2006. <https://www.benedelman.org/publications/advsel-trust-draft.pdf>
100. Edelman B. "Certifications and Site Trustworthiness." 2006-09-25. <https://www.benedelman.org/news-092506/>
101. CNIL press release — Shein €150M. <https://www.cnil.fr/en/cookies-placed-without-consent-shein-fined-150-million-euros-cnil>
102. EDPB news mirror — Shein. <https://www.edpb.europa.eu/news/national-news/2025/french-sa-cookies-placed-without-consent-shein-fined-150-000-000-eur-cnil_en>
103. CNIL — 2025 sanctions overview. <https://www.cnil.fr/en/sanctions-and-corrective-measures-cnils-actions-2025>
104. CNIL — 2024 sanctions overview. <https://www.cnil.fr/en/sanctions-and-corrective-measures-cnils-actions-2024>
105. EDPB news — Replika fine 2025. <https://www.edpb.europa.eu/news/national-news/2025/ai-italian-supervisory-authority-fines-company-behind-chatbot-replika_en>
106. Irish DPC — TikTok €530M. <https://www.dataprotection.ie/en/news-media/latest-news/irish-data-protection-commission-fines-tiktok-eu530-million-and-orders-corrective-measures-following>
107. EDPB news — TikTok €530M. <https://www.edpb.europa.eu/news/news/2025/irish-supervisory-authority-fines-tiktok-eu530-million-and-orders-corrective_en>
108. IAPP — TikTok €345M children's. <https://iapp.org/news/a/irelands-dpc-issues-345m-euro-tiktok-childrens-privacy-fine>
109. MediaNama — DPC X/Grok inquiry. <https://www.medianama.com/2025/04/223-irish-data-regulator-probe-x-eu-users-data-grok/>
110. noyb — Austrian DSB Google Analytics. <https://noyb.eu/en/austrian-dsb-eu-us-data-transfers-google-analytics-illegal>
111. noyb — Austrian DPA option €6B. <https://noyb.eu/en/austrian-dpa-has-option-fine-google-eu6-billion>
112. Privacy Laws & Business — UK ICO 2024 review. <https://www.privacylaws.com/reports-gateway/articles/uk139/uk139fines/>
113. URM Consulting — UK ICO 2025. <https://www.urmconsulting.com/blog/analysis-of-enforcement-action-by-the-ico-in-2025-enforcement-way-down-fines-way-up>
114. enforcementtracker.com — list of GDPR fines. <https://www.enforcementtracker.com/>
115. CMS — GDPR Enforcement Tracker. <https://cms.law/en/int/publication/gdpr-enforcement-tracker-report>
116. DLA Piper Privacy Matters — Spain AEPD 2024. <https://privacymatters.dlapiper.com/2025/06/spain-spanish-data-protection-authority-publishes-annual-report/>
117. Linklaters — Spain AEPD record fines. <https://techinsights.linklaters.com/post/102kcof/the-spanish-data-watchdog-ramps-up-enforcement-with-fines-totalling-over-35-5-mi>
118. CMS — Portugal CNPD enforcement. <https://cms.law/en/aut/publication/gdpr-enforcement-tracker-report/portugal>
119. noyb — official site / FAQs. <https://noyb.eu/en/faqs>
120. Wikipedia — NOYB. <https://en.wikipedia.org/wiki/NOYB>
121. noyb — 422 GDPR complaints Aug 2022. <https://noyb.eu/en/noyb-files-422-formal-gdpr-complaints-nerve-wrecking-cookie-banners>
122. noyb — 500+ campaign. <https://noyb.eu/en/noyb-aims-end-cookie-banner-terror-and-issues-more-500-gdpr-complaints>
123. CURIA — La Quadrature du Net case C-511/18. <https://curia.europa.eu/juris/document/document.jsf?docid=232084&doclang=en>
124. Columbia Global Freedom of Expression — LQDN/PI cases. <https://globalfreedomofexpression.columbia.edu/cases/the-cases-of-privacy-international-la-quadrature-du-net-and-others/>
125. Cohen Milstein — In re Meta Pixel Healthcare. <https://www.cohenmilstein.com/case-study/in-re-meta-pixel-healthcare-litigation/>
126. Milberg — Aurora Health $12.25M. <https://milberg.com/news/aurora-health-data-breach-proposed-settlement/>
127. The Lyon Firm — Meta pixel docket. <https://thelyonfirm.com/class-action/data-privacy/meta-pixel-tracking-lawsuit/>
128. HIPAA Journal — pixel settlements. <https://www.hipaajournal.com/healthcare-organizations-settle-website-tracking-class-action-lawsuits/>
129. Risk & Insurance — cookie/tracking SMB cyber. <https://riskandinsurance.com/cookie-and-tracking-litigation-emerges-as-a-major-cyber-loss-driver-for-smbs/>
130. Ogletree — website-tracker litigation update. <https://ogletree.com/insights-resources/blog-posts/website-tracker-litigation-continues-to-pose-compliance-headache-updates-on-cipa-and-related-litigation/>

### User ecosystem / tools

131. webXray.llc. <https://webxray.llc/>
132. Tim Libert CV. <https://www.timlibert.me/pdf/libert_cv.pdf>
133. Global Privacy Audit. <https://globalprivacyaudit.org/2026/california>
134. The Markup — Blacklight launch press release Sep 2020. <https://themarkup.org/press-release-20200922>
135. The Markup — How Blacklight was built. <https://themarkup.org/blacklight/2020/09/22/how-we-built-a-real-time-privacy-inspector>
136. The Markup — hospital-Pixel investigation. <https://themarkup.org/pixel-hunt/2022/06/16/facebook-is-receiving-sensitive-medical-information-from-hospital-websites>
137. The Markup — Senate inquiry follow-up. <https://themarkup.org/pixel-hunt/2022/09/19/meta-faces-mounting-questions-from-congress-on-health-data-privacy-as-hospitals-remove-facebook-tracker>
138. The Markup — 10M Blacklight scans. <https://themarkup.org/blacklight/2023/05/03/10-million-blacklight-scans-later-heres-what-you-found>
139. CalMatters — Blacklight TikTok/X update Feb 2026. <https://calmatters.org/economy/technology/2026/02/blacklight-update-tiktok-x-twitter/>
140. The Markup — Blacklight Query CLI Oct 2024. <https://themarkup.org/blacklight/2024/10/16/blacklight-query>
141. Knight Foundation — The Markup launch. <https://knightfoundation.org/press/releases/the-markup-news-organization-that-investigates-societal-impacts-of-technology-begins-buildout-for-launch-with-20-million-gift-from-craigslist-founder-craig-newmark-support-from-major-foundations/>
142. The Markup donors. <https://themarkup.org/donors>
143. Nieman Lab — Newmark pulling back from journalism. <https://www.niemanlab.org/2026/01/craig-newmark-explains-why-hes-pulling-back-on-funding-journalism/>
144. Exodus Privacy. <https://exodus-privacy.eu.org/en/>
145. PrivacyScore TU Darmstadt project page. <https://www.informatik.tu-darmstadt.de/privacy-trust/research_privacy_trust/research_5/research_area_c__privacy_and_trust_in_sensor_augmented_environments/c__1_privacy_protection_in_human_centered_sensor_augmented_environments/sub_project__privacyscore/index.en.jsp>
146. Privacy Badger GitHub (EFF). <https://github.com/EFForg/privacybadger>
147. EFF — Privacy Badger. <https://www.eff.org/pages/privacy-badger>
148. Disconnect tracker protection. <https://disconnect.me/trackerprotection>
149. Mozilla shavar-prod-lists. <https://github.com/mozilla-services/shavar-prod-lists>
150. EasyList. <https://easylist.to/pages/about.html>
151. OpenWPM GitHub. <https://github.com/openwpm/OpenWPM>
152. OpenWPM Englehardt-Narayanan 2015 PDF. <https://senglehardt.com/papers/openwpm_03-2015.pdf>
153. OpenWPM 1-million-site CCS 2016. <https://www.cs.princeton.edu/~arvindn/publications/OpenWPM_1_million_site_tracking_measurement.pdf>
154. OpenWPM Papers list. <https://openwpm.readthedocs.io/en/stable/Papers.html>
155. CNIL LINC — CookieViz 2.3. <https://linc.cnil.fr/en/cookieviz-23-new-more-secure-and-stable-version-and-focus-role-intermediaries>
156. CookieViz GitHub LINCnil. <https://github.com/LINCnil/CookieViz>
157. GPA award — CookieViz 2021. <https://globalprivacyassembly.com/wp-content/uploads/2021/07/B5.-CNIL-France-Innovation-CookieViz.pdf>
158. CyberSignal — state health exchanges to TikTok/Meta. <https://www.thecybersignal.com/state-health-exchanges-sent-citizenship-race-data-tiktok-meta-bloomberg-investigation/>
159. Le Monde / gblock — ad-tech exposed French spies. <https://www.gblock.app/articles/ad-tech-exposed-french-spies-email-privacy>
160. Follow The Money. <https://www.ftm.eu/>
161. Hogan Lovells — CNIL cookie sweep. <https://www.hoganlovells.com/en/publications/cnil-cookie-sweep-in-september-and-audits-in-october>
162. Hunton — CNIL sweep results. <https://www.hunton.com/privacy-and-cybersecurity-law-blog/cnil-publishes-internet-sweep-results-new-guidelines-websites-aimed-children>
163. Cookie Information — CNIL formal notice cookie banners. <https://cookieinformation.com/blog/cnil-formal-notice-dark-patterns-website-cookie-banners/>
164. IAB Tech Lab DDRF endorsement. <https://iabtechlab.com/press-releases/iab-tech-labs-data-deletion-request-framework-ddrf-endorsed-by-the-uk-information-commissioners-office/>
165. ICO 2025 Tech Horizons. <https://www.hunton.com/privacy-and-information-security-law/uk-ico-publishes-2025-tech-horizons-report>
166. Cookie-Script APAC summary. <https://cookie-script.com/privacy-laws/asia-pacific-nuances-appi-pipa-pdpa>
167. CMU CyLab — Cranor. <https://www.cylab.cmu.edu/directory/bios/cranor-lorrie.html>
168. CMU CyLab — Beyond the fine print. <https://www.cylab.cmu.edu/news/2025/11/14-beyond-the-fine-print.html>
169. Inria/Bielova — Gray et al. CHI 2021 PDF. <http://www-sop.inria.fr/members/Nataliia.Bielova/papers/Gray-etal-21-CHI.pdf>
170. Edelson PC firm page. <https://edelson.com/inside-the-firm/class-actions/>
171. Lowey — Meta Pixel medical data. <https://lowey.com/cases/facebook-meta-pixel-medical-data-collection-investigation/>
172. Hashmeta — CMP comparison. <https://hashmeta.com/blog/consent-management-platforms-onetrust-vs-cookiebot-vs-osano-complete-comparison-guide/>
173. Contrary research — OneTrust. <https://research.contrary.com/company/onetrust>
174. Cookiebot noyb writeup. <https://www.cookiebot.com/en/noyb-cookie-banners/>
175. Osano — comparisons. <https://www.osano.com/comparison/onetrust-competitors>
176. Securiti — LGPD cookies. <https://securiti.ai/blog/lgpd-cookies/>
177. Deloitte SOC 2 page. <https://www.deloitte.com/us/en/services/audit-assurance/services/third-party-assurance.html>
178. Schellman — SOC + Big 4. <https://www.schellman.com/blog/soc-examinations/which-audit-big-4-should-perform-your-soc-audit>
179. Bitsight — CAIQ vs SIG. <https://www.bitsight.com/blog/caiq-vs-sig-top-questionnaires-vendor-risk-assessment>
180. Shared Assessments — SIG. <https://sharedassessments.org/sig/>
181. Captain Compliance — cyber insurance 2026. <https://captaincompliance.com/education/cyber-insurance-in-2026-mfa-and-consent-management-are-mandatory/>
182. InformationWeek — Meta €1.3B. <https://www.informationweek.com/data-management/meta-hit-with-record-1-3b-gdpr-fine>
183. Dastra — adequacy table. <https://www.dastra.eu/en/blog/the-list-of-countries-deemed-adequate-for-gdpr-transfers-table/59031>
184. Byte Back — 2025 update website tracking. <https://www.bytebacklaw.com/2025/11/2025-update-website-tracking-litigation-and-enforcement/>
185. FTC blog — Lurking Beneath the Surface 2023. <https://www.ftc.gov/policy/advocacy-research/tech-at-ftc/2023/03/lurking-beneath-surface-hidden-impacts-pixel-tracking>
186. Morgan Lewis — Saudi PDPL enforcement. <https://www.morganlewis.com/pubs/2024/09/saudi-arabia-personal-data-protection-law-transition-period-ends-september-14>
187. CMS Lawnow — Saudi SDAIA rules. <https://cms-lawnow.com/en/ealerts/2024/09/new-sdaia-rules-and-guidelines-published-as-ksa-s-personal-data-protection-framework-is-now-enforceable>
188. TechCrunch — Amazon €746M. <https://techcrunch.com/2021/07/30/eu-hits-amazon-with-record-breaking-887m-gdpr-fine-over-data-misuse/>
189. Enzuzo — biggest GDPR fines. <https://www.enzuzo.com/blog/biggest-gdpr-fines>
190. Columbia — Brussels Effect scholarship. <https://scholarship.law.columbia.edu/books/232/>
191. Brussels Effect book site. <https://www.brusselseffect.com/>
192. Wikipedia — Brussels Effect. <https://en.wikipedia.org/wiki/Brussels_effect>
193. European Commission — adequacy decisions. <https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en>
194. Washington Post — Blacklight launch coverage. <https://www.washingtonpost.com/technology/2020/09/25/privacy-check-blacklight/>

---

## Section 8 — Open Questions for Alfred (no answers, just framing)

1. **Should the SSRP scope expand to include policy-text auditing via one of the 5 Section 1.4 angles?** (Decision needed in May; depends on Dr. Singh + Qiyao alignment Zoom.)
2. **Should the README's UMBRA description be corrected to remove "static snapshots"?** (Low-cost edit; aligns project framing with verified facts.)
3. **Should `data/sites.csv` include the China-overseas sub-cohort (B.1 advisory)?** (Deadline 2026-05-31 per `ssrp_scope_tweak_advisory.md`.)
4. **Should Layer 3 output an evidence-card export format optimized for NGO/journalism/plaintiffs' use?** (See §5.7.)
5. **Which of the 5 first-user types (§4.7) should Alfred design output for?** (Defer to post-SSRP, but design choices made now affect future fit.)
6. **Should the OpenAI Italian Garante annulment (Mar 2026) be cited alongside the original fine in the paper?** (Trivial; yes for academic honesty.)
7. **Which deferred items in §6 (9-17) are worth re-verifying for the v1 strategy doc?** (None block SSRP main line; re-verification can wait.)
8. **Should Alfred reach out to Bouhoula / Khandelwal / WebSP-Eval authors as potential collaborators?** (Their stacks are closest to his; they may be open to citation/collaboration.)

---

## Closing boundary statement

This document does not make decisions for Alfred. It separates fact from inference, lists what's verified and what's not, and stops short of recommending. Decision power is 100% Alfred's.
