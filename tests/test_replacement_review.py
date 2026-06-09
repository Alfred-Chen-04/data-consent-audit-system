"""Tests for reviewing replacement candidates before sample-lock promotion."""

import csv
from pathlib import Path

from consent_audit.replacement_review import (
    build_replacement_review,
    export_expanded_weekly_targets,
    export_replacement_review_to_csv,
    summarize_replacement_review,
)


def test_build_replacement_review_promotes_only_full_layer1_reproductions(
    tmp_path: Path,
) -> None:
    candidates = tmp_path / "replacement_candidates.csv"
    candidates.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://www.coca-cola.com/us/en,Coca-Cola,food,false,batch2\n"
        "https://www.ikea.com/us/en/,IKEA,ecommerce,false,batch2\n"
        "https://www.pepsi.com,Pepsi,food,false,batch2\n"
        "https://www.salesforce.com,Salesforce,software,false,batch2\n",
        encoding="utf-8",
    )
    access_probe = tmp_path / "access_probe.csv"
    access_probe.write_text(
        "url,final_url,http_status,banner_detected,banner_selector_hit,"
        "block_signal,screenshot_path,error,notes\n"
        "https://www.coca-cola.com/us/en,https://www.coca-cola.com/us/en,"
        "200,true,#onetrust-consent-sdk,,captures/coke.png,,\n"
        "https://www.ikea.com/us/en/,https://www.ikea.com/us/en/,200,true,"
        "#onetrust-banner-sdk,,captures/ikea.png,,\n"
        "https://www.pepsi.com,https://www.pepsi.com/,200,false,,,"
        "captures/pepsi.png,,\n"
        "https://www.salesforce.com,https://www.salesforce.com/,403,false,,"
        "access_denied,captures/salesforce.png,,\n",
        encoding="utf-8",
    )
    consent_table = tmp_path / "consent_table.csv"
    consent_table.write_text(
        "url,capture_date,banner_detected,accept_available,reject_available,"
        "customize_available,layer1_gate_passed,tier,notes\n"
        "https://www.coca-cola.com/us/en,2026-05-30,true,true,true,true,true,"
        "Compliant,\n"
        "https://www.ikea.com/us/en/,2026-05-30,false,false,false,false,false,"
        "High-Risk,\n",
        encoding="utf-8",
    )

    rows = build_replacement_review(candidates, access_probe, consent_table)

    assert [row.replacement_status for row in rows] == [
        "verified_replacement",
        "promising_reprobe",
        "no_banner_or_locale_shift",
        "blocked_or_error",
    ]
    assert rows[0].recommended_action == (
        "add to expanded weekly capture shortlist pending advisor confirmation"
    )
    assert rows[0].priority == 1
    assert rows[1].recommended_action == (
        "reprobe with fresh context before any sample-lock promotion"
    )
    assert rows[2].recommended_action == (
        "do not use as banner-present replacement unless kept as contrast case"
    )
    assert rows[3].evidence_notes == "access blocked: access_denied"


def test_export_replacement_review_to_csv_and_summary(tmp_path: Path) -> None:
    candidates = tmp_path / "replacement_candidates.csv"
    candidates.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://www.coca-cola.com/us/en,Coca-Cola,food,false,batch2\n",
        encoding="utf-8",
    )
    access_probe = tmp_path / "access_probe.csv"
    access_probe.write_text(
        "url,final_url,http_status,banner_detected,banner_selector_hit,"
        "block_signal,screenshot_path,error,notes\n"
        "https://www.coca-cola.com/us/en,https://www.coca-cola.com/us/en,"
        "200,true,#onetrust-consent-sdk,,captures/coke.png,,\n",
        encoding="utf-8",
    )
    consent_table = tmp_path / "consent_table.csv"
    consent_table.write_text(
        "url,capture_date,banner_detected,accept_available,reject_available,"
        "customize_available,layer1_gate_passed,tier,notes\n"
        "https://www.coca-cola.com/us/en,2026-05-30,true,true,true,true,true,"
        "Compliant,\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "replacement_review.csv"

    rows = build_replacement_review(candidates, access_probe, consent_table)
    export_replacement_review_to_csv(out_csv, rows)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    assert summarize_replacement_review(rows) == {"verified_replacement": 1}
    assert exported[0]["url"] == "https://www.coca-cola.com/us/en"
    assert exported[0]["replacement_status"] == "verified_replacement"
    assert exported[0]["access_loaded"] == "true"
    assert exported[0]["layer1_gate_passed"] == "true"
    assert exported[0]["priority"] == "1"


def test_export_expanded_weekly_targets_adds_verified_replacements_only(
    tmp_path: Path,
) -> None:
    base_targets = tmp_path / "base_targets.csv"
    base_targets.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://www.cnn.com,CNN,news,false,weekly shortlist\n",
        encoding="utf-8",
    )
    replacement_review = tmp_path / "replacement_review.csv"
    replacement_review.write_text(
        "url,name,category,access_loaded,access_banner_detected,"
        "access_block_signal,access_screenshot_path,capture_observed,"
        "capture_date,consent_banner_detected,layer1_gate_passed,"
        "accept_available,reject_available,customize_available,tier,"
        "replacement_status,priority,recommended_action,evidence_notes\n"
        "https://www.coca-cola.com/us/en,Coca-Cola,food,true,true,,"
        "captures/coke.png,true,2026-05-30,true,true,true,true,true,"
        "Compliant,verified_replacement,1,add to shortlist,ready\n"
        "https://www.ikea.com/us/en/,IKEA,ecommerce,true,true,,"
        "captures/ikea.png,true,2026-05-30,false,false,false,false,false,"
        "High-Risk,promising_reprobe,2,reprobe,unstable\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "expanded_targets.csv"

    count = export_expanded_weekly_targets(base_targets, replacement_review, out_csv)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    assert count == 2
    assert [row["url"] for row in exported] == [
        "https://www.cnn.com",
        "https://www.coca-cola.com/us/en",
    ]
    assert exported[1]["notes"] == "verified_replacement: add to shortlist"
