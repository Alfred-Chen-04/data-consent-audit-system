# Legal Cheatsheet — 8 Articles Alfred Must Master

**Purpose**: A 1-page lookup card for the legal anchors of this audit system. Every scoring decision in Layers 1/2/3 should be traceable to one of these. Use this when writing the paper, designing rubrics, or drafting outreach.

**Read first, then use as reference**. Estimated mastery time: 30 minutes.

---

## The 8 Articles

### 1. GDPR Art. 4(11) — Definition of "consent"

> "any **freely given, specific, informed and unambiguous** indication of the data subject's wishes by which he or she, by a statement or by a clear affirmative action, signifies agreement to the processing of personal data relating to him or her."

- **The four conditions** (memorize verbatim): freely given · specific · informed · unambiguous.
- **Where it bites**: any audit finding can be re-stated as "consent fails one of these four."
- **Maps to**: the entire reason Layer 1 exists.
- **Cite**: [EUR-Lex consolidated GDPR](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02016R0679-20160504) · [gdpr-info Art. 4](https://gdpr-info.eu/art-4-gdpr/)

### 2. GDPR Art. 7 — Conditions for consent

Four operative rules:
- **7(1)** Controller must be able to *demonstrate* consent was given.
- **7(2)** Consent request must be clearly distinguishable from other matters, intelligible, easily accessible.
- **7(3)** **Withdrawal must be as easy as giving consent** ← the single most-cited operative rule.
- **7(4)** Consent is "not freely given" if performance of a contract is conditioned on consent that is not necessary for that contract.

- **Maps to**: Layer 1 (Reject pathway must exist + must be reachable in ≤2 actions, mirroring how Accept is reachable). CNIL operationalizes 7(3) as "Reject must be same size, same depth as Accept."
- **Cite**: [gdpr-info Art. 7](https://gdpr-info.eu/art-7-gdpr/)

### 3. GDPR Art. 12 — Transparent information

Information must be in **concise, transparent, intelligible, easily accessible form**, in **clear and plain language**.

- **Maps to**: Layer 3 (banner text framing). If a banner uses legalese, hides the third-party list behind two layers, or uses ambiguous phrasing, that is an Art. 12 finding — not an Art. 7 finding.
- **Cite**: [gdpr-info Art. 12](https://gdpr-info.eu/art-12-gdpr/)

### 4. GDPR Art. 3 — Territorial scope (extraterritorial)

- **3(1)** Controllers established in the Union, regardless of where processing occurs.
- **3(2)** Non-EU controllers when (a) offering goods/services to EU data subjects, OR (b) monitoring their behaviour.

- **Why it matters for you**: Lets you audit a US- or China-based site under GDPR if it serves EU users. Demonstrated by real fines: Clearview AI (US) €30.5M Dutch DPA 2024-05-16; OpenAI (US) €15M Italian Garante 2024-12-20 (note: Court of Rome annulled this 2026-03-18 — cite both).
- **Maps to**: justifies why your site sample doesn't need to be EU-only.
- **Cite**: [gdpr-info Art. 3](https://gdpr-info.eu/art-3-gdpr/) · [EDPB Guidelines 3/2018 on territorial scope](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-32018-territorial-scope-gdpr-article-3-version_en)

### 5. GDPR Art. 80 — Representation of data subjects

Non-profit bodies active in data-protection rights may, on a data subject's mandate (80(1)) — or independently where Member State allows (80(2)) — lodge complaints, seek judicial remedy, claim compensation. Implemented liberally in Germany, France, Italy, Belgium.

- **Why it matters for you**: this is the legal basis for noyb / La Quadrature du Net to file complaints using your audit data. **CNIL €50M Google fine (Jan 2019) was triggered by joint Art. 80 complaints from noyb + LQDN.**
- **Maps to**: justifies the "NGO evidence database" Track 1 positioning — your output has a direct legal pipeline.
- **Cite**: [gdpr-info Art. 80](https://gdpr-info.eu/art-80-gdpr/)

### 6. ePrivacy Directive Art. 5(3) — The actual cookie law

> "Member States shall ensure that the storing of information, or the gaining of access to information already stored, in the terminal equipment of a subscriber or user is only allowed on condition that the subscriber or user concerned has given his or her consent, having been provided with clear and comprehensive information..."

- **The thing 95% of cookie fines are based on** — not GDPR. Transposed into national law in each Member State (e.g., Art. 82 of France's Loi Informatique et Libertés is the CNIL's hook for the Shein €150M and Google €325M fines).
- **Crucial difference from GDPR**: ePrivacy bypasses the GDPR "one-stop-shop" — **27 national DPAs can act in parallel** on cookie violations. This is why CNIL (France) keeps issuing the biggest cookie fines.
- **Maps to**: the legal underpinning of Layer 1. When you say "this cookie was set before consent was given," ePrivacy 5(3) is what was violated.
- **Cite**: [Directive 2002/58/EC consolidated on EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02002L0058-20091219)

### 7. EDPB Guidelines 03/2022 — Deceptive Design Patterns (the official taxonomy)

EDPB's official 6-category taxonomy of dark patterns in social-media interfaces (the only official EU-level taxonomy for consent UI):

| Category | Plain language | Example in cookie context |
|---|---|---|
| **Overloading** | Too many choices, walls of options | 47-toggle settings panel hiding the master Reject |
| **Skipping** | Designing flow so user skips key info | Auto-scrolling past the privacy choice |
| **Stirring** | Manipulating via emotion | "Are you sure you want to leave us??" guilt prompt |
| **Obstructing** | Adding friction to certain choices | Reject requires 4 clicks, Accept requires 1 |
| **Fickle** | Inconsistent design | Reject button moves around or changes wording |
| **Left in the Dark** | Hiding key information | Third-party list buried under "Customize → Vendors → 856 partners" |

- **Maps to**: Layer 2 (Path Effort) and Layer 3 (Framing) tagging. Each finding can carry one or more of these as labels.
- **Cite**: [EDPB Guidelines 03/2022 PDF](https://www.edpb.europa.eu/system/files/2023-02/edpb_03-2022_guidelines_on_deceptive_design_patterns_in_social_media_platform_interfaces_v2_en_0.pdf)
- **Bonus**: The EDPB + EEA member states formed a "Cookie Banner Taskforce" in 2023 that publishes coordinated investigation results — your data could feed this.

### 8. CNIL 2021 Guidelines — The operational baseline

CNIL operationalized the abstract Art. 7 rules into a concrete UI test:

- "Accept All" present ⇒ "Reject All" must be present at the **same level**, with **equivalent visual prominence** (size, color, contrast).
- The number of clicks to refuse must be **≤** the number of clicks to accept.
- Refusing must NOT be "more troublesome" than accepting.

- **Why it matters for you**: this is the most concrete benchmark in the entire legal corpus. Your Layer 2 metrics (`reject_depth`, `reject_time`, `visual_prominence_ratio`) are direct CNIL operationalizations.
- **Enforcement teeth**: Google €60M+€40M (Dec 2020) and Amazon €35M (Dec 2020) under exactly these rules. Then Google €325M and Shein €150M in 2025 reinforcing.
- **Cite**: [CNIL "Refusing cookies should be as easy as accepting them"](https://www.cnil.fr/en/refusing-cookies-should-be-easy-accepting-them-cnil-continues-its-action-and-issues-new-orders)

---

## Quick Mapping — Which Article Justifies Which Layer

```
Layer 1 (Path Availability)
  ├── Reject must exist                     → GDPR Art. 4(11) "specific" + Art. 7
  ├── Reject must be reachable ≤ 2 actions  → CNIL 2021 Guidelines (operationalizes Art. 7(3))
  └── Cookies must not be set pre-consent   → ePrivacy Art. 5(3)

Layer 2 (Path Effort)
  ├── Reject visual prominence              → CNIL 2021 + EDPB "Obstructing"
  ├── Click depth comparison                → CNIL 2021 + EDPB "Obstructing"
  └── Withdraw flow effort                  → GDPR Art. 7(3)

Layer 3 (Transparency & Framing)
  ├── Disclosure topic coverage             → GDPR Art. 12 + Art. 13
  ├── Plain-language requirement            → GDPR Art. 12
  ├── Framing neutrality                    → GDPR Art. 4(11) "freely given"
  └── Dark-pattern category labels          → EDPB Guidelines 03/2022 (6 categories)

Cross-cutting
  ├── Why audit non-EU sites                → GDPR Art. 3(2)
  └── Why NGOs would consume your data      → GDPR Art. 80
```

---

## Use This Cheatsheet When You

- Define a new audit metric → check it maps to an article above; if not, the metric is ad-hoc.
- Write the paper's Background / Methods → cite the relevant article verbatim with EUR-Lex / EDPB primary URL.
- Draft outreach email to NGO / DPA / journalist → invoke Art. 80 (for NGOs) or Art. 3(2) (for non-EU users).
- Triage a finding → tag it with one of the 6 EDPB categories so it's actionable downstream.

---

## What's NOT in this cheatsheet (deliberately)

- US law (CCPA, CIPA, BIPA, VPPA, FTC §5) — these matter only when you scope to US sites; if you do, see [`background_with_citations.md`](./background_with_citations.md) §2.3.
- China law (PIPL, CSL, DSL) — only relevant for the Track 2 commercial extension (post-September); see [`../strategy/positioning_and_future_extension.md`](../strategy/positioning_and_future_extension.md).
- GDPR Articles 6, 22, 32, 42 — relevant for general privacy compliance but not directly for cookie-banner auditing. See `background_with_citations.md` §2.1.
- Brazil LGPD, Saudi PDPL, Korea PIPA, India DPDP — out of scope for SSRP 2026.

---

**Source of truth**: [`background_with_citations.md`](./background_with_citations.md) §2.1-2.3. This cheatsheet is a derived summary; if any conflict arises, the longer doc with full citations wins.
