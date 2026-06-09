"""Tests for partial single-site audit orchestration."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from consent_audit import pipeline
from consent_audit.models import (
    CaptureBundle,
    ElementRef,
    EventLogRef,
    MultimodalFingerprint,
    PathOutcome,
    Pathway,
)
from scripts import run_audit


def _element(pathway: Pathway) -> ElementRef:
    return ElementRef(
        dom_selector=f"button.{pathway.value}",
        visible_text=pathway.value.title(),
    )


def _bundle() -> CaptureBundle:
    return CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime.now(UTC),
        layers=[],
        path_outcomes={
            pathway: PathOutcome(
                pathway=pathway,
                attempted=True,
                succeeded=True,
                click_depth=1,
                trigger_element=_element(pathway),
            )
            for pathway in Pathway
        },
        fingerprint=MultimodalFingerprint(dom_hash="dom", perceptual_image_hash="img"),
        event_log=[
            EventLogRef(
                event_index=index,
                action=f"click_{pathway.value}",
                target=_element(pathway),
                outcome="success",
            )
            for index, pathway in enumerate(Pathway)
        ],
    )


@pytest.mark.asyncio
async def test_run_audit_prints_partial_report_when_layer3_is_unimplemented(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    async def fake_capture_site(url: str, *, timeout_seconds: int) -> CaptureBundle:
        _ = (url, timeout_seconds)
        return _bundle()

    def fake_score_layer3(*args: Any, **kwargs: Any) -> None:
        _ = (args, kwargs)
        raise NotImplementedError("Layer 3 not implemented")

    monkeypatch.setattr(pipeline, "capture_site", fake_capture_site)
    monkeypatch.setattr(pipeline, "score_layer3", fake_score_layer3)

    await run_audit._run("https://example.com", save=False)

    captured = capsys.readouterr()
    assert "Layer 1" in captured.out
    assert "Layer 2" in captured.out
    assert "Layer 3 not implemented" not in captured.out


@pytest.mark.asyncio
async def test_run_audit_can_append_consent_table_row(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    async def fake_capture_site(url: str, *, timeout_seconds: int) -> CaptureBundle:
        _ = (url, timeout_seconds)
        return _bundle()

    def fake_score_layer3(*args: Any, **kwargs: Any) -> None:
        _ = (args, kwargs)
        raise NotImplementedError("Layer 3 not implemented")

    monkeypatch.setattr(pipeline, "capture_site", fake_capture_site)
    monkeypatch.setattr(pipeline, "score_layer3", fake_score_layer3)
    out_csv = tmp_path / "consent_table.csv"

    await run_audit._run(
        "https://example.com",
        save=False,
        consent_table_path=out_csv,
        cohort="smoke",
    )

    contents = out_csv.read_text(encoding="utf-8")
    assert "https://example.com/" in contents
    assert "smoke" in contents
    assert "Layer 3 scorer is not implemented" in contents
