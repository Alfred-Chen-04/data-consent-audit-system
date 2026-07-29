# Longitudinal Presentation and Poster Delivery, 2026-07-29

## Current Artifacts

| Artifact | Size | SHA-256 |
|---|---:|---|
| `presentation/ssrp_consent_longitudinal_presentation_2026-07-29.pptx` | 1,277,329 bytes | `5f772542b007ee02d6f892a11cf97b5b1ab4fef18902de04ea508bada68bc63d` |
| `presentation/ssrp_consent_longitudinal_presentation_2026-07-29_montage.png` | 313,327 bytes | `5ae1281133e2429d83484fb2aa685295251e1a17dddb9c7951f61cea01a45993` |
| `poster/ssrp_consent_longitudinal_poster_2026-07-29.pptx` | 979,238 bytes | `c528f9f6f4671a6f32072d2067b2254b486f0fa2d4775c65eeb44995971fac8b` |
| `poster/ssrp_consent_longitudinal_poster_2026-07-29.pdf` | 736,601 bytes | `617a25560063fc1b8432889b7bccfcbcc99c93b7941069280765b289f6e85975` |
| `poster/ssrp_consent_longitudinal_poster_2026-07-29.png` | 1,292,276 bytes | `1a6c3ce908687c7119ae3b2c329d3eb5928b23f1c753930b32d6db0dc329704a` |

## Story Applied

- The title and opening claim now foreground longitudinal evolution.
- RQ1 is presented as the repeatable measurement and RQ2 as the matched time
  series.
- Improvement, regression, mixed change, stability, and insufficient evidence
  are operationally defined.
- The analysis denominator is five sites and one matched May 29-June 5
  interval, not 42 reports or 20 summaries.
- The Guardian and Coca-Cola appear as paired evidence. Their raw alerts are
  separated from directional findings.
- CNN, Booking.com, and NerdWallet remain repeated no-visible-first-screen
  contexts rather than banner-path failures.
- The conclusion states that the method is feasible but no sampled site can yet
  be called improved or regressed.

## CWRU Alignment

The poster contains an explicit question, method, results, conclusion, future
research, and source trail, with a left-to-right reading path. The presentation
uses assertion titles, large figures, sparse slide-level copy, page numbers,
and source notes. The 48 x 36 poster fits the official 40 x 60 board option.
The registered board option still needs confirmation before printing.

## Verification

- Presentation: 10/10 slides rendered and visually inspected at full size.
- Presentation: `slides_test.py` reports no overflow.
- Poster: editable PPTX and artifact-tool PNG visually inspected.
- Poster: `slides_test.py` reports no overflow.
- PDF: Poppler render visually inspected with no clipping or font substitution.
- PDF: one page, 3456 x 2592 points = 48 x 36 inches.
- Source notes: `[Sources]` blocks are present in the deck and poster notes.

The machine-readable QA record is
`data/longitudinal_revision_qa_2026-07-29.csv`. The dedicated 13-file inventory
is `data/longitudinal_artifact_manifest_2026-07-29.json`. A verified backup is
stored outside the repository at
`/Users/alfred/Documents/data consent audit system/backup/ssrp_consent_longitudinal_closeout_2026-07-29.zip`,
with a neighboring `.sha256` file. Only live rehearsal and registered board-size
confirmation remain pending.
