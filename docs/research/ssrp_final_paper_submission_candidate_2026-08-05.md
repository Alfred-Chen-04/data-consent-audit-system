# How Cookie Consent Interfaces Changed

## A Traceable Longitudinal Audit With a Controlled Pilot and Six Dated Cases

Qianyi (Alfred) Chen
Mentor: Dr. Jagdip Singh
SSRP 2026 final-paper submission candidate, August 5, 2026

## Abstract

Cookie-consent interfaces are often assessed through a single banner or
screenshot. That perspective cannot establish whether refusal becomes easier,
whether a user can understand the choice, or whether the same interface changes
over time. This paper presents a traceable longitudinal audit framework with
four components: path availability, path effort, transparency, and choice
effectiveness. The framework is applied in two evidence lanes. A controlled
five-site pilot tests whether the capture, versioning, and scoring workflow can
preserve comparable observations; because it has only one validated interval,
all five local directional labels remain insufficient evidence. A separate,
purposively selected case series reconstructs six dated company trajectories
from primary regulatory decisions, regulator follow-ups, and one company
announcement. Five cases improve at least one audited component and one later
regresses. In all three first-layer cases, refusal moves from an
acceptance-favoring path to one-click or equivalently simple rejection. Orange
and SHEIN document technical remediation of refusal or withdrawal, while
Vanity Fair shows that a later functional failure can follow an earlier closed
proceeding. The findings do not estimate web-wide prevalence or establish a
single causal effect of regulation. They support a narrower conclusion:
concrete interactions that regulators can specify and verify are the clearest
site of documented improvement, while information quality and technical respect
for refusal can remain incomplete or reversible.

## 1. Introduction

Cookie banners make a consequential choice look deceptively simple. A visitor
may see an Accept button, a Reject button, a link to settings, or no refusal
route at all. The visible first layer is not the whole decision: a refusal can
require several additional actions, the consequences can be unclear, and a
site can continue reading or writing consent-dependent cookies after rejection.
An audit that treats the first screenshot as the complete object of study can
therefore miss the pathway and behavioral parts of the decision.

This problem also has a temporal dimension. A changed DOM, screenshot, or
button label is evidence that an interface changed, not evidence that user
choice improved. To support a directional claim, the two states must be dated
and comparable, the same decision components must be assessed at both points,
and the result must be distinguished from any proposed explanation for why the
change occurred. This paper develops that distinction as a practical research
method.

The work is positioned alongside, rather than as a replacement for, broad
historical measurement. Dimova et al. examined archived banners from 11,364
websites in 30 countries and found that the share offering both Accept and
Reject rose from 2.94 percent in 2018 to 30.66 percent in 2024 [1]. Their
archive-based result supplies an important population-level trend, with an
explicit lower-bound caveat. The contribution here is narrower: a traceable
component rubric applied to company-level, dated change points, with direction
and explanatory strength recorded separately.

The project asks two linked questions:

1. How can a computational audit and scoring system quantify layered consent
   interfaces in terms of unbiased choice across the full consent pathway?
2. How can firms' privacy interfaces be captured and versioned to document
   change systematically over time?

The first question supplies the ruler; the second supplies the timeline. The
paper does not report a randomized experiment, issue legal compliance verdicts,
or infer an internet-wide improvement rate from the selected cases.

## 2. Method

### 2.1 Component rubric

Each consent state is assessed with four user-facing components.

- **Path availability:** whether a user can reach acceptance, rejection, and
  customization.
- **Path effort:** the number and character of actions required for each route,
  including whether refusal has parity with acceptance.
- **Transparency:** whether purposes and consequences are presented clearly.
- **Choice effectiveness:** whether refusal or withdrawal governs the relevant
  technical behavior, including cookie reads and writes.

The rubric is deliberately not one scalar privacy score. A page can improve on
one component and remain weak on another. For example, a first-layer reject
button can remove effort asymmetry while the surrounding information remains
unclear; conversely, an apparently balanced interface cannot demonstrate that a
refusal changes backend behavior.

For a dated pair, an improvement requires at least one audited component to
improve with no assessed component regressing. A regression requires the
reverse; mixed is reserved for opposing component changes; insufficient
evidence applies when states are not comparable or the evidence cannot support
the comparison. A raw technical difference alone is not a directional result.

### 2.2 Two evidence lanes

The controlled pilot tested the capture, versioning, and comparison workflow
across five sites over one validated May 29--June 5 interval. It produced a
preserved, reviewable capture package, but one interval cannot establish a
defensible local trajectory. All five labels therefore remain
`insufficient_evidence`. This is a method result: it demonstrates why capture
context, scorer version, and evidence review must be preserved before an
interface difference becomes a substantive claim.

The retrospective case series answers a different question. A case was included
only when it named a company and consent surface, described two dated states in
one jurisdiction, supplied primary evidence for both states, supported coding
of at least one rubric component, and allowed observed direction to be
separated from the reason for change. The resulting six cases are purposively
selected source-complete trajectories, not a representative sample of firms or
websites.

### 2.3 Evidence strength

Direction and explanation are graded separately. Direction is strong when a
regulator records both states or verifies remediation. It is moderate when the
comparison uses a company announcement for one state or a broader
regulator-recorded compliance transition. Explanation is recorded as direct
company attribution, regulator-verified order response, change during an
investigation or proceeding, or unknown. This guardrail prevents timing alone
from being converted into a universal causal claim.

## 3. Results

### 3.1 Controlled pilot

The checked-in local package contains 42 audit reports and 20 longitudinal
summaries. The five matched-site reviews remain directionally insufficient.
This conservative result is substantive: the study does not recode missing
time points, same-day repeats, capture failures, or changed scorer behavior as
evidence that a consent interface became better or worse.

### 3.2 Six dated company trajectories

| Company and surface | Earlier dated state | Later dated state | Component result | Direction / explanation evidence |
|---|---|---|---|---|
| Google Search and YouTube | Acceptance took one action; rejection took at least five | Equal first-screen Reject all and Accept all actions | Availability and effort improved | Moderate split-source direction; direct company attribution [3,4] |
| Facebook | Immediate acceptance had no refusal mechanism of equivalent simplicity | Equivalent refusal was deployed and CNIL closed the injunction | Availability, effort, and verified operation improved | Strong direction; regulator-verified order response [5,6] |
| TikTok | Acceptance took one action; rejection took at least three | A first-layer Tout refuser button was added | Availability and effort improved; purpose information remained deficient | Strong direction; investigation-period change [7] |
| Orange | Cookies continued to be read after withdrawal | First-party cookies were removed and new third-party requests stopped | Withdrawal effectiveness improved | Strong direction; regulator-verified order response [8] |
| Vanity Fair France | An earlier compliance proceeding closed | Later checks found pre-choice cookies and continued behavior after rejection or withdrawal | Transparency and refusal effectiveness regressed | Moderate state-transition direction; reason unknown [9] |
| SHEIN | Cookies were observed before choice and after refusal or withdrawal | The authority recorded refusal and withdrawal remediation during proceedings | Technical refusal and withdrawal effectiveness improved | Strong direction; proceedings-period change [10] |

Across the six selected cases, five improve at least one audited component and
one regresses. The three first-layer cases all reduce acceptance-favoring
rejection effort: Google introduces equal first-screen actions, Facebook
deploys equivalent refusal, and TikTok adds a first-layer rejection button.
Those fractions summarize this case series only and are not prevalence
estimates.

The component distinction matters within the positive cases. Google provides
the clearest direct attribution: the company stated that its revised Europe
cookie choices followed updated regulatory guidance and specific CNIL direction
[4]. Facebook and Orange have a different but still strong pattern: a regulator
ordered a correction and later verified the changed mechanism [6,8]. TikTok and
SHEIN document a change during regulatory activity, but the available records
do not prove that the investigation or proceeding was the only cause [7,10].

The result is not a simple story of visual improvement. TikTok's first-layer
refusal reduced effort while the regulatory decision still found cookie-purpose
information insufficient [7]. Orange and SHEIN address the technical effect of
refusal or withdrawal, which cannot be inferred from button labels alone.
Vanity Fair supplies the counterexample: later checks found cookies before
choice and continued operations after rejection or withdrawal even though an
earlier proceeding had been closed [9]. The later regression is documented; its
cause is not.

## 4. Discussion

The repeated pattern is that concrete user interactions improve most clearly
when an authority can specify and verify them. Equal refusal, one-click
rejection, and a cessation of specified cookie operations after withdrawal are
all observable remedies. This is compatible with, but does not prove, a wider
influence of regulatory scrutiny. The evidence is strongest for Google's own
attribution and the Facebook and Orange order-and-follow-up records; it is
weaker for changes that merely occurred during a regulatory process.

The findings also explain why a single visual audit is not enough. A button
that looks balanced does not establish whether the user understood the choice
or whether the choice changed data behavior. Conversely, a later technical
failure may not be visible in the banner at all. A defensible audit should thus
keep availability, effort, transparency, and choice effectiveness visible as
separate components and should repeat the assessment rather than treating an
earlier closure or a polished banner as permanent certification.

The methodology offers a practical bridge between controlled web capture and
historical evidence. Local capture supplies reproducible context and can reveal
why a short interval is not yet adequate for a trajectory. Dated regulator and
company records can recover longer company histories where preserved local
browser states are unavailable. The two lanes should not be merged into one
sample: they have different provenance and answer different questions.

## 5. Limitations

The local pilot has only one validated interval, so it does not support a local
directional conclusion. The historical cases were selected because their public
records were source-complete; their `5/6` and `1/6` fractions cannot estimate
the prevalence of improvement across the web. The cases are concentrated in a
French regulatory setting, and their later states use mixed primary-source
forms: regulator decisions, regulator follow-ups, and one company
announcement. Finally, the study does not establish that regulation alone
caused each observed change, and it does not make a legal determination beyond
the dated observations recorded by the cited sources.

## 6. Conclusion

The project treats RQ1 as a repeatable component measure and RQ2 as the
timeline needed to interpret change. The controlled pilot validates a cautious
capture-and-comparison workflow while remaining directionally insufficient.
The six-case series shows that the same rubric can recover dated,
source-linked evolution: five cases improve at least one component and one
functionally regresses. The appropriate conclusion is not that cookie-consent
interfaces universally improved. It is that concrete, verifiable choice
mechanisms are the clearest site of documented improvement, while transparency
and technical respect for refusal remain component-specific and reversible.

## References

[1] M. Dimova, V. Toubiana, T. Van Goethem, W. Desmet, and W. Joosen, “A
history of GDPR cookie banner compliance: the roles of publishers, regulators
and CMPs,” arXiv:2606.31485, 2026. https://arxiv.org/abs/2606.31485

[2] European Data Protection Board, *Report of the Work Undertaken by the
Cookie Banner Taskforce*, Jan. 18, 2023. https://www.edpb.europa.eu/system/files/2023-01/edpb_20230118_report_cookie_banner_taskforce_en.pdf

[3] CNIL / Legifrance, *Deliberation SAN-2021-023 concerning Google*, Dec. 31,
2021. https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000044840062

[4] Google, “New cookie choices in Europe,” Apr. 21, 2022.
https://blog.google/company-news/inside-google/around-the-globe/google-europe/new-cookie-choices-in-europe/

[5] CNIL / Legifrance, *Deliberation SAN-2021-024 concerning Facebook*, Dec.
31, 2021. https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000044840532

[6] CNIL / Legifrance, *Deliberation SAN-2022-016 closing the Facebook
injunction*, Jul. 11, 2022. https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000046096716

[7] CNIL / Legifrance, *Deliberation SAN-2022-027 concerning TikTok*, Dec. 29,
2022. https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000046977994/

[8] CNIL, “Closure of the injunction issued against ORANGE,” Sep. 18, 2025.
https://www.cnil.fr/en/closure-injunction-issued-against-orange

[9] CNIL, “Cookies placed without consent: company that publishes website
vanityfair.fr fined 750,000 euros,” Nov. 27, 2025.
https://www.cnil.fr/en/cookies-placed-without-consent-company-publishes-website-vanityfairfr-fined-750000-euros

[10] CNIL, *Deliberation SAN-2025-005 concerning SHEIN*, Sep. 1, 2025.
https://www.cnil.fr/sites/default/files/2025-09/cnil_sanction_shein_en.pdf

## Submission Boundary

This candidate has a claim/source audit and a complete reference list, but it
is not evidence that a paper was submitted. Before upload, the project owner
must apply any mentor or URO-specific formatting direction and retain the
actual submission confirmation separately.
