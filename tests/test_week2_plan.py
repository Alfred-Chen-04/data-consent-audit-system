"""Tests for Week 2 capture-list preparation."""

import csv
from pathlib import Path

from consent_audit.week2_plan import export_week2_capture_targets


def test_export_week2_capture_targets_copies_expanded_targets_with_week2_notes(
    tmp_path: Path,
) -> None:
    expanded = tmp_path / "expanded_targets.csv"
    expanded.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://www.cnn.com,CNN,news,false,weekly shortlist\n"
        "https://www.coca-cola.com/us/en,Coca-Cola,food,false,verified replacement\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "week2_targets.csv"

    count = export_week2_capture_targets(expanded, out_csv)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    assert count == 2
    assert rows == [
        {
            "url": "https://www.cnn.com",
            "name": "CNN",
            "category": "news",
            "inherited_from_phd_mentor": "false",
            "notes": "week2_default_capture: weekly shortlist",
        },
        {
            "url": "https://www.coca-cola.com/us/en",
            "name": "Coca-Cola",
            "category": "food",
            "inherited_from_phd_mentor": "false",
            "notes": "week2_default_capture: verified replacement",
        },
    ]
