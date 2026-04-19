"""Summarize access_probe CSV output for a mentor-facing memo.

Prints:
  - Overall totals (loaded / banner / blocked / error)
  - Breakdown by block_signal
  - Breakdown by banner CMP vendor (selector hit)
  - Per-site rows highlighted by status

Usage:
    uv run python scripts/access_probe_summarize.py data/access_probe_v0.csv
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from rich.console import Console
from rich.markup import escape
from rich.table import Table


def classify(row: dict[str, str]) -> str:
    if row.get("error"):
        return "error"
    if row.get("block_signal"):
        return "blocked"
    status = row.get("http_status", "")
    if not status or (status.isdigit() and int(status) >= 400):
        return "http_error"
    if row.get("banner_detected", "").lower() == "true":
        return "loaded_with_banner"
    return "loaded_no_banner"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv_path", type=Path, nargs="?", default=Path("data/access_probe_v0.csv"))
    args = ap.parse_args()

    if not args.csv_path.exists():
        raise SystemExit(f"not found: {args.csv_path}")

    with args.csv_path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    console = Console()
    console.print(f"\n[bold]Access probe summary[/bold] — {args.csv_path} ({len(rows)} sites)\n")

    status_counts: Counter[str] = Counter(classify(r) for r in rows)
    block_counts = Counter(r["block_signal"] for r in rows if r.get("block_signal"))
    cmp_counts = Counter(r["banner_selector_hit"] for r in rows if r.get("banner_detected", "").lower() == "true")

    totals = Table(title="Status breakdown", show_header=True)
    totals.add_column("Category")
    totals.add_column("Count", justify="right")
    totals.add_column("%", justify="right")
    for key in ["loaded_with_banner", "loaded_no_banner", "blocked", "http_error", "error"]:
        n = status_counts.get(key, 0)
        pct = f"{100 * n / len(rows):.0f}%" if rows else "-"
        totals.add_row(key, str(n), pct)
    console.print(totals)

    if block_counts:
        bt = Table(title="Block signals", show_header=True)
        bt.add_column("Signal")
        bt.add_column("Count", justify="right")
        for sig, n in block_counts.most_common():
            bt.add_row(sig, str(n))
        console.print(bt)

    if cmp_counts:
        ct = Table(title="Banner selector hits (proxy for CMP vendor)", show_header=True)
        ct.add_column("Selector")
        ct.add_column("Count", justify="right")
        for sel, n in cmp_counts.most_common():
            ct.add_row(escape(sel), str(n))
        console.print(ct)

    access_rate = (status_counts["loaded_with_banner"] + status_counts["loaded_no_banner"]) / len(rows) if rows else 0
    banner_rate = status_counts["loaded_with_banner"] / len(rows) if rows else 0
    console.print(
        f"\n[bold]Headline numbers[/bold]  "
        f"access_rate={access_rate:.0%}  banner_rate={banner_rate:.0%}"
    )
    console.print(
        "[dim]Reminder: banner_rate depends heavily on geo. Low rate from a US IP is expected; "
        "compare with an EU residential proxy before drawing conclusions.[/dim]\n"
    )


if __name__ == "__main__":
    main()
