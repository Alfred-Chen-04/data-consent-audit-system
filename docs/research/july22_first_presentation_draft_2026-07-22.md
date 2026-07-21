# July 22 First Presentation Draft, 2026-07-22

## Output

The first independent SSRP presentation draft now exists:

- Editable deck: `docs/research/presentation/ssrp_consent_audit_presentation_draft_2026-07-22.pptx`
- Rendered overview: `docs/research/presentation/ssrp_consent_audit_presentation_draft_2026-07-22_montage.png`
- Content/source map: `docs/research/july22_presentation_content_plan_2026-07-22.md`

This is a review draft, not the final presentation.

## What The Deck Contains

- 10 widescreen slides.
- The original RQ1/RQ2 project spine.
- An explicit current-runtime boundary: Playwright plus deterministic scoring,
  exports, diffing, and local persistence.
- The verified pilot counts: 5 targets, 42 audit-report rows, 20 longitudinal
  summary rows, 326 tracked screenshots, and 0 synced referenced raw HTML files.
- Guardian and Coca-Cola banner-present evidence cards.
- CNN, Booking.com, and NerdWallet no-visible-first-screen-banner contrasts.
- An RQ2 timeline that stops at the latest exported `week_of`, June 6, 2026.
- A 16-day July 22-August 7 closeout action slide.

## Evidence And Claim Boundary

The draft uses only the five stored 1440 x 900 screenshots listed in the July
9 asset manifest. It adds no browser capture, new site observation, advisor
decision, score, or legal judgment.

The deck intentionally does not display the automated 40 High-Risk / 2
Compliant split because the no-visible-banner coding rule remains unresolved.
It also does not claim active LLM/VLM calls, PostgreSQL/R2, APScheduler,
per-report PDF generation, raw-DOM sync, continuous July tracking, or a final
20-site sample.

## QA Performed

1. Rendered every slide from the artifact source and inspected all 10 at full
   size.
2. Ran the presentation overflow checker: `Test passed. No overflow detected.`
3. Rendered the final PPTX itself through LibreOffice/Poppler at approximately
   1600 x 900 and inspected all 10 resulting slides at full size.
4. Fixed three first-pass issues: a cover callout overflow, four title/rule
   collisions, and a Layer 3 heading/body overlap.
5. Fixed a final-PPTX-only title clipping issue on slide 4 and rerendered the
   PPTX successfully.
6. Confirmed the PPTX contains 10 slide XML files and 5 embedded media files.

No clipping, unintended overlap, broken glyph, missing screenshot, or
unresolved placeholder remained in the final reviewed render.

Repository verification after the documentation/status corrections also
passed: 245 tests, Ruff, Mypy across 61 source files, `git diff --check`, and
161 current-entrypoint local links with 0 missing.

## File Verification

| File | Bytes | SHA-256 |
|---|---:|---|
| `ssrp_consent_audit_presentation_draft_2026-07-22.pptx` | 1,645,523 | `607ab0791f0062c91ec52090d5b598d936f7de2d033de04af5fe49fb368bcd1a` |
| `ssrp_consent_audit_presentation_draft_2026-07-22_montage.png` | 360,887 | `ae25bd0bde2d68f5aace2a5d5d58a5be16c61b8ef2fdef376065ab74af99ebb6` |

## Remaining Review Gate

Before calling the deck final:

1. confirm or visibly carry the five poster-review decisions;
2. align any revised poster wording with the deck;
3. rehearse the spoken explanation and shorten any slide that needs less copy;
4. rerun content, render, link, test, and hash verification after the final edit.
