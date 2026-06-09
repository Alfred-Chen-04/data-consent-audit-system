# Post-Capture Advisor Update Template, 2026-06-06

Use this after the scheduled Week 2 capture. Do not send it before replacing
the bracketed fields with actual capture results.

## Subject

SSRP Consent Interface Audit: Week 2 Capture Results and Sample Logic

## Email Draft

Dear Professor Singh,

I wanted to send the follow-up update after running the scheduled Week 2 capture
for the consent-interface audit project.

## 1. Capture Results

The Week 2 target list contained five sites:

| Site | Category | Capture status | Evidence status | Notes |
|---|---|---|---|---|
| The Guardian | news | [complete / failed / needs review] | [screenshot / DOM / hash / report status] | [notes] |
| CNN | news | [complete / failed / needs review] | [screenshot / DOM / hash / report status] | [notes] |
| Booking.com | travel | [complete / failed / needs review] | [screenshot / DOM / hash / report status] | [notes] |
| NerdWallet | finance | [complete / failed / needs review] | [screenshot / DOM / hash / report status] | [notes] |
| Coca-Cola | food | [complete / failed / needs review] | [screenshot / DOM / hash / report status] | [notes] |

The main evidence gate result is: [ready / needs triage / blocked], based on
the Week 2 sanity check.

## 2. Sample Decision Logic

Following your guidance, I am using three sample categories:

1. **Banner-present deep-sample cases**: sites where a visible consent interface
   and pathway evidence are captured.
2. **No-banner contrast cases**: repeated public desktop captures where no
   visible consent banner appears, treated as contrast observations rather than
   failed samples.
3. **Access-friction / replacement cases**: sites where the capture shows
   blocking, robot checks, network/security pages, or otherwise non-normal
   public-page access.

Current no-banner contrast candidates include BBC, New York Times, Amazon,
Airbnb, Spotify, and Chase. Reddit and Walmart currently look more like
access-friction cases than clean no-banner contrasts.

## 3. Paper Structure

The paper structure is now:

1. Introduction: consent interfaces as dynamic privacy communication.
2. Background: Notice-and-Choice, cookie-banner/interface audits, and
   longitudinal privacy measurement.
3. Methods: capture bundle, three-layer scoring, deterministic evidence checks,
   and weekly versioning.
4. Pilot evidence: Week 2 capture results and longitudinal examples.
5. Discussion: what dynamic evidence adds beyond a static snapshot.
6. Limitations: public desktop pages, unauthenticated access, location/session
   effects, and no legal-compliance determination.

## 4. Next Step

My next step is to expand from the Week 2 evidence gate toward a roughly 20-site
deep sample. In parallel, I will treat the broader 80-ish site list as a
lightweight tracker or candidate pool so the project remains scalable without
making the paper too shallow.

Best,
Qianyi
