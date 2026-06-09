# Advisor Meeting PM Brief, 2026-05-31

用途：明天和导师更新项目进度时使用。  
角色定位：你不是去汇报“我已经把所有东西做完了”，而是去汇报“研究主线已经清楚，工具链和初步证据已经搭好，接下来需要导师帮我确认几个研究设计决定”。

## 0. Meeting 目标

这次 meeting 最重要的目标是拿到导师对下面几件事的确认：

1. 研究主线是否继续锁定为 RQ1 scoring + RQ2 longitudinal capture。
2. 当前 5 个 Week 2 target 是否可以作为下一次正式 capture 的起点。
3. 8 个 CMP/manual-review rows 应该怎么处理，尤其 no-banner cases 是否可以进 sample。
4. 后续 sample expansion 是先追求 20 个 deep sample，还是重新考虑更大的 80+ list。
5. SSRP paper/poster 的叙事是否应该以 evidence traceability 为核心。

你 meeting 后最理想的结果不是“导师把所有问题都解决”，而是拿到 3 个明确方向：

- Week 2 capture 怎么跑。
- sample 怎么扩。
- paper 怎么讲。

## 1. 30 秒项目概述

可以这样跟导师开场：

> My project is a traceable audit of cookie and consent interfaces. I am keeping the scope focused on two research questions: first, how to score consent interfaces based on path availability, path effort, transparency, and unbiased choice; second, how to capture these interfaces over time and document changes. I have the initial pipeline and paper-facing artifacts set up, but I need your guidance on sample decisions and how to handle no-banner or CMP-uncertain cases.

中文理解：

> 我现在不是在做一个商业 audit 平台，而是在做一个 SSRP research project：用可复查的证据链去评估 consent interface，并观察它们随时间变化。

## 2. 当前项目状态

你可以汇报：

- 核心 pipeline 已搭好：capture -> scoring -> report -> longitudinal diff -> research export。
- 当前 research package 里有 37 个 audit reports。
- 当前有 15 个 longitudinal summaries。
- Week 2 已冻结 5 个 capture targets：The Guardian、CNN、Booking.com、NerdWallet、Coca-Cola。
- 当前 paper artifacts 已生成：paper skeleton、results tables、figure plan、writing pack、claim register、poster plan。
- 这些结果目前都还是 provisional，因为 scheduled Week 2 live capture 还没跑。

当前状态命令：

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

目前关键状态：

- Preflight: `ready_for_capture`
- Sanity: `pending_capture`
- Cycle capture: `scheduled_date_not_reached`
- CMP confirmations: `pending=8`

依据文档：

- `docs/research/week2_advisor_update_2026-06-06.md`
- `docs/research/week2_checkin_index_2026-06-06.md`
- `docs/research/ssrp_project_clarity_plan_2026-05-30.md`
- `docs/research/ssrp_remaining_work_audit_2026-05-30.md`

## 3. 明天 meeting 建议流程

### 0-3 分钟：快速定位研究主线

你要说清楚：

- 我保留两个 RQ。
- AI 是 method，不是新的 research question。
- Paper 是主交付，poster/demo 是 supporting deliverables。

依据文档：

- `docs/research/ssrp_paper_skeleton_2026-06-06.md`
- `CONCEPTS.md`
- `docs/research/ssrp_project_clarity_plan_2026-05-30.md`

导师需要确认：

- 这两个 RQ 是否足够。
- 是否同意先不把 SOC 2 当核心研究框架。

### 3-8 分钟：汇报目前已经完成的东西

你要说：

- 我已经把证据链和研究输出结构搭起来了。
- 已经可以导出 RQ1/RQ2 tables。
- 已经可以生成 paper skeleton 和 poster plan。
- 当前不是 final evidence，而是 pilot / pre-Week-2 evidence。

依据文档：

- `data/research_package/research_manifest.json`
- `data/research_package/audit_report_summary.csv`
- `data/research_package/longitudinal_summary.csv`
- `docs/research/ssrp_results_tables_2026-06-06.md`
- `docs/research/ssrp_claim_register_2026-06-06.md`

导师需要听到的重点：

- 你没有过度 claim。
- 你知道哪些证据是 provisional。
- 你知道下一次正式 capture 是关键 gate。

### 8-15 分钟：讨论 Week 2 capture

你要说：

- Week 2 capture list 已冻结为 5 个站点。
- Preflight 已 ready。
- Live capture 计划在 2026-06-06 跑。
- 这次 capture 的目标是验证证据链，而不是立刻扩到很大 sample。

依据文档：

- `docs/research/week2_execution_runbook_2026-06-06.md`
- `docs/research/week2_capture_day_checklist_2026-06-06.md`
- `data/week2_deep_sample_targets_2026-06-06.csv`
- `docs/research/week2_preflight_check_2026-06-06.md`

导师需要确认：

- 5-site frozen list 是否可以作为正式 Week 2 start。
- 如果 1-2 个网站失败，是记录 limitation 继续，还是立刻替换。
- 是否接受先以 small deep sample 证明方法，再扩到大约 20 个。

### 15-25 分钟：重点讨论 CMP/manual-review

这是 meeting 最需要导师决策的部分。

你要说：

- 当前有 8 个 pending CMP/manual-review rows。
- 其中 6 个 draft 是 `keep_no_banner_case`：BBC、New York Times、Amazon、Airbnb、Spotify、Chase。
- 其中 2 个 draft 是 `replace_candidate`：Reddit、Walmart。
- 我不想自动把这些变成 final sample，需要导师确认。

依据文档：

- `docs/research/cmp_confirmation_request_2026-05-30.md`
- `docs/research/cmp_manual_review_brief_2026-05-30.md`
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
- `data/cmp_review_packet_pilot_2026-05-30/index.html`

导师需要回答：

1. no-banner contrast cases 能不能进 deep sample？
2. 如果可以，要不要限制在 2-3 个？
3. Reddit 和 Walmart 是否直接 replace？
4. 这些 CMP uncertain rows 需不需要再跑一次 fresh region/browser context？

### 25-35 分钟：讨论接下来 2 周计划

你要说：

- 下一个阶段不是大改系统，而是稳定执行研究流程。
- 先跑 Week 2 capture。
- capture 后 refresh outputs 和 sanity check。
- 再根据导师确认处理 CMP rows。
- 然后扩到约 20 个 deep sample。

依据文档：

- `docs/research/ssrp_project_clarity_plan_2026-05-30.md`
- `docs/research/ssrp_remaining_work_audit_2026-05-30.md`
- `docs/research/week2_sample_plan_2026-05-30.md`

导师需要确认：

- 是否同意 deep quality > broad shallow coverage。
- 是否同意 20 个左右 deep sample 是默认目标。
- 是否要保留一个 broader 80+ candidate tracker 作为 stretch，而不是主线。

### 35-45 分钟：paper/poster 叙事

你要说：

- Paper 的核心贡献不是“发现某个网站不好”，而是一个 traceable audit protocol。
- RQ1 是 scoring。
- RQ2 是 longitudinal versioning。
- Poster 可以展示 pipeline、three-layer rubric、sample evidence card、timeline。

依据文档：

- `docs/research/ssrp_paper_skeleton_2026-06-06.md`
- `docs/research/ssrp_writing_pack_2026-06-06.md`
- `docs/research/ssrp_figure_plan_2026-06-06.md`
- `docs/research/ssrp_poster_plan_2026-06-06.md`

导师需要确认：

- 这条 paper story 是否清楚。
- 是否需要把某个 concept 加强，比如 Notice-and-Choice、dark patterns、privacy communication。
- SOC 2/GRC 是否只放在 discussion 的一小段。

## 4. 后续任务拆解

### Task A：重新确认 research scope

目标：

- 把项目锁定在 RQ1 + RQ2，不再发散。

怎么做：

1. 读 `docs/research/ssrp_paper_skeleton_2026-06-06.md` 的 Research Questions。
2. 读 `CONCEPTS.md` 里三层 audit ontology。
3. meeting 时问导师：这两个 RQ 是否足够支撑 SSRP paper。
4. 如果导师要求改 RQ，只改 paper framing，不要马上改代码。

产出：

- 一句最终版 project thesis。
- 一版确认后的 RQ wording。

不要做：

- 不要把 SOC 2 改成核心。
- 不要把长篇 privacy policy analysis 拉回主线。

### Task B：准备 Week 2 capture

目标：

- 让 2026-06-06 的 live capture 有清楚输入、输出和 stop condition。

怎么做：

1. 打开 `docs/research/week2_execution_runbook_2026-06-06.md`。
2. 确认 target list 是 `data/week2_deep_sample_targets_2026-06-06.csv`。
3. 运行 `research-status` 看 preflight 是否 ready。
4. 到 capture day 先跑 dry run，再跑 live cycle。
5. capture 后跑 refresh outputs。

依据文档：

- `docs/research/week2_execution_runbook_2026-06-06.md`
- `docs/research/week2_capture_day_checklist_2026-06-06.md`
- `docs/research/week2_preflight_check_2026-06-06.md`
- `docs/research/week2_sanity_check_2026-06-06.md`

成功标准：

- 每个 target 有成功或失败记录。
- 有 screenshot / DOM / hash / audit report。
- sanity check 能解释当前状态。

如果失败：

- 失败 1 个站：记录 limitation，继续。
- 失败 2 个及以上：停止扩样本，先和导师讨论是否替换。

### Task C：处理 8 个 CMP/manual-review rows

目标：

- 不让 pending CMP rows 污染 final sample。

怎么做：

1. 打开 `docs/research/cmp_confirmation_request_2026-05-30.md`。
2. 打开 visual packet：`data/cmp_review_packet_pilot_2026-05-30/index.html`。
3. 和导师一起决定每个 row 的 final decision。
4. 在 `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv` 里填 confirmed decision。
5. 只在确认后 apply confirmations。

依据文档：

- `docs/research/cmp_confirmation_request_2026-05-30.md`
- `docs/research/cmp_manual_review_brief_2026-05-30.md`
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
- `data/cmp_review_packet_pilot_2026-05-30/index.html`

导师需要明确：

- no-banner cases 是否在 scope 内。
- Reddit / Walmart 是否 replace。
- 是否需要 fresh context rerun。

成功标准：

- 8 个 pending rows 至少有明确处理原则。
- final paper 里不会把 pending rows 写成 confirmed evidence。

### Task D：扩展 deep sample

目标：

- 从 5 个 frozen targets 扩到大约 20 个 well-documented sites。

怎么做：

1. 先等 Week 2 capture 和 sanity check 结果。
2. 从 replacement candidates 和 pilot readiness 中挑稳定网站。
3. 优先选 banner-present、可重复 capture、证据完整的网站。
4. 保持 category diversity，但不要为了类别牺牲 evidence quality。

依据文档：

- `data/sample_lock_plan_pilot_2026-05-30.csv`
- `data/replacement_review_batch2_2026-05-30.csv`
- `data/sample_action_queues_pilot_2026-05-30/queue_manifest.csv`
- `docs/research/week2_sample_plan_2026-05-30.md`

选择标准：

- 网站能访问。
- capture 不经常 block。
- 有 consent-related evidence。
- 能生成 report 和 weekly summary。
- 类别覆盖合理。

导师需要确认：

- 默认目标是不是 20 个 deep sample。
- 是否保留 80+ broader tracker 作为 stretch。
- no-banner rows 最多占多少比例。

### Task E：把 evidence 写进 paper

目标：

- 不只是有数据，还要能变成 SSRP paper。

怎么做：

1. 打开 `docs/research/ssrp_paper_skeleton_2026-06-06.md`。
2. 用 `docs/research/ssrp_writing_pack_2026-06-06.md` 写 methods。
3. 用 `docs/research/ssrp_results_tables_2026-06-06.md` 写 preliminary results。
4. 用 `docs/research/ssrp_claim_register_2026-06-06.md` 检查哪些 claim 可以说，哪些必须标 provisional。
5. 每次 capture 后 refresh paper artifacts。

依据文档：

- `docs/research/ssrp_paper_skeleton_2026-06-06.md`
- `docs/research/ssrp_writing_pack_2026-06-06.md`
- `docs/research/ssrp_results_tables_2026-06-06.md`
- `docs/research/ssrp_claim_register_2026-06-06.md`

成功标准：

- Introduction 能解释为什么 consent interface 需要 longitudinal audit。
- Methods 能解释三层 scoring 和 evidence discipline。
- Results 只写 evidence 支持的结论。
- Limitations 诚实写 capture instability、location/session effect、manual review gates。

### Task F：准备 poster，不急着做 demo

目标：

- 让 poster 成为 paper 的视觉化版本，而不是另一个独立项目。

怎么做：

1. 打开 `docs/research/ssrp_poster_plan_2026-06-06.md`。
2. 先决定 poster 的 4 个核心图：pipeline、rubric、evidence card、timeline。
3. 等 Week 2 capture 后再替换 provisional figures。
4. demo/evidence browser 只作为 supporting artifact，不要抢 paper/poster 时间。

依据文档：

- `docs/research/ssrp_poster_plan_2026-06-06.md`
- `docs/research/ssrp_figure_plan_2026-06-06.md`

导师需要确认：

- poster 是否要偏 methods contribution，还是偏 empirical findings。
- 是否需要一个 small demo 作为展示材料。

## 5. 明天必须问导师的问题

按优先级排序：

1. 您是否同意我把项目锁定为两个 RQ：consent-interface scoring 和 longitudinal capture/versioning？
2. Week 2 的 5-site frozen target list 是否可以作为正式 capture 起点？
3. no-banner contrast cases 是否应该纳入 deep sample？
4. 如果纳入，是否限制在 2-3 个？
5. Reddit 和 Walmart 是否应该直接 replace？
6. 后续 sample expansion 是否以大约 20 个 deep sample 为目标，而不是现在追 80+？
7. SSRP paper 的核心贡献是否应该写成 traceable audit protocol，而不是 commercial audit system？
8. SOC 2/GRC 是否只作为 discussion implication？
9. 您希望我下一次 meeting 带来什么：更多 capture evidence、sample decision table，还是 paper methods draft？

## 6. Meeting 时不要陷入的坑

不要说：

- “我已经完成了整个系统。”
- “这些结果已经 final。”
- “这个项目主要是 SOC 2 audit。”
- “我要马上做 80 个网站。”
- “demo 是主交付。”

应该说：

- “The pipeline and evidence structure are ready for the next capture cycle.”
- “Current results are provisional until the scheduled Week 2 capture and sanity check.”
- “I need your guidance on sample rules, especially no-banner and CMP-uncertain cases.”
- “My priority is the SSRP paper, with poster/demo as supporting outputs.”

## 7. Meeting 后你立刻做什么

meeting 后 30 分钟内做这几件事：

1. 把导师的决定写进 notes。
2. 更新 CMP confirmation sheet，如果导师给了明确决定。
3. 如果导师改了 scope，更新 paper skeleton 的 wording。
4. 如果导师确认 Week 2 path，就按 runbook 等到 2026-06-06 capture。
5. 如果导师要求更多 sample，先列候选，不要当天就盲跑大量 capture。

## 8. 你可以直接带去 meeting 的一句总结

> I have moved from project setup into evidence collection. The core audit pipeline and paper-facing exports are in place, and the next research risk is not coding the whole system, but making defensible sample and evidence decisions. For tomorrow, I mainly need your guidance on the Week 2 capture list, the pending CMP/no-banner cases, and whether the paper should emphasize the traceable audit protocol as the main contribution.

