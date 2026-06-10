# Folder Structure Guide, 2026-05-31

这份文档回答四个问题：

1. 每个文件夹或重要文件里是什么内容？
2. 它们各自的目的是什么，解决什么问题？
3. 哪些部分已经完成，哪些还没完成？
4. 整体进度现在到哪里了？

如果你打开整个 folder 觉得乱，先记住一句话：

> 这个 repo 不是单纯代码仓库。它同时包含研究设计、代码 pipeline、实验数据、自动生成的证据包、paper/poster 草稿、旧参考数据和测试。

## 1. 最重要的阅读顺序

如果你只想重新进入状态，不要从文件树开始一个一个看。按这个顺序看：

1. `docs/research/folder_structure_guide_2026-05-31.md`  
   也就是这份文档，先知道每个地方是干什么的。

2. `docs/research/ssrp_project_clarity_plan_2026-05-30.md`  
   看项目主线：研究什么、不研究什么、10 周怎么走。

3. `docs/research/advisor_meeting_pm_brief_2026-05-31.md`  
   看明天如何跟导师汇报、要问什么问题。

4. `docs/research/week2_checkin_index_2026-06-06.md`  
   这是 Week 2 advisor check-in 的入口文件，里面链接了所有关键 Week 2 证据。

5. `docs/research/ssrp_paper_skeleton_2026-06-06.md`  
   看 paper 应该怎么写。

6. `docs/research/ssrp_remaining_work_audit_2026-05-30.md`  
   看哪些完成了、哪些还没完成。

## 2. Top-Level 文件和文件夹

### `README.md`

内容：

- 项目简介。
- 为什么做这个 consent interface audit。
- 快速开始命令。
- 当前 repo layout。
- 当前 status。

目的：

- 给任何第一次打开项目的人快速理解项目。
- 告诉你常用命令怎么跑。

解决的问题：

- 避免你忘记 CLI 命令。
- 避免每次都从源码猜流程。

完成状态：

- 基本完成，但它是高层入口，不是详细研究计划。

### `AGENTS.md`

内容：

- 给 AI coding agent 的协作规则。
- 项目身份、技术栈、模块边界、编码规范、伦理约束。
- 三个不可破坏原则：每个分数有证据；检测和判断分离；动态路径比静态截图重要。

目的：

- 防止之后的 AI/人把项目做偏。
- 明确这个项目的工程边界。

解决的问题：

- 防止模型随便生成 final score。
- 防止代码把 capture、scoring、storage 混在一起。

完成状态：

- 完成，属于项目规则文件。

### `CONCEPTS.md`

内容：

- Audit ontology，也就是这个研究的概念字典。
- Layer 1：Path Availability。
- Layer 2：Path Effort。
- Layer 3：Transparency & Unbiased Choice。
- Overall score 和 longitudinal primitives。
- 明确排除的东西。

目的：

- 定义“我们到底怎么评价一个 consent interface”。

解决的问题：

- 防止 scoring 标准漂移。
- 防止你写 paper 时概念不统一。

完成状态：

- 核心完成。后续不要轻易改，除非导师明确要求调整 ontology。

### `SCHEMA.md`

内容：

- 项目从 research questions 到 pipeline、data structures、module layout、outputs、deliverables、current status 的总 schema。
- 当前执行顺序和 open decisions。

目的：

- 作为项目全局地图。

解决的问题：

- 让你知道一个 URL 从 capture 到 report/export 的完整流程。
- 让你知道哪些是输入、哪些是输出、哪些是 final deliverables。

完成状态：

- 基本完成，并且已经同步到当前 Week 2 workflow。

### `Chen_Qianyi_SSRP 2026_Proposal_Final Version.docx.pdf`

内容：

- 原始 SSRP proposal。

目的：

- 项目的原始依据。
- RQ1/RQ2 的来源。

解决的问题：

- 防止后面项目做着做着偏离 proposal。

完成状态：

- 已有。平时不用反复读，只有需要确认原始承诺时再看。

### `pyproject.toml`

内容：

- Python package 配置。
- 依赖。
- pytest / mypy / ruff 配置。
- CLI 入口：`consent-audit = "consent_audit.cli:app"`。

目的：

- 让项目作为 Python package 运行。

解决的问题：

- 统一运行命令、测试、lint、类型检查。

完成状态：

- 可用。

### `uv.lock`

内容：

- Python dependency lockfile。

目的：

- 锁定依赖版本，避免不同机器装出不同环境。

完成状态：

- 已有，平时不要手动改。

### `.env.example`

内容：

- 环境变量示例。

目的：

- 提醒后续 API key、budget cap、runtime config 应该怎么配置。

完成状态：

- 示例性质，不是研究主线。

### `task_plan.md`

内容：

- 项目推进的阶段记录。
- 现在已经有很多 phase，从最初 MVP 到 Week 2 artifacts、meeting brief。

目的：

- 记录“我们做过什么、现在在哪个 phase”。

解决的问题：

- 防止长对话/多天工作后失忆。

完成状态：

- 持续更新文件，不是 final deliverable。

### `findings.md`

内容：

- 每次研究/开发发现的结论。
- 包括 smoke probe、Layer 3、weekly pipeline、sample readiness、CMP review、Week 2 状态等。

目的：

- 存放过程中的事实和判断。

解决的问题：

- 防止重要发现只存在聊天记录里。

完成状态：

- 持续更新文件。

### `progress.md`

内容：

- 更细的操作日志。
- 记录改了什么、跑了什么验证、哪些测试通过。

目的：

- 给工作过程留痕。

解决的问题：

- 之后需要回溯“为什么这么做”时有依据。

完成状态：

- 持续更新文件。

### `.git/`

内容：

- Git 版本控制数据。

目的：

- 管理历史版本和 diff。

使用建议：

- 不要手动打开或编辑。

### `.venv/`

内容：

- 本地 Python 虚拟环境。

目的：

- 让你可以跑 `.venv/bin/python -m ...`。

使用建议：

- 不要手动改里面的文件。

### `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`

内容：

- 工具缓存。

目的：

- 加速 mypy、pytest、ruff。

使用建议：

- 可以忽略，不是研究内容。

## 3. `docs/`：研究说明和写作工作台

`docs/` 是你作为 researcher 最该看的地方。它比 `src/` 更重要，因为你的最终交付是 paper/poster，不是单纯代码。

### `docs/architecture.md`

内容：

- 工程架构说明。

目的：

- 解释 capture、scoring、storage、report 的边界。

完成状态：

- 背景文档，基本完成。

### `docs/nlp_design.md`

内容：

- NLP/LLM 相关设计。

目的：

- 说明文本分析、framing、transparency extraction 的思路。

完成状态：

- 背景设计文档，可作为 Layer 3 方法参考。

### `docs/alignment_memo.md`

内容：

- 给 Dr. Singh / Qiyao 对齐用的 memo 草稿。

目的：

- 用来沟通项目方向。

完成状态：

- 草稿，尚未正式发送。

### `docs/outreach/`

内容：

- Outreach 邮件/LinkedIn/校友搜索策略。

目的：

- 辅助找外部资源或 network。

完成状态：

- 不是当前 SSRP 核心，低优先级。

### `docs/references/`

内容：

- 参考资料入口。

目的：

- 放引用和外部资料说明。

完成状态：

- 辅助性。

### `docs/related_work/`

内容：

- 背景文献、rubric landscape、legal cheatsheet。

目的：

- 帮 paper 写 background / related work。

完成状态：

- 可用，但后续写 paper 时还需要精选引用。

### `docs/strategy/`

内容：

- 商业定位、future extension、scope tweak。

目的：

- 记录未来方向和商业化想法。

完成状态：

- 现在不是主线。不要让它影响 SSRP paper 的核心范围。

### `docs/research/`

这是最重要的 folder。它是你的研究工作台。

#### 当前最该看的文件

- `folder_structure_guide_2026-05-31.md`  
  当前这份 folder 导航图。

- `ssrp_project_clarity_plan_2026-05-30.md`  
  中文项目总梳理，解释项目是什么、下周怎么做、10 周路线。

- `advisor_meeting_pm_brief_2026-05-31.md`  
  明天和导师 meeting 的 PM brief。

- `week2_checkin_index_2026-06-06.md`  
  Week 2 advisor check-in 的入口。

- `week2_advisor_update_2026-06-06.md`  
  给导师看的状态更新。

- `ssrp_remaining_work_audit_2026-05-30.md`  
  哪些完成、哪些没完成的审计。

#### Week 2 运行相关

- `week2_execution_runbook_2026-06-06.md`  
  2026-06-06 capture day 的操作手册。

- `week2_capture_day_checklist_2026-06-06.md`  
  capture day checklist。

- `week2_preflight_check_2026-06-06.md`  
  capture 前检查：目标列表、artifact、manifest 是否 ready。

- `week2_sanity_check_2026-06-06.md`  
  capture 后检查：5 个 target 是否都有截图、DOM、hash、report、weekly summary。

- `week2_cycle_report_2026-06-06.md`  
  Week 2 cycle 的运行报告。当前状态是 scheduled date not reached。

- `week2_refresh_report_2026-06-06.md`  
  refresh outputs 后的结果。

- `week2_sample_plan_2026-05-30.md`  
  Week 2 sample freeze 和 CMP draft handling。

#### CMP/manual-review 相关

- `cmp_confirmation_request_2026-05-30.md`  
  给导师确认 8 个 CMP/manual-review rows 的文件。

- `cmp_manual_review_brief_2026-05-30.md`  
  CMP review 背景说明。

目的：

- 防止 pending CMP rows 被误当 final sample。

完成状态：

- review workflow 已搭好，但 8 个 rows 还没被导师/人工确认。

#### Paper/poster 写作相关

- `ssrp_paper_outline.md`  
  paper outline。

- `ssrp_paper_skeleton_2026-06-06.md`  
  论文骨架。

- `ssrp_results_tables_2026-06-06.md`  
  RQ1/RQ2 结果表草稿。

- `ssrp_figure_plan_2026-06-06.md`  
  figure queue。

- `ssrp_writing_pack_2026-06-06.md`  
  methods/results/discussion/limitations 的写作材料。

- `ssrp_claim_register_2026-06-06.md`  
  哪些 claim 有证据、哪些还是 provisional。

- `ssrp_poster_plan_2026-06-06.md`  
  poster storyboard 和素材规划。

完成状态：

- 框架完成，但内容仍是 provisional。需要等 Week 2 live capture、sanity check、CMP confirmation 后才能写成 final claims。

#### Sample/replacement 相关 brief

- `expanded_weekly_capture_brief_2026-05-30.md`
- `replacement_probe_brief_2026-05-30.md`
- `replacement_probe_batch2_brief_2026-05-30.md`
- `sample_strategy.md`

目的：

- 解释 candidate、replacement、sample expansion 的情况。

完成状态：

- 用于扩样本前参考，不是 final sample list。

## 4. `data/`：研究数据和证据产物

`data/` 不是“干净的原始数据 folder”。它现在包含原始输入、pilot 输出、capture 证据、review queue、research package。你不要每个 CSV 都手动打开。要按类别看。

### Site list / candidate list

- `data/sites.csv`  
  早期 placeholder/scaffold site list。不要作为当前正式 capture input。

- `data/sites_smoke.csv`  
  smoke test 用的网站列表。

- `data/deep_sample_candidates.csv`  
  pilot candidate list。

- `data/week2_deep_sample_targets_2026-06-06.csv`  
  当前最重要的正式 Week 2 target list，5 个网站。

状态：

- Week 2 target list 已 ready。
- broader candidate list 还不是 final sample。

### Access probe outputs

这些文件记录网站能不能访问、有没有初步 banner signal：

- `data/access_probe_smoke_2026-05-29.csv`
- `data/access_probe_pilot_2026-05-30.csv`
- `data/access_probe_replacements_2026-05-30.csv`
- `data/access_probe_replacements_batch2_2026-05-30.csv`
- `data/access_probe_v0.csv`

目的：

- 先判断网站是否可访问，减少浪费正式 capture。

状态：

- 已完成多轮 pilot/replacement probe。

### Consent table outputs

这些是每次 capture 后的 weekly record：

- `data/consent_table_template.csv`
- `data/consent_table_smoke_2026-05-29.csv`
- `data/consent_table_pilot_2026-05-30.csv`
- `data/consent_table_replacements_2026-05-30.csv`
- `data/consent_table_replacements_batch2_2026-05-30.csv`

目的：

- 记录 URL、capture date、banner 是否检测到、Accept/Reject/Customize/Dismiss、截图/DOM/hash、notes。

状态：

- 当前主要使用 `data/consent_table_pilot_2026-05-30.csv` 继续追加 Week 2 rows。

### CMP/manual-review outputs

这些围绕 8 个 pending CMP rows：

- `data/cmp_review_queue_pilot_2026-05-30.csv`
- `data/cmp_review_worksheet_pilot_2026-05-30.csv`
- `data/cmp_review_suggestions_pilot_2026-05-30.csv`
- `data/cmp_review_decision_draft_pilot_2026-05-30.csv`
- `data/cmp_review_confirmation_sheet_pilot_2026-05-30.csv`
- `data/cmp_review_rerun_targets_pilot_2026-05-30.csv`
- `data/cmp_review_packet_pilot_2026-05-30/`

目的：

- 把 uncertain/no-banner/CMP rows 拆出来，让人类/advisor 决定，而不是让代码自动决定。

状态：

- 工作流完成。
- 决策未完成：8 个 confirmation 还 pending。

### Sample readiness / sample lock outputs

- `data/sample_readiness_smoke_2026-05-29.csv`
- `data/sample_readiness_pilot_2026-05-30.csv`
- `data/sample_lock_plan_pilot_2026-05-30.csv`
- `data/sample_action_queues_pilot_2026-05-30/`

目的：

- 判断哪些网站 ready、哪些需要 rerun、哪些需要 manual review、哪些要 replacement。

状态：

- pilot sample planning 已完成。
- final deep sample 还没完成，目前只有 5 个 frozen Week 2 targets。

### Replacement outputs

- `data/replacement_candidates_2026-05-30.csv`
- `data/replacement_candidates_batch2_2026-05-30.csv`
- `data/replacement_review_batch2_2026-05-30.csv`
- `data/replacement_weekly_targets_2026-05-30.csv`
- `data/replacement_weekly_targets_batch2_2026-05-30.csv`
- `data/replacement_candidates_contact_sheet_2026-05-30.png`
- `data/replacement_candidates_batch2_contact_sheet_2026-05-30.png`

目的：

- 找更稳定、banner-present 的 replacement candidates。

状态：

- Coca-Cola 已作为 verified replacement 进入 Week 2 target list。
- 其他 replacement candidates 多数不稳定、blocked、或只适合后续参考。

### Research package

- `data/research_package/audit_report_summary.csv`
- `data/research_package/longitudinal_summary.csv`
- `data/research_package/research_manifest.json`

目的：

- 给 paper/poster 用的整洁导出。
- 这是写结果表时最该读的数据包。

当前状态：

- 42 audit reports。
- 20 longitudinal summaries。
- Week 2 live capture 已完成，sanity 是 `ready`。

### Reports store

- `data/reports/audit_reports.jsonl`
- `data/reports/weekly_summaries.jsonl`

目的：

- 机器可读的原始 report / weekly summary 存储。

状态：

- 已有历史 observations。
- 平时不要手改 JSONL。

### Captures

- `data/captures/access_probe/*.png`

目的：

- access probe 截图证据。

状态：

- 已存多轮 probe screenshots。

## 5. `src/consent_audit/`：Python pipeline 源码

如果你不是当天要改代码，不需要从这里开始看。它是工具，不是研究叙事本身。

### `src/consent_audit/cli.py`

内容：

- 所有 `consent-audit ...` 命令入口。

目的：

- 把各个功能变成可运行命令。

完成状态：

- 主要 CLI 已可用。

### `src/consent_audit/models/`

内容：

- Pydantic schema：CaptureBundle、Layer results、AuditReport、WeeklySummary 等。

目的：

- 统一所有数据结构。

解决的问题：

- 防止 LLM/VLM 或代码随便输出不规范数据。

完成状态：

- 核心完成。

### `src/consent_audit/capture/`

内容：

- `agent.py`：Playwright capture / path attempt。
- `fingerprint.py`：DOM/image/text fingerprint。
- `sanitize.py`：截图清理。

目的：

- 抓网页、截图、DOM、路径结果。

完成状态：

- MVP 可用，但真实网站仍可能 unstable/block。

### `src/consent_audit/layers/`

内容：

- `layer1_path_availability.py`
- `layer2_path_effort.py`
- `layer3_transparency.py`

目的：

- 三层 scoring。

完成状态：

- deterministic fallback 已完成。
- model-based extraction 不是当前必须完成项。

### `src/consent_audit/diff/`

内容：

- longitudinal diff logic。

目的：

- 比较同一网站两次 capture 的变化。

完成状态：

- 当前 weekly summary 生成可用。

### `src/consent_audit/llm/`

内容：

- budget logging。
- text / vision wrapper fallback。

目的：

- 未来接 LLM/VLM，同时保证预算和证据约束。

完成状态：

- fallback 可用。
- 大规模真实 LLM/VLM benchmark 还不是当前主线。

### `src/consent_audit/storage/`

内容：

- JSONL/local object-store fallback。

目的：

- 存 report、summary、截图/DOM artifact。

完成状态：

- 本地研究环境可用。

### `src/consent_audit/report/`

内容：

- Markdown report generator。

目的：

- 把 scoring 和 evidence 变成人类可读 report。

完成状态：

- 可用。

### Orchestration / export modules

这些文件把研究流程串起来：

- `pipeline.py`：single-site / weekly pipeline。
- `research_package.py`：导出 paper-facing package。
- `research_status.py`：生成当前状态 dashboard。
- `advisor_brief.py`：生成导师 update brief。
- `checkin_index.py`：生成 Week 2 check-in index。
- `week2_cycle.py`：Week 2 full cycle。
- `week2_refresh.py`：refresh package。
- `week2_preflight.py`：pre-capture gate。
- `week2_sanity.py`：post-capture sanity gate。
- `week2_checklist.py`：capture day checklist。
- `week2_plan.py`：Week 2 target/sample plan。
- `cmp_review.py`：CMP/manual review artifacts。
- `sample_readiness.py`：candidate readiness。
- `sample_lock.py`：sample decision queues。
- `replacement_review.py`：replacement candidates。
- `paper_skeleton.py`、`paper_tables.py`、`paper_figures.py`、`paper_writing_pack.py`、`paper_claims.py`、`poster_plan.py`：paper/poster artifacts。

完成状态：

- 研究脚手架和 Week 2 workflow 已经很完整。
- 还缺的是 scheduled live capture 和人工 sample decisions，不是基础代码。

## 6. `scripts/`：兼容旧运行方式的小入口

内容：

- `run_audit.py`
- `run_weekly.py`
- `access_probe.py`
- `access_probe_summarize.py`
- `export_audit_reports.py`
- `export_longitudinal_summary.py`
- `export_research_package.py`
- `_bootstrap.py`

目的：

- 保留直接运行脚本的方式。
- 让旧命令仍然可用。

当前建议：

- 优先用 `PYTHONPATH=src .venv/bin/python -m consent_audit.cli ...`。
- 不要从 scripts 里猜主流程。

完成状态：

- 兼容层可用。

## 7. `tests/`：验证代码和研究 artifacts 的测试

内容：

- `tests/layers/`：Layer 1/2/3 scoring tests。
- `tests/capture/`：capture/fingerprint/sanitize tests。
- `tests/diff/`：longitudinal diff tests。
- `tests/llm/`：budget/text/vision wrapper tests。
- `tests/report/`：report generator tests。
- `tests/storage/`：storage/object-store tests。
- `tests/scripts/`：script entrypoint tests。
- `tests/test_*.py`：CLI、research package、paper artifacts、Week 2 artifacts 等测试。

目的：

- 证明 pipeline 和 artifact generators 没坏。

完成状态：

- 测试覆盖已经比较完整。
- 但测试通过不代表研究完成；研究还需要 live capture、manual review、paper writing。

## 8. `Qiyao's data collection_0912/`

内容：

- 旧数据 collection。
- 当前统计看到大约 91 个 xlsx 和 231 张 png。
- 每个网站一个 folder，例如 `bbcuk`、`amazon_uk`、`weather` 等。

目的：

- 作为历史参考 / background。

解决的问题：

- 可以看之前 PhD/mentor 数据长什么样。
- 可以帮助理解 consent/privacy notice evidence。

当前状态：

- 不是当前 SSRP pipeline 的主输入。
- 不要把它和当前 Week 2 sample 混在一起。

## 9. 哪些已经完成

可以认为完成或基本完成的部分：

- 研究主线已经明确：RQ1 scoring + RQ2 longitudinal capture。
- Audit ontology 已定义：Layer 1/2/3。
- Python package 和 CLI 已搭好。
- Capture/scoring/report/export pipeline 已能跑。
- Deterministic Layer 1/2/3 fallback 已实现。
- Research package export 已有。
- Week 2 target list 已冻结为 5 个网站。
- Week 2 runbook / preflight / sanity / checklist / cycle report 已有。
- Advisor update 和 meeting PM brief 已有。
- CMP/manual-review workflow 已搭好。
- Paper skeleton、results tables、figure plan、writing pack、claim register、poster plan 已有。

## 10. 哪些还没完成

真正没完成的是研究执行和最终写作，不是“完全没有框架”。

未完成 / 仍然 gated：

- Week 2 sanity check 已经是 `ready`。
- 5 个 Week 2 evidence bundles 需要用 `data/week2_manual_evidence_review_2026-06-10.csv` 做人工确认。
- 8 个 CMP/manual-review rows 还没有导师/人工确认。
- deep sample 目前只有 5 个 frozen targets，还没扩到约 20 个。
- paper/poster 还不是 final draft，只是 scaffold/provisional artifacts。
- demo/evidence browser 还没必要优先做。
- 最终 dataset freeze 要等 Week 10 左右。

## 11. 整体进度判断

现在项目处于这个阶段：

> 研究框架和工具链已经搭好，进入“按周收集证据 + 人工确认 sample + 写 paper”的阶段。

不是：

- 不是刚开始。
- 不是已经完成。
- 不是需要马上做大规模商业 demo。
- 不是需要重写代码。

更准确地说：

- 工程 scaffolding：约 70-80% 已完成。
- 研究数据收集：刚进入正式阶段，约 20-30%。
- sample lock：未完成，需要导师确认。
- paper/poster：结构已搭好，正文和最终图表还没完成。
- demo：低优先级，可后置。

## 12. 你每天最该看的地方

如果你每天只打开 3 个东西，打开：

1. `docs/research/week2_checkin_index_2026-06-06.md`
2. `docs/research/ssrp_project_clarity_plan_2026-05-30.md`
3. `docs/research/advisor_meeting_pm_brief_2026-05-31.md`

如果你只跑 1 个命令，跑：

```bash
PYTHONPATH=src .venv/bin/python -m consent_audit.cli research-status
```

## 13. 下一步最清楚的动作

1. 明天 meeting 用 `docs/research/advisor_meeting_pm_brief_2026-05-31.md`。
2. 和导师确认 no-banner/CMP handling。
3. 等 2026-06-06 跑 Week 2 live capture。
4. capture 后跑 refresh 和 sanity。
5. 再扩 sample，不要现在盲目追 80+。
6. 每周把 evidence 写回 paper skeleton / writing pack。
