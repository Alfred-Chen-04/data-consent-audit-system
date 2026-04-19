"""Capture stage: drive a real browser, collect multimodal snapshots, fingerprint."""

from consent_audit.capture.agent import capture_site
from consent_audit.capture.fingerprint import compute_fingerprint

__all__ = ["capture_site", "compute_fingerprint"]
