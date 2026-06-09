# Week 2 Sample Plan, Prepared 2026-05-30

This note freezes the current Week 2 capture input and records a draft handling
plan for the 8 pending CMP/manual-review rows. It is designed for advisor review
before the June 6 weekly capture cycle.

Supporting artifacts:

- `data/week2_deep_sample_targets_2026-06-06.csv`
- `data/deep_sample_weekly_targets_expanded_2026-05-30.csv`
- `data/cmp_review_decision_draft_pilot_2026-05-30.csv`
- `data/cmp_review_packet_pilot_2026-05-30/index.html`
- `docs/research/expanded_weekly_capture_brief_2026-05-30.md`
- `docs/research/cmp_manual_review_brief_2026-05-30.md`

## Week 2 Capture Targets

The Week 2 default capture list has 5 active sites:

| Site | Category | Current role |
|---|---|---|
| The Guardian | news | Continuing weekly shortlist. |
| CNN | news | Continuing weekly shortlist. |
| Booking.com | travel | Continuing weekly shortlist after DOM fallback made capture stable enough. |
| NerdWallet | finance | Continuing weekly shortlist. |
| Coca-Cola | food | Verified replacement with repeated Compliant evidence. |

The list validates cleanly with `mentor_inherited=0` and categories
`finance=1`, `food=1`, `news=2`, and `travel=1`.

## CMP Decision Draft

The decision draft covers the 8 pending CMP/manual-review rows. These are not
final decisions; every row has `requires_human_confirmation=true`.

Draft counts:

- `keep_no_banner_case=6`: BBC, New York Times, Amazon, Airbnb, Spotify, Chase
- `replace_candidate=2`: Reddit, Walmart

Rationale:

- The six `keep_no_banner_case` rows have repeated no-banner observations in the
  current browser/location context. They are useful only if the methods section
  explicitly includes no-banner contrast cases.
- Reddit and Walmart are drafted as replacement candidates because the evidence
  looks like access friction rather than clean no-banner behavior.

## Advisor Questions

1. Should the paper include no-banner contrast rows at all?
2. If yes, should the cap be 2-3 rows rather than all 6?
3. Should Reddit and Walmart be replaced immediately?
4. Should the remaining sample expansion prioritize more banner-present
   replacements before broadening to the optional 80+ tracker?

## Advisor Response, 2026-06-05

Dr. Singh replied that the RQ1/RQ2 framing is on track, no-banner cases should
be treated as contrast cases, and a deeper analysis of fewer sites is
appropriate at this stage as long as the project can scale later.

Operational implications:

- Keep RQ1 scoring and RQ2 longitudinal capture/versioning as the paper spine.
- Treat clean repeated no-banner observations as contrast cases rather than
  failures or automatic replacements.
- Keep the SSRP paper centered on a roughly 20-site deep sample.
- Use Qiyao's 80-ish prior site set as a scaling pool / broad dynamic tracker,
  not as the immediate deep-analysis sample.
- Continue replacing access-friction rows that are not clean no-banner
  observations, especially Reddit and Walmart unless a later capture proves
  otherwise.

## Conservative Working Default

Use `data/week2_deep_sample_targets_2026-06-06.csv` as the next weekly capture
input. Treat the 8 CMP decision-draft rows as advisor-review material, not as
locked sample decisions.
