# SSRP Consent Interface Audit Implementation Plan

## Goal

Turn the May 29 SSRP plan into executable repo artifacts for the first research
cycle: research scaffolding, a lightweight consent-table layer, deterministic
Layer 1/2 scoring basics, capture/diff support, and tests that protect the core
audit invariants.

## Phases

| Phase | Status | Notes |
|---|---|---|
| 1. Repo grounding | complete | Read README, AGENTS, SCHEMA, CONCEPTS, proposal, docs, data summaries. |
| 2. Planning files | complete | Created persistent task, findings, and progress files in the project root. |
| 3. Test-first implementation | complete | Added tests for ConsentTable, Layer 1, tiering, and diff. |
| 4. Minimal code implementation | complete | Implemented behavior covered by tests. |
| 5. Week 1 research artifacts | complete | Added outline/sample/consent-table docs and starter CSVs. |
| 6. Verification | complete | Local `.venv` verification passes: pytest, Ruff, Mypy, compileall, and `git diff --check`. |
| 7. Capture support MVP | complete | Added deterministic fingerprinting, screenshot sanitization, and budget guard tests. |
| 8. Lightweight test environment | complete | Created ignored `.venv`, added pytest pythonpath config, and verified pytest/ruff/mypy. |
| 9. Browser capture MVP | complete | Local Playwright integration captures a static consent page and passes Layer 1. |
| 10. Layer 2 MVP | complete | Deterministic click-depth and immediate-feedback scoring with evidence. |
| 11. Partial single-site audit | complete | `run_audit` now produces partial reports when Layer 3 is not implemented. |
| 12. Consent table export | complete | `run_audit` can append paper-ready consent table rows to CSV. |
| 13. Weekly consent table export | complete | `run_weekly` can append partial weekly rows while Layer 3/storage are incomplete. |
| 14. Six-site smoke probe | complete | Added a sixth canary site, ran access probe and weekly partial audit, and saved dated CSV artifacts. |
| 15. Layer 3 text/framing rubric | complete | Added deterministic quote-validated topic/framing MVP plus unbiased-choice effort-asymmetry fallback. |
| 16. Report storage | complete | Added append-only local JSONL report storage and verified weekly smoke writes 6 reports. |
| 17. Pathway targeting refinement | complete | Added consent-context, iframe, and initial-viewport filtering to reduce false positives from page chrome/footer links. |
| 18. Evidence-card report output | complete | Report markdown now renders Layer 3 topic quotes, framing evidence, and unbiased-choice rationale. |
| 19. Weekly full-pipeline hardening | complete | Weekly CSV loading skips comment/blank rows and tests cover full Layer 1+2+3 CSV/report persistence. |
| 20. Deterministic weekly summaries | complete | `summarize_week()` now converts diff events into no-budget `WeeklySummary` objects for second-capture runs. |
| 21. Weekly summary persistence | complete | Added append-only JSONL storage for `WeeklySummary` and wired weekly runs to save diff summaries. |
| 22. Longitudinal CSV export | complete | Added a paper-facing CSV export for saved weekly summaries and change-event flags. |
| 23. Audit report CSV export | complete | Added a paper-facing CSV export for stored `AuditReport` layer scores and evidence refs. |
| 24. Research package export | complete | Added a one-command export that writes RQ1/RQ2 CSVs plus a manifest. |
| 25. Direct script execution | complete | Added shared script bootstrapping so core scripts run without manual `PYTHONPATH=src`. |
| 26. Installed CLI exports | complete | Wired `consent-audit` package commands for RQ1/RQ2/research-package exports. |
| 27. Shared audit pipeline CLI | complete | Moved live audit/weekly orchestration into package code and wired `consent-audit audit` / `weekly`. |
| 28. Site-list validation | complete | Added CSV validation for placeholders, duplicate URLs, malformed URLs, categories, and mentor-inherited counts. |
| 29. Sample readiness export | complete | Added advisor-facing readiness CSVs that merge candidates, access probes, and consent-table evidence. |
| 30. Pilot candidate expansion | complete | Expanded deep-sample candidates to 15 sites, ran pilot access probe, and regenerated readiness evidence. |
| 31. Pilot weekly capture | complete | Created weekly targets from unblocked pilot candidates, captured 7 of 8, and regenerated readiness. |
| 32. CMP/manual review queue | complete | Added a review queue export for `needs_cmp_review` sites with access/capture evidence refs and recommended actions. |
| 33. CMP/manual review worksheet | complete | Added a fillable decision worksheet for manual sample-lock review of the 8 CMP queue rows. |
| 34. Sample-lock action plan | complete | Added a readiness+worksheet action table for provisional selection, manual review, rerun, blocked, and control cases. |
| 35. Sample action queues | complete | Split the sample-lock plan into weekly shortlist, manual review, rerun, replacement, and optional-control CSV queues. |
| 36. Next weekly target export | complete | Added a site-list CSV export from weekly shortlist plus rerun queue for the next capture run. |
| 37. Four-site weekly rerun | complete | Ran the next target list; Guardian/CNN/NerdWallet wrote new captures and weekly summaries, while Booking.com failed again. |
| 38. Booking DOM fallback capture | complete | Added a `page.content()` fallback, reran Booking.com, and refreshed sample/readiness/export artifacts. |
| 39. CMP evidence review packet | complete | Added a static HTML/Markdown review packet for the 8 pending CMP/manual-review rows. |
| 40. CMP review decision suggestions | complete | Added non-final DOM-indicator suggestions for the 8 pending CMP/manual-review rows. |
| 41. CMP suggestion rerun targets | complete | Added a validated weekly site-list CSV for the 7 `rerun_fresh_context` CMP suggestions. |
| 42. CMP fresh-context rerun | complete | Captured the 7 CMP rerun targets, refreshed downstream artifacts, and preserved all 8 CMP rows for manual review. |
| 43. CMP manual review brief | complete | Added a human-facing review brief and contact sheet for deciding the 8 pending CMP rows. |
| 44. Replacement candidate probe | complete | Probed 12 replacements, fixed iframe button candidate handling, and recorded Weather.com as promising but unstable. |
| 45. Replacement probe batch 2 | complete | Probed 16 more replacements, promoted Coca-Cola through full weekly capture, hardened JSONL line-separator storage, and refreshed exports to 32 reports. |
| 46. Replacement promotion gate | complete | Added a replacement review table and expanded weekly targets so only verified full-pipeline replacements enter the next capture shortlist. |
| 47. Expanded weekly capture | complete | Captured the 5-site expanded shortlist, added Coca-Cola longitudinal stability evidence, and refreshed exports to 37 reports / 15 summaries. |
| 48. Week 2 sample freeze | complete | Froze the 5-site Week 2 capture list and added a human-confirmable CMP decision draft for the 8 pending review rows. |
| 49. Week 2 execution runbook | complete | Added the 2026-06-06 capture/export/advisor-review checklist and refreshed README status away from stale scaffolding language. |
| 50. CMP confirmation loop | complete | Added a pending confirmation sheet and commands to apply only human-confirmed CMP decisions back into the worksheet/sample-lock flow. |
| 51. Advisor update brief | complete | Added a generated Week 2 advisor brief summarizing target outcomes, research-package counts, longitudinal status, and CMP confirmation state. |
| 52. Week 2 sanity check | complete | Added a generated post-capture evidence gate that checks consent rows, screenshot/DOM/hash evidence, matching reports, and weekly summaries for the frozen target list. |
| 53. Advisor check-in index | complete | Added a generated Week 2 index linking the advisor brief, sanity check, runbook, research package, and CMP review artifacts. |
| 54. Week 2 preflight gate | complete | Added a generated pre-capture readiness check that validates targets, required artifacts, manifest counts, CMP confirmation state, and sanity status. |
| 55. Week 2 refresh orchestrator | complete | Added a one-command post-capture refresh that regenerates the research package, advisor brief, sanity check, check-in index, preflight check, and refresh report from fresh package CSVs. |
| 56. Week 2 full-cycle command | complete | Added a guarded one-command cycle that reruns preflight, blocks unsafe capture unless forced, runs weekly browser capture, refreshes outputs, and writes a cycle report. |
| 57. Weekly capture summary | complete | Added structured weekly run counts and failure details so Week 2 cycle reports attempts, successes, failures, and `needs_attention` when 2+ sites fail. |
| 58. Week 2 cycle dry run | complete | Added `week2-cycle --dry-run` so capture-day setup can rerun preflight and write a cycle report without opening browser capture or refreshing research counts. |
| 59. Dry-run report clarity | complete | Updated dry-run cycle reports to show `Cycle mode: dry_run` and the expected 5-site denominator as `0/5`, avoiding confusion with an empty target list. |
| 60. Cycle report input metadata | complete | Added target-list, consent-table, cohort, expected-target, force, and dry-run metadata to Week 2 cycle reports for post-hoc reproducibility. |
| 61. Cycle report next action | complete | Added status-specific `Next Action` guidance to Week 2 cycle reports, including a stop message for dry-run preflight warnings. |
| 62. Check-in index cycle report link | complete | Linked the Week 2 cycle report from the advisor check-in index and refresh chain so dry-run/live run evidence is reachable from the meeting entrypoint. |
| 63. Check-in index run controls | complete | Added preflight, dry-run, live cycle, and refresh commands to the advisor check-in index Run Controls section. |
| 64. Week 2 capture-day checklist | complete | Added a generated operator checklist for preflight, dry-run, live cycle, refresh, and evidence-gate confirmation. |
| 65. Post-cycle checklist sync | complete | Regenerated the capture-day checklist after final cycle report writes so last-cycle status cannot go stale. |
| 66. Aborted cycle denominator | complete | Preserved the expected target denominator in aborted Week 2 cycle reports and synced checklist status. |
| 67. Aborted cycle mode clarity | complete | Labeled preflight-blocked cycles distinctly and added a concrete rerun instruction. |
| 68. Capture limit propagation | complete | Wired weekly capture limits through the live Week 2 browser-capture call, not only post-capture exports. |
| 69. Capture limit report metadata | complete | Recorded the active capture limit in Week 2 cycle report inputs for reproducible limited runs. |
| 70. Weekly entrypoint limit option | complete | Exposed capture limits through the generic weekly CLI and legacy script entrypoint. |
| 71. Weekly entrypoint run summary | complete | Generic weekly entrypoints now print/return attempted, succeeded, failed, and budget-exceeded counts after a run. |
| 72. Weekly failure detail output | complete | Weekly run summaries now include failed site URLs and error messages when any capture fails. |
| 73. Local object-store fallback | complete | Replaced screenshot/DOM upload stubs with a local object-store fallback that sanitizes screenshots and rejects unsafe keys. |
| 74. LLM/VLM wrapper fallbacks | complete | Replaced text/vision wrapper stubs with budget-logged deterministic fallbacks that preserve evidence discipline and avoid hallucinated visual candidates. |
| 75. Weekly site-list preflight gate | complete | Weekly browser capture now reuses site-list validation and fails before capture when placeholders, duplicates, or malformed URLs are present. |
| 76. Weekly invalid-site-list operator output | complete | Weekly CLI/script entrypoints now print concise exit-1 validation messages when the preflight gate rejects a site list. |
| 77. Access-probe site-list preflight gate | complete | Access probe now rejects invalid/placeholder site lists before launching browser capture. |
| 78. Package access-probe command | complete | Access-probe logic now lives in the package CLI while the legacy direct script remains a thin wrapper. |
| 79. Package access-probe summary command | complete | Access-probe CSV summary logic now lives in the package CLI while the legacy script remains a thin wrapper. |
| 80. Research status dashboard | complete | Added a package CLI dashboard that summarizes current targets, artifact counts, preflight/sanity/cycle statuses, CMP confirmations, and next action. |
| 81. SCHEMA status sync | complete | Updated the project navigator away from stale stub/scaffold language toward the current Week 2 executable workflow and remaining research gates. |
| 82. SSRP paper skeleton export | complete | Added a package CLI generator that turns current RQ1/RQ2 research-package CSVs into a paper-writing skeleton with snapshot counts, target evidence table, table plan, figure queue, and known gaps. |
| 83. Week 2 schedule guard | complete | Added a scheduled-date block so live `week2-cycle` cannot write a 2026-05-30 observation into the 2026-06-06 cohort unless `--allow-early` is explicitly used. |
| 84. SSRP results tables export | complete | Added a package CLI generator and refresh-chain integration for paper-ready RQ1/RQ2 Markdown tables from the current research package. |
| 85. Research-status paper artifact links | complete | Updated the one-screen dashboard to show whether paper skeleton/results tables are present and link both artifacts from the key-artifacts block. |
| 86. SSRP figure plan export | complete | Added a package CLI generator, refresh-chain integration, research-status link, and current artifact for paper/poster figures. |
| 87. SSRP writing pack export | complete | Added a package CLI generator, refresh-chain integration, research-status link, and current artifact for draftable paper notes. |
| 88. SSRP claim register export | complete | Added a package CLI generator, refresh-chain integration, research-status link, and current artifact for evidence/status-labeled paper claims. |
| 89. SSRP poster plan export | complete | Added a generated poster storyboard/asset/checklist artifact wired into CLI, refresh outputs, and research-status. |
| 90. SSRP remaining-work audit | complete | Created a requirement-by-requirement audit of what is complete, provisional, blocked by schedule, or still missing. |
| 91. CMP confirmation request | complete | Added an advisor-facing request doc to resolve the 8 pending CMP/manual-review confirmations. |
| 92. Project clarity handoff | complete | User clarified the goal is not implementation; added a Chinese project map and next-step plan for the 10-week SSRP research cycle. |
| 93. Advisor meeting PM brief | complete | Added a Chinese PM-style meeting brief with task breakdown, execution paths, source documents, and mentor talking points. |
| 94. Folder structure guide | complete | Added a Chinese guide explaining top-level files/folders, purposes, completion state, and overall progress. |
| 95. Advisor response action plan | complete | Recorded Dr. Singh's June 5 guidance: keep RQ1/RQ2, treat no-banner rows as contrasts, use ~20 deep sites as paper sample, and keep the 80-ish list as scalable tracker/candidate pool. |
| 96. Advisor update drafts | complete | Added a ready-to-send June 5 advisor email draft and a June 6 post-capture update template with capture results, sample logic, paper structure, and scaling plan sections. |
| 97. Advisor packet index | complete | Added a one-file advisor communication entrypoint that links the send-now draft, post-capture template, confirmed decisions, current facts, non-claims, open questions, and June 6 work order. |
| 98. Week 2 dry-run rehearsal | complete | Ran `week2-cycle --dry-run` on 2026-06-05; preflight is ready, browser capture was not run, and the cycle/checklist now point to live `week2-cycle` as the next action. |
| 99. Advisor guideline alignment audit | complete | Audited current materials against Dr. Singh's June 5 guidance, refreshed generated paper/advisor artifacts to the latest `dry_run` status, and added a concise direction guardrail document. |
| 100. Week 2 live capture | complete | Ran the scheduled 2026-06-06 live Week 2 cycle: 5/5 capture attempts succeeded, research package now has 42 audit reports and 20 longitudinal summaries, and sanity is `ready`. |
| 101. Week label bug fix | complete | Fixed weekly summary dating so Week 2 scheduled captures use the cohort week label instead of UTC `datetime.now()`, then corrected the five affected Week 2 summary rows to `2026-06-06`. |
| 102. Post-capture advisor package | complete | Refreshed results tables, paper/poster artifacts, claim register, README/SCHEMA/status docs, and added a June 6 evidence-based advisor email draft. |
| 103. Standalone Week 2 CLI path fix | complete | Corrected `week2-sanity-check` and `advisor-update-brief` defaults so standalone commands read the refreshed research-package CSVs and preserve the completed Week 2 `ready` status. |
| 104. No-visible-banner evidence correction | complete | Added `banner_detected` to audit exports, regenerated paper-facing materials with banner_present=2 and no_visible_banner=3, and added a direct June 8 next-step advisor email draft. |
| 105. June 11 daily review and evidence cards | complete | Ran the daily status/sanity checks, documented the no-capture daily routine, and added two minimal banner-present evidence cards for The Guardian and Coca-Cola. |
| 106. June 13 capture decision packet | complete | Prepared a current-five continuity target list and a decision packet explaining when to run the next live capture versus wait for advisor sample decisions. |
| 107. June 14 failed capture evidence audit | complete | Attempted the prepared Week 3 current-five capture, recorded the 0/5 browser navigation failure, cross-checked HTTP reachability, and documented why no Week 3 RQ1/RQ2 result should be inferred. |
| 108. June 15 project audit and advisor email | complete | Audited current project facts, fixed stale README/SCHEMA navigation wording, and added the latest sendable advisor email reflecting the failed June 14 capture attempt. |
| 109. June 15 Coca-Cola smoke capture | complete | Ran a one-site `--no-save` Coca-Cola smoke after the June 14 failure; browser capture succeeded with screenshot/DOM evidence, but automated Layer 1 missed visible OneTrust controls. |
| 110. OneTrust pathway recognition fix | complete | Fixed OneTrust preference-center label classification, delayed CMP replay waits, and aria-label button clicking; post-fix Coca-Cola smoke now passes all Layer 1 paths. |
| 111. June 16 fact-consistency review | complete | Rechecked Git/research status and corrected stale June 15 wording so it no longer implied the OneTrust blocker remained unresolved after the post-fix smoke. |
| 112. June 18 current work note | complete | Added a fact-only daily work note after PR #4 merged and confirmed the research dashboard remained at 42 reports, 20 summaries, and 8 CMP pending confirmations. |
| 113. June 19 current-five evidence packet | complete | Consolidated the five Week 2 site evidence refs and screenshot interpretations into one current-five packet for advisor/user decision making. |
| 114. June 19 current-five decision sheet | complete | Added a fillable CSV for the five site decisions, the no-visible-banner table rule, and the next work mode. |
| 115. June 19 advisor decision email | complete | Added a short sendable email asking only for current-five treatment, no-visible-banner handling, and next work mode. |
| 116. June 19 publish check | complete | Verified the local branch is clean and testable, confirmed the matching GitHub branch is absent, and recorded that sandboxed GitHub write attempts timed out before approval. |
| 117. June 20 daily evidence gate | complete | Rechecked local/GitHub/research status, confirmed the remote branch is still absent, and added a June 20 work note that blocks blind capture until current-five decisions are recorded. |
| 118. June 22 GitHub PR publication | complete | Pushed `codex/june18-current-work-note`, created draft PR #5, synced the branch with latest `main`, and added a June 22 work note with the PR URL and validation status. |
| 119. June 25 fact-consistency audit | complete | Audited recent PR/publication notes against GitHub, local Git, `research-status`, targeted tests, and the current-five decision sheet; corrected stale PR #5 draft/count wording and added a June 25 fact-audit note. |

## Decisions

- Work on branch `codex/ssrp-plan-mvp`, not `main`.
- Treat SOC 2 as a discussion implication only, not the core research frame.
- Default sample strategy: focused deep sample first, broader 80+ tracking only if time permits.
- Preserve evidence traceability and deterministic scoring boundaries.
- 2026-06-05 advisor response resolves three pending sample questions: RQ1/RQ2 remain on track, no-banner rows are contrast cases, and the SSRP paper should prioritize a deeper fewer-site sample that can scale later.

## Errors Encountered

| Error | Attempt | Resolution |
|---|---|---|
| `uv` unavailable | `uv run pytest -q` | Record environment blocker; use available Python checks where possible. |
| `pytest` unavailable in available Python environments | `python -m pytest -q` | Tests can be added but not run until dev dependencies are installed. |
| Package import failed in pytest | `.venv/bin/python -m pytest -q` | Added `pythonpath = ["src"]` to pytest config. |
| Layer 3 stub stopped single-site report generation | `scripts/run_audit._run` with Layer 3 patched to raise | Catch `NotImplementedError` and emit a partial report. |
| Weekly pipeline stopped on unimplemented Layer 3/storage | `scripts/run_weekly._audit_one` with patched stubs | Catch `NotImplementedError`, record warning notes, and still append a consent-table row. |
| Direct script execution could not import `consent_audit` from `.venv` | `.venv/bin/python scripts/run_weekly.py --help` | Use `PYTHONPATH=src` for local script runs until the package is installed editable. |
| Consent table marked every page snapshot as a banner | Six-site weekly smoke audit | Changed `banner_detected` to use pathway candidates rather than mere presence of a screenshot layer. |
| Access probe did not count HTTP 401 as blocked/error | Reuters smoke probe returned 401 while summary said `blocked_or_error=0` | Added HTTP status block signals such as `http_401`. |
| BBC/Guardian smoke rows contained pathway false positives | Weekly smoke audit after first capture MVP | Added consent-context filtering so generic labels like `Settings`/`Allow` require cookie/privacy context. |
| Guardian Sourcepoint iframe was not inspected | Local iframe fixture failed Layer 1 | Extended candidate extraction and click attempts across Playwright frames. |
| Hidden/offscreen privacy links were counted as consent controls | Guardian screenshot showed no visible banner while iframe text was detected | Added initial-viewport bounding-box filtering for candidate controls. |
| Layer 3 was still a hard stub | `tests/layers/test_layer3_transparency.py` failed with `NotImplementedError` | Implemented deterministic topic coverage, framing, and unbiased-choice scoring with verbatim quote validation discipline. |
| Layer 3 report text only showed two grades | `tests/report/test_generator.py` lacked evidence-card assertions | Expanded report markdown with topic coverage rows, quote fields, framing findings, and unbiased-choice details. |
| Weekly pipeline treated comment rows as URLs | `tests/scripts/test_run_weekly.py` passed a `# Replace...` CSV row into `_audit_one` | Added `_load_urls()` to skip blank/comment rows like the access probe does. |
| Second weekly capture would hit a summary stub | `tests/diff/test_engine.py` called `summarize_week()` with pathway/score changes | Implemented deterministic no-budget `WeeklySummary` generation. |
| Weekly summaries were generated but discarded | Second-report weekly test expected saved longitudinal evidence | Added `save_weekly_summary()` and `list_weekly_summaries_for_url()` JSONL storage, then saved summaries from `run_weekly`. |
| Longitudinal evidence was queryable but not paper-ready | Export tests expected one CSV row per `WeeklySummary` with event flags | Added `consent_audit.longitudinal_export` and `scripts/export_longitudinal_summary.py`. |
| Stored audit reports were not directly paper-ready | Export tests expected one CSV row per `AuditReport` with layer grades and evidence refs | Added `consent_audit.audit_export`, `scripts/export_audit_reports.py`, and `list_reports()`. |
| Research exports required remembering multiple commands | Package export test expected both CSVs and a manifest from one command | Added `scripts/export_research_package.py`. |
| Targeted Mypy could not resolve local package when run on scripts alone | `.venv/bin/python -m mypy scripts/export_*.py` | Use the project verification shape with `src` included in the Mypy invocation. |
| Core scripts failed when run directly from repo root | Direct `--help` smoke test without `PYTHONPATH` failed with `ModuleNotFoundError: consent_audit` | Added `scripts/_bootstrap.py` and a direct-execution smoke test for core script entrypoints. |
| Bootstrap helper had two import identities under Mypy | Mypy saw `_bootstrap` and `scripts._bootstrap` | Added `scripts/__init__.py` and made entrypoints import `scripts._bootstrap` after adding repo root to `sys.path`. |
| Package CLI entrypoint was still a stub | `tests/test_cli.py` expected export commands in Typer help | Added real `consent-audit export-audit-reports`, `export-longitudinal-summary`, and `export-research-package` commands. |
| Live package CLI commands still pointed users back to scripts | CLI tests expected `audit` and `weekly` to call a package pipeline | Added `consent_audit.pipeline` and made both CLI and script wrappers call it. |
| Sample CSV could silently run a placeholder site | `data/sites.csv` still contains `https://example.com` | Added `validate-sites` and a reusable validator that fails on placeholder URL/category rows. |
| Direct module execution could not resolve local package outside pytest | `.venv/bin/python -m consent_audit.cli validate-sites ...` | Used `PYTHONPATH=src` for local module smoke checks; README keeps the intended `uv run consent-audit ...` package entrypoint. |
| Deep candidate review required manually joining three CSVs | Candidates, access probe, and consent table lived separately | Added `sample-readiness` to export one advisor-facing merged review table. |
| Candidate table was still smoke-only and included `example.com` | New research artifact test expected 10-15 pilot candidates across categories | Replaced it with 15 public pilot candidates and regenerated readiness outputs. |
| Pilot readiness could not combine smoke and pilot consent tables | `sample-readiness` accepted only one consent table path | Added multi-consent-table support and defaulted the CLI to smoke + pilot evidence. |
| Booking.com pilot weekly capture failed during navigation | `weekly` logged `Page.content: Unable to retrieve content because the page is navigating and changing the content.` | Left Booking.com as `needs_weekly_capture` in readiness and recorded it as a sample-feasibility issue. |
| `needs_cmp_review` rows were not directly actionable | Readiness only gave a status, not a compact evidence-review queue | Added `cmp-review-queue` with access screenshots, capture screenshots/DOM, hashes, review reason, and recommended action. |
| CMP review had no structured place to record human decisions | Queue rows told the reviewer what to inspect but not how to record sample-lock outcomes | Added `cmp-review-worksheet` with blank manual review fields and fixed decision options. |
| Candidate readiness still required mental sorting before sample lock | Readiness and worksheet rows did not state which sites were selected, blocked, pending, or due for rerun | Added `sample-lock-plan` to produce an action table and summary counts. |
| Sample-lock plan still required manual filtering into work queues | One action table mixed weekly capture, manual review, rerun, replacement, and control tasks | Added `sample-action-queues` to write separate queue CSVs plus a manifest. |
| Action queues were not yet a direct weekly pipeline input | Shortlist and rerun rows lived in separate queue CSVs with extra columns | Added `sample-weekly-targets` to merge them into a normal validated site-list CSV. |
| Booking.com failed again during rerun capture | `weekly` logged `Page.content: Unable to retrieve content because the page is navigating and changing the content.` | Preserve it as `needs_weekly_capture` / rerun queue evidence; review or replace if repeated. |
| Booking.com dynamic navigation prevented DOM snapshot capture | Booking-only rerun reproduced the same `Page.content` navigation churn failure before any consent-table row was written | Added `snapshot_dom_html()` fallback to `document.documentElement.outerHTML`; Booking.com now writes screenshot, DOM, consent-table row, and report with a capture warning. |
| CMP review evidence was split across CSV columns | Manual sample-lock review required opening queue/worksheet CSVs and copying screenshot/DOM paths by hand | Added `cmp-review-packet` to write `index.html` and `index.md` cards with screenshots, DOM links, reasons, actions, and decision options. |
| CMP review still lacked a first-pass triage recommendation | Packet cards made evidence visible but left all worksheet decisions blank | Added `cmp-review-suggestions`, a non-final DOM-indicator CSV with suggested decisions and mandatory human-confirmation flags. |
| CMP rerun suggestions were not yet executable by the weekly pipeline | Suggestions identified 7 fresh-context reruns but were not in site-list shape | Added `cmp-review-rerun-targets` to write a normal validated site-list CSV and exclude the Reddit no-banner suggestion. |
| Ad-hoc sample-lock counter used an obsolete column name | A quick CSV inspection script tried to count `sample_action` in `sample_lock_plan`, which now uses `lock_status` | Re-read the CSV header and used the generated command summaries/artifact tests as authoritative counts. |
| CMP review still required reading multiple artifacts at once | Packet, suggestions, consent table rows, and longitudinal rows each exposed part of the decision context | Added `docs/research/cmp_manual_review_brief_2026-05-30.md` plus a contact sheet to make the human review decision explicit. |
| Weather.com exposed iframe consent controls but Layer 1 missed them | Sourcepoint-style nested iframe buttons had tiny local context, while a broad aria dialog was misclassified as Accept | Added regression coverage and updated candidate collection to use consent-bearing ancestor context and skip non-interactive aria containers. |
| Weather.com click attempts failed on duplicate hidden text | The click helper only tried the first exact text match, which can be hidden in CMP UIs | Updated clicking to iterate visible duplicate text matches across frames. |
| Ad-hoc JSONL parsing failed on Coca-Cola report text | `Path.read_text().splitlines()` split one JSON record at literal U+2028 line-separator characters inside captured page text | Confirmed file iteration had 32 valid records, added regression tests, changed JSONL writes to `ensure_ascii=True`, normalized existing JSONL, and regenerated exports. |
| Local one-off Python commands could not import `consent_audit` without package context | `.venv/bin/python - <<'PY'` was run without `PYTHONPATH=src` | Reran with `PYTHONPATH=src`; package CLI/module commands continue to use that local development prefix when not installed editable. |
| Expanded weekly target generation initially failed | `replacement-review` and `expanded-weekly-targets` were launched in parallel, so the expanded target command read the review CSV before it existed | Reran dependent commands sequentially and recorded the dependency; replacement review must be generated before expanded targets. |
| Ruff reported unsorted CLI imports | `.venv/bin/python -m ruff check src tests scripts` after adding replacement review imports | Ran Ruff's import-sort fix for `src/consent_audit/cli.py` and reran full verification. |
| Stable repeated captures disappeared from RQ2 export | Coca-Cola had a second `Compliant` `AuditReport` but no `WeeklySummary` because the pipeline saved summaries only when change events existed | Added a regression test, removed the `if events` guard, backfilled Coca-Cola's no-change summary, and refreshed longitudinal exports. |
| Aborted Week 2 cycle reports hid the expected target count | New regression expected an aborted preflight cycle to show `Capture attempts: 0/5` instead of `0/0` | Added zero attempt/success/failure counts and the expected target denominator to the aborted summary branch. |
| Aborted Week 2 cycle reports looked like live captures | New regression expected preflight-blocked reports to avoid `Cycle mode: live_capture` | Added a `preflight_blocked` cycle mode and a concrete next action for aborted cycles. |
| Week 2 cycle `limit` did not limit live capture | New regression expected the live capture call to receive `limit=3`, and the weekly pipeline to audit only two URLs when called with `limit=2` | Added optional `limit` support to `run_weekly_audit()` and passed the Week 2 cycle limit into the live capture call. |
| Week 2 limited capture was not reconstructable from the cycle report | New regression expected `Capture limit: 3` in the report inputs | Added the cycle limit to report input metadata and rendered it in the `Inputs` section. |
| Generic weekly entrypoints could not request limited capture | New regressions expected `consent-audit weekly --limit 2` and `scripts/run_weekly._run(limit=2)` to pass the limit into the pipeline | Added `limit` options to both entrypoints and forwarded them to `run_weekly_audit()`. |
| Targeted pytest command used stale test names | Attempted CLI weekly nodes that did not exist | Used `rg` to locate the actual `test_cli_weekly_invokes_weekly_pipeline` node and reran the targeted set. |
| Ruff rejected new weekly script import ordering | `ruff check` after importing `scripts.run_weekly` in tests | Ran Ruff import sorting on `tests/scripts/test_run_weekly.py`. |
| Generic weekly entrypoints completed silently | New regressions expected `weekly` CLI output and script `_run()` return values to expose run counts | Added shared `format_weekly_run_summary()`, echoed it from both command entrypoints, and returned `WeeklyRunSummary` from the script wrapper. |
| Weekly formatter failure details broke an older fake summary | Targeted regression suite failed because the CLI test fake lacked the new `failures` field | Updated the test fixture to match the `WeeklyRunSummary` formatter contract. |
| Ruff rejected new formatter test import ordering | `ruff check` after importing `WeeklyRunSummary` / `WeeklySiteFailure` in `tests/scripts/test_run_weekly.py` | Reordered imports according to Ruff/isort. |
| Object-store uploads were still hard stubs | New storage tests expected screenshot sanitization, DOM copying, and safe-key validation | Added a local `data/object_store` fallback with `sanitize_screenshot()` before screenshot copy and path-traversal rejection. |
| Initial object-store patch missed the real file context | `apply_patch` expected an import that was not yet present | Re-read `src/consent_audit/storage/object_store.py` and applied a smaller patch against the actual stub. |
| LLM/VLM wrappers were still hard stubs | New wrapper tests expected budget logging, clean budget failures, verbatim text evidence, and no hallucinated visual candidates | Added deterministic no-network fallbacks to `llm/text.py` and `llm/vision.py` with ledger entries before extraction. |
| Weekly capture could still run placeholder site lists | New regression expected `run_weekly_audit()` to reject `https://example.com` before calling capture | Added `validate_site_list()` at the start of weekly runs and raised a clear validation error with issue codes. |
| Week 2 live capture could be run before its scheduled cohort date | New regression expected a 2026-05-30 run against `week_of=2026-06-06` to stop before browser capture | Added explicit `run_date` / `allow_early` handling, a `scheduled_date_not_reached` report state, and CLI output that tells the operator to wait until 2026-06-06 or consciously override with `--allow-early`. |
| Paper skeleton named RQ1/RQ2 tables but did not generate them | New regressions expected a concrete `ssrp-results-tables` command and `docs/research/ssrp_results_tables_2026-06-06.md` artifact | Added `consent_audit.paper_tables`, CLI command `ssrp-results-tables`, and integrated both tables and the paper skeleton into `week2-refresh-outputs`. |
| Research-status hid the new paper artifacts | New regression expected `research-status` to show paper skeleton/results table presence and paths | Added `results_tables_md` and `paper_skeleton_md` inputs to the renderer and CLI defaults so the dashboard is a true paper-writing entrypoint. |
| June 16 fact-consistency review | June 15 docs still contained a pre-fix OneTrust recommendation that could be read as current guidance | Checked current Git/research status and corrected stale June 15 wording so it no longer implies the OneTrust blocker remains unresolved after the post-fix Coca-Cola smoke. |
| June 18 current-work note | No 2026-06-18 handoff existed after PR #4 merged and the research status remained unchanged | Added a fact-only daily work note and linked it from README and the advisor check-in index. |
| June 19 current-five evidence packet | Existing evidence cards covered only the two banner-present cases, while the advisor decision also depends on the three no-visible-banner contrast candidates | Re-read the manual evidence worksheet, research-package summaries, and screenshots; added a five-site evidence packet with source refs and cautions. |
| June 19 current-five decision sheet | The evidence packet still required a separate place to record advisor/user choices | Added a fillable CSV decision sheet for the five site-level decisions plus the no-visible-banner table rule and next-work mode. |
| June 19 short advisor decision email | The June 15 advisor email was evidence-rich but long; the new decision sheet needed a concise sendable prompt | Added a short advisor email that asks only for current-five treatment, no-visible-banner table rule, and next-work mode decisions. |
| June 19 GitHub publish blocked by sandbox approval | `git push -u origin codex/june18-current-work-note` failed on SSH port 22 in the sandbox, two escalated retries timed out before approval, and GitHub API branch creation also timed out before approval | Do not repeat the same sandbox push loop; have the user run `git push -u origin codex/june18-current-work-note` locally or retry only after explicit external write approval. |
| June 20 daily evidence gate | The project could drift into another blind capture even though the remote branch is still absent and no current-five decision is recorded | Added `docs/research/today_work_note_2026-06-20.md` with verified GitHub/local/research status and a concrete no-capture/publish/email next-action gate. |
| June 22 GitHub PR publication | The branch was previously local-only, so the advisor decision packet was not visible as a GitHub PR | Pushed the branch, created draft PR #5, merged latest `origin/main` into the branch to make GitHub compare `behind_by=0`, and recorded the PR URL in `docs/research/today_work_note_2026-06-22.md`. |
| June 25 stale PR #5 status in recent notes | PR #5 had been merged, but recent notes still read like draft/open publication state and older PR counts | Corrected the June 22 note, added the June 25 fact-audit note, and updated README/index/planning records to point at the merged-PR status and the remaining decision-sheet blocker. |
