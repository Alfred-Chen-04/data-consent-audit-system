"""Local integration test for browser capture against a static consent page."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from pydantic import HttpUrl, TypeAdapter

from consent_audit.capture import capture_site
from consent_audit.capture.agent import (
    CandidateElement,
    _attempt_pathway_clicks,
    _click_candidate_in_any_frame,
    _collect_candidates,
)
from consent_audit.layers import score_layer1
from consent_audit.models import Pathway


@pytest.mark.asyncio
async def test_capture_site_builds_bundle_from_local_consent_page(tmp_path: Path) -> None:
    html = """
    <!doctype html>
    <html>
      <body>
        <section id="cookie-banner">
          <p>We use cookies for analytics and advertising.</p>
          <button>Accept All</button>
          <button>Reject All</button>
          <button>Cookie Settings</button>
          <button aria-label="Close">Close</button>
        </section>
      </body>
    </html>
    """
    (tmp_path / "index.html").write_text(html, encoding="utf-8")

    handler = partial(SimpleHTTPRequestHandler, directory=str(tmp_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = TypeAdapter(HttpUrl).validate_python(
            f"http://127.0.0.1:{server.server_port}/index.html"
        )

        bundle = await capture_site(url, timeout_seconds=15)
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert bundle.layers
    assert Path(bundle.layers[0].screenshot_ref).exists()
    assert Path(bundle.layers[0].dom_snapshot_ref).exists()
    assert "We use cookies" in bundle.layers[0].visible_text
    assert set(bundle.path_outcomes) == set(Pathway)
    assert len(bundle.event_log) == 4

    layer1 = score_layer1(bundle)
    assert layer1.gate_passed
    assert layer1.accept_available
    assert layer1.reject_available
    assert layer1.customize_available
    assert layer1.dismiss_available


@pytest.mark.asyncio
async def test_capture_site_builds_bundle_from_iframe_consent_page(tmp_path: Path) -> None:
    index_html = """
    <!doctype html>
    <html>
      <body>
        <main>
          <h1>News front page</h1>
          <iframe src="/consent.html" title="Privacy choices"></iframe>
        </main>
      </body>
    </html>
    """
    consent_html = """
    <!doctype html>
    <html>
      <body>
        <section id="cookie-banner">
          <p>We use cookies for analytics and advertising.</p>
          <button>Accept All</button>
          <button>Reject All</button>
          <button>Cookie Settings</button>
          <button aria-label="Close">Close</button>
        </section>
      </body>
    </html>
    """
    (tmp_path / "index.html").write_text(index_html, encoding="utf-8")
    (tmp_path / "consent.html").write_text(consent_html, encoding="utf-8")

    handler = partial(SimpleHTTPRequestHandler, directory=str(tmp_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = TypeAdapter(HttpUrl).validate_python(
            f"http://127.0.0.1:{server.server_port}/index.html"
        )

        bundle = await capture_site(url, timeout_seconds=15)
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    layer1 = score_layer1(bundle)
    assert layer1.gate_passed
    assert layer1.accept_available
    assert layer1.reject_available
    assert layer1.customize_available


@pytest.mark.asyncio
async def test_collect_candidates_keeps_nested_iframe_buttons_with_dialog_context(
    tmp_path: Path,
) -> None:
    index_html = """
    <!doctype html>
    <html>
      <body>
        <iframe
          src="/privacy-manager.html"
          title="Privacy manager"
          style="width: 1440px; height: 900px"
        ></iframe>
      </body>
    </html>
    """
    privacy_manager_html = """
    <!doctype html>
    <html>
      <body>
        <div role="dialog" aria-label="privacy manager">
          <h1>Manage Cookie Settings</h1>
          <p>We use cookies and personal data for advertising partners.</p>
          <div class="purpose-stack">
            <div class="purpose-row">
              <span>International transfer</span>
              <div class="button-shell"><button>Accept</button></div>
            </div>
            <div class="purpose-row">
              <span>Functional Technology</span>
              <div class="button-shell">
                <button>Accept</button>
                <button>Reject</button>
              </div>
            </div>
          </div>
          <button aria-label="Save my choices">Save my choices</button>
        </div>
      </body>
    </html>
    """
    (tmp_path / "index.html").write_text(index_html, encoding="utf-8")
    (tmp_path / "privacy-manager.html").write_text(
        privacy_manager_html,
        encoding="utf-8",
    )

    handler = partial(SimpleHTTPRequestHandler, directory=str(tmp_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context(
                locale="en-US",
                viewport={"width": 1440, "height": 900},
            )
            page = await context.new_page()
            await page.goto(
                f"http://127.0.0.1:{server.server_port}/index.html",
                wait_until="domcontentloaded",
                timeout=15_000,
            )

            candidates = await _collect_candidates(page)

            await context.close()
            await browser.close()
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    labels = [candidate.visible_text for candidate in candidates]
    assert "Accept" in labels
    assert "Reject" in labels
    assert all("Manage Cookie Settings" not in label for label in labels)


@pytest.mark.asyncio
async def test_click_candidate_tries_visible_duplicate_text_matches(tmp_path: Path) -> None:
    html = """
    <!doctype html>
    <html>
      <body>
        <button style="display: none">Reject</button>
        <button onclick="document.body.dataset.clicked = 'reject'">Reject</button>
      </body>
    </html>
    """
    (tmp_path / "index.html").write_text(html, encoding="utf-8")

    handler = partial(SimpleHTTPRequestHandler, directory=str(tmp_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context(
                locale="en-US",
                viewport={"width": 1440, "height": 900},
            )
            page = await context.new_page()
            await page.goto(
                f"http://127.0.0.1:{server.server_port}/index.html",
                wait_until="domcontentloaded",
                timeout=15_000,
            )

            clicked = await _click_candidate_in_any_frame(page, "Reject")
            marker = await page.evaluate("() => document.body.dataset.clicked || ''")

            await context.close()
            await browser.close()
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert clicked
    assert marker == "reject"


@pytest.mark.asyncio
async def test_click_candidate_uses_accessible_button_name(tmp_path: Path) -> None:
    html = """
    <!doctype html>
    <html>
      <body>
        <button
          aria-label="Close preference center"
          onclick="document.body.dataset.clicked = 'close'"
        >X</button>
      </body>
    </html>
    """
    (tmp_path / "index.html").write_text(html, encoding="utf-8")

    handler = partial(SimpleHTTPRequestHandler, directory=str(tmp_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context(
                locale="en-US",
                viewport={"width": 1440, "height": 900},
            )
            page = await context.new_page()
            await page.goto(
                f"http://127.0.0.1:{server.server_port}/index.html",
                wait_until="domcontentloaded",
                timeout=15_000,
            )

            clicked = await _click_candidate_in_any_frame(page, "Close preference center")
            marker = await page.evaluate("() => document.body.dataset.clicked || ''")

            await context.close()
            await browser.close()
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert clicked
    assert marker == "close"


@pytest.mark.asyncio
async def test_attempt_pathway_clicks_waits_for_delayed_cmp_controls(tmp_path: Path) -> None:
    html = """
    <!doctype html>
    <html>
      <body>
        <main>Brand page</main>
        <script>
          setTimeout(() => {
            const panel = document.createElement('section');
            panel.id = 'onetrust-consent-sdk';
            panel.innerHTML = `
              <p>Privacy Preference Center: we use cookies for advertising.</p>
              <button aria-label="Close preference center">X</button>
              <button>Allow All</button>
              <button>Confirm My Choices</button>
              <button>Reject All</button>
            `;
            document.body.appendChild(panel);
          }, 1800);
        </script>
      </body>
    </html>
    """
    (tmp_path / "index.html").write_text(html, encoding="utf-8")

    handler = partial(SimpleHTTPRequestHandler, directory=str(tmp_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            candidates = [
                CandidateElement(
                    selector="button.close",
                    visible_text="Close preference center",
                ),
                CandidateElement(selector="button.accept", visible_text="Allow All"),
                CandidateElement(
                    selector="button.customize",
                    visible_text="Confirm My Choices",
                ),
                CandidateElement(selector="button.reject", visible_text="Reject All"),
            ]

            succeeded = await _attempt_pathway_clicks(
                browser,
                f"http://127.0.0.1:{server.server_port}/index.html",
                candidates,
                15_000,
            )

            await browser.close()
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert succeeded == {
        Pathway.ACCEPT,
        Pathway.REJECT,
        Pathway.CUSTOMIZE,
        Pathway.DISMISS,
    }
