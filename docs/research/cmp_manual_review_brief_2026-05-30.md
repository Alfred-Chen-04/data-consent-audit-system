# CMP Manual Review Brief, 2026-05-30

This brief summarizes the 8 `needs_cmp_review` rows after the fresh-context CMP
rerun. It is a decision aid, not a replacement for the human worksheet. Do not
copy these notes into final sample decisions without checking the linked
screenshots/DOM evidence.

Supporting artifacts:

- `data/cmp_review_queue_pilot_2026-05-30.csv`
- `data/cmp_review_worksheet_pilot_2026-05-30.csv`
- `data/cmp_review_suggestions_pilot_2026-05-30.csv`
- `data/cmp_review_rerun_targets_pilot_2026-05-30.csv`
- `data/cmp_review_packet_pilot_2026-05-30/index.html`
- `data/cmp_review_packet_pilot_2026-05-30/contact_sheet.png`
- `data/longitudinal_summary.csv`
- `docs/research/cmp_confirmation_request_2026-05-30.md`

## Current State

- 7 sites were rerun with cohort `cmp-rerun-2026-05-30`: BBC, New York Times,
  Amazon, Walmart, Airbnb, Spotify, and Chase.
- All 7 rerun rows still have `banner_detected=false`.
- Reddit was not rerun by the CMP target list because its saved DOM lacked the
  configured CMP indicator terms.
- The sample-lock plan should keep all 8 rows in `pending_manual_review` until
  a human reviewer decides whether they are no-banner contrast cases, region or
  browser-context artifacts, access failures, or replacement candidates.

## Site Notes

| Site | Evidence pattern | Visual read | Suggested human worksheet direction |
|---|---|---|---|
| BBC | 2 observations across smoke plus CMP rerun; no banner observed; DOM indicators include `cookie`, `consent`, and `gdpr`. | Normal BBC page, no visible consent layer. | Do not promote automatically. If the study allows persistent no-banner evidence, consider `keep_no_banner_case`; otherwise mark for replacement or a region-specific check. |
| New York Times | 2 observations across smoke plus CMP rerun; no banner observed; DOM indicators include `cookie`, `consent`, and `gdpr`. | Normal homepage, no visible consent layer. | Same as BBC: useful as a region/context finding, but weak as a banner-present sample. |
| Reddit | 1 smoke observation; no configured CMP indicators in DOM. | Screenshot shows a network/security block rather than a normal homepage. | Prefer `replace_candidate` unless the project wants an access-block canary. Do not treat this as a clean no-banner contrast without another successful capture. |
| Amazon | 2 pilot observations; no banner observed; DOM indicators include `cookie`, `consent`, `gdpr`, and `privacy choices`. | Normal shopping page, no visible consent layer. | Possible no-banner/ecommerce contrast case. Keep only if contrast cases are part of the methods; otherwise replace with a site that exposes a banner. |
| Walmart | 2 pilot observations; no banner observed; DOM indicators include `cookie`, `consent`, `ccpa`, and `privacy choices`. | Robot/human challenge interrupts the page. | Prefer `replace_candidate` or access-feasibility review; the current evidence is not a clean consent-interface observation. |
| Airbnb | 2 pilot observations; no banner observed; DOM indicators include `onetrust`, `cookie`, and `consent`. | Sparse Airbnb search page, no visible consent layer. | Keep in review. It is a strong region/context artifact candidate because Onetrust appears in DOM but no banner is visible. |
| Spotify | 2 pilot observations; no banner observed; DOM indicators include `cookie`. | Spotify page with sign-up/promotional UI; no visible consent layer. | Possible no-banner/entertainment contrast case, but not a banner-present sample. |
| Chase | 2 pilot observations; no banner observed; DOM indicators include `cookie`. | Normal banking login/marketing page, no visible consent layer. | Possible no-banner/finance contrast case if the study keeps contrast rows; otherwise replace. |

## Recommended Discussion Questions

1. Should the deep sample include any no-banner contrast cases, or should every
   retained site have an observed consent interface?
2. If no-banner contrast cases are allowed, what cap should we use? A practical
   cap is 2-3 rows so they support comparison without taking over the sample.
3. Should Reddit and Walmart be replaced now because the screenshots show access
   friction rather than clean no-banner behavior?
4. For BBC, New York Times, Airbnb, Amazon, Spotify, and Chase, is it worth one
   region/browser-context check before replacing, or is the current U.S./desktop
   evidence enough to classify them as no-banner/replace?

## Conservative Next Step

For the SSRP paper, deep quality matters more than broad coverage. The safest
sample-lock move is:

- keep the 4 current `provisionally_selected` rows in weekly capture;
- keep at most 2-3 confirmed no-banner contrast rows if the methods section
  explicitly wants them;
- replace Reddit and Walmart unless a reviewer wants access-friction canaries;
- prioritize finding additional banner-present candidates before expanding the
  optional 80+ tracker.
