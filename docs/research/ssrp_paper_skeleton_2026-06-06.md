# SSRP 2026 Paper Skeleton, 2026-06-06

## Abstract Draft

This paper presents a traceable computational audit framework for layered consent interfaces and a longitudinal capture workflow for documenting how those interfaces change over time. The current draft uses the completed Week 2 evidence gate as pilot evidence, not as the final SSRP dataset.

## Research Questions

1. How to develop a computational audit and scoring system to quantify the layered consent interfaces in terms of unbiased choice across the full consent pathway?
2. How can we automatically capture and version firms' privacy interfaces to systematically document interface changes over time?

## Current Evidence Snapshot

- Evidence window: Week 2
- Target sites: 5
- Categories: finance=1, food=1, news=2, travel=1
- Audit reports in package: 42
- Longitudinal summaries in package: 20
- Banner evidence classes: banner_present=2, no_visible_banner=3
- Banner-present automated tiers: High-Risk=2
- Raw automated target tiers: High-Risk=5
- Latest longitudinal severity: C=3, D=2

## Draft Section Map

Generated drafting artifact: run `consent-audit ssrp-writing-pack` to refresh `docs/research/ssrp_writing_pack_2026-06-06.md`.

1. Introduction: consent interfaces as privacy communication and why static audits miss operational change.
2. Background: Notice-and-Choice, cookie-banner auditing, longitudinal privacy measurement, and multimodal agents as method.
3. Methods: three-layer scoring, evidence requirements, deterministic grades after schema validation, and weekly capture/versioning.
4. Pilot Evidence: current RQ1 scoring table and RQ2 longitudinal change summaries.
5. Discussion: what longitudinal evidence adds, what is not a legal determination, and small GRC/SOC 2 relevance note.
6. Limitations: desktop-only, public unauthenticated pages, English-focused, location/session effects, and manual validation gates.

## Current Deep-Sample Evidence Table

| Site | Category | Banner evidence | RQ1 coding | Latest automated tier | Path status | Longitudinal |
|---|---|---|---|---|---|---|
| The Guardian | news | banner/control evidence | banner-present scored case | High-Risk | missing accept\|reject\|customize\|dismiss | D / 4 |
| CNN | news | no visible first-screen banner | no-visible-banner contrast; do not treat as banner-path failure | High-Risk | missing accept\|reject\|customize\|dismiss | C / 3 |
| Booking.com | travel | no visible first-screen banner | no-visible-banner contrast; do not treat as banner-path failure | High-Risk | missing accept\|reject\|customize\|dismiss | C / 3 |
| NerdWallet | finance | no visible first-screen banner | no-visible-banner contrast; do not treat as banner-path failure | High-Risk | missing accept\|reject\|customize\|dismiss | C / 3 |
| Coca-Cola | food | banner/control evidence | banner-present scored case | High-Risk | Accept | D / 5 |

## Results Tables To Fill

Generated table artifact: run `consent-audit ssrp-results-tables` to refresh `docs/research/ssrp_results_tables_2026-06-06.md`.

| Table | Purpose | Current source |
|---|---|---|
| RQ1 scoring summary | Path availability, tier, Layer 2/3 columns by site | `data/research_package/audit_report_summary.csv` |
| RQ2 longitudinal summary | Event counts, event types, severity, implications by site-week | `data/research_package/longitudinal_summary.csv` |
| Sample construction log | Why sites were selected, replaced, or held for review | `data/sample_lock_plan_pilot_2026-05-30.csv` |

## Figure Queue

Generated figure artifact: run `consent-audit ssrp-figure-plan` to refresh `docs/research/ssrp_figure_plan_2026-06-06.md`.

- Architecture diagram: URL to capture bundle to three layers to report/export.
- Three-layer rubric table from `CONCEPTS.md`.
- Evidence card example with screenshot, DOM/hash refs, pathway outcomes, and quotes.
- Longitudinal timeline for 2-3 sites with visible change events.

## Known Gaps Before Draft Freeze

- Review the completed Week 2 evidence gate and select the strongest examples.
- Resolve or explicitly bracket the 8 pending CMP/manual-review rows.
- Decide whether no-banner contrast cases belong in the methods section.
- Add final limitations text after the observed capture failures and manual-review outcomes are known.

## Source Artifacts

- Targets: `data/week2_deep_sample_targets_2026-06-06.csv`
- RQ1 table: `data/research_package/audit_report_summary.csv`
- RQ2 table: `data/research_package/longitudinal_summary.csv`
- Manifest: `data/research_package/research_manifest.json`
