# CONCEPTS.md — Audit Ontology

This file is the **single source of truth** for every audit dimension name, definition, input, and output in this project. Every module, every test, every paper chapter must use the vocabulary defined here — verbatim. If a definition needs to evolve, evolve it **here first**, then propagate.

**Rule of thumb**: if you cannot cite a line in this file to justify a scoring decision, the decision is ad-hoc and must be rejected in review.

---

## 0. Background vocabulary

**Consent Interface**: the full multi-layered UI that a website presents to a visitor to obtain consent for data collection. Includes: the **first-layer banner** (pop-up on page load), any **second-layer panel** (settings / preference center) reached from the first layer, and the **third-layer policy link** (full privacy policy) if linked from within the banner. This project audits **first and second layers**. The third layer is out of scope (covered well by PRISMe).

**Consent Pathway**: a user-reachable outcome of the consent decision. The project enumerates exactly four:
- **Accept** — agree to all / optional data processing
- **Reject** — refuse all / optional data processing
- **Customize** — open the second layer to choose per-category
- **Dismiss** — close the banner without making an explicit choice (often treated as implicit accept by the site — which itself is a finding)

**Capture Bundle**: the multimodal snapshot of one site at one time, produced by `capture.agent`. Contains, per layer visited: a screenshot, a DOM serialization, the extracted visible text, and a structured event log of agent actions. See `models/audit.py::CaptureBundle`.

**Multimodal Fingerprint**: a tuple `(dom_hash, perceptual_image_hash, text_embedding_vector)` used by the diff engine to cheaply detect when a site's consent interface has meaningfully changed week-to-week. Not an audit dimension, a tracking primitive.

---

## 1. Layer 1 — Path Availability

**What it measures**: whether each of the four consent pathways is *present and reachable* in the UI.

**Input**: `CaptureBundle` (first and second layers).

**Output**: `Layer1Result`
```
accept_available:     bool
reject_available:     bool     # must be reachable within 2 user actions from the first layer
customize_available:  bool
dismiss_available:    bool
missing_paths:        list[str]
evidence:             dict[str, ElementRef]   # pathway name → DOM element + bounding box
```

**Scoring rule**: 
- If `reject_available = False` or `customize_available = False`, the interface is flagged **High Risk** regardless of Layer 2/3 results.
- An `accept_available = False` site is unusual but not a compliance risk; flag as **Note** only.
- `dismiss_available` is informational — its *effect* (does dismissal equal consent?) is part of Layer 3, not here.

**Specific tests a Layer-1 implementation must pass** (see `tests/layers/test_layer1.py`):
1. A site with a visible "Reject All" button on the banner → `reject_available = True`.
2. A site where "Reject All" requires opening Customize → opening Customize → clicking a hidden toggle → `reject_available = False` (violates 2-action rule). This is UMBRA's DP15 pattern.
3. A site with no explicit close "X" and no obvious dismiss area → `dismiss_available = False`.

**Why this layer is a gate**: the downstream layers measure how hard a path is or how biased its framing is. If a path doesn't exist, those measurements are meaningless.

---

## 2. Layer 2 — Path Effort

**What it measures**: how much operational effort a user must expend to execute each pathway. Path Effort is an **independent risk signal** *and* a **weighting factor** applied to Layer 3.

**Input**: `CaptureBundle` + `Layer1Result` (skip paths that don't exist).

**Output**: `Layer2Result`
```
per_path_effort:    dict[pathway, EffortScore]
overall_category:   {"Easy", "Average", "Poor"}
```

Where `EffortScore` is a continuous value in `[0.0, 1.0]` (0 = trivially easy, 1 = maximally friction), composed of six sub-features. Each sub-feature is measured independently and combined by a deterministic weighted sum (weights are project-defined, fixed, documented here):

| Sub-feature | Definition | Weight | Source |
|---|---|---|---|
| `button_size_ratio` | min(path_button_area) / max(path_button_area) across all pathways. <1.0 means this path's button is smaller than a sibling. | 0.25 | VLM vision output |
| `color_contrast` | WCAG contrast ratio between button and banner background. Low contrast → hard to find. | 0.15 | deterministic from pixel values |
| `layout_symmetry` | 1 if all pathways are at the same visual level / alignment; penalized if this path is visually demoted (smaller font, subtler placement). | 0.15 | VLM vision output |
| `click_depth` | Number of user actions from first-layer banner appearance to path execution. 1 action = no friction. | 0.20 | Agent event log |
| `label_clarity` | Whether the button label is direct ("Reject All") vs. euphemistic ("Manage Preferences", "Show Purposes") for a reject action. | 0.15 | VLM + LLM joint judgment with rubric |
| `immediate_feedback` | Whether clicking the path produces clear confirmation vs. silent state change. | 0.10 | Agent event log |

**Score aggregation**: `EffortScore(path) = Σ w_i × feature_i(path)` → normalize to [0,1].

**Overall category mapping** (across all paths weighted equally):
- `Easy`:    mean effort ≤ 0.30
- `Average`: 0.30 < mean effort ≤ 0.60
- `Poor`:    mean effort > 0.60

**Traceability requirement**: every sub-feature value in the output MUST be accompanied by `evidence: ElementRef | ScreenshotBBox | EventLogRef`. A value without evidence is a schema violation.

---

## 3. Layer 3 — Transparency & Unbiased Choice

Layer 3 splits into two analytically distinct scores. They are deliberately **not combined** into one number, because their causes and remedies differ.

### 3.1 Transparency

**What it measures**: the communicative quality of privacy information — is it clear, complete, and consistent across interface layers?

Two independent sub-scores:

#### 3.1a Disclosure Topic Coverage
**What**: whether the banner (first layer) explicitly discloses each of the four mandatory topic categories:
1. **Data types collected** — cookies, identifiers, behavioral data, etc.
2. **Purposes of use** — personalization, advertising, analytics, etc.
3. **Third-party sharing** — advertisers, partners, affiliates, data brokers
4. **Decision consequences** — what changes if I accept vs. reject?

**Output per topic**:
```
present:           bool
clarity_grade:     {"A", "B", "C", "F"}  # A = specific+concrete, F = absent-or-misleading
evidence_quote:    str                   # verbatim text span from banner
consistent_with_layer2:  bool            # same topic appears & agrees in settings panel
```

**Rubric for `clarity_grade`**:
- A: Specific, concrete, no weasel words. "We share your email with Meta and Google for ad targeting."
- B: Topic clearly named but with some vagueness. "We share data with advertising partners."
- C: Acknowledged but evasive. "We may share data with selected partners."
- F: Missing or actively misleading.

#### 3.1b Communicative Framing Effects
**What**: how factually-equivalent information is framed across the consent flow, measured along four mechanisms. Each mechanism is `{"neutral", "mild_bias", "strong_bias"}`.

1. **Emphasis patterns** — visual or textual prominence of benefits vs. risks (e.g., "improve your experience" in large text, "we track you" in small text).
2. **Linguistic complexity** — Flesch-Kincaid grade level differential between positively-framed and negatively-framed text.
3. **Information sequencing** — does the banner lead with benefits of acceptance, with risks of rejection, or neutrally? Order matters per cognitive-bias literature.
4. **Benefit/risk selective prominence** — are positive outcomes of acceptance mentioned but negative outcomes of acceptance omitted (and vice versa)?

**Aggregation**: Any single mechanism at `strong_bias` drops Transparency score one full letter grade. Two or more at `mild_bias` drops one grade.

**First-layer weighting**: first-layer disclosures carry 2× the weight of second-layer disclosures in the final Transparency score, because of the dominant-anchor effect on user interpretation (justification in the paper, cited to Martin & Murphy 2016).

**Final Transparency output**:
```
topic_coverage:  dict[topic, TopicResult]
framing:         dict[mechanism, BiasLevel]
letter_grade:    {"A", "B", "C", "D", "F"}
rationale:       str    # LLM-generated, citing specific evidence refs
```

### 3.2 Unbiased Choice

**What it measures**: whether the **visual and structural presentation** of consent options systematically favors one pathway over others. Deliberately narrower than Transparency — concerned only with observable asymmetry, not communication quality.

**Input**: VLM output on the banner screenshot + DOM structural analysis.

**Features**:
- `visual_prominence_asymmetry`: dominant-color saturation, button-shadow difference, hover/focus styling
- `structural_asymmetry`: whether buttons are visually grouped as siblings (neutral) or separated with hierarchy (e.g., Reject as a text link next to a big Accept button)
- `default_state`: whether any toggles are pre-checked in favor of consent

**Output**:
```
asymmetry_score:   float    # 0 = perfectly symmetric, 1 = maximally biased
biased_toward:     {"accept", "reject", "none"}   # usually "accept" if biased
evidence:          list[ElementRef]
letter_grade:      {"A", "B", "C", "D", "F"}
```

**Separation from Transparency**: a site CAN score A on Unbiased Choice while scoring F on Transparency (buttons are equally sized and colored, but the text around them manipulates through framing). And vice versa. **Never collapse these two into a single score.** The paper's reviewers will check for this collapse.

---

## 4. Overall Audit Score

The project **does not** emit a single scalar "privacy grade." It emits a structured report with multiple dimensions. If external consumers need a summary (e.g., for the demo site's leaderboard), use the following categorical summary, *not* a weighted sum:

```
Tier = {
  "Exemplary":       Layer-1 all available ∧ Layer-2 Easy ∧ Transparency ≥ B ∧ Unbiased ≥ B
  "Compliant":       Layer-1 reject+customize available ∧ Layer-2 ≤ Average ∧ Transparency ≥ C ∧ Unbiased ≥ C
  "Marginal":        Layer-1 passes gate ∧ (Layer-2 Poor OR Transparency D OR Unbiased D)
  "High-Risk":       Layer-1 fails gate OR any combined Layer-2 Poor + Transparency/Unbiased ≤ D
}
```

**Design rationale**: weighted scalar scores encourage optimization toward a number and obscure root causes. Tiered categorical summaries keep the underlying dimensions legible.

---

## 5. Longitudinal Primitives

**Change Event**: produced by the diff engine when two consecutive captures of the same site differ beyond threshold on any fingerprint channel. Types:

| Type | Trigger |
|---|---|
| `layout_change` | perceptual image hash distance > threshold |
| `copy_change` | text embedding cosine < threshold |
| `dom_restructure` | DOM hash differs AND layout_change detected |
| `pathway_change` | Layer-1 availability booleans changed |
| `score_change` | any Layer-2/3 score category changed |

**Weekly Summary**: produced by LLM over the week's Change Events for a site. Structured as `{summary, severity, implications_for_user}`. **LLM is summarizing, not judging** — the judgment is already in the Layer results; the summary just makes the week's diff human-readable.

---

## 6. Things this ontology deliberately excludes

These are **not** first-class dimensions in this audit:

- **Runtime tracker behavior** — Privado / Feroot cover this; we're about interface design
- **Cookie lifecycle analysis** — UMBRA / CookieBlock cover this; we're about the decision moment
- **Privacy policy full-text audit** — PRISMe covers this; we're about the banner / second-layer interface
- **Legal compliance determination** — we emit *design-level risk signals*, not legal opinions. The phrase "compliance risk indicator" is intentional; "compliance violation" is forbidden in our output.
- **GDPR-vs-CCPA differential analysis** — deferred post-summer

If a feature request implies one of these, push back or route to an explicit extension ticket.
