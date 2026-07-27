# July 26 Decision-To-Revision Matrix, 2026-07-26

## Purpose

Prepare the final content pass without inventing a response or changing either
review artifact early. The companion CSV maps each joint decision to exact
presentation, poster, and evidence-package surfaces:

- `data/closeout/joint_decision_revision_matrix_2026-07-26.csv`

This is an execution map, not a decision record. The joint decision sheet
remains the only place for actual advisor responses, and its five rows remain
`pending` with blank confirmation fields.

## Verified Current State

- Local branch, remote branch, and PR #8 head were synchronized at
  `7c51f985599647637dfaa95b766bfc4186bcae38` before this matrix was written.
- PR #8 was open, draft, and mergeable with no submitted review or inline
  review thread recorded.
- The joint sheet remained 5 pending/blank; the historical poster-only sheet
  remained 5 pending/blank; current-five remained 7 blank; CMP/manual review
  remained 8 pending/blank.
- The presentation PPTX contains 10 slides. The aligned poster PPTX contains
  one 48 x 36 inch slide.
- PPTX structure was read directly to identify slide numbers, shape IDs,
  named poster shapes, and current text. No PPTX, PDF, PNG, capture, score, or
  decision changed.

## Matrix Coverage

The CSV has 20 execution rows:

| Artifact | Rows | What is mapped |
|---|---:|---|
| Presentation | 8 | Cover/scope, evidence cards, contrast slide, unresolved-decision closeout, and RQ2 timeline |
| Poster | 8 | Pilot labels, status/footer claims, both main cards, contrast block, 7/8 limitation block, and RQ2 framing |
| Evidence package | 4 | Manifest status, contrast-table rule, human-decision state, and longitudinal freeze/refresh path |

Every row is `waiting_for_response_branch`. The following fields are blank by
design: `selected_value`, `response_basis`, `applied_by`, `applied_at`, and
`notes`.

## How To Use It

### Actual response

1. Record the answer and reviewer/date provenance in
   `data/joint_advisor_review_decision_sheet_2026-07-25.csv`.
2. Copy the exact confirmed value into `selected_value` only for rows with the
   matching `decision_id`.
3. Set `response_basis=actual_advisor_response`.
4. Set `execution_status=ready_to_apply`, then apply only the mapped surfaces
   and required cross-artifact updates.
5. After the edit and verification succeed, set
   `execution_status=applied_verified` and record the executor plus an ISO 8601
   timestamp with timezone.

### No response after the internal cutoff

1. Leave all advisor-confirmation fields blank and pending.
2. Select the project fallback label from the July 26 protocol only after
   July 29, 2026 at 23:59 Asia/Shanghai.
3. Set `response_basis=project_fallback_after_internal_cutoff`; do not use
   `actual_advisor_response`.
4. Set `execution_status=ready_to_apply` and apply only the default/fallback
   actions in the matrix.
5. After verification, set `execution_status=applied_verified`, record the
   executor/timestamp, and state the project basis explicitly in the final
   closeout note.

## Decision Surface Summary

| Joint decision | Primary presentation surfaces | Primary poster surfaces | Evidence-package effect |
|---|---|---|---|
| `shared_scope_framing` | Slides 1, 5, and 10 | `header-eyebrow`, `status-text`, `footer-takeaway` | Keep `finalized=false` until the selected branch and final checks are recorded |
| `main_evidence_cards` | Slides 6 and 7 | Guardian and Coca-Cola labels, pictures, and captions | Any replacement needs a present screenshot, source note, and refreshed hashes |
| `contrast_case_treatment` | Slide 8 | Full contrast block and `contrast-note` | Update current-five treatment and final tables together |
| `unresolved_review_items` | Slide 10 closeout item | 7/8 metrics and `limits-copy` | Preserve blank confirmations or refresh all counts from actual reviewed rows |
| `rq2_continuity_gate` | Slide 9 timeline | RQ2, pipeline note, snapshot caption | Freeze current 20-row export or fully refresh after one approved controlled question |

## Historical Poster-Only Question

`final_print_revision` exists only in the superseded poster-only decision
sheet. It is not silently promoted into a sixth joint decision and it remains
pending/blank as dated history. Regardless of that historical response state,
the selected joint branch still requires poster overflow, PDF/PNG render, print
dimension, and visual inspection before closeout.

## Required Final Verification

- Confirm selected values have an allowed response basis and provenance.
- Recheck all current-surface text and every changed evidence source.
- Render and inspect all 10 presentation slides and the one-page poster.
- Run presentation/poster overflow and poster print-dimension checks.
- Rebuild final transport/evidence packages from the revised sources.
- Regenerate the closeout manifest and verify file/ref hashes.
- Run the full test, Ruff, Mypy, link, JSON, ZIP, and Git-state checks.
- Keep the artifacts non-final until every selected matrix row is applied and
  verified.

## Stop Conditions

- Do not fill `selected_value` before an actual response or the internal cutoff.
- Do not use a recommended default as advisor confirmation.
- Do not change only one artifact when a matrix row requires parity.
- Do not add a continuity capture without a specific approved RQ2 question.
- Do not use file presence or passing tests as proof of research validity.
