# July 15 Poster PDF and Print QA, 2026-07-15

Purpose: add a print/review PDF for the already verified July 14 poster mockup
and test the derived file without changing the poster's research content. This
work adds no browser capture, no new site observation, no new scoring result,
and no new consent-interface judgment.

## Why This Was Today's Safe Task

The current research dashboard still reports 5 Week 2 targets, 42 audit reports,
20 longitudinal summaries, and 8 pending CMP confirmations. Structured CSV
reads still show 7 blank current-five decisions and 8 pending CMP/manual review
confirmations. The checkout still contains 326 site `layer1.png` screenshots
and 0 synced site `layer1.html` files.

Those unresolved items require human/advisor decisions. The completed July 14
poster already had an editable PPTX and PNG preview, but no PDF. Exporting and
verifying that PDF advances the planned poster-review workflow without
inventing new evidence or bypassing the decision gate.

## Delivered File

- [Print/review PDF](poster/ssrp_poster_mockup_2026-07-14.pdf)
- Source [editable PPTX](poster/ssrp_poster_mockup_2026-07-14.pptx)
- Existing [PNG preview](poster/ssrp_poster_mockup_2026-07-14.png)

The PDF was exported directly from the source PPTX with LibreOffice Impress.
No visible poster copy, evidence image, score, or claim was edited during the
export.

## Verified Results

- PDF pages: 1.
- PDF page size: 3456 x 2592 points, exactly 48 x 36 inches.
- PDF file size at verification: 840,076 bytes.
- PDF SHA-256:
  `a85539040b7948fcb73dfc54f6c41b743357fcc678a4b7e33cfc45187ab84536`.
- Source PPTX SHA-256:
  `5c55af9e349e166d8c5398817fb4b1f7d7ed4bbe4c35e9b4ca74272d2f87e290`.
- PPTX overflow test: `Test passed. No overflow detected.`
- PDF was rendered back to PNG at 72 dpi and visually inspected at full page.
  No clipping, overlap, black boxes, or broken glyphs were found.
- Extracted PDF text contains the poster title, the 42/20/326 evidence counts,
  the 7 blank current-five decisions, the 8 pending CMP confirmations, and the
  visible statement that this is not a final 20-site dataset.
- After resizing the PDF render to the existing PNG dimensions, the mean
  absolute RGB channel differences were 4.886, 4.774, and 4.576 out of 255.
  The small rasterization difference is consistent with the visually matching
  composition; it is not evidence of a content change.

## Current Calendar and Decision Gate

- Date checked: 2026-07-15.
- Core research window: May 30-August 7, 2026.
- Calendar progress: 47 of 70 core-cycle days, or 67.1%.
- Days left before August 7: 23.
- Days left before August 31: 47.
- Current next action remains advisor review of poster framing, evidence-card
  selection, contrast-case labels, and unresolved decision sheets.

## Claim Boundary

The PDF is a delivery-format derivative of the July 14 pilot/method poster. It
does not make the dataset final, lock a 20-site sample, sync missing raw HTML,
resolve blank review decisions, establish a current live-site state, or support
legal compliance or non-compliance verdicts.
