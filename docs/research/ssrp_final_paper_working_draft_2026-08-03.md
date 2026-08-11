# How Cookie Consent Interfaces Changed

## A Traceable Longitudinal Audit With a Controlled Pilot and Six Dated Cases

**Working draft, August 3, 2026.** This is a source-linked writing starter,
not a submission-ready manuscript. Replace the reference keys with the final
required citation style only after the claim/source audit.

## Abstract

Cookie-consent interfaces change in response to technical, organizational, and
regulatory conditions, yet a static screenshot cannot show whether user choice
improves or regresses. This project develops a traceable longitudinal audit
framework that combines a component rubric for path availability, path effort,
transparency, and choice effectiveness with dated capture and versioning. A
controlled five-site pilot evaluates the workflow but provides only one usable
matched interval, so its directional labels remain insufficient. A separate
purposively selected case series uses primary regulatory decisions, follow-up
records, and one company announcement to reconstruct six company trajectories.
Five cases improve at least one audited component and one later regresses.
Across three first-layer cases, rejection moves from acceptance-favoring effort
asymmetry to one-click or equivalently simple refusal. Orange and SHEIN also
show technical remediation of refusal or withdrawal, while Vanity Fair shows
that functional compliance can later fail. The evidence suggests that concrete
interactions that regulators can specify and verify improve first, but visible
parity does not guarantee informed or technically effective consent. The study
therefore argues for component-level, recurring consent-interface audits.

## 1. Introduction

Cookie-consent assessment is often based on one visible state: a banner, a
button, or a screenshot. That view misses the full decision path and cannot
show whether the same interface changes over time. Prior work has already
measured consent interfaces, tracking behavior, and broad historical trends at
scale. The contribution here is narrower: a traceable bridge between a
component-level consent rubric, controlled local capture, and dated
company-level historical cases. [B1]

The project asks two linked questions. RQ1 develops a computational audit and
scoring system for layered consent interfaces and unbiased choice across the
full consent pathway. RQ2 captures and versions firms' privacy interfaces to
systematically document change. RQ1 is the stable ruler; RQ2 creates the
timeline on which a directional claim can be assessed. [G1]

This distinction matters because a change in visible wording or a button label
does not necessarily change the user's practical ability to refuse. A first
layer can become visually balanced while purpose information stays unclear, or
refusal can appear available while tracking continues. The paper therefore
separates observed direction from the evidence available for explaining that
direction.

## 2. Research Questions And Claim Boundary

**RQ1.** How can we develop a computational audit and scoring system to
quantify layered consent interfaces in terms of unbiased choice across the full
consent pathway?

**RQ2.** How can we automatically capture and version firms' privacy
interfaces to systematically document interface changes over time?

The study does not report an experiment, a legal compliance verdict, or an
internet-wide improvement rate. Its local pilot establishes that the capture
and scoring workflow can preserve a comparable interval. Its retrospective
series establishes that the same component rubric can recover documented,
dated direction in a purposively selected set of cases. [G1; R1]

## 3. Method

### 3.1 Component Rubric

Each consent state is read through four user-facing dimensions:

1. **Path availability:** can a user reach acceptance, rejection, and settings?
2. **Path effort:** how much interaction does each route require?
3. **Transparency:** are purposes and consequences disclosed clearly?
4. **Choice effectiveness:** does the selected choice actually govern the
   relevant behavior, including refusal and withdrawal?

For a dated comparison, a case is labeled improved when one or more assessed
components improve and none regress; regressed when one or more components
regress and none improve; mixed when direction differs across components; and
insufficient when the states or evidence are not comparable. [G1; C1]

### 3.2 Two Evidence Lanes

The controlled local pilot contains five sites and one validated May 29-June 5
interval. Its five directional labels are all `insufficient_evidence`, because
one interval is insufficient to support a defensible local trajectory claim.
The pilot is therefore evidence for the capture-and-comparison method, not a
claim that the sampled websites improved or regressed. [L1]

The retrospective series includes a named company and surface, two dated states
in the same jurisdiction, primary evidence for the earlier and later state,
enough detail to score at least one component, and an explicit separation
between direction and cause. It contains six source-complete cases supported by
12 registered sources. [R1; S01-S12]

### 3.3 Evidence Strength

Direction and explanation are not equivalent. Direction is strong when a
regulator records both states or verifies remediation, and moderate when one
side relies on a company announcement or a broader regulator-recorded state
transition. Reasons are then graded separately as direct company attribution,
verified order response, change during investigation or proceedings, or
unknown. This prevents temporal proximity from being presented as universal
causation. [R1; S01-S12]

## 4. Results

### 4.1 Controlled Pilot

The pilot produced 42 audit reports and 20 longitudinal summaries across the
checked-in package. Its five current matched-site direction labels remain
`insufficient_evidence`. This is a deliberate conservative result: the project
does not convert missing time points, same-day repeats, or infrastructure
metadata into substantive interface evolution. [L1; G1]

### 4.2 Retrospective Case Series

| Company | Earlier state | Later state | Component result | Direction evidence | Explanation evidence |
|---|---|---|---|---|---|
| Google | Reject required at least five actions while acceptance took one | Equal first-screen reject and accept actions | Availability and effort improved | Moderate split-source | Direct company attribution |
| Facebook | No refusal mechanism of equivalent simplicity | Equivalent refusal and regulator-verified closure | Availability, effort, and effectiveness improved | Strong | Verified order response |
| TikTok | Reject required at least three actions | First-layer `Tout refuser` added | Availability and effort improved; purpose information stayed deficient | Strong | Investigation-period change |
| Orange | Cookies continued to be read after withdrawal | First-party cookies removed and new third-party requests stopped | Withdrawal effectiveness improved | Strong | Verified order response |
| Vanity Fair France | Earlier proceeding closed | Later checks found pre-choice cookies and continued behavior after refusal or withdrawal | Refusal effectiveness regressed; transparency not assessed | Moderate state transition | Unknown |
| SHEIN | Cookies before choice and continued reads/writes after refusal or withdrawal | Refusal and withdrawal remediated during proceedings | Technical refusal/withdrawal effectiveness improved | Strong | Proceedings-period change |

Across the six purposively selected cases, `5/6` improved at least one audited
component and `1/6` regressed. All three first-layer button cases moved from
acceptance-favoring effort asymmetry to a one-click or equivalently simple
refusal route. These are case-series fractions, not prevalence estimates.
[R1; S01-S12]

## 5. Discussion

The results support a bounded discussion claim: consent interactions appear to
improve most clearly where a regulator can name a concrete behavior and verify
the remedy. In the cases here, this includes equal first-layer refusal and
effective withdrawal. The strongest explanation evidence is not evenly shared:
Google directly attributed its redesign to regulatory guidance, Facebook and
Orange had order-and-follow-up records, TikTok and SHEIN changed during
regulatory activity, and Vanity Fair's later regression has no established
cause. [R1; S01-S12]

The cases also show why visible parity is insufficient. TikTok improved refusal
effort while purpose information remained deficient. Orange and SHEIN concern
whether refusal or withdrawal actually changed technical behavior. Vanity Fair
shows that a case can later fail after a prior proceeding closed. The practical
implication is that consent auditing should remain component-specific and
recurring rather than treating one compliant-looking banner as a durable final
state. [R1]

## 6. Limitations

The local pilot has one validated interval and is not used to infer direction.
The historical cases are purposively selected and use mixed primary-source
types, so their fractions cannot estimate the prevalence of improvement across
the web. Some later states are regulator-verified while others rely in part on
a company announcement or a process-period record. The study also does not
establish that regulation alone caused every observed change. [R1]

## 7. Conclusion

RQ1 supplies a repeatable component measure and RQ2 supplies the timeline
needed to interpret change. The controlled pilot validates a conservative
capture workflow but remains directionally insufficient. The separate six-case
series shows that the rubric can recover dated, source-linked interface
evolution: five cases improve at least one component and one regresses. The
appropriate conclusion is not that consent interfaces universally improved; it
is that concrete, verifiable user interactions are the clearest site of
documented improvement, while information quality and technical respect for
refusal remain incomplete and reversible.

## Reference-Key Map For Final Formatting

- **[G1]** `docs/research/current_project_goal_2026-07-02.md`
- **[C1]** `CONCEPTS.md`
- **[L1]** `data/longitudinal_directional_review_2026-07-29.csv`
- **[R1]** `docs/research/july29_retrospective_longitudinal_evidence_rescue_2026-07-29.md`
- **[S01-S12]** `data/retrospective_source_registry_2026-07-29.csv`
- **[B1]** `docs/related_work/background_with_citations.md`

Before submission, replace these keys with the citation style requested by the
Undergraduate Research Office or mentor and run the final claim/source audit in
`ssrp_final_paper_completion_plan_2026-07-30.md`.
