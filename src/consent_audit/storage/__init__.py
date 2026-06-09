"""Storage adapters. Side-effect-only — no business logic."""

from consent_audit.storage.db import (
    list_reports,
    list_reports_for_url,
    list_weekly_summaries,
    list_weekly_summaries_for_url,
    load_report,
    save_report,
    save_weekly_summary,
)
from consent_audit.storage.object_store import upload_dom_snapshot, upload_screenshot

__all__ = [
    "list_reports",
    "list_reports_for_url",
    "list_weekly_summaries",
    "list_weekly_summaries_for_url",
    "load_report",
    "save_report",
    "save_weekly_summary",
    "upload_dom_snapshot",
    "upload_screenshot",
]
