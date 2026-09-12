# Consent Reliability Triage

这是 data-consent-audit-system 仓库中的一个新项目分支，用于在 10 周、约 30–50 小时的范围内，训练以 Data Science / Analytics 为主体、以业务决策为落点的 consent reliability 分析能力。

项目核心流程是：

~~~
messy public data → candidate issues → verify → prioritize → recommend an action → measure or backtest
~~~

当前主要计划见 [PROJECT_CHARTER.md](PROJECT_CHARTER.md)。

## 项目目标

从 DuckDuckGo AutoConsent 的公开运行数据、历史记录和维护信息中，识别值得优先调查的 consent automation 失败模式，验证候选问题是否真实且可复现，并形成一项能够帮助维护者分配有限测试或维护资源的行动建议。

## 项目边界

- 研究对象是 AutoConsent 的公开运行与维护场景，不是企业内部合规审计。
- 项目不把网站直接判定为违法，也不承诺真实商业 ROI。
- SQL 和本地 analytical warehouse 是计划中的核心能力。
- 真实用户 A/B test 不在范围内；只有在验证后自然出现可执行 Treatment 时，才做小规模、配对随机化的 controlled comparison。
- 最终可以生成一个基于版本化分析结果的轻量级静态开源网站。

## 仓库关系

仓库根目录中原有的 Dynamic Consent Interface Audit System 项目保持不变。本文件夹是后续独立的 Consent Reliability Triage 项目，不覆盖原有研究、数据或代码。
