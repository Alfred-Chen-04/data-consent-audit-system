# Replacement Candidate Probe Batch 2 Brief, 2026-05-30

This brief records the second replacement-candidate probe after the first probe
found Weather.com promising but unstable. The goal was to find at least one
banner-present, public, unauthenticated site that can strengthen the deep sample
if Reddit/Walmart or blocked pilot rows are replaced.

Supporting artifacts:

- `data/replacement_candidates_batch2_2026-05-30.csv`
- `data/access_probe_replacements_batch2_2026-05-30.csv`
- `data/replacement_candidates_batch2_contact_sheet_2026-05-30.png`
- `data/replacement_weekly_targets_batch2_2026-05-30.csv`
- `data/consent_table_replacements_batch2_2026-05-30.csv`
- `data/replacement_review_batch2_2026-05-30.csv`
- `data/deep_sample_weekly_targets_expanded_2026-05-30.csv`
- `data/audit_report_summary.csv`
- `data/research_package/`

## Access Probe Summary

- 16 replacement candidates were probed.
- 7 loaded with HTTP status below 400.
- 4 showed access-probe banner selector hits.
- 9 had block/error signals.

The access-probe banner hits were:

| Site | Selector hit | Probe interpretation |
|---|---|---|
| Coca-Cola | `#onetrust-consent-sdk` | Clear OneTrust preference center. |
| IKEA | `#onetrust-banner-sdk` | Visible cookie bar in probe screenshot. |
| IBM | `#truste-consent-track` | Consent panel visible, but locale redirected to Japanese. |
| Intuit | `#onetrust-banner-sdk` | Bottom OneTrust banner in probe screenshot. |

## Weekly Capture Outcome

| Site | Weekly outcome | Research use |
|---|---|---|
| Coca-Cola | Full pipeline passed Layer 1 with Accept, Reject, and Customize available; Layer 2 was Easy; Transparency grade B; Unbiased Choice grade A; final tier Compliant. | Strong banner-present replacement candidate. Promote for human/advisor review as a likely deep-sample addition. |
| IKEA | Access probe showed a banner, but full weekly capture did not stably reproduce visible actionable paths. | Promising but unstable; keep as reprobe/context-control candidate, not locked. |
| IBM | Access probe showed a TrustArc panel, but full capture redirected to Japanese content and did not detect paths. | Unstable/locale-sensitive; not a default English deep-sample replacement. |
| Intuit | Access probe showed a banner, but full capture returned an XML-like page snapshot and no paths. | Unstable capture target; not locked. |

## Other Candidate Outcomes

Loaded without banner hits:

- Pepsi
- Nike, which redirected to `nike.com.cn`
- National Geographic

Blocked or errored:

- McDonald's, Adobe, United, and NBA: `net::ERR_HTTP2_PROTOCOL_ERROR`
- Salesforce, Delta, and Marriott: access denied / 403
- Oracle and Hyatt: HTTP 403

## Sampling Decision

Coca-Cola is the first replacement candidate that reproduced a complete,
traceable, banner-present audit in the full pipeline. It should be treated as a
strong candidate for the locked deep sample, pending human/advisor confirmation
and category-balance review.

IKEA, IBM, and Intuit are evidence-useful but should stay in a reprobe bucket.
They help document region, locale, and dynamic-rendering instability, but they
should not be counted as stable banner-present replacements yet.

The machine-readable replacement review table now makes that distinction
explicit:

- `verified_replacement=1`: Coca-Cola
- `promising_reprobe=3`: IKEA, IBM, Intuit
- `no_banner_or_locale_shift=3`: Nike, Pepsi, National Geographic
- `blocked_or_error=9`: McDonald's, Adobe, Salesforce, Oracle, Delta, United,
  Marriott, Hyatt, NBA

The expanded weekly target list adds only the verified replacement to the
current capture shortlist. Current expanded targets are The Guardian, CNN,
Booking.com, NerdWallet, and Coca-Cola.
