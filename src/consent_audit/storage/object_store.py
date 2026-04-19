"""S3-compatible object storage for screenshots and DOM snapshots.

All uploads pass through capture.sanitize first (AGENTS.md §8).
"""

from pathlib import Path


def upload_screenshot(local_path: Path, *, key: str) -> str:
    """Upload a (sanitized) screenshot. Returns the object-store URL/key for later retrieval."""
    raise NotImplementedError("implement week 1")


def upload_dom_snapshot(local_path: Path, *, key: str) -> str:
    raise NotImplementedError("implement week 1")
