# Advisor Response Action Plan, 2026-06-05

This document converts Dr. Singh's June 5 response into concrete next actions.
It does not change the research questions or claim final Week 2 results.

## Decisions Now Resolved

| Question | Advisor response | Project decision |
|---|---|---|
| RQ framing | On track | Keep RQ1 consent-interface scoring and RQ2 longitudinal capture/versioning. |
| No-banner cases | Treat them as contrasts | Keep clean no-banner observations as contrast cases in the sample logic. |
| 20 vs 80+ | Fewer sites with deeper analysis is appropriate if scalable | Use around 20 sites for deep paper analysis; use the 80-ish list as a scaling pool / lightweight tracker. |

## Updated Sample Policy

The sample now has three tiers:

| Tier | Target size | Purpose | Evidence depth |
|---|---:|---|---|
| Week 2 evidence gate | 5 | Confirm the capture/report/diff chain works on frozen targets. | Full evidence check after capture. |
| Deep SSRP sample | About 20 | Main paper analysis. | Full Layer 1/2/3 scoring plus longitudinal summaries. |
| Broad tracker | About 80 | Scalable monitoring pool, including Qiyao-derived candidates if approved. | Lightweight capture status, screenshot/DOM refs, hashes, banner/no-banner flag, change flag, failure reason. |

The deep sample should include:

- banner-present sites with usable screenshot, DOM, path, and report evidence;
- a small set of clean no-banner contrast cases;
- replacements for access-friction rows that do not show a normal page or clean
  no-banner observation.

Current no-banner contrast candidates:

- BBC
- New York Times
- Amazon
- Airbnb
- Spotify
- Chase

Current replace/access-friction candidates:

- Reddit
- Walmart

## Work To Do Before The June 6 Capture

1. Keep the frozen Week 2 target list unchanged:
   `data/week2_deep_sample_targets_2026-06-06.csv`.
2. Do not promote the full 80-ish list into the deep sample before the Week 2
   evidence gate.
3. Treat the no-banner decision as resolved in methods framing: no-banner rows
   are contrast cases, not failed samples.
4. Prepare to show the next advisor update around three artifacts:
   first capture results, sample decision logic, and clearer paper structure.

## Work To Do On June 6

Run the scheduled Week 2 cycle on or after 2026-06-06:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-cycle
```

Then refresh/check:

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-refresh-outputs
PYTHONPATH=src .venv/bin/python -m consent_audit.cli week2-sanity-check
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

Expected next evidence:

- one new cohort row per successful Week 2 target;
- screenshot and DOM references for each completed capture;
- refreshed audit report summary;
- refreshed longitudinal summary;
- a sanity result that is either ready or explicitly triaged.

## Next Advisor Update Structure

Use this structure for the next update:

1. **First capture results**
   - which Week 2 sites completed;
   - which sites failed or need attention;
   - whether screenshot/DOM/hash/report evidence exists.

2. **Sample decision logic**
   - banner-present deep sample rows;
   - no-banner contrast rows;
   - access-friction / replacement rows;
   - why the paper uses about 20 sites while the broad tracker can scale toward 80.

3. **Paper structure**
   - Introduction: consent interfaces as dynamic privacy communication;
   - Background: Notice-and-Choice, cookie-banner audits, longitudinal measurement;
   - Methods: capture bundle, three-layer scoring, deterministic evidence checks;
   - Pilot evidence: Week 2 results and longitudinal examples;
   - Discussion: why dynamic evidence matters;
   - Limitations: public desktop pages, location/session effects, no legal-compliance claim.

4. **Scaling plan**
   - deep sample expands toward about 20 after sanity is stable;
   - 80-ish list becomes a lightweight tracker / candidate pool;
   - Qiyao-derived rows are used only if provenance and release constraints are respected.

## Paper Framing Update

The paper should now say that no-banner cases are analytically useful contrast
cases because absence of a visible consent banner in a repeated public desktop
capture is itself a traceable interface observation. These rows should not be
scored as if they were banner-present consent flows; they should be used to
compare visible-banner interfaces against pages where no visible consent layer
appears in the observed context.

SOC 2 remains outside the core paper frame. It can appear only as a short
discussion implication: consent-interface evidence may be relevant to privacy
or GRC readiness, but this project is not a SOC 2 audit.
