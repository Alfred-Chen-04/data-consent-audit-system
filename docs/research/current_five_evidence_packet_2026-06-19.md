# Current-Five Evidence Packet, 2026-06-19

## Purpose

This packet consolidates the five current Week 2 evidence bundles into one
advisor/user review file. It uses existing screenshot, DOM, research-package,
longitudinal-summary, and manual-review evidence only. It does not add a new
browser capture and does not change final SSRP scoring.

## Evidence Checked

| Evidence | File |
|---|---|
| Manual evidence worksheet | `data/week2_manual_evidence_review_2026-06-10.csv` |
| Audit report summary | `data/research_package/audit_report_summary.csv` |
| Longitudinal summary | `data/research_package/longitudinal_summary.csv` |
| Existing banner evidence cards | `docs/research/week2_evidence_cards_2026-06-11.md` |
| Visual screenshot re-check | Five screenshot files listed in the cards below |

## Current-Five Summary

| Site | Evidence class | Human coding | Latest automated tier | Longitudinal severity | Use now |
|---|---|---|---|---|---|
| The Guardian | Banner present | `banner_present_manual_review` | High-Risk | D | Strong evidence card; advisor confirmation still needed before final scoring. |
| Coca-Cola | Banner present | `banner_present_manual_review` | High-Risk | D | Strong evidence card; post-fix smoke separately shows OneTrust recognition can pass. |
| CNN | No visible banner | `no_visible_banner_contrast` | High-Risk | C | Contrast candidate, not a banner-path failure. |
| Booking.com | No visible banner | `no_visible_banner_contrast` | High-Risk | C | Contrast candidate, not a banner-path failure. |
| NerdWallet | No visible banner | `no_visible_banner_contrast` | High-Risk | C | Contrast candidate, not a banner-path failure. |

## Evidence Card: The Guardian

| Field | Current Evidence |
|---|---|
| URL | `https://www.theguardian.com/` |
| Category | News |
| Screenshot | `data/captures/sites/www_theguardian_com_20260605_160209/layer1.png` |
| DOM snapshot | `data/captures/sites/www_theguardian_com_20260605_160209/layer1.html` |
| DOM hash | `60b9add43b807053adcc722ceec43f334cfd81e33f4c6befbef3f17600e91624` |
| Image hash | `ffffff0000000030:0f41adfb6920585c` |
| Automated path fields | accept=false, reject=false, customize=false, dismiss=false |
| Manual screenshot coding | `banner_present_manual_review` |
| Longitudinal result | Severity D; 4 events: copy change, DOM restructure, layout change, pathway change |

Visual re-check on 2026-06-19: the screenshot shows a visible Guardian choice
interface with "Yes, I accept", "No, thank you", and "Manage cookies".

Current interpretation: keep as a banner-present evidence card, but do not use
the automated path booleans alone as final scoring.

## Evidence Card: Coca-Cola

| Field | Current Evidence |
|---|---|
| URL | `https://www.coca-cola.com/us/en` |
| Category | Food |
| Screenshot | `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.png` |
| DOM snapshot | `data/captures/sites/www_coca_cola_com_20260605_160238/layer1.html` |
| DOM hash | `bb63e6524504c6a0c7326091fa3a9b3fccb26e005a10eb53ff0474d9b24f0f23` |
| Image hash | `3c3c3c3c3c3c3c3c:8e7ec4ffaca9b2d2` |
| Automated path fields | accept=true, reject=false, customize=false, dismiss=false |
| Manual screenshot coding | `banner_present_manual_review` |
| Longitudinal result | Severity D; 5 events: copy change, DOM restructure, layout change, pathway change, score change |

Visual re-check on 2026-06-19: the screenshot shows a visible Privacy
Preference Center with "Allow All", "Confirm My Choices", "Reject All", and
category toggles.

Current interpretation: keep as a banner-present evidence card. Do not describe
the Week 2 automated row as final scoring without manual validation; the June
15 post-fix smoke separately shows the OneTrust pathway-recognition bug was
fixed for the Coca-Cola smoke case.

## Contrast Card: CNN

| Field | Current Evidence |
|---|---|
| URL | `https://www.cnn.com/` |
| Category | News |
| Screenshot | `data/captures/sites/www_cnn_com_20260605_160221/layer1.png` |
| DOM snapshot | `data/captures/sites/www_cnn_com_20260605_160221/layer1.html` |
| DOM hash | `3adfda3091d23765c6263140c8b46eef2b907b95578b39042886f3661635944b` |
| Image hash | `000000ff3cffffff:4f74651f62930cbe` |
| Automated path fields | accept=false, reject=false, customize=false, dismiss=false |
| Manual screenshot coding | `no_visible_banner_contrast` |
| Longitudinal result | Severity C; 3 events: copy change, DOM restructure, layout change |

Visual re-check on 2026-06-19: the screenshot shows the CNN homepage with no
visible first-screen cookie or consent banner.

Current interpretation: keep as a no-visible-banner contrast candidate. Do not
count it as a banner-path failure unless the advisor confirms that table rule.

## Contrast Card: Booking.com

| Field | Current Evidence |
|---|---|
| URL | `https://www.booking.com/` |
| Category | Travel |
| Screenshot | `data/captures/sites/www_booking_com_20260605_160226/layer1.png` |
| DOM snapshot | `data/captures/sites/www_booking_com_20260605_160226/layer1.html` |
| DOM hash | `1b527847e49cda4bcda330f27f168431cc1860d833919d869f36f6f06fd8369a` |
| Image hash | `0000003cffffffff:711dada1fa77e3a7` |
| Automated path fields | accept=false, reject=false, customize=false, dismiss=false |
| Manual screenshot coding | `no_visible_banner_contrast` |
| Longitudinal result | Severity C; 3 events: copy change, DOM restructure, layout change |

Visual re-check on 2026-06-19: the screenshot shows the Booking.com search
homepage with no visible first-screen cookie or consent banner.

Current interpretation: keep as a no-visible-banner contrast candidate. Do not
count it as a banner-path failure unless the advisor confirms that table rule.

## Contrast Card: NerdWallet

| Field | Current Evidence |
|---|---|
| URL | `https://www.nerdwallet.com/` |
| Category | Finance |
| Screenshot | `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.png` |
| DOM snapshot | `data/captures/sites/www_nerdwallet_com_20260605_160232/layer1.html` |
| DOM hash | `a66bf169c10d8f61913cba5eff10147e8d9853fee94f0e0f81dac6e4f59d711d` |
| Image hash | `ff00000000ffffff:7e6528c60cb65b42` |
| Automated path fields | accept=false, reject=false, customize=false, dismiss=false |
| Manual screenshot coding | `no_visible_banner_contrast` |
| Longitudinal result | Severity C; 3 events: copy change, DOM restructure, layout change |

Visual re-check on 2026-06-19: the screenshot shows the NerdWallet homepage and
product cards with no visible first-screen cookie or consent banner.

Current interpretation: keep as a no-visible-banner contrast candidate. Do not
count it as a banner-path failure unless the advisor confirms that table rule.

## What This Packet Proves

- The current five have traceable screenshot, DOM, hash, audit-summary, and
  longitudinal-summary evidence.
- The Guardian and Coca-Cola are the two strongest current banner/control
  evidence cases.
- CNN, Booking.com, and NerdWallet are better represented as no-visible-banner
  contrast candidates under the current evidence rule.

## What This Packet Does Not Prove

- It does not prove Week 3 continuity evidence exists.
- It does not resolve the 8 pending CMP/manual-review rows.
- It does not decide whether no-visible-banner rows belong in the main RQ1
  table or a separate contrast/limitations table.
- It does not expand the deep sample beyond the current five.

## Recommended Use

Use this packet for the next advisor/user discussion. The concrete decision is:

Should the next research step be a post-fix current-five continuity rerun, or
should these evidence cards become the manual-validation base before expanding
toward the roughly 20-site deep sample?
