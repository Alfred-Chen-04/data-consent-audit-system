# July 21 Poster Review Bundle, 2026-07-21

Purpose: package the existing verified poster-review materials into one
advisor-facing ZIP with an internal manifest and integrity checks. This work
adds no browser capture, site observation, score, consent-interface judgment,
or confirmed advisor decision.

## Why This Is Today's Planned Work

The branch and PR head were synchronized at the start of 2026-07-21, and the
research dashboard remained unchanged at 5 Week 2 targets, 42 audit reports,
20 longitudinal summaries, and 8 pending CMP confirmations.

Structured reads also showed no new human input:

- Poster-review sheet: 5 pending rows and 5 blank confirmed decisions.
- Current-five sheet: 7 blank confirmed decisions.
- CMP/manual-review sheet: 8 pending confirmations and 8 blank confirmed
  decisions.

Those facts do not support a stronger poster revision or new empirical claim.
The current plan calls for advisor review, so consolidating the already
verified review files into a single attachment is the available work that
advances that plan without crossing the decision gate.

## Delivered Bundle

- [Single-file poster review bundle](poster/ssrp_poster_review_bundle_2026-07-21.zip)
- [Bundle README and internal manifest](poster/ssrp_poster_review_bundle_README_2026-07-21.txt)

Final ZIP facts:

- File count: 8.
- ZIP size: 3,973,713 bytes.
- Uncompressed content size: 4,164,478 bytes.
- ZIP SHA-256:
  `4f697275580b0a05cf0197c51493147953d6755c6667fdf8cf970c0734e9de1c`.
- Internal README SHA-256:
  `f3bd8beca4cbcb0607740f1642fcc6a3101475fd48bfc540a3189b5e6a6c37b8`.

## Included Files

1. `ssrp_poster_mockup_2026-07-14.pdf`
2. `ssrp_poster_mockup_2026-07-14.pptx`
3. `ssrp_poster_mockup_2026-07-14.png`
4. `advisor_email_poster_mockup_review_2026-07-14.md`
5. `july15_poster_pdf_and_print_qa_2026-07-15.md`
6. `july16_poster_review_decision_sheet_2026-07-16.md`
7. `poster_review_decision_sheet_2026-07-16.csv`
8. `ssrp_poster_review_bundle_README_2026-07-21.txt`

The archive is flat so the PDF, email, decision CSV, and README are visible
immediately after extraction.

## Verification

- `unzip -t` reported no errors in compressed data.
- The archive contained exactly the eight listed files.
- All eight extracted file hashes matched the corresponding source files or
  the tracked internal README.
- The bundled email includes the single-file ZIP path as the first review-file
  option.
- Calendar check: 53 of 70 core-cycle days, or 75.7%; 17 days remain before
  August 7 and 41 days remain before August 31.

## Decision Gate

The ZIP is a transport artifact only. It does not convert recommendations into
confirmed decisions, make the dataset final, lock a 20-site sample, sync raw
HTML, establish current live-site conditions, or support legal compliance or
non-compliance verdicts.

The next valid action remains: send or share the bundle for advisor review,
then record actual answers in
`data/poster_review_decision_sheet_2026-07-16.csv` before revising claims.
