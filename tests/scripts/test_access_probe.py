"""Tests for access-probe result classification."""

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import access_probe
from scripts.access_probe import _status_block_signal


def test_status_block_signal_marks_http_error_statuses() -> None:
    assert _status_block_signal(401) == "http_401"
    assert _status_block_signal(403) == "http_403"
    assert _status_block_signal(500) == "http_500"
    assert _status_block_signal(200) == ""
    assert _status_block_signal(None) == ""


def test_access_probe_rejects_invalid_site_list_before_browser_run(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    seen: list[list[str]] = []

    async def fake_run(
        sites: list[str],
        out_csv: Path,
        concurrency: int,
        timeout_ms: int,
    ) -> None:
        _ = (out_csv, concurrency, timeout_ms)
        seen.append(sites)

    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://example.com,Example,placeholder,false,delete before real run\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(access_probe, "run", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "access_probe.py",
            "--sites",
            str(sites_csv),
            "--out",
            str(tmp_path / "probe.csv"),
        ],
    )

    with pytest.raises(SystemExit) as excinfo:
        access_probe.main()

    assert excinfo.value.code == 2
    assert seen == []
    assert "site list validation failed before access probe: placeholder_url" in capsys.readouterr().err


def test_access_probe_script_delegates_to_shared_csv_runner(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    seen: dict[str, object] = {}

    async def fake_run_access_probe_from_csv(
        sites_csv: Path,
        out_csv: Path,
        *,
        concurrency: int,
        timeout_ms: int,
    ) -> SimpleNamespace:
        seen["sites_csv"] = sites_csv
        seen["out_csv"] = out_csv
        seen["concurrency"] = concurrency
        seen["timeout_ms"] = timeout_ms
        return SimpleNamespace(
            total=1,
            loaded=1,
            banner_detected=0,
            blocked_or_error=0,
            out_csv=out_csv,
            screenshot_dir=tmp_path / "captures" / "access_probe",
        )

    async def fail_old_list_runner(*args: object, **kwargs: object) -> None:
        _ = (args, kwargs)
        raise AssertionError("script should use run_access_probe_from_csv")

    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://valid.example,Valid,news,false,\n",
        encoding="utf-8",
    )
    out_csv = tmp_path / "probe.csv"
    monkeypatch.setattr(
        access_probe,
        "run_access_probe_from_csv",
        fake_run_access_probe_from_csv,
        raising=False,
    )
    monkeypatch.setattr(access_probe, "run", fail_old_list_runner)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "access_probe.py",
            "--sites",
            str(sites_csv),
            "--out",
            str(out_csv),
            "--concurrency",
            "2",
            "--timeout-ms",
            "1234",
        ],
    )

    access_probe.main()

    assert seen == {
        "sites_csv": sites_csv,
        "out_csv": out_csv,
        "concurrency": 2,
        "timeout_ms": 1234,
    }
    assert "total=1" in capsys.readouterr().err
