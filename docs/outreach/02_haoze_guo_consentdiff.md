# Email → Haoze Guo (ConsentDiff at Scale 作者)

**发送时机**: 2026-04-22 ~ 04-24(越早越好,他现在论文刚发,关注度最高)
**语言**: 英文(学术惯例)
**目的**:
  1. 确认你的 VLM + within-month volatility 差异化是否真的是 gap
  2. 打开长期交流通道(未来可能合作 / 互相 cite)
  3. 避免踩重复工作的雷区

---

## 发送前检查

- [ ] 去 arxiv 点 "view email" 链接获取他真实邮箱: https://arxiv.org/abs/2512.04316
- [ ] 再读一遍他的 abstract + extended abstract,确保邮件里引用的细节正确
- [ ] 你的自我介绍要简洁(本科 + SSRP + 项目一句话)
- [ ] **核心**:两个问题要足够具体,让他回答时**就暴露他没覆盖的部分**(= 你的差异化)

---

## Subject

```
Question about ConsentDiff at Scale — undergrad researcher working on a related angle
```

(学术圈比较吃这种 "specific paper + specific role" 的题头,比 generic "hello" 回复率高很多)

---

## 正文

```
Hi Haoze,

I read your ConsentDiff at Scale paper (arXiv 2512.04316) last week
and wanted to reach out — I'm an undergrad at Dartmouth starting an
SSRP project this summer that sits in the same neighborhood, and your
work changed how I'm thinking about the rubric. Really nice paper,
especially the weighted claim-UI alignment score.

I'm writing to ask two specific questions, mostly to make sure I'm
not duplicating things you've already thought through:

1. Your snapshot cadence is monthly. In your data, did you see any
   evidence of sub-monthly churn — i.e., sites that flip UI elements
   (reject button visibility, default toggle states) on a faster
   timescale than your sampling resolution? I'm considering a higher
   frequency for a smaller site set and wondering if it would find
   new phenomena or just add noise.

2. How do you handle within-session variability — e.g., the same site
   serving different consent UIs to different sessions (either via
   A/B tests or personalization)? Your pipeline seems designed around
   one canonical UI per site per month; curious whether you saw this
   as a real issue or dismissed it early.

The angle I'm exploring is: primary analysis through VLM + LLM
(rather than DOM + weak-supervision vision), with a focus on
*volatility* as a separate dimension from point-in-time compliance.
Half of that angle's value depends on whether (1) and (2) above are
real gaps — so any quick read from you would genuinely shape the
project's direction.

No rush, and please feel free to reply with just a sentence or two
if that's easier than a full response. Happy to send the project
one-pager if helpful.

Thanks,
Alfred Chen
Dartmouth College '27
```

---

## 为什么这两个问题是对的

**Q1(sub-monthly churn)**:如果他回"没看到,噪声居多"→ 你做 weekly 就有理论依据证明存在 monthly 遗漏的信号。如果他回"我们没测"→ 你直接捡到 gap。
**Q2(within-session variability / A/B)**:这是他**明确没做**的。让他 confirm 一下,你就有了"引用他论文的 limitation 来论证你的 contribution"的弹药。

**两个问题的共同特点**: 都是你愿意听到的答案都能推进你的项目。无论他怎么回你都赢。

---

## 不要做的事

- ❌ 问 "can we collaborate" —— 太早,互相不了解
- ❌ 长篇介绍你的方法 —— 他没义务读
- ❌ 暗示他的工作不够 —— 友好的 peer 姿态,不是竞争对手
- ❌ 一次问 3 个以上问题 —— 回复率暴跌

---

## 如果他回了(想好怎么接)

- 如果他**短回**(1-2 句)→ 感谢 + 给他项目 one-pager + 留下"半年后出 preliminary results 时再联系你"的钩子
- 如果他**长回**或**反过来问你**→ 说明他有兴趣,可以提议一个 async 邮件往返或 Zoom
- 如果他**建议合作**→ 先缓,和 Dr. Singh / Qiyao 商量过再回

---

## 如果 5 天没回

再等 5 天,然后发一封一行的 polite bump:
```
Hi Haoze — just bumping this in case it got buried. No worries if
you're swamped, even a one-line thought would be valuable.
```
超过 15 天没回 = 放弃,走别的路径。
