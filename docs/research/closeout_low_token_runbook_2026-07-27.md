# SSRP Closeout Low-Token Runbook, 2026-07-27

## Use

This is the shortest safe path from the current pre-freeze state to project
closeout. Use the control index for artifact navigation and this file for the
next action. Do not reconstruct the plan from older daily notes.

**Current state on July 27:** all current closeout deliverables are present;
the active joint sheet has five `pending` rows with blank response provenance;
the revision matrix has 20 `waiting_for_response_branch` rows; no actual
response or project fallback is recorded; final-freeze readiness is `false`.

The internal fallback cutoff is July 29, 2026 at 23:59 Asia/Shanghai. It is a
project-management cutoff, not an advisor deadline.

The checked-in plan uses August 7, 2026 as the core closeout target.

## Direction Check

**Assessment:** the project is on track for the current bounded deliverable: a
five-site pilot/method presentation, a 48 x 36 poster, and a traceable evidence
package. That assessment depends on selecting the response branch, completing
the mapped revisions, and finishing final QA by August 7. The repository does
not support relabeling the work as a broad completed empirical study, and that
is not the current deliverable.

Already prepared and rechecked; do not recreate these from old notes:

- Week 2 evidence exports, current counts, limitations, and claim guardrails.
- A 10-slide presentation draft and aligned poster PPTX/PDF/PNG.
- One nine-file joint review packet and one active five-row response sheet.
- A validated map from five decisions to 20 exact revision surfaces.
- A schema-v2 manifest that blocks unsupported response provenance and a
  premature final-freeze claim.
- A five-row final-QA record and a final-index generator that refuses incomplete
  manifest, revision, QA, provenance, or artifact state.
- A separate historical trail that preserves older pending sheets without
  using them for current intake.

The remaining dependencies are not missing framework work:

- There is no checked-in proof that the joint packet was sent or discussed.
- Actual advisor answers can only be recorded when they are received.
- Project fallback values cannot be selected before the internal cutoff.
- Final visual inspection, rehearsal, and backup checks must follow the final
  artifact revisions; they cannot be truthfully completed in advance.

## One Status Command

```bash
uv run consent-audit research-status
```

Short Codex prompt:

> 检查 closeout 当前状态，只报告仓库和真实回复里的事实，然后执行当前允许的下一步；不要猜。

Stop if the manifest, joint sheet, or matrix is structurally invalid. Do not
use a historical decision sheet for current intake.

## Select The Response Branch

Always preview first:

```bash
uv run consent-audit closeout-prepare-revisions
```

This command is dry-run by default. It validates the five-row joint sheet, the
20-row matrix, response provenance, allowed values, and the cutoff. It can
combine recorded actual answers with post-cutoff fallback values for the rows
that remain pending. It never marks an artifact revision as verified.

### Actual reply received

1. Put only the exact received answer in the matching joint-sheet row.
2. Set `review_status=confirmed`, and record reviewer plus review date.
3. For an unlisted answer, use `other` and preserve the exact wording in
   `notes`.
4. Run the dry-run command. If it reports no error and only the intended
   decisions, write the matrix branch:

```bash
uv run consent-audit closeout-prepare-revisions --write
```

Short Codex prompt:

> 按我提供的真实回复更新 joint sheet，保留 reviewer/date；先 dry-run，通过后再写 revision matrix，不要补写我没提供的内容。

### No reply after the cutoff

For each decision that remains unanswered, leave its advisor confirmation,
reviewer, and date fields blank and pending. Preserve any actual responses
already recorded. After the cutoff, run the same dry-run and inspect that only
the still-pending decisions use
`project_fallback_after_internal_cutoff`. Then rerun with `--write`.

For a reproducible check, an explicit timestamp may be supplied:

```bash
uv run consent-audit closeout-prepare-revisions --as-of 2026-07-30T00:01:00+08:00
```

Short Codex prompt:

> 先确认已过 2026-07-29 23:59 +08:00 且 joint sheet 仍无相应回复；运行 fallback dry-run，零错误后再 --write，不要改 advisor confirmation 字段。

## Apply And Verify The 20 Rows

Use
`data/closeout/joint_decision_revision_matrix_2026-07-26.csv` as the execution
list. Work only on `ready_to_apply` rows. For each row:

1. Apply its selected branch to the named presentation, poster, or evidence
   surface. A retain-current action still requires a source-text check.
2. Run the row's `required_verification` checks.
3. Only after those checks pass, set `execution_status=applied_verified` and
   add `applied_by` plus a timezone-aware ISO 8601 `applied_at` value.
4. Keep failed or unperformed checks out of `applied_verified`.

Short Codex prompt:

> 按 revision matrix 的 ready_to_apply 行逐项修改并验证；只把实际通过 required_verification 的行标成 applied_verified，记录执行人和带时区时间。

Do not start a new continuity capture unless a specific RQ2 question was
actually approved. Do not broaden the five-site pilot claim without reviewed
evidence.

## Final Freeze

After all 20 rows are verified:

1. Rerender and visually inspect all 10 presentation slides and the poster.
2. Check presentation/poster overflow, poster 48 x 36 dimensions, final
   PDF/PNG, presentation montage, and rehearsal timing.
3. Refresh evidence exports and packages only from revised sources.
4. Run full pytest, Ruff, Mypy, compileall, local-link, JSON, ZIP, manifest
   reproducibility, Git diff-scope, and `git diff --check` checks. A final clean
   Git-state check follows the generated final-index commit.
5. Copy the final presentation, poster, and evidence package to the selected
   backup location and open each copied artifact.
6. Record only checks that actually passed in
   `data/closeout/final_qa_checklist_2026-07-27.csv`. A verified row requires
   concrete evidence, verifier, and an ISO 8601 timestamp with timezone.
7. Regenerate the manifest:

```bash
uv run consent-audit closeout-prefreeze-manifest
uv run consent-audit research-status
```

8. Proceed only when the regenerated manifest reports
   `ready_for_final_freeze=true` with zero blockers.
9. Validate the final-index gate without writing:

```bash
uv run consent-audit closeout-final-index
```

10. If the dry-run passes, generate the one final index and open every linked
    artifact from it:

```bash
uv run consent-audit closeout-final-index --write
```

Short Codex prompt:

> 执行 final closeout：完整渲染、仓库验证和备份打开检查，按事实填写 final QA；重建 manifest，final-index dry-run 通过后才 --write 和宣布完成。

## Facts That Must Remain Visible

- The evidence package contains 42 audit rows and 20 longitudinal rows; the
  latest longitudinal `week_of` is 2026-06-06.
- The current audit CSV has 42 locally present screenshot references and 42
  locally missing DOM references; it has no `report_pdf_ref` column.
- The five joint decisions are separate from 25 open rows counted across four
  current and historical sheets.
- Passing tests and file hashes prove software/inventory properties, not legal
  compliance, research validity, advisor approval, or a current live-site
  observation.
