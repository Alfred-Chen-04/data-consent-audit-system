# Script Index

Prefer the `consent-audit` CLI for routine use. These scripts are thin wrappers
or reproducible artifact builders kept for direct execution and closeout.

## Capture and Export Wrappers

- `run_audit.py`: audit one URL.
- `run_weekly.py`: execute the dated multi-site capture pipeline.
- `access_probe.py` and `access_probe_summarize.py`: test site accessibility and
  summarize the result.
- `export_audit_reports.py`, `export_longitudinal_summary.py`, and
  `export_research_package.py`: create paper-facing tabular exports.

## Final Artifact Builders

- `build_final_evidence_cards.py`: build offline claim/source locator cards.
- `build_final_paper_docx.py`: render the final paper from its Markdown source.
- `build_cwru_print_pdfs.py`: produce exact 40 x 32 and 60 x 40 board PDFs.
- `build_final_handoff_manifest.py`: hash-check the final handoff inventory.
- `build_final_submission_bundle.py`: create the portable final submission ZIP.

## Longitudinal Closeout Builders

- `build_longitudinal_artifact_manifest.py`: hash the longitudinal evidence and
  deliverable set.
- `build_longitudinal_closeout_backup.py`: create the portable closeout backup.

## Shared Support

- `_bootstrap.py`: makes direct script execution resolve the local package.
- `__init__.py`: marks the directory as an importable package for tests.

Run scripts from the repository root with the locked environment, for example:

```bash
uv run python scripts/build_final_handoff_manifest.py
```

The exact final build order is recorded in
`../docs/research/final/FINAL_DELIVERABLES_2026-08-11.md` and verified by the
test suite.
