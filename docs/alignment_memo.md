# SSRP 2026 Alignment Emails

Two drafts below — one for Dr. Singh (faculty mentor, big-picture direction), one for Qiyao (PhD mentor, comparison + 80-site collaboration). Both assume my current thinking is an AI-layer extension of the already-approved proposal, not a new project.

Availability for a 30-min Zoom: **any time after 3 pm on May 5**. The next two weeks are packed, so the meeting should be scheduled for on or after May 5.

---

## Email 1 — to Dr. Singh

**Subject**: SSRP 2026 direction check-in — AI extension on top of the approved proposal

Dear Dr. Singh,

I hope the semester is winding down well. I wanted to share a short update on how I am shaping the SSRP 2026 project before the summer starts, and get your read on the overall direction.

The core of the proposal you approved stays the same: the Notice-and-Choice framework, the three-layer audit (Path Availability → Path Effort → Transparency & Unbiased Choice), and the longitudinal database. What I would like to add on top is an AI layer for each of those three components:

- **Layer 1** — a browser agent (Playwright + VLM) that actually traverses the consent path, instead of a static DOM scan.
- **Layer 2** — a vision-language model that analyzes the banner screenshot and returns structured visual features (button-size ratio, color contrast, layout symmetry, etc.), with every output linked back to a bounding box on the screenshot.
- **Layer 3** — an LLM for Disclosure Topic Coverage and Framing Analysis, with every score tied to a verbatim quote from the banner text.

The reasoning behind the pivot is twofold. First, my career goal is to become an AI PM with a data-privacy background, so I would like the summer to showcase the ability to package AI into an explainable, evidence-traceable product (a public demo + a public dataset), not just a larger sample. Second, the academic space is still open: PRISMe (2025) works on policy text with an LLM, and UMBRA / "Abyss" (2026) audits banners with rule-based heuristics, but neither is *multimodal + agent-driven + longitudinal*, and UMBRA has not released its tool or data.

The 10-week summer target (late May to early August) would be: a paper draft (methodology + 80-site case study), the SSRP poster, a public demo website, and an open-source repo + dataset. I have gated the plan so that if the AI components underperform at week 3 or week 5, the scope contracts down to a smaller sample while keeping the methodology intact.

A few questions I would love your take on whenever you have a moment:

1. Does treating AI as both the engine and the product interaction feel like the right framing for SSRP, or would you push it back toward a pure research output?
2. Are there risks you have seen on similar projects — especially around VLMs misreading small UI elements or browser agents getting blocked — that I should plan around now?
3. Is the scope above too ambitious, and if so, what would you cut first?

There is no rush on my end — I would rather you send thoughts whenever they come to mind, and I will keep iterating on the framework in the meantime. If a live conversation would help, I am free **any time after 3 pm on May 5** for a 30-minute Zoom. The next two weeks are crowded for me, so anything on or after May 5 works best.

Thank you again for supporting this direction.

Best,
Qianyi (Alfred) Chen

---

## Email 2 — to Qiyao (PhD mentor)

**Subject**: SSRP 2026 — would love to build on your 80-site audit

Hi Qiyao,

I wanted to give you a short heads-up on the shape my SSRP 2026 project is taking, because the most important collaboration point with you sits in it, and I would rather flag it early than late.

The project is still the three-layer consent-interface audit from the proposal Dr. Singh approved. The change is that I am adding an AI layer to each of the three components: a browser agent that actually traverses the consent path, a vision-language model that scores the banner screenshot, and an LLM that scores the text (Disclosure Topic Coverage + Framing). Every score is required to link back to a DOM element, a bounding box, or a verbatim quote, so the report is evidence-traceable rather than a black-box number.

Where your work becomes central: I would like to reuse the **80-site list you already audited statically**, rerun it with this dynamic AI pipeline, and write a **static-vs-dynamic comparison** as one of the main case studies of the summer paper. I think this is a strong framing for both of us — your static audit becomes the baseline that makes my dynamic results interpretable, and the comparison itself is a novel contribution neither piece carries alone.

Two things I wanted to check with you before I commit to that framing:

1. Are you comfortable with me reusing your 80-site list, and with me publishing a direct comparison against your static results in the paper? If yes, I would cite your work as the baseline and co-author / acknowledge as you prefer.
2. How do you feel about the site list itself being released publicly alongside the paper and the dataset? If you would rather it stay private, I can keep the comparison in the paper but not release the names.

I also wanted to flag a couple of risks I expect to hit, in case you have already run into them on your own audits: (a) VLMs tend to misread very small or cramped banners, and (b) some sites block automated traversal. Any lessons from your experience would save me a lot of week-2 pain.

None of this is urgent. Please send thoughts whenever they come to you — I will be iterating on the framework over the next couple of weeks. When you are ready for a live conversation, I am free **any time after 3 pm on May 5** for a 30-minute Zoom, and we can go through the pipeline and the comparison design in detail then. The next two weeks are packed on my side, so May 5 onward is the realistic window.

Thanks so much, and looking forward to working on this with you this summer.

Best,
Qianyi (Alfred) Chen
