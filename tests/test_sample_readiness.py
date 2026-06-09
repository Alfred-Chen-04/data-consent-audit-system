"""Tests for advisor-facing sample readiness exports."""

import csv
from pathlib import Path

from consent_audit.sample_readiness import build_sample_readiness, export_sample_readiness_to_csv


def test_build_sample_readiness_merges_candidates_probe_and_capture(tmp_path: Path) -> None:
    candidates = tmp_path / "candidates.csv"
    candidates.write_text(
        "url,name,category,cohort,selection_reason,status\n"
        "https://www.bbc.com,BBC,news,smoke,Known candidate,pending_review\n"
        "https://www.reuters.com,Reuters,news,smoke,Known candidate,pending_review\n"
        "https://www.wikipedia.org,Wikipedia,reference,smoke,Control candidate,pending_review\n",
        encoding="utf-8",
    )
    access_probe = tmp_path / "access_probe.csv"
    access_probe.write_text(
        "url,final_url,http_status,banner_detected,block_signal,screenshot_path,error\n"
        "https://www.bbc.com,https://www.bbc.com/,200,true,,captures/bbc.png,\n"
        "https://www.reuters.com,https://www.reuters.com/,401,false,http_401,captures/reuters.png,\n"
        "https://www.wikipedia.org,https://www.wikipedia.org/,200,false,,captures/wiki.png,\n",
        encoding="utf-8",
    )
    consent_table = tmp_path / "consent_table.csv"
    consent_table.write_text(
        "url,capture_date,banner_detected,layer1_gate_passed,tier,notes\n"
        "https://www.bbc.com/,2026-05-29,true,true,Exemplary,\n"
        "https://www.wikipedia.org/,2026-05-29,false,false,High-Risk,\n",
        encoding="utf-8",
    )

    rows = build_sample_readiness(candidates, access_probe, consent_table)

    assert [row.readiness_status for row in rows] == [
        "pilot_ready",
        "access_blocked",
        "control_candidate",
    ]
    assert rows[0].access_loaded is True
    assert rows[0].capture_observed is True
    assert rows[1].readiness_notes == "access blocked: http_401"
    assert rows[2].readiness_notes == "no banner observed; keep only as control if intentional"


def test_export_sample_readiness_to_csv(tmp_path: Path) -> None:
    candidates = tmp_path / "candidates.csv"
    candidates.write_text(
        "url,name,category,cohort,selection_reason,status\n"
        "https://www.bbc.com,BBC,news,smoke,Known candidate,pending_review\n",
        encoding="utf-8",
    )
    access_probe = tmp_path / "access_probe.csv"
    access_probe.write_text(
        "url,final_url,http_status,banner_detected,block_signal,screenshot_path,error\n"
        "https://www.bbc.com,https://www.bbc.com/,200,true,,captures/bbc.png,\n",
        encoding="utf-8",
    )
    consent_table = tmp_path / "consent_table.csv"
    consent_table.write_text(
        "url,capture_date,banner_detected,layer1_gate_passed,tier,notes\n"
        "https://www.bbc.com/,2026-05-29,true,true,Exemplary,\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "readiness.csv"

    rows = build_sample_readiness(candidates, access_probe, consent_table)
    export_sample_readiness_to_csv(out_csv, rows)

    with out_csv.open(newline="", encoding="utf-8") as fh:
        exported = list(csv.DictReader(fh))

    assert exported == [
        {
            "url": "https://www.bbc.com",
            "name": "BBC",
            "category": "news",
            "cohort": "smoke",
            "candidate_status": "pending_review",
            "selection_reason": "Known candidate",
            "access_http_status": "200",
            "access_loaded": "true",
            "access_banner_detected": "true",
            "access_block_signal": "",
            "access_screenshot_path": "captures/bbc.png",
            "capture_observed": "true",
            "capture_date": "2026-05-29",
            "consent_banner_detected": "true",
            "layer1_gate_passed": "true",
            "tier": "Exemplary",
            "readiness_status": "pilot_ready",
            "readiness_notes": "access and weekly capture available",
        }
    ]


def test_build_sample_readiness_accepts_multiple_consent_tables(tmp_path: Path) -> None:
    candidates = tmp_path / "candidates.csv"
    candidates.write_text(
        "url,name,category,cohort,selection_reason,status\n"
        "https://www.theguardian.com,The Guardian,news,smoke,Known candidate,pending_review\n"
        "https://www.cnn.com,CNN,news,pilot,Known candidate,pending_review\n",
        encoding="utf-8",
    )
    access_probe = tmp_path / "access_probe.csv"
    access_probe.write_text(
        "url,final_url,http_status,banner_detected,block_signal,screenshot_path,error\n"
        "https://www.theguardian.com,https://www.theguardian.com/international,200,true,,captures/guardian.png,\n"
        "https://www.cnn.com,https://edition.cnn.com/,200,true,,captures/cnn.png,\n",
        encoding="utf-8",
    )
    smoke_consent = tmp_path / "smoke_consent.csv"
    smoke_consent.write_text(
        "url,capture_date,banner_detected,layer1_gate_passed,tier,notes\n"
        "https://www.theguardian.com/,2026-05-29,false,false,High-Risk,\n",
        encoding="utf-8",
    )
    pilot_consent = tmp_path / "pilot_consent.csv"
    pilot_consent.write_text(
        "url,capture_date,banner_detected,layer1_gate_passed,tier,notes\n"
        "https://www.cnn.com/,2026-05-30,false,false,High-Risk,\n",
        encoding="utf-8",
    )

    rows = build_sample_readiness(candidates, access_probe, [smoke_consent, pilot_consent])

    assert [row.url for row in rows] == [
        "https://www.theguardian.com",
        "https://www.cnn.com",
    ]
    assert [row.capture_observed for row in rows] == [True, True]
    assert [row.readiness_status for row in rows] == ["pilot_ready", "pilot_ready"]
