# Week 2 Advisor Check-in Index, 2026-06-06

Use this index as the first file for advisor check-ins.

## Status

- Week 2 sanity status: `ready`
- Audit reports in package: 42
- Longitudinal summaries in package: 20
- CMP review state: pending advisor confirmation

## Read First

- [Advisor update](week2_advisor_update_2026-06-06.md)
- [Sanity check](week2_sanity_check_2026-06-06.md)
- [Capture checklist](week2_capture_day_checklist_2026-06-06.md)
- [Cycle report](week2_cycle_report_2026-06-06.md)
- [Execution runbook](week2_execution_runbook_2026-06-06.md)
- [Week 2 sample plan](week2_sample_plan_2026-05-30.md)

## Data Package

- [Research package](../../data/research_package)
- [Research manifest](../../data/research_package/research_manifest.json)
- [Audit report summary](../../data/research_package/audit_report_summary.csv)
- [Longitudinal summary](../../data/research_package/longitudinal_summary.csv)

## Manual Review

- [CMP confirmation sheet](../../data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv)
- [CMP evidence packet](../../data/cmp_review_packet_pilot_2026-05-30/index.html)

## Run Controls

- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-preflight-check`
- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-cycle --dry-run`
- `AGENT_SITE_TIMEOUT=40 PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-cycle`
- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-refresh-outputs`
- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-capture-checklist`
- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli export-research-package`
- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli advisor-update-brief`
- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-sanity-check`
- `PYTHONPATH=src .venv/bin/python -m consent_audit.cli checkin-index`
