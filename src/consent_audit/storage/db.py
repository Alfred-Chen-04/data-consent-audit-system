"""PostgreSQL persistence. Versioned — every capture produces a new row."""

from uuid import UUID

from pydantic import HttpUrl

from consent_audit.models import AuditReport


def save_report(report: AuditReport) -> UUID:
    """Insert a new AuditReport row. Returns report_id."""
    raise NotImplementedError("implement week 1 — schema designed after models/ stabilizes")


def load_report(report_id: UUID) -> AuditReport:
    raise NotImplementedError("implement week 1")


def list_reports_for_url(url: HttpUrl, limit: int = 50) -> list[AuditReport]:
    """Chronological list for longitudinal view on the demo site."""
    raise NotImplementedError("implement week 8 — demo site timeline view")
