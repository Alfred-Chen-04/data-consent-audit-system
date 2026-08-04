# SSRP Presentation Readiness, 2026-08-04

## Current Fact-Based State

The machine-checked rehearsal deck is
`docs/research/presentation/ssrp_consent_longitudinal_presentation_rehearsal_ready_2026-08-04.pptx`.
It preserves the July 30 audience-facing slides and adds a talk track,
transition cue, and `[Sources]` block to the speaker notes on every slide.

No presentation date, event format, registration, attendance, or completed
human rehearsal is asserted here. The Summer 2026 Intersections event has
already passed, and the repository does not contain attendance evidence. The
official SSRP page says recipients may present at Summer 2026, Fall 2026, or
Spring 2027 Intersections and must submit a final paper by August 31, 2026.
The next external fact to obtain is therefore the URO's confirmation of the
available Fall/Spring route, unless a real Summer record is found.

## One-Line Throughline

This is not a claim that cookie consent steadily improves: six purposively
selected, source-complete trajectories show that concrete, regulator-verifiable
choice mechanisms improved most clearly, while information and backend
behavior could remain weak or regress.

## Core Claims To Keep Exact

- The local controlled pilot has five sites and one validated interval per
  site; all five local direction labels remain `insufficient_evidence`.
- The retrospective observational case series contains six selected,
  source-complete company trajectories and 12 registered sources.
- Five of six cases improve at least one audited component; one of six
  functionally regresses.
- All three first-layer cases improve rejection parity or effort.
- Google has direct company attribution; Facebook and Orange have
  regulator-verified order-response evidence; TikTok and SHEIN changed during
  investigation or proceedings; Vanity Fair's reason is unknown.
- These are component-level directional findings, not a prevalence estimate,
  legal verdict, experiment, or universal causal estimate.

## Practice Formats

### Full Deck: Initial 6:15 Run

This is an internal initial target, not a claimed event requirement. Use the
speaker notes in the rehearsal-ready deck; do not read the slide text line by
line.

| Slide | Target | Purpose | Transition to say aloud |
|---|---:|---|---|
| 1 | 0:20 | Frame the tension and result | “First, the two questions that organize the project.” |
| 2 | 0:35 | State RQ1/RQ2 and the bounded answer | “That boundary comes from separating the evidence into two lanes.” |
| 3 | 0:35 | Separate method pilot from historical result | “To make that separation operational, direction is coded component by component.” |
| 4 | 0:35 | Explain the component ruler | “Before the cases, the broader history shows why this matters.” |
| 5 | 0:30 | Give benchmark context without borrowing its causality | “The case series supplies the company-level direction and evidence grades.” |
| 6 | 0:45 | Land the 5 improved / 1 regressed result | “Google is the clearest direct-attribution example.” |
| 7 | 0:35 | Explain Google’s direct attribution | “The next two cases show why parity is necessary but not sufficient.” |
| 8 | 0:35 | Explain parity plus incomplete information | “The last set moves below the button layer to technical effect and reversibility.” |
| 9 | 0:35 | Explain technical remediation and regression | “That uncertainty is what the conclusion must preserve.” |
| 10 | 0:35 | Close with continuous component audit | Stop; invite the discussion questions already on the slide. |

### 90-Second Poster Version

This project asks how the same cookie-consent interface changes over time. RQ1
defines a stable ruler: whether Reject or Customize is reachable, how much
effort each path requires, whether the information is clear, and whether
refusal actually stops tracking. RQ2 uses that ruler to compare dated versions.

The local five-site pilot validates the capture and comparison workflow, but it
has only one usable interval, so it does not support a local improvement claim.
The longitudinal result therefore comes from six purposively selected company
trajectories with dated primary evidence. Five improve at least one component
and one later regresses. Google, Facebook, and TikTok make rejection easier;
Orange and SHEIN improve the technical effect of refusal; Vanity Fair shows
that a later functional failure can occur after an earlier proceeding closed.

The takeaway is not that consent steadily improves. Concrete interactions that
regulators can specify and verify improve most clearly, but a balanced-looking
button can coexist with weak information or backend tracking. That is why the
project argues for continuous, component-level audit rather than one-time
certification.

### 25-Second Opening

I study whether cookie-consent interfaces become easier or harder to refuse
over time. Using dated primary evidence for six companies, I find five
component-level improvements and one functional regression. The pattern is
that concrete, checkable refusal mechanisms improve most clearly, but those
gains can be incomplete and reversible.

## Question Bank

| Question | Safe answer |
|---|---|
| Is this an experiment? | No. It is a controlled method pilot plus a purposively selected observational case series. The sources support dated direction, not randomized causation. |
| Why are there only six companies? | Each case had to have a named surface, two dated states, primary before/after evidence, and enough detail to code an RQ1 component. The case series explains mechanisms; it does not estimate prevalence. |
| Did regulation cause every change? | No. Cause is graded separately. Google directly attributed its redesign; Facebook and Orange have order-and-follow-up evidence; TikTok and SHEIN changed during proceedings; Vanity Fair's cause is unknown. |
| Why retain the weak local pilot? | It validates the capture, versioning, and component-scoring workflow, and it visibly demonstrates why a short interval must not be exaggerated into a trend. |
| Does a Reject all button prove consent works? | No. TikTok shows effort can improve while information remains weak; Orange, SHEIN, and Vanity Fair show why refusal has to be checked technically. |
| What should a next study do? | Collect three or more controlled time points per site, freeze context and scorer versions, double-code a subset, and test technical refusal as well as visible parity. |

## Run Order

1. Open the rehearsal-ready PPTX in Presenter View and run the full deck once
   with a timer.
2. Run the 90-second version without looking at notes.
3. Answer three question-bank prompts aloud, beginning with the experiment and
   causality questions.
4. Make at most two evidence-preserving corrections to wording, pace, or a
   transition. Do not add a stronger claim just to make the story sound more
   decisive.
5. Record the observed result in
   `data/closeout/human_closeout_confirmation_2026-07-30.csv` using this exact
   compact form: `彩排=总时长X:XX; Q&A=X:XX; 修改1=...; 修改2=...`.
6. Only after a real run is recorded, change `presentation_final_qa` from
   `pending` to `verified` and execute the closeout final-index command in
   `docs/research/closeout_low_token_runbook_2026-07-27.md`.

## Source Pointers

- Case table: `data/retrospective_longitudinal_cases_2026-07-29.csv`
- Source registry: `data/retrospective_source_registry_2026-07-29.csv`
- Full evidence and limitations: `docs/research/july29_retrospective_longitudinal_evidence_rescue_2026-07-29.md`
- Current closeout state: `docs/research/aug03_closeout_reconciliation_2026-08-03.md`
- Official SSRP requirements: https://case.edu/studentlife/ugresearch/programs-and-funding/ssrp
