# SSRP 2026 Alignment Email

Single email to both Dr. Singh and Qiyao. Availability for a 30-min Zoom: any time after 3 pm on May 5 — the next two weeks are packed.

---

**To**: Dr. Singh, Qiyao
**Subject**: SSRP 2026 direction check-in — AI extension on the approved proposal

Dear Dr. Singh and Qiyao,

I wanted to share a short update on how I am shaping the SSRP 2026 project before the summer starts, and get both of your reads on the direction while there is still plenty of time to adjust.

The core of the proposal Dr. Singh approved stays the same: the Notice-and-Choice framework, the three-layer audit (Path Availability → Path Effort → Transparency & Unbiased Choice), and the longitudinal database. What I would like to add on top is an AI layer for each of those three components:

- **Layer 1** — a browser agent (Playwright + VLM) that actually traverses the consent path, instead of a static DOM scan.
- **Layer 2** — a vision-language model that analyzes the banner screenshot and returns structured visual features (button-size ratio, color contrast, layout symmetry, etc.), with every output linked to a bounding box on the screenshot.
- **Layer 3** — an LLM for Disclosure Topic Coverage and Framing Analysis, with every score tied to a verbatim quote from the banner text.

The reasoning behind the pivot is twofold. First, my career goal is to become an AI PM with a data-privacy background, so I would like the summer to showcase the ability to package AI into an explainable, evidence-traceable product (a public demo + a public dataset), not just a larger sample. Second, the academic space is still open: PRISMe (2025) works on policy text with an LLM, and UMBRA / "Abyss" (2026) audits banners with rule-based heuristics, but neither is *multimodal + agent-driven + longitudinal*, and UMBRA has not released its tool or data.

The single most important collaboration piece sits with Qiyao. I would like to reuse the **80-site list you already audited statically**, rerun it with this dynamic AI pipeline, and write a **static-vs-dynamic comparison** as one of the main case studies of the summer paper. I think this is a strong framing — your static audit becomes the baseline that makes my dynamic results interpretable, and the comparison itself is a novel contribution neither piece carries alone. Two things I want to check with you before I commit to that framing: (1) are you comfortable with me reusing the list and publishing a direct comparison against your static results, and (2) how do you feel about the site list itself being released publicly alongside the paper and dataset? If you would rather it stay private, I can keep the comparison in the paper but not release the names.

The 10-week summer target (late May to early August) would be: a paper draft (methodology + 80-site case study), the SSRP poster, a public demo website, and an open-source repo + dataset. I have gated the plan so that if the AI components underperform at week 3 or week 5, the scope contracts down to a smaller sample while keeping the methodology intact.

A few open questions I would love either of your takes on:

1. Does treating AI as both the engine and the product interaction feel like the right framing for SSRP, or would you push it back toward a pure research output?
2. Are there risks you have seen on similar projects — especially around VLMs misreading small UI elements or browser agents getting blocked — that I should plan around now?
3. Is the scope above too ambitious, and if so, what would you cut first?

There is no rush on my end — please send thoughts whenever they come to mind, and I will keep iterating on the framework over the next couple of weeks. When you are ready for a live conversation, I am free **any time after 3 pm on May 5** for a 30-minute Zoom, and we can go through the pipeline and the comparison design in detail then. The next two weeks are packed on my side, so May 5 onward is the realistic window.

Thank you both for supporting this direction.

Best,
Qianyi (Alfred) Chen
