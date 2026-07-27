# July 7 Poster Build Work Order, 2026-07-07

Purpose: turn the July 6 poster section draft into an execution-ready poster
build plan using only verified pilot evidence and current limitations.

This work order adds no new browser capture and no new consent-interface
evidence. It should be used to build the next poster/presentation draft, not to
claim a final experiment result.

## Current Facts Used

- Date: 2026-07-07.
- Core research window: May 30-August 7, 2026.
- Calendar progress: 39 of 70 core-cycle days, or 55.7%.
- Days left before August 7 core deadline: 31.
- Days left before August 31 polish deadline: 55.
- PR #8: open, draft, mergeable, not merged into `main`.
- Local branch and upstream: `958d22046c0383493cc0e255433a5867008d6adc`.
- `research-status`: preflight `ready_for_capture`, sanity `ready`, cycle
  capture `completed`.
- Research package: 42 audit reports and 20 longitudinal summaries.
- Banner-detected counts in `audit_report_summary.csv`: true=9, false=33.
- Screenshot evidence: 326 site `layer1.png` files; 0 synced site
  `layer1.html` raw DOM files.
- Current-five decision sheet: 7 rows, 7 blank decisions.
- CMP/manual-review confirmation sheet: 8 rows, 8 pending confirmations.
- Targeted validation before this work order: 40 relevant pytest checks passed,
  `research-status` was consistent, and `git diff --check` was clean.

## Poster Build Structure

Build the poster as a pilot/method poster with seven panels:

1. Title and research questions.
2. Method pipeline.
3. Current evidence snapshot.
4. Banner-present evidence cards.
5. No-visible-banner contrast cases.
6. Limitations and guardrails.
7. Next decisions.

Recommended title:

> Traceable Consent Interface Audit and Versioning

Main poster claim:

> This project develops a computational audit and versioning workflow for
> website consent interfaces. RQ1 scores whether layered consent pathways
> support unbiased choice, while RQ2 captures and compares interface evidence
> over time.

## Panel Content

### 1. Title And Research Questions

Use:

- RQ1: How can layered consent interfaces be scored for unbiased choice across
  the full consent pathway?
- RQ2: How can privacy and consent interfaces be captured and versioned over
  time to document interface change?

Do not make screenshot collection the research question. Screenshots, DOM refs,
hashes, visible text, and event logs are evidence inputs for RQ1/RQ2.

### 2. Method Pipeline

Show this sequence:

1. Capture website evidence: screenshot, DOM ref/hash, visible text,
   interaction attempts, and event metadata.
2. Score Layer 1 path availability.
3. Score Layer 2 path effort.
4. Score Layer 3 transparency and unbiased-choice framing.
5. Export evidence-linked `AuditReport` rows.
6. Repeat captures over time.
7. Compare screenshots, DOM hashes, visible text, and pathway outputs for
   longitudinal summaries.

Poster-safe methods sentence:

> Evidence is extracted from screenshots, DOM refs, hashes, visible text, and
> interaction logs. Final scores are deterministic after extraction and schema
> validation; model output is not accepted as an unsupported final grade.

### 3. Current Evidence Snapshot

Use this table:

| Item | Current verified count |
|---|---:|
| Week 2 target sites | 5 |
| Audit reports in research package | 42 |
| Longitudinal summaries | 20 |
| Site `layer1.png` screenshots | 326 |
| Synced site `layer1.html` raw DOM files | 0 |
| Current-five blank decisions | 7 |
| CMP/manual-review pending confirmations | 8 |

Label this panel as current pilot evidence. Do not label it final dataset
coverage.

### 4. Banner-Present Evidence Cards

Use two evidence cards:

| Site | Role | Screenshot ref | Safe claim |
|---|---|---|---|
| The Guardian | Banner-present choice example | `data/captures/sites/www_theguardian_com_20260605_160209/layer1.png` | Stored screenshot evidence shows a visible Guardian consent-choice screen with accept/reject/manage-cookie choices. |
| Coca-Cola | Banner-present preference-center example | `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png` | Stored screenshot evidence shows a visible Privacy Preference Center with consent controls. |

Use these as method evidence cards. Do not claim they prove legal compliance or
non-compliance.

### 5. No-Visible-Banner Contrast Cases

Use three contrast cards:

| Site | Role | Screenshot ref | Safe claim |
|---|---|---|---|
| CNN | No-visible-banner contrast | `data/captures/sites/www_cnn_com_20260605_160221/layer1.png` | Stored screenshot shows the CNN homepage with no visible first-screen cookie banner. |
| Booking.com | No-visible-banner contrast | `data/captures/sites/www_booking_com_20260605_160226/layer1.png` | Stored screenshot shows the Booking.com homepage/search UI with no visible first-screen cookie banner. |
| NerdWallet | No-visible-banner contrast | `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png` | Stored screenshot shows the NerdWallet homepage/product UI with no visible first-screen cookie banner. |

Required label:

> No-visible-banner contrast cases are not banner-path failures. They require a
> separate table label or advisor decision before final scoring claims.

### 6. Limitations And Guardrails

Use this wording:

> The current poster is a pilot and method demonstration. Raw `layer1.html`
> files are not synced in this checkout; current-five decisions remain blank;
> CMP/manual-review confirmations are pending; and PR #8 is not merged into
> `main`. The evidence supports method and traceability claims, not final
> compliance conclusions.

Do not claim:

- The final dataset is complete.
- The 20-site sample is locked.
- Raw HTML files are synced.
- CNN, Booking.com, or NerdWallet are banner-path failures.
- Any site is legally compliant or non-compliant.
- PR #8 is merged into `main`.
- The poster proves sample-wide empirical findings.

### 7. Next Decisions

Ask for or record these decisions before final poster freeze:

1. Should the poster stay as a five-site pilot/method poster, or expand toward
   more banner-present examples?
2. How should no-visible-banner rows be labeled in result tables?
3. Should Guardian and Coca-Cola be the two main evidence cards?
4. Should the 7 current-five blank decisions be filled, or carried as explicit
   limitations?
5. Should the 8 CMP/manual-review confirmations be resolved now, or excluded
   from final poster claims?

## Build Checklist

- [ ] Create the poster layout with the seven panels above.
- [ ] Use Guardian and Coca-Cola as the two banner-present cards.
- [ ] Use CNN, Booking.com, and NerdWallet only as no-visible-banner contrast
      cases.
- [ ] Include the current evidence snapshot table exactly or with the same
      counts.
- [ ] Add the required limitation language.
- [ ] Keep all claims tied to screenshot/report/table evidence refs.
- [ ] Do not add final 20-site, legal-compliance, raw-HTML, or sample-wide
      claims.

## Bottom Line

Today's concrete work is poster assembly from verified existing evidence. The
project is healthy for a pilot poster/presentation package, but it is still
blocked from final experiment claims by unresolved current-five decisions,
pending CMP confirmations, missing synced raw HTML, and the unmerged draft PR.
