# Week 2 Evidence Cards, 2026-06-11

## Purpose

These are short, paper/poster-friendly evidence cards for the two strongest
current banner-present Week 2 cases. They are based on the manual screenshot
review worksheet and should stay paired with the screenshot references listed
below. The DOM references are historical/generated refs in CSV/report exports;
the raw HTML files are not synced in the current checkout.

These cards are not the final SSRP results. They are the cleanest current
examples to discuss with the advisor before expanding the deep sample.

## Evidence Card: The Guardian

| Field | Current Evidence |
|---|---|
| URL | `https://www.theguardian.com/` |
| Category | News |
| Evidence class | Banner/control evidence |
| Draft coding | Banner-present manual review case |
| Screenshot | `data/captures/sites/www_theguardian_com_20260605_160209/layer1.png` |
| DOM ref in exports | `data/captures/sites/www_theguardian_com_20260605_160209/layer1.html` (raw HTML file not synced in current checkout) |
| Longitudinal severity | D |
| Event count | 4 |
| Event types | copy change, DOM restructure, layout change, pathway change |

### Screenshot-Grounded Observation

The screenshot shows a visible choice interface with these controls:

- "Yes, I accept"
- "No, thank you"
- "Manage cookies"

### Interpretation

This should be reviewed as a banner-present case, even though the automated
export reported no first-layer paths. The screenshot provides direct evidence
of accept, reject-like, and manage/customize controls.

### Current Caution

Do not rely only on the automated path booleans for this row. The current paper
table should either allow manual override after screenshot review or explicitly
separate automated extraction from human-confirmed evidence.

## Evidence Card: Coca-Cola

| Field | Current Evidence |
|---|---|
| URL | `https://www.coca-cola.com/us/en` |
| Category | Food |
| Evidence class | Banner/control evidence |
| Draft coding | Banner-present manual review case |
| Screenshot | `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png` |
| DOM ref in exports | `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.html` (raw HTML file not synced in current checkout) |
| Longitudinal severity | D |
| Event count | 5 |
| Event types | copy change, DOM restructure, layout change, pathway change, score change |

### Screenshot-Grounded Observation

The screenshot shows a visible Privacy Preference Center with these controls:

- "Allow All"
- "Confirm My Choices"
- "Reject All"
- category toggles

### Interpretation

This should be reviewed as a banner-present case with richer visible pathway
evidence than the latest automated row captured. The screenshot shows reject
and confirmation controls that were not fully reflected in the automated
first-layer path fields.

### Current Caution

Do not describe Coca-Cola as currently `Compliant` based on the latest Week 2
automated row. The stronger claim is narrower: the screenshot shows visible
banner/control evidence and should be manually reviewed before final scoring.

## Contrast Cases To Keep Separate

CNN, Booking.com, and NerdWallet should stay out of the banner-present evidence
card set for now. Their Week 2 screenshots show no visible first-screen consent
banner, so they are better represented as no-visible-banner contrast candidates
until the advisor confirms the table rule.
