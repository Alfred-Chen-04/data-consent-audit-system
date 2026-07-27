# Presentation/Poster Work Order, 2026-07-02

## Purpose

This is the current work order after the July 1 scope update.

Canonical goal statement:

- `docs/research/current_project_goal_2026-07-02.md`

The summer deliverables are:

- presentation;
- large poster;
- traceable evidence package.

A formal paper is not required for the current summer scope unless Dr. Singh
reintroduces it later.

## Current Evidence Base

Use only the current evidence state:

- Week 2 evidence gate: 5 sites.
- Research package: 42 audit reports and 20 longitudinal summaries.
- Screenshot evidence: 326 tracked `layer1.png` files.
- Raw HTML files: 0 synced `layer1.html` files in this checkout.
- Current-five decision sheet: 7 blank `confirmed_decision` cells.
- CMP/manual-review sheet: 8 pending rows.

## Presentation/Poster Story

The safest story right now is:

1. The project follows the original two proposal RQs: RQ1 computational
   audit/scoring of layered consent interfaces, and RQ2 automatic
   capture/versioning of privacy interfaces over time.
2. The workflow records screenshots, DOM hashes/report refs, scoring outputs,
   and longitudinal summaries.
3. Guardian and Coca-Cola are the current banner-present evidence-card
   candidates.
4. CNN, Booking.com, and NerdWallet are no-visible-banner contrast candidates.
5. The final poster should be honest about unresolved pieces: current-five
   treatment, CMP/manual review, no raw HTML sync, and whether to expand beyond
   five sites.

## Work Blocks

| Order | Work block | Output | Stop condition |
|---|---|---|---|
| 1 | Send advisor scope-update email | Advisor response or meeting time | Stop if advisor changes scope/sample rule. |
| 2 | Record current-five decisions | Filled `data/current_five_decision_sheet_2026-06-19.csv` | Do not expand until decisions are recorded. |
| 3 | Manual-validate current five | Evidence-card notes for Guardian/Coca-Cola and contrast notes for CNN/Booking/NerdWallet | Stop if screenshots do not support the current treatment. |
| 4 | Build presentation outline | Slide outline with intro, method, evidence cards, limits, next steps | Stop before polishing visuals if sample treatment is still unresolved. |
| 5 | Build poster wireframe | Poster sections and figure placeholders | Use current figures only; no invented charts. |
| 6 | Decide expansion | Either stay with five-site story or add banner-present examples | Only run capture after this decision. |

## Slide Outline Draft

1. Title: Traceable Consent Interface Audit
2. Research problem: firms use layered privacy interfaces as communication
   tools, but unbiased choice and interface change are hard to audit
   systematically.
3. RQ1 method: capture bundle -> Layer 1/2/3 scoring -> report.
4. RQ2 method: repeated capture -> multimodal fingerprint -> longitudinal
   summary.
5. Evidence card 1: The Guardian.
6. Evidence card 2: Coca-Cola.
7. Contrast cases: CNN, Booking.com, NerdWallet.
8. Longitudinal/versioning evidence: current summaries and limits.
9. Limitations: no final 20-site sample, pending CMP review, no synced raw HTML,
   no-visible-banner treatment pending.
10. Next steps: advisor decision, sample expansion or manual validation, final
   poster/demo polish.

## Poster Sections Draft

| Section | Content |
|---|---|
| Question | RQ1: how can layered consent interfaces be scored for unbiased choice? RQ2: how can privacy interfaces be captured/versioned over time? |
| Workflow | Capture bundle -> scoring layers -> AuditReport; repeated captures -> fingerprints -> longitudinal summaries. |
| Evidence Cards | Guardian and Coca-Cola. |
| Contrast Cases | CNN, Booking.com, NerdWallet as no-visible-banner examples. |
| Findings So Far | 5-site Week 2 evidence gate, 42 reports, 20 summaries. |
| Limitations | Pending decisions, CMP review, no raw HTML sync, sample not final. |
| Next Step | Advisor chooses validation/rerun/expansion path. |

## Do Not Claim

- Do not say the final presentation/poster is complete.
- Do not say there is a locked 20-site final sample.
- Do not say raw HTML snapshots are synced.
- Do not say no-visible-banner rows are banner-path failures.
- Do not say the project no longer has future-paper potential; only say the
  current summer scope does not require a formal paper.
