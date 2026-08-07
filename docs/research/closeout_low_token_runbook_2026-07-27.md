# SSRP Closeout Low-Token Runbook, Current as of 2026-08-06

## Current Truth

- Summer 2026 Intersections occurred on July 30, 10:00 a.m.-12:00 p.m. in the
  Tinkham Veale Grand Ballroom. The repository cannot prove registration,
  attendance, poster number, or board selection.
- Registration closed July 12 and PI approval was due July 15. This is now a
  historical event, not a pending same-day action.
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
- A 10-slide August 4 rehearsal-ready presentation with source notes and a
  short question bank.
- A 48 x 36 July 30 poster in PPTX, PDF, and PNG form.
- Direction and causal-strength fields kept separate.
- Final-index code points to the latest longitudinal artifacts.
- Machine QA, manifest, backup, and final-index dry run are reproducible
  without new research decisions.
- A seven-page, source-audited final-paper submission candidate with numbered
  references is ready for an owner formatting check.

Do not recreate these from older daily notes.

## The Only Three Human Inputs

Send these as three short lines. Unknown is an acceptable factual answer, but it
triggers the URO follow-up below.

```text
夏季展示=已参加/已注册未参加/未注册/未知; 证据=邮件或CampusGroups记录/无; board=40x60/32x40/未知; poster号=值/未知
彩排=总时长X:XX; Q&A=X:XX; 修改1=...; 修改2=...
论文提交=已提交/未提交; 渠道=实际渠道/未知; 回执=确认号或截图位置/无; 时间=YYYY-MM-DDThh:mm:ss+08:00/未知
```

These inputs update
`data/closeout/human_closeout_confirmation_2026-07-30.csv`. Do not infer them
from file presence.

## Presentation Obligation After Summer Intersections

### Summer Status Is Confirmed

1. Record the factual result and supporting evidence in the human-confirmation
   CSV.
2. If the project was presented, retain the confirmation as external
   completion evidence; do not change research claims.
3. If it was registered but not presented, use the URO reply to select the
   Fall 2026 or Spring 2027 path.

### Summer Status Is Unknown Or No Presentation Occurred

1. Do not claim that Summer Intersections was completed.
2. Ask URO which Fall 2026 or Spring 2027 Intersections will satisfy the SSRP
   presentation requirement and whether any Summer registration record exists.
3. Keep the current poster as the submission-ready artifact. It can be rotated
   for a future board if URO confirms a different orientation.

Ready-to-send message:

```text
Subject: SSRP 2026 presentation requirement and Intersections status

Hello Undergraduate Research Office,

I am completing my 2026 SSRP project. Could you please confirm whether my
project was registered and approved for the July 30 Summer Intersections event?
If it was not presented, could you confirm the next Fall 2026 or Spring 2027
Intersections registration path that will satisfy my SSRP presentation
requirement? My poster and evidence package are ready.

Thank you,
Qianyi (Alfred) Chen
```

## Machine Closeout

After a timed rehearsal is recorded:

```bash
uv run consent-audit research-status
uv run consent-audit closeout-prefreeze-manifest
uv run python scripts/build_longitudinal_artifact_manifest.py
uv run python scripts/build_longitudinal_closeout_backup.py
uv run consent-audit closeout-final-index
```

`closeout-final-index` must refuse while rehearsal evidence is pending. The
Summer event status is an SSRP-obligation record, not evidence that can be
inferred from this repository. A verified row requires concrete evidence,
verifier, and a timezone-aware ISO 8601 timestamp. Only after every gate
passes:

```bash
uv run consent-audit closeout-final-index --write
```

`uv run consent-audit research-status` also lists the exact pending external
confirmation IDs, including final-paper submission; use it as the one-command
status check before changing any row.

## Final Paper Path

Use the August 5 submission candidate as the starting point, not the older
working draft. Check only actual mentor/URO formatting direction before upload;
the repository does not contain a public SSRP paper template or page-count
requirement. After a real upload, record its channel, receipt, and timestamp in
the human-confirmation CSV.

The low-token prompts are:

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
