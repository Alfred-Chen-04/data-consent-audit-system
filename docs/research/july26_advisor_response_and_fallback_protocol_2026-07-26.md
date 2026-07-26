# July 26 Advisor Response And Fallback Protocol, 2026-07-26

## Purpose

Turn the July 25 joint review packet into an executable closeout gate without
inventing advisor input. This protocol covers both an actual response and no
response by the internal review cutoff.

## Current Gate

Verified on July 26:

- Today is day 58 of the 70-day May 30-August 7 core window, or 82.9% of
  that calendar window. Twelve calendar days remain before August 7.
- The joint decision sheet has 5 pending rows and 5 blank
  `confirmed_decision` fields.
- The poster-only sheet remains 5 pending/blank, the current-five sheet remains
  7 blank, and the CMP confirmation sheet remains 8 pending/blank.
- The nine-file joint ZIP passes archive integrity checks locally and is
  available on the remote PR branch with the same 5,964,170-byte size and
  SHA-256
  `98b2c7b779a9a4b451c6cde992fee9c582b56ebdc90872c9d09169548de00fdd`.
- At pre-freeze publication head
  `7c51f985599647637dfaa95b766bfc4186bcae38`, PR #8 was open, draft,
  mergeable, 26 commits ahead of and 0 behind `main`.
- PR #8 has 0 conversation comments, 0 submitted reviews, 0 inline review
  threads, and 0 pull-request workflow runs for the current head.

The absence of review input is evidence only that no response is recorded. It
does not imply approval, disagreement, or silence from any specific person.

## Send Preflight

The packet is `ready_to_send_or_discuss` because:

1. The email, presentation, aligned poster, decision sheet, and gap note are in
   one verified ZIP.
2. The ZIP is present on the remote review branch and matches the local hash.
3. The five questions are shared across the presentation, poster, and evidence
   package.
4. Every confirmation field is blank, so the packet cannot be mistaken for a
   completed review.

Use:

- Email: `docs/research/advisor_email_joint_presentation_poster_review_2026-07-25.md`
- Attachment: `docs/research/joint_review/ssrp_joint_advisor_review_2026-07-25.zip`
- Response record: `data/joint_advisor_review_decision_sheet_2026-07-25.csv`
- Decision-aware execution map: `data/closeout/joint_decision_revision_matrix_2026-07-26.csv`
- Current evidence inventory: `docs/research/july26_closeout_prefreeze_manifest_2026-07-26.md`

## Actual-Response Path

For each answer received:

1. Match it to one `decision_id` in the joint CSV.
2. Record only the actual answer in `confirmed_decision`.
3. Set `review_status=confirmed`, plus `reviewer` and `review_date`.
4. Use `other` and explain the wording in `notes` when the response does not
   match a listed option.
5. Revise only the affected artifact scope shown below.

| Decision | Default-compatible action | Alternate-answer gate |
|---|---|---|
| `shared_scope_framing` | Keep five-site pilot/method framing in both artifacts | Require reviewed evidence before any broader empirical claim |
| `main_evidence_cards` | Keep Guardian and Coca-Cola as the two large cards | Replace only with a present, verified screenshot and evidence note |
| `contrast_case_treatment` | Keep CNN, Booking.com, and NerdWallet as labeled contrasts | Change both artifacts and final tables together; never relabel them as failures by implication |
| `unresolved_review_items` | Keep 7 current-five blanks and 8 CMP rows visible as limitations | Stronger claims wait until the underlying rows are actually reviewed |
| `rq2_continuity_gate` | Freeze the current evidence package | Run at most one controlled capture tied to the approved RQ2 question, then refresh all affected exports |

After recording responses, rerun the poster/presentation content check, visual
render checks, link check, tests, archive integrity check, and final hashes.

## No-Response Path

Internal review cutoff: July 29, 2026 at 23:59 Asia/Shanghai. This is a project
management cutoff, not an advisor-provided deadline.

If no response is recorded by that cutoff:

- Leave all `confirmed_decision`, `reviewer`, and `review_date` fields blank.
- Leave `review_status=pending`; do not rewrite it as confirmed or approved.
- Use the following values only as project closeout fallback labels:

| Decision | Project fallback label | Resulting action |
|---|---|---|
| `shared_scope_framing` | `five_site_pilot_method` | Keep the existing bounded contribution claim |
| `main_evidence_cards` | `guardian_and_coca_cola` | Keep the existing two evidence cards |
| `contrast_case_treatment` | `no_visible_first_screen_banner_contrast` | Keep the three rows separate from banner-path failures |
| `unresolved_review_items` | `carry_as_visible_limitations_unless_stronger_claims_requested` | Keep all unresolved counts visible and avoid stronger claims |
| `rq2_continuity_gate` | `freeze_current_evidence_unless_specific_rq2_question_is_approved` | Do not start a new capture solely to make the timeline look newer |

Record a fallback in the final closeout note as a project decision made under
the no-response protocol. Do not place it in the CSV's advisor-confirmation
fields and do not describe it as advisor-confirmed.

## Date-Driven Work Order

| Date | Action | Exit condition |
|---|---|---|
| July 26 | Send or discuss the joint packet; keep PR #8 draft while review input is absent | Reviewer has one attachment and one five-row response path |
| July 27-29 | Record actual answers and make one concise follow-up if needed | Each received answer has provenance, or the cutoff passes with fields still blank |
| July 30 | Select the actual-response or no-response branch explicitly | Final revision basis is documented without invented approval |
| July 30-August 2 | Apply only allowed presentation/poster revisions | Both artifacts use the same framing, cases, limitations, and runtime boundary |
| August 3-5 | Freeze evidence manifest, present/missing refs, hashes, and limitations | Every displayed claim resolves to evidence or an explicit limitation |
| August 6-7 | Rehearse, rerender, verify, back up, and freeze core deliverables | One current index opens the final presentation, poster, and evidence package |

## Stop Conditions

- Do not run a continuity capture without a specific approved RQ2 question.
- Do not convert recommendations into confirmed decisions.
- Do not broaden the sample or claim scope to compensate for missing review.
- Do not mark the presentation, poster, or evidence package final before the
  selected response branch and final verification are recorded.
