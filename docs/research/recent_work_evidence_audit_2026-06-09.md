# Recent Work Evidence Audit, 2026-06-09

## Purpose

This audit reviews the recent consent-interface audit work before sending the
next advisor email. It separates supported facts from interpretation and turns
the current evidence into decision questions.

## Evidence Checked

- `consent-audit research-status`
- `docs/research/week2_cycle_report_2026-06-06.md`
- `docs/research/week2_sanity_check_2026-06-06.md`
- `docs/research/ssrp_results_tables_2026-06-06.md`
- `docs/research/ssrp_claim_register_2026-06-06.md`
- `docs/research/advisor_response_action_plan_2026-06-05.md`
- `data/research_package/audit_report_summary.csv`
- `data/research_package/longitudinal_summary.csv`
- `data/research_package/research_manifest.json`
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
- Git history through commit `7088b3a`.

## Supported Recent Work

| Area | Supported fact | Evidence |
|---|---|---|
| Week 2 capture | The scheduled Week 2 evidence gate completed with 5/5 attempted and 5/5 successful captures. | `week2_cycle_report_2026-06-06.md` |
| Evidence completeness | All five Week 2 targets have consent rows, screenshot/DOM/hash evidence, matching audit reports, and weekly summaries. | `week2_sanity_check_2026-06-06.md` |
| Research package | Current package contains 42 audit reports and 20 longitudinal summaries. | `research-status`; `research_manifest.json` |
| RQ1 snapshot | Week 2 target evidence separates into 2 banner-present cases and 3 no-visible-banner cases. | `ssrp_results_tables_2026-06-06.md`; `audit_report_summary.csv` |
| RQ2 snapshot | Latest Week 2 longitudinal severity is C=3 and D=2. | `ssrp_results_tables_2026-06-06.md`; `longitudinal_summary.csv` |
| Screenshot evidence | 363 PNG screenshots are tracked in Git. | Git tracked files under `data/captures/**/*.png` |
| Paper/poster support | Paper skeleton, results tables, claim register, figure plan, writing pack, and poster plan are present. | `research-status` |
| Remaining manual review | 8 CMP/manual-review confirmation rows remain pending. | `cmp_review_confirmation_sheet_pilot_2026-05-30.csv` |

## Site-Level Facts

| Site | Current evidence class | Latest RQ1 interpretation | Latest RQ2 evidence |
|---|---|---|---|
| The Guardian | Banner/control evidence | Banner-present scored case; automated tier High-Risk; no first-layer paths detected. | Severity D; copy, DOM, layout, and pathway changes. |
| CNN | No visible first-screen banner | Contrast candidate; should not be treated as a banner-path failure claim. | Severity C; copy, DOM, and layout changes. |
| Booking.com | No visible first-screen banner | Contrast candidate; should not be treated as a banner-path failure claim. | Severity C; copy, DOM, and layout changes. |
| NerdWallet | No visible first-screen banner | Contrast candidate; should not be treated as a banner-path failure claim. | Severity C; copy, DOM, and layout changes. |
| Coca-Cola | Banner/control evidence | Banner-present scored case; Accept observed, Reject/Customize/Dismiss not observed in latest first layer. | Severity D; copy, DOM, layout, pathway, and score changes. |

## Claims That Are Safe To Make

- The project has moved from setup into a first traceable evidence gate.
- The current evidence gate is complete for the five frozen Week 2 sites.
- The pipeline now produces evidence-linked RQ1/RQ2 tables and draft paper/poster artifacts.
- The current sample is still pilot/evidence-gate material, not the final SSRP dataset.
- No-visible-banner observations should be discussed as contrast observations, not as failed banner-present consent flows.

## Claims To Avoid

- Do not say the final SSRP dataset is complete.
- Do not say all five Week 2 sites have visible consent banners.
- Do not say CNN, Booking.com, or NerdWallet failed consent-path availability as banner-present interfaces.
- Do not make legal compliance claims.
- Do not frame the project as a SOC 2 audit system.
- Do not treat the broader 80-ish candidate pool as the active deep sample.

## Decision Questions Derived From Evidence

1. **Next work mode:** Now that the five-site evidence gate is complete, should the next work block be manual labeling of these five evidence bundles, or expansion toward the about-20-site deep sample?
2. **No-visible-banner rule:** Since three of five Week 2 targets are no-visible-banner contrast observations, should the final RQ1 table include them in the main table with a type label, cap them as a contrast group, or move them to a separate contrast/limitations table?
3. **Expansion priority:** Should expansion prioritize additional banner-present sites with visible controls, even if that means replacing some no-visible-banner or access-friction candidates?
4. **Longitudinal cadence:** Should the next weekly capture around 2026-06-13 rerun the current five sites for continuity, or wait until the sample is adjusted/expanded?
5. **Advisor review format:** For the next check-in, should the evidence be shown as a compact site-level table or as one evidence card per site with screenshot/DOM/report references?

## Recommended Email Position

The email should report the completed evidence gate and then ask for decisions
on sample coding and next-step sequencing. It should not ask broad questions
like "what should I do next" without evidence. The most important decision is
how to handle no-visible-banner cases in the final deep sample and RQ1 table.
