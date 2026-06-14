# Full Project Audit, 2026-06-15

## Purpose

This audit reviews the current project state from the evidence that exists in
the repository. It separates current facts from historical drafts and records
the fixes made on 2026-06-15.

## Evidence Checked

| Evidence | Current fact |
|---|---|
| `git status --short --branch` | Branch is `codex/ssrp-plan-mvp` and was clean before this audit edit. |
| `git log --oneline -5` | Latest committed work before this audit was `3d6feb9 Record June 14 capture attempt audit`. |
| `consent-audit research-status` | Week 2 sanity `ready`, cycle `completed`, 42 audit reports, 20 longitudinal summaries, 8 CMP confirmations pending. |
| `docs/research/june14_capture_attempt_audit_2026-06-14.md` | Week 3 continuity capture was attempted but failed 0/5 at browser navigation; no new RQ1/RQ2 result should be inferred. |
| `data/week3_continuity_targets_2026-06-13.csv` | Prepared current-five continuity target list validates as 5 active sites. |
| `docs/research/week2_checkin_index_2026-06-06.md` | Current advisor entrypoint links the June 14 failure audit and June 13 capture decision packet. |
| `docs/research/ssrp_results_tables_2026-06-06.md` | Current paper-facing RQ1/RQ2 tables still reflect Week 2 evidence, not a Week 3 update. |
| Full pytest run | Sandboxed run failed only because local HTTP-server tests could not bind `127.0.0.1`; rerun with appropriate local permissions passed 221 tests. |

## Current Truth Snapshot

- The project remains a consent-interface audit for SSRP with two research
  questions: RQ1 consent-interface scoring and RQ2 longitudinal capture.
- The valid evidence package is still the completed Week 2 gate.
- Current valid package counts are 42 audit reports and 20 longitudinal
  summaries.
- The current five-site Week 2 evidence split is:
  - banner-present manual-review cases: The Guardian and Coca-Cola;
  - no-visible-banner contrast candidates: CNN, Booking.com, and NerdWallet.
- The June 14 Week 3 continuity capture attempt failed at browser navigation
  across all five targets and produced no valid screenshot/DOM observations.
- The June 14 failure should not be interpreted as site behavior, consent
  interface change, no-banner evidence, or pathway availability evidence.
- The 8 CMP/manual-review rows are still pending and should not be silently
  applied to sample-lock decisions.
- The next advisor-facing question is now broader than "should we run June 13":
  it should include how to handle the failed June 14 capture and whether to
  rerun after a one-site browser smoke.

## Problems Found On 2026-06-15

| Problem | Why it matters | Fix |
|---|---|---|
| README still pointed to the June 6 post-capture email as the current advisor email. | It could cause an outdated email to be sent instead of the current June 15 version. | Updated README to point to the June 15 advisor email and latest check-in index. |
| SCHEMA status date stopped at 2026-06-10. | The navigator did not mention the June 13 target list or June 14 failed capture evidence audit. | Updated SCHEMA current-state wording and execution order. |
| The operational next step still read like the next work was simply Week 2 / sample review. | After the failed Week 3 attempt, the immediate action should be advisor review plus a controlled rerun decision. | Added June 14 failure handling and one-site smoke recommendation. |
| The June 11 advisor email was still phrased around "next weekly capture around June 13." | That date has passed and a real attempt failed on June 14. | Added a new June 15 sendable email draft. |

## Verification Notes

- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status`
  still reports 42 audit reports, 20 longitudinal summaries, sanity `ready`,
  and cycle `completed`.
- Targeted research artifact/status tests passed: 31 tests.
- Full test suite first failed in the sandbox on four
  `tests/capture/test_capture_site_integration.py` tests because
  `ThreadingHTTPServer(("127.0.0.1", 0), ...)` could not bind a local port
  (`PermissionError: [Errno 1] Operation not permitted`).
- The same full test command passed after rerunning with local-port permission:
  `221 passed in 16.89s`.

## Current Safe Claims

- "The Week 2 evidence gate is complete and sanity is ready."
- "The current valid research package contains 42 audit reports and 20
  longitudinal summaries."
- "The current evidence split is two banner-present manual-review cases and
  three no-visible-banner contrast candidates."
- "The June 14 Week 3 continuity capture was attempted but failed 0/5 at
  browser navigation, so it should not be used as a consent-interface result."
- "A follow-up capture should start with a one-site browser smoke or a rerun
  after the browser/network context is stable."

## Unsafe Claims

- "Week 3 evidence was successfully captured."
- "The June 14 run proves the five sites changed their consent interfaces."
- "The June 14 run proves all five sites were unreachable."
- "CNN, Booking.com, and NerdWallet are banner-path failures."
- "Coca-Cola is currently Compliant based on the latest Week 2 capture."
- "The final SSRP dataset is complete."

## Recommended Next Action

Send the June 15 advisor email, then wait for decisions on:

1. no-visible-banner table representation;
2. whether to rerun the current five after a one-site browser smoke;
3. whether to expand toward ~20 sites before or after resolving the current
   five evidence cards;
4. whether to resolve the 8 CMP/manual-review pending rows now or keep them as
   secondary candidates.
