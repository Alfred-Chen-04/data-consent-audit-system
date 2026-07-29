# Current Project Goal, 2026-07-02

This is the current canonical explanation of the project goal. If another
current-facing document sounds like the project is only about screenshots,
paper prose, a legal verdict, or SOC 2, use this file to correct it.

## One-Sentence Goal

The project is a longitudinal study of how the same firms' consent interfaces
change over time and whether those changes improve, regress, mix, or preserve
user choice. RQ1 defines the repeatable measurement; RQ2 creates the comparable
time series needed to interpret change.

In the proposal's original division of labor, RQ1 scores layered consent interfaces for unbiased choice across the full pathway, and RQ2 captures and versions repeated observations. The longitudinal objective is the synthesis of those two operations.

## Overarching Longitudinal Objective

The proposal did not state this as a separate research question, but it is the
reason the two proposal questions belong together:

> Across repeated, controlled observations of the same website, how does its
> consent interface evolve, and what do changes in pathway availability,
> pathway effort, transparency, and unbiased choice imply for users?

This is an overarching objective, not a replacement or a newly invented RQ3.
The proposal questions below remain verbatim.

## The Two Proposal RQs

These two questions operationalize the longitudinal objective:

1. RQ1: How can we develop a computational audit and scoring system to quantify
   layered consent interfaces in terms of unbiased choice across the full
   consent pathway?
2. RQ2: How can we automatically capture and version firms' privacy interfaces
   to systematically document interface changes over time?

RQ1 supplies a stable ruler. RQ2 applies that ruler repeatedly. A longitudinal
conclusion is possible only after matched captures are validated under the same
browser context and scoring version.

## What The Project Is

- A longitudinal consent-interface study.
- A repeatable consent-interface audit framework.
- A scoring system for choice architecture, path availability, path effort,
  transparency, and unbiased choice.
- A longitudinal capture/versioning system for repeated, matched observations
  of the same interfaces.
- A directional interpretation protocol: improvement, regression, mixed
  change, stable, or insufficient evidence.
- A research workflow that keeps every score and change claim tied to evidence.

## What The Project Is Not

- Not a screenshot collection project.
- Not a browser-capture demo as the main product.
- Not a legal compliance verdict.
- Not a SOC 2 audit system.
- Not a long-form privacy-policy text audit.
- Not a final long-term evolution result yet.
- Not a claim that every technical hash or severity change is a substantive
  interface improvement or regression.

## Role Of Screenshots And Evidence

Screenshots, DOM refs, visible text, hashes, path attempts, and event logs are
evidence inputs. They exist to support RQ1 and RQ2:

- For RQ1, they support scoring: what paths exist, how hard they are to use,
  how text is framed, and whether choices are visually/structurally balanced.
- For RQ2, they support versioning: what changed across matched captures and
  whether the same RQ1 dimensions improved, regressed, moved in both
  directions, or stayed stable.

Evidence traceability is a design requirement, not the research question.

## Current Summer Deliverables

The current summer deliverables are:

1. Presentation.
2. Large poster.
3. Traceable evidence package supporting the presentation/poster.

A formal paper is not required as the current summer deliverable unless
Dr. Singh reintroduces it. Existing paper artifacts remain useful source notes.

## What To Say In Presentation

Use this framing:

> This project asks how the same consent interface evolves over time. RQ1
> defines a repeatable measure of pathway availability, effort, transparency,
> and unbiased choice. RQ2 applies that measure to matched captures. The pilot
> proves that the evidence pipeline can surface change candidates, but the
> current one-interval dataset is not long enough or consistent enough to claim
> improvement or regression.

## Current Evidence State

Current verified state:

- Week 2 evidence gate: 5 target sites.
- Current matched comparison: May 29 to June 5 for the five target sites.
- Research package: 42 audit reports and 20 longitudinal summaries, including
  same-day repeats and non-target sites; these counts are not 42 and 20
  independent long-term observations.
- Local screenshot evidence: 326 tracked site `layer1.png` files.
- Current evidence classes: 2 banner-present matched cases and 3 repeated
  no-visible-first-screen-banner contrasts.
- Current directional result: insufficient evidence for a defensible
  improvement or regression claim.
- Open decisions: 7 blank current-five decisions and 8 pending CMP/manual-review
  rows.

## Current Document Map

| Document | Current role |
|---|---|
| `SCHEMA.md` | Research questions, ontology navigator, pipeline map. |
| `CONCEPTS.md` | Authoritative scoring ontology. |
| `docs/research/current_project_goal_2026-07-02.md` | Canonical plain-language goal and presentation framing. |
| `docs/research/july3_scope_fact_review_and_poster_plan_2026-07-03.md` | Latest scope/fact review, completion-risk check, and poster-safe writing plan. |
| `docs/research/current_scope_2026-07-01.md` | Current summer deliverable scope. |
| `docs/research/project_inventory_and_poster_story_2026-07-02.md` | What exists, what evidence is verified, and how to avoid screenshot-only framing. |
| `docs/research/presentation_poster_work_order_2026-07-02.md` | Operational order for building presentation/poster materials. |
| `docs/research/ssrp_results_tables_2026-06-06.md` | Current evidence summaries for RQ1/RQ2, not final paper tables. |
| `docs/research/ssrp_claim_register_2026-06-06.md` | Claim safety register. |

## Safe Current Conclusion

The safe current conclusion is:

> RQ1 provides a repeatable multidimensional measure and RQ2 can apply it to
> matched captures. In the current five-site, one-interval pilot, automated
> change signals identify cases for review, but they do not establish that any
> consent interface improved or regressed. A defensible evolution claim
> requires additional controlled time points and same-version rescoring.

## Do Not Claim

- Do not say the project is mainly screenshots.
- Do not say the final dataset is complete.
- Do not say there is a locked 20-site final sample.
- Do not say all current sites failed consent compliance.
- Do not say no-visible-banner contrast cases are banner-path failures.
- Do not say raw HTML snapshots are synced locally.
- Do not translate longitudinal severity letters into improvement or
  regression; they are review-priority signals.
- Do not treat a scoring-code change as a website-interface change.
