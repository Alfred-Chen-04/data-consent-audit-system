"""Week 0 access feasibility probe.

For each URL in a CSV, headlessly loads the page and records HTTP/load status,
banner selector hits, block signals, and an access-probe screenshot.

Usage:
    uv run python scripts/access_probe.py \\
        --sites data/deep_sample_candidates.csv \\
        --out data/access_probe_v0.csv \\
        --concurrency 4
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts._bootstrap import ensure_src_on_path

ensure_src_on_path()

from consent_audit.access_probe import (
    BANNER_SELECTORS,
    BLOCK_PATTERNS,
    DEFAULT_CONCURRENCY,
    DEFAULT_TIMEOUT_MS,
    AccessProbeSummary,
    ProbeResult,
    _status_block_signal,
    format_access_probe_summary,
    load_probe_sites,
    probe_one,
    run_access_probe,
    run_access_probe_from_csv,
    slugify,
)

load_sites = load_probe_sites
run = run_access_probe


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--sites", type=Path, default=Path("data/sites.csv"))
    parser.add_argument("--out", type=Path, default=Path("data/access_probe_v0.csv"))
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument("--timeout-ms", type=int, default=DEFAULT_TIMEOUT_MS)
    args = parser.parse_args()

    try:
        summary = asyncio.run(
            run_access_probe_from_csv(
                args.sites,
                args.out,
                concurrency=args.concurrency,
                timeout_ms=args.timeout_ms,
            )
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    print(format_access_probe_summary(summary), file=sys.stderr)


__all__ = [
    "BANNER_SELECTORS",
    "BLOCK_PATTERNS",
    "DEFAULT_CONCURRENCY",
    "DEFAULT_TIMEOUT_MS",
    "AccessProbeSummary",
    "ProbeResult",
    "_status_block_signal",
    "format_access_probe_summary",
    "load_probe_sites",
    "load_sites",
    "main",
    "probe_one",
    "run",
    "run_access_probe",
    "run_access_probe_from_csv",
    "slugify",
]


if __name__ == "__main__":
    main()
