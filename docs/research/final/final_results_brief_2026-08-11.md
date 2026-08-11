# Final Results Brief

## Project Result

The project answers the proposal's two research questions with one measurement
framework and two deliberately separate evidence lanes.

### RQ1: How can a computational audit quantify layered consent interfaces?

The answer is a traceable component rubric rather than a single privacy score.
It evaluates:

1. path availability: whether Reject and Customize are reachable;
2. path effort: how many actions and how much interaction each route requires;
3. transparency: whether purposes and consequences are communicated clearly;
4. choice effectiveness: whether rejection or withdrawal changes the relevant
   cookie behavior.

Every score must resolve to a DOM element, screenshot region, action trace, or
verbatim text span. Detection remains separate from deterministic judgment.
A longitudinal direction is assigned only when dated states are comparable.

The controlled five-site pilot validates this workflow. The checked-in package
contains 42 audit-report rows, 20 longitudinal-summary rows, and 365 capture
PNGs. However, only one matched May 29-June 5 interval is reliable, and all
five local direction labels remain `insufficient_evidence`. That is a method
result, not evidence that the sites improved or regressed.

### RQ2: How can consent interfaces be captured and versioned over time?

The answer is to preserve dated states, score the same components at each
state, and grade direction separately from causal evidence. The local pilot
demonstrates the controlled capture path. A separate purposive case series
recovers longer trajectories from eight direct primary sources within a
twelve-source registry.

Across six companies:

- five improved at least one audited component;
- one, Vanity Fair, functionally regressed;
- all three first-layer cases reduced acceptance-favoring rejection effort;
- Google has direct company attribution;
- Facebook and Orange have regulator-verified order responses;
- TikTok and SHEIN changed during regulatory activity without proof that it was
  the sole cause;
- Vanity Fair's regression cause remains unknown.

## Final Interpretation

Concrete interactions that regulators can specify and verify are the clearest
site of documented improvement. First-layer refusal can become easier and a
technical withdrawal mechanism can become effective, while information quality
or other parts of the consent system remain incomplete. A later functional
failure can also follow an earlier closed proceeding.

The result is observational. It is not a randomized experiment, a legal
compliance verdict, or an estimate of how frequently all websites improve.
The selected-case fraction `5/6` must never be presented as a population rate.

## Productive Contribution

The project's durable contribution is a reusable audit protocol:

`capture -> preserve context -> score components -> compare dated states -> validate evidence -> grade direction -> grade explanation`

This protocol turns screenshots and source documents into reviewable evidence
without treating a visual difference as a substantive conclusion by itself.

## Evidence Entry Points

- `CONCEPTS.md`: canonical component and direction definitions.
- `data/final_claim_evidence_matrix_2026-08-11.csv`: claim-level evidence chain.
- `data/retrospective_longitudinal_cases_2026-07-29.csv`: six coded cases.
- `data/retrospective_source_registry_2026-07-29.csv`: twelve-source registry.
- `docs/research/final/evidence/source_cards_2026-08-11/`: offline source locator cards.
- `docs/research/final/evidence_chain_audit_2026-08-11.md`: final verification and limitations.

