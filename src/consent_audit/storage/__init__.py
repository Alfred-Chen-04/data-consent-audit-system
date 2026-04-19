"""Storage adapters. Side-effect-only — no business logic."""

from consent_audit.storage.db import save_report, load_report, list_reports_for_url
from consent_audit.storage.object_store import upload_screenshot, upload_dom_snapshot

__all__ = [
    "list_reports_for_url",
    "load_report",
    "save_report",
    "upload_dom_snapshot",
    "upload_screenshot",
]
