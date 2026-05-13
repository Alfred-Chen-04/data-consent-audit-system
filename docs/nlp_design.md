# NLP Design — Prompts, Schemas, Rubrics, Ground Truth

**Status**: Design draft 2026-05-12. NO code written yet. This doc captures the design for review **before** implementation begins.

**Scope**: Three NLP tasks required by [CONCEPTS.md](../CONCEPTS.md) — nothing more. Specifically, this doc covers ONLY first-layer + second-layer text (matching the SSRP proposal scope per [SCHEMA.md §1](../SCHEMA.md)). Policy-long-text NLP is out of scope.

**Authority hierarchy**:
- [CONCEPTS.md](../CONCEPTS.md) defines what each metric MEASURES — authoritative for semantics
- [src/consent_audit/models/audit.py](../src/consent_audit/models/audit.py) defines the Pydantic data classes — authoritative for shape
- This doc designs the LLM prompts, ground-truth datasets, and evaluation methods that go between them

If any conflict: CONCEPTS wins for semantics, models/audit.py wins for shape, this doc wins for prompt + eval.

---

## 0. Cross-cutting Invariants (apply to all 3 tasks)

Every NLP task in this project obeys these rules:

### 0.1 Verbatim evidence (anti-hallucination)
Every claim returned by an LLM MUST carry an `evidence_quote` that is **a substring of the input text** (case-insensitive, ignoring whitespace).

After every LLM call, the wrapper validates:
```python
assert evidence_quote.strip().lower() in input_text.strip().lower(), \
    f"hallucinated quote: {evidence_quote!r}"
```
If validation fails → retry once with a schema-correction prompt. If retry fails → return conservative default + `confidence_low = True`.

### 0.2 Schema enforcement
All LLM outputs are returned as JSON validated by Pydantic. Schemas live in [src/consent_audit/models/audit.py](../src/consent_audit/models/audit.py). On JSON parse failure or Pydantic ValidationError:
- Retry once with the validation error message appended to the prompt
- On second failure: conservative default + `confidence_low = True`

### 0.3 No side effects in LLM calls
LLM/VLM call functions are pure: take input, return Pydantic object. They do NOT write to DB, object store, or filesystem. All persistence happens in the orchestration layer (`scripts/run_audit.py`, `scripts/run_weekly.py`).

### 0.4 Budget cap per call
Every LLM call must check `llm.budget.is_under_cap()` BEFORE invocation. If over cap → raise `BudgetExceededError` to orchestration; do NOT silently degrade.

### 0.5 Determinism
Use `temperature = 0.0`, `top_p = 1.0`, fixed `seed` where the provider supports it. The same input produces the same output across runs. This is required for the longitudinal RQ2 — we cannot diff results week-over-week if scoring is noisy.

### 0.6 Model selection (deferred to §10 Decision 5 in SCHEMA)
Until benchmark is run, default to:
- **LLM**: `claude-opus-4-7` for text reasoning (Layer 3 framing, topic coverage)
- **VLM**: `claude-sonnet-4-6` for vision tasks (out of scope for this doc — covered separately in vision design)
- Fallback: `gpt-4o-2024-08-06` if Anthropic rate-limited

---

## 1. NLP-1: Layer 2 `label_clarity`

### 1.1 What it measures
For each pathway (Accept / Reject / Customize / Dismiss), how clearly the button label describes what action that button performs. CONCEPTS.md §2 row 5:

> `label_clarity` — Whether the button label is direct ("Reject All") vs. euphemistic ("Manage Preferences", "Show Purposes") for a reject action.

This is **one of six sub-features** in the Layer 2 Path Effort score (weight = 0.15 in the deterministic weighted sum).

### 1.2 Input

```python
class LabelClarityInput(BaseModel):
    pathway: Pathway                   # which pathway this button is the trigger for
    button_text: str                   # verbatim, e.g., "Manage Preferences"
    surrounding_banner_text: str       # the banner-text context, for disambiguation
    button_role: Literal["primary_button", "secondary_button", "link", "icon"]
```

Why include `surrounding_banner_text`: a button labeled "Continue" can mean different things depending on what the banner says above it ("By continuing you accept" vs "Continue to settings"). Context disambiguates.

### 1.3 Output

```python
class LabelClarityCategory(str, Enum):
    direct = "direct"           # 1.0
    near_direct = "near_direct" # 0.7
    euphemistic = "euphemistic" # 0.4
    deceptive = "deceptive"     # 0.0

class LabelClarityResult(BaseModel):
    pathway: Pathway
    category: LabelClarityCategory
    score: float = Field(ge=0.0, le=1.0)       # derived from category, but stored explicitly
    rationale: str                              # ≤ 50 words
    evidence_quote: str                         # verbatim button text
    confidence_low: bool = False
```

The score is mapped deterministically from category to avoid LLM-introduced numeric noise:
```python
SCORE_MAP = {direct: 1.0, near_direct: 0.7, euphemistic: 0.4, deceptive: 0.0}
```

### 1.4 Rubric (with anchored examples)

| Category | Score | Definition | Examples (reject pathway) | Examples (accept pathway) |
|---|---|---|---|---|
| **direct** | 1.0 | The label names the action plainly and unambiguously, using the verb of the action. | "Reject All", "Decline", "Refuse Cookies", "Decline All Cookies" | "Accept All", "Agree", "I Accept" |
| **near_direct** | 0.7 | Names the action with a softening or framing that is still unambiguous in context. | "No thanks", "Continue without accepting", "Reject non-essential", "Save my settings" (when no toggles changed) | "OK", "Continue", "Got it" (when context is consent) |
| **euphemistic** | 0.4 | Names a related but indirect action; the user must infer the privacy consequence. | "Manage Preferences", "Show Purposes", "Cookie Settings", "Customize", "More Options" (when this is the only path to reject) | "Personalize", "Improve Experience" |
| **deceptive** | 0.0 | The label misrepresents what the button does OR there is no usable label (icon only with no aria-label). | "Continue to site" (actually Accept All), "X" close button that records implicit accept, no clear text | "Privacy Policy" used as the only opt-in trigger |

Notes:
- A "Save Settings" button when the user did NOT change defaults from "Accept" is **near_direct** for that user's intended reject pathway only if Reject is genuinely available as a separate button. If "Save Settings" is the only way to confirm a manually-built reject, then it's **direct**.
- "Customize" is **euphemistic for reject** when the customize panel is the only path to reject. But "Customize" is **direct for the customize pathway itself**. Score per pathway, not per button.

### 1.5 Prompt design

**System message**:
```
You are a privacy interface auditor.

Your job is to classify how clearly a single button label tells a user what the
button does. You receive one button's text, the pathway it triggers, and the
banner text around it for context.

You return JSON matching this schema EXACTLY:
{
  "category": one of "direct" | "near_direct" | "euphemistic" | "deceptive",
  "rationale": a sentence under 50 words explaining the choice,
  "evidence_quote": the verbatim button text, character-for-character
}

The four categories use this rubric:
- direct: names the privacy action plainly using the action verb. Example for
  reject: "Reject All", "Decline", "Refuse Cookies".
- near_direct: names the action with mild softening but still unambiguous.
  Example for reject: "No thanks", "Continue without accepting".
- euphemistic: names a related but indirect action; user must infer the
  privacy consequence. Example for reject: "Manage Preferences", "Cookie
  Settings", "Customize" (when this is the only path to reject).
- deceptive: label misrepresents what the button does, OR no usable label.
  Example: "Continue to site" that is actually Accept All.

Important rules:
1. Score per pathway, not per button. The same button may be "direct" for the
   customize pathway but "euphemistic" for the reject pathway.
2. Context disambiguates. The same word "Continue" can be direct or deceptive
   depending on what the banner says.
3. The evidence_quote MUST be the verbatim button text, unchanged.
4. Do not invent text. If the button text is "OK", return "OK", not "OK button".
```

**User message template**:
```
Pathway being assessed: {pathway}
Button text (verbatim): "{button_text}"
Button role: {button_role}
Surrounding banner context: "{surrounding_banner_text}"

Return the JSON.
```

**Output validator**:
1. Parse JSON.
2. Validate against `LabelClarityResult` Pydantic schema.
3. Check `evidence_quote.strip().lower() == button_text.strip().lower()` — if not, retry.
4. Map category → score deterministically.

### 1.6 Few-shot examples (embed in prompt for first 100 sites then drop)

```
Example 1:
  Pathway: reject
  Button text: "Reject All"
  Context: "We use cookies to improve your experience. Accept All or Reject All."
  → {"category": "direct", "rationale": "Names the reject action plainly using the action verb.", "evidence_quote": "Reject All"}

Example 2:
  Pathway: reject
  Button text: "Manage Preferences"
  Context: "We use cookies to give you the best experience. [Accept All] [Manage Preferences]"
  → {"category": "euphemistic", "rationale": "User must open settings and infer reject is available there; does not name the reject action.", "evidence_quote": "Manage Preferences"}

Example 3:
  Pathway: accept
  Button text: "Continue to site"
  Context: "By continuing to browse you accept our use of cookies."
  → {"category": "deceptive", "rationale": "Misrepresents acceptance as merely 'continuing'; user does not realize this is consent.", "evidence_quote": "Continue to site"}

Example 4:
  Pathway: customize
  Button text: "Customize"
  Context: "[Accept All] [Reject All] [Customize]"
  → {"category": "direct", "rationale": "Names the customize action directly when a separate reject is available.", "evidence_quote": "Customize"}

Example 5:
  Pathway: reject
  Button text: "Customize"
  Context: "[Accept All] [Customize]" (no separate Reject)
  → {"category": "euphemistic", "rationale": "The customize panel is the only path to reject; user must infer.", "evidence_quote": "Customize"}
```

### 1.7 Ground truth

**Source**: Bouhoula et al., USENIX Security 2024 — 97k EU sites with LLM-classifier-labeled buttons across Accept / Reject / Save / Settings classes [(repo + dataset link)](https://www.usenix.org/conference/usenixsecurity24/presentation/bouhoula).

**Mapping**: Bouhoula's 4 button classes do not perfectly map to our 4 categories. Adaptation:
- Bouhoula `accept`/`reject`/`save`/`settings` are coarse-grained button-class labels (what the button DOES)
- Our 4 categories are fine-grained label-clarity labels (how CLEARLY the button is named)
- We use Bouhoula's `pathway label` as the input `pathway` field; our LLM produces the clarity category

**Eval procedure**:
1. Sample 1000 buttons from Bouhoula data, stratified by their 4 button classes
2. Two human raters (Alfred + 1) independently label all 1000 with our 4 clarity categories
3. Compute inter-rater κ (target ≥ 0.6)
4. Run our LLM on the same 1000 buttons
5. Compute LLM-vs-human-majority κ (target ≥ 0.5 for v0; ≥ 0.7 for v1)
6. Inspect disagreements (~ 50 sample) qualitatively

### 1.8 Implementation footprint

| Where | What |
|---|---|
| `src/consent_audit/llm/text.py` | `def score_label_clarity(input: LabelClarityInput) -> LabelClarityResult` |
| `src/consent_audit/llm/prompts/label_clarity.py` (new) | System + user template + few-shot block as strings |
| `src/consent_audit/models/audit.py` | Add `LabelClarityInput`, `LabelClarityCategory`, `LabelClarityResult` |
| `tests/llm/test_label_clarity.py` (new) | 10 unit tests on hand-crafted inputs, asserting category + verbatim quote |
| `tests/fixtures/labels/` (new) | JSON fixture files of {input, expected_category} |

Estimated effort: **3-5 days** of focused work.

---

## 2. NLP-2: Layer 3.1a Disclosure Topic Coverage

### 2.1 What it measures
Per [CONCEPTS.md §3.1a](../CONCEPTS.md): does the banner (first layer) explicitly disclose each of four mandatory topic categories, and is the disclosure consistent at second layer?

### 2.2 The four topics

```python
class DisclosureTopic(str, Enum):
    data_types = "data_types"        # cookies, identifiers, behavioral data, location, ...
    purposes = "purposes"            # personalization, advertising, analytics, ...
    third_party_sharing = "third_party_sharing"  # advertisers, partners, brokers
    decision_consequences = "decision_consequences"  # what changes if I accept vs reject
```

### 2.3 Input

```python
class TopicCoverageInput(BaseModel):
    first_layer_text: str          # full banner text
    second_layer_text: str | None  # settings panel text if reachable
    banner_url: HttpUrl            # for logging
```

### 2.4 Output

```python
class TopicCoverageResult(BaseModel):
    topic: DisclosureTopic
    present: bool
    clarity_grade: LetterGrade        # A / B / C / F
    evidence_quote: str | None        # verbatim from first_layer_text (or None if absent)
    consistent_with_layer2: bool | None  # None if second_layer_text is None
    second_layer_evidence_quote: str | None  # verbatim from second_layer_text if applicable
    rationale: str                    # ≤ 80 words
    confidence_low: bool = False
```

The complete output for one site is `dict[DisclosureTopic, TopicCoverageResult]` (4 rows).

### 2.5 Rubric (per CONCEPTS.md §3.1a, anchored)

| Grade | Definition | data_types example | purposes example | third_party example | consequences example |
|---|---|---|---|---|---|
| **A** | Specific, concrete, no weasel words | "We collect your email, browsing history, and device ID." | "We use cookies for advertising (showing ads on Meta and Google) and analytics." | "We share your email with Meta, Google, and Criteo for ad targeting." | "If you reject, we will not show personalized ads but you will still see ads." |
| **B** | Topic clearly named with some vagueness | "We collect personal data and usage data." | "We use cookies for advertising and analytics." | "We share data with advertising partners." | "Rejection may limit some features." |
| **C** | Acknowledged but evasive | "We may collect certain data." | "We use cookies to improve your experience." | "We may share data with selected partners." | "Your choice affects your experience." |
| **F** | Missing or actively misleading | (topic not mentioned) | (only says "essential cookies" while advertising cookies fire) | (only says "we may share" with no third-party named) | (no mention of consequences at all) |

If `present == False` → `clarity_grade == F`.
If `present == True` and `evidence_quote is None` → schema error, retry.

### 2.6 `consistent_with_layer2` semantics

For a topic that is `present == True` at first layer:
- `True`: Settings panel covers the same topic with NO contradiction and equal or greater specificity
- `False`: Settings panel either omits this topic OR contradicts the first-layer claim (e.g., banner says "no advertising cookies" but second layer has an Advertising toggle)
- `None`: Second layer not captured (gate failed in Layer 1)

This field directly supports the paper's "promise-vs-reality" sub-thread without leaving Plan A scope (per SCHEMA §1.4) — the "promise" is the first layer, the "reality" is the second layer + cookie behavior, both already in scope.

### 2.7 Prompt design

**One LLM call per topic** (4 calls per site) — better than a single combined call because:
- Each call has a focused rubric
- Failures are isolated (one bad topic doesn't poison others)
- Budget can be cut mid-site (e.g., skip Layer 2 consistency check if cap nearing)

**System message** (parameterized by topic):
```
You are a privacy interface auditor.

Your job is to assess how clearly a cookie banner discloses ONE specific topic
to users. You are evaluating the topic: "{topic_human_name}".

The topic definition: {topic_definition}

You receive the full banner text (first layer) and, if available, the
settings-panel text (second layer).

You return JSON matching this schema EXACTLY:
{
  "present": true | false,
  "clarity_grade": "A" | "B" | "C" | "F",
  "evidence_quote": verbatim substring of first_layer_text, or null if not present,
  "consistent_with_layer2": true | false | null,
  "second_layer_evidence_quote": verbatim substring of second_layer_text or null,
  "rationale": a sentence under 80 words
}

Clarity grade rubric (for this topic):
- A: {topic_grade_A_definition}
- B: {topic_grade_B_definition}
- C: {topic_grade_C_definition}
- F: topic not mentioned, or mentioned in actively misleading way.

Important rules:
1. evidence_quote MUST be a verbatim substring of the first-layer text. Do
   NOT paraphrase. If you cannot find a verbatim quote, set present=false
   and evidence_quote=null.
2. If first-layer disclosure is present, also check second-layer text. Mark
   consistent_with_layer2 true ONLY if second layer covers the same topic
   with no contradiction.
3. If second_layer_text is null, set consistent_with_layer2 to null.
4. Do not invent disclosures. If the banner is silent on this topic,
   present=false.
```

**User message template**:
```
TOPIC: {topic_human_name}

FIRST-LAYER TEXT:
"""
{first_layer_text}
"""

SECOND-LAYER TEXT:
"""
{second_layer_text_or_NONE}
"""

Return the JSON.
```

### 2.8 Per-topic definitions and rubric anchors (passed to prompt)

```python
TOPIC_SPECS = {
    DisclosureTopic.data_types: {
        "human_name": "Data Types Collected",
        "definition": "What categories of personal data the website collects (e.g., cookies, identifiers, behavioral data, location, IP address, biometric data).",
        "grade_A": "Names specific data types concretely.",
        "grade_B": "Names broad categories without specifics.",
        "grade_C": "Acknowledges 'data' or 'information' without categorization.",
    },
    DisclosureTopic.purposes: {
        "human_name": "Purposes of Data Use",
        "definition": "Why the data is collected — what business purposes it serves (e.g., personalization, advertising, analytics, fraud prevention).",
        "grade_A": "Names specific purposes concretely and exhaustively.",
        "grade_B": "Names broad purpose categories.",
        "grade_C": "Vague 'to improve your experience' without specifics.",
    },
    DisclosureTopic.third_party_sharing: {
        "human_name": "Third-Party Sharing",
        "definition": "With whom the data is shared — specifically third parties outside the site itself (advertisers, partners, affiliates, data brokers).",
        "grade_A": "Names specific third parties (e.g., 'Meta', 'Google', 'Criteo') or links to an exhaustive vendor list.",
        "grade_B": "Names categories of third parties (e.g., 'advertising partners', 'analytics vendors').",
        "grade_C": "Vague 'selected partners' or 'trusted third parties' without specifics.",
    },
    DisclosureTopic.decision_consequences: {
        "human_name": "Decision Consequences",
        "definition": "What changes for the user depending on whether they accept or reject — what features or services are affected by their choice.",
        "grade_A": "Concrete, accurate description of what changes (e.g., 'If you reject, we will not show personalized ads').",
        "grade_B": "Vague description of effects.",
        "grade_C": "Mention of 'effects' or 'impact' without specifics.",
    },
}
```

### 2.9 Ground truth

**Topic 2 (purposes)**: Santos et al., WPES 2021 — labeled ~400 banner texts for purpose-disclosure quality [(paper)](https://arxiv.org/abs/2110.02597). Map their 3-tier label (specific / vague / absent) to our A-F:
- "specific" → A or B (Alfred manually disambiguates 50 samples)
- "vague" → C
- "absent" → F

**Topics 1, 3, 4**: NO existing labeled dataset. Build our own:
- Alfred + 1 second rater independently label 50 sites for each topic
- Stratify the 50 by inferred banner type (long disclosure, short banner, no banner, walled)
- Compute Cohen's κ between raters (target ≥ 0.6)
- Resolve disagreements through discussion; create the gold set
- Total: 50 sites × 3 topics × 2 raters = 300 hand-labels (≈ 6-8 hours)

### 2.10 Evaluation

- Topic 2 against Santos: agreement rate + confusion matrix (A/B/C/F vs specific/vague/absent)
- Topics 1, 3, 4 against the hand-labeled gold set: per-topic accuracy + macro-averaged F1
- Cross-topic Layer-2 consistency: spot-check 30 sites where `consistent_with_layer2 == False` and verify manually

### 2.11 Implementation footprint

| Where | What |
|---|---|
| `src/consent_audit/llm/text.py` | `def score_topic_coverage(input: TopicCoverageInput, topic: DisclosureTopic) -> TopicCoverageResult` |
| `src/consent_audit/llm/prompts/topic_coverage.py` (new) | System template + 4 topic-spec dicts + user template |
| `src/consent_audit/models/audit.py` | Verify `TopicCoverageResult` (already exists per audit.py line 147); ensure `second_layer_evidence_quote` field exists; if missing, add |
| `tests/llm/test_topic_coverage.py` (new) | 16 unit tests (4 topics × 4 grades) on hand-crafted inputs |
| `tests/fixtures/banners/` (new) | JSON fixtures: banner text + ground-truth grade per topic |

Estimated effort: **2 weeks** (1 week prompt + 1 week ground-truth labeling).

---

## 3. NLP-3: Layer 3.1b Communicative Framing

### 3.1 What it measures
Per [CONCEPTS.md §3.1b](../CONCEPTS.md): how factually equivalent information is framed across the consent flow, measured along four mechanisms.

### 3.2 The four mechanisms

```python
class FramingMechanism(str, Enum):
    emphasis_patterns = "emphasis_patterns"
    linguistic_complexity = "linguistic_complexity"
    information_sequencing = "information_sequencing"
    benefit_risk_asymmetry = "benefit_risk_asymmetry"

class BiasLevel(str, Enum):
    neutral = "neutral"
    mild_bias = "mild_bias"
    strong_bias = "strong_bias"
```

### 3.3 Mechanisms are NOT all LLM tasks

| Mechanism | Method | Why |
|---|---|---|
| `linguistic_complexity` | **Deterministic Flesch-Kincaid calculation**, NOT LLM | We compute reading grade for positively-framed text vs negatively-framed text; bias = difference. No LLM judgment needed. |
| `emphasis_patterns` | **VLM** + LLM combined | Visual prominence (font size, color, position) is a vision task; textual emphasis is LLM. Final score combines both. |
| `information_sequencing` | **LLM** | Pure semantic — which idea comes first, which is mentioned, which is buried. |
| `benefit_risk_asymmetry` | **LLM** | Pure semantic — are benefits of acceptance enumerated while costs of acceptance are not, etc. |

This is the most complex of the three tasks. Spelling out each below.

### 3.4 Mechanism 1: `linguistic_complexity` (DETERMINISTIC, no LLM)

**Input**: first-layer text. Two pre-classified spans (output of a small LLM pre-pass — see §3.4.1):
- `positively_framed_span`: text presenting acceptance favorably ("improve your experience", "personalize for you")
- `negatively_framed_span`: text presenting acceptance unfavorably ("share with advertisers", "track your behavior")

**Computation**:
```python
def linguistic_complexity_bias(pos: str, neg: str) -> BiasLevel:
    pos_grade = flesch_kincaid_grade(pos)
    neg_grade = flesch_kincaid_grade(neg)
    delta = neg_grade - pos_grade   # positive delta = negative framing harder to read
    if abs(delta) < 1.0:
        return BiasLevel.neutral
    elif abs(delta) < 3.0:
        return BiasLevel.mild_bias
    else:
        return BiasLevel.strong_bias
```

#### 3.4.1 Span pre-pass

Before the deterministic calculation, an LLM call segments the banner into positively-framed and negatively-framed spans. Prompt:

```
You are tagging a cookie banner's text into spans by sentiment toward
acceptance.

Return JSON:
{
  "positively_framed_spans": [list of verbatim substrings that present
                              acceptance favorably (benefits, comforts,
                              improvements)],
  "negatively_framed_spans": [list of verbatim substrings that present
                              acceptance unfavorably (tracking, sharing,
                              risks)]
}

If no positively-framed text exists, return empty list. Same for negative.
Every span MUST be a verbatim substring of the input.
```

The deterministic computation only runs if both spans are non-empty.

### 3.5 Mechanism 2: `emphasis_patterns` (LLM + VLM combined)

**Visual half** (VLM, scope of vision_design.md not this doc):
- Font size ratio between positively-framed and negatively-framed text
- Color contrast difference
- Position salience

**Textual half** (LLM, this doc):
- Repetition count (how many times is a benefit mentioned vs a cost?)
- Sentence-position salience (lead sentence is positive vs negative?)
- Adjective valence (positive adjectives vs negative adjectives)

LLM call returns:
```python
class EmphasisTextualResult(BaseModel):
    benefit_repetition_count: int
    cost_repetition_count: int
    lead_sentence_valence: Literal["positive", "negative", "neutral"]
    positive_adjective_count: int
    negative_adjective_count: int
    rationale: str
```

Combined bias level (computed in code, not LLM):
```python
def emphasis_bias(visual: VisualEmphasis, textual: EmphasisTextualResult) -> BiasLevel:
    # weight visual 0.5, textual 0.5
    # if visual_ratio > 1.5 AND textual lead_valence == "positive": strong_bias
    # if either alone shows strong asymmetry: mild_bias
    # else: neutral
    ...
```

### 3.6 Mechanism 3: `information_sequencing` (pure LLM)

**Input**: first-layer text + second-layer text.

**LLM task**: identify the order of presentation across these elements:
- Benefits of acceptance
- Risks/costs of acceptance
- Rejection option
- Customization option

Prompt:
```
You are analyzing the SEQUENCE of information in a cookie banner.

Read the first-layer text and identify, in order of appearance, where each
of these is FIRST mentioned (use character offsets or "not present"):

1. Benefits of accepting
2. Risks or costs of accepting
3. The reject option
4. The customize/manage option

Return JSON:
{
  "first_benefit_position": int or "not_present",
  "first_risk_position": int or "not_present",
  "first_reject_mention_position": int or "not_present",
  "first_customize_mention_position": int or "not_present",
  "rationale": one sentence,
  "evidence_quote_benefit": verbatim quote or null,
  "evidence_quote_risk": verbatim quote or null
}
```

Bias scoring (deterministic from these positions):
- Benefits before risks by > 50 chars AND reject mentioned > 100 chars after accept → strong_bias
- Benefits before risks AND reject mentioned later than accept → mild_bias
- Else → neutral

### 3.7 Mechanism 4: `benefit_risk_asymmetry` (pure LLM)

**Input**: first-layer text.

**LLM task**: count benefits-of-acceptance mentioned and costs-of-acceptance mentioned.

Prompt:
```
You are counting how a cookie banner describes acceptance.

Read the first-layer text. List:
1. Each benefit of accepting that is mentioned (e.g., "personalized
   content", "improved experience").
2. Each cost or risk of accepting that is mentioned (e.g., "we will
   share your email with advertisers", "we will track your browsing").

Return JSON:
{
  "benefits_mentioned": [list of verbatim quotes],
  "costs_mentioned": [list of verbatim quotes],
  "rationale": one sentence
}

Each item MUST be a verbatim quote from the text. Do not infer; only
report what is literally stated.
```

Bias scoring (deterministic from the lists):
- benefits ≥ 2 AND costs == 0 → strong_bias
- benefits ≥ 1 AND costs == 0 → mild_bias
- benefits == 0 AND costs ≥ 1 → mild_bias (toward reject — unusual but possible)
- Else → neutral

### 3.8 Aggregation into `FramingResult`

For each mechanism:
```python
class FramingResult(BaseModel):                  # already in models/audit.py
    mechanism: FramingMechanism
    level: BiasLevel
    rationale: str
    evidence_quotes: list[str]
```

CONCEPTS.md §3.1b aggregation rule:
- Any single mechanism at `strong_bias` → drop the overall Transparency letter grade ONE FULL STEP
- Two or more at `mild_bias` → drop ONE STEP
- Else: no drop

### 3.9 Ground truth

**No existing labeled corpus.** This is the hardest part — we must build it.

**Plan**:
1. Sample 60 sites stratified by inferred framing type (rough buckets: very neutral, mildly biased, heavily biased)
2. Alfred + 1 second rater (ideally Qiyao or a CWRU peer) independently label each site for all 4 mechanisms × 3 levels
3. Compute per-mechanism Cohen's κ (target ≥ 0.5 — this is a hard inter-rater task)
4. Resolve disagreements through discussion; create gold set of ≥ 40 sites with full agreement
5. Evaluate LLM against this gold set per mechanism
6. Report: "We achieve κ = X with human raters; LLM agrees with the gold set at Y%."

This is realistic to land in 2-3 weeks if Alfred labels alongside development.

### 3.10 Evaluation

- Per-mechanism agreement with the gold set (60% target for v0)
- Sanity: a site with all 4 mechanisms `neutral` per LLM should pass a human spot check ≥ 80% of the time
- Robustness: re-run on the same 30 sites a week later, check stability (≥ 90% category stability for deterministic mechanisms)

### 3.11 Implementation footprint

| Where | What |
|---|---|
| `src/consent_audit/llm/text.py` | 4 functions: `score_emphasis_textual`, `score_sequencing`, `score_asymmetry`, `tag_framing_spans` |
| `src/consent_audit/llm/prompts/framing.py` (new) | 4 prompt templates |
| `src/consent_audit/layers/layer3_framing.py` (new module) | Deterministic span aggregation + Flesch-Kincaid calc + mechanism-to-overall aggregation |
| `src/consent_audit/models/audit.py` | Verify `FramingResult` (already exists per audit.py line 158); add `EmphasisTextualResult` |
| `tests/llm/test_framing.py` (new) | Per-mechanism unit tests |

Estimated effort: **3 weeks** (1 week prompt design + 1 week ground-truth labeling + 1 week integration).

---

## 4. Cross-Task Implementation Roadmap

### 4.1 Sequence

Recommended order based on dependency and risk:

| Phase | Weeks | Task | Why now |
|---|---|---|---|
| **Phase A** | 1-2 | NLP-1 label_clarity full pipeline | Smallest scope; Bouhoula ground truth ready; validates LLM-wrapper, schema enforcement, evidence-quote check |
| **Phase B** | 3 | Build hand-labeled ground truth for NLP-2 Topics 1, 3, 4 | Blocks NLP-2 evaluation; can be done in parallel with Phase A integration |
| **Phase C** | 4-5 | NLP-2 topic_coverage full pipeline | Builds on Phase A infra |
| **Phase D** | 6-7 | Build hand-labeled ground truth for NLP-3 | Blocks NLP-3 evaluation |
| **Phase E** | 7-9 | NLP-3 framing full pipeline | Most complex; benefits from infra hardened in A+C |
| **Phase F** | 10-11 | Integration into `run_audit.py` end-to-end; first real audits | Brings all three into production |
| **Phase G** | 12-13 | Paper writing + (stretch goal) Plan B policy demo on 5 sites | Plan A done by week 11; Plan B happens here ONLY IF schedule holds |

This fits the 13-week SSRP window (May 18 – Aug 14, 2026) with a buffer in case any phase slips.

### 4.2 Parallel tracks

While NLP work proceeds, the following are independently buildable:
- `capture/agent.py` (Playwright pipeline) — required input to all NLP tasks
- `storage/db.py` and `storage/object_store.py` — required for persistence
- `layers/layer1_path_availability.py` — Layer 1 gate, no NLP dependency
- `diff/engine.py` — Layer 1 + 2 + 3 outputs are inputs; can be built once schemas are stable

### 4.3 What to commit when

Per [AGENTS.md](../AGENTS.md) commit discipline:
- One task at a time, complete and tested before next.
- Each phase ends with a working end-to-end demo on 3 canary sites.
- Tests required for each new module before merging.

---

## 5. Cost Model (Rough)

Per-site cost estimate at current Anthropic pricing (2026-Q2):

| Call | Input tokens | Output tokens | Cost ~$ |
|---|---|---|---|
| NLP-1 × 4 pathways | 4 × 200 in | 4 × 80 out | $0.012 |
| NLP-2 × 4 topics | 4 × 800 in | 4 × 200 out | $0.040 |
| NLP-3 emphasis_textual | 600 in | 200 out | $0.008 |
| NLP-3 sequencing | 600 in | 150 out | $0.007 |
| NLP-3 asymmetry | 600 in | 150 out | $0.007 |
| NLP-3 span_tagging | 600 in | 100 out | $0.006 |
| **Per-site NLP total** | | | **~$0.08** |

For 500 sites × 52 weeks = 26,000 audits × $0.08 = **~$2,080 in NLP budget alone**.

Plus VLM costs (separate doc) and infrastructure → fits within $4,000 SSRP budget with margin.

Per-call budget cap enforced in `llm/budget.py`.

---

## 6. Open Questions for Alfred to Decide Before Implementation Starts

These do NOT block this draft, but block writing actual code:

1. **Model lock-in** — claude-opus-4-7 for LLM, claude-sonnet-4-6 for VLM, ok? Or benchmark 3 options first (SCHEMA §10 Decision 5)?
2. **Topic 2 ground truth source** — use Santos 2021 directly, or re-label to align with our A/B/C/F scheme? (If using directly, A/B distinction is muddier.)
3. **Second rater for hand-labels** — Qiyao? a CWRU peer? a paid undergraduate? IRB needed for paid?
4. **Plan B stretch goal** — at week 11, who decides if Plan A is "done enough" to spend weeks 12-13 on the policy demo? Suggest: a checklist with hard thresholds (e.g., "if all 3 NLP κ ≥ 0.5 AND end-to-end runs on 100 sites in < 6 hours, proceed to Plan B").
5. **Caching / idempotency** — should LLM outputs be cached by (input_hash, model_version)? Saves cost on re-runs but complicates reproducibility claims.

---

## 7. Boundary Statement

This document designs THREE NLP tasks for FIRST-LAYER and SECOND-LAYER text only. Anything labeled "policy text" (the long privacy policy long-form document) is **out of scope** per [SCHEMA.md §1.4](../SCHEMA.md). The narrow Plan-B stretch goal (3-5 testable claim extractions from policy on a handful of sites) is a SEPARATE pipeline that may be designed in a follow-up doc IF schedule allows at week 11.
