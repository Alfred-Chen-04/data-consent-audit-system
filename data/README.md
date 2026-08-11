# Data and Evidence Index

This directory combines final evidence tables, controlled captures, closeout
records, generated exports, and dated pilot inputs. The date and role of a file
matter; not every CSV is a final dataset.

## Final Evidence

| Path | Role |
|---|---|
| `final_claim_evidence_matrix_2026-08-11.csv` | Final RQ claim-to-evidence chain and limitations |
| `retrospective_longitudinal_cases_2026-07-29.csv` | Six coded company trajectories used in the final case series |
| `retrospective_source_registry_2026-07-29.csv` | Twelve dated primary/context sources and exact claim locators |
| `final_source_card_manifest_2026-08-11.csv` | Hash inventory for offline source cards |
| `final_handoff_manifest_2026-08-11.json` | Hash inventory for the final handoff |
| `final_submission_bundle_manifest_2026-08-11.csv` | Contents and hashes for the portable submission ZIP |
| `captures/` | Controlled screenshot evidence retained by the local pipeline |

## Closeout and Decisions

- `closeout/`: final QA, project-owner decisions, advisor-decision history, and
  the CWRU requirement audit.
- `longitudinal_artifact_manifest_2026-07-30.json`: reproducibility manifest for
  the six-case longitudinal revision.
- `longitudinal_directional_review_2026-07-29.csv`: conservative review of the
  five-site local matched interval; all directions remain insufficient.

## Generated Research Outputs

- `reports/`: append-only JSONL audit reports and weekly summaries.
- `research_package/`: paper-facing export package and manifest.
- `audit_report_summary.csv` and `longitudinal_summary.csv`: flattened current
  exports from the controlled local pipeline.

## Pilot and Intermediate Files

Root-level files containing `pilot`, `smoke`, `replacement`, `week2`, or
`week3` are dated execution inputs, review queues, or intermediate outputs.
They are retained for provenance and testing. They are not a single final
analysis table. In particular, `sites.csv` remains a scaffold input; the frozen
Week 2 target list is `week2_deep_sample_targets_2026-06-06.csv`.

Generated files should normally be refreshed through the CLI or the builders
documented in `../scripts/README.md`, not edited in place.
