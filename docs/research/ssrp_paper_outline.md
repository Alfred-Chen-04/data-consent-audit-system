# SSRP 2026 Paper Outline

**Working title**: Privacy Interfaces as Corporate Communication: A Computational Auditing Framework for Tracking Consent Interface Designs

## Paper Goal

Produce an SSRP research稿 by August 2026 that explains and demonstrates a computational audit framework for layered consent interfaces. The paper should be complete enough for SSRP evaluation and advisor review, not yet optimized as a conference submission.

Current generated writing entrypoint: [ssrp_paper_skeleton_2026-06-06.md](ssrp_paper_skeleton_2026-06-06.md).
Current generated drafting notes: [ssrp_writing_pack_2026-06-06.md](ssrp_writing_pack_2026-06-06.md).
Current generated claim register: [ssrp_claim_register_2026-06-06.md](ssrp_claim_register_2026-06-06.md).
Current generated poster plan: [ssrp_poster_plan_2026-06-06.md](ssrp_poster_plan_2026-06-06.md).
Current generated RQ1/RQ2 tables: [ssrp_results_tables_2026-06-06.md](ssrp_results_tables_2026-06-06.md).
Current generated figure queue: [ssrp_figure_plan_2026-06-06.md](ssrp_figure_plan_2026-06-06.md).
Current remaining-work audit: [ssrp_remaining_work_audit_2026-05-30.md](ssrp_remaining_work_audit_2026-05-30.md).

## Core Research Questions

1. How to develop a computational audit and scoring system to quantify the layered consent interfaces in terms of unbiased choice across the full consent pathway?
2. How can we automatically capture and version firms' privacy interfaces to systematically document interface changes over time?

## Proposed Structure

1. **Introduction**
   - Consent banners as privacy communication, not only legal widgets.
   - Static audits miss change over time.
   - Contribution: traceable layered scoring plus longitudinal capture/versioning.

2. **Background and Related Work**
   - Notice-and-Choice framework.
   - Cookie-banner dark-pattern and compliance audits.
   - Longitudinal web/privacy measurement.
   - AI/VLM use as method, not as the research question.

3. **Audit Framework**
   - Layer 1: Path Availability.
   - Layer 2: Path Effort.
   - Layer 3: Transparency and Unbiased Choice.
   - Evidence discipline: every score ties to DOM, screenshot, quote, or event log evidence.

4. **Longitudinal Capture Method**
   - Weekly capture unit.
   - Consent table as the minimum stable research record.
   - Multimodal fingerprints: DOM hash, perceptual image hash, visible text.
   - Change events and weekly summaries.

5. **Pilot Study**
   - Focused deep sample of approximately 20 websites.
   - Optional broad tracking set if the pipeline stabilizes early.
   - Report path availability, effort categories, transparency/unbiased-choice grades, and week-over-week changes.

6. **Findings**
   - What interface patterns appear at baseline?
   - Which pathways are missing or hidden?
   - Which sites change over time, and how?
   - What does longitudinal evidence reveal that a single-time audit misses?

7. **Discussion**
   - Design-level risk signals, not legal determinations.
   - Practical relevance for firms, regulators, researchers, and privacy/GRC teams.
   - SOC 2/GRC mention stays small: consent evidence may matter downstream, but this is not a SOC 2 audit system.

8. **Limitations and Future Work**
   - Desktop-only.
   - English-focused.
   - Public unauthenticated pages only.
   - VLM/LLM outputs require validation and bounded schemas.
   - Continue weekly capture after August if useful.

## Figures and Tables To Build

- System architecture diagram.
- Three-layer audit rubric table.
- Consent table schema table.
- Pilot sample table.
- Example evidence card: screenshot + quote + path outcome.
- Longitudinal change timeline for 2-3 sites.
- Summary table of pathway availability and score categories.
