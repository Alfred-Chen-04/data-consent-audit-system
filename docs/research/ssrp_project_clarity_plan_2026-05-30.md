# SSRP 项目梳理与下一步计划

日期：2026-05-30

这份文档的目的不是继续加功能，而是把这个 10 周 research 项目捋清楚：你到底在研究什么、现在有什么、下周开始按什么顺序做。

## 1. 一句话版本

你的项目是：

> 做一个可复查的 consent interface audit：每周抓取一批网站的 cookie/consent 界面，记录它们有没有 Accept / Reject / Customize 等路径、这些路径是否难找、文案是否透明，然后把变化和证据整理成 SSRP paper/poster。

最重要的不是“做一个很酷的软件”。最重要的是：

- 每一个判断都有截图、DOM、文本或 hash 证据。
- 每一个分数都能解释。
- 最后能写成一篇 SSRP research 稿。

## 2. 研究问题

保留两个研究问题就够了。

**RQ1：Consent interface scoring**

网站的 consent interface 是否给用户提供公平、清楚、可到达的选择？

你要看的东西：

- 是否有 Accept
- 是否有 Reject
- 是否有 Customize
- Reject 是否比 Accept 更难找
- 文案是否透明
- 界面是否有诱导性 framing

**RQ2：Longitudinal capture/versioning**

这些 consent interfaces 随时间会不会变化？

你要看的东西：

- 一周后按钮有没有变
- 文案有没有变
- 路径有没有变难或变简单
- 同一个网站是否稳定
- 这些变化对用户选择有什么影响

## 3. 不要让项目发散

现在先不要把项目变成这些东西：

- 不要把它写成 SOC 2 audit system。SOC 2 只能放在 discussion 里当市场 relevance。
- 不要追求 80+ 网站的大规模覆盖。先把 20 个左右网站做深。
- 不要把 public demo 当主产品。demo 只是 supporting evidence。
- 不要现在重做完整前端、数据库或商业 SaaS。
- 不要把长篇 privacy policy analysis 变成主线。主线是 consent interface，不是隐私政策全文。

## 4. 现在仓库里已经有什么

当前状态可以这样理解：

- 核心 pipeline 已经有了：capture -> scoring -> report -> weekly diff -> research export。
- 现在研究包里有 42 个 audit reports。
- 现在有 20 个 longitudinal summaries。
- Week 2 冻结的 5 个 capture targets 已经完成 live capture。
- paper skeleton、results tables、figure plan、writing pack、claim register、poster plan 都已经生成了。
- 这些 paper/poster artifacts 现在是 Week 2 evidence-gate scaffold，不是最终 10 周结果。

当前主要卡点：

- Week 2 sanity check 已经是 `ready`。
- 5 个 Week 2 evidence bundles 需要人工确认/标注，入口是 `data/week2_manual_evidence_review_2026-06-10.csv`。
- 8 个 CMP/manual-review rows 还需要人类/advisor 确认。
- deep sample 目前只有 5 个 frozen targets，还没到大约 20 个。

所以现在不是“项目没有开始”，而是“研究框架和工具已经搭好，接下来要按周收证据、扩样本、写 paper”。

## 5. 你真正要交付什么

优先级从高到低：

1. SSRP research paper
2. SSRP poster
3. 小 demo / evidence browser

Paper 最重要。Poster 是 paper 的视觉版。Demo 只是证明你真的有证据链，不是主产品。

## 6. 你下周开始的顺序

下周不要同时做很多事。只做下面这条线。

### Step 1：先读 4 个文件，重新进入状态

先打开：

- `README.md`
- `CONCEPTS.md`
- `docs/research/week2_checkin_index_2026-06-06.md`
- `docs/research/ssrp_paper_skeleton_2026-06-06.md`

读的时候只问自己三个问题：

- 我的两个 RQ 是什么？
- 当前证据支持什么？
- 还有哪些 claim 不能说死？

### Step 2：确认 Week 2 capture 准备好了

运行或查看当前状态：

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

你要看到：

- preflight 是 `ready_for_capture`
- sanity 是 `ready`
- cycle 是 `completed`

如果状态不是这样，要先看 `docs/research/week2_cycle_report_2026-06-06.md`
和 `docs/research/week2_sanity_check_2026-06-06.md` 找原因。

### Step 3：人工 review 5 个 Week 2 evidence bundles

Week 2 live cycle 已经完成。现在不要盲目再跑 capture，先人工看 5 个
evidence bundles。

目标不是“所有网站都完美”。目标是确认：

- 哪些是真的 banner-present case。
- 哪些是 no-visible-banner contrast candidate。
- 哪些适合留在 deep sample。
- 哪些更适合作为 contrast 或 replacement。

### Step 4：capture 后立刻 refresh + sanity check

capture 后运行 refresh，然后看 sanity check。

你要确认：

- 5 个 target 是否都有新 cohort row
- screenshot/DOM/hash 是否齐
- report 是否能对上
- weekly summary 是否生成

如果 sanity 不是 ready，也没关系。把原因写进 limitations。

### Step 5：处理 8 个 CMP/manual-review rows

这 8 个不是你用代码自动决定的。它们需要人看一眼再确认。

你要做的是：

- 看 `docs/research/cmp_confirmation_request_2026-05-30.md`
- 决定哪些是 keep no-banner case
- 决定哪些是 replace candidate
- 不要把 pending row 当 final evidence 写进 paper

### Step 6：再考虑扩到大约 20 个 deep sample

只有当 Week 2 的 5 个目标跑通并且 sanity 可解释之后，再扩样本。

扩样本标准：

- 能访问
- 有证据
- 不太容易被 block
- 类别有代表性
- 能重复 capture

## 7. 10 周路线图

### Week 1：把研究问题和证据结构固定

你要完成：

- 明确 RQ1/RQ2。
- 读懂 current artifacts。
- 确认 Week 2 target list。
- 准备 advisor 问题。

不要做：

- 不要重构系统。
- 不要追求 80+ 网站。
- 不要做商业化 demo。

### Week 2：跑第一次正式 weekly capture

你要完成：

- 跑 Week 2 capture。
- refresh research package。
- 检查 sanity。
- 记录失败原因。

产出：

- 新 consent table rows
- 新 audit reports
- 新 longitudinal summaries
- 更新后的 paper skeleton/results tables

### Week 3：人工读证据，修正方法说明

你要完成：

- 看 5 个 target 的 evidence。
- 确认哪些 score 有说服力。
- 把不稳定或失败的地方写成 limitations。
- 处理 CMP/manual-review rows。

### Week 4：扩样本

你要完成：

- 从 replacement candidates 里挑更稳定的网站。
- 目标是逐步接近 20 个 deep sample。
- 不追求数量，先保证每个网站有证据链。

### Week 5：整理 Layer 3 和文案/framing

你要完成：

- 总结透明度和诱导性文案模式。
- 把 quote evidence 放进 methods/results。
- 明确 deterministic scoring 和 model extraction 的边界。

### Week 6：生成第一版 paper results

你要完成：

- RQ1 table
- RQ2 table
- 初版 figures
- 初版 methods prose

### Week 7：第二/第三次 weekly observation

你要完成：

- 看哪些网站变了。
- 总结 change patterns。
- 找 2-3 个最能讲清楚的 case study。

### Week 8：跑完整 deep sample

你要完成：

- 尽量完成 20 个左右网站。
- 把不能用的网站剔除或标成 limitations。
- 开始写 results/discussion。

### Week 9：写 paper

你要完成：

- results
- limitations
- discussion
- 小段 GRC/SOC 2 implication

SOC 2 只写成一句小 implications，不要让它抢主线。

### Week 10：冻结 SSRP paper draft

你要完成：

- freeze dataset
- freeze tables/figures
- 完成 paper skeleton -> paper draft
- poster 用同一套 evidence 改写

## 8. 每周固定节奏

每周只按这个节奏走：

1. 周初：确认 target list 和本周目标。
2. capture day：跑 capture。
3. capture 后：refresh outputs。
4. 当天：看 sanity check。
5. 周末：把结果写进 paper notes。

不要每天改方向。这个项目最怕的不是做得慢，而是不断换主线。

## 9. 如果自动化不稳定怎么办

自动化不稳定不等于研究失败。

如果 capture 自动化不够稳，就切到 semi-automated protocol：

- 保留 screenshot
- 保留 DOM/text hash
- 保留 consent table row
- 人工记录路径是否存在
- 人工写 validation notes

Paper 仍然可以成立，因为研究重点是 traceable consent-interface evidence，不是炫耀全自动。

## 10. 你现在最该记住的三句话

1. 这个研究不是要做完一个商业系统，而是要写出一篇证据链清楚的 SSRP paper。
2. 深度比广度重要；20 个好网站胜过 80 个浅表网站。
3. 每个分数都必须能回到截图、DOM、文本或 hash 证据。

## 11. 下次打开项目时先做什么

打开项目后先运行：

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

然后看：

- `docs/research/week2_checkin_index_2026-06-06.md`
- `docs/research/ssrp_paper_skeleton_2026-06-06.md`
- `docs/research/ssrp_remaining_work_audit_2026-05-30.md`

如果你不知道下一步做什么，就回到这份文档，从第 6 节开始。
