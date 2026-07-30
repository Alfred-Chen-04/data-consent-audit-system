# SSRP Final Paper Completion Plan, 2026-07-30

## Paper Claim

This paper presents a traceable method for comparing layered cookie-consent
interfaces over time and an observational six-company case series showing five
component improvements and one functional regression. It does not present a
randomized experiment or an internet-wide improvement rate.

## Draft Abstract

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

## Section And Source Map

| Section | Required content | Checked-in source |
|---|---|---|
| 1. Introduction | Static snapshots miss evolution; RQ1 and RQ2 work together | `docs/research/current_project_goal_2026-07-02.md` |
| 2. Related work | Notice-and-Choice, banner audits, longitudinal banner history | `docs/related_work/background_with_citations.md` |
| 3. Method | Four component dimensions, evidence rule, direction taxonomy | `CONCEPTS.md`; `docs/research/july29_longitudinal_reframing_and_source_alignment_2026-07-29.md` |
| 4. Controlled pilot | Five sites, one validated interval, all direction insufficient | `data/longitudinal_directional_review_2026-07-29.csv` |
| 5. Retrospective cases | Six trajectories and source-level limitations | `data/retrospective_longitudinal_cases_2026-07-29.csv`; source registry |
| 6. Results | `5/6` improved, `1/6` regressed, `3/3` first-layer parity | evidence-rescue analysis |
| 7. Discussion | Concrete interactions improve first; partial and reversible change | evidence-rescue analysis; poster discussion prompts |
| 8. Limitations | Purposive sample, mixed source types, geography, no prevalence or randomized causation | evidence sufficiency audit and claim boundaries |
| 9. Conclusion | RQ1 ruler plus RQ2 timeline supports recurring component audits | current project goal and July 30 presentation |

## Figures And Tables

1. Figure 1: RQ1 ruler plus RQ2 timeline, adapted from presentation slide 4.
2. Table 1: local five-site directional review, all `insufficient_evidence`.
3. Table 2: six retrospective trajectories with direction and causal evidence
   level.
4. Figure 2: broad 2018-2024 accept/reject trend from Dimova et al.; cite the
   preprint and retain its archive-limit caveat.
5. Figure 3: evidence-strength ladder: direct attribution, order follow-up,
   proceedings-period change, unknown cause.

## Writing Schedule

| Date | Output | Exit condition |
|---|---|---|
| August 15-18 | Introduction, related work, method | Every nontrivial claim has a source placeholder |
| August 19-22 | Pilot, case series, results | Counts reproduce from the two CSVs |
| August 23-25 | Discussion, limitations, conclusion | No experiment, prevalence, or universal-cause language |
| August 26-28 | Figures, references, formatting | Tables and figure captions resolve to checked-in evidence |
| August 29-30 | Claim/source audit and mentor corrections | Zero unsupported factual claims |
| August 31 | Final submission | Submission evidence retained separately |

## Final Claim Audit

- Every company result resolves to one or more registered source IDs.
- Direction and reason evidence are stated separately.
- `5/6` is always labeled as a purposive case-series fraction.
- The local five are never combined with the historical six as one sample.
- The paper does not claim that a visible reject button proves technical
  effectiveness.
- Tests, hashes, and render checks are described as artifact QA, not research
  validity.
