# Project Inventory and Poster Story, 2026-07-02

这份文件回答一个最基本的问题：现在项目里到底有什么，截图是不是真的，
poster 最后要讲什么，以及现在已经做出来了什么。

## Important Correction

The project is not "a screenshot project." Screenshots are evidence inputs.

The original proposal's spine is two research questions:

1. RQ1: develop a computational audit and scoring system for layered consent
   interfaces and unbiased choice across the full consent pathway.
2. RQ2: automatically capture and version firms' privacy interfaces so changes
   can be documented over time.

So the correct framing is:

- RQ1 asks whether the consent interface gives users fair, reachable, and
  understandable choices.
- RQ2 asks whether those interfaces can be captured, versioned, and compared
  across time.
- Screenshots, DOM refs, hashes, visible text, and event logs are the evidence
  used to answer those questions.

## 一句话版本

这个项目不是在做一个法律结论系统，也不是在证明某家公司违规。

它现在最稳的定位是：

> 一个计算化、可追踪的 consent-interface audit and versioning system：
> RQ1 评估 consent interface 是否支持 unbiased choice；RQ2 记录同一批
> privacy interfaces 随时间如何变化。截图只是证据之一，不是最终目标。

## 现在已经有的东西

| 类别 | 现在有的东西 | 证据位置 |
|---|---|---|
| 项目定义 | RQ1 审查 consent interface；RQ2 跟踪界面随时间变化 | `CONCEPTS.md`; `docs/research/current_scope_2026-07-01.md` |
| 代码 | capture agent、Layer 1/2/3、diff、report export、research-status CLI | `src/consent_audit` has 52 non-cache source files |
| 数据表 | target lists、consent tables、decision sheets、research package | `data/*.csv`; `data/research_package` |
| 当前研究包 | 42 audit reports and 20 longitudinal summaries | `data/research_package/audit_report_summary.csv`; `data/research_package/longitudinal_summary.csv` |
| 截图证据 | 326 tracked site `layer1.png` screenshots; 39 access-probe screenshots | `data/captures/sites`; `data/captures/access_probe` |
| 当前 5 个核心样本 | Guardian, CNN, Booking.com, NerdWallet, Coca-Cola | `data/week2_manual_evidence_review_2026-06-10.csv` |
| Poster/展示材料 | results tables、claim register、poster plan、work order | `docs/research/ssrp_results_tables_2026-06-06.md`; `docs/research/ssrp_claim_register_2026-06-06.md`; `docs/research/presentation_poster_work_order_2026-07-02.md` |
| 当前未解决问题 | 7 blank current-five decisions; 8 pending CMP/manual-review rows | `data/current_five_decision_sheet_2026-06-19.csv`; `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` |

## 原始计划到底想做什么？

| Proposal part | Real meaning | Current project mapping |
|---|---|---|
| RQ1 audit/scoring system | Build a way to score layered consent interfaces for unbiased choice across the full pathway. | Layer 1 Path Availability, Layer 2 Path Effort, Layer 3 Transparency & Unbiased Choice. |
| RQ2 capture/versioning system | Build a way to repeatedly capture the same privacy interfaces and document changes over time. | Weekly capture, multimodal fingerprints, diff events, longitudinal summaries. |
| AI methods | Help extract visual/text/path evidence more effectively. | Browser agent for traversal, VLM-style visual features, LLM-style text/framing summaries. |
| Poster/presentation | Explain the research framework and show pilot evidence. | Workflow figure, scoring rubric, evidence cards, RQ1/RQ2 tables, limitations. |

The key idea is not "we collected screenshots." The key idea is:

> consent interfaces are corporate communication objects, and we can audit them
> computationally by scoring their choice architecture and tracking how that
> architecture changes over time.

## 截图是真的吗？

结论：截图文件是真的存在、能打开、不是空路径，也不是坏 PNG。

我在 2026-07-02 做了三层核查：

1. 文件核查：
   - `data/captures/sites` has 326 `layer1.png` files.
   - All 326 are valid PNG files.
   - All 326 are 1440x900 screenshots.
   - File sizes range from 14,031 bytes to 738,434 bytes.
   - There are 0 synced `layer1.html` raw DOM files in this checkout.

2. 报告引用核查：
   - `data/research_package/audit_report_summary.csv` has 42 rows.
   - Those 42 rows reference 42 screenshot paths.
   - All 42 referenced screenshot paths exist locally.

3. Current-five 视觉抽查：
   - The Guardian screenshot exists and shows a visible Guardian choice screen
     with accept/reject/manage cookie choices.
   - Coca-Cola screenshot exists and shows a visible Privacy Preference Center
     with Allow All, Confirm My Choices, Reject All, and toggles.
   - CNN screenshot exists and shows the CNN homepage with no visible
     first-screen cookie banner.
   - Booking.com screenshot exists and shows the Booking.com homepage/search
     UI with no visible first-screen cookie banner.
   - NerdWallet screenshot exists and shows the NerdWallet homepage/product UI
     with no visible first-screen cookie banner.

What this proves:

- The local screenshot evidence exists.
- The key screenshot paths used by the reports exist.
- The five most important screenshots visually match the current manual
  evidence sheet.

What this does not prove:

- It does not prove the live websites still look the same today.
- It does not prove the missing local `layer1.html` raw DOM files are synced.
- It does not turn the no-visible-banner rows into banner-path failures.

## 现在能说的结果

Use this as the current poster-safe wording:

1. The project has a working pilot pipeline for both proposal RQs.
2. For RQ1, the pipeline can produce evidence-linked audit reports for consent
   interface path availability and preliminary scoring.
3. For RQ2, the pipeline can produce longitudinal summaries from repeated
   captures and multimodal fingerprints.
4. The Week 2 evidence gate covers 5 target sites.
5. The current evidence splits into:
   - 2 banner-present evidence-card candidates: The Guardian and Coca-Cola.
   - 3 no-visible-banner contrast candidates: CNN, Booking.com, NerdWallet.
6. The research package contains 42 audit reports and 20 longitudinal summaries.
7. The current longitudinal snapshot reports severity C=3 and D=2 for the five
   Week 2 targets.
8. The best current conclusion is about method and traceability, not about
   legal compliance.

Do not say:

- "All five sites failed consent compliance."
- "CNN/Booking/NerdWallet had broken cookie banners."
- "The 20-site final sample is locked."
- "The final dataset is complete."
- "Raw HTML snapshots are synced locally."
- "The formal paper is the required summer deliverable."

## Poster 最后应该讲什么

Poster 的主线可以是：

> Firms use privacy interfaces as communication tools. This project develops a
> computational audit framework to score whether layered consent interfaces
> support unbiased choice, and a longitudinal capture system to document how
> those interfaces change over time.

更像中文口语一点：

> 我做的不是单纯截图，而是一个“consent interface 评分 + 版本追踪”的研究框架。
> 第一部分评估网站有没有公平、清楚、可到达的选择；第二部分记录这些界面之后
> 有没有改、怎么改。截图、DOM、hash、event log 都是为了让每个评分和变化结论
> 能被复查。

## Poster 可以放的结论

当前最安全的结论是：

1. The proposal's two-part system is feasible at pilot scale: RQ1 scoring and
   RQ2 versioning can run on the same evidence pipeline.
2. Screenshot review matters: the automated table alone can overstate risk
   when no first-screen banner is visible.
3. The five-site pilot already shows two different evidence classes:
   banner-present cases and no-visible-banner contrast cases.
4. Longitudinal tracking is useful because consent-interface evidence can
   change across captures.
5. The next research decision is sample treatment: either keep the five-site
   pilot as a careful evidence demo or expand toward a deeper sample after
   advisor confirmation.

## 现在做出来的成品是什么？

已做出来：

- A runnable Python package/CLI for the audit workflow.
- A research-status dashboard.
- A Week 2 evidence package with 5 current target sites.
- 326 local site screenshots.
- 42 audit-report summary rows.
- 20 longitudinal-summary rows.
- Current-five manual evidence review.
- Poster/results/claim-register drafts.
- A direct advisor email and a presentation/poster work order.

还没做完：

- Final poster layout.
- Final presentation slides.
- Final decision on whether the current five are enough or whether to expand.
- Advisor/user decisions in the current-five decision sheet.
- The 8 CMP/manual-review confirmations.
- Locally synced raw HTML evidence.

## 下一步应该做什么

Do these in order:

1. Ask Dr. Singh to confirm current-five treatment and whether to expand.
2. Fill `data/current_five_decision_sheet_2026-06-19.csv`.
3. Build two evidence cards for poster: Guardian and Coca-Cola.
4. Build one contrast panel: CNN, Booking.com, NerdWallet.
5. Build one workflow figure: capture -> scoring layers -> report ->
   longitudinal summary.
6. Only run new capture after the sample decision is clear.

## If you have to explain the project in 30 seconds

I am building a computational audit system for website consent interfaces. The
first research question is how to score layered consent interfaces for unbiased
choice across the full pathway: Accept, Reject, Customize, and Dismiss. The
second research question is how to automatically capture and version these
interfaces over time. The pilot currently has 5 current sites, 326 local
screenshots, 42 audit reports, and 20 longitudinal summaries. The poster should
show the RQ1 scoring framework, the RQ2 versioning pipeline, and a small set of
evidence cards and limitations.
