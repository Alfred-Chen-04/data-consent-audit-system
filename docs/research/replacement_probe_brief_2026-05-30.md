# Replacement Candidate Probe Brief, 2026-05-30

This brief records a small replacement-candidate probe intended to find
banner-present sites for the deep sample after Reddit/Walmart looked weak in the
CMP manual review brief.

Supporting artifacts:

- `data/replacement_candidates_2026-05-30.csv`
- `data/access_probe_replacements_2026-05-30.csv`
- `data/replacement_candidates_contact_sheet_2026-05-30.png`
- `data/replacement_weekly_targets_2026-05-30.csv`
- `data/consent_table_replacements_2026-05-30.csv`

## Access Probe Summary

- 12 replacement candidates were probed.
- 8 loaded with HTTP status below 400.
- 1 showed a clear access-probe banner hit: Weather.com.
- 6 had block/error signals.

## Candidate Outcomes

| Site | Category | Probe outcome | Research use |
|---|---|---|---|
| Weather.com | weather | Clear Sourcepoint/privacy-manager banner in access probe. | Most promising replacement candidate, but weekly capture was not yet stable enough to lock. |
| AP News | news | Loaded cleanly, no banner selector hit. | Possible no-banner contrast, not a banner-present replacement. |
| USA Today | news | Loaded cleanly, no banner selector hit. | Possible no-banner/ad-supported media contrast, not a banner-present replacement. |
| eBay | ecommerce | Loaded cleanly, no banner selector hit. | Possible ecommerce no-banner contrast. |
| Best Buy | ecommerce | Loaded cleanly but landed on country selector. | Weak replacement unless a stable U.S. page is chosen. |
| Indeed | jobs | Loaded cleanly but redirected to Japanese Indeed. | Weak replacement for English desktop sample without URL/locale control. |
| Forbes | news | HTTP 200 but CAPTCHA/block text detected. | Replacement risk; avoid unless manually verified. |
| WebMD | health | HTTP 200 but CAPTCHA/block text detected. | Replacement risk; avoid unless manually verified. |
| Home Depot | ecommerce | Access denied / 403. | Replace/avoid. |
| Etsy | ecommerce | 403 / temporarily restricted. | Replace/avoid. |
| Tripadvisor | travel | 403 / temporarily restricted. | Replace/avoid. |
| Expedia | travel | HTTP 429 bot screen. | Replace/avoid. |

## Weather.com Follow-Up

Weather.com exposed a useful Sourcepoint-style consent panel in access probe,
including purpose-level Accept/Reject controls. Running the full weekly capture
surfaced a Layer 1 capture-agent issue: nested iframe buttons were filtered out
or not clicked when duplicate hidden text existed. Regression tests now cover
both cases, and the agent can collect concrete `Accept`/`Reject` iframe buttons
in a Weather-like fixture.

Weather.com is still not locked as a deep-sample row. Later weekly captures did
not consistently show the visible consent overlay, so the current status should
be `promising_reprobe`, not `provisionally_selected`.

## Next Sampling Move

The replacement search needs a second batch. Favor sites with known public,
English, unauthenticated pages and likely CMP overlays. Avoid candidates that
quickly showed hard blocks in this probe unless they are being kept only as
access-feasibility canaries.
