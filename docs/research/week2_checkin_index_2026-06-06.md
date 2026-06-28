# Week 2 Advisor Check-in Index, 2026-06-06

Use this index as the first file for advisor check-ins.

## Status

- Week 2 sanity status: `ready`
- Audit reports in package: 42
- Longitudinal summaries in package: 20
- CMP review state: pending advisor confirmation

## Read First

- [Today work note, 2026-06-28](today_work_note_2026-06-28.md)
- [Recent task fact audit, 2026-06-28](recent_task_fact_audit_2026-06-28.md)
- [Advisor decision-gate email, 2026-06-28](advisor_email_decision_gate_2026-06-28.md)
- [Today work note, 2026-06-27](today_work_note_2026-06-27.md)
- [Today work note, 2026-06-26](today_work_note_2026-06-26.md)
- [Today work note, 2026-06-25](today_work_note_2026-06-25.md)
- [Today work note, 2026-06-22](today_work_note_2026-06-22.md)
- [Today work note, 2026-06-20](today_work_note_2026-06-20.md)
- [Today work note, 2026-06-18](today_work_note_2026-06-18.md)
- [Current-five advisor decision email, 2026-06-19](advisor_email_current_five_decision_2026-06-19.md)
- [Current-five evidence packet, 2026-06-19](current_five_evidence_packet_2026-06-19.md)
- [June 15 Coca-Cola smoke capture audit, 2026-06-15](june15_coca_cola_smoke_audit_2026-06-15.md)
- [Latest advisor email draft, 2026-06-15](advisor_email_latest_2026-06-15.md)
- [Full project audit, 2026-06-15](full_project_audit_2026-06-15.md)
- [June 14 capture attempt audit, 2026-06-14](june14_capture_attempt_audit_2026-06-14.md)
- [June 13 capture decision packet, 2026-06-13](june13_capture_decision_packet_2026-06-13.md)
- [Advisor email review questions, 2026-06-11](advisor_email_review_questions_2026-06-11.md)
- [Today work note, 2026-06-11](today_work_note_2026-06-11.md)
- [Week 2 evidence cards, 2026-06-11](week2_evidence_cards_2026-06-11.md)
- [Latest advisor email draft, 2026-06-10](advisor_email_latest_update_2026-06-10.md)
- [Week 2 manual evidence review notes, 2026-06-10](week2_manual_evidence_review_notes_2026-06-10.md)
- [Full project fact audit, 2026-06-10](full_project_fact_audit_2026-06-10.md)
- [Today work note, 2026-06-10](today_work_note_2026-06-10.md)
- [Evidence-based next-step advisor email, 2026-06-09](advisor_email_evidence_based_next_steps_2026-06-09.md)
- [Recent work evidence audit, 2026-06-09](recent_work_evidence_audit_2026-06-09.md)
- [Today work note, 2026-06-09](today_work_note_2026-06-09.md)
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
- [Week 2 manual evidence review worksheet](../../data/week2_manual_evidence_review_2026-06-10.csv)
- [Current-five decision sheet](../../data/current_five_decision_sheet_2026-06-19.csv)

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
