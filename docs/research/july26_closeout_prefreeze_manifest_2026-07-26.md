# SSRP Closeout Pre-Freeze Manifest

**Status: `pre_freeze` - this is not a final or frozen manifest.**

Generated at: `2026-07-26T12:21:10.210044+00:00`

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
| `docs/research/joint_review/ssrp_joint_advisor_review_2026-07-25.zip` | present | 5964170 | `98b2c7b779a9a4b451c6cde992fee9c582b56ebdc90872c9d09169548de00fdd` |
| `data/joint_advisor_review_decision_sheet_2026-07-25.csv` | present | 2493 | `875a708c56ccfa44301762df93740597df0d2eab71667b6670e75646fbd91888` |
| `docs/research/july26_advisor_response_and_fallback_protocol_2026-07-26.md` | present | 6301 | `8f53bdafd5d088390dfdafad294c38b8657d19847c3647dcd3d958bcae4bc070` |

## Limitations

- This is a pre-freeze inventory, not a final or frozen manifest.
- A missing reference records checkout availability only; it does not prove the artifact never existed.
- Recommendations and fallback labels are not counted as confirmed human decisions.
- File hashes establish byte identity, not research validity or legal compliance.
