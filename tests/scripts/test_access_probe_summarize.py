"""Tests for access-probe summary script wrapper behavior."""

import sys
from pathlib import Path

import pytest

from scripts import access_probe_summarize


def test_access_probe_summary_script_delegates_to_shared_renderer(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    seen: dict[str, Path] = {}

    def fake_render_access_probe_summary(csv_path: Path) -> str:
        seen["csv_path"] = csv_path
        return "probe summary"

    csv_path = tmp_path / "access_probe.csv"
    monkeypatch.setattr(
        access_probe_summarize,
        "render_access_probe_summary",
        fake_render_access_probe_summary,
        raising=False,
    )
    monkeypatch.setattr(sys, "argv", ["access_probe_summarize.py", str(csv_path)])

    access_probe_summarize.main()

    assert seen == {"csv_path": csv_path}
    assert "probe summary" in capsys.readouterr().out
