# 工作包 01 过程记录与当前边界

更新时间：2026-09-13

这份文件记录工作包 01 的实际过程、讨论形成的理解和当前决定。它让后续工作不依赖聊天记录；它不是最终研究结论，也不代表 AutoConsent 维护者已经确认任何问题。

## 我们要解决的问题

项目暂时以 AutoConsent 为案例，研究在人工排查时间有限时，如何从公开运行数据中找到值得优先核查的异常，并在核查后给出有证据的下一步建议。

主线是：

```text
公开 coverage 数据 → 候选调查顺序 → 实际核查 → 解释证据 → 建议行动
```

排序只是中间步骤。当前还没有开始正式排序，也没有确认 bug、违法或真实用户影响。

## 到目前为止做了什么

1. 阅读 Charter、工作包安排和 Decision Log，确认当前只执行工作包 01。
2. 保存当前 coverage、前三份历史 coverage、规则、测试、Playwright runner、README、LICENSE 和 package 文件。
3. 对 coverage JSON 做结构检查，并保存 `evidence/schema_profile.json`。
4. 核对仓库中 38 次 coverage 更新，发现 rule 数量会随快照变化。
5. 选 Bandcamp 作为开发试跑样本，因为它有 coverage 失败样本、网站规则和官方 Playwright 测试。
6. 在干净的桌面 Chromium 环境运行一次 opt-out，并保存日志、环境、失败上下文和截图。
7. 把来源、字段、试跑边界和后续错误分类写入项目文档与 Decision Log。

## 当前 baseline 数据

第一版 baseline 暂定使用最新的 `data/coverage.json` 快照，而不是把历史快照混在一起。

- 最新快照有 205 个顶层 `rule key`。
- 有 433 条 `rule key × region` 记录。
- 地区为 US、GB、DE，但不是每个 rule 都出现在三个地区。
- `rule key` 不是网站数量，也不是平台数量；它是 AutoConsent 仓库中的一套处理逻辑名称。
- 规则可能是通用 CMP 规则（如 `Onetrust`）、网站专用规则（如 `bandcamp.com`）或启发式规则（如 `HEURISTIC-REJECT`）。
- `sites` 是该规则在指定 coverage 网站列表中被检测到的网站数量。

历史上最早快照有 135 个 rule key，历史最多的一次有 223 个；因此 205 只是当前 baseline 的规模，不是整个项目历史的总规则数。

## 字段理解

- `sites`：检测到该规则的网站数量，不是用户数、完整尝试数或成功率分母。
- `errors`：处理该规则时记录到执行错误的网站数量；不能直接解释为规则 bug。
- `selfTestFailures`：opt-out 动作完成后，规则自带的结果检查没有通过的网站数量。
- `exampleSites`：最多 5 个普通匹配网站示例，不是完整列表。
- `failingSites`：最多 5 个 self-test 失败网站示例。
- `errorSites`：最多 5 个处理 error 网站示例。
- `unsuccessfulSites`：实际 JSON 中存在，但官方数据说明没有解释；在找到生成逻辑前不进入核心指标。

`self-test` 可以理解为第三步自动验收：先识别弹窗，再点击 opt-out，最后检查 cookie、页面状态或其他规则定义的条件是否变成预期状态。点击成功而 self-test 失败是可能的；它不等于程序一定报错。

## Bandcamp 试跑记录

本次试跑是开发样本，不是排序结果，也不用于声称历史地区复现。

- 网站：Bandcamp
- 来源快照：2026-08-13 coverage
- 运行：HTTPS、桌面 Chromium、干净上下文、一次 opt-out
- 地区：`LOCAL_UNVERIFIED`，没有配置 US/GB/DE 代理
- 结果：CMP 和 popup 被识别；`optOutResult=true`；一次点击完成；self-test 返回 `false`
- 限制：只运行一次，未能区分页面状态、cookie、地区、网络或规则本身的原因

证据在 `evidence/pilot/`。当前最准确的表述是：该样本显示“操作完成但验证未通过”的现象，而不是“已经确认 AutoConsent 有 bug”。

## 后续核查必须区分的错误阶段

| 阶段 | 含义 |
|---|---|
| 漏检（false negative） | 页面有 consent 弹窗，但没有规则识别到；可能根本不会出现在 coverage error 中 |
| 错分类/误识别 | 网站实际适合规则 A，却识别或尝试使用规则 B |
| 正确识别但执行错误 | rule key 基本正确，但点击、等待或页面处理失败 |
| 执行完成但验证失败 | opt-out 动作完成，但 self-test 没有通过 |
| 环境/页面条件失败 | 网络、地区、cookie 状态、页面改版或运行环境导致异常 |

每条正式核查记录应尽量保存：实际 CMP/页面线索、识别的 rule key、动作、验证条件、失败阶段、运行环境和证据链接。无法判断时写“无法判断”，不强行归因。

`true positive`、`false positive`、`false negative` 不能直接套在 coverage 聚合数字上。要先定义独立、可核验的真实案例，再把识别结果和人工或规则证据对齐。Top-K 样本也不是随机样本，不能据此估计全体规则的总体误报率。

## 当前明确的边界

目前不做：正式 rule 排名或最终权重；把 205 个 rule 当作 205 个平台或网站；把 `errors` 直接当作已确认 bug；把 `selfTestFailures` 直接当作法律违规；把 `unsuccessfulSites` 当作已知含义的失败集合；用 coverage 提交日期冒充网站采集日期；从当前小样本推断总体成功率、recall、误报率或商业收益；公开运行中的账号、凭据、个人信息或未经核查的外部结论。

## 下一步

工作包 01 的可行性闸门已通过，下一步进入工作包 02：将最新 baseline 和历史快照拆成明确粒度的本地分析表，保留 raw/cleaned/analytical 三层关系，检查字段、缺失、重复、规则变化和地区分布，追查 `unsuccessfulSites` 的生成逻辑；在完成 EDA 前不冻结最终排序公式。

## 可公开与暂不公开

适合之后放到 GitHub 的内容：来源说明、字段字典、数据模型、可重建的 schema profile、方法边界、去敏后的试跑摘要和复现说明。暂不直接公开本地环境路径、临时安装日志、未经整理的完整运行报告、可能包含会话信息的截图和未经核实的“bug”表述。
