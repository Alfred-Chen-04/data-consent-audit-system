# Positioning & Future Extension Roadmap

**作者**: Qianyi (Alfred) Chen
**日期**: 2026-04-26
**状态**: 战略参考文档 — 不影响 SSRP 主线工作
**关联**: 这是 SSRP 项目 (`README.md`, `CONCEPTS.md`) 之外的**延伸方向沉淀**, 9 月之后启动。
SSRP 暑假 scope 完全不依赖此文档。

---

## 0. 一句话定位 (草稿, 待迭代)

> **"为中国出海 vendor 生成欧盟买方可读的、人类签字 + AI 持续验证的隐私合规证据包 —
> 不当认证机构本身, 而做认证生态的中介信任桥。"**

这是**对内**的一句话。对外可视客户群再精炼。

关键词解释:
- **"为中国出海 vendor"** — 客户端清晰: 服务对象是 China-HQ、服务海外用户的 SaaS / e-com / IoT / B2B
  公司。**不是国内业务**, 不是欧美 vendor。
- **"欧盟买方可读"** — 报告的目标读者是**欧盟买方** (procurement, CISO, DPO, DPA),
  不是中国老板看的合规自我安慰报告。语言、引用条款、证据类型必须是欧盟侧的认知格式。
- **"人类签字 + AI 持续验证"** — 双层结构: AI 做监控 + 证据收集 (这是降本环节);
  人类 auditor 命名签字 + 承担 E&O 责任 (这是不可被 AI 替代的环节)。
- **"不当认证机构本身, 而做认证生态的中介信任桥"** — 不直接发 cert, 不发 seal。
  报告**映射到买方已经信任的框架** (ISO 27701 / SOC 2 Privacy TSC / GDPR Art. 32),
  借力既有信任。这是**反 TRUSTe 失败模式**的核心选择。

---

## 1. 战略洞察 synthesis (4 路调研提炼)

### 1.1 AI 不吃签字, 只吃签字内部的劳动

**事实 (2026 Q1)**: 2026-02-20 Anthropic 发布 Claude Code Security, 两天内 CrowdStrike 跌
6.8%, Okta 9.2%, Cloudflare 8.1%, JFrog 约 25% (CNBC, Bloomberg, SiliconAngle)。
Palo Alto CEO 称这次抛售"paranoid"; CrowdStrike Q4 FY26 营收同比仍涨 23%。

**结构性解读**: 同期 Vanta、Drata 把自己 rebrand 成"agentic trust platforms",
Vanta 的 AI agent 声称对 vendor 安全问卷回答 95% 准确。GRC 顾问的 50K-100K 美元/单
工作正在被压成 SaaS 价格。但 Schellman、A-LIGN、Coalfire 这些**专做 attestation 签字**
的精品事务所**反而在涨价** — 因为它们的成本被 AI 降低了, 客户却还是必须有签字。

**为什么签字层结构性安全**:
- **Regulator-named bodies**: SOC 2 报告**必须** CPA 事务所签字; ISO 27001 证书**必须** UKAS / ANAB 认证机构签发;
  EU AI Act 要求 notified bodies 做高风险系统 conformity assessment。LLM 不能成为 notified body —
  认证身份发给法律实体, 配 E&O 保险、命名审计员、政府登记。
- **Insurance gates**: 2025 年起, 网络保险承保人**不再接受**自我声明的 MFA / EDR / backup 控制 — 必须第三方证据 + 命名高管签字承担个人法律责任。
- **Liability transfer / "trust laundering"**: 客户 A 找 vendor B 要保证, A 不要 B 自己 AI 生成的 PDF, A 要的是**一个出问题可以告的第三方**。这是 30 年来财务审计软件没有杀死 Big-4 的同样道理。

**对本项目的启示**: 如果定位"扫描工具" → 直接和 Claude Code Security 比, 必输。
如果定位"签字方 / 中介信任桥" → AI 是**成本杠杆**, 不是竞争对手。

### 1.2 TOEFL 起飞条件 — 反向工程出三个必要条件

**TOEFL/UL/PCI/SOC 2 起飞共同点**:
1. **协调的需求侧 + kill switch**: UL = 保险公司联合拒保; PCI = Visa/MC 可以切支付通道; SOC 2 = 企业 procurement 把它写进合同; TOEFL = 1964 年福特基金会 + College Board + 大学联盟。
2. **比替代方案便宜**: SOC 2 替代了 200 题 vendor 安全问卷, 因此被采纳。
3. **认证链中立**: 认证机构由买卖任一方都不控制的第三方 accredit (AICPA, ISO/IAF, PCI SSC)。

**反面教材**:
- TRUSTe (1997-): Edelman 2006 实证研究 — TRUSTe 网站违反隐私的概率比非 TRUSTe **高 50%**。FTC 2014 起诉造假。失败原因: **没有协调的买方需求**。
- ePrivacy Seal (德国): **2025 年 5 月清算关门**。
- BBB Online Privacy / TRUSTe 现状: 网站装饰品, 不进 procurement 问卷。

**最关键的一句**: **founding consortium = the gatekeepers, not the test-takers**。
TOEFL 不是创业公司 pitch 大学的故事, 是大学联盟创办的故事。从 vendor 端做"印章
卖给中国公司"= 重复 TRUSTe 的死法。**所以 Phase 0 必须先访谈 buyer side, 不是 vendor side**。

### 1.3 现有 privacy 认证生态 — 真实空白

**真在 procurement RFP 里要的** (ISC2 2025 调研: 77% 列为 vendor 必要条件):
- SOC 2 (AICPA) — Privacy TSC 是真实差异化点
- ISO 27001 (基线)
- ISO 27701 (rising, 2025 版**可独立认证**了, 不再要求 27001 prereq)

**特定区域 / 行业要的**:
- C5:2025 (BSI 德国) — 德国公共部门 / 医疗云强制
- CSA STAR L2 — 云采购
- Europrivacy — 唯一 EDPB endorsed 的 GDPR Art. 42 认证, 接收了 ePrivacy Seal 的衣钵

**装饰品 (procurement 不审)**:
- TrustArc / TRUSTe
- BBB Online Privacy
- OneTrust Credly 部署徽章

**已经死的**: ePrivacy Seal (2025-05 清算)、EuroPriSe

**海外不认的**:
- 中国 PIP 跨境认证 (2026-01 生效, CAC + SAMR 主导): 海外买方不会信中国官方机构签的字。
- APEC Global CBPR (2025-06 启动): **大陆中国不参与**, 直接对中国 vendor 没用。

**真实空白 (无人填)**:
1. **持续机器验证的 consent-UX attestation** — 没有任何 cert 专门审 GDPR Art. 7/12 valid consent
   / cookie banner dark patterns / CCPA opt-out flow。CNIL 2025 年罚了 €486.8M,
   83 起 sanctions, 但事后罚款不解决事前 due diligence。
2. **"中国 vendor × 海外买方信任" 专属 attestation** — 既不是 Big-4 (太贵, 中国 SME 付不起),
   也不是中国官方 (海外不认), 也不是 vanity badge。这一格是空的。

### 1.4 中国出海 corridor 的 privacy 摩擦地图

| 地理 | 摩擦类型 | privacy-cert 是否能解 |
|---|---|---|
| **中国 → 美国** | **地缘政治** (CFIUS, NDAA, FCC, BIS, 国家安全审查) | ❌ — 任何 cert 都救不了 TikTok 类型问题 |
| **中国 → 欧盟** | **privacy 合规** (GDPR, DSA, RED, EU Data Act) — 已在执法 | ✅ — Shein €150M cookie 罚单证明: 罚的是 cookie 违规, 不是因为是中国公司 |
| **中国 → 沙特/UAE** | privacy (PDPL, 48 起执法) — 无反华 | ✅ — Vision 2030 buyer pull 强 |
| **中国 → SEA** | 法律有, 执法弱, 买方未问 | ⚠️ — 时机太早 |
| **中国 → 巴西/拉美** | privacy (LGPD, 2025-08 跨境新规) | ✅ — 但买方 pull 待验证 |

**最重要的判断**: 美国不在候选内, 不是因为难, 是因为**问题类型错了**。CFIUS 看的是
"你是不是被中国政府控制 / 中国母公司能不能拿到数据" — 这是 ownership / sovereignty 问题,
不是 cookie banner 问题。任何 cert 都不能让 Hikvision 在五眼联盟反弹。

---

## 2. 中国 → 海外 corridor 候选清单 (matrix, 不预选)

按 6 维评估的候选 (TAM / privacy-可解 / buyer-pulled / regulator hook / 竞争密度 / 起步难度):

| Corridor | TAM | Privacy-可解 | Buyer-pulled | Regulator hook | 竞争密度 | 起步难度 | 备注 |
|---|---|---|---|---|---|---|---|
| EU × 中国跨境 B2C e-com (Shein/Temu/AliExpress/RedNote/TikTok Shop) | **大** | ✅ | ✅ 强 | GDPR + DSA + Cookie/ePrivacy | 中 (Big-4 + Europrivacy) | **中-低** | Shein €150M 罚单是现成 demo; 数万 SME 中国卖家付不起 Big-4 |
| EU × 中国 IoT/智能硬件 (Anker/Roborock/Dreame/eufy) | 中 | ✅ | ✅ 中 | RED 2025-08 + GDPR | **低** | 中 | 需审 firmware, 技术门槛较高 |
| EU × 中国 EV tier-2/3 供应商 (含 BYD 周边) | **大** | ✅ | ⚠️ 看 OEM | EU Data Act 2026-09 | 低 | **高** (B2B 销售周期 12-18 月) | 高客单价但慢 |
| 沙特/UAE × 中国 B2B (cloud/smart city/fintech) | 中 | ✅ | ✅ Vision 2030 pull | PDPL (48 起执法) | **低** | 中 | 无反华政治, 防御性 niche |
| 巴西 × 中国 B2C | 中 | ✅ | ⚠️ 早期 | LGPD 2025-08 跨境新规 | 低 | 中-高 | 时机略早, 1-2 年再看 |
| SEA × 中国 SaaS / 游戏 (miHoYo / Tencent 类) | 中 | ⚠️ 执法弱 | ❌ | 法律分散 | 低 | **太早** | 暂不建议 |

> ⚠️ **anti-pattern (不在候选内)**: 美国 × 中国任何品类。原因: 摩擦是地缘政治
> (CFIUS/NDAA/FCC), privacy cert 不解决 ownership / sovereignty 问题。

**推荐起步顺序 (供 Phase 0 验证后再定, 当前不预选)**:
1. EU × 跨境 B2C e-com (主 wedge, TAM 最大, demo 最现成)
2. EU × IoT (横向扩, 同 regulator 体系)
3. 沙特/UAE B2B (地理对冲, 防御性)

---

## 3. 9 月后扩展路线图 (3 phase)

### Phase 0 (2026-09 → 2026-12) — Demand-side validation

**这是 TRUSTe 失败模式的关键反向操作**: 先访谈 gatekeepers, 不是 vendors。

**目标**: 5-10 个欧盟企业的 procurement / CISO / DPO 访谈, 验证一个核心问题:

> **"你们买中国 vendor 的服务时, 会不会因为某种 privacy attestation 而把它从
> '排除' 移到 '可考虑'? 这个 attestation 必须满足什么条件你才会要求 / 接受?"**

如果 5 人访谈后, 答案是"good to have but not contractually required" → 直接证伪,
省 1-2 年徒劳建设, pivot。如果是"yes, if A and B and C" → 把 A/B/C 写进 Phase 1 specs。

**访谈对象类型**:
- 欧盟大型零售 / 电商平台的 vendor security 团队 (买中国 IoT 供应链)
- 欧盟跨境支付 / 物流公司的 DPO (集成中国 SaaS)
- 欧盟保险 / 金融的 procurement (评估中国云 / 数据服务)
- 欧盟 DPA (regulator 视角)

**输出**: `docs/strategy/phase0_findings.md` — 不写 SSRP 论文, 是商业 due diligence 的 working memo。

### Phase 1 (2027-01 → 2027-06) — 证据 pipeline + 试点客户

**前提**: Phase 0 通过, 即 buyer side 至少有 3 家明确说 "如果 vendor 给我们这种证据包, 会显著降低 onboarding 摩擦"。

**做什么**:
- 把 SSRP 期间的 audit codebase 包装成可销售的**证据生产 pipeline** (不是 SaaS,
  是服务交付 + 工具)。
- 输出格式严格映射 ISO 27701 controls / GDPR Art. 32 evidence / SIG Lite 问卷。
- 招募 2-3 家中国跨境 vendor 做付费试点 (5K-15K 美元区间, 远低于 Big-4 50K+)。
- 命名一个**人类 auditor 签字** — 即使是你自己, 也走法律实体 + E&O 保险架构。

**不做什么**: 不卖证书, 不卖印章, 不发 seal。卖**证据包 + 服务**。原因: cert 业务
要 EDPB endorsement, Phase 1 还没资格。

### Phase 2 (2027-07+) — 走向 cert 生态 OR 精品服务

看 Phase 1 traction 决定:

**(a) 申请 GDPR Art. 42 认证机制路径**:
- 难度高: 必须 EDPB 批准 + 国家 DPA accredit
- 需要法律实体 + E&O 保险 + 命名审计员团队
- 时间: 12-24 个月审批周期
- 回报: moat 最大, 进入 procurement 是 default

**(b) 精品 attestation 服务公司路径** (Schellman/A-LIGN 模式):
- 难度低于 (a)
- 通过 Big-4 转包 / 联合署名进入 procurement
- 边走边长, 收入更早
- 回报: 现金流好, moat 较弱

**当前判断**: 路径 (b) 更可行, (a) 更有 moat。Phase 2 建议同时探索, (b) 维生, (a) 长期投入。

---

## 4. 护城河 / 防 AI 压缩论证

四条互锁:

1. **保留人类签字 + 命名责任**: AI 做 80% 证据解析 (LLM 读 cookie banner、解析 DOM、
   匹配 GDPR 条款), 但报告**必须有命名 auditor + E&O 保险 + 责任承担**。这不是怀旧, 是结构性需求 — 保险公司、监管者、买方法务部门**只接受能告的人**。
2. **接 regulator-named hook**: 长期对接点选一: GDPR Art. 42 / EU AI Act notified bodies
   / CCPA cyber audit (2025 年 8 月新规) / NYDFS Part 500。**有 hook = 基础设施;
   无 hook = SaaS, 会被 AI 压**。
3. **卖给 buyer side, 不卖给 vendor engineer**: engineer 永远买便宜的 scanner;
   procurement / 保险 / regulator 永远要"出问题可以告的人"。客户搞错 = 直接被 AI 压。
4. **AI 是成本杠杆, 不是竞争对手**: 内部 LLM = margin lever (毛利从 30% 拉到 70%);
   外部品牌 = 命名 auditor。两者不冲突, 而是**AI 让小团队也能做精品事务所**。

---

## 5. 关键风险 + 待验证假设

**假设 (Phase 0 必须验证)**:
- A1: 欧盟 buyer 真的会**合同性要求**这种 cert (而不只是觉得"good to have")。
- A2: 中国出海 vendor 愿意**付钱** (5K-15K 美元/年) 而不是用免费 self-attestation。
- A3: 不需要 Big-4 联名也能进入 procurement (冒险, 可能到 Phase 2 才知道)。
- A4: AI-driven 持续验证比人类年度审计在 procurement 眼里**有信号增量** (而不是"看起来很 fancy 但同样的事")。

**风险**:
- R1: 中国 vendor 可能更愿意用中国官方 PIP 跨境认证 (2026-01 生效, 便宜 + 国内合规一并解决)。
  应对: 价格 / 效果对比测试, 强调海外买方读不懂中国官方报告。
- R2: 监管路径变化 (EU AI Act 修订 / GDPR 修订 / 跨境数据条约) 可能改变结构。
  应对: 接多个 regulator hook 而不是单一押注。
- R3: Big-4 自己下沉做 commodity 中国 vendor cert, 把价格打下来。
  应对: 速度 + AI 持续验证差异化 (Big-4 是年度审计, 不是持续)。
- R4: 中美关系恶化, "信任中国 vendor"整个市场结构性消失。
  应对: 这是不可控宏观风险, Phase 0 期间持续监控, 必要时把 wedge 切到沙特/UAE。

---

## 6. 如何与 SSRP 主线协同 (不混入)

**SSRP 主线**: 学术研究, AI-driven 多模态 consent audit framework, 论文产出。导师 = Dr. Singh。

**延伸方向 (本文档)**: 9 月后启动, 商业 / 服务定位, 客户 = 欧盟 buyer + 中国 vendor。

**两者关系**:
- SSRP 期间: 不动 scope, 不混入商业叙事, 不影响和 Dr. Singh 的合作。
- SSRP 输出 (论文, 数据集, codebase): **可以**在 9 月后被复用, 但不为复用而调整 SSRP scope。
- 见 `ssrp_scope_tweak_advisory.md` — 是一份完全可选的微调建议, 默认不采纳。

**心态**: SSRP 是学术 deliverable, 这个延伸方向是商业 deliverable。两者**结构上独立**,
不让任何一个被另一个绑架。

---

## 7. 接下来动作 (Alfred 主导)

- [ ] 阅读本文档 (建议 ~20 分钟)
- [ ] 阅读 `ssrp_scope_tweak_advisory.md` (建议 ~10 分钟)
- [ ] **2026-08 之前**不需要采取任何动作。本文档目的是沉淀, 不是逼迫。
- [ ] 2026-09 启动 Phase 0 时, 起一个新对话:"启动 Phase 0 demand-side validation,
      请基于 `positioning_and_future_extension.md` 第 3 节, 帮我做欧盟 procurement 访谈对象清单 + outreach 模板"。
- [ ] 期间任何时候有新洞察 / 新疑问, 在文档下方追加 changelog 即可。
