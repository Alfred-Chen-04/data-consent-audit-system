# CMP Confirmation Request, 2026-05-30

This is the short advisor/human-review handoff for the 8 CMP/manual-review rows
that are still blocking sample-lock decisions. It should be used together with
the visual packet and confirmation CSV, not as an automatic decision file.

## What To Open

1. Visual evidence packet: `data/cmp_review_packet_pilot_2026-05-30/index.html`
2. Contact sheet: `data/cmp_review_packet_pilot_2026-05-30/contact_sheet.png`
3. Confirmation sheet to edit: `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
4. Background brief: `docs/research/cmp_manual_review_brief_2026-05-30.md`

## Allowed Confirmation Values

Set `confirmation_status=confirmed` only after reviewing the packet evidence.
Then fill `confirmed_decision` with one of:

- `keep_consent_sample`
- `keep_no_banner_case`
- `rerun_fresh_context`
- `replace_candidate`
- `exclude`

If the evidence is not clear, leave `confirmation_status=pending` and add a
short note in `reviewer_notes`. Do not apply draft decisions automatically.

## Review Questions

1. Should no-banner contrast rows be allowed in the deep sample at all?
2. If yes, should the cap be 2-3 no-banner rows so banner-present sites remain
   the center of the sample?
3. Should access-friction rows such as Reddit and Walmart be replaced rather
   than treated as no-banner cases?
4. Should any site get one more region/browser-context check before replacement?

## Row-by-Row Request

| Site | Draft decision | Evidence pattern | Requested confirmation |
|---|---|---|---|
| BBC | `keep_no_banner_case` | Repeated no-banner evidence; DOM indicators include cookie/consent/GDPR terms. | Confirm only if no-banner contrast cases are in scope; otherwise mark `replace_candidate` or `rerun_fresh_context`. |
| New York Times | `keep_no_banner_case` | Repeated no-banner evidence; DOM indicators include cookie/consent/GDPR terms. | Same as BBC. Confirm as no-banner only if contrast rows are allowed. |
| Reddit | `replace_candidate` | No configured CMP indicators and screenshot evidence looks like access friction rather than a clean homepage. | Prefer `replace_candidate` unless an access-friction canary is explicitly desired. |
| Amazon | `keep_no_banner_case` | Repeated no-banner evidence with cookie/consent/GDPR/privacy-choice DOM indicators. | Confirm only if ecommerce no-banner contrast is useful; otherwise replace with a banner-present candidate. |
| Walmart | `replace_candidate` | DOM has cookie/consent/privacy-choice signals, but visual evidence shows robot/human challenge friction. | Prefer `replace_candidate` or access-feasibility review. |
| Airbnb | `keep_no_banner_case` | Repeated no-banner evidence with Onetrust/cookie/consent DOM indicators. | Strong region/context artifact candidate; confirm no-banner only if contrast rows are allowed. |
| Spotify | `keep_no_banner_case` | Repeated no-banner evidence with cookie DOM indicators and normal promotional page. | Confirm only if entertainment no-banner contrast is useful. |
| Chase | `keep_no_banner_case` | Repeated no-banner evidence with cookie DOM indicators and normal banking login/marketing page. | Confirm only if finance no-banner contrast is useful. |

## Suggested Conservative Outcome

If the advisor wants the cleanest SSRP paper sample:

- Confirm at most 2-3 no-banner contrast rows.
- Replace Reddit and Walmart.
- Keep BBC, New York Times, Airbnb, Amazon, Spotify, and Chase pending only if a
  region/browser-context check is planned.
- Prioritize finding more banner-present replacements before expanding beyond
  the current 5-site Week 2 capture list.

## After Review

After the confirmation sheet is edited, run:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli cmp-review-apply-confirmations
PYTHONPATH=src .venv/bin/python -m consent_audit.cli sample-lock-plan
PYTHONPATH=src .venv/bin/python -m consent_audit.cli sample-action-queues
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

Then update the paper/poster claim register before copying any final sample
language into the SSRP draft.
