"""Longitudinal diff engine. Consumes two consecutive reports, emits ChangeEvents."""

from consent_audit.diff.engine import detect_changes, summarize_week

__all__ = ["detect_changes", "summarize_week"]
