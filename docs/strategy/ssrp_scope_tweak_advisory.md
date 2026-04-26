# SSRP Scope Tweak — Advisory ONLY

**作者**: Qianyi (Alfred) Chen
**日期**: 2026-04-26
**状态**: ⚠️ **Advisory only** — 全部建议都是可选的, SSRP 主线 scope 不需要因此改变。
**关联**: 这是 `positioning_and_future_extension.md` 的姊妹文档。
后者讲 9 月后延伸方向, 本文档讲"如果以后真要启动延伸方向, 暑假期间可以做哪些极轻量的微调让未来工作无缝复用"。

---

## ⚠️ 头部声明

**此文档目的**: 如果未来某天 (9 月后) 真的启动延伸方向 (见
`positioning_and_future_extension.md`), 那么 SSRP 暑假期间做的工作可以**无缝复用**,
而不需要 SSRP 期间承担任何额外风险。

**此文档非目的**:
- 不是要求 Alfred 做这些。
- 不是为了商业化牺牲 SSRP 学术 integrity。
- 不是 Dr. Singh 的工作 scope 增加。

**默认决策**: 全部忽略, SSRP 按原计划走, 不影响任何东西。
**采纳决策**: 单独评估每一条 (B.1, B.2, B.3, B.4), 可单独采纳, 也可全部采纳, 也可全忽略。

---

## A. 哪些**不应该**改 (优先讲)

以下内容是 SSRP 学术 integrity 的核心, **绝对不动**:

### A.1 论文 framing
不要为商业化提前在论文 abstract / introduction / contribution 中加商业叙事。
论文的 audience 是 HCI / privacy / AI 学术圈, 商业化叙事会损害学术评审。

### A.2 与 Dr. Singh 的合作 scope
不要把"商业延伸"提到 Dr. Singh 面前作为 SSRP 的目标。Dr. Singh 是学术导师, 期望
是学术产出。商业方向是 Alfred 个人独立线, 不动师生关系定义。

### A.3 `CONCEPTS.md` 的 ontology
audit 的三层架构 (Path Availability / Path Effort / Transparency & Unbiased Choice) 是
论文核心方法论。**不动**。任何商业映射都基于这个 ontology 作为 source of truth, 而不是反过来。

### A.4 `docs/architecture.md` 现有架构
capture / layers / llm / models 模块边界不动。任何"延伸用得着"的字段都作为 optional 加, 不重构。

### A.5 现有 outreach 文档 (`docs/outreach/01-04`)
内容 / 措辞 / 联系顺位都不动。这些是 SSRP 学术资源积累的, 商业方向应该有独立的 outreach line。

---

## B. 极轻量、可选的微调建议 (每条独立)

每一条可以**单独**采纳或忽略。任意组合都可行。

### B.1 数据集层 — sub-cohort 标签

**做什么**: 在 `data/sites.csv` 中, **增加一列** `china_overseas_cohort` (bool), 把
"中国 HQ 但服务欧盟用户的网站"标记为 `True`。建议候选名单:

| 类别 | 站点 (举例) |
|---|---|
| 跨境电商 | Shein.com (EU), Temu.com (EU), AliExpress.com (EU), Lightinthebox |
| 智能硬件全球站 | Anker.com, EuFy.com, Roborock.com, Dreame-technology.com |
| 内容 / 社交 | RedNote (xiaohongshu 国际), miHoYo / HoYoverse, TikTok Shop EU |
| B2B SaaS | Alibaba Cloud (EU 区域站), DingTalk International |
| 视频 / 直播 | Bigo Live, Kwai International |

建议数量: **20 个站点**作为子集, 现有总样本 + 20。

**论文层面**: 子集**不需要在论文里专门讨论**。可以一提"我们的样本中包含 X 个 cross-border vendor 站点"作为代表性的一笔, 但不需要专章分析。

**复用价值**: 9 月后做 vendor 访谈 / Phase 0 demand-side validation 时, 数据可直接调出来作为对话锚点。

**成本**: 增加 ~20 个站点 + 一列布尔标签 + 选样时多一道筛选。
**决定窗口**: ⏰ **最迟 2026-05-31** — 之后 site 选样定型, 后期插入会污染 baseline。

---

### B.2 报告 schema 层 — 可选 regulatory mapping 字段

**做什么**: 在 `src/consent_audit/models/audit.py::AuditReport` (或对应 schema) 中
**增加一个 optional 字段**:

```python
regulatory_mapping: Optional[dict[str, list[str]]] = None
# 例: {
#   "finding_id_xxx": ["GDPR Art. 7(2)", "GDPR Art. 12(1)", "ePrivacy Dir. 5(3)"],
#   "finding_id_yyy": ["CCPA §1798.135", "DSA Art. 25"]
# }
```

**实现路径**: 在每个 finding (Layer 1/2/3) 的输出处, 增加一个 optional `cite_regs:
list[str]` 字段, 然后 aggregator 收集成 `regulatory_mapping` dict。

**默认行为**: 不导出, 不进论文 PDF, 不进 evaluation table。论文里这个字段就是不存在的。

**复用价值**: 9 月后切换商业模式时, 模块已经在那里, 不用重写。
**成本**: 几小时 schema 设计 + 每个 finding 处加一个字典查表 (可以用 LLM-assisted 一次性生成 GDPR 条款映射表)。
**决定窗口**: ⏰ **任何时候都行** — 不在关键路径。

**注意**: 实现时可以用 LLM (Claude / GPT) 一次性生成 GDPR / CCPA / DSA / PIPL 条款 mapping 表
作为静态查表, 不需要 runtime LLM 调用。这件事本身可能是另一个有趣的小研究 — 但 SSRP 主线不依赖。

---

### B.3 论文 abstract / discussion — 留 1-2 句开放讨论

**做什么**: 在论文 discussion / future work 部分留 **1-2 句**关于
"applicability to cross-border vendor due diligence" 的开放讨论。

**举例措辞 (供参考)**:

> "While our framework is methodologically focused on visitor-facing consent UI quality,
> the same evidence types (multi-modal capture, longitudinal diff, structured layer scoring)
> map naturally onto the artifacts that enterprise privacy due-diligence workflows
> demand from third-party vendors — particularly for cross-border B2C platforms operating under
> overlapping GDPR and ePrivacy regimes. We leave this commercial application as future work."

**为什么这样写**:
- 不宣称"商业 contribution" — 学术评审看不出过度宣传。
- 但提及"applicability" — 之后给 vendor / procurement 做 outreach 时, 可以引用论文这一句作为 anchor。
- 让论文成为对外的 trust anchor, 而不是只在学术圈流通。

**决定窗口**: ⏰ **写 discussion 时再决定** — 7 月后, SSRP 后半段。

---

### B.4 内部 working memo — Post-SSRP outreach 候选清单 (不发送)

**做什么**: 在 `docs/outreach/` 下创建一个**内部草稿** (例如 `99_post_ssrp_outreach_draft.md`),
**先列**未来 9 月后可能联系的 EU procurement / CISO / DPO 联系池。

**重要约束**:
- ⚠️ **不发送**, 不开始联系。
- ⚠️ **不在 SSRP 期间**和 Dr. Singh 提到这条 outreach line。
- 文档头部明确写 "DO NOT SEND BEFORE 2026-09-01"。

**对象示例 (待 Phase 0 时再填实名)**:
- 欧盟大型零售 / 电商平台 vendor security 团队 (买中国 IoT)
- 欧盟跨境支付 / 物流公司 DPO
- 欧盟保险 / 金融 procurement
- 欧盟 DPA (regulator)

**复用价值**: 9 月时不用从零开始, 池子已经在那里。
**成本**: 0-2 小时, 任何时候有空都能做, 比如周末闲下来。
**决定窗口**: ⏰ **任何时候都行**, 内部 memo 不影响外部。

---

## C. 决定窗口汇总

| 建议 | 决定窗口 | 紧迫程度 |
|---|---|---|
| B.1 数据集 sub-cohort 标签 | ⏰ **最迟 2026-05-31** | **高** (后期插不进) |
| B.2 schema regulatory_mapping 字段 | 任何时候 | 低 |
| B.3 论文 framing 1-2 句 | 写 discussion 时再说 (~7 月) | 低 |
| B.4 post-SSRP outreach 草稿 | 任何时候 | 低 (但建议早做以免遗忘) |

**真正紧迫的只有 B.1**。其他都可以 SSRP 中期 / 后期再决定。

---

## D. 如果选择"全部忽略"会发生什么

**完全可行**。SSRP 仍然产出原计划的论文 + codebase + 数据集, 论文质量和发表前景不受影响。

**机会成本**: 9 月后启动延伸方向时, 会多花约 **2-4 周**补做 B.1 (重新抓 20 个中国 vendor 站点) +
B.2 (在已经稳定的 schema 上加 regulatory mapping)。这不是阻塞, 只是浪费一点重复时间。

**判断标准**: 如果 Alfred 在 8 月之前对延伸方向**信心不足 50%**, 全部忽略是合理选择 — 不要为了一个不确定的未来在 SSRP 期间额外承担注意力成本。如果信心 > 70%, 至少做 B.1 + B.4 (这两个最便宜)。

---

## E. Changelog (供 Alfred 之后追加)

- 2026-04-26: 文档创建 (Claude assist Alfred)
- (留空, 之后采纳 / 否决任何一条时来这里记一笔)

---

## F. Alfred 现在不需要做任何决定

阅读完即可。任何决定都可以稍后慢慢来 — 除了 B.1 在 5 月底前必须 yes/no。
其他在论文写到对应章节时再决定即可。

如果阅读完有疑问, 起新对话, 按 `B.x` 标号定位讨论。
