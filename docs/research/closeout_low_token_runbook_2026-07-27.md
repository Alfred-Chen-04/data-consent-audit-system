# SSRP Closeout Low-Token Runbook, Current as of 2026-07-30

## Current Truth

- Summer 2026 Intersections is today, July 30, 10:00 a.m.-12:00 p.m. in the
  Tinkham Veale Grand Ballroom.
- Registration closed July 12 and PI approval was due July 15. The repository
  cannot prove registration, attendance, poster number, or board selection.
- The official SSRP program period ends July 31.
- SSRP requires an Intersections presentation in Summer 2026, Fall 2026, or
  Spring 2027 and a final paper by August 31, 2026.
- The current research result is an observational six-company case series:
  five component improvements and one functional regression. It is not an
  experiment or a prevalence estimate.
- The current local five-site pilot still has insufficient evidence for a
  directional claim.

## What Is Already Prepared

- Six source-complete historical trajectories and a 12-source registry.
- A 10-slide July 30 presentation with source notes.
- A 48 x 36 July 30 poster in PPTX, PDF, and PNG form.
- Direction and causal-strength fields kept separate.
- Final-index code points to the latest longitudinal artifacts.
- Machine QA, manifest, and backup can be regenerated without new research
  decisions.

Do not recreate these from older daily notes.

## The Only Two Human Inputs

Send these as two short lines. Unknown is an acceptable factual answer.

```text
展示状态=已注册/未注册/未知; 实际展示=是/否/未知; board=40x60/32x40/未知; poster号=值/未知
彩排=总时长X:XX; Q&A=X:XX; 修改1=...; 修改2=...
```

These inputs update
`data/closeout/human_closeout_confirmation_2026-07-30.csv`. Do not infer them
from file presence.

## Today Branch

### Registered for Summer Intersections

1. Check the URO location/number email or CampusGroups record.
2. Use the 48 x 36 poster only if the selected board is 40 x 60.
3. Bring the printed poster; URO provides the board, easel, and clips.
4. Deliver the 90-second poster pitch in the rehearsal script and record the
   actual presentation status afterward.

### Not Registered or Status Unknown

1. Do not claim that Summer Intersections was completed.
2. Ask URO/advisor which Fall 2026 or Spring 2027 Intersections will satisfy the
   SSRP presentation requirement.
3. Keep the current poster as the submission-ready artifact.

Minimal message:

```text
I am completing my 2026 SSRP project and need to confirm which upcoming
Intersections session should satisfy my presentation requirement. My poster and
evidence package are ready. Could you confirm the next registration window?
```

## Machine Closeout

After the two human inputs are recorded:

```bash
uv run consent-audit research-status
uv run consent-audit closeout-prefreeze-manifest
uv run consent-audit closeout-final-index
```

`closeout-final-index` must refuse while rehearsal evidence is pending. A
verified row requires concrete evidence, verifier, and a timezone-aware ISO
8601 timestamp. Only after every gate passes:

```bash
uv run consent-audit closeout-final-index --write
```

## Final Paper Path

Use `docs/research/ssrp_final_paper_completion_plan_2026-07-30.md`. The low-token
prompts are:

```text
按 final paper plan 写第1-2节，只用登记来源。
按 final paper plan 写第3-4节，保留 observational case-series 边界。
对 final paper 做一次 claim/source audit，不添加新事实。
```

## Facts That Must Remain Visible

- `5/6` describes a purposively selected case series, not the internet.
- The local five and historical six use different evidence protocols.
- Google has direct company attribution; Facebook and Orange have formal
  order-response evidence; TikTok and SHEIN have proceedings-period evidence;
  Vanity Fair's regression cause is unknown.
- A visible reject button is not proof that refusal stops tracking.
- Tests and hashes prove software and file properties, not legal compliance,
  causal validity, advisor approval, or event attendance.
