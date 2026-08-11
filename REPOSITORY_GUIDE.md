# Repository Guide

This is the current map for the completed SSRP 2026 project. It explains where
to start without changing the stable paths used by evidence manifests, tests,
and dated research records.

## Fast Routes

| Task | Start here |
|---|---|
| Submit or hand off the project | `docs/research/final/FINAL_DELIVERABLES_2026-08-11.md` |
| Read the final English result | `docs/research/final/final_results_brief_2026-08-11.md` |
| Read the Chinese summary | `docs/research/final/项目最终结论与展示提纲_2026-08-11.md` |
| Give the presentation | `docs/research/presentation/README.md` |
| Print or edit the poster | `docs/research/poster/README.md` |
| Audit the evidence chain | `docs/research/final/evidence_chain_audit_2026-08-11.md` |
| Understand the method | `CONCEPTS.md`, then `SCHEMA.md` and `docs/architecture.md` |
| Reproduce or test the code | `README.md`, `scripts/README.md`, and `tests/` |
| Review the dated work history | `docs/research/README.md` |

## Directory Map

| Path | Role | Status |
|---|---|---|
| `docs/research/final/` | Paper, final results, evidence audit, CWRU closeout, registration text, and portable submission bundle | Final |
| `docs/research/presentation/` | Current rehearsal-ready deck plus earlier deck versions | Current + history |
| `docs/research/poster/` | Current poster, board-size print PDFs, and earlier poster versions | Current + history |
| `docs/research/joint_review/` | July advisor-review bundle | Historical |
| `docs/research/project_log/` | Long-running task, finding, and progress records moved from the repository root | Historical |
| `docs/research/*.md` | Dated research notes, audits, plans, and advisor drafts | Historical unless an index says otherwise |
| `data/` | Capture evidence, coded cases, source registry, decision records, exports, and manifests | Evidence + generated outputs |
| `src/consent_audit/` | Auditing, capture, scoring, diff, storage, and reporting implementation | Code |
| `scripts/` | Direct wrappers and reproducible artifact builders | Code |
| `tests/` | Unit, integration, artifact, and closeout checks | Verification |
| `docs/related_work/` | Literature and legal background | Research support |
| `docs/references/` | Archived-source notes and reference instructions | Research support |
| `docs/outreach/` | Networking and outreach drafts | Historical/support |
| `docs/strategy/` | Positioning and possible future extensions | Non-final strategy |
| `Qiyao's data collection_0912/` | Auxiliary 2025 collection inherited for background comparison | Auxiliary, not final sample |
| `archive/local_recovery_2026-08-11/` | Historical patches and external closeout backups recovered from outside the active repository before computer handoff | Recovery archive |

## Root Files

- `README.md`: short public entrypoint and development commands.
- `CONCEPTS.md`: canonical audit ontology and interpretation rules.
- `SCHEMA.md`: one-page research-question-to-system map.
- `AGENTS.md`: repository collaboration rules.
- `pyproject.toml` and `uv.lock`: Python project and locked dependencies.
- `Chen_Qianyi_SSRP 2026_Proposal_Final Version.docx.pdf`: original proposal.

## Status Labels

- **Final**: use for submission or claims. These files live primarily under
  `docs/research/final/` and are hash-indexed.
- **Current**: use operationally, such as the rehearsal-ready presentation and
  the July 30 poster.
- **Historical**: retain for provenance, but do not treat as the latest result.
- **Auxiliary**: background material that is not part of the final analyzed
  sample.
- **Generated**: reproducible exports or manifests; inspect their source script
  before editing by hand.

## Preservation Rules

1. Do not move or rename final artifacts, capture evidence, source cards, or
   files listed in a hash manifest without regenerating and revalidating the
   affected manifests.
2. Keep dated notes even when superseded. Their dates and original scope are
   part of the project record.
3. Put new final-facing material in `docs/research/final/`; put new engineering
   guidance beside the code or in `docs/`.
4. Use the directory README files as navigation rather than adding another
   long flat list to the repository root.

No research artifact was deleted during this organization pass. Most dated
files remain in place because their paths are already referenced by tests,
indexes, manifests, and other records.
