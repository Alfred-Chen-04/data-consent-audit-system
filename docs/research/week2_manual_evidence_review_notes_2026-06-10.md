# Week 2 Manual Evidence Review Notes, 2026-06-10

## Purpose

This note records a screenshot-grounded review of the five Week 2 evidence
bundles. It is a review draft for advisor/user confirmation, not a final sample
lock decision.

## Evidence Sources

- Worksheet: `data/week2_manual_evidence_review_2026-06-10.csv`
- Screenshots:
  - `data/captures/sites/www_theguardian_com_20260605_160209/layer1.png`
  - `data/captures/sites/www_cnn_com_20260605_160221/layer1.png`
  - `data/captures/sites/www_booking_com_20260605_160226/layer1.png`
  - `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png`
  - `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png`
- DOM refs in exports, not raw files in the current checkout:
  - `data/captures/sites/www_theguardian_com_20260605_160209/layer1.html`
  - `data/captures/sites/www_cnn_com_20260605_160221/layer1.html`
  - `data/captures/sites/www_booking_com_20260605_160226/layer1.html`
  - `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.html`
  - `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.html`

Note added 2026-06-28: the screenshot PNGs above are synced; these raw HTML
files are not present in the current Git checkout. Use DOM hashes and report
exports as the synced DOM evidence unless raw HTML files are restored or
recaptured.

## Review Summary

| Site | Screenshot-grounded finding | Draft coding | Review priority |
|---|---|---|---|
| The Guardian | The screenshot shows a visible choice interface with "Yes, I accept", "No, thank you", and "Manage cookies". | Banner-present manual review case. | High |
| CNN | The screenshot shows the CNN homepage with no visible first-screen consent banner. The DOM contains a hidden OneTrust preference center, so the visible screenshot should control the current coding. | No-visible-banner contrast pending table rule. | Medium |
| Booking.com | The screenshot shows the Booking.com search homepage with no visible first-screen consent banner. The DOM includes OneTrust script evidence, but no visible first-screen banner appears in the screenshot. | No-visible-banner contrast pending table rule. | Medium |
| NerdWallet | The screenshot shows a normal NerdWallet homepage/product-card view with no visible first-screen consent banner. | No-visible-banner contrast pending table rule. | Medium |
| Coca-Cola | The screenshot shows a visible Privacy Preference Center with "Allow All", "Confirm My Choices", "Reject All", and category toggles. | Banner-present manual review case. | High |

## Corrections To Automated Interpretation

- The Guardian's automated export reported no available first-layer paths, but
  the screenshot visibly shows accept, reject-like, and manage/customize
  controls. It should be manually reviewed as a banner-present case.
- Coca-Cola's automated export reported Accept available but Reject/Customize
  missing. The screenshot visibly shows "Reject All" and "Confirm My Choices"
  as well as category toggles. It should be manually reviewed as a banner-
  present case with richer pathway evidence than the automated row captured.
- CNN, Booking.com, and NerdWallet should not be treated as banner-path
  failures because the screenshots do not show a visible first-screen banner.

## Current Decision Need

The next advisor decision is not whether no-visible-banner observations exist;
the current evidence shows they do. The decision is how to represent them:

1. keep them in the main RQ1 table with a type label;
2. cap them as a small contrast group;
3. move them to a separate contrast/limitations table.

Until that rule is decided, sample expansion should prioritize additional
banner-present sites while preserving these three rows as contrast candidates.
