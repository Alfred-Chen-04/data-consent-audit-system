"""Summarize access-probe CSV output for a mentor-facing memo.

Usage:
    uv run python scripts/access_probe_summarize.py data/access_probe_v0.csv
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts._bootstrap import ensure_src_on_path

ensure_src_on_path()

from consent_audit.access_probe_summary import (
    classify_access_probe_row,
    render_access_probe_summary,
    summarize_access_probe_csv,
)

classify = classify_access_probe_row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, nargs="?", default=Path("data/access_probe_v0.csv"))
    args = parser.parse_args()

    try:
        summary = render_access_probe_summary(args.csv_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    print(summary)


__all__ = [
    "classify",
    "classify_access_probe_row",
    "main",
    "render_access_probe_summary",
    "summarize_access_probe_csv",
]


if __name__ == "__main__":
    main()
