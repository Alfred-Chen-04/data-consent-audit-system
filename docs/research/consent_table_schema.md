# Consent Table Schema

The consent table is the minimum weekly research record. It lets the paper continue even if full LLM/VLM scoring needs more time.

## Required Columns

| Column | Type | Meaning |
|---|---|---|
| `url` | string | Final audited URL. |
| `capture_date` | date | Local date of capture. |
| `captured_at` | datetime | ISO timestamp. |
| `cohort` | string | `smoke`, `pilot`, `deep_sample`, or `broad_tracker`. |
| `banner_detected` | bool | Whether a first-layer consent interface was captured. |
| `accept_available` | bool | Layer-1 Accept path availability. |
| `reject_available` | bool | Layer-1 Reject path availability, applying the 2-action gate. |
| `customize_available` | bool | Layer-1 Customize path availability, applying the 2-action gate. |
| `dismiss_available` | bool | Dismiss/close path availability. |
| `layer1_gate_passed` | bool | True only if Reject and Customize are available. |
| `first_screenshot_ref` | string | Screenshot path or object-store key for the first-layer banner. |
| `first_dom_snapshot_ref` | string | DOM snapshot path or object-store key. |
| `dom_hash` | string | DOM fingerprint for longitudinal diffing. |
| `image_hash` | string | Perceptual screenshot fingerprint. |
| `layer2_mean_effort` | float? | Optional Layer-2 mean effort. |
| `layer2_overall_category` | string? | Optional `Easy`, `Average`, or `Poor`. |
| `transparency_grade` | string? | Optional Layer-3 Transparency grade. |
| `unbiased_choice_grade` | string? | Optional Layer-3 Unbiased Choice grade. |
| `tier` | string? | Optional categorical summary tier. |
| `notes` | string | Human notes, blocker reason, or semi-automated audit caveat. |

## Invariants

- A row without screenshot/DOM evidence is incomplete unless `notes` explains a capture failure.
- `layer1_gate_passed` must be false if Reject or Customize is false.
- Optional Layer 2/3 fields stay blank until the relevant scoring module has run.
- Do not write legal conclusions such as "GDPR violation" in this table.
