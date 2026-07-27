# July 22 Presentation Content Plan, 2026-07-22

## Purpose

Build the first independent SSRP presentation from verified pilot evidence.
This plan does not create new observations, resolve pending decisions, or turn
automated labels into final site judgments.

## Audience And Story

Audience: SSRP advisor/review audience.

Story: the project answers two linked questions. RQ1 defines an evidence-linked
three-layer audit for unbiased choice across the full consent pathway. RQ2
defines repeated capture and versioning so interface changes can be documented.
The current artifact is a five-site pilot/method demonstration, not a final
sample-wide result.

## Slide Map

| # | Slide | Visible message | Verified source |
|---:|---|---|---|
| 1 | Title | Traceable Consent Interface Audit and Versioning | Current canonical goal |
| 2 | Two research questions | RQ1 scores pathways; RQ2 captures and versions change | Original proposal RQs and current goal |
| 3 | What runs today | Playwright + deterministic evidence/scoring/diff + local storage | Current source modules and July 22 implementation audit |
| 4 | Three-layer audit | Availability gate -> effort -> transparency and unbiased choice | `CONCEPTS.md` and `SCHEMA.md` |
| 5 | Pilot evidence base | 5 targets, 42 report rows, 20 summaries, 326 screenshots, 0 synced raw HTML | Current CSV/file audit |
| 6 | Evidence card: Guardian | Stored screenshot shows a visible consent-choice screen | Guardian screenshot and current-five packet |
| 7 | Evidence card: Coca-Cola | Stored screenshot shows a visible preference center with consent controls | Coca-Cola screenshot and current-five packet |
| 8 | Contrast cases | CNN, Booking.com, and NerdWallet have no visible first-screen banner in stored screenshots; this is not a failure verdict | Three stored screenshots and current-five packet |
| 9 | What RQ2 currently proves | The pipeline produced pilot summaries through June 6; it does not establish continuous weekly July tracking | Longitudinal export and July 22 audit |
| 10 | Closeout | Finalize decisions, presentation, poster, and evidence package by August 7 | July 22 closeout plan |

## Asset Map

| Site | Role | Screenshot |
|---|---|---|
| The Guardian | Banner-present evidence card | `data/captures/sites/www_theguardian_com_20260605_160209/layer1.png` |
| Coca-Cola | Banner-present evidence card | `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png` |
| CNN | No-visible-banner contrast | `data/captures/sites/www_cnn_com_20260605_160221/layer1.png` |
| Booking.com | No-visible-banner contrast | `data/captures/sites/www_booking_com_20260605_160226/layer1.png` |
| NerdWallet | No-visible-banner contrast | `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png` |

All five files exist, parse as PNG, and are 1440 x 900 in the audited checkout.

## Claim Rules For The Deck

- Say "deterministic pilot runtime," not "AI-powered production system."
- Say "42 report rows" and "20 longitudinal-summary rows," not final sample
  results.
- Say "stored screenshot shows," not "the site currently shows."
- Say "no visible first-screen banner," not "consent failure."
- Say the latest longitudinal export is June 6; do not imply July continuity.
- Say raw DOM refs exist in exports but zero referenced HTML files are synced.
- Do not display the 40 High-Risk / 2 Compliant automated split as a finding.
- Do not state or imply a legal compliance verdict.

## Review Gate

First review output:

- `docs/research/presentation/ssrp_consent_audit_presentation_draft_2026-07-22.pptx`
- `docs/research/presentation/ssrp_consent_audit_presentation_draft_2026-07-22_montage.png`
- `docs/research/july22_first_presentation_draft_2026-07-22.md`

The first draft may be reviewed now. A final deck requires:

1. full-slide render and overflow checks;
2. confirmation that every visible count matches the current checkout;
3. advisor decisions or explicit fallback limitation labels;
4. final evidence-package and link verification.
