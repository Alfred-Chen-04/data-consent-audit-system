# Advisor Email Draft, 2026-06-06

Subject: SSRP Consent Interface Audit: Week 2 Capture Results and Next Sample Step

Dear Professor Singh,

I wanted to send the follow-up update after running the scheduled Week 2
capture for the consent-interface audit project.

The Week 2 evidence gate completed successfully. The five frozen target sites
all produced traceable evidence: consent-table row, screenshot reference, DOM
reference, hashes, matching audit report, and weekly summary. The sanity check
is now `ready`.

## Capture Results

| Site | Category | Capture status | Evidence status | Visible consent-banner evidence | Current coding note | RQ2 longitudinal status |
|---|---|---|---|---|---|---|
| The Guardian | news | complete | screenshot + DOM + hashes + report + weekly summary | banner/control evidence detected | banner-present case for manual evidence review | D / 4 events |
| CNN | news | complete | screenshot + DOM + hashes + report + weekly summary | no visible first-screen consent banner in the captured screenshot | no-visible-banner contrast candidate, not a banner-path failure claim | C / 3 events |
| Booking.com | travel | complete | screenshot + DOM + hashes + report + weekly summary | no visible first-screen consent banner in the captured screenshot | no-visible-banner contrast candidate, not a banner-path failure claim | C / 3 events |
| NerdWallet | finance | complete | screenshot + DOM + hashes + report + weekly summary | no visible first-screen consent banner in the captured screenshot | no-visible-banner contrast candidate, not a banner-path failure claim | C / 3 events |
| Coca-Cola | food | complete | screenshot + DOM + hashes + report + weekly summary | banner/control evidence detected | banner-present case; Accept observed, Reject/Customize/Dismiss not observed in the first layer | D / 5 events |

The updated RQ1 table now separates banner-present evidence from no-visible-
banner evidence. In this five-site gate, The Guardian and Coca-Cola are the
clearer banner-present cases. CNN, Booking.com, and NerdWallet have evidence
bundles, but their screenshots do not show a visible first-screen consent
banner, so I am treating them as no-visible-banner contrast candidates pending
the sample-coding rule rather than as banner-path failure claims.

The current RQ2 table shows longitudinal severity `C=3, D=2`. The two
highest-priority examples for closer evidence review are Coca-Cola and The
Guardian, because their latest summaries include pathway-level changes in
addition to visual/text/DOM changes.

## Sample Logic

I am continuing with the direction from your June 5 guidance:

1. Keep RQ1 consent-interface scoring and RQ2 longitudinal capture/versioning
   as the paper spine.
2. Treat clean repeated no-banner observations as contrast cases rather than
   failed samples.
3. Expand from this 5-site evidence gate toward an approximately 20-site deep
   sample only after the evidence gate is stable.
4. Keep the broader 80-ish prior list as a scaling/candidate pool, not as the
   immediate deep-analysis sample.

The manual-review queue is still separate from locked sample decisions. There
are 8 pending CMP/manual-review rows. Current no-banner contrast candidates
include BBC, New York Times, Amazon, Airbnb, Spotify, and Chase. Reddit and
Walmart still look more like access-friction or replacement cases than clean
no-banner contrasts.

## Artifacts

The main local evidence files are:

- `docs/research/week2_sanity_check_2026-06-06.md`
- `docs/research/week2_cycle_report_2026-06-06.md`
- `docs/research/ssrp_results_tables_2026-06-06.md`
- `docs/research/ssrp_claim_register_2026-06-06.md`
- `data/research_package/audit_report_summary.csv`
- `data/research_package/longitudinal_summary.csv`

## Questions

I have three questions before expanding the sample:

1. For the next update, would you prefer a compact site-level table like the
   one above, or one evidence card per site with screenshot/DOM/report
   references?
2. Should the 20-site deep sample include only a small number of clean
   no-banner contrast examples, or should all repeated no-banner observations
   remain in the main sample table with a type label?
3. For the next expansion step, should I prioritize more banner-present sites
   with complete pathway evidence, or preserve the current mix of banner-present
   cases plus clean no-banner contrasts?

My immediate next step is to review the five evidence bundles, keep weekly
capture running on the frozen targets, and then expand carefully toward the
roughly 20-site deep sample.

Best,
Qianyi
