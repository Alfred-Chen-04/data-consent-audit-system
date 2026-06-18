# Findings

## Repo State

- Project is a Python 3.11+ package named `consent-audit`.
- The docs are mature: `SCHEMA.md` defines the research spine and open decisions, `CONCEPTS.md` defines the audit ontology, and `docs/architecture.md` defines runtime boundaries.
- Code was mostly scaffolded at the start of this pass. Key modules had signatures and `NotImplementedError` placeholders.
- `data/sites.csv` is still a placeholder; `data/sites_smoke.csv` has canary sites.
- Qiyao's imported dataset contains about 90 `privacy_notice_data.xlsx` workbooks and 231 screenshots. It is useful background/reference but not the core plan unless reintroduced.

## Research Frame

- Core RQs remain the Feb. 15 proposal's two questions:
  1. Develop a computational audit/scoring system for layered consent interfaces and unbiased choice.
  2. Automatically capture and version privacy interfaces over time.
- AI is a method layer, not a new RQ.
- SOC 2 is relevant only as downstream market/GRC context. The project is not a SOC 2 audit system.

## Implementation Target For This Pass

- Add a lightweight consent-table layer for weekly records.
- Make Layer 1 deterministic from `CaptureBundle.path_outcomes`.
- Add tier classification and basic report generation.
- Add deterministic longitudinal diff behavior for path, score, copy, layout, and DOM changes.
- Add Week 1 paper/sample planning artifacts.

## Current Implemented MVP

- The repo now has an executable partial audit path: capture bundle generation, deterministic Layer 1, deterministic Layer 2 subset, partial report generation, consent-table CSV export, and longitudinal diff primitives.
- `scripts/run_audit.py` and `scripts/run_weekly.py` intentionally continue with warning notes when Layer 3 or report storage are still unimplemented, so the paper-facing consent table can grow before the full stack is finished.
- Fresh verification on 2026-05-29 passes for pytest, Ruff, Mypy, compileall, and `git diff --check`.

## Remaining Research-Critical Gaps

- Inspect persisted report JSONL artifacts and decide whether local JSONL remains sufficient through Week 3 or should move to SQLite/Postgres before the deep sample.
- Improve visible consent-control recall on real CMPs without reintroducing footer/hidden-frame false positives.
- Replace deterministic Layer 3 heuristics with LLM/VLM extractors when API budget and validation harness are ready; keep the same schema and quote-validation gates.

## 2026-06-05 Advisor Guideline Alignment Audit

- Current direction is aligned with Dr. Singh's June 5 guidance: keep RQ1/RQ2,
  treat no-banner observations as contrast cases, prioritize about 20 deep
  sites after the 5-site Week 2 evidence gate, and keep the 80-ish list as a
  tracker/candidate pool rather than the immediate main sample.
- The latest authoritative dashboard state is `preflight=ready_for_capture`,
  `sanity=pending_capture`, and `cycle=dry_run`. Final Week 2 results should
  not be claimed until live `week2-cycle` and sanity confirmation run on or
  after 2026-06-06.
- Direction risk remains communicative rather than technical: do not overclaim
  pilot evidence, do not expand to the 80-ish list before the evidence gate is
  stable, and keep SOC 2/GRC as a short discussion implication only.

## 2026-06-06 Week 2 Live Evidence Gate

- The scheduled Week 2 cycle completed successfully for all five frozen targets:
  The Guardian, CNN, Booking.com, NerdWallet, and Coca-Cola. Capture attempts
  were 5/5, successes were 5/5, and failures were 0.
- The refreshed research package now contains 42 audit reports and 20
  longitudinal summaries. Week 2 sanity is `ready`: 5/5 consent rows,
  5/5 evidence-complete rows, 5/5 matching audit reports, and 5/5 weekly
  summaries for cohort `week2-2026-06-06`.
- Current RQ1 evidence-gate snapshot: latest target tiers are `High-Risk=5`.
  This reflects the observed first-layer pathway evidence: most targets did not
  expose complete Accept/Reject/Customize/Dismiss pathways, and Coca-Cola
  exposed Accept but not Reject/Customize/Dismiss in the first-layer observation.
- Current RQ2 evidence-gate snapshot: latest longitudinal severity is
  `C=3, D=2`. Highest-priority timeline candidates are Coca-Cola, The Guardian,
  and CNN.
- A UTC/local-date bug was fixed after capture. The live run occurred just after
  midnight Asia/Shanghai while UTC was still 2026-06-05, so the initial weekly
  summaries were labeled `2026-06-05`. The pipeline now passes the scheduled
  `week_of` into weekly summary generation, and the five affected Week 2 rows
  were corrected structurally to `2026-06-06`.
- The 5-site gate is evidence-ready but not the final SSRP dataset. The next
  research step is advisor/sample review: keep the 8 CMP confirmations pending,
  decide the no-banner contrast treatment, and expand carefully toward roughly
  20 deep sites.

## 2026-05-29 Smoke Probe Findings

- The smoke list now has 6 public canary sites: BBC, The Guardian, NY Times, Reuters, Reddit, and Wikipedia.
- Access probe artifact: `data/access_probe_smoke_2026-05-29.csv`.
- Weekly consent-table artifact: `data/consent_table_smoke_2026-05-29.csv`.
- Access probe summary after HTTP status fix: 6 total, 5 loaded with HTTP < 400, 1 banner selector hit, 1 blocked/error signal.
- Reuters returned HTTP 401 and is recorded as `http_401`; keep it as a useful access-feasibility canary or replace it if the Week 2 sample should avoid blocked pages.
- The Guardian was the only site with an access-probe banner selector hit. The weekly capture path also found candidate consent controls on BBC, but no site passed the Layer 1 reject+customize gate in this MVP run.
- These smoke rows are not final paper scores. They are first-pass evidence that capture/export/diff scaffolding works and that the next technical bottlenecks are better pathway targeting, Layer 3, and report storage.

## 2026-05-29 Pathway Targeting Update

- The first smoke run showed that broad page-level candidate extraction could misread ordinary controls as consent pathways.
- Capture now filters candidates by consent/cookie/privacy context and by initial viewport intersection, then scans all Playwright frames for iframe-based CMPs.
- After the update, the 6-site smoke consent table records no first-layer visible consent pathways in the current US/Shanghai run context. This is conservative: it avoids paper-damaging false positives, but recall still needs improvement on real CMPs.
- Local JSONL storage now persists full `AuditReport` objects at `data/reports/audit_reports.jsonl`; the latest smoke run wrote 6 reports.

## 2026-05-30 Layer 3 MVP Findings

- Layer 3 is no longer blocked on model calls. The current scorer is deterministic and intentionally conservative.
- Transparency output now covers all four ontology topics and all four framing mechanisms, with verbatim source quotes only when present in captured visible text.
- Missing disclosure topics are represented as `present=false`, `clarity_grade=F`, and `evidence_quote=None`; the scorer does not invent supporting evidence.
- Unbiased Choice remains analytically separate from Transparency. The MVP uses Layer 2 pathway effort asymmetry as a fallback signal until screenshot-grounded VLM features are added.
- Report markdown now exposes Layer 3 evidence in a paper/poster-friendly form instead of hiding it inside JSON: topic rows, quotes, framing mechanisms, and unbiased-choice rationale are rendered in the saved `AuditReport.report_markdown`.

## 2026-05-30 Weekly Pipeline Findings

- `scripts/run_weekly.py` now uses the same basic CSV hygiene as the access probe: blank rows and comment rows whose URL starts with `#` are skipped.
- A full mocked weekly audit now proves the happy path: Layer 1 gate passes, Layer 2 scores, Layer 3 grades are written to the consent table, and the persisted report contains evidence-card markdown.
- This makes `data/sites.csv` safer to keep as a human-editable research queue with placeholder comments during Week 1 sample selection.
- The longitudinal diff path no longer stops at `summarize_week()`. For the SSRP MVP, weekly summaries are deterministic and no-budget: they preserve detected events, summarize event types/descriptions, and flag pathway/score changes as high-attention items for manual evidence review.
- The deterministic weekly summary is a paper-saving fallback, not the final AI method. Later LLM summarization can replace only the prose layer while keeping event detection and severity mapping schema-validated.
- Weekly summaries now persist separately from audit reports at `data/reports/weekly_summaries.jsonl`. This keeps the RQ2 longitudinal layer queryable without re-parsing every report JSONL row.
- A mocked two-capture weekly run now proves the intended chain: prior `AuditReport` + new `AuditReport` -> deterministic `ChangeEvent`s -> saved `WeeklySummary`.
- Saved weekly summaries can now be exported as a flat CSV table with one row per site-week observation. The export includes event type flags, event count, max magnitude, severity, summary text, and user-facing implications, making the RQ2 output usable for SSRP paper tables and poster figures.
- Stored audit reports can now be exported as a flat RQ1 results table. The export includes path availability, Layer 2 effort, Layer 3 grades, overall tier, first screenshot/DOM refs, hashes, and API cost, so the cross-sectional scoring results can be inspected without opening JSONL.
- The project now has a one-command research package export that writes both paper-facing CSVs plus `research_manifest.json`. This reduces runbook friction before advisor check-ins and helps make the data package auditable.
- Core script entrypoints can now be run directly from the repo root without manually setting `PYTHONPATH=src`. This removes a likely Week 1/2 usability snag when running capture/export commands repeatedly.
- The installed package CLI now exposes the paper-facing exports too: `consent-audit export-audit-reports`, `consent-audit export-longitudinal-summary`, and `consent-audit export-research-package`. This gives the project a cleaner advisor/demo surface than remembering individual script paths.
- Live audit orchestration now lives in package code at `consent_audit.pipeline`, not only under `scripts/`. Both `consent-audit audit` and `consent-audit weekly` call that shared pipeline, while the legacy script files remain thin wrappers for direct execution.
- Site-list validation is now explicit. `validate-sites` reports active-site counts, category counts, mentor-inherited rows, duplicates, invalid URLs, and placeholder rows before browser capture is spent.
- Current `data/sites_smoke.csv` validates cleanly with 6 active sites. Current `data/sites.csv` intentionally fails validation because it still contains the `https://example.com` placeholder row; this is a useful guard until the real mentor-approved list is inserted.
- Sample readiness is now reviewable as a single CSV: `data/sample_readiness_smoke_2026-05-29.csv` merges `data/deep_sample_candidates.csv`, the smoke access probe, and the smoke consent table.
- Current readiness summary: Guardian is `pilot_ready`; BBC, NYT, and Reddit need CMP/manual review because no banner was observed in the conservative weekly capture; Wikipedia is a control candidate; Example Domain still needs access probe evidence if it remains in the candidate table.
- `data/deep_sample_candidates.csv` has been expanded to 15 non-placeholder pilot candidates across 7 categories: news, social, ecommerce, travel, entertainment, finance, and reference/control.
- Pilot access probe artifact: `data/access_probe_pilot_2026-05-30.csv`. Result summary: 15 total, 14 loaded, 5 banner selector hits, 2 blocked/error signals.
- Pilot readiness artifact: `data/sample_readiness_pilot_2026-05-30.csv`. Result summary: Guardian remains `pilot_ready`; 8 newly probed sites need weekly capture; BBC/NYT/Reddit still need CMP/manual review; Wikipedia is the control candidate; Reuters and Netflix are blocked/error review cases.
- Pilot weekly target artifact: `data/pilot_weekly_targets_2026-05-30.csv`, derived from the unblocked pilot candidates that needed weekly capture.
- Pilot consent table artifact: `data/consent_table_pilot_2026-05-30.csv`. The first pilot weekly run wrote 7 rows; Booking.com failed during dynamic navigation and remains uncaptured.
- Updated pilot readiness summary after weekly capture: `pilot_ready=3`, `needs_weekly_capture=1`, `needs_cmp_review=8`, `control_candidate=1`, `access_blocked=2`. CNN and NerdWallet moved to `pilot_ready` alongside Guardian because access probe found a banner and weekly capture evidence now exists.
- CMP/manual review queue artifact: `data/cmp_review_queue_pilot_2026-05-30.csv`. It contains the 8 `needs_cmp_review` sites and enriches each with access screenshot path, weekly capture screenshot/DOM refs, DOM/image hashes, review reason, and recommended action.
- Current CMP review queue category spread: news=2, ecommerce=2, social=1, travel=1, entertainment=1, finance=1. This is the immediate manual-review bottleneck before locking a ~20-site deep sample.
- CMP/manual review worksheet artifact: `data/cmp_review_worksheet_pilot_2026-05-30.csv`. It covers the same 8 sites and adds fillable fields for `manual_banner_observed`, `manual_cmp_vendor`, `sample_decision`, `reviewer`, `reviewed_at`, and `reviewer_notes`.
- Current worksheet status is intentionally unresolved: all 8 rows are `pending_manual_decision`. The allowed decision labels are `keep_consent_sample`, `keep_no_banner_case`, `rerun_fresh_context`, `replace_candidate`, and `exclude`.
- Sample-lock action plan artifact: `data/sample_lock_plan_pilot_2026-05-30.csv`. It covers all 15 readiness rows and turns the current evidence into action states.
- Current sample-lock status: `provisionally_selected=3` (The Guardian, CNN, NerdWallet), `pending_manual_review=8` (BBC, New York Times, Reddit, Amazon, Walmart, Airbnb, Spotify, Chase), `needs_capture_rerun=1` (Booking.com), `blocked_review_or_replace=2` (Reuters, Netflix), and `optional_control=1` (Wikipedia).
- Sample action queues artifact directory: `data/sample_action_queues_pilot_2026-05-30/`. It contains `weekly_capture_shortlist.csv` (3 rows), `manual_review_queue.csv` (8 rows), `rerun_capture_queue.csv` (1 row), `replacement_review_queue.csv` (2 rows), `optional_control_queue.csv` (1 row), and `queue_manifest.csv`.
- Current weekly shortlist is The Guardian, CNN, and NerdWallet. Current rerun queue is Booking.com. Current replacement review queue is Reuters and Netflix.
- Next weekly target artifact: `data/deep_sample_weekly_targets_pilot_2026-05-30.csv`. It merges the weekly shortlist with the rerun queue into a normal site-list CSV for `consent-audit weekly`.
- The next weekly target list validates cleanly with 4 active sites: The Guardian, CNN, NerdWallet, and Booking.com; categories are news=2, finance=1, travel=1.
- Four-site weekly rerun artifact updates: `data/consent_table_pilot_2026-05-30.csv` now has 10 data rows; `data/reports/audit_reports.jsonl` has 17 reports; `data/reports/weekly_summaries.jsonl` has 3 summaries.
- Booking.com failed a second time with the same dynamic navigation `Page.content` error and remains `needs_weekly_capture`.
- New longitudinal evidence: Guardian has a severity D summary with pathway, layout, copy, and DOM changes; CNN has severity C with layout/copy/DOM changes; NerdWallet has severity B with copy change only.
- Paper-facing exports were refreshed: `data/audit_report_summary.csv` has 17 reports, `data/longitudinal_summary.csv` has 3 weekly summaries, and `data/research_package/research_manifest.json` records 17 audit reports and 3 weekly summaries.
- Booking.com's repeated failure was localized to `page.content()` during dynamic navigation churn. The capture layer now falls back to `document.documentElement.outerHTML`, preserving a DOM snapshot while recording a capture warning.
- A Booking-only rerun wrote the missing evidence row: `data/consent_table_pilot_2026-05-30.csv` now has a Booking.com row with screenshot/DOM refs and a `page.content` fallback note; `data/reports/audit_reports.jsonl` now has 18 reports.
- Updated readiness status: `pilot_ready=4`, `needs_cmp_review=8`, `control_candidate=1`, `access_blocked=2`, and no remaining `needs_weekly_capture` rows.
- Updated sample-lock queues: `weekly_capture_shortlist=4`, `rerun_capture_queue=0`, `manual_review_queue=8`, `replacement_review_queue=2`, and `optional_control_queue=1`.
- Refreshed paper-facing exports now record 18 audit reports and 3 weekly summaries.
- CMP/manual review now has a visual packet artifact at `data/cmp_review_packet_pilot_2026-05-30/`. It contains `index.html` and `index.md` with 8 review cards for BBC, New York Times, Reddit, Amazon, Walmart, Airbnb, Spotify, and Chase.
- The packet links access-probe screenshots, weekly-capture screenshots, DOM snapshots, review reasons, recommended actions, and the fixed worksheet decision options. This makes the next sample-lock step less dependent on manually joining CSV columns.
- CMP/manual review now also has non-final decision suggestions at `data/cmp_review_suggestions_pilot_2026-05-30.csv`.
- Current suggestion summary: `rerun_fresh_context=7` for BBC, New York Times, Amazon, Walmart, Airbnb, Spotify, and Chase because saved DOM contains cookie/consent/CMP indicators while no banner was observed; `keep_no_banner_case=1` for Reddit because the captured DOM lacks configured CMP indicators. All 8 rows keep `requires_human_confirmation=true`.
- The executable rerun target artifact is now `data/cmp_review_rerun_targets_pilot_2026-05-30.csv`. It covers the 7 `rerun_fresh_context` suggestions, validates as a normal site list, and intentionally excludes Reddit's current `keep_no_banner_case` suggestion.
- The fresh-context CMP rerun wrote 7 new consent-table rows and 7 new weekly summaries for BBC, New York Times, Amazon, Walmart, Airbnb, Spotify, and Chase. Evidence still shows `banner_detected=false` for all 7 rerun rows, so the rerun reduced capture uncertainty but did not surface visible consent banners in the current environment.
- After regenerating downstream artifacts, the current readiness/sample-lock status is unchanged in the important places: `pilot_ready=4`, `needs_cmp_review=8`, `access_blocked=2`, `control_candidate=1`; sample-lock remains `provisionally_selected=4`, `pending_manual_review=8`, `blocked_review_or_replace=2`, and `optional_control=1`.
- Refreshed paper-facing exports now record 25 audit reports and 10 weekly summaries. The 7 new summaries come from CMP fresh-context reruns and should be treated as RQ2 evidence about environment-dependent/no-banner persistence, not as automatic sample-lock approvals.
- CMP manual review now has a synthesized brief at `docs/research/cmp_manual_review_brief_2026-05-30.md` and a visual contact sheet at `data/cmp_review_packet_pilot_2026-05-30/contact_sheet.png`. The brief recommends treating Reddit and Walmart as likely replacement/access-friction cases, while the other 6 pending rows require a methods decision about whether no-banner contrast cases belong in the deep sample.
- Replacement probe artifact: `data/replacement_candidates_2026-05-30.csv` plus `data/access_probe_replacements_2026-05-30.csv`. Summary: 12 candidates probed, 8 loaded, 1 banner hit, 6 block/error signals.
- Weather.com is the only promising banner-present replacement from the first replacement probe. Its access probe showed a Sourcepoint/privacy-manager panel with purpose-level Accept/Reject controls, but full weekly capture was not stable enough to lock it into the deep sample.
- Replacement probe blockers: Home Depot, Etsy, Tripadvisor, and Expedia produced hard block/error signals; Forbes and WebMD loaded with CAPTCHA/block text. AP News, USA Today, eBay, Best Buy, and Indeed loaded but did not show banner selector hits.
- Capture-agent improvement from Weather.com: nested iframe buttons now keep consent-bearing ancestor context, non-interactive aria containers no longer become fake Accept candidates, and duplicate text clicking now skips hidden matches before clicking visible controls.
- Refreshed paper-facing exports now record 28 audit reports and 10 weekly summaries after the replacement probe captures.

## 2026-05-30 Replacement Probe Batch 2 Findings

- Batch 2 added 16 replacement candidates across ecommerce, food, software, technology, finance, travel, sports, and media.
- Access probe summary: 16 total candidates, 7 loaded with HTTP status below 400, 4 banner selector hits, and 9 block/error signals.
- The access-probe banner hits were Coca-Cola (`#onetrust-consent-sdk`), IKEA (`#onetrust-banner-sdk`), IBM (`#truste-consent-track`), and Intuit (`#onetrust-banner-sdk`).
- Full weekly capture confirmed Coca-Cola as the strongest replacement so far: Accept, Reject, and Customize were all available, Layer 1 passed, Layer 2 was Easy, Transparency was B, Unbiased Choice was A, and the final tier was Compliant.
- IKEA, IBM, and Intuit remain unstable. They showed access-probe banners but did not reproduce visible actionable paths in the weekly pipeline; IBM also redirected to Japanese content, and Intuit produced an XML-like snapshot.
- Loaded no-banner or locale-shift cases from batch 2 were Pepsi, Nike redirecting to `nike.com.cn`, and National Geographic.
- Block/error batch 2 cases were McDonald's, Adobe, United, NBA, Salesforce, Delta, Marriott, Oracle, and Hyatt.
- The audit report JSONL file was valid under normal newline iteration but unsafe for `read_text().splitlines()` because Coca-Cola text contained literal U+2028 line separators. JSONL writes now use ASCII escaping, existing JSONL was normalized, and paper-facing exports now record 32 audit reports and 10 weekly summaries.

## 2026-05-30 Replacement Promotion Gate Findings

- Replacement candidates now have a machine-readable review layer at `data/replacement_review_batch2_2026-05-30.csv`.
- The review gate intentionally requires full weekly reproduction of the key Layer 1 paths before a replacement is promoted. This avoids treating access-probe-only banner hits as stable deep-sample rows.
- Batch 2 review status counts: `verified_replacement=1`, `promising_reprobe=3`, `no_banner_or_locale_shift=3`, and `blocked_or_error=9`.
- Coca-Cola is the only verified replacement because it reproduced Accept, Reject, and Customize in weekly capture and passed Layer 1.
- IKEA, IBM, and Intuit are kept as `promising_reprobe`; they are useful instability evidence but should not enter the next weekly shortlist as banner-present replacements.
- The expanded weekly target artifact is `data/deep_sample_weekly_targets_expanded_2026-05-30.csv`. It validates cleanly with 5 active sites: The Guardian, CNN, Booking.com, NerdWallet, and Coca-Cola.

## 2026-05-30 Expanded Weekly Capture Findings

- The expanded weekly target list completed for all 5 active sites and appended 5 consent-table rows to `data/consent_table_pilot_2026-05-30.csv`.
- The run saved 5 new `AuditReport` rows. Stored report count is now 37.
- The run produced change summaries for The Guardian, CNN, Booking.com, and NerdWallet. Coca-Cola had no detected change between its two captures, which exposed that stable repeated captures were not being exported as RQ2 observations.
- The weekly pipeline now saves a `WeeklySummary` whenever two reports exist for a URL, including the no-change case. Empty-event summaries are severity A with `event_count=0`.
- Coca-Cola now has both RQ1 evidence and RQ2 stability evidence: two `Compliant` audit reports and one longitudinal summary reading "No detected consent-interface changes for this observation window."
- Current paper-facing exports record 37 audit reports and 15 longitudinal summaries.

## 2026-05-30 Week 2 Sample Freeze Findings

- Week 2 default capture targets are frozen in `data/week2_deep_sample_targets_2026-06-06.csv`.
- The Week 2 target list has 5 active sites: The Guardian, CNN, Booking.com, NerdWallet, and Coca-Cola.
- Category counts for the Week 2 list are `finance=1`, `food=1`, `news=2`, and `travel=1`; `mentor_inherited=0`.
- The pending CMP/manual-review rows now have a human-confirmable decision draft at `data/cmp_review_decision_draft_pilot_2026-05-30.csv`.
- Draft CMP decisions are `keep_no_banner_case=6` for BBC, New York Times, Amazon, Airbnb, Spotify, and Chase, and `replace_candidate=2` for Reddit and Walmart.
- Every CMP decision-draft row keeps `requires_human_confirmation=true`; the draft is an advisor-review aid, not a final sample lock.
- `docs/research/week2_sample_plan_2026-05-30.md` is the compact advisor-facing note tying together the Week 2 capture list, CMP decision draft, and open sample-method questions.

## 2026-05-30 Week 2 Execution Runbook Findings

- `docs/research/week2_execution_runbook_2026-06-06.md` is now the operational entrypoint for the next capture cycle.
- The runbook uses `data/week2_deep_sample_targets_2026-06-06.csv` as the frozen input and keeps appending observations to `data/consent_table_pilot_2026-05-30.csv` until the advisor locks a final sample name.
- The runbook explicitly separates longitudinal capture from sample-lock review: the 5 frozen targets can keep collecting evidence while the 8 CMP decision-draft rows wait for human confirmation.
- README status now reflects the actual current state: Week 2 ready, 37 audit reports, 15 weekly summaries, and pending advisor review for CMP rows.

## 2026-05-30 CMP Confirmation Loop Findings

- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` now covers the same 8 pending CMP/manual-review rows as the decision draft.
- The confirmation sheet starts with `confirmation_status=pending` and blank `confirmed_decision` fields for all 8 rows; draft decisions are not applied automatically.
- `cmp-review-apply-confirmations` writes a worksheet copy and only applies rows explicitly marked `confirmation_status=confirmed` with a valid final decision.
- This creates the missing loop from advisor review back into `sample-lock-plan` without violating the project invariant that sample decisions need human confirmation.

## 2026-05-30 Advisor Update Brief Findings

- `docs/research/week2_advisor_update_2026-06-06.md` is now generated from current research tables rather than hand-written.
- The brief summarizes the frozen 5-site target list, current research-package counts, latest target outcomes, longitudinal severity/event counts, and CMP confirmation status.
- Current generated counts are 5 target sites, 37 audit reports, 15 longitudinal summaries, and 8 pending CMP confirmations.
- Coca-Cola appears in the advisor brief as the only current `Compliant` Week 2 target, with `Accept+Reject+Customize` paths and severity A / 0 longitudinal status.

## 2026-05-30 Week 2 Sanity Check Findings

- `docs/research/week2_sanity_check_2026-06-06.md` is now generated from the Week 2 target list, consent table, audit-report summary, and longitudinal summary.
- The sanity check validates four pieces of post-capture evidence per target: consent-table row for the expected cohort, complete screenshot/DOM/hash evidence, matching audit-report fingerprint evidence, and weekly summary presence.
- Current pre-run baseline for cohort `week2-2026-06-06` is `pending_capture`: 0 of 5 targets have Week 2 consent rows, evidence-complete rows, matching audit reports, or weekly summaries.
- After the Week 2 capture run, this check should be rerun before telling the advisor that the capture cycle is complete.

## 2026-05-30 Advisor Check-In Index Findings

- `docs/research/week2_checkin_index_2026-06-06.md` is now generated as the first file to open for advisor check-ins.
- The index links the Week 2 advisor update, sanity check, execution runbook, sample plan, research package, research manifest, RQ1/RQ2 CSVs, CMP confirmation sheet, and CMP evidence packet.
- It records the current Week 2 sanity status as `pending_capture`, along with the current research-package counts of 37 audit reports and 15 longitudinal summaries.
- The runbook now includes `checkin-index` in the post-capture export refresh sequence so the handoff page stays current after each weekly run.

## 2026-05-30 Week 2 Preflight Gate Findings

- `docs/research/week2_preflight_check_2026-06-06.md` is now generated as the pre-capture readiness gate for the 2026-06-06 observation cycle.
- Current status is `ready_for_capture`: the Week 2 target list has 5 active sites, no validation issues, category counts `finance=1`, `food=1`, `news=2`, and `travel=1`, and no mentor-inherited rows.
- The preflight check also confirms the advisor update, sanity check, check-in index, runbook, research manifest, CMP confirmation sheet, and CMP evidence packet are present.
- It keeps `pending_capture` as an acceptable pre-capture sanity status while still surfacing the research-package counts of 37 audit reports and 15 longitudinal summaries and the CMP confirmation count of `pending=8`.

## 2026-05-30 Week 2 Refresh Orchestrator Findings

- `week2-refresh-outputs` now refreshes the post-capture Week 2 artifact chain in one command: research package, advisor update, sanity check, check-in index, preflight check, and refresh report.
- The orchestrator intentionally feeds the freshly generated `data/research_package/audit_report_summary.csv` and `data/research_package/longitudinal_summary.csv` into the advisor brief and sanity check. This avoids stale root-level summary CSVs after a capture run.
- Current refresh report: `docs/research/week2_refresh_report_2026-06-06.md`.
- Current refresh status remains pre-capture: 37 audit reports, 15 longitudinal summaries, sanity status `pending_capture`, and preflight status `ready_for_capture`.

## 2026-05-30 Week 2 Full-Cycle Command Findings

- `week2-cycle` is now the preferred one-command path for the scheduled Week 2 capture day.
- The command reruns the preflight gate before browser capture and blocks the weekly browser pipeline unless the preflight status is `ready_for_capture` or `--force` is explicitly used.
- After capture, it calls `week2-refresh-outputs`, so the research package, advisor brief, sanity check, check-in index, preflight check, and refresh report are regenerated from fresh evidence.
- `docs/research/week2_cycle_report_2026-06-06.md` is reserved for the actual cycle run report. It is intentionally not generated in this pre-capture implementation pass because that would require running the live 5-site browser capture.

## 2026-05-30 Weekly Capture Summary Findings

- `run_weekly_audit()` now returns a structured run summary instead of only logging site-level failures.
- The summary records target count, attempted count, succeeded count, failed count, failed URL/error pairs, and whether the budget cap stopped the run.
- `week2-cycle` writes those counts into the cycle report and marks capture status as `needs_attention` when 2 or more Week 2 targets fail, matching the runbook stop condition.
- Single-site failures still do not abort the weekly pipeline; the run continues and records the failure for post-run review.

## 2026-05-30 Week 2 Cycle Dry-Run Findings

- `week2-cycle --dry-run` is now the safe pre-capture rehearsal command for the scheduled Week 2 run.
- The dry run reruns `week2-preflight-check` and writes `docs/research/week2_cycle_report_2026-06-06.md`, but it does not call the browser capture pipeline or `week2-refresh-outputs`.
- A ready preflight produces capture status `dry_run`; a non-ready preflight produces `dry_run_needs_attention` unless `--force` is explicitly included.
- The dry-run report records zero capture attempts/successes/failures and notes that browser capture and refresh were skipped, so it can be used without changing research counts.
- Dry-run reports now keep the expected 5-site denominator visible: the generated report shows `Cycle mode: dry_run`, `Capture attempts: 0/5`, and `Capture successes: 0/5`. This distinguishes a rehearsal from an empty target-list configuration.
- Week 2 cycle reports now include an `Inputs` section: target list, consent table, cohort, expected target count, force flag, and dry-run flag. This makes each weekly observation reconstructable from the report itself rather than relying on shell history.
- Week 2 cycle reports now include a status-specific `Next Action` section. A ready dry run tells the runner to start live capture; a dry run with preflight warnings tells the runner not to start live capture until the preflight is ready or a force rationale is recorded.
- The advisor check-in index now links the Week 2 cycle report directly in the Read First section. `week2-refresh-outputs` and `checkin-index` both preserve this link, so dry-run/live run evidence is reachable from the advisor meeting entrypoint.
- The advisor check-in index Run Controls section now lists the capture-day sequence directly: preflight, `week2-cycle --dry-run`, live `week2-cycle` with `AGENT_SITE_TIMEOUT=40`, `week2-refresh-outputs`, and the advisor-facing export commands.
- `docs/research/week2_capture_day_checklist_2026-06-06.md` is now the operator-facing capture-day checklist. It records current preflight/sanity/cycle status, links the target list and consent table, and requires screenshot, DOM, hash, and report evidence before the run is treated as complete.
- `week2-refresh-outputs` now regenerates the capture-day checklist before regenerating the check-in index, and the refresh report links the checklist as a refreshed output.
- `week2-cycle` now regenerates the capture-day checklist after writing its final cycle report. This prevents the checklist's last-cycle fields from reflecting the older report that existed before the cycle started.
- Aborted Week 2 cycles now keep the expected target denominator visible in the cycle report and checklist: if preflight blocks a 5-site run, the report records `Capture attempts: 0/5` and `Capture successes: 0/5` instead of looking like an empty target-list run.
- Aborted Week 2 cycles now use cycle mode `preflight_blocked` rather than `live_capture`, and the report next action tells the runner to resolve preflight warnings before rerunning capture.
- Week 2 cycle `limit` now controls the live browser capture as well as the post-capture export refresh. This makes limited rehearsal captures behave predictably instead of only limiting the exported summary counts.
- Week 2 cycle reports now record `Capture limit` in the `Inputs` section, so a report with fewer capture attempts can be distinguished from an incomplete full run during later advisor or paper-method review.
- Generic weekly capture entrypoints now expose the same limit control: `consent-audit weekly --limit N` and `scripts/run_weekly._run(..., limit=N)` both pass the cap into `run_weekly_audit()`.
- Generic weekly capture entrypoints now surface immediate run outcomes. `consent-audit weekly` and `scripts/run_weekly.py` print a concise summary with attempted/target, succeeded, failed, and budget-exceeded counts; the script `_run()` also returns the structured `WeeklyRunSummary` for automation.
- The weekly run summary now includes failed URL/error lines when any target fails. This keeps capture-day triage visible in terminal output without forcing the operator to immediately inspect structured logs.
- The object-store adapter is no longer a hard stub. In the local research environment it writes to `data/object_store`, sanitizes screenshots before copying them, copies DOM snapshots as evidence artifacts, and rejects unsafe `../` style keys. This keeps Week 1/2 evidence persistence executable without requiring S3 credentials.
- The LLM/VLM wrapper modules are no longer hard stubs. Text wrappers now log budget entries and return deterministic topic/framing schema objects with verbatim source quotes; vision wrappers log budget entries, return empty pathway candidates rather than hallucinating from screenshots, and compute visual feature fallbacks only for supplied bbox-backed candidates.
- Weekly browser capture now has an internal site-list validation gate. `run_weekly_audit()` checks for placeholders, duplicate URLs, malformed URLs, and missing URL columns before any browser capture is attempted, so the default placeholder `data/sites.csv` cannot accidentally spend capture time.
- Weekly entrypoints should keep that gate understandable for a tired operator. `consent-audit weekly` and `scripts/run_weekly.py` now catch site-list `ValueError`s, print the validation message, and exit with status 1 instead of surfacing an empty Typer result/traceback path.
- README quick-start commands now point validation and generic weekly capture at the frozen Week 2 target list, and explicitly labels `data/sites.csv` as a scaffold placeholder until the broader mentor list is approved.
- The access probe now uses the same site-list validation discipline before browser launch. Invalid placeholders such as `https://example.com` are rejected with `site list validation failed before access probe: ...`, preventing the Week 0 feasibility command from spending browser time on scaffold rows.
- Access probe is now a first-class package command. The browser probing implementation lives in `consent_audit.access_probe`, `consent-audit access-probe` exposes it through Typer, and `scripts/access_probe.py` remains as a direct-execution compatibility wrapper over the same CSV runner.
- Access-probe summarization is now package-level too. `consent-audit access-probe-summary` renders the mentor/advisor triage summary from a probe CSV, and `scripts/access_probe_summarize.py` remains a compatibility wrapper over the shared renderer.
- `consent-audit research-status` now provides the single-screen orientation command that was missing from the workflow. It reads existing Week 2 artifacts, reports target/category counts, preflight/sanity/cycle status, research-package counts, CMP confirmation counts, and the next action from the cycle report without opening browser capture or mutating data.
- `SCHEMA.md` no longer describes the project as early scaffolding with unimplemented module stubs. Its status section now names the current executable Week 2 workflow, the 37-report / 15-summary research package, the `research-status` orientation command, and the remaining research gates: live Week 2 capture, sanity confirmation, CMP/manual-review confirmation, careful sample expansion, and paper/poster/demo writing.
- `consent-audit ssrp-paper-skeleton` now turns the current research package into a paper-writing entrypoint at `docs/research/ssrp_paper_skeleton_2026-06-06.md`. The skeleton carries the two approved RQs, target/category counts, current RQ1/RQ2 package counts, latest target tier/severity counts, a deep-sample evidence table, results-table plan, figure queue, and explicit gaps before draft freeze.
- The paper skeleton intentionally treats current rows as evidence-in-progress: it says to run live Week 2 capture, rerun sanity checks, resolve CMP/manual-review rows, and decide no-banner contrast handling before claiming final results.

## 2026-05-30 Week 2 Schedule Guard Findings

## 2026-05-30 SSRP Poster Plan Findings

- Paper-side generated artifacts now cover tables, skeleton, figure queue, writing notes, and claim status. The remaining SSRP deliverable gap is a poster-specific storyboard that turns those artifacts into panels, figure assets, copy blocks, and final-gate checks.
- The poster plan should remain evidence-conservative: current RQ1/RQ2 counts can be shown as provisional, but final poster claims must wait for scheduled Week 2 capture, sanity confirmation, and CMP/manual-review confirmation.
- The clean integration point is the same paper-artifact chain used by the claim register: a package exporter, `ssrp-poster-plan` CLI command, `week2-refresh-outputs` regeneration, `research-status` presence link, and a current artifact under `docs/research/`.
- `docs/research/ssrp_poster_plan_2026-06-06.md` now exists. It reports 5 Week 2 target sites, RQ1/RQ2 poster data availability of 5/5, latest target tiers `Compliant=1, High-Risk=4`, latest longitudinal severity `A=1, B=1, C=2, D=1`, pending CMP confirmations, and a `scheduled_date_not_reached` claim gate.
- The generated poster storyboard uses eight panels: title/thesis, research questions, pipeline, three-layer scoring, RQ1 evidence, RQ2 timeline, limitations, and takeaway. Its figure assets mark the longitudinal timeline as blocked for final poster use until the scheduled capture is complete.

## 2026-05-30 SSRP Remaining Work Audit Findings

- `docs/research/ssrp_remaining_work_audit_2026-05-30.md` now records the plan requirements against current evidence rather than relying on memory or optimism.
- The audit confirms the core pipeline, paper scaffold, poster storyboard, claim register, and deterministic scoring path are in place, but it also names the hard blockers for full goal completion: scheduled Week 2 live capture has not happened, sanity remains `pending_capture`, 8 CMP confirmations remain pending, the deep sample has only 5 frozen Week 2 targets, final paper/poster deliverables are still provisional, and the supporting demo/evidence browser is not implemented.
- The next viable sequence is explicit: run scheduled `week2-cycle` on 2026-06-06, refresh outputs, require sanity `ready`, resolve CMP confirmations, expand toward roughly 20 sites, and then design/implement the small evidence browser after design approval.

## 2026-05-30 CMP Confirmation Request Findings

- `docs/research/cmp_confirmation_request_2026-05-30.md` now turns the 8 pending CMP/manual-review rows into an advisor-facing confirmation request.
- The request points the reviewer to the visual packet, contact sheet, confirmation sheet, and manual review brief, then lists allowed final decisions for `confirmed_decision`.
- The row-by-row request keeps the current conservative interpretation: Reddit and Walmart are likely replacement/access-friction cases, while BBC, New York Times, Amazon, Airbnb, Spotify, and Chase should become no-banner contrast rows only if the methods section explicitly allows that category.
- This does not resolve the pending CMP blocker by itself. It makes the human review step concrete enough that the confirmation sheet can be edited and then applied with the existing `cmp-review-apply-confirmations` flow.

## 2026-05-30 Project Clarity Handoff Findings

- User clarified that the immediate goal is not more implementation; the useful deliverable is a clear explanation of what the project is and what to do next.
- Added `docs/research/ssrp_project_clarity_plan_2026-05-30.md` as a Chinese handoff document.
- The document reframes the project around two RQs, explains what is already built, names the current blockers, lists what not to do, and gives a week-by-week route through the 10-week SSRP cycle.
- This handoff treats the paper as the priority, the poster as the paper's visual translation, and demo/evidence browser work as optional supporting evidence.

## 2026-05-30 Advisor Meeting PM Brief Findings

- User needs a PM-style structure for the 2026-05-31 advisor meeting, not more implementation.
- Added `docs/research/advisor_meeting_pm_brief_2026-05-31.md`.
- The brief gives a meeting objective, 30-second project overview, current status, timed meeting flow, task breakdown, source documents for each task, mentor questions, pitfalls to avoid, and post-meeting actions.
- The main meeting decisions are Week 2 target approval, no-banner/CMP handling, deep-sample size, paper contribution framing, and the next advisor deliverable.

## 2026-05-31 Folder Structure Guide Findings

- User is unfamiliar with the folder contents and needs a map of what each folder/file does, why it exists, what is complete, what is incomplete, and where overall progress stands.
- Added `docs/research/folder_structure_guide_2026-05-31.md`.
- The guide groups the repo into research docs, data/evidence artifacts, Python pipeline source, compatibility scripts, tests, planning logs, and Qiyao's old reference dataset.
- Current overall status is clarified as: engineering scaffolding and research artifact generation are mostly built; research execution is at the start of scheduled Week 2 evidence collection; CMP decisions, sample expansion, live sanity, and final paper/poster remain open.

- Current local date is 2026-05-30, while the frozen Week 2 observation cohort is `week2-2026-06-06` / `week_of=2026-06-06`.
- `week2-cycle` now blocks live capture when the run date is earlier than the scheduled `week_of` date, unless the operator explicitly passes `--allow-early`. Dry runs remain allowed before the scheduled date.
- The default live command now writes `scheduled_date_not_reached` into `docs/research/week2_cycle_report_2026-06-06.md` and syncs the capture-day checklist before exiting, so the project state explains why no browser capture happened.
- `consent-audit research-status` now reports the guarded state as `Cycle capture status: scheduled_date_not_reached` and next action: wait until 2026-06-06 or rerun with `--allow-early` after recording the timing risk.

## 2026-05-30 SSRP Results Tables Findings

- `consent-audit ssrp-results-tables` now generates `docs/research/ssrp_results_tables_2026-06-06.md` from the current Week 2 targets plus `data/research_package/audit_report_summary.csv` and `data/research_package/longitudinal_summary.csv`.
- The generated artifact contains two paper-facing tables: RQ1 consent-interface scoring summary and RQ2 longitudinal change summary. It uses the latest row per canonical URL, so repeated same-site observations do not require manual CSV sorting before writing.
- Current generated table coverage is 5/5 target sites for RQ1 and 5/5 for RQ2, with latest target tiers `Compliant=1, High-Risk=4` and longitudinal severity `A=1, B=1, C=2, D=1`.
- `week2-refresh-outputs` now refreshes both `ssrp_results_tables_2026-06-06.md` and `ssrp_paper_skeleton_2026-06-06.md` after rebuilding the research package, so live Week 2 capture will update the paper-writing artifacts in the same command.

## 2026-05-30 Research Status Paper Artifact Findings

- `consent-audit research-status` now reports the generated paper artifacts alongside operational capture state.
- Current dashboard output shows `Paper artifacts: paper_skeleton=present, results_tables=present`.
- The dashboard's Key Artifacts section now links `docs/research/ssrp_results_tables_2026-06-06.md` and `docs/research/ssrp_paper_skeleton_2026-06-06.md`, so a single command orients both capture operations and paper-writing work.

## 2026-05-30 SSRP Figure Plan Findings

- `consent-audit ssrp-figure-plan` now generates `docs/research/ssrp_figure_plan_2026-06-06.md` from the current Week 2 targets, RQ1/RQ2 research-package CSVs, paper artifacts, and cycle report.
- The figure plan separates ready method figures from provisional evidence figures and final-paper figures blocked by the scheduled Week 2 live capture.
- Current figure data coverage is RQ1 `5/5` and RQ2 `5/5`, but the cycle capture status remains `scheduled_date_not_reached`, so the longitudinal timeline is explicitly blocked for final paper claims until 2026-06-06 live capture evidence exists.
- The generated plan names Coca-Cola as the current provisional evidence-card candidate and The Guardian, CNN, and Booking.com as current longitudinal timeline candidates.
- `week2-refresh-outputs` now regenerates the figure plan alongside the results tables and paper skeleton, and `research-status` reports all three paper artifacts as present.

## 2026-05-30 SSRP Writing Pack Findings

- `consent-audit ssrp-writing-pack` now generates `docs/research/ssrp_writing_pack_2026-06-06.md` from current Week 2 targets, RQ1/RQ2 research-package CSVs, CMP confirmations, paper artifacts, and the cycle report.
- The writing pack turns current evidence into draftable methods, preliminary results, limitations, and discussion notes without turning pre-capture evidence into final claims.
- Current generated writing notes show target coverage RQ1 `5/5`, RQ2 `5/5`, target tiers `Compliant=1, High-Risk=4`, longitudinal severity `A=1, B=1, C=2, D=1`, and CMP confirmations `pending=8`.
- Because the cycle capture status is still `scheduled_date_not_reached`, the writing pack marks claims as provisional until the scheduled Week 2 capture completes and the sanity check is refreshed.
- `week2-refresh-outputs` now regenerates the writing pack alongside the results tables, paper skeleton, and figure plan, and `research-status` reports all four paper artifacts as present.

## 2026-05-30 SSRP Claim Register Findings

- `consent-audit ssrp-claim-register` now generates `docs/research/ssrp_claim_register_2026-06-06.md` from current target coverage, RQ1/RQ2 summaries, CMP confirmation state, paper artifacts, and the Week 2 cycle report.
- The claim register labels each paper claim as `Supported`, `Provisional`, `Open limitation`, or `Blocked`, with a source artifact and next action.
- Current generated claim mode is `provisional` because the cycle capture status remains `scheduled_date_not_reached`.
- Current supported claims include the implemented three-layer audit workflow and the bounded GRC/SOC 2 implication note; current RQ1/RQ2 coverage and result-distribution claims remain provisional.
- Final Week 2 result claims are explicitly blocked until live capture and sanity confirmation, keeping the paper draft from overclaiming pre-capture evidence.
- `week2-refresh-outputs` now regenerates the claim register alongside the results tables, paper skeleton, figure plan, and writing pack, and `research-status` reports all five paper artifacts as present.

## 2026-06-06 Standalone Week 2 CLI Path Findings

- The refreshed Week 2 research package was valid, but running standalone `week2-sanity-check` after refresh rewrote `docs/research/week2_sanity_check_2026-06-06.md` to `needs_attention`.
- The cause was stale CLI defaults: `week2-sanity-check` and `advisor-update-brief` still pointed at root CSV exports under `data/`, while the active Week 2 workflow uses `data/research_package/audit_report_summary.csv` and `data/research_package/longitudinal_summary.csv`.
- Updated both standalone command defaults and added CLI regressions so future standalone status/advisor runs read the same package as `week2-refresh-outputs`.
- Re-running standalone `week2-sanity-check` and `research-status` now preserves the completed gate: consent rows `5/5`, evidence-complete rows `5/5`, matching audit reports `5/5`, weekly summaries `5/5`, and sanity `ready`.

## 2026-06-08 No-Visible-Banner Coding Findings

- Manual screenshot review confirmed that CNN, Booking.com, and NerdWallet did not show a visible first-screen consent banner in the Week 2 capture. Treating those rows as ordinary banner-path failures would overclaim the evidence.
- The audit report export now carries `banner_detected`, allowing paper-facing artifacts to separate `banner_present=2` from `no_visible_banner=3`.
- `docs/research/ssrp_results_tables_2026-06-06.md`, the paper skeleton, writing pack, claim register, and poster plan now state banner-present automated tiers separately from raw automated target tiers.
- The current advisor-facing framing is: The Guardian and Coca-Cola are banner/control-evidence cases; CNN, Booking.com, and NerdWallet are no-visible-banner contrast candidates until Dr. Singh confirms the sample rule.

## 2026-06-15 Coca-Cola Smoke Capture Findings

- A controlled one-site Coca-Cola smoke run after the June 14 0/5 capture failure succeeded at the browser-capture level: `layer1.png` and `layer1.html` were created under `data/captures/sites/www_coca_cola_com_20260615_043524/`.
- The run used `--no-save`, so `research-status` still reports the valid Week 2 package counts: 42 audit reports and 20 longitudinal summaries.
- The smoke CSV row at `data/smoke_coca_cola_2026-06-15.csv` records `banner_detected=true` but automated Layer 1 path booleans as all false, producing a `High-Risk` smoke row.
- Manual screenshot/DOM review shows a visible OneTrust Privacy Preference Center with `Allow All`, `Reject All`, `Confirm My Choices`, and category toggles. This means the capture environment worked, but automated control extraction missed visible OneTrust preference-center controls.
- The raw DOM snapshot remains a local ignored capture artifact by repo policy; the synced evidence excerpt is `data/smoke_coca_cola_2026-06-15_dom_evidence.csv`.
- Do not treat this smoke row as a final Coca-Cola RQ1 score. It should become either an extraction-fix regression case or a manually validated evidence-card case before any full current-five continuity rerun.

## 2026-06-15 OneTrust Pathway Fix Findings

- The Coca-Cola smoke failure was not in `score_layer1()` itself. Layer 1 correctly reads `PathOutcome`; the problem was earlier in capture-agent pathway labeling and click replay.
- Root causes found:
  - `Confirm My Choices` and `Save my choices` were not recognized as customize-like controls.
  - `Close preference center` was being pulled toward customize because of the word "preference" instead of being treated as dismiss.
  - Non-action dialog text such as `Privacy Preference Center` could be treated as a pathway-like candidate.
  - Coca-Cola's OneTrust preference center may appear after about 3 seconds, while click replay only waited 1 second.
  - The close button is aria-labeled; the click helper only used exact visible text, so it could not click accessible-name-only buttons.
- Regression tests now cover OneTrust label classification, OneTrust footer-control filtering, aria-label button clicking, and delayed CMP replay.
- Post-fix live smoke at `data/smoke_coca_cola_postfix_2026-06-15.csv` passed all Layer 1 paths for Coca-Cola: accept, reject, customize, dismiss, and gate are all `true`; tier is `Exemplary`.

## 2026-06-16 Fact-Consistency Review Findings

- The real project directory remains `/Users/alfred/Desktop/data-consent-audit-system`; `/Users/alfred/Documents/data consent audit system` was an empty Git repository before a writable local clone was created for this review.
- `git status --short --branch` in the real project reports `main...origin/main`, and `git log` shows `38da2ac Fix OneTrust pathway recognition` at `HEAD`.
- `research-status` still reports the current valid Week 2 package: 42 audit reports, 20 longitudinal summaries, sanity `ready`, cycle `completed`, and 8 pending CMP confirmations.
- The postfix smoke CSV confirms the OneTrust blocker was fixed for the Coca-Cola smoke case: accept/reject/customize/dismiss and the Layer 1 gate are all `true`, with tier `Exemplary`.
- Corrected two stale June 15 document passages so the initial OneTrust-fix recommendation is clearly superseded by the post-fix verification.

## 2026-06-18 Current Work Findings

- GitHub PR #4, `[codex] Clarify June 15 post-fix audit guidance`, is merged into `main` with merge commit `428394fa7e52d9f007737a123ace5ed6e1a7b13b`.
- The local research dashboard remains unchanged from the valid Week 2 evidence gate: sanity `ready`, cycle `completed`, 42 audit reports, 20 longitudinal summaries, and 8 pending CMP confirmations.
- No repository evidence shows a new advisor/sample decision after the June 15 email draft.
- Added a June 18 daily work note to keep the next action evidence-based: do not rerun blind capture; decide between a post-fix current-five rerun and manual evidence cards before expansion.

## 2026-06-19 Current-Five Evidence Packet Findings

- The current Week 2 five-site evidence set has complete screenshot/DOM/hash refs in `data/week2_manual_evidence_review_2026-06-10.csv`.
- Visual re-check of the five listed screenshots confirms the existing manual split: The Guardian and Coca-Cola have visible consent/control interfaces; CNN, Booking.com, and NerdWallet show no visible first-screen cookie/consent banner.
- The current no-visible-banner rows should remain contrast candidates unless the advisor confirms that they belong in the main RQ1 scoring table.
- Added `docs/research/current_five_evidence_packet_2026-06-19.md` so the next advisor/user discussion can use one five-site evidence packet rather than separate CSVs and screenshots.
- Added `data/current_five_decision_sheet_2026-06-19.csv` so advisor/user decisions can be recorded without editing the evidence packet itself.
