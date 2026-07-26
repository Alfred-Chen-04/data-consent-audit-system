# SSRP Closeout Pre-Freeze Manifest

**Status: `pre_freeze` - this is not a final or frozen manifest.**

Generated at: `2026-07-26T17:04:15.752310+00:00`

Machine-readable source: [`../../data/closeout/closeout_prefreeze_manifest_2026-07-26.json`](../../data/closeout/closeout_prefreeze_manifest_2026-07-26.json)

Regenerate from the repository root with `uv run consent-audit closeout-prefreeze-manifest`.

## Evidence Tables

| Table | Status | Rows | Bytes | SHA-256 |
|---|---:|---:|---:|---|
| `data/research_package/audit_report_summary.csv` | present | 42 | 20937 | `c4fd673a115f14c6969dcaa58e50c7e1c52a23d98bb590411497cce8a078bc49` |
| `data/research_package/longitudinal_summary.csv` | present | 20 | 9141 | `f1069383db8bd2ac9b777eaefbff26d4134490c55d397198275db0f5602258c0` |

## Evidence References

| CSV column | Present | Nonblank | Blank | Present refs | Missing refs | External | Outside repo |
|---|---:|---:|---:|---:|---:|---:|---:|
| `first_screenshot_ref` | true | 42 | 0 | 42 | 0 | 0 | 0 |
| `first_dom_snapshot_ref` | true | 42 | 0 | 0 | 42 | 0 | 0 |
| `report_pdf_ref` | false | n/a | n/a | 0 | 0 | 0 | 0 |

## Decision Gates

| Gate | Rows | Pending | Blank confirmations | Open rows | Status |
|---|---:|---:|---:|---:|---:|
| `joint_advisor_review` | 5 | 5 | 5 | 5 | present |
| `poster_review` | 5 | 5 | 5 | 5 | present |
| `current_five` | 7 | n/a | 7 | 7 | present |
| `cmp_manual_review` | 8 | 8 | 8 | 8 | present |

## Revision Execution Gate

| Matrix | Rows | Waiting | Ready to apply | Applied + verified | Basis claims | Basis errors | Coverage errors | Inconsistent | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `data/closeout/joint_decision_revision_matrix_2026-07-26.csv` | 20 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | present |

Joint decision contract errors: 0.

**Ready for final freeze: `false`.**

| Readiness blocker | Count |
|---|---:|
| `revision_rows_not_applied_verified` | 20 |

## Key Deliverables

| Path | Status | Bytes | SHA-256 |
|---|---:|---:|---|
| `data/research_package/audit_report_summary.csv` | present | 20937 | `c4fd673a115f14c6969dcaa58e50c7e1c52a23d98bb590411497cce8a078bc49` |
| `data/research_package/longitudinal_summary.csv` | present | 9141 | `f1069383db8bd2ac9b777eaefbff26d4134490c55d397198275db0f5602258c0` |
| `data/research_package/research_manifest.json` | present | 244 | `628236fe5b418dde276f9f212153fc784bd98ed34b76cd3bc57be914514bfc7f` |
| `docs/research/presentation/ssrp_consent_audit_presentation_draft_2026-07-22.pptx` | present | 1645523 | `607ab0791f0062c91ec52090d5b598d936f7de2d033de04af5fe49fb368bcd1a` |
| `docs/research/presentation/ssrp_consent_audit_presentation_draft_2026-07-22_montage.png` | present | 360887 | `ae25bd0bde2d68f5aace2a5d5d58a5be16c61b8ef2fdef376065ab74af99ebb6` |
| `docs/research/poster/ssrp_poster_aligned_review_2026-07-25.pptx` | present | 1619551 | `c2dd51ea3c7711785ecccb8850c5d6648ae65a7711fba645c13d87ce49655220` |
| `docs/research/poster/ssrp_poster_aligned_review_2026-07-25.pdf` | present | 840621 | `1cf0121ca68d8d6c1693cf623e6eb7c7e236af65bfff6d6bf8e533540661819f` |
| `docs/research/poster/ssrp_poster_aligned_review_2026-07-25.png` | present | 1694393 | `73427915c149d0fe75d74cccf838670eda109e81d4b104a3e5e39ed4a8c50f71` |
| `docs/research/joint_review/ssrp_joint_advisor_review_2026-07-25.zip` | present | 5963814 | `0b4374a85cd1c7a27f2b5307abd0d19246cb5110b4335c44b5b657e86393737a` |
| `data/joint_advisor_review_decision_sheet_2026-07-25.csv` | present | 2419 | `0789672311fde4907c93744cd0d3d27b58d3c216ef9c375bd590687d44de059d` |
| `docs/research/july26_advisor_response_and_fallback_protocol_2026-07-26.md` | present | 7170 | `99b7d03ffb15c276a678f8fabee2a50a468b0911aa385e1db82b5ca970165a9b` |
| `data/closeout/joint_decision_revision_matrix_2026-07-26.csv` | present | 13778 | `01a14c29a661280cacf742a7ea2ad51e6b4bdf37798f3a77ac19527c0179cc6f` |
| `docs/research/july26_decision_to_revision_matrix_2026-07-26.md` | present | 5453 | `a4d712da03aa4b5b80ac2410cf51bacc763ae6465f6ea1cff284eae85503e522` |
| `docs/research/closeout_control_index_2026-07-26.md` | present | 10356 | `ced66556d4bddcb3235704f8abe508afab309631ae591dc2f13c443d58b93b8a` |
| `docs/research/closeout_low_token_runbook_2026-07-27.md` | present | 6873 | `48626e174a266bfc5382ff99f7d635a7162a0be9c3c735b2638004db2002a088` |

## Limitations

- This is a pre-freeze inventory, not a final or frozen manifest.
- A missing reference records checkout availability only; it does not prove the artifact never existed.
- Recommendations and fallback labels are not counted as confirmed human decisions.
- Open decision-sheet rows are reported separately from revision execution because the documented no-response branch preserves blank confirmations.
- File hashes establish byte identity, not research validity or legal compliance.
