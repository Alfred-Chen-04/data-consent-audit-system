# Feasibility report（工作包 01）

## 结论

建议继续，但缩小当前承诺：进入工作包 02 时先使用 coverage 聚合数据、规则/测试元数据和少量可访问样本；不把 `unsuccessfulSites` 放进核心指标，不把 snapshot commit 日期当作采集日期，也不承诺历史故障检出率。

## 已完成检查

- 最新 coverage 可解析，无重复 JSON key；205 个 rule、433 条 rule×region 记录。
- 计划字段均存在。所有七个实际字段在 433 行中均出现；官方说明没有解释 `unsuccessfulSites`。
- `exampleSites`、`failingSites`、`errorSites` 均是合法 HTTP(S) URL 列表，且最多 5 个；跨列表去重后有 1304 个 URL，但 242 个 URL 出现在多个 rule/region/字段位置，不能按 URL 直接计数。
- 最新快照 US 的 `errors` 全为 0，但有 18 条记录、合计 96 个 `selfTestFailures`；因此 error-count baseline 在 US 不提供排序差异。
- 三个地区都有错误或 self-test 信号，但数量和规则组成随快照变化。最近两对快照分别只有 414/433、386/425 个 rule×region key 重合；历史可比性尚未建立。
- Bandcamp 规则和官方测试存在，能追溯到 `detectCmp`、popup、opt-out button 和 cookie self-test。

## 最小试跑

试跑证据在 `evidence/pilot/`：运行前固定了 protocol，使用一台桌面 Chromium、干净上下文、HTTPS Bandcamp、opt-out，一次运行，未使用地区代理。

观察到：

1. CMP 被识别，popup 被找到；
2. `optOutResult` 为 `true`，一次点击完成，运行耗时约 2005 ms；
3. `selfTestResult` 为 `false`，Playwright 测试因此失败；
4. 截图、日志、环境、失败上下文均已保存。

这证明最小闭环在技术上可运行，也证明 coverage 的 self-test failure 不能直接写成“规则完全不能操作”：本次操作完成了，但测试条件没有通过。由于没有地区代理、只运行一次，不能声称已复现 US/DE/GB 的历史采集结果，也不能判断失败根因。

## 历史和比较能力

仓库中至少有 38 次 coverage 更新，且最新三份可重建。当前可以做：规则/地区 key 的变化、信号是否在多个快照出现、示例 URL 是否变化。当前不能做：逐网站历史真值、全体候选 recall、真实错误率或因果效果。规则重命名、top-site 列表变化、采集时间缺失都需要在后续连接前处理。

## 初步工时情景

本次自动运行约 16 秒，但人工有效核查时间不能由脚本时间代替；截图阅读、网络失败、重跑和写记录应单独计时。建议下一步对 2–3 个开发样本实测后再冻结预算：

| 范围 | 计算口径 | 当前判断 |
|---|---|---|
| 自定义 Top 10 | 10 个候选基础核查；若与基线比较，最多核查两组并集 20 个候选 | 目标可行，但需实测人工分钟数 |
| 自定义 Top 20 | 同 K 基线并集最多 40 个候选 | 暂不承诺；很可能超过 7–8 周预留核查时间 |

## 工作包 02 的边界

先建立 raw/cleaned/analytical 三层的本地表，但只保留能解释的字段：快照、rule、region、计数、五类 URL 列表、来源 commit、规则元数据和后续核查记录。EDA 先描述 missingness、key 漂移、计数分布和跨快照持续性；在这些检查完成前不设计最终权重或排名。

## 尚未解决的问题

- `unsuccessfulSites` 的生成语义和与 `errorSites`/`failingSites` 的关系；
- 本地运行如何稳定模拟 US/GB/DE 条件；
- Bandcamp self-test false 的具体原因，是页面状态、cookie、规则、网络还是地区差异；
- 人工每个候选的真实耗时。

## 后续核查必须保留的错误分类框架

coverage 的 `errors` 或 `selfTestFailures` 只是异常信号，不能直接写成“规则有 bug”。每个候选在后续核查中都要尽量区分以下阶段：

| 分类 | 含义 | 可能在 coverage 中表现为 |
|---|---|---|
| 漏检（false negative） | 页面有 consent 弹窗，但没有任何规则识别到它 | 可能完全没有记录；不能只看 `errors` 发现 |
| 错分类/误识别 | 网站实际使用规则 A，却被识别或尝试使用规则 B | 可能随后出现 `errors` 或 `selfTestFailures`，但字段不会直接说明原因 |
| 正确识别但执行错误 | rule key 对应的规则基本正确，但点击、等待或页面处理过程出错 | `errors` / `errorSites` |
| 执行完成但验证失败 | opt-out 动作返回完成，但规则定义的 self-test 没有通过 | `selfTestFailures` / `failingSites` |
| 环境或页面条件失败 | 网络、地区、cookie 状态、页面改版或运行时条件导致结果异常 | 可能表现为上述任一信号 |

后续每条核查记录至少要记录：页面实际 CMP/弹窗线索、AutoConsent 识别的 rule key、执行动作、验证条件、失败阶段和证据链接。若无法判断阶段，状态写为“无法判断”，不强行归因。

术语说明：这里的 true positive / false positive 不能直接套在 coverage 聚合数字上。只有先定义“什么是独立核验的真实案例”，并把识别结果与人工或规则证据对齐后，才可以讨论误报、漏报或检出情况。Top-K 核查样本也不是随机样本，不能据此估计全体规则的总体误报率。
