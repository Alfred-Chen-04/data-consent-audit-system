"""Tests for weekly pipeline partial audit behavior."""

import csv
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from typer.testing import CliRunner

from consent_audit import pipeline
from consent_audit.llm.budget import BudgetLedger
from consent_audit.models import (
    AuditReport,
    CaptureBundle,
    ElementRef,
    EventLogRef,
    Layer1Result,
    LayerSnapshot,
    MultimodalFingerprint,
    PathOutcome,
    Pathway,
    Tier,
)
from consent_audit.pipeline import WeeklyRunSummary, WeeklySiteFailure
from consent_audit.storage import db
from scripts import run_weekly

runner = CliRunner()


def _element(pathway: Pathway) -> ElementRef:
    return ElementRef(
        dom_selector=f"button.{pathway.value}",
        visible_text=pathway.value.title(),
    )


def _bundle(
    url: str = "https://example.com",
    *,
    visible_text: str = "",
) -> CaptureBundle:
    return CaptureBundle(
        url=url,  # type: ignore[arg-type]
        captured_at=datetime.now(UTC),
        layers=[
            LayerSnapshot(
                layer_index=1,
                screenshot_ref="captures/example/layer1.png",
                dom_snapshot_ref="captures/example/layer1.html",
                visible_text=visible_text,
            )
        ]
        if visible_text
        else [],
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
async def test_audit_one_writes_consent_table_even_when_layer3_and_storage_are_unimplemented(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    async def fake_capture_site(url: str, *, timeout_seconds: int) -> CaptureBundle:
        _ = timeout_seconds
        return _bundle(url)

    def fake_score_layer3(*args: Any, **kwargs: Any) -> None:
        _ = (args, kwargs)
        raise NotImplementedError("Layer 3 not implemented")

    def fake_save_report(*args: Any, **kwargs: Any) -> None:
        _ = (args, kwargs)
        raise NotImplementedError("storage not implemented")

    monkeypatch.setattr(pipeline, "capture_site", fake_capture_site)
    monkeypatch.setattr(pipeline, "score_layer3", fake_score_layer3)
    monkeypatch.setattr(pipeline, "save_report", fake_save_report)
    out_csv = tmp_path / "weekly_consent_table.csv"

    await pipeline.audit_weekly_site(
        "https://example.com",
        BudgetLedger(cap_usd=10.0),
        consent_table_path=out_csv,
        cohort="weekly_smoke",
    )

    with out_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    assert len(rows) == 1
    assert rows[0]["url"] == "https://example.com/"
    assert rows[0]["cohort"] == "weekly_smoke"
    assert "Layer 3 scorer is not implemented" in rows[0]["notes"]
    assert "Report storage is not implemented" in rows[0]["notes"]


@pytest.mark.asyncio
async def test_run_skips_blank_and_comment_site_rows(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    seen_urls: list[str] = []

    async def fake_audit_one(
        url: str,
        ledger: BudgetLedger,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        summary_week_of: datetime | None = None,
    ) -> None:
        _ = (ledger, consent_table_path, cohort, summary_week_of)
        seen_urls.append(url)

    monkeypatch.setattr(pipeline, "audit_weekly_site", fake_audit_one)
    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name\n"
        "# Replace this row later,Comment\n"
        "\n"
        "https://valid.example,Example\n",
        encoding="utf-8",
    )

    summary = await pipeline.run_weekly_audit(sites_csv)

    assert seen_urls == ["https://valid.example"]
    assert summary.target_count == 1
    assert summary.attempted_count == 1
    assert summary.succeeded_count == 1
    assert summary.failed_count == 0


@pytest.mark.asyncio
async def test_run_weekly_audit_respects_limit_before_capture(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    seen_urls: list[str] = []

    async def fake_audit_one(
        url: str,
        ledger: BudgetLedger,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        summary_week_of: datetime | None = None,
    ) -> None:
        _ = (ledger, consent_table_path, cohort, summary_week_of)
        seen_urls.append(url)

    monkeypatch.setattr(pipeline, "audit_weekly_site", fake_audit_one)
    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name\n"
        "https://first.example,First\n"
        "https://second.example,Second\n"
        "https://third.example,Third\n",
        encoding="utf-8",
    )

    summary = await pipeline.run_weekly_audit(sites_csv, limit=2)

    assert seen_urls == ["https://first.example", "https://second.example"]
    assert summary.target_count == 2
    assert summary.attempted_count == 2
    assert summary.succeeded_count == 2
    assert summary.failed_count == 0


@pytest.mark.asyncio
async def test_run_weekly_audit_rejects_invalid_site_list_before_capture(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    seen_urls: list[str] = []

    async def fake_audit_one(
        url: str,
        ledger: BudgetLedger,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        summary_week_of: datetime | None = None,
    ) -> None:
        _ = (ledger, consent_table_path, cohort, summary_week_of)
        seen_urls.append(url)

    monkeypatch.setattr(pipeline, "audit_weekly_site", fake_audit_one)
    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://example.com,Example,placeholder,false,delete before real run\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="placeholder_url"):
        await pipeline.run_weekly_audit(sites_csv)

    assert seen_urls == []


@pytest.mark.asyncio
async def test_run_weekly_script_passes_limit_to_pipeline(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    seen: dict[str, Any] = {}

    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None = None,
    ) -> SimpleNamespace:
        seen["sites_csv"] = sites_csv
        seen["consent_table_path"] = consent_table_path
        seen["cohort"] = cohort
        seen["limit"] = limit
        return SimpleNamespace(
            target_count=2,
            attempted_count=2,
            succeeded_count=1,
            failed_count=1,
            budget_exceeded=True,
        )

    monkeypatch.setattr(run_weekly, "run_weekly_audit", fake_run_weekly_audit)
    sites_csv = tmp_path / "sites.csv"
    consent_table = tmp_path / "consent.csv"

    summary = await run_weekly._run(
        sites_csv,
        consent_table_path=consent_table,
        cohort="weekly_probe",
        limit=2,
    )

    assert seen == {
        "sites_csv": sites_csv,
        "consent_table_path": consent_table,
        "cohort": "weekly_probe",
        "limit": 2,
    }
    assert summary.target_count == 2
    assert summary.attempted_count == 2
    assert summary.succeeded_count == 1
    assert summary.failed_count == 1
    assert summary.budget_exceeded is True


def test_run_weekly_script_reports_site_list_validation_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    async def fake_run_weekly_audit(
        sites_csv: Path,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        limit: int | None = None,
    ) -> SimpleNamespace:
        _ = (sites_csv, consent_table_path, cohort, limit)
        raise ValueError("site list validation failed before weekly capture: placeholder_url")

    monkeypatch.setattr(run_weekly, "run_weekly_audit", fake_run_weekly_audit)
    sites_csv = tmp_path / "sites.csv"

    result = runner.invoke(run_weekly.app, ["--sites-csv", str(sites_csv)])

    assert result.exit_code == 1
    assert "site list validation failed before weekly capture: placeholder_url" in result.output


def test_format_weekly_run_summary_includes_failed_site_details() -> None:
    summary = WeeklyRunSummary(
        target_count=2,
        attempted_count=2,
        succeeded_count=1,
        failed_count=1,
        failures=[
            WeeklySiteFailure(
                url="https://broken.example",
                error="capture exploded",
            )
        ],
    )

    text = pipeline.format_weekly_run_summary(summary)

    assert "attempted=2/2" in text
    assert "failed=1" in text
    assert "Failures:" in text
    assert "- https://broken.example: capture exploded" in text


@pytest.mark.asyncio
async def test_run_weekly_audit_returns_failure_summary_and_continues(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    seen_urls: list[str] = []

    async def fake_audit_one(
        url: str,
        ledger: BudgetLedger,
        *,
        consent_table_path: Path | None = None,
        cohort: str = "weekly",
        summary_week_of: datetime | None = None,
    ) -> None:
        _ = (ledger, consent_table_path, cohort, summary_week_of)
        seen_urls.append(url)
        if "broken" in url:
            raise RuntimeError("capture exploded")

    monkeypatch.setattr(pipeline, "audit_weekly_site", fake_audit_one)
    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name\n"
        "https://first.example,First\n"
        "https://broken.example,Broken\n"
        "https://last.example,Last\n",
        encoding="utf-8",
    )

    summary = await pipeline.run_weekly_audit(
        sites_csv,
        consent_table_path=tmp_path / "consent.csv",
        cohort="week2",
    )

    assert seen_urls == [
        "https://first.example",
        "https://broken.example",
        "https://last.example",
    ]
    assert summary.target_count == 3
    assert summary.attempted_count == 3
    assert summary.succeeded_count == 2
    assert summary.failed_count == 1
    assert summary.failures[0].url == "https://broken.example"
    assert summary.failures[0].error == "capture exploded"
    assert summary.budget_exceeded is False


@pytest.mark.asyncio
async def test_audit_one_writes_full_layer3_row_and_persisted_report(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    visible_text = (
        "We use cookies and device identifiers for analytics, personalised advertising, "
        "and content measurement. We share data with advertising partners. "
        "You can accept, reject, or customize these choices at any time."
    )

    async def fake_capture_site(url: str, *, timeout_seconds: int) -> CaptureBundle:
        _ = timeout_seconds
        return _bundle(url, visible_text=visible_text)

    monkeypatch.setattr(pipeline, "capture_site", fake_capture_site)
    monkeypatch.setattr(db, "REPORT_STORE_PATH", tmp_path / "reports.jsonl")
    out_csv = tmp_path / "weekly_consent_table.csv"

    await pipeline.audit_weekly_site(
        "https://example.com",
        BudgetLedger(cap_usd=10.0),
        consent_table_path=out_csv,
        cohort="weekly_full",
    )

    with out_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    assert len(rows) == 1
    assert rows[0]["layer1_gate_passed"] == "true"
    assert rows[0]["layer2_overall_category"] == "Easy"
    assert rows[0]["transparency_grade"] == "A"
    assert rows[0]["unbiased_choice_grade"] == "A"
    assert rows[0]["tier"] == "Exemplary"
    assert rows[0]["notes"] == ""

    reports = db.list_reports_for_url("https://example.com")
    assert len(reports) == 1
    assert "### Disclosure Topic Coverage" in reports[0].report_markdown
    assert '"We share data with advertising partners."' in reports[0].report_markdown


@pytest.mark.asyncio
async def test_audit_one_persists_weekly_summary_when_second_report_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    visible_text = (
        "We use cookies and device identifiers for analytics, personalised advertising, "
        "and content measurement. We share data with advertising partners. "
        "You can accept, reject, or customize these choices at any time."
    )

    async def fake_capture_site(url: str, *, timeout_seconds: int) -> CaptureBundle:
        _ = timeout_seconds
        return _bundle(url, visible_text=visible_text)

    old_bundle = CaptureBundle(
        url="https://example.com",  # type: ignore[arg-type]
        captured_at=datetime(2026, 5, 30, tzinfo=UTC),
        layers=[
            LayerSnapshot(
                layer_index=1,
                screenshot_ref="old.png",
                dom_snapshot_ref="old.html",
                visible_text="Accept cookies only.",
            )
        ],
        path_outcomes={},
        fingerprint=MultimodalFingerprint(dom_hash="old-dom", perceptual_image_hash="old-img"),
    )
    old_layer1 = Layer1Result(
        accept_available=True,
        reject_available=False,
        customize_available=False,
        dismiss_available=False,
        missing_paths=[Pathway.REJECT, Pathway.CUSTOMIZE],
        evidence={},
        gate_passed=False,
    )
    old_report = AuditReport(
        bundle=old_bundle,
        layer1=old_layer1,
        layer2=None,
        layer3=None,
        tier=Tier.HIGH_RISK,
        report_markdown="old",
        total_api_cost_usd=0.0,
        generated_at=datetime(2026, 5, 30, tzinfo=UTC),
    )

    monkeypatch.setattr(pipeline, "capture_site", fake_capture_site)
    monkeypatch.setattr(db, "REPORT_STORE_PATH", tmp_path / "reports.jsonl")
    monkeypatch.setattr(db, "WEEKLY_SUMMARY_STORE_PATH", tmp_path / "weekly_summaries.jsonl")
    db.save_report(old_report)

    await pipeline.audit_weekly_site(
        "https://example.com",
        BudgetLedger(cap_usd=10.0),
        consent_table_path=tmp_path / "weekly_consent_table.csv",
        cohort="weekly_full",
        summary_week_of=datetime(2026, 6, 6, tzinfo=UTC),
    )

    summaries = db.list_weekly_summaries_for_url("https://example.com")

    assert len(summaries) == 1
    assert summaries[0].week_of == datetime(2026, 6, 6, tzinfo=UTC)
    assert summaries[0].severity.value == "D"
    assert {event.change_type.value for event in summaries[0].events} >= {
        "pathway_change",
        "score_change",
    }


@pytest.mark.asyncio
async def test_audit_one_persists_no_change_weekly_summary_for_stable_observation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    visible_text = (
        "We use cookies and device identifiers for analytics, personalised advertising, "
        "and content measurement. We share data with advertising partners. "
        "You can accept, reject, or customize these choices at any time."
    )

    async def fake_capture_site(url: str, *, timeout_seconds: int) -> CaptureBundle:
        _ = timeout_seconds
        return _bundle(url, visible_text=visible_text)

    old_report = AuditReport(
        bundle=_bundle("https://example.com", visible_text=visible_text),
        layer1=Layer1Result(
            accept_available=True,
            reject_available=True,
            customize_available=True,
            dismiss_available=True,
            missing_paths=[],
            evidence={},
            gate_passed=True,
        ),
        layer2=None,
        layer3=None,
        tier=Tier.COMPLIANT,
        report_markdown="old",
        total_api_cost_usd=0.0,
        generated_at=datetime(2026, 5, 30, tzinfo=UTC),
    )

    monkeypatch.setattr(pipeline, "capture_site", fake_capture_site)
    monkeypatch.setattr(pipeline, "detect_changes", lambda previous, current: [])
    monkeypatch.setattr(db, "REPORT_STORE_PATH", tmp_path / "reports.jsonl")
    monkeypatch.setattr(db, "WEEKLY_SUMMARY_STORE_PATH", tmp_path / "weekly_summaries.jsonl")
    db.save_report(old_report)

    await pipeline.audit_weekly_site(
        "https://example.com",
        BudgetLedger(cap_usd=10.0),
        consent_table_path=tmp_path / "weekly_consent_table.csv",
        cohort="weekly_full",
    )

    summaries = db.list_weekly_summaries_for_url("https://example.com")

    assert len(summaries) == 1
    assert summaries[0].events == []
    assert summaries[0].severity.value == "A"
    assert summaries[0].summary == "No detected consent-interface changes for this observation window."
