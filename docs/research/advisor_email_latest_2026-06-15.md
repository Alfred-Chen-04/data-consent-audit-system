# Advisor Email Draft, 2026-06-15

Subject: Consent Interface Audit: Current Evidence Status and Next Decisions

Dear Professor Singh,

I am writing with the latest status of the consent-interface audit project and
the specific decisions I need before I change the sample or rerun the capture.

The valid evidence package is still the completed Week 2 evidence gate. The
research package currently has 42 audit reports and 20 longitudinal summaries,
and the Week 2 sanity check is `ready`: each of the five target sites has a
consent-table row, screenshot and DOM references, hashes, a matching audit
report, and a weekly summary.

After manual screenshot review, the current five sites split into two groups:

| Site | Current interpretation |
|---|---|
| The Guardian | Banner-present manual-review case: visible choice interface with "Yes, I accept", "No, thank you", and "Manage cookies". |
| Coca-Cola | Banner-present manual-review case: visible Privacy Preference Center with "Allow All", "Confirm My Choices", "Reject All", and category toggles. |
| CNN | No visible first-screen consent banner in the screenshot; DOM contains hidden OneTrust preference-center material. |
| Booking.com | No visible first-screen consent banner in the screenshot; DOM includes OneTrust script evidence. |
| NerdWallet | No visible first-screen consent banner in the screenshot. |

I also attempted the planned Week 3 continuity capture on June 14 using the
same five-site list. That attempt failed at browser navigation for all five
sites, so I am not treating it as new consent-interface evidence. A light HTTP
check afterward showed that CNN, Booking.com, NerdWallet, and Coca-Cola were
reachable at the HTTP layer, while The Guardian timed out. So the correct
interpretation is a browser/capture-context failure, not evidence that the
interfaces changed.

Before I continue, I need to confirm these decisions:

1. For the RQ1 results table, should no-visible-banner cases stay in the main
   table with a clear type label, be capped as a small contrast group, or move
   to a separate contrast/limitations table?
2. Should I finish evidence cards for the current five sites first, or begin
   expanding immediately toward the roughly 20-site deep sample?
3. When expanding, should I prioritize sites with visible banner/control
   evidence, even if that means replacing some no-visible-banner or
   access-friction candidates?
4. Given the June 14 browser-navigation failure, should I rerun the current
   five-site continuity capture after a one-site smoke test, or wait until the
   target list is adjusted?
5. There are still 8 CMP/manual-review rows pending from the earlier candidate
   pool. Should I resolve those now as part of sample selection, or keep them
   as secondary candidates while building a cleaner deep sample?

My proposed next step is to keep the Week 2 evidence as the current valid
dataset, write evidence cards for The Guardian and Coca-Cola first, keep
CNN/Booking.com/NerdWallet as labeled no-visible-banner contrast candidates,
and only rerun the Week 3 capture after a small browser smoke confirms the
capture environment is working.

Best,
Qianyi
