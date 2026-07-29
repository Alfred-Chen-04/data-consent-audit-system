# Retrospective Longitudinal Evidence Rescue, 2026-07-29

## Decision

The project now uses two evidence lanes that answer different questions:

1. The **controlled local pilot** tests whether the capture, versioning, and
   scoring workflow can preserve comparable observations. Its five sites still
   have only one validated interval, so their directional labels remain
   `insufficient_evidence`.
2. The **retrospective regulatory case series** tests whether the same RQ1
   component rubric can recover documented change over longer periods. It adds
   five companies with dated before and after evidence from primary regulatory
   decisions, regulatory follow-ups, and one company announcement.

The second lane supplies a defensible longitudinal finding without pretending
that missing local captures exist. It is an observational case series, not a
random sample or a causal experiment.

## Inclusion Rule

A retrospective case is included only when all of the following are present:

- a named company and web surface;
- at least two dated states in the same jurisdiction;
- a primary source describing the user path or cookie behavior before change;
- a primary source describing or verifying the later state;
- enough detail to score at least one RQ1 component;
- an explicit separation between observed direction and inferred cause.

The source registry is
`data/retrospective_source_registry_2026-07-29.csv`. The scored case table is
`data/retrospective_longitudinal_cases_2026-07-29.csv`.

## Five Dated Trajectories

| Company and surface | Earlier state | Later state | Component result | Direction |
|---|---|---|---|---|
| Google Search and YouTube | On June 1, 2021, accept required one action and reject required at least five | In April 2022, equal first-screen `Reject all` and `Accept all` buttons each required one click | Reject availability and effort improved | Improved |
| Facebook | On April 8, 2021, immediate acceptance had no refusal mechanism of equivalent simplicity | Changes deployed from late February 2022 offered equivalent refusal; an April 12 CNIL check supported closure of the order | Reject availability, effort, and verified operation improved | Improved |
| TikTok | On June 3, 2021, accept required one action and reject required at least three | On February 28, 2022, TikTok added a first-layer `Tout refuser` button | Availability and effort improved; purpose information remained deficient | Improved, incomplete |
| Orange | In November 2024, cookies continued to be read on `orange.fr` after withdrawal | By September 2025, first-party cookies were removed and new third-party requests stopped after withdrawal | Withdrawal effectiveness improved | Improved |
| Vanity Fair France | A prior compliance proceeding closed in July 2022 | Checks from July 2023 through February 2025 found pre-consent cookies and continued operations after `Reject all` or withdrawal | Transparency and refusal effectiveness regressed | Regressed |

These are component labels, not legal verdicts issued by this project. The
underlying regulatory sources make their own legal findings; this project
reuses only the dated observations to apply one longitudinal measurement rule.

## Computed Result

For the five purposively selected, source-complete trajectories:

- `4/5` improved in at least one audited component with no observed component
  regression across the selected interval.
- `1/5` regressed in functional respect for refusal after an earlier compliance
  proceeding had closed.
- `3/3` first-layer button cases moved from acceptance-favoring effort
  asymmetry to a one-click or equivalently simple reject path.
- `2/5` later states were independently accepted through formal regulatory
  follow-up decisions: Facebook and Orange.
- `1/5` has direct company attribution: Google stated that the redesign
  followed updated regulatory guidance and specific CNIL direction.
- TikTok changed during the regulatory investigation, but the public record
  does not establish that one event alone caused the change.
- The source does not establish why Vanity Fair's later functional regression
  occurred.

These fractions describe this case series only. They are not prevalence
estimates for companies or websites generally.

## External Benchmark

The new 2026 preprint *A history of GDPR cookie banner compliance: the roles of
publishers, regulators and CMPs* independently evaluates 11,364 websites across
30 countries using Wayback Machine and HTTP Archive material. It reports that
websites offering both accept and reject increased from `2.94%` in September
2018 to `30.66%` in September 2024 and finds a strong correlation between
higher compliance and stronger data-protection-authority activity.

That study supplies a population-level historical trend. This project's five
cases add auditable, company-level mechanisms and show why a positive aggregate
trend should not be read as monotonic or complete progress.

Primary research source:

- https://arxiv.org/abs/2606.31485

## What Explains Change

The evidence supports a graded answer rather than one universal cause:

| Causal claim | Cases | Strength |
|---|---|---|
| Specific regulatory direction prompted redesign | Google | Direct company statement |
| A formal order was followed by a changed and regulator-verified mechanism | Facebook, Orange | Strong event-linked evidence |
| Change occurred during an active regulatory investigation | TikTok | Moderate temporal and procedural evidence |
| The system later failed after an earlier proceeding had closed | Vanity Fair | Strong direction evidence; cause unknown |

The common mechanism is regulatory pressure focused on observable user-choice
friction. The strongest repeated change is not more policy text; it is moving a
reject action onto the first layer or making withdrawal technically effective.

## Discussion-Worthy Finding

The project can now support this conclusion:

> Consent interfaces tend to improve first where regulators can specify and
> verify a concrete interaction, such as one-click rejection or effective
> withdrawal. But improvement is component-specific and reversible: a visible
> reject button can coexist with unclear purpose information or a backend that
> continues tracking, and a previously closed compliance case can later fail.

This creates three substantive discussion questions:

1. Does enforcement produce genuine user autonomy, or mainly visible interface
   parity that is easy to demonstrate to a regulator?
2. Who should be responsible when a banner looks balanced but the underlying
   cookie behavior ignores refusal: the publisher, the CMP, or both?
3. Should compliance be certified once, or continuously re-audited because
   consent systems can regress after a prior closure?

## Important Nuance

Google's later account-creation case illustrates the component distinction. A
CNIL decision reports that Google added an equally easy reject button in
October 2023, while the authority still found that users were not adequately
informed about the consequences of the choice. A path can improve without the
whole consent process becoming informed or unbiased.

Source:

- https://www.cnil.fr/fr/publicites-inserees-entre-les-courriels-et-cookies-la-cnil-sanctionne-google-dune-amende-de-325

## Claim Boundaries

- Do not merge the five retrospective cases into the five local pilot sites.
  They have different sampling and capture provenance.
- Do not call `4/5` an internet-wide improvement rate.
- Do not state that a fine alone caused every change.
- Do not treat a visible `Reject all` label as proof that refusal is honored.
- Do not describe the retrospective case series as randomized or experimental.
- Do describe it as evidence that the RQ1/RQ2 framework can recover real,
  directional, historically documented evolution.

## Primary Sources

- Google before: https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000044840062
- Google after and direct attribution: https://blog.google/company-news/inside-google/around-the-globe/google-europe/new-cookie-choices-in-europe/
- Facebook before: https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000044840532
- Facebook after: https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000046096716
- TikTok before and after: https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000046977994/
- Orange before and after: https://www.cnil.fr/en/closure-injunction-issued-against-orange
- Vanity Fair before and after: https://www.cnil.fr/en/cookies-placed-without-consent-company-publishes-website-vanityfairfr-fined-750000-euros
- EDPB cookie-banner task force: https://www.edpb.europa.eu/system/files/2023-01/edpb_20230118_report_cookie_banner_taskforce_en.pdf
- CNIL longitudinal action-plan evaluation: https://www.cnil.fr/en/evolution-practices-web-regarding-cookies-cnil-evaluates-impact-its-action-plan-0
