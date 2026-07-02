# Current Project Goal, 2026-07-02

This is the current canonical explanation of the project goal. If another
current-facing document sounds like the project is only about screenshots,
paper prose, a legal verdict, or SOC 2, use this file to correct it.

## One-Sentence Goal

The project develops a computational audit and versioning framework for
privacy/consent interfaces as corporate communication objects: RQ1 scores
layered consent interfaces for unbiased choice across the full consent pathway,
and RQ2 captures and versions those interfaces to document change over time.

## The Two Proposal RQs

These two questions are the spine of the project:

1. RQ1: How can we develop a computational audit and scoring system to quantify
   layered consent interfaces in terms of unbiased choice across the full
   consent pathway?
2. RQ2: How can we automatically capture and version firms' privacy interfaces
   to systematically document interface changes over time?

Everything else is a method, evidence source, deliverable, or limitation.

## What The Project Is

- A consent-interface audit framework.
- A scoring system for choice architecture, path availability, path effort,
  transparency, and unbiased choice.
- A longitudinal capture/versioning system for repeated observations of the
  same interfaces.
- A research workflow that keeps every score and change claim tied to evidence.

## What The Project Is Not

- Not a screenshot collection project.
- Not a browser-capture demo as the main product.
- Not a legal compliance verdict.
- Not a SOC 2 audit system.
- Not a long-form privacy-policy text audit.
- Not a final 20-site dataset yet.

## Role Of Screenshots And Evidence

Screenshots, DOM refs, visible text, hashes, path attempts, and event logs are
evidence inputs. They exist to support RQ1 and RQ2:

- For RQ1, they support scoring: what paths exist, how hard they are to use,
  how text is framed, and whether choices are visually/structurally balanced.
- For RQ2, they support versioning: what changed across captures and whether
  the interface stayed stable or shifted.

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

> Firms use privacy and consent interfaces as communication tools. My project
> builds a computational audit and versioning framework for those interfaces.
> RQ1 asks how to score whether layered consent pathways support unbiased
> choice. RQ2 asks how to repeatedly capture and version those interfaces so
> changes over time can be documented. The current pilot shows the pipeline,
> evidence cards, longitudinal summaries, and the limits that still need
> advisor confirmation.

## Current Evidence State

Current verified state:

- Week 2 evidence gate: 5 target sites.
- Research package: 42 audit reports and 20 longitudinal summaries.
- Local screenshot evidence: 326 tracked site `layer1.png` files.
- Current evidence classes: 2 banner-present evidence-card candidates and 3
  no-visible-banner contrast candidates.
- Open decisions: 7 blank current-five decisions and 8 pending CMP/manual-review
  rows.

## Current Document Map

| Document | Current role |
|---|---|
| `SCHEMA.md` | Research questions, ontology navigator, pipeline map. |
| `CONCEPTS.md` | Authoritative scoring ontology. |
| `docs/research/current_project_goal_2026-07-02.md` | Canonical plain-language goal and presentation framing. |
| `docs/research/current_scope_2026-07-01.md` | Current summer deliverable scope. |
| `docs/research/project_inventory_and_poster_story_2026-07-02.md` | What exists, what evidence is verified, and how to avoid screenshot-only framing. |
| `docs/research/presentation_poster_work_order_2026-07-02.md` | Operational order for building presentation/poster materials. |
| `docs/research/ssrp_results_tables_2026-06-06.md` | Current evidence summaries for RQ1/RQ2, not final paper tables. |
| `docs/research/ssrp_claim_register_2026-06-06.md` | Claim safety register. |

## Safe Current Conclusion

The safe current conclusion is:

> The proposal's two-part system is feasible at pilot scale. The current work
> can produce evidence-linked audit reports for RQ1 and longitudinal summaries
> for RQ2, but final claims require advisor decisions about current-five
> treatment, CMP/manual-review rows, and whether to expand beyond the five-site
> evidence gate.

## Do Not Claim

- Do not say the project is mainly screenshots.
- Do not say the final dataset is complete.
- Do not say there is a locked 20-site final sample.
- Do not say all current sites failed consent compliance.
- Do not say no-visible-banner contrast cases are banner-path failures.
- Do not say raw HTML snapshots are synced locally.
