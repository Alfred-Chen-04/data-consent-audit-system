"""Week 2 sample/capture-list preparation helpers."""

from __future__ import annotations

import csv
from pathlib import Path

WEEK2_TARGET_FIELDNAMES = [
    "url",
    "name",
    "category",
    "inherited_from_phd_mentor",
    "notes",
]


def export_week2_capture_targets(
    expanded_targets_csv: Path,
    out_csv: Path,
) -> int:
    """Freeze the expanded capture shortlist as the Week 2 default target list."""
    rows: list[dict[str, str]] = []
    with expanded_targets_csv.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            url = (row.get("url") or "").strip()
            if not url:
                continue
            notes = (row.get("notes") or "").strip()
            rows.append(
                {
                    "url": url,
                    "name": (row.get("name") or "").strip(),
                    "category": (row.get("category") or "").strip(),
                    "inherited_from_phd_mentor": (
                        row.get("inherited_from_phd_mentor") or "false"
                    ).strip(),
                    "notes": f"week2_default_capture: {notes}".strip(),
                }
            )

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=WEEK2_TARGET_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
