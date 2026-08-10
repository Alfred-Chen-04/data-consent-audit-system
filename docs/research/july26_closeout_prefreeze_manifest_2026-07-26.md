# SSRP Closeout Pre-Freeze Manifest

**Status: `pre_freeze` - this is not a final or frozen manifest.**

Generated at: `2026-08-10T06:45:30.754129+00:00`

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
| `data/closeout/joint_decision_revision_matrix_2026-07-26.csv` | 20 | 0 | 0 | 20 | 20 | 0 | 0 | 0 | present |

Joint decision contract errors: 0.

**Ready for final freeze: `true`.**

| Readiness blocker | Count |
|---|---:|
| none | 0 |

## Key Deliverables

| Path | Status | Bytes | SHA-256 |
|---|---:|---:|---|
| `data/research_package/audit_report_summary.csv` | present | 20937 | `c4fd673a115f14c6969dcaa58e50c7e1c52a23d98bb590411497cce8a078bc49` |
| `data/research_package/longitudinal_summary.csv` | present | 9141 | `f1069383db8bd2ac9b777eaefbff26d4134490c55d397198275db0f5602258c0` |
| `data/research_package/research_manifest.json` | present | 244 | `628236fe5b418dde276f9f212153fc784bd98ed34b76cd3bc57be914514bfc7f` |
| `docs/research/presentation/ssrp_consent_audit_presentation_closeout_2026-07-29.pptx` | present | 1645273 | `590ff39f334141da4122c2831df98b43ba5c4c4f54c5a2526c4f7e6a6f6afe9e` |
| `docs/research/presentation/ssrp_consent_audit_presentation_closeout_2026-07-29_montage.png` | present | 361121 | `f82ed08fd38eedb87ccfa239960dfdc28dd1f163cba998c0b1b80c3d277c3c49` |
| `docs/research/poster/ssrp_poster_closeout_2026-07-29.pptx` | present | 1619230 | `97ee28d64bb20f2b1d1b2712a29c5159a4c1dcbf75e6bd85f2add8ccb4c4b398` |
| `docs/research/poster/ssrp_poster_closeout_2026-07-29.pdf` | present | 840603 | `6bd9dbdef0afff18cfefc0888838fb0035c6879b1dceaa89478036b2969255c3` |
| `docs/research/poster/ssrp_poster_closeout_2026-07-29.png` | present | 1677500 | `747a41452e05059eb0658f0441806ba2c2d43274e9ca8d8fb3c089995a232845` |
| `docs/research/joint_review/ssrp_joint_advisor_review_2026-07-25.zip` | present | 5963814 | `0b4374a85cd1c7a27f2b5307abd0d19246cb5110b4335c44b5b657e86393737a` |
| `data/joint_advisor_review_decision_sheet_2026-07-25.csv` | present | 2419 | `0789672311fde4907c93744cd0d3d27b58d3c216ef9c375bd590687d44de059d` |
| `data/closeout/project_owner_decision_sheet_2026-07-29.csv` | present | 1825 | `dc47a8e55df8cd645faf88c995b519a6de15ce25f1dd5c55ba0a87d6a31dae0b` |
| `docs/research/july29_project_owner_closeout_decisions_2026-07-29.md` | present | 2123 | `6bb9eb375b03a19811acc3c5e6c8680506e1ed15235feb79d2eb6f443e892317` |
| `docs/research/july26_advisor_response_and_fallback_protocol_2026-07-26.md` | present | 7696 | `c215674d2752b99141ff8db112d0ddac1ab33d9cfaad9d5c25a9518b8417775b` |
| `data/closeout/joint_decision_revision_matrix_2026-07-26.csv` | present | 15752 | `d8466173126bc85bddfb8dcc5fcd8d1ef82d42ee278346f0e6344cfadbeed8a1` |
| `docs/research/july26_decision_to_revision_matrix_2026-07-26.md` | present | 6019 | `9148a643f6f88794083a27029277d47607b2da09c20ba930e4a4ab6459666dce` |
| `docs/research/closeout_control_index_2026-07-26.md` | present | 17622 | `80567fe689c433d3fe54a5f98ea6db5627ab6ef86795d82cb1c57e826bc172b9` |
| `docs/research/closeout_low_token_runbook_2026-07-27.md` | present | 5577 | `cc663f92c6719d0c6ca9307b7f979bf7f737b4ca17b884357841a60719049d96` |
| `data/closeout/final_qa_checklist_2026-07-27.csv` | present | 2756 | `8fd99209c8d94e8578d46df875feecff8748971d26b53d3bf625c44d152ba36c` |

## Limitations

- This is a pre-freeze inventory, not a final or frozen manifest.
- A missing reference records checkout availability only; it does not prove the artifact never existed.
- Recommendations and fallback labels are not counted as confirmed human decisions.
- Open decision-sheet rows are reported separately from revision execution because the documented no-response branch preserves blank confirmations.
- File hashes establish byte identity, not research validity or legal compliance.
