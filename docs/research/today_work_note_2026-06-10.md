# Today Work Note, 2026-06-10

## Evidence Checked

- `consent-audit research-status`
- `docs/research/today_work_note_2026-06-09.md`
- `docs/research/recent_work_evidence_audit_2026-06-09.md`
- `data/research_package/audit_report_summary.csv`
- `data/research_package/longitudinal_summary.csv`
- `data/week2_deep_sample_targets_2026-06-06.csv`

## Current State

- Week 2 five-site evidence gate is complete.
- Sanity status is `ready`.
- Cycle capture status is `completed`.
- Current research package has 42 audit reports and 20 longitudinal summaries.
- The latest Week 2 evidence has 2 banner-present cases and 3 no-visible-banner contrast candidates.
- There are still 8 pending CMP/manual-review confirmation rows.
- No advisor response is recorded in the repo after the 2026-06-09 evidence-based next-step email draft.

## Decision

Today should not be another blind capture day. The evidence-based next step is
to prepare the five current Week 2 evidence bundles for manual review, because
the project needs a human coding decision before expanding toward the about
20-site deep sample.

## Work Done Today

Created a five-site manual evidence review worksheet:

- `data/week2_manual_evidence_review_2026-06-10.csv`

The worksheet is generated from current RQ1/RQ2 evidence and includes:

- site/category/URL;
- current evidence class;
- current coding interpretation;
- automated tier and available/missing first-layer paths;
- latest longitudinal severity and event types;
- screenshot and DOM references;
- DOM/image hashes;
- blank fields for human confirmation and notes.

## How To Use The Worksheet

For each of the five rows:

1. Open the screenshot reference.
2. Confirm whether a visible banner/control is actually present.
3. Fill `human_visible_banner_confirmed`.
4. Fill `human_final_coding`.
5. Decide whether the site should stay in the deep sample, become a contrast case, or be replaced.
6. Add notes that can later support paper/poster evidence cards.

## Recommended Next Step

Wait for Professor Singh's answer to the 2026-06-09 evidence-based email if it
has been sent. If no answer is available before the next work block, manually
review the five rows in `data/week2_manual_evidence_review_2026-06-10.csv` and
prepare a candidate expansion list that prioritizes banner-present sites.
