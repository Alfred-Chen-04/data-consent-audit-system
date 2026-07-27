# July 3 Scope/Fact Review and Poster Plan, 2026-07-03

Purpose: answer the user's current question in a fact-grounded way: what this
project is, what has actually been done, whether the work still fits the
original scope, whether the final summer plan is realistic, and what the poster
can honestly say now.

This is a status and planning document. It adds no new browser capture and no
new consent-interface evidence.

## Current Project Spine

Use the July 2 canonical goal as the controlling explanation:

- RQ1 scoring: computationally score layered consent interfaces for unbiased
  choice across the full consent pathway.
- RQ2 versioning: automatically capture and version privacy/consent interfaces
  so interface changes can be documented over time.

Screenshots, DOM refs, visible text, hashes, event logs, report CSVs, and
longitudinal summaries are evidence inputs for RQ1/RQ2. They are not the final
research question by themselves.

## Fact Sources Checked Today

Current facts below come from these checks:

- `git status -sb`
- `git log -1 --oneline --decorate`
- GitHub connector read of PR #8
- `PYTHONPATH=src /Users/alfred/Desktop/data-consent-audit-system/.venv/bin/consent-audit research-status`
- structured reads of:
  - `data/current_five_decision_sheet_2026-06-19.csv`
  - `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
  - `data/research_package/audit_report_summary.csv`
  - `data/research_package/longitudinal_summary.csv`
- filesystem counts under `data/captures/sites`
- keyword review across README, SCHEMA, CONCEPTS, and 70 existing research
  Markdown docs before this file was added.

## Current Verified State

Calendar:

- July 3, 2026 is 35 of 70 days in the May 30-August 7 core research window.
- That is 50.0% of the core build/research window.
- There are 35 calendar days left before August 7, and 59 days before the
  August 31 polish deadline.

GitHub/project status:

- Local branch: `codex/project-status-plain-language`.
- Latest local/remote commit before today's edits: `42f8b76 Add canonical
  project goal alignment`.
- PR #8 is open, draft, mergeable, and targets `main`.

Research package:

- `research-status` reports Week 2 targets: 5.
- `research-status` reports preflight `ready_for_capture`, sanity `ready`, and
  cycle capture `completed`.
- The research package has 42 audit reports and 20 longitudinal summaries.
- The exported audit summary currently has banner_detected counts:
  true=9, false=33.

Evidence files:

- `data/captures/sites` contains 326 tracked site `layer1.png` screenshots.
- The same tree contains 0 synced `layer1.html` raw DOM files in this checkout.

Open human decisions:

- `data/current_five_decision_sheet_2026-06-19.csv` has 7 rows and 7 blank current-five decisions.
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` has 8 rows, all 8
  pending CMP/manual-review confirmations, and 8 blank confirmed decisions.

## Scope And Unsupported-Claim Review

Today I checked the current-facing materials for the main ways this project can
drift out of scope or overclaim.

Safe current framing:

- The project is still aligned with the original proposal spine: RQ1 scoring
  and RQ2 versioning.
- AI/browser automation are methods used to collect and interpret evidence.
- Evidence traceability is a design requirement, not the whole research goal.
- Current summer deliverables are presentation, large poster, and traceable
  evidence package.

Do not claim yet:

- The final dataset is complete.
- The 20-site sample is locked.
- The 80-ish broader tracker is operational as a finished sample.
- Raw `layer1.html` files are synced locally.
- CNN, Booking.com, or NerdWallet are confirmed banner-path failures.
- All current sites failed consent compliance.
- This is a legal compliance verdict or a SOC 2 audit system.
- A formal paper is required for the current summer scope unless Dr. Singh says
  so again.

Review result:

- The current entrypoints now mostly contain those guardrails explicitly:
  `current_project_goal_2026-07-02.md`,
  `project_inventory_and_poster_story_2026-07-02.md`, and
  `presentation_poster_work_order_2026-07-02.md`.
- Older historical documents still contain some paper-oriented or
  pre-correction wording. Treat those as historical notes unless a current
  entrypoint repeats them.
- The most important practical risk is not false evidence; it is accidentally
  presenting pilot/current evidence as final research results.

## Can The Final Summer Plan Be Completed?

Yes, if the final product is framed as:

- a presentation;
- a large poster;
- a small demo/evidence browser if time permits;
- a traceable pilot evidence package.

This is realistic because the method, pipeline, evidence cards, current tables,
and limitations already exist.

No, or at least not safely without more decisions, if the final product is
framed as:

- a finished 20-site longitudinal dataset;
- a conference-ready paper;
- a legal/compliance audit result;
- a claim that all current examples are final validated cases.

The project is at the calendar midpoint. The technical and documentation
scaffold is ahead of the poster, but the final empirical claim strength is still
limited by unresolved sample treatment and manual decisions.

## What To Do Next

Recommended next sequence:

1. Merge or review PR #8 so `main` contains the current plain-language project
   scope.
2. Use `docs/research/current_project_goal_2026-07-02.md` as the canonical
   explanation when talking to Dr. Singh or writing slides.
3. Fill or discuss `data/current_five_decision_sheet_2026-06-19.csv`.
4. Decide what to do with the 8 pending CMP/manual-review rows.
5. Build the presentation/poster around the current pilot/evidence story before
   running more blind capture.
6. If Dr. Singh wants stronger empirical results, expand toward more
   banner-present examples after the current-five rules are settled.
7. If expansion is not required, finish a careful pilot poster and label the
   unresolved pieces as limitations/future work.

## Poster Can Be Drafted Now

Poster can be drafted now as a pilot/evidence poster.

What can already be written strongly:

- Research question section: RQ1 scoring and RQ2 versioning.
- Background/problem section: consent interfaces as corporate communication and
  choice-architecture objects.
- Method section: capture bundle -> Layer 1/2/3 scoring -> AuditReport;
  repeated captures -> fingerprints/diffs -> longitudinal summaries.
- Evidence section: Guardian and Coca-Cola as current banner/control evidence
  cards; CNN, Booking.com, and NerdWallet as no-visible-banner contrast
  examples.
- Current evidence snapshot: 5 Week 2 targets, 42 audit reports and 20
  longitudinal summaries, 326 screenshot files, and the unresolved decision
  counts above.
- Limitations section: no final 20-site sample, no synced raw HTML files,
  pending no-visible-banner treatment, pending CMP/manual review, and no legal
  compliance verdict.

What should wait:

- Final numerical results across a 20-site deep sample.
- Final claims about which sites are risky or compliant.
- Any claim that the system is complete beyond pilot scale.
- A polished paper-style results/discussion section unless Dr. Singh asks for a
  formal paper again.

## How To Explain It In Presentation

Short version:

> I am building a computational audit and versioning framework for website
> consent interfaces. RQ1 asks how to score whether layered consent pathways
> support unbiased choice. RQ2 asks how to repeatedly capture and compare those
> interfaces over time. The current work demonstrates the pipeline at pilot
> scale with evidence-linked reports, screenshot/DOM references, and
> longitudinal summaries. The poster will show the method, current evidence
> cards, contrast cases, and the open decisions before scaling the sample.

Plain-language Chinese version:

> 我现在做的不是单纯截图，也不是法律判定。这个项目的主线是：第一，给网站的
> consent interface 做可复查的评分，看用户选择是否公平、清楚、可到达；第二，
> 把这些界面按时间捕捉和版本化，看它们之后有没有变化。现在已经有 pilot 级别
> 的 pipeline、截图证据、audit reports 和 longitudinal summaries；poster 可以先
> 写成方法和证据展示，但不能说最终 20-site 数据集已经完成。
