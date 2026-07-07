# July 7 Poster Layout Draft, 2026-07-07

Purpose: convert the July 7 poster build work order into a first poster layout
draft that can be used for a slide, poster canvas, or design mockup.

This draft adds no new browser capture and no new consent-interface evidence.
It is a layout/content draft only.

## Current Build Decision

Build the poster as a pilot/method poster, not as a final empirical-results
poster.

The poster should answer:

1. What is the research question?
2. What did the audit pipeline do?
3. What evidence exists now?
4. What can be safely shown from the current five-site pilot?
5. What remains unresolved before final claims?

## Layout Frame

Use a landscape poster with one full-width title band, three main columns, and a
short bottom strip. If the final print size is unknown, preserve this structure
and resize later.

| Area | Width | Poster role |
|---|---:|---|
| Top band | 100% | Title, one-sentence claim, RQ1/RQ2 |
| Left column | 30% | Problem, research questions, method pipeline |
| Middle column | 40% | Evidence snapshot and two banner-present cards |
| Right column | 30% | Contrast cases, limitations, next decisions |
| Bottom strip | 100% | Takeaway and artifact links |

## Top Band

Title:

> Traceable Consent Interface Audit and Versioning

Subtitle:

> A pilot workflow for scoring layered consent interfaces and tracking how
> privacy interface evidence changes over time.

Research questions:

> RQ1: How can layered consent interfaces be scored for unbiased choice across
> the full consent pathway?
>
> RQ2: How can privacy and consent interfaces be captured and versioned over
> time to document interface change?

Small status label:

> Current evidence package: pilot/method evidence, not a final 20-site dataset.

## Left Column

### Panel A: Why This Matters

Poster text:

> Consent interfaces are not just legal notices. They are layered design and
> communication systems that can make privacy choices easy, difficult, visible,
> hidden, stable, or volatile over time.

Use three short callouts:

- Choice pathway: are Accept, Reject, Customize, and Dismiss available?
- Choice effort: how much interaction is needed to reach each path?
- Choice framing: does the text support transparent, unbiased choice?

### Panel B: Audit Pipeline

Use this flow:

```text
Website URL
  -> Screenshot + DOM ref/hash + visible text
  -> Path attempts and event log
  -> Layer 1: path availability
  -> Layer 2: path effort
  -> Layer 3: transparency and unbiased-choice framing
  -> AuditReport
  -> WeeklySummary for longitudinal change
```

Poster text:

> The same evidence bundle supports both proposal questions: RQ1 scoring and
> RQ2 longitudinal versioning.

### Panel C: Scoring Guardrail

Poster text:

> Model extraction can help locate visual and text evidence, but final scores
> are deterministic after schema validation. No unsupported model-generated
> final grades are accepted.

## Middle Column

### Panel D: Current Evidence Snapshot

Use this table:

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

> Counts reflect the current PR branch evidence package on 2026-07-07.

### Panel E: Evidence Card 1, The Guardian

Image placeholder:

- `data/captures/sites/www_theguardian_com_20260605_160209/layer1.png`

Card copy:

> Stored screenshot evidence shows a visible Guardian consent-choice screen
> with accept/reject/manage-cookie choices.

Evidence role:

- `banner_present`
- visible choice-interface example
- use as method evidence, not a legal-compliance claim

### Panel F: Evidence Card 2, Coca-Cola

Image placeholder:

- `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png`

Card copy:

> Stored screenshot evidence shows a visible Privacy Preference Center with
> consent controls.

Evidence role:

- `banner_present`
- preference-center example
- use as method evidence, not a legal-compliance claim

## Right Column

### Panel G: No-Visible-Banner Contrast Cases

Use a compact three-row strip:

| Site | Screenshot ref | Poster-safe label |
|---|---|---|
| CNN | `data/captures/sites/www_cnn_com_20260605_160221/layer1.png` | No visible first-screen cookie banner in stored screenshot. |
| Booking.com | `data/captures/sites/www_booking_com_20260605_160226/layer1.png` | No visible first-screen cookie banner in stored screenshot. |
| NerdWallet | `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png` | No visible first-screen cookie banner in stored screenshot. |

Required note:

> No-visible-banner contrast cases are not banner-path failures. They require a
> separate table label or advisor decision before final scoring claims.

### Panel H: What The Pilot Shows

Poster text:

> The pilot evidence shows that a traceable pipeline can produce both
> evidence-linked audit reports and longitudinal summaries from the same capture
> workflow.

Use three bullets:

- RQ1 output exists: evidence-linked `AuditReport` rows.
- RQ2 output exists: longitudinal summaries over repeated observations.
- Manual review is still needed for no-visible-banner and CMP-uncertain rows.

### Panel I: Limitations

Use this wording:

> Current results are pilot/method evidence. Raw `layer1.html` files are not
> synced in this checkout; the current-five decision sheet is blank; 8
> CMP/manual-review confirmations are pending; and PR #8 is not merged into
> `main`.

Do not claim:

- final dataset complete;
- 20-site sample locked;
- raw HTML synced;
- no-visible-banner rows are banner-path failures;
- legal compliance or non-compliance;
- sample-wide empirical conclusions.

### Panel J: Next Decisions

Use this checklist:

- Keep poster as five-site pilot/method poster, or expand?
- Confirm Guardian and Coca-Cola as the two main evidence cards.
- Decide table label for no-visible-banner rows.
- Resolve or explicitly carry the 7 current-five blank decisions.
- Resolve or exclude the 8 CMP/manual-review rows from final claims.

## Bottom Strip

Takeaway:

> The contribution is a traceable audit-and-versioning workflow for consent
> interface evidence. Deep, evidence-linked pilot cases are safer than broad
> unsupported claims.

Artifact links to show in small text:

- `docs/research/current_project_goal_2026-07-02.md`
- `docs/research/july7_poster_build_work_order_2026-07-07.md`
- `docs/research/july6_recent_work_validation_and_gap_audit_2026-07-06.md`
- `data/research_package/audit_report_summary.csv`
- `data/research_package/longitudinal_summary.csv`

## Visual Build Notes

- Use screenshots as evidence cards, not decorative images.
- Keep Guardian and Coca-Cola large enough to inspect the consent controls.
- Keep CNN, Booking.com, and NerdWallet smaller as contrast thumbnails or a
  compact table.
- Avoid large final-results charts unless the unresolved decisions are labeled
  clearly.
- Put limitations near results, not hidden in the footer.

## Build Status

This draft is ready for a first visual mockup. It is not final until the
advisor/user decides whether to keep the poster as a five-site pilot/method
poster or expand toward more banner-present examples.
