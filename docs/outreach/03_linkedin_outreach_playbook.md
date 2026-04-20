# LinkedIn 外联 Playbook

**发送时机**: 滚动进行,不急。建议 04-28 起每天 1-2 条 connect 请求
**目的**: 绕过机构 `info@` 黑洞,找到**具名**、**可回复**的业内人员

---

## LinkedIn 冷 DM 的四条铁律

1. **先 connect,再 DM** —— 不 connect 直接 DM 对方看不到(除非 InMail 付费)
2. **Connection request 带 note**(300 字符以内)—— 无 note 的 request 接受率 <10%,带 note 且说清楚 why 能到 40-60%
3. **一次只问一个问题** —— 不问"能不能聊 30 分钟",问"X 这事你怎么看" 这种 5 分钟能回的
4. **profile 先布置好** —— 对方会点你头像看你是不是销售/机器人。确保你 LinkedIn 有 Dartmouth、SSRP、项目一句话介绍

---

## 你的 LinkedIn profile 准备清单(先改 profile 再发 DM)

- [ ] **Headline**: "Undergrad @ Dartmouth | SSRP 2026 Researcher — AI x Privacy Auditing"(不是"student")
- [ ] **About**(前 3 行,在"see more"折叠之上): "Working on longitudinal consent auditing using VLMs for SSRP 2026. Previously [something]. Reach out if you work on privacy / regtech / dark patterns."
- [ ] **Featured**: 放一个你 SSRP 项目的 one-pager 链接(Google Doc / Notion)
- [ ] **Experience**: SSRP 2026 应作为 experience entry 独立列出(不只是 education 底下带一句)

---

## Tier 1 候选人(高精确匹配)

### A. Arne Bauer — Tech Trainee @ noyb
- **为什么**:年龄最近,角色对等(trainee ↔ undergrad),noyb 内部做技术/证据工作最可能的人
- **怎么找**: LinkedIn 搜 "Arne Bauer noyb" 或 "Arne Bauer data protection Vienna"
- **Connect note 模板**:

```
Hi Arne — I'm an undergrad researcher at Dartmouth starting a summer
project on longitudinal consent UI auditing (VLM-based, ~monthly
snapshots). Curious whether historical UI data ever comes up in noyb's
enforcement work — would love to connect and trade notes if you're open.
```

- **Accept 后首条 DM**(连在后面,2-3 天后发):

```
Thanks for connecting! Quick specific question if you have a minute:

When noyb builds a case against a site's consent UI, do you ever wish
you had evidence of how that UI looked 3 / 6 / 12 months ago — e.g.,
screenshots with timestamps showing the reject button was there and
then disappeared? I'm trying to figure out if that kind of historical
record would actually be useful in enforcement or if it's mostly an
academic curiosity.

Even a one-line "yes useful because X" / "not really because Y" would
be super helpful for a decision I'm making this week. No pressure.
```

### B. Felix Mikolasch — Data Protection Lawyer @ noyb
- **为什么**:打 consent 官司的前线律师,判断"证据价值"的权威
- **只有在 Arne 没回或答案不确定时再联系**(不要同一机构一次 spam 多个人)
- Connect note 改成更正式口吻:"researcher working on consent audit methodology — would value your view on evidentiary standards for UI-based deceptive patterns"

### C. Cooper Quintin — Senior Public Interest Technologist, EFF Threat Lab
- **为什么**:EFF 技术侧代表,Privacy Badger 相关
- **Accept 率**: 中等(很忙,但对学生友好)
- Connect note:
```
Hi Cooper — big fan of EFF's work on tracking. I'm an undergrad at
Dartmouth starting a project on longitudinal consent UI auditing
(VLM-based, complementary to what Privacy Badger does for trackers).
Would love to connect — no ask, just think you might appreciate the
direction.
```
(第一轮不要问问题,只 connect。等他接受后看他 feed 再找话题。)

### D. Lena (Privacy Badger @ EFF)
- LinkedIn 上需要先找到她全名(EFF staff 页可查)
- 精确匹配度最高,但也最技术,问题要更具体

---

## Tier 2: Regtech / Industry 视角(LinkedIn 搜索字符串)

### 搜索套路

LinkedIn 搜索框输入以下关键词组合,按"People"筛选,加"Current company"过滤:

| 关键词 | 目标公司 filter | 目标 |
|---|---|---|
| `"privacy engineer" consent CMP` | OneTrust, Cookiebot, Didomi, Usercentrics, TrustArc | 构建 CMP 的工程师,懂内部 |
| `"product manager" privacy consent` | OneTrust, Osano, Securiti | PM 视角,知道客户需求 |
| `"DPO" OR "data protection officer"` | 任意 EU 大公司 | 买 CMP 的甲方,知道痛点 |
| `"privacy researcher" consent dark patterns` | Mozilla, DuckDuckGo, Brave | 隐私技术研究 |

### 通用 connect note(Tier 2)

```
Hi [Name] — undergrad at Dartmouth doing summer research on
longitudinal consent UI auditing. Trying to understand how people
who work on the "real" side of consent (not just academia) think
about what makes a CMP better or worse. Would love to connect.
```

### 通用 follow-up DM(accept 后)

```
Thanks for connecting! One specific question if you have 2 minutes:

If someone handed you a free tool that produced a monthly "consent
UI health report" for any website — reject button visibility,
toggle defaults, path length, change history over time — would
that be useful to you? If yes, what would you want in the report
that you're not getting from current tools? If no, what would
*actually* be useful?
```

---

## Tier 3: 学术圈 LinkedIn(低优先级,邮件更好)

学术人在 LinkedIn 上一般不活跃。如果对方没有 personal website 或 arxiv 邮箱不好拿,LinkedIn 才用。**Haoze Guo 优先走邮件(见 02 文件)**,除非邮件拿不到。

---

## 节奏建议

- **每天最多 3 个新 connect request** —— 超过可能触发 LinkedIn 反 spam
- **等 3-5 天再发 accept 后的首条 DM** —— 立刻 DM 像是机器人
- **每周汇总一次反馈** —— 谁接受了 / 谁回了 / 回了什么,记在简单 CSV 里
- **不要群发相同 DM** —— LinkedIn 能检测,且有人会截图发出来

---

## 衡量成功的指标(2 周后复盘)

- Connect 接受率 >30%(低于说明 profile 或 note 有问题)
- DM 回复率 >20%(低于说明 ask 太大或太模糊)
- 至少 1 个回复里提到具体的用例 / 痛点,能让你改 rubric —— 这才是真有用的信号
