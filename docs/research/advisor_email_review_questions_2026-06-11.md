# Advisor Email Draft, 2026-06-11

Subject: Consent Interface Audit: Evidence Review Questions Before Next Capture

Dear Professor Singh,

I am writing to update you on the current state of the consent-interface audit
project and to ask a few specific questions before I run the next capture or
expand the sample.

The Week 2 evidence gate is complete. The current package has 5 Week 2 target
sites, 42 audit reports, and 20 longitudinal summaries. The sanity check is
`ready`: each Week 2 target has a consent-table row, screenshot and DOM
references, hashes, a matching audit report, and a weekly summary.

After manually reviewing the Week 2 screenshots, the five sites split into two
groups:

| Site | Current screenshot-based interpretation |
|---|---|
| The Guardian | Visible consent choice interface with "Yes, I accept", "No, thank you", and "Manage cookies". |
| Coca-Cola | Visible Privacy Preference Center with "Allow All", "Confirm My Choices", "Reject All", and category toggles. |
| CNN | No visible first-screen consent banner in the screenshot, although the DOM contains hidden OneTrust preference-center material. |
| Booking.com | No visible first-screen consent banner in the screenshot, although the DOM includes OneTrust script evidence. |
| NerdWallet | No visible first-screen consent banner in the screenshot. |

This means I should not describe CNN, Booking.com, or NerdWallet as
banner-path failures. For now, I am treating them as no-visible-banner contrast
cases. The Guardian and Coca-Cola are the two strongest current banner-present
cases for evidence cards and closer scoring review.

Before I continue, I need to confirm these points:

1. For the RQ1 results table, how should I represent no-visible-banner cases?
   Should they stay in the main table with a clear type label, be capped as a
   small contrast group, or move to a separate contrast/limitations table?
2. For the next step, should I first finish short evidence cards for the
   current five sites, or should I immediately expand toward the roughly
   20-site deep sample?
3. When expanding the sample, should I prioritize more sites with visible
   banner/control evidence, even if that means replacing some no-visible-banner
   or access-friction candidates?
4. For the next weekly capture around June 13, should I rerun the current five
   sites for continuity, or wait until the target list is adjusted?
5. There are still 8 CMP/manual-review rows pending from the earlier candidate
   pool. Should I resolve those now as part of sample selection, or leave them
   as secondary candidates while I build the cleaner 20-site deep sample?

My proposed plan, unless you would rather change it, is:

1. keep The Guardian and Coca-Cola as the first two banner-present evidence
   cards;
2. keep CNN, Booking.com, and NerdWallet as labeled no-visible-banner contrast
   cases;
3. prepare a short expansion list that prioritizes sites with visible
   banner/control evidence;
4. run the next weekly capture only after deciding whether the target list
   should remain the same or be adjusted.

Best,
Qianyi
