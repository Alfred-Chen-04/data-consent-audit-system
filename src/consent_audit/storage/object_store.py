"""S3-compatible object storage for screenshots and DOM snapshots.

All uploads pass through capture.sanitize first (AGENTS.md §8).
"""

from pathlib import Path, PurePosixPath
from shutil import copy2

from consent_audit.capture.sanitize import sanitize_screenshot

LOCAL_OBJECT_STORE_ROOT = Path("data/object_store")


def upload_screenshot(local_path: Path, *, key: str) -> str:
    """Upload a (sanitized) screenshot. Returns the object-store URL/key for later retrieval."""
    sanitized_path = sanitize_screenshot(local_path)
    return _copy_to_local_store(sanitized_path, key=key)


def upload_dom_snapshot(local_path: Path, *, key: str) -> str:
    return _copy_to_local_store(local_path, key=key)


def _copy_to_local_store(local_path: Path, *, key: str) -> str:
    safe_key = _safe_key(key)
    destination = LOCAL_OBJECT_STORE_ROOT / Path(*safe_key.parts)
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy2(local_path, destination)
    return str(destination)


def _safe_key(key: str) -> PurePosixPath:
    normalized = key.strip().replace("\\", "/").lstrip("/")
    path = PurePosixPath(normalized)
    if not normalized or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("object-store key must be a safe relative path")
    return path
