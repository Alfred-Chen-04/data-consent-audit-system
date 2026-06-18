# Today Work Note, 2026-06-18

## Bottom Line

Today is a fact-check and decision-setup day, not a blind browser-capture day.

Current verified facts:

- GitHub PR #4, `[codex] Clarify June 15 post-fix audit guidance`, is merged
  into `main`.
- `research-status` still reports Week 2 sanity `ready`, cycle capture
  `completed`, 42 audit reports, 20 longitudinal summaries, and
  `pending=8` CMP confirmations.
- The valid evidence package remains the completed Week 2 gate.
- The June 14 Week 3 capture attempt remains a browser-navigation failure
  record, not consent-interface evidence.
- The June 15 post-fix Coca-Cola smoke remains a technical verification that
  the OneTrust pathway-recognition blocker was resolved for that smoke case.

No new advisor response or sample-lock decision is recorded in the repository
as of this note.

## What Was Checked Today

Commands / sources checked:

```bash
git status -sb
git log --oneline --decorate -8
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

External GitHub state checked:

- PR #4 is `merged=true`, with merge commit
  `428394fa7e52d9f007737a123ace5ed6e1a7b13b`.

Repository evidence checked:

- `README.md`
- `SCHEMA.md`
- `docs/research/week2_checkin_index_2026-06-06.md`
- `docs/research/advisor_email_latest_2026-06-15.md`
- `docs/research/full_project_audit_2026-06-15.md`
- `docs/research/june15_coca_cola_smoke_audit_2026-06-15.md`

## What Can Be Done Today

1. Use this note and the latest advisor email as the current project handoff.
2. If contacting Dr. Singh, use
   `docs/research/advisor_email_latest_2026-06-15.md` as the starting point.
3. If doing research work without an advisor reply, prepare evidence cards or
   manual-validation notes from existing screenshots/DOM instead of rerunning a
   full capture.
4. Do not treat the 8 CMP/manual-review rows as locked sample decisions until
   the confirmation sheet is filled by a human/advisor.
5. Do not claim Week 3 continuity evidence exists until a successful new
   current-five run or a documented semi-automated validation pass exists.

## Do Not Do Blindly

- Do not rerun the full current-five capture just because the calendar advanced.
- Do not expand to ~20 sites before deciding how no-visible-banner rows should
  appear in the RQ1 table.
- Do not change paper/poster claims from the Week 2 evidence gate unless new
  evidence is captured and the research package is refreshed.

## Next Decision

The next real decision is still:

Should the project prioritize a post-fix current-five continuity rerun, or
should it first write manual evidence cards and then expand toward the roughly
20-site deep sample?

The repository currently supports either path, but it does not prove which path
the advisor/user has chosen.
