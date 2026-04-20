# Consent 审计评分体系 — 市场与文献扫描

*版本: 2026-04-19  |  作者: Alfred (with Claude)*
*目的: 在定义我们自己的 rubric 之前,摸清学术界、监管方、商业界已经在用什么,找到空白定位。*

---

## TL;DR — 一句话结论

**现有评分体系几乎全是静态、单时刻、预定义规则式的**;唯一直接竞争的纵向工作 ConsentDiff at Scale (arxiv 2512.04316) 用的是 DOM + weak-supervision vision,**没有用 VLM/LLM,也没有把 volatility 当作一流指标**。这就是我们的空白:**"三层 VLM-grounded 审计 × 时间轨迹 × 波动率"作为合规健康的新范式**。

---

## 1. 学术 rubric(按时间顺序)

### 1.1 Nouwens et al., CHI 2020 — *Dark Patterns after the GDPR*
- **打分对象**: UK top-10,000 网站里用五大 CMP 的 680 个站点
- **指标**:
  - opt-out 按钮是否出现在首页
  - 是否提供 granular controls
  - 是否预勾选(pre-ticked)
  - 是否需要"implied consent"(滚动即同意等)
- **核心发现**: 只有 **11.8%** 的站点满足欧盟法律的最低要求
- **方法**: 静态 DOM 爬取 + 40 人用户实验
- **局限**: 一次性快照;仅覆盖主流 CMP;没有量化"路径长度"
- 引用: [arxiv 2001.02479](https://arxiv.org/abs/2001.02479)

### 1.2 Matte et al., IEEE S&P 2020 — *Do Cookie Banners Respect My Choice?*
- **打分对象**: 22,949 欧洲网站,深度测试 560 个 IAB TCF 合规的 CMP
- **指标**(都是 boolean violation):
  - 未选择即记录 positive consent
  - 通过预选项 nudge 用户
  - 用户明确 opt-out 后仍存储 positive consent
- **核心发现**: **54%** 的站点至少有一项违规
- **方法**: 抓取 + 解析 IAB TCF 的 consent string(`euconsent-v2`)直接验证是否真尊重用户选择
- **局限**: 仅限 TCF 框架内站点;不看视觉层;无时间维度
- 引用: [arxiv 1911.09964](https://arxiv.org/abs/1911.09964)
- **对我们的启发**: 用 consent string 解码做 ground-truth 验证是极强的技术路径 —— 我们 Layer 1 (Path Availability) 可以在 TCF 站点上做类似的交叉验证

### 1.3 Utz et al., CCS 2019 — *(Un)informed Consent*
- **打分对象**: 一个德国网站,3 次大规模 A/B 实验,**80,000+ 用户**
- **指标**: 通知位置、选项类型、措辞影响
- **核心发现**:
  - 左下角显示交互率最高
  - binary choice → 接受率远高于分类选择
  - Nudging 效应巨大
- **方法**: 活体 A/B 实验(不是审计工具)
- **关键意义**: **证明小的设计改动会显著改变 consent 决策** —— 这是"动态审计有价值"的底层论据
- 引用: [arxiv 1909.02638](https://arxiv.org/abs/1909.02638)

### 1.4 Bielova et al., USENIX Security 2024 — *The Effect of Design Patterns*
- 延续 Matte/Utz 传统,深入分析 design pattern 对 present/future consent 的影响
- 静态分析为主
- 引用: [usenix.org](https://www.usenix.org/system/files/usenixsecurity24-bielova.pdf)

### 1.5 PRISMe, 2025 — *LLM-Powered Privacy Policy Assessment*
- **范围**: **privacy policy 文本**(不是 consent banner UI)
- **方法**: LLM 读政策文本,以交通灯系统呈现评分
- **与我们的差异**: 它审计的是**文字政策**,我们审计的是**交互 UI + 政策整体**。PRISMe 是我们 Layer 3 (Transparency) 的参考,不是竞争
- 引用: [arxiv 2501.16033](https://arxiv.org/html/2501.16033v1)

### 1.6 Qu et al., MADWeb 2025 — *A Longitudinal Study of Cookie Banner Practices*
- **方法**: 用 **Wayback Machine** 回溯 2010 以来的快照
- **发现**: 2023 年后 "Only Opt-In" 类 dark pattern 显著下降,**对应 CNIL 对 Google 的 1.5 亿欧元罚款**(因果关联)
- **与我们差异**: 回溯法 → 覆盖长,但 Wayback 只抓 HTML 不跑 JS,**CMP 延迟注入的 banner 会漏掉**;我们做 live 持续抓取可以补上这部分
- 引用: [madweb25-qu.pdf](https://madweb.work/papers/2025/madweb25-qu.pdf)

### 1.7 ⭐ **ConsentDiff at Scale** (arxiv 2512.04316) — 最接近的竞品
**这是你必须仔细读的一篇**,它几乎就是你想做的事情,但方法不同。

- **打分对象**: 2,400 域名 × 9 个月 = **21,600 个 site-month 快照**
- **地理分布**: EU 900 / US-CA 1000 / Other 500
- **Rubric** — **Claim-UI Alignment Score A ∈ [0,1]**:
  | 预测变量 | 权重 |
  |---|---|
  | Visible "Reject all" button | 0.40 |
  | Default-off toggles | 0.30 |
  | Steps-to-reject ≤ 2 | 0.20 |
  | Reopen/withdrawal affordance | 0.10 |
- **UI 五类**: Scroll-Wall / Accordion / Multi-Step / Pre-ticked / Reject-Hidden
- **方法**: DOM 分析 + **弱监督视觉分类器**(不是 VLM/LLM)
- **主要发现**:
  - Scroll-Wall 逐步转 Accordion
  - EU 区 Pre-ticked 在执法后显著减少
  - "Reject all" 可见性 **+9.3 pp**(执法前后)
  - EU 对齐分数比 US-CA 中位数高 0.09
- **承认的局限**:
  - 19-48% 的站点(取决于区域)banner 根本没弹出来 — 抓取基础设施不够强
  - DOM+vision 分类器在边缘 case 会误标
  - **"只反映我们自己 session 看到的行为" — 无法捕捉服务端变化** ← 这句话直接给你留了个 A/B testing 的口子
- **它不做的**: VLM semantic parsing、文字 framing 分析(Layer 3)、trajectory / volatility 作为 rubric

**对我们的意义**:
- ✅ 这篇的存在**验证了方向是对的** —— 顶会水平的团队也在做纵向 consent 审计
- ⚠️ 这是我们的**第一个引用 + 第一个差异化对象** —— 论文 Related Work 必须正面处理它
- 🎯 **我们的空白**: (i) 真 VLM/LLM 驱动(它是 DOM+弱监督);(ii) 三层而不是四指标;(iii) volatility/trajectory 作为一级指标而非分析输出;(iv) 文字 framing (Layer 3);(v) 他们承认的"无法捕捉服务端变化"=我们的 A/B testing 观察维度

---

## 2. 监管 / 官方 rubric

这些不是工具,是**法律基准线** —— 你的 rubric 要站得住,就要 map 到它们。

### 2.1 GDPR Art. 7(3) + ePrivacy Directive
- 同意必须: **"freely given, specific, informed, unambiguous"**
- 撤回同意必须和给予同样容易
- 任何 rubric 都要能 operationalize 这四个形容词 —— 这是论文写作时反复引用的源点

### 2.2 EDPB Guidelines 03/2022 (final 2023-02) — *Deceptive Design Patterns*
- 官方列出的 dark pattern 分类:
  - **Overloading** (信息过载)
  - **Skipping** (关键步骤被跳过)
  - **Stirring** (情绪操纵)
  - **Obstructing** (制造摩擦)
  - **Fickle** (不一致的设计)
  - **Left in the Dark** (隐藏关键信息)
- **2023 年 EDPB + EEA 成员国成立 "Cookie Banner Taskforce"**,公开调查结果
- 引用: [EDPB Guidelines 03/2022](https://www.edpb.europa.eu/system/files/2023-02/edpb_03-2022_guidelines_on_deceptive_design_patterns_in_social_media_platform_interfaces_v2_en_0.pdf)
- **对我们**: 我们的 Layer 2 (Path Effort) 和 Layer 3 (Transparency) 可以直接按这 6 类打标签,天然可引用

### 2.3 CNIL 2021 Guidelines (FR 主管机构)
- **硬指标**:
  - "Accept All" 在场 → "Reject All" 必须**同等大小、同一层级**
  - 拒绝操作步数 ≤ 接受操作步数
- **执法案例**: Google 1.5 亿欧元,Meta 6000 万欧元(拒绝按钮不对等)
- **对我们**: Reject-depth 指标直接对应 CNIL 的"同等简单"要求 — 强可引用

### 2.4 IAB TCF v2.2 (2023-2024) / v2.3
- 2024-06 起移除了 Purpose 3-6 的 "legitimate interest" 作为合法基础
- 新增 Special Purpose 3 "Save and communicate privacy choices"
- 技术层: vendors 必须用 event listener 接收 consent 变化
- **对我们**: TCF consent string 是强 ground truth 源(参考 Matte 2020) — 对用 TCF 的站点我们能精确验证
- 引用: [iabeurope.eu](https://iabeurope.eu/all-you-need-to-know-about-the-transition-to-tcf-v2-3/)

---

## 3. 商业工具(简要,你可能不需要深读)

| 工具 | 功能 | 我们的差异 |
|---|---|---|
| **OneTrust** | 卖 CMP 本身 + 客户自查 audit(私有数据) | 他们审计自己客户;我们审计"公开 web 的合规现状" |
| **Osano** | cookie scanner,列出站点发出的 cookies 和来源 | 他们看 cookie 流,我们看 UI 是否允许用户拒绝 |
| **Termly / Cookiebot / Secure Privacy** | 站长合规自查工具 | 面向 B2B 客户,不公开评分方法 |
| **Auditzo / Verified CONSENT** | 第三方 SaaS 审计 | 黑盒打分,不学术 |

**核心观察**: 商业工具都是**"面向合规方的自检"**(帮客户不被罚款),**不是面向社会的透明度研究**。它们的评分方法不公开,数据不共享,无学术价值。**我们的定位不是和它们竞争,而是做它们做不到的公共研究**。

---

## 4. ⭐ Consent Banner A/B Testing — 文献与证据

你当时问"真的会有这种情况吗?合法吗?"— 答案:

### 4.1 商业 A/B testing 是**公开、常见、合法**的
- **OneTrust 官方博客**直接卖 "A/B testing your cookies to improve ROI"
- **Usercentrics**、**Cookie-script** 都提供 banner A/B testing 工具
- **合法性**: 只要**所有变体本身合规**,测试行为本身不违法(GDPR 没禁止 consent UI 的 A/B 测试)
- 一个 2022 年的大规模 RCT (Behavioural Insights Team 的 Predictiv 平台): 37% 用户永远 accept,26% 永远 reject,**只有约 1/3 的用户选择受设计影响** —— 但这 1/3 就是 A/B 优化的金矿

### 4.2 但学术界尚未系统研究"野外 A/B 测试"
- Utz 2019 是在自己的网站跑 A/B(主动实验,n=80,000)
- **没有论文系统记录:哪些真实商业站点正在对其 consent UI 做 A/B 测试,各变体的合规差异有多大**
- ConsentDiff 明确承认它**"无法捕捉服务端变化"** —— 就是这个空白

### 4.3 我们做这件事的价值 & 成本
- **价值**: 如果发现大站点的某个 A/B 变体隐藏了 reject 按钮 → 是新的监管案例素材
- **技术代价**: 要从多个 session / IP / cookie state 抓同一个站点 → 等于工程量翻倍
- **建议**: **不做主线,做 opportunistic 分析** —— 我们本来就会重复抓同一站点(每周),如果发现**同一 IP 同一周内**看到的 banner 不同 = 疑似 A/B,自然触发。无额外基础设施成本。

---

## 5. 空白图 — 我们落在哪

### 5.1 二维定位图

```
                    静态快照                      纵向/动态
                  ┌──────────────────────┬──────────────────────┐
    单指标        │ Matte 2020 (TCF)     │ MADWeb 2025          │
    / 规则式      │ CNIL checklists      │ (Wayback, HTML-only) │
                  │ IAB TCF compliance   │                      │
                  ├──────────────────────┼──────────────────────┤
    多指标        │ Nouwens 2020         │ ConsentDiff at Scale │
    / 评分式      │ Bielova 2024         │ (DOM + weak-sup vis) │
                  │ EDPB 6-pattern       │                      │
                  ├──────────────────────┼──────────────────────┤
    VLM/LLM       │ PRISMe 2025          │ ╔══════════════════╗ │
    多维 + 语义   │ (policy text only)   │ ║  🎯 我们的位置   ║ │
                  │                      │ ║  三层 × 时间     ║ │
                  │                      │ ║  volatility      ║ │
                  │                      │ ╚══════════════════╝ │
                  └──────────────────────┴──────────────────────┘
```

### 5.2 我们的差异化(5 条,按重要性排序)

1. **Volatility / Trajectory 作为一级指标**,不是分析输出 — 现有所有工具都给"当前分数",我们给"当前分 × 稳定性 × 方向"
2. **三层框架的 Layer 3 (Transparency / 文字 framing)** — 现有 UI 工具几乎不做,PRISMe 做但只看政策文本,不看 banner 里的措辞
3. **VLM-grounded** — 处理非 CMP 自研弹窗、视觉暗模式(按钮对比度、字号差异)、跨语言站点,这些 DOM / weak-supervision 方法会漏掉
4. **更长的时间窗** — ConsentDiff 是 9 个月,我们起点是 Qiyao 2025-09 (T=0),终点延续到 2027 春,**总窗口 > 18 个月**
5. **Opportunistic A/B testing 观察** — ConsentDiff 明确承认的空白

### 5.3 我们需要诚实承认的不足(写论文时别遮掩)

- **站点数** 起步可能比 ConsentDiff (2400) 少一个数量级 — 但我们的深度(三层 + 每周)更高
- **抓取成功率** 大概率也会有 19-48% 失败 — 这是共性问题
- **VLM 成本** > DOM 分析,所以规模扩展有瓶颈

---

## 6. 对你原 rubric 的具体建议

基于这份扫描,建议把原三层框架改成:

```
Layer 1: Path Availability
  State:       has_reject / has_accept_all / has_customize  (boolean; 对标 Matte 2020)
  Trajectory:  新增 / 删除 / 不变  over time
  Volatility:  每月 boolean flip 次数

Layer 2: Path Effort
  State:       reject_depth (点击数), reject_time (秒), visual prominence ratio
               (对标 CNIL "同等简单" + ConsentDiff "steps ≤ 2")
  Trajectory:  depth delta
  Volatility:  depth variance over time

Layer 3: Transparency & Framing
  State:       VLM/LLM 对 banner 文字的 framing 评分(中性 / 引导 / 欺骗)
               — 这是我们独有的维度,可引用 EDPB 6-pattern 打标签
  Trajectory:  framing shift
  Volatility:  wording 变更频率
```

**三个 meta-score 作为输出**:
- **Compliance Score**(State 维度的传统分)— 用来和 ConsentDiff / Nouwens 做对比
- **Compliance Trajectory**(改善 / 稳定 / 退化)— 原创
- **Compliance Volatility**(低/中/高)— 原创

Volatility 的价值陈述(写 abstract 时能用):**"A site with stable C-grade compliance may carry less regulatory risk than a site oscillating between A and D."**

---

## 7. 立即 actionable 的下一步

1. **把 ConsentDiff at Scale 原文通读一遍** — 它是论文第一引用,必须吃透
2. **把 Matte 2020 的 consent string 验证法加进我们的 Layer 1 ground truth 工具链** — 对 TCF 站点可以做精确验证
3. **在 sites.csv 里标注每个站是否用 TCF** — 决定能不能对它做 consent string 验证
4. **rubric 的最终定义进入 spec 文档** — 见 §6 提议,需要你确认后写成正式 spec
5. **(可选)给 Dr. Singh 发 1 页 memo**: "我们扫了现有 rubric,发现 ConsentDiff 是直接竞品,定位已调整为 X Y Z" — 展示 field awareness

---

## 引用清单

### 学术
- Nouwens et al. 2020 — [arxiv 2001.02479](https://arxiv.org/abs/2001.02479)
- Matte et al. 2020 — [arxiv 1911.09964](https://arxiv.org/abs/1911.09964)
- Utz et al. 2019 — [arxiv 1909.02638](https://arxiv.org/abs/1909.02638)
- Bielova et al. 2024 — [USENIX](https://www.usenix.org/system/files/usenixsecurity24-bielova.pdf)
- PRISMe 2025 — [arxiv 2501.16033](https://arxiv.org/html/2501.16033v1)
- MADWeb 2025 (Qu et al.) — [madweb.work](https://madweb.work/papers/2025/madweb25-qu.pdf)
- **ConsentDiff at Scale — [arxiv 2512.04316](https://arxiv.org/html/2512.04316)** ⭐

### 监管
- [EDPB Guidelines 03/2022 Deceptive Design Patterns](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-032022-deceptive-design-patterns-social-media_en)
- [CNIL: Refusing cookies should be easy as accepting them](https://www.cnil.fr/en/refusing-cookies-should-be-easy-accepting-them-cnil-continues-its-action-and-issues-new-orders)
- [IAB Europe TCF v2.2 / v2.3](https://iabeurope.eu/transparency-consent-framework/)

### 商业(背景)
- [OneTrust on TCF 2.2](https://www.onetrust.com/blog/iab-tcf-2-2-what-you-need-to-know/)
- [Osano cookie audit](https://www.osano.com/articles/how-cookies-work)
- [OneTrust on A/B testing cookies](https://www.onetrust.com/blog/a-b-testing-essential-to-improve-roi/)
