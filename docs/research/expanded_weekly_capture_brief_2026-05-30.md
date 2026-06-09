# Expanded Weekly Capture Brief, 2026-05-30

This brief records the first weekly capture run using the expanded target list
that adds the verified Coca-Cola replacement to the existing four-site
shortlist.

Supporting artifacts:

- `data/deep_sample_weekly_targets_expanded_2026-05-30.csv`
- `data/consent_table_pilot_2026-05-30.csv`
- `data/audit_report_summary.csv`
- `data/longitudinal_summary.csv`
- `data/research_package/`

## Capture Summary

- Expanded target list: 5 active sites.
- Categories: news=2, travel=1, finance=1, food=1.
- New consent-table rows appended: 5.
- New `AuditReport` rows saved: 5.
- New `WeeklySummary` rows saved or backfilled: 5.

The current paper-facing export counts are:

- `AuditReport` rows: 37
- Longitudinal summary rows: 15

## Site Outcomes

| Site | Cohort | Latest outcome | Longitudinal note |
|---|---|---|---|
| The Guardian | `expanded-weekly-2026-05-30` | Banner detected; Accept and Customize visible; Reject not detected; final tier High-Risk. | D severity pathway/layout/copy/DOM change. |
| CNN | `expanded-weekly-2026-05-30` | No actionable consent paths detected in latest capture; final tier High-Risk. | C severity layout/copy/DOM change. |
| Booking.com | `expanded-weekly-2026-05-30` | No actionable consent paths detected in latest capture; final tier High-Risk. | C severity layout/DOM change. |
| NerdWallet | `expanded-weekly-2026-05-30` | No actionable consent paths detected in latest capture; final tier High-Risk. | B severity copy-only change. |
| Coca-Cola | `expanded-weekly-2026-05-30` | Banner detected; Accept, Reject, and Customize visible; final tier Compliant. | A severity no-change observation. |

## Pipeline Note

This run exposed a paper-facing longitudinal gap: stable repeated captures were
being stored as `AuditReport` rows but not exported as longitudinal observations
because the weekly pipeline only saved summaries when change events existed.
The pipeline now saves a `WeeklySummary` whenever two reports exist for the
same URL. When no events are detected, the summary is severity A with
`event_count=0`.

Coca-Cola's latest two reports were backfilled into one no-change longitudinal
summary so the replacement candidate now has both cross-sectional and
longitudinal evidence in the research package.
