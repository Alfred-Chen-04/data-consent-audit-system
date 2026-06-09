"""Audit orchestration shared by CLI and script entrypoints."""

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import structlog

from consent_audit.capture import capture_site
from consent_audit.config import settings
from consent_audit.consent_table import append_row_to_csv, row_from_bundle
from consent_audit.diff import detect_changes, summarize_week
from consent_audit.layers import score_layer1, score_layer2, score_layer3
from consent_audit.llm.budget import BudgetExceeded, BudgetLedger
from consent_audit.models import (
    AuditReport,
    CaptureBundle,
    Layer1Result,
    Layer2Result,
    Layer3Result,
)
from consent_audit.report import generate_report
from consent_audit.site_list import validate_site_list
from consent_audit.storage import list_reports_for_url, save_report, save_weekly_summary

log = structlog.get_logger()


@dataclass(frozen=True)
class WeeklySiteFailure:
    url: str
    error: str


@dataclass(frozen=True)
class WeeklyRunSummary:
    target_count: int
    attempted_count: int
    succeeded_count: int
    failed_count: int
    failures: list[WeeklySiteFailure]
    budget_exceeded: bool = False


def format_weekly_run_summary(summary: WeeklyRunSummary) -> str:
    budget_exceeded = str(summary.budget_exceeded).lower()
    text = (
        "Completed weekly audit "
        f"(attempted={summary.attempted_count}/{summary.target_count}, "
        f"succeeded={summary.succeeded_count}, "
        f"failed={summary.failed_count}, "
        f"budget_exceeded={budget_exceeded})"
    )
    if not summary.failures:
        return text

    failure_lines = "\n".join(
        f"- {failure.url}: {failure.error}" for failure in summary.failures
    )
    return f"{text}\nFailures:\n{failure_lines}"


async def run_single_site_audit(
    url: str,
    *,
    save: bool,
    consent_table_path: Path | None = None,
    cohort: str = "",
) -> AuditReport:
    ledger = BudgetLedger(cap_usd=settings.ssrp_budget_cap)

    bundle = await capture_site(url, timeout_seconds=settings.agent_site_timeout)  # type: ignore[arg-type]
    l1 = score_layer1(bundle)
    l2 = score_layer2(bundle, l1) if l1.gate_passed else None
    l3 = _score_layer3_or_none(bundle, l1, l2)

    report = generate_report(bundle, l1, l2, l3, api_cost_usd=ledger.spent_usd)

    if consent_table_path is not None:
        append_row_to_csv(
            consent_table_path,
            row_from_bundle(
                bundle,
                l1,
                layer2=l2,
                layer3=l3,
                tier=report.tier,
                cohort=cohort,
                notes="; ".join(bundle.capture_warnings),
            ),
        )

    if save:
        save_report(report)
    return report


async def run_weekly_audit(
    sites_csv: Path,
    *,
    consent_table_path: Path | None = None,
    cohort: str = "weekly",
    limit: int | None = None,
    summary_week_of: datetime | None = None,
) -> WeeklyRunSummary:
    ledger = BudgetLedger(cap_usd=settings.ssrp_budget_cap)
    validation = validate_site_list(sites_csv)
    if validation.errors:
        issue_codes = ", ".join(issue.code for issue in validation.errors)
        raise ValueError(f"site list validation failed before weekly capture: {issue_codes}")

    urls = load_site_urls(sites_csv)
    if limit is not None:
        if limit < 0:
            raise ValueError("limit must be non-negative")
        urls = urls[:limit]
    attempted_count = 0
    succeeded_count = 0
    failures: list[WeeklySiteFailure] = []
    budget_exceeded = False

    for url in urls:
        attempted_count += 1
        try:
            await audit_weekly_site(
                url,
                ledger,
                consent_table_path=consent_table_path,
                cohort=cohort,
                summary_week_of=summary_week_of,
            )
            succeeded_count += 1
        except BudgetExceeded:
            log.error("budget_exceeded", url=url, spent=ledger.spent_usd)
            failures.append(WeeklySiteFailure(url=url, error="budget_exceeded"))
            budget_exceeded = True
            break
        except Exception as exc:
            log.error("site_failed", url=url, error=str(exc))
            failures.append(WeeklySiteFailure(url=url, error=str(exc)))
            continue

    return WeeklyRunSummary(
        target_count=len(urls),
        attempted_count=attempted_count,
        succeeded_count=succeeded_count,
        failed_count=len(failures),
        failures=failures,
        budget_exceeded=budget_exceeded,
    )


def load_site_urls(sites_csv: Path) -> list[str]:
    with sites_csv.open(encoding="utf-8") as fh:
        urls: list[str] = []
        for row in csv.DictReader(fh):
            url = (row.get("url") or "").strip()
            if not url or url.startswith("#"):
                continue
            urls.append(url)
        return urls


async def audit_weekly_site(
    url: str,
    ledger: BudgetLedger,
    *,
    consent_table_path: Path | None = None,
    cohort: str = "weekly",
    summary_week_of: datetime | None = None,
) -> AuditReport:
    bundle = await capture_site(url, timeout_seconds=settings.agent_site_timeout)  # type: ignore[arg-type]
    l1 = score_layer1(bundle)
    l2 = score_layer2(bundle, l1) if l1.gate_passed else None
    l3 = _score_layer3_or_none(bundle, l1, l2)
    report = generate_report(bundle, l1, l2, l3, api_cost_usd=ledger.spent_usd)
    storage_available = True
    try:
        save_report(report)
    except NotImplementedError:
        storage_available = False
        bundle.capture_warnings.append("Report storage is not implemented; report was not saved.")

    if consent_table_path is not None:
        append_row_to_csv(
            consent_table_path,
            row_from_bundle(
                bundle,
                l1,
                layer2=l2,
                layer3=l3,
                tier=report.tier,
                cohort=cohort,
                notes="; ".join(bundle.capture_warnings),
            ),
        )

    if not storage_available:
        return report

    history = list_reports_for_url(url, limit=2)
    if len(history) >= 2:
        events = detect_changes(history[1], history[0])
        summary = await summarize_week(url, events, ledger=ledger, week_of=summary_week_of)
        save_weekly_summary(summary)
    return report


def _score_layer3_or_none(
    bundle: CaptureBundle,
    layer1: Layer1Result,
    layer2: Layer2Result | None,
) -> Layer3Result | None:
    if layer2 is None:
        return None
    try:
        return score_layer3(bundle, layer1, layer2)
    except NotImplementedError:
        bundle.capture_warnings.append("Layer 3 scorer is not implemented; report is partial.")
        return None
