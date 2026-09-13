# Data dictionary（初稿）

## Coverage 行

一行定义为一个快照中的一个 `rule × region` 记录。最新快照有 205 个 rule、433 行；并非每个 rule 都在三个地区出现。

| 字段 | 类型 | 最新快照检查 | 可用于 | 当前不能用于 |
|---|---|---|---|---|
| rule key | string | 205 个 | 连接规则、测试和维护记录 | 默认视为跨快照稳定 ID；重命名需另查 |
| region | string | US/GB/DE | 分组和可比性检查 | 推断用户真实所在地或完整地区覆盖 |
| `sites` | integer ≥1 | 1–1195 | 被检测到该规则的站点数（影响范围代理） | 用户数、全部尝试数、成功率分母 |
| `errors` | integer ≥0 | 最大 2；最新 US 全为 0 | 处理规则时的错误信号 | 错误根因；与其他失败数直接相加 |
| `selfTestFailures` | integer ≥0 | 最大 69 | 有 self-test 的规则未通过验证的计数信号 | 所有规则统一失败率；没有失败不证明成功 |
| `exampleSites` | list[str] | 每行最多 5 个；13 行为空 | 找到可访问样本 | 完整样本清单 |
| `failingSites` | list[str] | 每行最多 5 个；365 行为空 | 找到 self-test 失败样本 | 完整失败集合或历史真值 |
| `errorSites` | list[str] | 每行最多 5 个；430 行为空 | 找到 error 样本 | 完整错误集合 |
| `unsuccessfulSites` | list[str] | 实际存在；官方说明未解释 | 暂存并调查生成口径 | 进入核心指标或解释为某种失败 |

## 三种分析单位

- 原始记录：`snapshot × rule × region`。例如最新 Bandcamp/US 行：`sites=1, errors=0, selfTestFailures=1`，并列出 `http://bandcamp.com/`。
- 核查运行：`website × environment × time × run_id`。本次试跑是 Bandcamp、HTTPS、桌面 Chromium、`LOCAL_UNVERIFIED`、一次 opt-out 运行。
- 决策候选：一条明确的 rule、region、异常信号和证据链接组成的调查对象。本次开发样本可写成“Bandcamp rule 在三地区快照均有 self-test failure 信号，先核查该样本”，但它尚未经过排序选择。

候选数、网站数和运行次数必须分别计数。
