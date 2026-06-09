"""AuditReport persistence.

The production target is PostgreSQL, but the SSRP research workflow needs a
zero-service local store first. This module therefore implements an append-only
JSONL store behind the same public functions the future DB adapter will keep.
"""

from pathlib import Path
from uuid import UUID

from pydantic import HttpUrl

from consent_audit.models import AuditReport, WeeklySummary

REPORT_STORE_PATH = Path("data") / "reports" / "audit_reports.jsonl"
WEEKLY_SUMMARY_STORE_PATH = Path("data") / "reports" / "weekly_summaries.jsonl"


def save_report(report: AuditReport) -> UUID:
    """Persist a new AuditReport row. Returns report_id."""
    REPORT_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_STORE_PATH.open("a", encoding="utf-8") as fh:
        fh.write(report.model_dump_json(ensure_ascii=True))
        fh.write("\n")
    return report.report_id


def load_report(report_id: UUID) -> AuditReport:
    for report in _iter_reports():
        if report.report_id == report_id:
            return report
    raise KeyError(f"AuditReport not found: {report_id}")


def list_reports_for_url(url: HttpUrl | str, limit: int = 50) -> list[AuditReport]:
    """Return recent reports for one URL, newest first."""
    target_url = _canonical_url(url)
    reports = [
        report
        for report in _iter_reports()
        if _canonical_url(report.bundle.url) == target_url
    ]
    reports.sort(key=lambda report: report.generated_at, reverse=True)
    return reports[:limit]


def list_reports(limit: int = 500) -> list[AuditReport]:
    """Return recent reports across all URLs, newest first."""
    reports = _iter_reports()
    reports.sort(key=lambda report: report.generated_at, reverse=True)
    return reports[:limit]


def save_weekly_summary(summary: WeeklySummary) -> None:
    """Persist a new WeeklySummary row."""
    WEEKLY_SUMMARY_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with WEEKLY_SUMMARY_STORE_PATH.open("a", encoding="utf-8") as fh:
        fh.write(summary.model_dump_json(ensure_ascii=True))
        fh.write("\n")


def list_weekly_summaries_for_url(
    url: HttpUrl | str,
    limit: int = 50,
) -> list[WeeklySummary]:
    """Return recent weekly summaries for one URL, newest first."""
    target_url = _canonical_url(url)
    summaries = [
        summary
        for summary in _iter_weekly_summaries()
        if _canonical_url(summary.url) == target_url
    ]
    summaries.sort(key=lambda summary: summary.week_of, reverse=True)
    return summaries[:limit]


def list_weekly_summaries(limit: int = 500) -> list[WeeklySummary]:
    """Return recent weekly summaries across all URLs, newest first."""
    summaries = _iter_weekly_summaries()
    summaries.sort(key=lambda summary: summary.week_of, reverse=True)
    return summaries[:limit]


def _canonical_url(url: HttpUrl | str) -> str:
    return str(url).rstrip("/")


def _iter_reports() -> list[AuditReport]:
    if not REPORT_STORE_PATH.exists():
        return []

    reports: list[AuditReport] = []
    with REPORT_STORE_PATH.open(encoding="utf-8") as fh:
        for line in fh:
            payload = line.strip()
            if not payload:
                continue
            reports.append(AuditReport.model_validate_json(payload))
    return reports


def _iter_weekly_summaries() -> list[WeeklySummary]:
    if not WEEKLY_SUMMARY_STORE_PATH.exists():
        return []

    summaries: list[WeeklySummary] = []
    with WEEKLY_SUMMARY_STORE_PATH.open(encoding="utf-8") as fh:
        for line in fh:
            payload = line.strip()
            if not payload:
                continue
            summaries.append(WeeklySummary.model_validate_json(payload))
    return summaries
