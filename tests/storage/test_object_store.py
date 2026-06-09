"""Tests for local object-store fallback behavior."""

from pathlib import Path

import pytest
from PIL import Image

from consent_audit.storage import object_store


def test_upload_screenshot_sanitizes_and_copies_to_local_store(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    store_root = tmp_path / "object_store"
    monkeypatch.setattr(object_store, "LOCAL_OBJECT_STORE_ROOT", store_root, raising=False)
    source = tmp_path / "source.png"
    Image.new("RGB", (8, 6), "red").save(source)

    uploaded = object_store.upload_screenshot(source, key="screenshots/site/layer1.png")

    uploaded_path = Path(uploaded)
    assert uploaded_path == store_root / "screenshots/site/layer1.png"
    assert uploaded_path.exists()
    assert source.with_name("source.sanitized.png").exists()


def test_upload_dom_snapshot_copies_to_local_store(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    store_root = tmp_path / "object_store"
    monkeypatch.setattr(object_store, "LOCAL_OBJECT_STORE_ROOT", store_root, raising=False)
    source = tmp_path / "layer1.html"
    source.write_text("<html><body>Consent</body></html>", encoding="utf-8")

    uploaded = object_store.upload_dom_snapshot(source, key="dom/site/layer1.html")

    uploaded_path = Path(uploaded)
    assert uploaded_path == store_root / "dom/site/layer1.html"
    assert uploaded_path.read_text(encoding="utf-8") == "<html><body>Consent</body></html>"


def test_object_store_rejects_path_traversal_keys(tmp_path: Path) -> None:
    source = tmp_path / "layer1.html"
    source.write_text("<html></html>", encoding="utf-8")

    with pytest.raises(ValueError, match="safe relative path"):
        object_store.upload_dom_snapshot(source, key="../layer1.html")
