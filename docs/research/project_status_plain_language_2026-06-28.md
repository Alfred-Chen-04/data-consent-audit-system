# Project Status Plain-Language Handoff, 2026-06-28

## One-Sentence Status

This project currently has a working research scaffold, a real five-site Week 2
evidence gate, synced screenshots, generated RQ1/RQ2 tables, and paper/poster
drafting artifacts. It is not a finished SSRP paper, not a final 20-site
dataset, and not a SOC 2 audit product.

## What I Checked

This handoff is based on current repo state, not memory:

- GitHub PR #7 is merged into `main` at merge commit
  `28ee83755bc1eb379b08a8941ebad146d9c8fd45`.
- `consent-audit research-status` reports 5 Week 2 targets, sanity `ready`,
  cycle `completed`, 42 audit reports, 20 longitudinal summaries, and 8
  pending CMP confirmations.
- `data/reports/audit_reports.jsonl` exists with 42 report rows.
- `data/reports/weekly_summaries.jsonl` exists with 20 summary rows.
- `data/research_package/audit_report_summary.csv` exists with 42 rows.
- `data/research_package/longitudinal_summary.csv` exists with 20 rows.
- `data/current_five_decision_sheet_2026-06-19.csv` has 7 blank
  `confirmed_decision` cells.
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` has 8 rows, all
  still `pending`.
- `data/captures/sites` has 326 tracked `layer1.png` screenshot files.
- The current checkout has 0 synced `layer1.html` files. The `.gitignore`
  tracks screenshot PNGs but excludes raw capture HTML files.

## Where The Evidence Is

Start with these files:

- Overall status: `README.md`
- Advisor/research index: `docs/research/week2_checkin_index_2026-06-06.md`
- Recent fact audit: `docs/research/recent_task_fact_audit_2026-06-28.md`
- Current-five evidence packet:
  `docs/research/current_five_evidence_packet_2026-06-19.md`
- Current-five decision sheet:
  `data/current_five_decision_sheet_2026-06-19.csv`
- Advisor email draft:
  `docs/research/advisor_email_decision_gate_2026-06-28.md`

Current-five screenshot evidence:

| Site | Screenshot | Current visual reading |
|---|---|---|
| The Guardian | `data/captures/sites/www_theguardian_com_20260605_160209/layer1.png` | Visible consent choice page with accept, reject-like, and manage-cookies controls. |
| Coca-Cola | `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png` | Visible Privacy Preference Center with Allow All, Confirm My Choices, Reject All, and toggles. |
| CNN | `data/captures/sites/www_cnn_com_20260605_160221/layer1.png` | CNN homepage; no visible first-screen cookie banner. |
| Booking.com | `data/captures/sites/www_booking_com_20260605_160226/layer1.png` | Booking search homepage; no visible first-screen cookie banner. |
| NerdWallet | `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png` | NerdWallet homepage/product cards; no visible first-screen cookie banner. |

Important DOM caveat:

- CSVs and generated reports still contain DOM hashes and historical
  `layer1.html` reference strings.
- The actual raw `.html` snapshot files are not present in this Git checkout.
- Therefore, use screenshot files, DOM hashes, JSONL reports, and CSV exports
  as the synced evidence. Do not tell the advisor that local raw HTML files are
  currently synced unless those HTML files are restored or recaptured.

## What Has Actually Been Done

The useful work falls into five buckets:

1. Research direction was narrowed: RQ1 is consent-interface scoring, RQ2 is
   longitudinal capture/versioning. AI is a method, not a separate RQ.
2. The codebase now has a working audit pipeline: capture, Layer 1/2/3 scoring
   fallbacks, JSONL report storage, weekly summaries, CSV exports, research
   package export, and CLI status commands.
3. Week 2 produced a real five-site evidence gate: The Guardian, CNN,
   Booking.com, NerdWallet, and Coca-Cola.
4. Paper/poster scaffolding exists: results tables, paper skeleton, writing
   pack, claim register, figure plan, and poster plan.
5. Recent work has mostly been cleanup and decision-gating: checking facts,
   preparing advisor emails, recording PR status, and preventing blind new
   captures before the sample decisions are recorded.

## What Is Messy Or Easy To Misread

- Some older docs are historical and stale. Use this handoff, README,
  `week2_checkin_index`, and `recent_task_fact_audit_2026-06-28` as current
  entrypoints.
- Several CSV/docs list `layer1.html` paths, but those raw HTML files are not
  synced in the current checkout. This is the main evidence-location mismatch.
- CNN, Booking.com, and NerdWallet are not hidden cookie-option examples. Their
  Week 2 screenshots show no visible first-screen consent banner. Treat them as
  no-visible-banner contrast cases unless Dr. Singh chooses another table rule.
- The Week 2 automated tier `High-Risk` should not be used alone as the final
  human interpretation for all five sites. Guardian and Coca-Cola need manual
  validation because the screenshots show controls that the automated fields did
  not fully capture.
- The 42 audit reports and 20 longitudinal summaries are current evidence, not
  the final SSRP dataset.

## What Is Not Done Yet

- The 20-site deep sample is not locked.
- The final SSRP paper is not written.
- The poster is not final.
- The demo/evidence browser is not final.
- The current-five decision sheet is still blank.
- The 8 CMP/manual-review confirmation rows are still pending.
- The June 14 Week 3 capture attempt failed and did not create valid new
  consent-interface observations.

## What To Ask Dr. Singh Next

Use `docs/research/advisor_email_decision_gate_2026-06-28.md` as the email
draft. The concrete questions are:

1. For the current five sites, should we treat Guardian and Coca-Cola as
   banner-present evidence cards, and CNN/Booking/NerdWallet as contrast cases?
2. Should no-visible-banner rows stay in the main RQ1 table, move to a separate
   contrast table, or be capped as limitations evidence?
3. Should the next work be a current-five rerun, manual validation/reporting, or
   expansion toward about 20 deep sites?
4. When should the next working session happen, and what should be prepared for
   that session?

## Daily Routine

You do not need to run a new browser capture every day.

On a normal project day, run only:

```bash
cd "/Users/alfred/Documents/data consent audit system/repo"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /Users/alfred/Desktop/data-consent-audit-system/.venv/bin/python -m consent_audit.cli research-status
```

Run tests when code or generated artifact logic changes:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /Users/alfred/Desktop/data-consent-audit-system/.venv/bin/python -m pytest tests/test_research_artifacts.py tests/test_research_status.py -q -p no:cacheprovider
```

Run live capture only after the target list and decision rule are clear.
