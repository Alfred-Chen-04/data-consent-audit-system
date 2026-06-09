# Week 2 Capture-Day Checklist, 2026-06-06

Use this checklist when running the weekly capture cycle.

## Current State

- Week of: 2026-06-06
- Cohort: `week2-2026-06-06`
- Expected targets: 5
- Preflight status: `ready_for_capture`
- Sanity status: `ready`
- Last cycle mode: `live_capture`
- Last capture status: `completed`
- Last capture attempts: 5/5

## Evidence Links

- [Week 2 targets](../../data/week2_deep_sample_targets_2026-06-06.csv)
- [Consent table](../../data/consent_table_pilot_2026-05-30.csv)
- [Preflight check](week2_preflight_check_2026-06-06.md)
- [Cycle report](week2_cycle_report_2026-06-06.md)
- [Refresh report](week2_refresh_report_2026-06-06.md)
- [Sanity check](week2_sanity_check_2026-06-06.md)
- [Check-in index](week2_checkin_index_2026-06-06.md)
- [Advisor update](week2_advisor_update_2026-06-06.md)

## Run Checklist

- [ ] Open the check-in index and confirm the target list and cohort.
- [ ] Run `PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-preflight-check`.
- [ ] Confirm preflight status is `ready_for_capture` or record a force rationale.
- [ ] Run `PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-cycle --dry-run`.
- [ ] Read the cycle report `Next Action` before live capture.
- [ ] Run `AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-cycle`.
- [ ] Run `PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-refresh-outputs` if the live cycle did not reach refresh.
- [ ] Confirm every target has screenshot, DOM, hash, and report evidence.
- [ ] Confirm Week 2 sanity status is `ready` before treating capture complete.
