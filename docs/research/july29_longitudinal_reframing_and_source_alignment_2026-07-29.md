# Longitudinal Reframing and CWRU SOURCE Alignment, 2026-07-29

## Decision

The project's main contribution is a longitudinal comparison framework for
consent interfaces, now evaluated through a controlled local pilot and a
primary-source retrospective case series. The two proposal questions are
necessary subproblems, not the final destination:

1. RQ1 defines a repeatable measure of pathway availability, pathway effort,
   transparency, and unbiased choice.
2. RQ2 applies that measure to repeated versions of the same interface.
3. Matched, validated deltas are then classified as improved, regressed, mixed,
   stable, or insufficient evidence.

The presentation and poster should lead with this logic. Capture counts,
software architecture, and static evidence cards support it; they are not the
headline.

## What The Current Evidence Supports

- The package contains 42 audit reports and 20 longitudinal summaries.
- Those are processing-output counts, not independent long-term observations.
  They include same-day repeats, non-target sites, and automated comparisons.
- The current five have one matched weekly interval: May 29 to June 5, 2026.
- The June 14 Week 3 attempt produced 0/5 valid observations and cannot extend
  the timeline.
- A June 15 Coca-Cola post-fix smoke is valid technical evidence but was run
  with `--no-save` and is not part of the main longitudinal package.
- The latest five automated summaries flag two `D` and three `C` cases. These
  letters encode review priority from detected event types, not direction.

Manual side-by-side review of the stored first-screen screenshots gives a more
conservative result:

| Case | What is visible at both time points | Defensible directional result |
|---|---|---|
| The Guardian | A consent-choice screen with accept, reject-like, and manage controls | Insufficient evidence; the screens look structurally stable while automated path results conflict |
| Coca-Cola | A privacy preference center with Allow All, Confirm My Choices, Reject All, and toggles | Insufficient evidence; the screens look structurally stable and a later detector fix changed recognition |
| CNN | No visible first-screen banner | No banner-quality trajectory can be scored |
| Booking.com | No visible first-screen banner | No banner-quality trajectory can be scored |
| NerdWallet | No visible first-screen banner | No banner-quality trajectory can be scored |

Therefore the controlled local pilot does **not** show that one of its five
sampled websites improved or regressed. It shows that the workflow can retain
matched evidence and surface candidate changes, and that automated deltas must
be separated from validated substantive change.

That local limit is no longer the whole project result. A separate retrospective
case series adds six source-complete trajectories documented by CNIL,
Legifrance, and one direct Google announcement:

| Retrospective case | Dated directional result |
|---|---|
| Google Search and YouTube | Improved: reject effort fell from at least five actions to one, with equal first-screen accept/reject buttons |
| Facebook | Improved: CNIL verified that refusal became as simple as acceptance after a formal order |
| TikTok | Improved but incomplete: at least three reject actions became a first-layer reject button, while information remained deficient |
| Orange | Improved: post-withdrawal cookie reads/writes on `orange.fr` stopped after an injunction |
| Vanity Fair France | Regressed: later checks found pre-consent cookies and ineffective reject/withdrawal after an earlier proceeding had closed |
| SHEIN | Improved: CNIL recorded ineffective refusal and withdrawal in August 2023 and later recorded remediation during the proceedings |

Across these purposively selected cases, `5/6` improved in at least one audited
component and `1/6` regressed. All `3/3` first-layer button cases moved from an
acceptance-favoring effort asymmetry to one-click or equivalently simple
refusal. These are case-series fractions, not population estimates.

The complete evidence and causal audit is in
`july29_retrospective_longitudinal_evidence_rescue_2026-07-29.md`.

## Directional Outcome Rule

Use the component dimensions, not raw hashes or severity letters:

| Label | Rule for one validated interval |
|---|---|
| Improved | One or more audited dimensions improve and none regress |
| Regressed | One or more audited dimensions regress and none improve |
| Mixed | At least one dimension improves and another regresses |
| Stable | No meaningful component changes under the fixed rubric |
| Insufficient evidence | Context is unmatched, evidence is missing, capture failed, scorer changed without back-coding, or evidence conflicts |

Path availability improves when Reject or Customize becomes reachable under the
same rule. Path effort improves when required effort decreases. Transparency
and unbiased choice improve when their grades rise under the same rubric. Copy,
layout, DOM, and image-hash changes are review triggers only.

## Research-Depth Audit

The conceptual depth is now sufficient for a pilot-method poster, but not for a
claim about long-term evolution. The missing pieces are specific:

| Gap | Why it matters | Resolution |
|---|---|---|
| Too few validated local time points | One interval detects difference; it does not establish a local evolution pattern | Keep the local pilot as method validation; add source-complete retrospective cases now and collect at least three future controlled points per local case |
| Context controls not stored as analysis fields | Geography, language, viewport, browser state, and prior consent can change what appears | Freeze and report a capture-context profile for every matched run |
| Scorer-version confound | The Coca-Cola detector fix can mimic website improvement | Store scorer/rubric version and back-code earlier captures before comparison |
| Raw technical diff lacks direction | Hash changes say that something changed, not whether user choice improved | Apply the directional component rubric after manual evidence review |
| Reliability not measured | A single coder may interpret pathways or grades inconsistently | Double-code a subset and report agreement or disagreements |
| Small, selective evidence sets | Neither five local sites nor six purposive historical cases can support a prevalence estimate | Use the 2026 11,364-site historical study as the external trend benchmark and present this project's six cases as mechanism-focused evidence |
| Policy scope is ambiguous | Long-form privacy policies require a different unit and rubric | Keep the core unit as first/second-layer consent UI; treat linked notice text as context, not a full policy audit |

The repository records the current local five in
`data/longitudinal_directional_review_2026-07-29.csv` and the source-complete
historical six in `data/retrospective_longitudinal_cases_2026-07-29.csv`.
Historical evidence is admitted only when a dated primary source supplies the
missing observation; it is never inferred from an absent screenshot.

## CWRU SOURCE / Intersections Requirements Used

Official CWRU guidance supports an in-progress research presentation and asks
for a clear poster path rather than a software inventory:

- Intersections accepts research from initial exploration through final
  findings, so the current pilot can be presented honestly as work in progress.
- Official preparation guidance lists title, presenters/contributors, logos,
  introduction/abstract, methods, results, conclusions, and references as core
  poster content.
- The recommended poster flow is center-to-top-to-bottom vertically and
  left-to-right horizontally.
- The official presentation-skills resource recommends roughly 30% text, 40%
  graphics, and 30% open space; title around 60 pt, headings around 30 pt, body
  around 24 pt, with sans-serif type.
- For slides, the same resource recommends assertion-style statements, large
  clear figures, visible citations, slide numbers, at least 18 pt type, and
  sparse copy.
- Official board options are 32 x 40 inches or 40 x 60 inches. The current
  48 x 36 landscape poster fits a 40 x 60 board but not a 32 x 40 board; the
  registered board size must be confirmed before printing.
- Summer 2026 Intersections is Thursday, July 30, 2026 from 10:00 a.m. to
  12:00 p.m. Registration closed July 12 and PI approval was due July 15. The
  repository does not establish whether this project registered or received a
  poster number.
- The official SSRP page requires presentation at Summer 2026, Fall 2026, or
  Spring 2027 Intersections and a final paper by August 31, 2026.

Official sources:

- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium
- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium/preparing-intersections
- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium/poster-judging-intersections
- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium/registration-and-information
- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium/registration-and-information/intersections-faqs
- https://case.edu/studentlife/ugresearch/programs-and-funding/ssrp
- https://case.edu/studentlife/ugresearch/sites/default/files/2022-12/SOURCE_%20Improving%20Presentation%20Skills.pptx%20%281%29.pdf

The Fall 2024 winning posters linked from CWRU were used as organization
references. Their common strength is explicit sectioning and a visible
goal-method-result-conclusion path. They are not copied as visual templates.

## Revised Poster Story

Use a left-to-right sequence:

1. **Question:** A snapshot can describe one interface, but cannot show how it
   evolves.
2. **Measurement:** RQ1 fixes the comparison dimensions.
3. **Longitudinal design:** RQ2 repeats the same capture under controlled
   conditions.
4. **Interpretation:** validated deltas become improved, regressed, mixed,
   stable, or insufficient.
5. **Longitudinal result:** six primary-source historical trajectories yield
   five component improvements and one functional regression.
6. **Interpretation:** regulation repeatedly changes visible reject effort, but
   purpose disclosure and technical respect for refusal can remain deficient or
   later regress.
7. **Contribution and next study:** a traceable framework, a supported
   mechanism-focused result, and a concrete plan for future controlled points.

The two paired Guardian and Coca-Cola examples should replace isolated static
screenshots. The three no-visible-banner cases belong in one compact context
band, not three large result cards.

## Revised Twelve-Slide Story

1. Tracking How Consent Interfaces Evolve.
2. A single snapshot cannot reveal design evolution.
3. Two evidence lanes answer feasibility and historical change.
4. RQ1 is the ruler; RQ2 creates the timeline.
5. A 2026 study shows the broad reject-button trend from 2018 to 2024.
6. Six primary-source cases meet the retrospective inclusion rule.
7. Google reduced reject effort from at least five actions to one.
8. Facebook and TikTok also moved refusal toward first-layer parity.
9. Orange and SHEIN improved technical refusal/withdrawal while Vanity Fair
   later regressed.
10. Change reasons have different evidentiary strength.
11. Main finding: visible parity improves first, but autonomy can remain
    incomplete and reversible.
12. Discussion and next study: continuous auditing, publisher/CMP
    responsibility, and controlled future capture.

## Final Answer To The Project

The project answers **how** to build a longitudinal comparison: use RQ1's
multidimensional audit as a stable ruler, use RQ2 to preserve matched versions,
validate each technical change against evidence, and classify component
deltas. It now also identifies documented directional cases: Google, Facebook,
TikTok, Orange, and SHEIN improved at least one user-choice component, while
Vanity Fair later regressed in functional respect for refusal.

The deeper conclusion is that consent evolution is component-specific and
reversible. Regulatory pressure repeatedly produces a concrete reject or
withdrawal improvement, but a balanced button does not guarantee clear
information or backend respect for the choice. The controlled local pilot still
needs additional time points; its limitation no longer erases the supported
historical finding.
