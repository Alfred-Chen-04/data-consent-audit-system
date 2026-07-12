# July 12 Poster Assembly Packet, 2026-07-12

Purpose: turn the July 7 layout draft and July 9 asset manifest into a
single poster assembly packet that can be used to build the first visual
poster mockup or brief Dr. Singh.

This packet adds no new browser capture and no new consent-interface evidence.
It organizes already verified evidence into a poster-ready build sequence.

## Current Facts Used

- Date checked: 2026-07-12.
- Core research window: May 30-August 7, 2026.
- Calendar progress: 44 of 70 core-cycle days, or 62.9%.
- Days left before August 7 core deadline: 26.
- Days left before August 31 polish deadline: 50.
- Local branch and upstream: `codex/project-status-plain-language` at
  `62e98b7f332c8ff958fe85f0dde6904eda41914e`.
- GitHub PR #8: open, draft, mergeable, not merged into `main`.
- `main` remains at `28ee83755bc1eb379b08a8941ebad146d9c8fd45`.
- `research-status`: preflight `ready_for_capture`, sanity `ready`, cycle
  capture `completed`.
- Research package: 42 audit reports and 20 longitudinal summaries.
- Banner-detected counts in `audit_report_summary.csv`: true=9, false=33.
- Screenshot evidence: 326 site `layer1.png` files; 0 synced site
  `layer1.html` raw DOM files.
- Current-five decision sheet: 7 rows, 7 blank decisions.
- CMP/manual-review confirmation sheet: 8 rows, 8 pending confirmations.

## What Is Safe To Do Today

Build a first visual poster mockup from existing verified evidence.

Do not start new live capture today unless the advisor/user first resolves the
current decision blockers. The current useful work is poster assembly because
the verified evidence already supports a pilot/method poster, while the final
dataset claims remain blocked.

## Poster Build Order

1. Create a landscape poster canvas with one title band, three content columns,
   and a short bottom strip.
2. Place the title, subtitle, and RQ1/RQ2 from the July 7 layout draft in the
   top band.
3. Put the problem framing, audit pipeline, and deterministic scoring guardrail
   in the left column.
4. Put the current evidence snapshot plus The Guardian and Coca-Cola evidence
   cards in the middle column.
5. Put CNN, Booking.com, and NerdWallet as compact no-visible-banner contrast
   rows in the right column.
6. Put limitations and next decisions close to the evidence, not hidden only in
   the footer.
7. Use the bottom strip for the one-sentence contribution and artifact refs.

## Poster Copy Blocks

Title:

> Traceable Consent Interface Audit and Versioning

Subtitle:

> A pilot workflow for scoring layered consent interfaces and tracking how
> privacy interface evidence changes over time.

Status label:

> Current evidence package: pilot/method evidence, not a final 20-site dataset.

Contribution sentence:

> The contribution is a traceable audit-and-versioning workflow for consent
> interface evidence; deep, evidence-linked pilot cases are safer than broad
> unsupported claims.

Method sentence:

> The same evidence bundle supports both proposal questions: RQ1 scoring and
> RQ2 longitudinal versioning.

Scoring guardrail:

> Model extraction can help locate visual and text evidence, but final scores
> are deterministic after schema validation.

## Evidence Snapshot Panel

| Evidence item | Verified count |
|---|---:|
| Week 2 target sites | 5 |
| Audit reports | 42 |
| Longitudinal summaries | 20 |
| Site `layer1.png` screenshots | 326 |
| Synced raw `layer1.html` files | 0 |
| Current-five blank decisions | 7 |
| CMP/manual-review pending confirmations | 8 |

Caption:

> Counts reflect the current PR branch evidence package on 2026-07-12.

## Screenshot Placements

| Site | Poster placement | Screenshot path | Safe label |
|---|---|---|---|
| The Guardian | Middle column large evidence card | `data/captures/sites/www_theguardian_com_20260605_160209/layer1.png` | Stored screenshot evidence shows a visible Guardian consent-choice screen with accept/reject/manage-cookie choices. |
| Coca-Cola | Middle column large evidence card | `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png` | Stored screenshot evidence shows a visible Privacy Preference Center with consent controls. |
| CNN | Right column compact contrast row | `data/captures/sites/www_cnn_com_20260605_160221/layer1.png` | No visible first-screen cookie banner in the stored screenshot. |
| Booking.com | Right column compact contrast row | `data/captures/sites/www_booking_com_20260605_160226/layer1.png` | No visible first-screen cookie banner in the stored screenshot. |
| NerdWallet | Right column compact contrast row | `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png` | No visible first-screen cookie banner in the stored screenshot. |

Required note:

> No-visible-banner contrast cases are not banner-path failures. They require a
> separate table label or advisor decision before final scoring claims.

## Claims To Use

- The current package contains traceable pilot/method evidence.
- The pipeline produces evidence-linked `AuditReport` rows.
- The pipeline produces longitudinal summaries over repeated observations.
- Five poster screenshots have already been verified as present PNG assets.
- Manual/advisor review is still needed for no-visible-banner and CMP-uncertain
  rows.

## Claims Not To Use

- Final dataset complete.
- 20-site sample locked.
- Raw HTML files synced.
- CNN, Booking.com, or NerdWallet failed consent-path availability.
- This site is legally compliant.
- This site is legally non-compliant.
- The live website still looks the same today.
- PR #8 is merged into `main`.

## Advisor Questions For The Poster

Ask only these concrete questions:

1. Should the poster stay framed as a five-site pilot/method poster?
2. Are Guardian and Coca-Cola acceptable as the two main evidence cards?
3. What label should be used for no-visible-banner rows: contrast case,
   unresolved case, or excluded from final scoring?
4. Should the 7 current-five blank decisions be resolved now or carried as a
   limitation?
5. Should the 8 CMP/manual-review pending rows be resolved now or excluded from
   final poster claims?

## Build Status

The next concrete deliverable is a first visual poster mockup using this packet.
The content is ready for assembly, but final empirical claims are not ready
until the unresolved decisions above are answered.
