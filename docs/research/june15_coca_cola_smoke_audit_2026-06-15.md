# June 15 Coca-Cola Smoke Capture Audit

## Purpose

This note records the controlled one-site browser smoke run after the June 14
Week 3 continuity capture failed 0/5 at browser navigation. The goal was to
test whether the browser capture environment could produce a real screenshot
and DOM bundle again before rerunning the current five-site continuity list.

## Command

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli audit \
  https://www.coca-cola.com/us/en \
  --no-save \
  --consent-table-path data/smoke_coca_cola_2026-06-15.csv \
  --cohort smoke-2026-06-15
```

`--no-save` was used deliberately. This smoke run wrote a capture bundle and a
separate smoke consent-table row, but it did not append a new `AuditReport` to
the main research package.

## Artifacts

| Artifact | Path |
|---|---|
| Smoke consent table | `data/smoke_coca_cola_2026-06-15.csv` |
| Screenshot | `data/captures/sites/www_coca_cola_com_20260615_043524/layer1.png` |
| Local raw DOM snapshot | `data/captures/sites/www_coca_cola_com_20260615_043524/layer1.html` |
| Synced DOM evidence excerpt | `data/smoke_coca_cola_2026-06-15_dom_evidence.csv` |

The smoke CSV row records:

- `banner_detected=true`
- `accept_available=false`
- `reject_available=false`
- `customize_available=false`
- `dismiss_available=false`
- `layer1_gate_passed=false`
- `tier=High-Risk`
- DOM hash `3eb099b02052ca9db95162a116380a4539d9d0e9c78966726eb88d9119bb9e85`
- image hash `ff1818181c1c3fff:5f048dfed57fd08d`

## Manual Evidence Check

Manual review of the screenshot and DOM contradicts the automated path
booleans. The capture itself succeeded and shows a visible OneTrust Privacy
Preference Center.

Visible / DOM-confirmed controls include:

| Evidence | Interpretation |
|---|---|
| `Privacy Preference Center` | Consent preference modal is visible. |
| `Allow All` | Accept-like path is present. |
| `Reject All` | Reject-like path is present. |
| `Confirm My Choices` | Save/customize-like path is present. |
| Category toggles for analytics, advertising, personalization, and social media cookies | Per-category preference controls are present. |

Relevant DOM evidence appears in the local `layer1.html`, including OneTrust
controls with `accept-recommended-btn-handler`, `ot-pc-refuse-all-handler`, and
`save-preference-btn-handler`. A compact synced excerpt is saved at
`data/smoke_coca_cola_2026-06-15_dom_evidence.csv` so the key evidence is
available without committing the full raw webpage HTML.

## Interpretation

This smoke run is useful evidence about the capture environment, not a final
RQ1 score.

- The browser/capture context is no longer globally failing: it produced a real
  screenshot and DOM snapshot for Coca-Cola.
- The automated Layer 1 extraction missed visible OneTrust preference-center
  controls in this run.
- The automated `High-Risk` row should therefore not be used as a final Coca-Cola
  RQ1 result without manual correction or an extraction fix.
- A full current-five Week 3 continuity rerun should wait until this
  OneTrust/control-recognition issue is handled, otherwise the pipeline may
  generate traceable but misleading path-availability rows.

## Initial Recommended Next Action

This was the recommendation immediately after the first smoke run. It is now
superseded by the post-fix verification below.

Before rerunning the five-site continuity list, do one of these:

1. Add a regression/fix so OneTrust preference-center controls such as
   `Allow All`, `Reject All`, and `Confirm My Choices` are counted correctly by
   Layer 1.
2. Or switch this week's continuity work to a semi-automated protocol: capture
   screenshots/DOM, then manually validate path booleans in an evidence card
   before treating the rows as RQ1/RQ2 evidence.

The second option is enough for the SSRP paper if automation remains unstable,
as long as every score has a screenshot/DOM/table evidence trail.

## Post-Fix Verification

After the initial smoke exposed the OneTrust recognition gap, the capture-agent
pathway logic was updated in two places:

- OneTrust labels now map correctly: `Confirm My Choices` / `Save my choices`
  are treated as customize-like controls, `Close preference center` is treated
  as a dismiss-like control, and the non-action title `Privacy Preference
  Center` is not treated as a pathway.
- Browser click replay now waits for delayed CMP controls and can click buttons
  by accessible name, which is needed for aria-labeled close buttons.

The follow-up smoke command was:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli audit \
  https://www.coca-cola.com/us/en \
  --no-save \
  --consent-table-path data/smoke_coca_cola_postfix_2026-06-15.csv \
  --cohort smoke-postfix-2026-06-15
```

Post-fix artifacts:

| Artifact | Path |
|---|---|
| Post-fix smoke consent table | `data/smoke_coca_cola_postfix_2026-06-15.csv` |
| Post-fix screenshot | `data/captures/sites/www_coca_cola_com_20260615_051240/layer1.png` |
| Local raw DOM snapshot | `data/captures/sites/www_coca_cola_com_20260615_051240/layer1.html` |
| Synced DOM evidence excerpt | `data/smoke_coca_cola_postfix_2026-06-15_dom_evidence.csv` |

Post-fix result:

- `banner_detected=true`
- `accept_available=true`
- `reject_available=true`
- `customize_available=true`
- `dismiss_available=true`
- `layer1_gate_passed=true`
- `layer2_overall_category=Easy`
- `transparency_grade=B`
- `unbiased_choice_grade=A`
- `tier=Exemplary`

Interpretation: the immediate OneTrust pathway-recognition blocker is resolved
for the Coca-Cola smoke case. This does not finalize the whole Week 3 dataset,
but it supersedes the initial recommendation to fix OneTrust recognition before
rerunning. The next current-five rerun is technically more defensible than it
was after the June 14 failure and the first June 15 smoke, if it still matches
the advisor/sample plan.
