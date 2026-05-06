# Background Research with Citations

**Author**: Qianyi (Alfred) Chen, with research assistance from Claude
**Date created**: 2026-04-26
**Status**: Phase A draft (core verifications). Phase B (broader lit review + regulatory framework + user ecosystem) will be appended after additional research-agent runs.
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

### Scope of Phase A (this draft)

Phase A verifies the most load-bearing claims that the assistant made in earlier conversation, plus the three papers Alfred specifically asked about (PRISMe, UMBRA/Abyss, ConsentDiff). It does **not** yet:
- Cover the 15-25 additional papers Alfred asked for ("狠狠查询")
- Cover the full GDPR / CCPA / DSA / RED legal scaffolding
- Cover the user-ecosystem question ("which countries / which users")
- Cover regulatory enforcement beyond TRUSTe and Shein

Phase B (research agents to be dispatched after rate-limit reset) will append those.

---

## Section 1.1 — The Three Papers Alfred Has Heard Of (verified)

### 1.1.1 PRISMe (CHI 2026) — VERIFIED ✅

> [CORRECTED] The assistant previously described PRISMe as "PRISMe (2025)". The arxiv submission is from January 2025 [1], but the **actual venue is ACM CHI 2026** [1]. The latest revision is January 2026 [1]. So citing it as "PRISMe (2026, CHI)" is more accurate than "(2025)".

`[FACT]` Full title: **"Helping Johnny Make Sense of Privacy Policies with LLMs"** [1].

`[FACT]` Authors: **Vincent Freiberger, Arthur Fleig, Erik Buchmann** [1]. (Affiliations not extracted from arxiv landing page; further verification possible via the linked PDF.)

`[FACT]` First arxiv submission: 2025-01-27. Latest revision: 2026-01-28. Venue: **ACM CHI 2026** [1].

`[FACT]` What it does (from the verbatim abstract [1]):
> "We present PRISMe, an interactive browser extension that combines LLM-based policy assessment with a dashboard and customizable chat interface, enabling users to skim quick overviews or explore policy details in depth while browsing. We conduct a user study (N=22) [...]"

`[FACT]` PRISMe's input is **privacy policy text** (the long legal documents) — not cookie banners or consent UI [1].

`[FACT]` PRISMe explicitly investigates a **RAG (retrieval-augmented generation) approach** to mitigate hallucination, after the user study surfaced concerns about adversarial robustness and hallucinations [1].

> [SUMMARY] PRISMe is a CHI-flavored, user-study-driven, LLM-based privacy policy explainer. It is **HCI-leaning** (N=22 user study, design implications) rather than measurement-leaning. The core artefact is a browser extension + dashboard + chat, not a large-scale audit pipeline.

> [INFERENCE — for Alfred's question "can I also audit policy text without overlapping PRISMe?"]
>
> PRISMe occupies a specific corner of the policy-text-with-LLM space:
> - Input: single policy at the time the user is browsing
> - Method: LLM + RAG, evaluated through user study
> - Output: an interpretive UI for one user reading one policy
>
> Open angles that **do not** overlap PRISMe (Alfred's call which to take):
> 1. **Longitudinal policy drift** — PRISMe is a single-policy explainer, not a measurement of how policies change over time. ConsentDiff at Scale [2] explicitly studies clause-level churn over time, but pairs it with UI; a paper that focuses purely on multi-year policy drift across thousands of sites is not closed.
> 2. **Cross-modal consistency between policy text and banner UI** — does the cookie banner say "essential cookies only" while the policy says ad-tech is implicit? PRISMe doesn't read banners; UMBRA [3] doesn't read policies. The seam is open.
> 3. **Policy-text framing analysis tied to specific GDPR/CCPA articles** as audit findings — PRISMe is user-facing explanation, not enforcement-grade evidence.
> 4. **Multi-language policy comprehension** — PRISMe English-centric; whether LLM accuracy degrades for Chinese/Japanese/Arabic policies is open.
>
> Each of these can cite PRISMe in Related Work without competing with it. Citing PRISMe as "the most recent and methodologically rigorous LLM-based policy work, focused on end-user comprehension" is honest positioning. **Decision: which (if any) of these to take is Alfred's.**

### 1.1.2 UMBRA / "When the Abyss Looks Back" — VERIFIED ✅, EARLIER CHARACTERIZATION PARTIALLY WRONG ⚠️

> [CORRECTED] The README.md and the assistant's prior summary said UMBRA "audits banner interfaces with rule-based heuristics, but uses no AI and only captures **static snapshots**" [Repo README]. Verification surfaces nuance:
> - "Rule-based heuristics, no AI/LLM" — **confirmed** [3]
> - "Only static snapshots" — **partially wrong**. UMBRA explicitly does **interaction tracing and stateful cookie monitoring** to "capture multi-step consent flows missed by prior tools" [3]. It is NOT a single-screenshot tool. Whether it is **longitudinal** (same site at multiple dates) was not extractable from the abstract alone — that question is still open.

`[FACT]` Full title: **"When the Abyss Looks Back: Unveiling Evolving Dark Patterns in Cookie Consent Banners"** [3]. UMBRA is the system name within that paper.

`[FACT]` Authors: **Nivedita Singh, Seyoung Jin, Hyoungshick Kim** [3]. Affiliations not extracted from landing page (Hyoungshick Kim is publicly known to be at Sungkyunkwan University in South Korea — `[UNVERIFIED]` for this paper specifically; Phase B should confirm).

`[FACT]` arxiv submission: **2026-03-23** (only v1 listed) [3]. arxiv ID: **2603.21515**. Category: cs.CR.

`[FACT]` What it does (verbatim abstract [3]):
> "We present UMBRA, a consent management platform (CMP)-agnostic system that detects both previously studied patterns (DP1-DP10) and nine newly evolved patterns (DP11-DP19) targeting information disclosure, consent revocation, and legal ambiguity, including pay-to-opt-out schemes, revocation barriers, and fake opt-outs. UMBRA combines text analysis, visual heuristics, interaction tracing, and cookie-state monitoring to capture multi-step consent flows missed by prior tools. We evaluate UMBRA on a manually annotated ground-truth dataset and achieve 99% detection accuracy. We further conduct a large-scale compliance-oriented measurement across 14,000 websites spanning the EU, the US, and top-ranked global domains. [...] On sites with revocation barriers, cookies increase by 25% on average [...]"

`[FACT]` Sample size: **14,000 websites** across EU + US + global [3].

`[FACT]` Self-reported detection accuracy on manually annotated ground truth: **99%** [3].

`[UNVERIFIED]` Whether UMBRA is longitudinal (same sites at multiple time points) or one-shot.
`[UNVERIFIED]` Whether code/dataset is open-sourced.
`[UNVERIFIED]` Author affiliations.

> [SUMMARY] UMBRA is a much more capable system than "static snapshot rule scanner" suggests. It does:
> - **Text analysis** of banner content
> - **Visual heuristics** on screenshots (button prominence, layout)
> - **Interaction tracing** (multi-click flows: Accept → Reject → Revoke)
> - **Cookie-state monitoring** (what cookies actually get set, when)
> - Detects **19 dark patterns** (DP1-DP10 from prior literature + DP11-DP19 their contribution)
>
> It is **rule-based** (no LLM/VLM), but it is **not static** — interaction tracing is the part Alfred should pay close attention to, because it is the closest existing thing to what an "agent-based dynamic auditor" does.

> [INFERENCE — for Alfred's positioning]
>
> The earlier project framing ("UMBRA is rule-based + static, we're AI + dynamic") is partly off. The accurate framing is:
> - UMBRA: **rule-based + interactive (multi-step) + non-AI**, 14,000-site cross-section
> - Alfred's project: **AI/LLM/VLM-grounded + interactive + longitudinal**, smaller sample, deeper time depth
>
> The differentiator is **NOT "we have agent-based traversal" (UMBRA already does interaction tracing)**. The defensible differentiators are:
> 1. **AI/LLM/VLM grounding** — UMBRA is brittle on novel layouts, dark-pattern variants outside DP1-DP19, and multi-language sites. LLM/VLM should generalize better, but Alfred has to demonstrate this empirically.
> 2. **Longitudinal depth** — UMBRA's 14k cross-section is broader than Alfred can match in one summer; Alfred's edge is **same site, every week, for >12 months**.
> 3. **Layer 3 (Transparency / Framing)** — UMBRA detects dark *interaction* patterns (DP11-DP19); UMBRA does not do nuanced **framing analysis of banner text** (neutral vs. nudging vs. coercive language). PRISMe does framing-ish work on policies, not banners. Alfred's Layer 3 sits in this gap.
> 4. **Volatility/Trajectory as primary metric** (already in `consent_audit_rubrics_landscape.md` §5.2) — UMBRA does not surface stability of compliance over time; Alfred's Compliance Trajectory + Volatility outputs are still novel.
>
> **What Alfred should NOT continue claiming**: "no one has done multi-step interactive consent audit before". UMBRA has. The honest claim is "no one has done multi-step interactive + AI-grounded + longitudinal + framing-aware audit before."
>
> **Decision is Alfred's**: whether to keep all four differentiators, drop Differentiator 1 (if VLM doesn't actually outperform UMBRA's heuristics) and double down on 2/3/4, or revise further. Phase B will help by surfacing what the rest of the lit looks like.

### 1.1.3 ConsentDiff at Scale (Haoze Guo) — VERIFIED ✅

`[FACT]` Full title: **"ConsentDiff at Scale: Longitudinal Audits of Web Privacy Policy Changes and UI Frictions"** [2].

`[FACT]` Single author: **Haoze Guo** [2]. arxiv ID: **2512.04316**. First submission: 2025-12-03. Latest revision: 2026-04-13 (v7).

`[FACT]` What it does (verbatim abstract [2]):
> "Web privacy is experienced via two public artifacts: site utterances in policy texts, and the actions users are required to take during consent interfaces. In the extensive cross-section audits we've studied, there is a lack of longitudinal data detailing how these artifacts are changing together, and if interfaces are actually doing what they promise in policy. ConsentDiff provides that longitudinal view. We build a reproducible pipeline that snapshots sites every month, semantically aligns policy clauses to track clause-level churn, and classifies consent-UI patterns by pulling together DOM signals with cues provided by screenshots. We introduce a novel weighted claim-UI alignment score [...]"

`[FACT]` Method: **DOM signals + screenshot cues + monthly snapshots + clause-level policy churn alignment** [2]. ConsentDiff explicitly tracks **both policy text AND UI** simultaneously, and aligns claims (in policies) to predicates (in UI).

`[FACT]` Sample / cadence (from the existing rubric landscape doc which inspected this paper [4]): 2,400 domains × 9 months = 21,600 site-month snapshots; geo: EU 900, US-CA 1000, Other 500.

> [SUMMARY] ConsentDiff is the **single closest related work** to Alfred's project. It is longitudinal, it spans both policy and UI, it has a quantitative alignment score. But it uses **DOM + weak-supervision vision** (not LLM/VLM); it has 9 months not >12; and it does not surface trajectory or volatility as a first-class output (the existing analysis in `consent_audit_rubrics_landscape.md` §1.7 confirmed this).

> [INFERENCE] ConsentDiff is what Alfred's Related Work section will lead with. The four differentiators above (AI grounding, longer time window, Layer-3 framing, volatility-as-output) are exactly the gaps ConsentDiff itself acknowledges or leaves unaddressed (per §1.7 of the existing rubric landscape doc, which Alfred wrote earlier).

---

## Section 6 — Self-Check of Assistant's Earlier Assertions

The user explicitly asked the assistant not to fabricate. Below is a checklist of every load-bearing claim the assistant made in **the conversation prior to this document**, with verification status.

| # | Earlier claim | Status | Notes / Citation |
|---|---|---|---|
| 1 | PRISMe (2025) audits privacy policy text with LLMs | ⚠️ Partially wrong | Title actually "Helping Johnny Make Sense of Privacy Policies with LLMs"; venue **CHI 2026**, not "2025"; arxiv submission was Jan 2025 but final revision Jan 2026. Mechanism description correct. [1] |
| 2 | UMBRA / "Abyss" (2026) audits banners with rule-based heuristics, no AI, **only static snapshots** | ⚠️ Partially wrong | "Rule-based, no AI" confirmed. **"Static snapshots" is wrong** — UMBRA does interaction tracing + cookie-state monitoring + multi-step flows. Authors: Nivedita Singh, Seyoung Jin, Hyoungshick Kim. arxiv 2026-03. [3] |
| 3 | ConsentDiff at Scale (Haoze Guo) | ✅ Verified | Title and author confirmed. arxiv 2512.04316. v7 latest 2026-04-13. [2] |
| 4 | FTC settled against TRUSTe in 2014 for "造假" | ✅ Verified | Date 2014-11-17 (final order 2015-03-18). Specific allegations: (a) failed to conduct annual recertifications in 1,000+ instances 2006-2013, (b) misrepresented non-profit status after becoming for-profit in 2008. Penalty: $200,000 + 10 years annual reporting. [5][6] |
| 5 | Edelman 2006 study showed TRUSTe sites had ~50% higher violation rate | ✅ Verified, slightly stronger than I said | January 2006, Benjamin Edelman, Harvard. **TRUSTe sites were 50% more likely to violate privacy policies** than uncertified sites — original framing accurate. More precise: 5.4% of TRUSTe sites rated "bad" vs 2.5% baseline = **>2× more likely**. So my "50% higher" was directionally right but actually understated. [7][8] |
| 6 | Shein €150M cookie fine | ✅ Verified | 2025-09-01, CNIL fined INFINITE STYLES SERVICES CO. LIMITED (Irish subsidiary of SHEIN). €150,000,000. Reasons: cookies before consent, incomplete banner, failure to honor refusals, missing third-party info. Shein is appealing. [9][10] |
| 7 | CNIL 2025 cookie enforcement total €486.8M | ✅ Verified | Actually total CNIL sanctions across **all categories** in 2025 = €486,839,500 across 83 sanctions. Of these, **21 sanctions were specifically for cookies**, dominated by Google €325M + Shein €150M = €475M. So **€486.8M is the all-category total, not the cookie-only total** — but cookies were the dominant category. [11] |
| 8 | ePrivacy Seal 2025-05 liquidation | ✅ Verified | EuroPriSe Cert GmbH ceased operations as of **2025-05-30**. Started 2003 as EU-funded project; converted to for-profit GmbH. ⚠️ Note: this is **not** the same as the EU's ePrivacy Regulation (proposal), which was separately dropped from the EU 2025 work programme on 2026-02-12 [12][13]. |
| 9 | 2026-02-20 Claude Code Security launch + cyber stock drops (CRWD -6.8%, Okta -9.2%, JFrog ~-25%) | ⏳ Not re-verified in Phase A | These were cited in v1 strategic doc with sources (CNBC, Bloomberg, SiliconAngle). Phase B should re-confirm if the strategic doc gets revised. Defer. |
| 10 | ETS 2024 revenue $1.16B; 30% from College Board contract | ⏳ Not re-verified in Phase A | Cited in `positioning_and_future_extension.md` §1.2. Defer to Phase B. |
| 11 | TOEFL founded 1964 by Ford Foundation + College Board + universities | ⏳ Not re-verified in Phase A | Defer to Phase B. |
| 12 | UL founded 1894 by insurance companies | ⏳ Not re-verified in Phase A | Defer to Phase B. |
| 13 | APEC Global CBPR launched 2025-06; Chinese mainland not participating | ⏳ Not re-verified in Phase A | Defer to Phase B. |
| 14 | China PIP cross-border certification effective 2026-01-01 | ⏳ Not re-verified in Phase A | Defer to Phase B. |
| 15 | Saudi PDPL 48 enforcement actions | ⏳ Not re-verified in Phase A | Defer to Phase B. |
| 16 | BYD outsold Tesla in Europe May 2025 | ⏳ Not re-verified in Phase A | Defer to Phase B. |
| 17 | ISC2 2025 survey: 77% list ISO 27001 / NIST / SOC 2 as top vendor requirement | ⏳ Not re-verified in Phase A | Defer to Phase B. |
| 18 | EuroPriSe was EDPB-endorsed under GDPR Art. 42 | ⏳ Not re-verified — note tension: I earlier said Europrivacy is the EDPB-endorsed seal, and that EuroPriSe is the predecessor that wound down | ⚠️ Risk of confusion. Phase B should clearly distinguish: **EuroPriSe** (wound down 2025-05) vs **Europrivacy** (currently EDPB-endorsed). [12] |

> [INFERENCE on the meta-question of trustworthiness]
> Of items 1-8 (verified in Phase A): **2 had material errors** (PRISMe venue/year; UMBRA "static" wording), **1 had a phrasing imprecision** (item 7, total vs. cookie-only). The rest were directionally correct. This is a useful prior on how much to trust the assistant's earlier free-flowing summaries: **mostly correct on direction, ~25% rate of factual imprecision worth catching**. Item 9-18 will get the same treatment in Phase B.

---

## Section 7 (Partial) — References Cited in Phase A

References are numbered for inline citations above. URL access dates: 2026-04-26.

1. Freiberger V., Fleig A., Buchmann E. **"Helping Johnny Make Sense of Privacy Policies with LLMs"**. arXiv:2501.16033. Submitted 2025-01-27, revised 2026-01-28. Venue: ACM CHI 2026. <https://arxiv.org/abs/2501.16033>
2. Guo H. **"ConsentDiff at Scale: Longitudinal Audits of Web Privacy Policy Changes and UI Frictions"**. arXiv:2512.04316. Submitted 2025-12-03, v7 2026-04-13. <https://arxiv.org/abs/2512.04316>
3. Singh N., Jin S., Kim H. **"When the Abyss Looks Back: Unveiling Evolving Dark Patterns in Cookie Consent Banners"** (system: UMBRA). arXiv:2603.21515. Submitted 2026-03-23. <https://arxiv.org/abs/2603.21515>
4. Chen Q. **`consent_audit_rubrics_landscape.md`**, repo `数据隐私审计系统研究`. Authored 2026-04-19 with assistance.
5. **FTC press release**: "TRUSTe Settles FTC Charges it Deceived Consumers Through Its Privacy Seal Program", 2014-11-17. <https://www.ftc.gov/news-events/news/press-releases/2014/11/truste-settles-ftc-charges-it-deceived-consumers-through-its-privacy-seal-program>
6. **FTC press release**: "FTC Approves Final Order In TRUSTe Privacy Case", 2015-03-18. <https://www.ftc.gov/news-events/news/press-releases/2015/03/ftc-approves-final-order-truste-privacy-case>
7. Edelman B. **"Adverse Selection in Online 'Trust' Certifications"**. Working paper, January 2006. <https://www.benedelman.org/publications/advsel-trust-draft.pdf>
8. Edelman B. — supplemental analysis "Certifications and Site Trustworthiness", 2006-09-25. <https://www.benedelman.org/news-092506/>
9. **CNIL press release**: "Cookies placed without consent: SHEIN fined 150 million euros by the CNIL", 2025-09-01. <https://www.cnil.fr/en/cookies-placed-without-consent-shein-fined-150-million-euros-cnil>
10. **EDPB news mirror**: "French SA: Cookies placed without consent: SHEIN fined 150 000 000 EUR by the CNIL", 2025. <https://www.edpb.europa.eu/news/national-news/2025/french-sa-cookies-placed-without-consent-shein-fined-150-000-000-eur-cnil_en>
11. **CNIL**: "Sanctions and corrective measures: CNIL's actions in 2025". <https://www.cnil.fr/en/sanctions-and-corrective-measures-cnils-actions-2025>. Cross-reference: BABL AI summary, "France's Data Protection Authority Issues €486.8 Million in Fines as Cookie Violations and Workplace Surveillance Lead 2025 Enforcement". <https://babl.ai/frances-data-protection-authority-issues-e486-8-million-in-fines-as-cookie-violations-and-workplace-surveillance-lead-2025-enforcement/>
12. **EuroPriSe Cert GmbH closure notice** at <https://euprivacyseal.com/en/> (accessed 2026-04-26): operations ceased 2025-05-30. Cross-reference: Privacy Seal — Wikipedia. <https://en.wikipedia.org/wiki/Privacy_seal>
13. **CMS Law Now**: "ePrivacy Regulation Cancelled in EU's 2025 Work Programme", Feb 2025. <https://cms-lawnow.com/en/ealerts/2025/02/eprivacy-newsletter-february-2025>

---

## Sections to Be Filled in Phase B

Pending after rate-limit reset and dispatch of three research agents:

- **Section 1.2** — 15-25 additional academic papers (Bouhoula SoK; Santos; Soe; Kretschmer TCF auditing; Bollinger CMP measurement; Rasaii mobile; Mathur dark-pattern shopping; Gunawan deceptive patterns taxonomy; Habib CMU consent flow; Sanchez-Rola; Hils LLM policy; etc.). Per-paper format: authors / year / venue / URL / 2-sentence method / 1-sentence "what it does NOT do".
- **Section 1.3** — 3D positioning cube (static↔dynamic × rules↔AI × banner↔policy↔multimodal) showing which cells are crowded vs empty.
- **Section 1.4** — Detailed answer to "can Alfred audit policy text without overlapping PRISMe?" with 3-5 angles scored on (overlap risk, novelty, feasibility), as `[INFERENCE]` only.
- **Section 2** — Regulatory framework: GDPR Articles 3 / 6 / 7 / 12 / 13-14 / 22 / 32 / 42 / 79 / 80 with EUR-Lex URLs; ePrivacy Directive vs GDPR distinction; CCPA / CPRA / CIPA / FTC §5; PIPL / CSL / DSL; LGPD / PDPL / PIPA / DPDP. **Who can sue / fine** under each.
- **Section 3** — Other significant enforcement actions in 2024-2026: Italian Garante (OpenAI), Irish DPC (Meta, TikTok), Austrian DSB, ICO, Dutch AP, German DPAs. China-export-specific cases: Temu DSA, TikTok CFIUS+DPC+ICO, Hikvision NDAA — distinguishing privacy-fixable vs geopolitical.
- **Section 4** — User ecosystem: real adoption stories of PrivacyScore, EXODUS Privacy, WebXray, Blacklight; user catalog by type (journalists / NGOs / DPAs / academics / plaintiffs' lawyers / procurement / Big-4 / insurers); country distribution; **GDPR extraterritorial Art. 3 + "Brussels effect"** explained with cases (Meta, Amazon, OpenAI fined under GDPR despite being US-based). Honest motivation map (humanitarian vs commercial vs regulatory vs journalism vs academic — including mixed motives like noyb's funding model).
- **Section 5** — `[INFERENCE]`-only block: how the verified findings might inform Alfred's SSRP scope decisions. **Pure suggestions, decision is Alfred's.**
- **Section 8** — Open questions for Alfred (no answers; just framing).

---

## Boundary Statement (repeated from §0)

This document **does not** make decisions for Alfred. It separates fact from inference, lists what's verified and what's not, and stops short of recommending. If Alfred wants to take any of the inferences as decisions, that is his call. If he wants to challenge any `[FACT]`, he can click the citation.
