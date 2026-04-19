# Test fixtures

This directory holds frozen CaptureBundles + expected Layer results used by unit tests.

## Structure

```
fixtures/
├── bundles/               — JSON-serialized CaptureBundle objects
│   ├── clean_banner.json      — reference "compliant" site
│   ├── missing_reject.json    — Layer-1 gate should fail
│   ├── tiny_reject.json       — Layer-2 should flag size asymmetry
│   └── framing_heavy.json     — Layer-3 should catch strong bias
├── screenshots/           — matching PNGs referenced by the bundles
└── expected/              — golden Layer1/2/3 results per fixture
```

## Why frozen fixtures

Layer scoring must be **deterministic given a bundle** (AGENTS.md §4). If a change to
scoring logic flips a fixture's expected output, the diff is explicit and reviewable.

## Adding a new fixture

1. Capture a real site with `scripts/run_audit.py --no-save`.
2. Inspect the CaptureBundle JSON, sanitize any PII, commit under `bundles/`.
3. Hand-author the expected Layer1/2/3 results under `expected/`.
4. Add a test in `tests/layers/` that asserts `score_layerN(bundle) == expected`.
