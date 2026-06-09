"""Summaries for access-probe CSV output."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AccessProbeSummaryReport:
    csv_path: Path
    total: int
    status_counts: Counter[str]
    block_counts: Counter[str]
    cmp_counts: Counter[str]

    @property
    def access_rate(self) -> float:
        if self.total == 0:
            return 0.0
        loaded = self.status_counts["loaded_with_banner"] + self.status_counts["loaded_no_banner"]
        return loaded / self.total

    @property
    def banner_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.status_counts["loaded_with_banner"] / self.total


def classify_access_probe_row(row: dict[str, str]) -> str:
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


def summarize_access_probe_csv(csv_path: Path) -> AccessProbeSummaryReport:
    if not csv_path.exists():
        raise ValueError(f"not found: {csv_path}")

    with csv_path.open(encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    status_counts: Counter[str] = Counter(classify_access_probe_row(row) for row in rows)
    block_counts: Counter[str] = Counter(row["block_signal"] for row in rows if row.get("block_signal"))
    cmp_counts: Counter[str] = Counter(
        row["banner_selector_hit"]
        for row in rows
        if row.get("banner_detected", "").lower() == "true" and row.get("banner_selector_hit")
    )
    return AccessProbeSummaryReport(
        csv_path=csv_path,
        total=len(rows),
        status_counts=status_counts,
        block_counts=block_counts,
        cmp_counts=cmp_counts,
    )


def render_access_probe_summary(csv_path: Path) -> str:
    report = summarize_access_probe_csv(csv_path)
    lines = [
        f"Access probe summary - {report.csv_path} ({report.total} sites)",
        "",
        "Status breakdown:",
    ]
    for key in ["loaded_with_banner", "loaded_no_banner", "blocked", "http_error", "error"]:
        count = report.status_counts.get(key, 0)
        pct = f"{100 * count / report.total:.0f}%" if report.total else "-"
        lines.append(f"- {key}: {count} ({pct})")

    if report.block_counts:
        lines.extend(["", "Block signals:"])
        for signal, count in report.block_counts.most_common():
            lines.append(f"- {signal}: {count}")

    if report.cmp_counts:
        lines.extend(["", "Banner selector hits:"])
        for selector, count in report.cmp_counts.most_common():
            lines.append(f"- {selector}: {count}")

    lines.extend(
        [
            "",
            "Headline numbers:",
            f"- access_rate={report.access_rate:.0%}",
            f"- banner_rate={report.banner_rate:.0%}",
            (
                "Reminder: banner_rate depends heavily on geo; compare with an EU "
                "residential proxy before drawing conclusions."
            ),
        ]
    )
    return "\n".join(lines)
