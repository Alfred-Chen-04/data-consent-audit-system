# July 9 Poster Asset Manifest, 2026-07-09

Purpose: turn the July 7 poster layout draft into a verified poster asset list
using only existing local screenshot evidence.

This manifest adds no new browser capture and no new consent-interface
evidence. It checks the files that the poster layout already intends to use.

## Current Facts Used

- Date checked: 2026-07-09.
- Core research window: May 30-August 7, 2026.
- Calendar progress: 41 of 70 core-cycle days, or 58.6%.
- Days left before August 7 core deadline: 29.
- Days left before August 31 polish deadline: 53.
- Branch and upstream at start of this July 9 work:
  `850b857ac2a6721c74a480d512c739479734f3cb`.
- PR #8: open, draft, mergeable, not merged into `main`.
- `research-status`: preflight `ready_for_capture`, sanity `ready`, cycle
  capture `completed`.
- Research package: 42 audit reports and 20 longitudinal summaries.
- Banner-detected counts in `audit_report_summary.csv`: true=9, false=33.
- Screenshot evidence: 326 site `layer1.png` files; 0 synced site
  `layer1.html` raw DOM files.
- Current-five decision sheet: 7 rows, 7 blank decisions.
- CMP/manual-review confirmation sheet: 8 rows, 8 pending confirmations.

## Manifest Scope

Use this manifest for poster asset placement and captioning only. It does not
change site coding, create new evidence, or resolve advisor/user decisions.

The July 8 draft task was carried forward on July 9 with updated calendar
facts. The evidence files themselves are the same verified Week 2 screenshots.

## Poster Screenshot Assets

| Site | Evidence role | Poster placement | Screenshot path | PNG status | Dimensions | Bytes | Safe caption | Do-not-claim note |
|---|---|---|---|---|---:|---:|---|---|
| The Guardian | Banner-present evidence card | Middle column large card | `data/captures/sites/www_theguardian_com_20260605_160209/layer1.png` | exists, parses as PNG | 1440x900 | 144914 | Stored screenshot evidence shows a visible Guardian consent-choice screen with accept/reject/manage-cookie choices. | Do not claim legal compliance or final site judgment. |
| Coca-Cola | Banner-present evidence card | Middle column large card | `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png` | exists, parses as PNG | 1440x900 | 338126 | Stored screenshot evidence shows a visible Privacy Preference Center with consent controls. | Do not claim legal compliance or final site judgment. |
| CNN | No-visible-banner contrast | Right column compact contrast row | `data/captures/sites/www_cnn_com_20260605_160221/layer1.png` | exists, parses as PNG | 1440x900 | 439361 | Stored screenshot shows the CNN homepage with no visible first-screen cookie banner. | Do not treat as a banner-path failure without the separate table rule. |
| Booking.com | No-visible-banner contrast | Right column compact contrast row | `data/captures/sites/www_booking_com_20260605_160226/layer1.png` | exists, parses as PNG | 1440x900 | 97083 | Stored screenshot shows the Booking.com homepage/search UI with no visible first-screen cookie banner. | Do not treat as a banner-path failure without the separate table rule. |
| NerdWallet | No-visible-banner contrast | Right column compact contrast row | `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png` | exists, parses as PNG | 1440x900 | 608556 | Stored screenshot shows the NerdWallet homepage/product UI with no visible first-screen cookie banner. | Do not treat as a banner-path failure without the separate table rule. |

## Placement Rules

- Use The Guardian and Coca-Cola as the two large banner-present evidence cards.
- Use CNN, Booking.com, and NerdWallet as smaller no-visible-banner contrast
  assets.
- Keep all five assets labeled as stored screenshots from the current evidence
  package, not live website states.
- Do not crop screenshots so tightly that the consent-interface context or
  no-visible-banner context disappears.
- If thumbnails are used for the three contrast cases, keep the no-visible-
  banner label next to each thumbnail.

## Poster Caption Guardrails

Allowed:

- "Stored screenshot evidence shows..."
- "Current pilot evidence..."
- "No visible first-screen cookie banner in the stored screenshot..."
- "Method/evidence example..."

Not allowed:

- "Final dataset complete."
- "20-site sample locked."
- "Raw HTML files synced."
- "CNN, Booking.com, or NerdWallet failed consent-path availability."
- "This site is legally compliant."
- "This site is legally non-compliant."
- "This screenshot proves the site still looks the same today."

## Missing Or Unresolved Evidence

- Raw `layer1.html` files are not synced in this checkout.
- The 7 current-five decision rows remain blank.
- The 8 CMP/manual-review confirmations remain pending.
- PR #8 is still draft/open and not merged into `main`.

## Build Status

The five poster screenshot assets are present and image-valid for a first
poster mockup. The poster can use them as traceable pilot evidence, but final
claims still need the unresolved decisions above.
