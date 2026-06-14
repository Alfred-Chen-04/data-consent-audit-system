# June 14 Capture Attempt Audit

## Purpose

This note records the 2026-06-14 Week 3 continuity capture attempt and the
evidence that should be used to interpret it. The attempt was real, but it did
not produce valid new consent-interface observations.

## Starting Evidence

Before the attempt:

- Git branch was clean and synced with `origin/codex/ssrp-plan-mvp`.
- Latest committed work was `e5d0edd Add June 13 capture decision packet`.
- The prepared Week 3 target list validated successfully:
  `data/week3_continuity_targets_2026-06-13.csv`
- `validate-sites` result:
  `5 active sites; mentor_inherited=0; categories: finance=1, food=1, news=2, travel=1`
- `research-status` reported:
  - Week 2 targets: 5
  - sanity: `ready`
  - cycle: `completed`
  - audit reports: 42
  - longitudinal summaries: 20
  - CMP confirmations pending: 8

## Command Attempted

```bash
AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m consent_audit.cli weekly \
  --sites-csv data/week3_continuity_targets_2026-06-13.csv \
  --consent-table-path data/consent_table_pilot_2026-05-30.csv \
  --cohort week3-2026-06-13
```

## Result

The weekly command completed as a failed run:

```text
Completed weekly audit (attempted=5/5, succeeded=0, failed=5, budget_exceeded=false)
```

Site-level browser navigation failures:

| Site | Browser failure |
|---|---|
| The Guardian | `Page.goto: net::ERR_TIMED_OUT` |
| CNN | `Page.goto: net::ERR_CONNECTION_CLOSED` |
| Booking.com | `Page.goto: net::ERR_TIMED_OUT` |
| NerdWallet | `Page.goto: Timeout 40000ms exceeded` |
| Coca-Cola | `Page.goto: net::ERR_TIMED_OUT` |

## Artifact Check

The failed browser attempt did not add valid consent-table rows and did not
change the research package counts.

Post-attempt checks:

- `data/consent_table_pilot_2026-05-30.csv` still ends with the Week 2
  `week2-2026-06-06` rows.
- `research-status` still reports 42 audit reports and 20 longitudinal
  summaries.
- Five timestamped capture directories were created, but each was empty
  (`0B`) and had no `layer1.png` or `layer1.html` file:
  - `data/captures/sites/www_theguardian_com_20260614_135848`
  - `data/captures/sites/www_cnn_com_20260614_135920`
  - `data/captures/sites/www_booking_com_20260614_135952`
  - `data/captures/sites/www_nerdwallet_com_20260614_140022`
  - `data/captures/sites/www_coca_cola_com_20260614_140103`

Because those directories contain no screenshot or DOM files, they are not
valid interface evidence.

## HTTP Connectivity Cross-Check

A light `curl -I -L --max-time 15` check was run after the browser failure.
This was not a consent-interface capture; it was only a connectivity check.

| Site | HTTP check result |
|---|---|
| The Guardian | Timed out after 15 seconds |
| CNN | Returned `302` then `200` from `edition.cnn.com` |
| Booking.com | Returned `202` |
| NerdWallet | Returned `200` |
| Coca-Cola | Returned `200` |

Interpretation: the failed weekly capture should not be described as all five
sites being unreachable. A more precise statement is that Playwright/browser
navigation failed across all five targets in the current run context, while
basic HTTP checks succeeded for four of the five sites.

## Research Interpretation

This attempt is evidence of a failed capture environment, not evidence about
the consent interfaces themselves.

Do not add a Week 3 RQ1/RQ2 result from this run.
Do not claim the sites changed their consent interfaces.
Do not infer no-banner, banner-present, or pathway availability from this
failed attempt.

## Next Action

The next useful action is to rerun the Week 3 continuity capture only after the
browser/network context is healthier, or to run a very small one-site browser
smoke first. If rerunning, keep the same target list unless the advisor has
changed the sample rule:

`data/week3_continuity_targets_2026-06-13.csv`
