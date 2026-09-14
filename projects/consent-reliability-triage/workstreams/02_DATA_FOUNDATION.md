# 工作包 02：数据基础与 EDA

> 对应周次：3–4｜计划工时：9 小时

## 这一块要回答什么

怎样把已经确认可用的公开数据整理成可信、可重复查询的分析表？数据里实际出现了哪些值得解释的现象？

## 依赖输入

- 已完成的工作包 01 及其 feasibility decision
- `docs/source_inventory.md`、`docs/data_dictionary.md`
- 冻结的数据来源、时间范围和候选单位
- `COLLABORATION.md`、`DECISION_LOG.md` 和 `docs/WORK_PACKAGE_01_RECORD.md`

固定 baseline 为 `evidence/sources/coverage_c2e9fcd6c22a.json`，身份与哈希依据 manifest 核验。控制值为 205 个 rule key、433 条 rule × region 记录；未来上游更新不替换本轮输入。历史快照先检查可比性，不直接混入 baseline。

## 具体任务

1. 建立最小目录和本地分析数据层，优先使用 DuckDB；若工作包 01 有充分理由也可用 SQLite。
2. 保留 raw、cleaned 和 analytical 层，记录来源版本与采集时间；原始文件保持不可变。
3. 分开建模 coverage 聚合事实与逐次核查事实，设计稳定主键和候选 ID，避免多对多 JOIN 放大计数。
4. 用 SQL 完成类型转换、去重、规则名称映射、有效观测标记和基本质量检查。
5. 做 EDA：覆盖范围、缺失模式、异常计数、地区／规则分组、可比较快照和时间变化。
6. 写出 3–5 个候选 insight。每个 insight 按“观察 → 可能解释 → 其他解释 → 需要的证据 → 对决策可能有什么影响”记录。
7. 为规则建立有来源、版本、分类理由和置信说明的初步分类；规则类型与地区适用性分开，证据不足标 unknown。

## 执行与独立审查

执行 agent 负责数据流程、分析与修正；独立审查者只提交审查和复核记录，不直接修改主实现。具体按 [协作方案](../COLLABORATION.md) 执行：

- G1：任务 1–4 完成后检查原始数据对账、字段类型、缺失、主键、JOIN 和可重建性，通过后开展依赖这些表的 EDA。
- G2：EDA 初稿后检查分类证据、地区和历史可比性、候选问题及结论边界。
- `sites` 是数量，只能从各类示例数组建立网站示例表，不能展开完整网站集合或要求示例数等于 `sites`。
- 本包不做正式排名；`unsuccessfulSites` 保留原值，语义未明确时不进入核心指标。

## 产出

- 可重建本地分析库的脚本
- `sql/` 中的清洗、建模、质量检查和 EDA 查询
- `docs/data_dictionary.md` 定稿
- `docs/data_quality_report.md`
- `analysis/eda.*` 和初步 insight 记录
- `docs/WORK_PACKAGE_02_RECORD.md`：进度、复现方式、决定和交接
- `reviews/WP02/`：G1／G2 审查版本、问题、回复和复核结果

## 完成标准

- 从原始输入可以一条命令重建核心分析表。
- 主键、粒度、缺失和适用性经过检查；关键 JOIN 不会静默增加记录。
- EDA 中的每个数字可以追到 SQL 和来源。
- 现象与根因分开表达，没有把 coverage 计数写成用户成功率。
- 工作包 03 能直接使用一张明确的 candidate feature base，而无需重新清洗数据。
- G1／G2 有实际独立审查记录，影响核心结果的问题已关闭；接受的限制及其对下游影响有记录。未启动审查时标待审，不视为通过。

## 本块重点训练

SQL JOIN、CTE、窗口函数、条件聚合、数据建模、data lineage、质量检查，以及从分布和缺失中提出可验证问题。

## 新对话开场提示

> 请阅读项目 Charter、`WORKSTREAMS.md`、`COLLABORATION.md`、`workstreams/02_DATA_FOUNDATION.md`，再读取工作包 01 的全部产出和 `DECISION_LOG.md`。我们现在只执行工作包 02：用 DuckDB／SQLite 建立可重建的数据层，完成数据质量检查和 EDA，并形成有证据的初步 insight。核验固定 baseline，保留原始数据，先确认粒度和 JOIN；仅将网站数组建成示例表。按 G1／G2 提交固定版本供独立审查，未审查则明确标待审。本包不做正式排名；所有代码、结果和决定保存到仓库，并维护工作包 02 交接记录。
