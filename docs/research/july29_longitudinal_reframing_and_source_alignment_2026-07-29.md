# Longitudinal Reframing and CWRU SOURCE Alignment, 2026-07-29

## Decision

The project's main contribution is a longitudinal comparison framework for
consent interfaces. The two proposal questions are necessary subproblems, not
the final destination:

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

Therefore the current study does **not** show that a sampled website improved
or regressed. It shows that the workflow can retain matched evidence and surface
candidate changes, and that automated deltas must be separated from validated
substantive change.

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
| Too few validated time points | One interval detects difference; it does not establish an evolution pattern | Collect at least three validated points per case; continue weekly or biweekly if the study continues |
| Context controls not stored as analysis fields | Geography, language, viewport, browser state, and prior consent can change what appears | Freeze and report a capture-context profile for every matched run |
| Scorer-version confound | The Coca-Cola detector fix can mimic website improvement | Store scorer/rubric version and back-code earlier captures before comparison |
| Raw technical diff lacks direction | Hash changes say that something changed, not whether user choice improved | Apply the directional component rubric after manual evidence review |
| Reliability not measured | A single coder may interpret pathways or grades inconsistently | Double-code a subset and report agreement or disagreements |
| Small, selective pilot | Five sites cannot support population claims | Present cases as method validation; predefine a larger sampling frame for future work |
| Policy scope is ambiguous | Long-form privacy policies require a different unit and rubric | Keep the core unit as first/second-layer consent UI; treat linked notice text as context, not a full policy audit |

The repository now records the current five in
`data/longitudinal_directional_review_2026-07-29.csv`. No missing historical
observation can be reconstructed without new evidence, so the honest remedy is
future controlled capture rather than invented results.

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

Official sources:

- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium
- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium/preparing-intersections
- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium/poster-judging-intersections
- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium/registration-and-information
- https://case.edu/studentlife/ugresearch/share-your-work/intersections-poster-symposium/registration-and-information/intersections-faqs
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
5. **Pilot result:** five sites, one matched interval; automated candidates were
   produced, but no directional evolution claim survives current validation.
6. **Contribution and next study:** a traceable framework plus a concrete plan
   for additional controlled time points and same-version rescoring.

The two paired Guardian and Coca-Cola examples should replace isolated static
screenshots. The three no-visible-banner cases belong in one compact context
band, not three large result cards.

## Revised Ten-Slide Story

1. Tracking How Consent Interfaces Evolve.
2. A single snapshot cannot reveal design evolution.
3. RQ1 is the ruler; RQ2 creates the timeline.
4. Improvement and regression require component-level rules.
5. Valid comparison requires matched capture context and scorer version.
6. The pilot contains five sites and one matched weekly interval.
7. Guardian shows why raw change alerts need evidence review.
8. Coca-Cola shows why scorer changes must be back-coded.
9. Current result: method feasibility, no directional evolution finding yet.
10. Next study: controlled repeated captures, validation, and trajectory coding.

## Final Answer To The Project

The project can already answer **how** to build a longitudinal comparison: use
RQ1's multidimensional audit as a stable ruler, use RQ2 to preserve matched
versions, validate each technical change against evidence, and classify the
component deltas. It cannot yet answer **which sampled sites improved over the
long term**, because the validated timeline has only one interval and contains
measurement conflicts. That distinction is the central conclusion, not a
failure of the project.
