# SSRP 2026 Writing Pack, 2026-06-06

## Evidence Snapshot

- Evidence window: Week 2
- Target sites: 5
- Categories: finance=1, food=1, news=2, travel=1
- RQ1 reports available for targets: 5/5
- RQ2 summaries available for targets: 5/5
- Banner evidence classes: banner_present=2, no_visible_banner=3
- Banner-present automated tiers: High-Risk=2
- Raw automated target tiers: High-Risk=5
- Latest longitudinal severity: C=3, D=2
- CMP confirmations: pending=8
- Cycle capture status: `completed`
- Claim status: ready for post-sanity drafting.

## Methods Draft Blocks

- Sample: This pilot uses a focused deep sample of 5 public websites selected for repeated evidence capture rather than a broad one-time crawl.
- Capture unit: each observation stores a screenshot, DOM snapshot, visible text, path-attempt log, hashes, and report references so later claims can be traced back to concrete evidence.
- Scoring discipline: model extraction can assist with text or visual cues, but final grades are produced by deterministic scoring after schema validation and evidence checks.
- Longitudinal unit: weekly summaries compare path availability, scores, text, DOM, layout, and fingerprint evidence so RQ2 can separate stable interfaces from changed ones.

## Preliminary Results Notes

- RQ1: banner-present automated tiers are High-Risk=2.
- RQ1 contrast context: no-visible-banner contrast candidates=3; raw automated tiers are High-Risk=5.
- RQ2: latest target longitudinal severity levels are C=3, D=2.
- Current claims remain ready for post-sanity drafting.
- Highest-priority longitudinal candidates: Coca-Cola, The Guardian, CNN.
- RQ1 result source: `docs/research/ssrp_results_tables_2026-06-06.md`.

## Discussion And Implication Notes

- The strongest contribution is the traceable link from visible consent-interface design to longitudinal evidence, not a legal conclusion about compliance.
- Use the longitudinal rows to explain why a single screenshot audit can miss meaningful interface drift, especially copy, layout, DOM, and pathway changes.
- Keep the small GRC/SOC 2 implication bounded: consent-interface evidence may support privacy readiness conversations, but this project is not a SOC 2 audit system.

## Limitations To Carry Forward

- Desktop public-page capture only; authenticated, mobile, geolocated, and user-history specific experiences may differ.
- English-focused visible text extraction and deterministic fallbacks may miss localized or heavily visual consent cues.
- Scheduled Week 2 live capture status is `completed`; result claims should cite the sanity check and source evidence references.
- pending CMP/manual-review confirmations remain unresolved: pending=8.
- Scores describe interface evidence, not legal compliance or user intent.

## Drafting Checklist

- Use ready Week 2 result claims only with the sanity check and source evidence refs.
- Run `consent-audit ssrp-claim-register` before polishing results prose.
- Re-run `week2-refresh-outputs` after live capture before copying tables or figure notes.
- Use exact screenshot, DOM, hash, and quote evidence when writing any site-specific claim.
- Keep SOC 2/GRC framing to a brief implication paragraph.

## Source Artifacts

- Targets: `data/week2_deep_sample_targets_2026-06-06.csv`
- RQ1 audit reports: `data/research_package/audit_report_summary.csv`
- RQ2 longitudinal summaries: `data/research_package/longitudinal_summary.csv`
- CMP confirmation sheet: `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
- Results tables: `docs/research/ssrp_results_tables_2026-06-06.md`
- Paper skeleton: `docs/research/ssrp_paper_skeleton_2026-06-06.md`
- Figure plan: `docs/research/ssrp_figure_plan_2026-06-06.md`
- Cycle report: `docs/research/week2_cycle_report_2026-06-06.md`
